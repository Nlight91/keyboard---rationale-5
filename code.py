import board
import digitalio
import time
import usb_hid

import adafruit_ble as able
#from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.Keyboard import Keyboard
import layers as lyr
from layers import Layers
from scancodes import Scancodes as _
from matrix import Kbd_Matrix

import gc


matrix = Kbd_Matrix(
    ("D13", "D12", "D11", "D10", "D9"),
    ("A0", "A1", "A2", "A3", "A4", "A5", "SCK", "MOSI", "MISO", "D2", "RX", "TX", "SDA", "SCL", "D7" ),
    pullup = False
) #TODO : set row and col pins
layout = Layers((15,5))

# let's create the key functions that allows the switching to other layers
KPAD_MO = layout.MOMENTARY("keypad", restore=False)
KPAD_TO = layout.TOGGLE("keypad", restore=False)
NAV = layout.MOKEY("navigation", _.SPACE,  restore=False, timing=0.08)
GR_SPACE = layout.MODKEY(_.R_ALT, _.SPACE, timing=0.08)
KRAK = layout.TOGGLE("kraken", restore=False)

layout.set_default_layer((
    _.ESC,       _.NUM_1,    _.NUM_2, _.NUM_3, _.NUM_4, _.NUM_5, _.NUM_6, _.NUM_7,  _.NUM_8, _.NUM_9,         _.NUM_0,  _.MINUS,         _.EQUALS,    _.BACKSLASH, _.DELETE,
    _.TAB,       None,       _.Q,     _.W,     _.E,     _.R,     _.T,     _.Y,      _.U,     _.I,             _.O,      _.P,             _.L_BRACKET, _.R_BRACKET, _.BACKSPACE,
    _.CAPS_LOCK, None,       _.A,     _.S,     _.D,     _.F,     _.G,     _.H,      _.J,     _.K,             _.L,      _.SEMICOLON,     _.QUOTE,     None,        _.ENTER,
    _.L_SHIFT,   None,       _.Z,     _.X,     _.C,     _.V,     _.B,     _.N,      _.M,     _.COMMA,         _.PERIOD, _.FORWARD_SLASH, None,        _.R_SHIFT,   KPAD_TO,
    _.L_CTRL,    _.L_CTRL,   _.WIN,   _.L_ALT, KPAD_MO, NAV,     None,    GR_SPACE, _.R_ALT, _.FORWARD_SLASH, KRAK,     None,            None,        None,        None
))

layout.add_layer(
    "keypad",(
    _.TRANS, _.F1,    _.F2,    _.F3,    _.F4,    _.F5,    _.F6,    _.F7,     _.F8,        _.F9,    _.F10,   _.F11,       _.F12,    _.TRANS,    _.TRANS,
    _.TRANS, None,    None,    None,    None,    None,    None,    _.KP_MIN, _.KP_7 ,     _.KP_8 , _.KP_9 , None,        None,     _.TRANS,    _.TRANS,
    _.TRANS, None,    None,    None,    None,    None,    None,    _.KP_ADD, _.KP_4 ,     _.KP_5 , _.KP_6 , _.KP_MUL,    None,     None,       _.TRANS,
    _.TRANS, None,    None,    None,    None,    None,    None,    _.KP_DIV, _.KP_1 ,     _.KP_2 , _.KP_3 , None,        None,     _.KP_ENTER, _.TRANS,
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.SPACE, None,    _.KP_0,   _.KP_PERIOD, _.TRANS, _.TRANS, _.TRANS,     None,     _.TRANS,    _.TRANS
))

layout.add_layer(
    "navigation",(
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS,     _.TRANS,     _.TRANS,     _.TRANS,  _.TRANS, _.TRANS, _.TRANS, _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.HOME,      _.PAGE_DOWN, _.PAGE_UP,   _.END  ,  _.TRANS, _.TRANS, _.TRANS, _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.LEFT,      _.DOWN ,     _.UP   ,     _.RIGHT,  _.TRANS, _.TRANS, None,    _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.BACKSPACE, _.TRANS,     _.TRANS,     _.DELETE, _.TRANS, None,    _.TRANS, _.TRANS,
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, None,    _.TRANS,     _.TRANS,     _.TRANS,     _.TRANS,  _.TRANS, None,    _.TRANS, _.TRANS
))

layout.add_layer(
    "kraken",(
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS,   _.TRANS, _.TRANS,  _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS,   _.TRANS, _.TRANS,  _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS,   _.TRANS,    None,  _.TRANS,
    _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.PAGE_UP, _.TRANS,    _.UP,  _.PAGE_DOWN,
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, None,    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.LEFT,    _.TRANS,  _.DOWN,  _.RIGHT
))


def main_loop(layout, matrix):
    # NOTE : there may be a problem when release_all() is triggered :
    # indeed, while keys are realease to the host,
    # these changes are not reflected in the matrix state.
    hid = HIDService()
    advertisement = ProvideServicesAdvertisement(hid)
    advertisement.appearance = 961
    ble = able.BLERadio()
    if ble.connected :
        for c in ble.connections :
            c.disconnect()
    ble.start_advertising(advertisement)
    advertising = True
    ble_keyboard = Keyboard(hid.devices)

    def release_old_pressed_keys(old_pressed):
        ble_keyboard.release(*(layout[idx] for idx in old_pressed))

    #(deprecated ?) old_state = (1<<matrix.length)-1
    print("success")
    while 1:
        # ...
        if ble.connected :
            advertising = False
            new_released, new_pressed, old_pressed = matrix.get_report()
            keys = []
            layers = []
            repress = False
            for key in (layout[idx] for idx in new_released):
                if key not in (None, _.TRANS) :
                    if callable(key): # if key function
                        if (type(key) is lyr.MOMENTARY ) or \
                            (type(key) is lyr.MOTO and key.beyond_timing()) or \
                            (type(key) is lyr.MOKEY and key.beyond_timing()):
                            keys.extend(layout[idx] for idx in old_pressed)
                            repress = True
                        elif (type(key) is lyr.MOKEY and not key.beyond_timing()):
                            release_old_pressed_keys(old_pressed)
                            ble_keyboard.press(key.key)
                            keys.append(key.key)
                        elif (type(key) is lyr.MODKEY):
                            if not key.beyond_timing():
                                ble_keyboard.release(key.mod)
                                ble_keyboard.press(key.key)
                                keys.append(key.key)
                            else :
                                keys.append(key.mod)
                        layers.append(key.depress)
                    elif type(key) is int:
                        keys.append(key)
            ble_keyboard.release(*keys)
            keys = []
            for key in (layout[idx] for idx in new_pressed):
                if key not in (None, _.TRANS) :
                    if callable(key):
                        if type(key) is lyr.MODKEY :
                            keys.append(key.mod)
                            release_old_pressed_keys(old_pressed)
                        elif type(key) is lyr.MOKEY:
                            release_old_pressed_keys(old_pressed)
                        elif not repress:
                            repress = True
                            release_old_pressed_keys(old_pressed)
                        layers.append(key.press)
                    elif type(key) is int:
                        if layout.tapped() :
                            ble_keyboard.press(key)
                            layout.untap()
                        else :
                            keys.append(key)
            for func in layers : func()
            if repress :
                keys.extend(layout[idx] for idx in old_pressed)
            ble_keyboard.press(*keys)
            gc.collect()

        elif not ble.connected and not advertising :
            ble.start_advertising(advertisement)
            advertising = True
        time.sleep(0.002)

if __name__ == '__main__':
    main_loop(layout, matrix)
