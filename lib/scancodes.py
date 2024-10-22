# things to know : 
#   - codes used for the keys here are HID Usage ID
#   - Usage ID are linked to Usage Page
#   - the way Adafruit set up the keyboard HID descriptor gives access to 3 Usage Pages : Keyboard (0x07), Mouse, Consumer(0x0c)

def get_hid_usage_id(_type, key_name):
    return getattr(globals()[_type.strip()], key_name.strip())

# Non keys
class no:
    TRANS = "no:TRANS"
    key = nop = _ = 0x0

#KeyBoard (Usage Page : 0x07)
class kb :
    A = 0x0004 # keyboard A and a
    B = 0x0005 # keyboard B and b
    C = 0x0006 # keyboard C and c
    D = 0x0007 # keyboard D and d
    E = 0x0008 # keyboard E and e
    F = 0x0009 # keyboard F and f
    G = 0x000a # keyboard G and g
    H = 0x000b # keyboard H and h
    I = 0x000c # keyboard I and i
    J = 0x000d # keyboard J and j
    K = 0x000e # keyboard K and k
    L = 0x000f # keyboard L and l
    M = 0x0010 # keyboard M and m
    N = 0x0011 # keyboard N and n
    O = 0x0012 # keyboard O and o
    P = 0x0013 # keyboard P and p
    Q = 0x0014 # keyboard Q and q
    R = 0x0015 # keyboard R and r
    S = 0x0016 # keyboard S and s
    T = 0x0017 # keyboard T and t
    U = 0x0018 # keyboard U and u
    V = 0x0019 # keyboard V and v
    W = 0x001a # keyboard W and w
    X = 0x001b # keyboard X and x
    Y = 0x001c # keyboard Y and y
    Z = 0x001d # keyboard Z and z
    _1 = 0x001e # keyboard 1 and !
    _2 = 0x001f # keyboard 2 and @
    _3 = 0x0020 # keyboard 3 and #
    _4 = 0x0021 # keyboard 4 and $
    _5 = 0x0022 # keyboard 5 and %
    _6 = 0x0023 # keyboard 6 and ^
    _7 = 0x0024 # keyboard 7 and &
    _8 = 0x0025 # keyboard 8 and *
    _9 = 0x0026 # keyboard 9 and (
    _0 = 0x0027 # keyboard 0 and )
    enter = 0x0028 # keyboard return
    # win : false
    escape = esc = 0x0029 # keyboard escape
    backspace = bkspc = 0x002a # keyboard delete (backspace)
    # win : false
    tab = 0x002b # keyboard tab
    space = 0x002c # keyboard spacebar
    minus = 0x002d # keyboard - and _
    equals = 0x002e # keyboard = and +
    l_bracket = lbckt = 0x002f # keyboard [ and {
    r_bracket = rbckt = 0x0030 # keyboard ] and }
    backslash = bslsh = 0x0031 # keyboard \ and |;
    pound = 0x0032 # # and ~ (non-us)
    #win : true
    semicolon = smcln = 0x0033 # keyboard ; and :
    quote = 0x0034 # keyboard ‘ and “
    grave_accent = 0x0035 # keyboard grave accent and tilde
    comma = 0x0036 # keyboard , and <
    period = priod = 0x0037 # keyboard . and &gt;
    forward_slash = fslsh = 0x0038 # keyboard / and&#160;?
    caps_lock = cplck = 0x0039 # keyboard caps lock
    F1 = 0x003a # keyboard f1
    F2 = 0x003b # keyboard f2
    F3 = 0x003c # keyboard f3
    F4 = 0x003d # keyboard f4
    F5 = 0x003e # keyboard f5
    F6 = 0x003f # keyboard f6
    F7 = 0x0040 # keyboard f7
    F8 = 0x0041 # keyboard f8
    F9 = 0x0042 # keyboard f9
    F10 = 0x0043 # keyboard f10
    F11 = 0x0044 # keyboard f11
    F12 = 0x0045 # keyboard f12
    print_screen = 0x0046 # keyboard printscreen
    scroll_lock = 0x0047 # keyboard scroll lock
    pause = 0x0048 # keyboard pause
    insert = 0x0049 # keyboard insert
    home = 0x004a # keyboard home
    page_up = pgup = 0x004b # keyboard pageup
    delete = dlete = 0x004c # keyboard delete(forward)
    end = 0x004d # keyboard end
    page_down = pgdwn = 0x004e # keyboard pagedown
    right = right_arrow = 0x004f # keyboard rightarrow
    left = left_arrow = 0x0050 # keyboard leftarrow
    down = down_arrow = 0x0051 # keyboard downarrow
    up = up_arrow = 0x0052 # keyboard uparrow
    application = 0x0065 # keyboard application (menu key) (win, unix)
    power = 0x0066 # keyboard power (mac, unix)
    F13 = 0x0068 # keyboard f13 (mac)
    F14 = 0x0069 # keyboard f14 (mac)
    F15 = 0x006a # keyboard f15 (mac)
    kp_lparen = 0x00b6 # keypad left parenthesis
    kp_rparen = 0x00b7 # keypad right parenthesis
    left_control = lctrl = l_ctrl = control= 0x00e0 # keyboard left control
    left_shift = lshft = l_shift = shift = 0x00e1 # keyboard left shift
    left_alt = lalt = l_alt = alt = 0x00e2 # keyboard left alt
    left_gui = lgui = l_gui = gui = windows = win = command = cmd = 0x00e3 # keyboard left gui
    right_control = rctrl = r_ctrl = 0x00e4 # keyboard right control
    right_shift = rshft = r_shift = 0x00e5 # keyboard right shift
    right_alt = ralt = r_alt = 0x00e6 # keyboard right alt
    right_gui = rgui = r_gui = r_win = right_command = r_cmd = 0x00e7 # keyboard right gui

