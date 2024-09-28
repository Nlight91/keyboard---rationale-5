import board
import digitalio
import time

import adafruit_ble as able
#from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.Keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
import layers as lyr
from layers import Layers
from scancodes import Scancodes as _
from matrix import Kbd_Matrix
#from light import Led

import gc

POLLING_RATE = 500 # expressed in hz

# Let's set up the matrix of our board, reflecting the physical layout we made
matrix = Kbd_Matrix(
    ("D13", "D12", "D11", "D10", "D9"),
    ("A0", "A1", "A2", "A3", "A4", "A5", "SCK", "MOSI", "MISO", "D2", "RX", "TX", "SDA", "SCL", "D7" ),
    pullup = False
)

# Let's create the object that will hold all the layers with key scancodes
layout = Layers((15,5))

# let's create the key functions that allows the switching to other layers
KPAD_MO = layout.MOMENTARY("keypad", restore=False)
KPAD_TO = layout.TOGGLE("keypad", restore=False)
#NAV = layout.MOKEY("navigation", _.SPACE,  restore=False, timing=0.05)
NAV = layout.MOMENTARY("navigation", restore=False)
MEDIA = layout.MOMENTARY("media", restore=False)
GAME0 = layout.TOGGLE("game0", restore=False)
# Here is an example usage of MODKEY :
#
#    GR_SPACE = layout.MODKEY(_.R_ALT, _.SPACE, timing=0.08)
#
# as you can see for this function, there is no need for layer name, because
# this function switches to none, however the first value must be the scancode
# of a modifier

# here we create the layers with the key scancodes or internal key special functions like switching layer
layout.set_default_layer((
    _.ESC,       _.NUM_1,  _.NUM_2, _.NUM_3, _.NUM_4, _.NUM_5, _.NUM_6, _.NUM_7, _.NUM_8, _.NUM_9,         _.NUM_0,  _.MINUS,         _.EQUALS,    _.BACKSLASH, _.DELETE,
    _.TAB,       _.NOKEY,  _.Q,     _.W,     _.E,     _.R,     _.T,     _.Y,     _.U,     _.I,             _.O,      _.P,             _.L_BRACKET, _.R_BRACKET, _.BACKSPACE,
    _.CAPS_LOCK, _.NOKEY,  _.A,     _.S,     _.D,     _.F,     _.G,     _.H,     _.J,     _.K,             _.L,      _.SEMICOLON,     _.QUOTE,     _.NOKEY,     _.ENTER,
    _.L_SHIFT,   _.NOKEY,  _.Z,     _.X,     _.C,     _.V,     _.B,     _.N,     _.M,     _.COMMA,         _.PERIOD, _.FORWARD_SLASH, _.NOKEY,     _.R_SHIFT,   MEDIA,
    _.L_CTRL,    _.L_CTRL, _.WIN,   _.L_ALT, KPAD_MO, NAV,     _.NOKEY, _.SPACE, _.R_ALT, _.FORWARD_SLASH, _._,      _.L_ALT,         _.NOKEY,     _.R_CTRL,    GAME0,
))

layout.add_layer(
    "keypad",(
    _.TRANS, _.F1,    _.F2,    _.F3,    _.F4,    _.F5,    _.F6, _.F7,     _.F8,        _.F9,    _.F10,   _.F11,    _.F12,   _.TRANS,    _.TRANS,
    _.TRANS, _.NOKEY, _.F5,    _.F6,    _.F7,    _.F8,    _._,  _.NUM_5,  _.KP_7,      _.KP_8,  _.KP_9,  _.MINUS,  _._,     _.TRANS,    _.TRANS,
    _.TRANS, _.NOKEY, _.F9,    _.F10,   _.F11,   _.F12,   _._,  _.KP_ADD, _.KP_4,      _.KP_5,  _.KP_6,  _.KP_MIN, _._,     _.NOKEY,    _.TRANS,
    _.TRANS, _.NOKEY, _._,     _._,     _._,     _._,     _._,  _.KP_DIV, _.KP_1,      _.KP_2,  _.KP_3,  _.KP_MUL, _.NOKEY, _.KP_ENTER, _.TRANS,
    _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.TRANS, _.SPACE, _._,  _.KP_0,   _.KP_PERIOD, _.TRANS, _.TRANS, _.TRANS,  _.NOKEY, _.TRANS,    _.TRANS,
))

layout.add_layer(
    "navigation",(
    _.TRANS, _._,     _._, _._, _._,         _._,      _._, _._,    _._,         _._,       _._,     _._,     _._,     _._,     _._,
    _.TRANS, _.NOKEY, _._, _._, _._,         _._,      _._, _._,    _.PAGE_DOWN, _.PAGE_UP, _._,     _._,     _._,     _._,     _._,
    _.TRANS, _.NOKEY, _._, _._, _.BACKSPACE, _.DELETE, _._, _.LEFT, _.DOWN,      _.UP,      _.RIGHT, _._,     _._,     _.NOKEY, _._,
    _.TRANS, _.NOKEY, _._, _._, _._,         _._,      _._, _._,    _.HOME,      _.END,     _._,     _._,     _.NOKEY, _.TRANS, _._,
    _.TRANS, _._,     _._, _._, _._,         _.TRANS,  _._, _._,    _._,         _._,       _._,     _.TRANS, _.NOKEY, _.TRANS, _._,
))

