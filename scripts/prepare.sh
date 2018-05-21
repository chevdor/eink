#!/bin/bash

echo Getting requirements...
wget -q https://raw.githubusercontent.com/adafruit/micropython-adafruit-bitmap-font/master/bitmapfont.py
# wget https://github.com/adafruit/micropython-adafruit-bitmap-font/blob/master/font5x8.bin?raw=true # we make our own
wget -q https://raw.githubusercontent.com/adafruit/micropython-adafruit-bitmap-font/master/font_to_bin.py
# wget https://github.com/adafruit/micropython-adafruit-bitmap-font/releases/download/2.0/bitmapfont.mpy # we make our own
mpy-cross -O2 bitmapfont.py

python3 font_to_bin.py 

echo Done