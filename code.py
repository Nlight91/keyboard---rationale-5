import board
import digitalio
import time

import adafruit_ble as able
#from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.Keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl

import scancodes 
from setup import setup

import gc

POLLING_RATE = 500 # expressed in hz


class MainLogic:
    def __init__(s, matrix:Kbd_Matrix, layers:Layers, ble_keyboard:Keyboard, ble_consumer_control:ConsumerControl):
        s.ble_keyboard = ble_keyboard
        s.ble_consumer_control = ble_consumer_control
        s.matrix = matrix
        s.layers:Layers = layers
        s.awaiting_physical_release = set()
    
    def _get_type_and_vcode(s, key_index:int):
        string = s.layers[key_index]
        assert ":" in string
        colon_index = string.index(":")
        return string[:colon_index], string[colon_index+1:]

    def __call__(s):
        new_released, new_pressed, still_pressed = s.matrix.get_report()

        # holds every methods `press` and `depress` of each <LayerFunc> that are
        # pressed and depressed in the matrix report
        switches_method = [] 

        # keyboard logic
        ## release logic
        keys = []
        for key_index in new_released :
            if key_index in s.awaiting_physical_release :
                s.awaiting_physical_release.difference_update({key_index})
                continue
            key_string = s.layers[key_index]
            key_type, key_vcode = s._get_type_and_vcode(key_index)
            #if key == "no:TRANS" or key_tp == "cc" : continue
            if key_string == "no:TRANS" : continue
            elif key_type == "sw" :
                for sp_idx in still_pressed :
                    sp_type, sp_vcode = s._get_type_and_vcode(sp_idx)
                    if sp_type == "cc" : continue
                    keys.append(scancodes.get_hid_usage_id(sp_type, sp_vcode))
                    s.awaiting_physical_release.update({sp_idx})
                switches_method.append(s.layers.switches[key_vcode].depress)
            else :
                if key_type == "cc" : queue = consumer_keys
                else : queue = keys
                queue.append( scancodes.get_hid_usage_id(key_type, key_vcode) )
        s.ble_keyboard.release( *keys )

        ## press logic
        queue = []
        for key_index in new_pressed :
            key_type, key_vcode = s._get_type_and_vcode(key_index)
            if key_type == "sw" :
                s.force_release_still_pressed_keys( still_pressed )
                switches_method.append( s.layers.switches[key_vcode].press )
            else : 
                queue.append( key_index )

        # first de/activate various <Switch> to set all the right layers on/off
        for func in switches_method : func()

        # now that new switches are pressed, complete press logic
        keyboard_keys = []
        consumer_keys = []
        for key_index in queue :
            key_type, key_vcode = s._get_type_and_vcode( key_index )
            if (key_type, key_vcode) == ("no", "TRANS") : continue
            elif key_type == "cc" :
                consumer_keys.append( (key_index, scancodes.get_hid_usage_id(key_type, key_vcode)) )
            else :
                keyboard_keys.append( scancodes.get_hid_usage_id(key_type, key_vcode) )
        
        for key_index, hid_uid in consumer_keys:
            s.ble_consumer_control.send( hid_uid )
            s.awaiting_physical_release.update({key_index})
        s.ble_keyboard.press( *keyboard_keys )
        gc.collect()

    def force_release_still_pressed_keys(s, still_pressed):
        keyboard_keys = []
        consumer_keys = []
        for key_idx in still_pressed :
            key_type, key_vcode = s._get_type_and_vcode(key_idx)
            if key_type == "cc" : continue
            keyboard_keys.append( scancodes.get_hid_usage_id( key_type, key_vcode ) )
            s.awaiting_physical_release.update({key_idx})
        s.ble_keyboard.release(*keyboard_keys)
    

def main_loop(layout, matrix):
    poll_rate_interval = 1. / POLLING_RATE

    # setting up of bluetooth
    hid = HIDService()
    advertisement = ProvideServicesAdvertisement(hid)
    advertisement.appearance = 961
    ble = able.BLERadio()
    if ble.connected :
        for c in ble.connections :
            c.disconnect()
    ble.start_advertising(advertisement)
    advertising = True
    devices = hid.devices
    ble_keyboard = Keyboard(devices)
    print("keyboard device found")
    ble_consumer_control = ConsumerControl(devices)
    print("consumer control found")

    main_logic = MainLogic(matrix, layout, ble_keyboard, ble_consumer_control)
    STATUS_CONNECTED = False

    # main logic
    while 1:
        if ble.connected :
            if not STATUS_CONNECTED :
                print("Connected, sleep 2 sec")
                time.sleep(2)
                advertising = False
                STATUS_CONNECTED = True
            while ble.connected :
                main_logic()
                time.sleep(poll_rate_interval)
        elif not ble.connected and not advertising :
            ble.start_advertising(advertisement)
            advertising = True
            STATUS_CONNECTED = False
        time.sleep(0.5)

if __name__ == '__main__':
    with open("config.json", "r") as file:
        matrix, layer_manager = setup(file.read())
    main_loop(layer_manager, matrix)