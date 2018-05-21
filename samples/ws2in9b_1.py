from machine import Pin, SPI
import waveshare2in9b
import random
from fbdrawing import FrameBufferExtended
import time 
import framebuf

# baudrate = int(20e6)
baudrate = int(20e6)
# Software SPI
# We use specific values below are they match the default hardware SPI pins
# Although hardware SPI works, I had however better perf and less troubles with software SPI. 
# Comment the line below is you want to use hardware SPI
spi = SPI(-1, baudrate=baudrate, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12)) 

# Hardware SPI
# Comment out the 2 lines below if you want to use hardware SPI
# hspi = SPI(1, baudrate=baudrate, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# spi = hspi

e = waveshare2in9b.EPD(spi, cs=32, dc=33, rst=25, busy=26, idle=0)

WIDTH = waveshare2in9b.EPD_WIDTH
HEIGHT = waveshare2in9b.EPD_HEIGHT

buf_b = bytearray(WIDTH * HEIGHT // 8)
buf_r = bytearray(WIDTH * HEIGHT // 8)
fb_black = FrameBufferExtended(buf_b, WIDTH, HEIGHT, framebuf.MONO_HLSB)
fb_red = FrameBufferExtended(buf_r, WIDTH, HEIGHT, framebuf.MONO_HLSB)

black = 0
white = 1

def test_r(r):
	""" Test Rotation and limits """
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)

	fb_black.set_rotate(r)
	w = fb_black.width
	h = fb_black.height
	print ("w x h: ", w, h)

	fb_black.set_pixel(0,0,1)
	fb_black.set_pixel(1,0,1)
	print()
	fb_black.set_pixel(w-1,0,1)
	fb_black.set_pixel(w-2,0,1)
	print()
	fb_black.set_pixel(0,h-1,1)
	print()
	fb_black.set_pixel(w-1,h-1,1)
	print()
	fb_black.set_pixel(w//2,h//2,1)
	print()

	e.display_frame(buf_b, buf_r)

def test_0():
	test_r(FrameBufferExtended.ROTATE_0)

def test_90():
	test_r(FrameBufferExtended.ROTATE_90)

def test_180():
	test_r(FrameBufferExtended.ROTATE_180)

def test_270():
	test_r(FrameBufferExtended.ROTATE_270)
