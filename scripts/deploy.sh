#!/bin/bash

DELAY=1

echo Copying fonts
ampy -d $DELAY put font5x8.bin

echo Copying font module
ampy -d $DELAY put bitmapfont.mpy

echo Coyping fbdrawing module
ampy -d $DELAY put fbdrawing.py

echo Copying waveshare module
ampy -d $DELAY put waveshare2in9b.py

ampy ls
echo Done