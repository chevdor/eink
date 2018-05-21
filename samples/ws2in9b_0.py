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

def getDate():
	date = [i for i in time.localtime()]
	printformat = "{:02d}:{:02d}:{:02d} {:02d}-{:02d}-{:4d}"
	return printformat.format(date[3],date[4], date[5], date[2], date[1], date[0])

def test1():
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.text('! IT WORKS !',10, 0, black)

	for x in range(0,100):
		fb_black.set_absolute_pixel(x,x, 1)

	e.display_frame(buf_b, buf_r)

def test2():
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.text('! IT WORKS !',10, 0, black)
	fb_red.text('Chevdor',10, 10, black)
	fb_red.text('2018-05-20',10, 20, black)
	fb_red.text(getDate(),10, 30, black)

	fb_black.draw_rectangle(10, 50 , 110, 150, 1)
	e.display_frame(buf_b, buf_r)

def test3():
	""" Draw rectangles at origin and accross diagonal """
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.fill_rect(0, 0, 10, 10, black)
	fb_red.fill_rect(WIDTH-10, HEIGHT-10, 10, 10, black)
	e.display_frame(buf_b, buf_r)

def test4():
	""" Basic pixel drawing without rotation """
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	
	fb_black.set_absolute_pixel(0,0,1)
	fb_black.set_absolute_pixel(WIDTH-1,0,1)
	fb_black.set_absolute_pixel(0,HEIGHT-1,1)
	fb_black.set_absolute_pixel(WIDTH-1,HEIGHT-1,1)
	fb_black.set_absolute_pixel(WIDTH//2,HEIGHT//2,1)
	
	e.display_frame(buf_b, buf_r)

def test5():
	""" Basic pixel drawing with rotation """
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)

	fb_black.set_pixel(0,0,1)
	fb_red.set_pixel(1,1,1)
	fb_black.set_pixel(10,10,1)
	fb_red.set_pixel(11,11,1)

	e.display_frame(buf_b, buf_r)

def test6():
	""" Test Rotation """
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	print("x from 0 to ", HEIGHT-1)
	print("y from 0 to ", WIDTH-1)
	for x in range(0, HEIGHT-1):
		for y in range(0, WIDTH-1):
			if (x % 2 == 0): 
				fb_black.set_pixel(x,y, 1)
			if (y % 2 == 1):
				fb_red.set_pixel(x+1,y+1, 1)
	e.display_frame(buf_b, buf_r)
	