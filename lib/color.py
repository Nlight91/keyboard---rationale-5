GAMMA = bytearray(256)
for i in range(256):
    GAMMA[i] = int(pow(float(i)/255, 2.7) * 255 + 0.5)

def rgb(string:str):
    num = int(string, 16)
    r = (num & 0xff0000) >> 16
    g = (num & 0xff00) >> 8
    b = num & 0xff
    return GAMMA[r], GAMMA[g], GAMMA[b]

RED         = rgb("ff0000")
GREEN       = rgb("00ff00")
BLUE        = rgb("0000ff")

YELLOW      = rgb("ffff00")
CYAN        = rgb("00ffff")
MAGENTA     = rgb("ff00ff")

WHITE       = rgb("ffffff")

ORANGE      = rgb("ff7f00")
LIME        = rgb("aeff00")
TURQUOISE   = rgb("00ffb3")
SKY         = rgb("0099ff")
PURPLE      = rgb("9900ff")