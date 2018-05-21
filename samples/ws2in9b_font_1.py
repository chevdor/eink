import random
import time 
import framebuf
from machine import Pin, SPI
import waveshare2in9b
from fbdrawing import FrameBufferExtended
from bitmapfont import BitmapFont

DISPLAY_WIDTH = waveshare2in9b.EPD_WIDTH
DISPLAY_HEIGHT = waveshare2in9b.EPD_HEIGHT

buf_b = bytearray(DISPLAY_WIDTH * DISPLAY_HEIGHT // 8)
buf_r = bytearray(DISPLAY_WIDTH * DISPLAY_HEIGHT // 8)
fb_black = FrameBufferExtended(buf_b, DISPLAY_WIDTH, DISPLAY_HEIGHT, framebuf.MONO_HLSB)
fb_red = FrameBufferExtended(buf_r, DISPLAY_WIDTH, DISPLAY_HEIGHT, framebuf.MONO_HLSB)

black = 0
white = 1

def main(spi):
	e = waveshare2in9b.EPD(spi, cs=32, dc=33, rst=25, busy=26, idle=0)
	e.init()
	fb_black.fill(white)
	fb_red.fill(white)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	MSG = 'It Works!'
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		with BitmapFont(fb_red.width, fb_red.height, fb_red.set_pixel) as bfr:	
			# message_width = bfb.width(MSG)   # Message width in pixels.
			bfb.text("It Works!",1,0,1)   
			bfr.text("Awesome, now we can have fun!",1,10,1)       
    
			e.display_frame(buf_b, buf_r)

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

main(spi)