layout.add_layer(
    "media", (
    _.TRANS, _._,     _._, _._, _._, _._,     _._,     _._, _._, _._, _._, _._,       _._,     _._,       _._,
    _.TRANS, _.NOKEY, _._, _._, _._, _._,     _._,     _._, _._, _._, _._, _._,       _._,     _._,       _._,
    _.TRANS, _.NOKEY, _._, _._, _._, _._,     _._,     _._, _._, _._, _._, _._,       _._,     _.NOKEY,   _._,
    _.TRANS, _.NOKEY, _._, _._, _._, _._,     _._,     _._, _._, _._, _._, "cc:mute", _.NOKEY, "cc:play", MEDIA,
    _.TRANS, _._,     _._, _._, _._, _.TRANS, _.NOKEY, _._, _._, _._, _._, "cc:vold", _.NOKEY, "cc:volu", "cc:calc",
    )
)

layout.add_layer(
    "game0", (
    _.ESC,       _.NUM_1,  _.NUM_2, _.NUM_3, _.NUM_4, _.NUM_5, _.NUM_6, _.NUM_7, _.NUM_8, _.NUM_9,         _.NUM_0,  _.MINUS,         _.EQUALS,    _.BACKSLASH, _.DELETE,
    _.TAB,       _.NOKEY,  _.Q,     _.W,     _.E,     _.R,     _.T,     _.Y,     _.U,     _.I,             _.O,      _.P,             _.L_BRACKET, _.R_BRACKET, _.BACKSPACE,
    _.CAPS_LOCK, _.NOKEY,  _.A,     _.S,     _.D,     _.F,     _.G,     _.H,     _.J,     _.K,             _.L,      _.SEMICOLON,     _.QUOTE,     _._,         _.ENTER,
    _.L_SHIFT,   _.NOKEY,  _.Z,     _.X,     _.C,     _.V,     _.B,     _.N,     _.M,     _.COMMA,         _.PERIOD, _.FORWARD_SLASH, _._,         _.R_SHIFT,   _._,
    _.L_CTRL,    _.L_CTRL, _.WIN,   _.L_ALT, _.H,     _.SPACE, _._,     _.P,     _.R_ALT, _.FORWARD_SLASH, _._,      _._,             _._,         _._,         GAME0,
))


class MainLogic:
    def __init__(s, matrix:Kbd_Matrix, layers:Layers, ble_keyboard:Keyboard, ble_consumer_control:ConsumerControl):
        s.ble_keyboard = ble_keyboard
        s.ble_consumer_control = ble_consumer_control
        s.matrix = matrix
        s.layers:Layers = layers

    def __call__(s):
        ble_keyboard = s.ble_keyboard
        release_old_pressed_keys = s.release_old_pressed_keys
        new_released, new_pressed, old_pressed = s.matrix.get_report()

        # holds every methods `press` and `depress` of each <LayerFunc> that are
        # pressed and depressed in the matrix report
        layers = [] 
        repress = False #sometimes you need some keys to be pressed again

        # keyboard logic
        # release logic
        keys = []
        for key in ( s.layers[idx] for idx in new_released ):
            if key in ( None, _.TRANS ) or type(key) == str: continue
            if callable( key ): # if key function
                if ( type( key ) is lyr.MOMENTARY ) :
                        keys.extend( s.layers[idx] for idx in old_pressed )
                        repress = True
                layers.append( key.depress )
            elif type( key ) is int:
                keys.append( key )
        ble_keyboard.release(*keys )

        # press logic
        keys = []
        for key in ( s.layers[idx] for idx in new_pressed ):
            if key in ( None, _.TRANS ) or type(key) == str : continue
            if callable( key ):
                if not repress:
                    repress = True
                    release_old_pressed_keys( old_pressed )
                layers.append( key.press )
            elif type( key ) is int:
                keys.append( key )

        # first de/activate various <LayerFunc>
        for func in layers : func()

        #consumer control logic
        for text in (s.layers[idx] for idx in new_released if type(s.layers[idx])==str):
            attr, key = text.split(":")
            code = getattr(_, attr)[key]
            assert type(code) == int
            s.ble_consumer_control.send(code)
        
        if repress : keys.extend( s.layers[idx] for idx in old_pressed )
        ble_keyboard.press( *keys )
        gc.collect()

    def release_old_pressed_keys(s, old_pressed):
        s.ble_keyboard.release(*(layout[idx] for idx in old_pressed))


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
        time.sleep(0.5)

if __name__ == '__main__':
    main_loop(layout, matrix)