# non-us (Usage Page : 0x07)
class nus:
    keyboard_int1 = roma = 0x0087 # keyboard int1 ro (japan: \)(brazil : /)
    keyboard_int2 = kana = 0x0088 # keyboard int2 kana (japan)
    keyboard_int3 = yen = 0x0089 # keyboard int3 yen (japan)
    keyboard_int4 = hen = henkan  = 0x008a # keyboard int4<br />henkan (conversion) (japan)
    keyboard_int5 = muhan = muhenkan = 0x008b # keyboard int5<br />muhenkan (non-conversion) (japan)
    keyboard_int6 = jpcom = kpjpcomma = 0x008c # keyboard int6<br />pc98 keypad comma
    keyboard_int7 = 0x008d # keyboard int7<br />pc98 toggle single-byte/double-byte mode
    keyboard_int8 = 0x008e # keyboard int8
    keyboard_int9 = 0x008f # keyboard int9
    keyboard_lang1 = hangl = hangul = 0x0090 # keyboard lang1<br />hangul/english toggle (korean)
    keyboard_lang2 = hanja = hanja = 0x0091 # keyboard lang2<br />hanja conversion (korean)
    keyboard_lang3 = 0x0092 # keyboard lang3<br />pc98 katakana
    keyboard_lang4 = 0x0093 # keyboard lang4<br />pc98 hiragana
    keyboard_lang5 = 0x0094 # keyboard lang5<br />pc98 "kaku": hankaku/zenkaku ("full-size"/"half-size"/"kanji") when not on keyboard tilde key (japanese)
    keyboard_lang6 = 0x0095 # keyboard lang6<br />pc98 furigana (hiragana as pronunciation-help above kanji)
    keyboard_lang7 = 0x0096 # keyboard lang7
    keyboard_lang8 = 0x0097 # keyboard lang8
    keyboard_lang9 = 0x0098 # keyboard lang9
    
#KeyPad (Usage Page : 0x07)
class kp :
    numlock = nmlck = 0x0053 # keypad num lock and clear
    foward_slash = div = 0x0054 # keypad /
    asterisk = mul = 0x0055 # keypad *
    minus = min = 0x0056 # keypad -
    plus = add = 0x0057 # keypad +
    enter = enter = 0x0058 # keypad enter
    _1 = one = 0x0059 # keypad 1 and end
    _2 = two = 0x005a # keypad 2  and down arrow
    _3 = three = 0x005b # keypad 3 and pagedn
    _4 = four = 0x005c # keypad 4 and left arrow
    _5 = five = 0x005d # keypad 5
    _6 = six = 0x005e # keypad 6 and right arrow
    _7 = seven = 0x005f # keypad 7  and home
    _8 = eight = 0x0060 # keypad 8 and up arrow
    _9 = nine = 0x0061 # keypad 9 and pageup
    _0 = zero = 0x0062 # keypad 0 and insert
    period = dot = period = 0x0063 # keypad . and delete
    backslash = bslsh = kp_bslash = 0x0064 # keyboard int, \ and &#124; (between left shift and z on iso layouts)
    equal = 0x67 # keypad = (mac)
    brasil_comma = brcomma = 0x0085 # keypad ,(brazil)

#Consumer Control (Usage Page : 0x0c)
class cc:
    play = 0xcd
    volup = 0xe9
    voldn = 0xea
    mute = 0xe2
    calc = 0x192
