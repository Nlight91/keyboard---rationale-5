class TRANS : pass

class Scancodes :

    NOKEY = 0x0
    
    EMPTY = 0x0

    A = 0x0004 # Keyboard a and A
    # win : True

    B = 0x0005 # Keyboard b and B
    # win : True

    C = 0x0006 # Keyboard c and C
    # win : True

    D = 0x0007 # Keyboard d and D
    # win : True

    E = 0x0008 # Keyboard e and E
    # win : True

    F = 0x0009 # Keyboard f and F
    # win : True

    G = 0x000a # Keyboard g and G
    # win : True

    H = 0x000b # Keyboard h and H
    # win : True

    I = 0x000c # Keyboard i and I
    # win : True

    J = 0x000d # Keyboard j and J
    # win : True

    K = 0x000e # Keyboard k and K
    # win : True

    L = 0x000f # Keyboard l and L
    # win : True

    M = 0x0010 # Keyboard m and M
    # win : True

    N = 0x0011 # Keyboard n and N
    # win : True

    O = 0x0012 # Keyboard o and O
    # win : True

    P = 0x0013 # Keyboard p and P
    # win : True

    Q = 0x0014 # Keyboard q and Q
    # win : True

    R = 0x0015 # Keyboard r and R
    # win : True

    S = 0x0016 # Keyboard s and S
    # win : True

    T = 0x0017 # Keyboard t and T
    # win : True

    U = 0x0018 # Keyboard u and U
    # win : True

    V = 0x0019 # Keyboard v and V
    # win : True

    W = 0x001a # Keyboard w and W
    # win : True

    X = 0x001b # Keyboard x and X
    # win : True

    Y = 0x001c # Keyboard y and Y
    # win : True

    Z = 0x001d # Keyboard z and Z
    # win : True

    NUM_1 = 0x001e # Keyboard 1 and !
    # win : True

    NUM_2 = 0x001f # Keyboard 2 and @
    # win : True

    NUM_3 = 0x0020 # Keyboard 3 and #
    # win : True

    NUM_4 = 0x0021 # Keyboard 4 and $
    # win : True

    NUM_5 = 0x0022 # Keyboard 5 and %
    # win : True

    NUM_6 = 0x0023 # Keyboard 6 and ^
    # win : True

    NUM_7 = 0x0024 # Keyboard 7 and &
    # win : True

    NUM_8 = 0x0025 # Keyboard 8 and *
    # win : True

    NUM_9 = 0x0026 # Keyboard 9 and (
    # win : True

    NUM_0 = 0x0027 # Keyboard 0 and )
    # win : True

    ENTER = 0x0028 # Keyboard Return
    # win : False

    ESCAPE = ESC = 0x0029 # Keyboard Escape
    # win : True

    BACKSPACE = 0x002a # Keyboard Delete (Backspace)
    # win : False

    TAB = 0x002b # Keyboard Tab
    # win : True

    SPACE = 0x002c # Keyboard Spacebar
    # win : True

    MINUS = 0x002d # Keyboard - and _
    # win : True

    EQUALS = 0x002e # Keyboard = and +
    # win : True

    L_BRACKET = 0x002f # Keyboard [ and {
    # win : True

    R_BRACKET = 0x0030 # Keyboard ] and }
    # win : True

    BACKSLASH = 0x0031 # Keyboard \ and |;
    # win : True

    POUND = 0x0032 # # and ~ (Non-US)
    #win : True

    SEMICOLON = 0x0033 # Keyboard ; and :
    # win : True

    QUOTE = 0x0034 # Keyboard ‘ and “
    # win : True

    GRAVE_ACCENT = 0x0035 # Keyboard Grave Accent and Tilde
    # win : True

    COMMA = 0x0036 # Keyboard , and <
    # win : True

    PERIOD = 0x0037 # Keyboard . and &gt;
    # win : True

    FORWARD_SLASH = 0x0038 # Keyboard / and&#160;?
    # win : True

    CAPS_LOCK = 0x0039 # Keyboard Caps Lock
    # win : True

    F1 = 0x003a # Keyboard F1
    # win : True

    F2 = 0x003b # Keyboard F2
    # win : True

    F3 = 0x003c # Keyboard F3
    # win : True

    F4 = 0x003d # Keyboard F4
    # win : True

    F5 = 0x003e # Keyboard F5
    # win : True

    F6 = 0x003f # Keyboard F6
    # win : True

    F7 = 0x0040 # Keyboard F7
    # win : True

    F8 = 0x0041 # Keyboard F8
    # win : True

    F9 = 0x0042 # Keyboard F9
    # win : True

    F10 = 0x0043 # Keyboard F10
    # win : True

    F11 = 0x0044 # Keyboard F11
    # win : True

    F12 = 0x0045 # Keyboard F12
    # win : True

    PRINT_SCREEN = 0x0046 # Keyboard PrintScreen
    # win : True

    SCROLL_LOCK = 0x0047 # Keyboard Scroll Lock
    # win : True

    PAUSE = 0x0048 # Keyboard Pause
    # win : True

    INSERT = 0x0049 # Keyboard Insert
    # win : True

    HOME = 0x004a # Keyboard Home
    # win : True

    PAGE_UP = 0x004b # Keyboard PageUp
    # win : True

    DELETE = 0x004c # Keyboard Delete(forward)
    # win : True

    END = 0x004d # Keyboard End
    # win : True

    PAGE_DOWN = 0x004e # Keyboard PageDown
    # win : True

    RIGHT = RIGHT_ARROW = 0x004f # Keyboard RightArrow
    # win : True

    LEFT = LEFT_ARROW = 0x0050 # Keyboard LeftArrow
    # win : True

    DOWN = DOWN_ARROW = 0x0051 # Keyboard DownArrow
    # win : True

    UP = UP_ARROW = 0x0052 # Keyboard UpArrow
    # win : True

    KEYPAD_NUMLOCK = KP_NLCK = 0x0053 # Keypad Num Lock and Clear
    # win : False

    KEYPAD_FOWARD_SLASH = KP_DIV = 0x0054 # Keypad /
    # win : True

    KEYPAD_ASTERISK = KP_MUL = 0x0055 # Keypad *
    # win : True

    KEYPAD_MINUS = KP_MIN = 0x0056 # Keypad -
    # win : True

    KEYPAD_PLUS = KP_ADD = 0x0057 # Keypad +
    # win : True

    KEYPAD_ENTER = KP_ENTER = 0x0058 # Keypad ENTER
    # win : True

    KP_1 = KEYPAD_ONE = 0x0059 # Keypad 1 and End
    # win : True

    KP_2 = KEYPAD_TWO = 0x005a # Keypad 2  and Down Arrow
    # win : True

    KP_3 = KEYPAD_THREE = 0x005b # Keypad 3 and PageDn
    # win : True

    KP_4 = KEYPAD_FOUR = 0x005c # Keypad 4 and Left Arrow
    # win : True

    KP_5 = KEYPAD_FIVE = 0x005d # Keypad 5
    # win : True

    KP_6 = KEYPAD_SIX = 0x005e # Keypad 6 and Right Arrow
    # win : True

    KP_7 = KEYPAD_SEVEN = 0x005f # Keypad 7  and Home
    # win : True

    KP_8 = KEYPAD_EIGHT = 0x0060 # Keypad 8 and Up Arrow
    # win : True

    KP_9 = KEYPAD_NINE = 0x0061 # Keypad 9 and PageUp
    # win : True

    KP_0 = KEYPAD_ZERO = 0x0062 # Keypad 0 and Insert
    # win : True

    KEYPAD_PERIOD = KP_PERIOD = 0x0063 # Keypad . and Delete
    # win : True

    KEYPAD_BACKSLASH = KP_BSLASH = 0x0064 # Keyboard Int, \ and &#124; (Between left Shift and Z on ISO layouts)
    # win : True

    APPLICATION = 0x0065 # Keyboard Application (Menu key)
    # win : True

    POWER = 0x0066 # Keyboard Power (MAC)
    # win : False

    F13 = 0x0068 # Keyboard F13
    # win : False

    F14 = 0x0069 # Keyboard F14
    # win : False

    F15 = 0x006a # Keyboard F15
    # win : False

    F16 = 0x006b # Keyboard F16
    # win : False

    F17 = 0x006c # Keyboard F17
    # win : False

    F18 = 0x006d # Keyboard F18
    # win : False

    F19 = 0x006e # Keyboard F19
    # win : False

    WIN_MUTE = 0X007F # mute (windows)
    # win : True

    WIN_VOLUME_UP = 0x0080 # volume up (windows)
    # win : True

    WIN_VOLUME_DOWN = 0x0080 # volume down (windows)
    # win : True

    KEYPAD_COMMA = 0x0085 # Keypad ,(brazil)
    # win : False

    KEYBOARD_INT1 = KEYBOARD_RO = 0x0087 # Keyboard INT1 Ro (Japan: \)(Brazil : /)
    # win : True

    KEYBOARD_INT2 = KEYBOARD_KANA = 0x0088 # Keyboard INT2 Kana (Japan)
    # win : True

    KEYBOARD_INT3 = KEYBOARD_YEN = 0x0089 # Keyboard INT3 Yen (Japan)
    # win : True

    KEYBOARD_INT4 = KEYBOARD_HENKAN  = 0x008a # Keyboard INT4<br />Henkan (Conversion) (Japan)
    # win : True

    KEYBOARD_INT5 = KEYBOARD_MUHENKAN = 0x008b # Keyboard INT5<br />Muhenkan (Non-conversion) (Japan)
    # win : True

    KEYBOARD_INT6 = 0x008c # Keyboard INT6<br />PC98 Keypad comma
    # win : False

    KEYBOARD_INT7 = 0x008d # Keyboard INT7<br />PC98 Toggle single-byte/double-byte mode
    # win : False

    KEYBOARD_INT8 = 0x008e # Keyboard INT8
    # win : False

    KEYBOARD_INT9 = 0x008f # Keyboard INT9
    # win : False

    KEYBOARD_LANG1 = KEYBOARD_HANGUL = 0x0090 # Keyboard LANG1<br />Hangul/English toggle (Korean)
    # win : False

    KEYBOARD_LANG2 = KEYBOARD_HANJA = 0x0091 # Keyboard LANG2<br />Hanja conversion (Korean)
    # win : False

    KEYBOARD_LANG3 = 0x0092 # Keyboard LANG3<br />PC98 Katakana
    # win : False

    KEYBOARD_LANG4 = 0x0093 # Keyboard LANG4<br />PC98 Hiragana
    # win : False

    KEYBOARD_LANG5 = 0x0094 # Keyboard LANG5<br />PC98 "Kaku": Hankaku/Zenkaku ("Full-size"/"Half-size"/"Kanji") when not on Keyboard Tilde key (Japanese)
    # win : False

    KEYBOARD_LANG6 = 0x0095 # Keyboard LANG6<br />PC98 Furigana (Hiragana as pronunciation-help above Kanji)
    # win : False

    KEYBOARD_LANG7 = 0x0096 # Keyboard LANG7
    # win : False

    KEYBOARD_LANG8 = 0x0097 # Keyboard LANG8
    # win : False

    KEYBOARD_LANG9 = 0x0098 # Keyboard LANG9
    # win : False

    LEFT_CONTROL = L_CTRL = CONTROL= 0x00e0 # Keyboard Left Control
    # win : True

    LEFT_SHIFT = L_SHIFT = SHIFT = 0x00e1 # Keyboard Left Shift
    # win : True

    LEFT_ALT = L_ALT = ALT = 0x00e2 # Keyboard Left Alt
    # win : True

    LEFT_GUI = L_GUI = GUI = WINDOWS = WIN = COMMAND = CMD = 0x00e3 # Keyboard Left GUI
    # win : False

    RIGHT_CONTROL = R_CTRL = 0x00e4 # Keyboard Right Control
    # win : True

    RIGHT_SHIFT = R_SHIFT = 0x00e5 # Keyboard Right Shift
    # win : True

    RIGHT_ALT = R_ALT = 0x00e6 # Keyboard Right Alt
    # win : True

    RIGHT_GUI = R_GUI = R_WIN = RIGHT_COMMAND = R_CMD = 0x00e7 # Keyboard Right GUI
    # win : False

    APP_CALC = 0X0192 # Windows calc
    # win : True

    APP_MY_COMPUTER = 0X0194 # Windows explorer on My Computer
    # win : True

    TRANS = TRANS

    @classmethod
    def modifier_bit(cls, keycode):
        return ( 1 << ( keycode - 0xe0 ) ) if cls.CONTROL <= keycode <= cls.R_GUI else 0
