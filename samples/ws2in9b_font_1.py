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

BLACK = 0
WHITE = 1

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

def test1():
	e.init()
	fb_black.fill(WHITE)
	fb_red.fill(WHITE)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		with BitmapFont(fb_red.width, fb_red.height, fb_red.set_pixel) as bfr:	
			for i in range (6):
				for j in range(45):
					val = i * 45 + j 
					if val < 256:
						# print("print char", val)
						if i % 2:
							bfb.draw_char(chr(val),j * (bfb._font_width +1 ),i * (bfb._font_height +1),1)   
						else:
							bfr.draw_char(chr(val),j * (bfr._font_width +1 ),i * (bfr._font_height +1),1)   

	e.display_frame(buf_b, buf_r)

def test2():
	e.init()
	fb_black.fill(WHITE)
	fb_red.fill(WHITE)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	MSG = 'It Works!'
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		with BitmapFont(fb_red.width, fb_red.height, fb_red.set_pixel) as bfr:	
			# message_width = bfb.width(MSG)   # Message width in pixels.
			bfb.text("It Works!",1,0,1)   
			bfr.text("Awesome, now we can have fun!",1,10,1)       
	
			e.display_frame(buf_b, buf_r)

def test3():
	""" Test char boundaries """
	e.init()
	fb_black.fill(WHITE)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		for c in ['A', '.', '-', ':', ' ']:
			print (c, '->',bfb.char_boundaries(c), bfb.char_width(c))   
				
# bfb = BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel); bfb.init()
# bfb.char_boundaries('.')

def test4():
	e.init()
	fb_black.fill(WHITE); fb_red.fill(WHITE)

	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		MSG = "AA...-::ZBCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		bfb.text(MSG,0,0,1)   		
		bfb.text_proportional(MSG,0,10,1) 
		MSG = 'The quick brown fox jumps over the lazy dog'  
		bfb.text(MSG,0,20,1)   		
		bfb.text_proportional(MSG,0,30,1) 

	e.display_frame(buf_b, buf_r)

def test5():
	e.init()
	fb_black.fill(WHITE)
	fb_red.fill(WHITE)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	y = 0
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		with BitmapFont(fb_red.width, fb_red.height, fb_red.set_pixel) as bfr:	
			bfr.text("Non Proportional font demo:",1,y,1); y += 8 + 1
			bfb.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,y,1); y += 8 + 1   
			bfb.text("abcdefghijklmnopqrstuvwxyz",1,y,1); y += 8 + 1       
			bfb.text("0123456789.",1,y,1); y += 8 + 1
			y += 8 + 1       
			
			bfr.text_proportional("Proportional font demo:",1,y,1); y += 8 + 1   
			bfb.text_proportional("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,y,1); y += 8 + 1   
			bfb.text_proportional("abcdefghijklmnopqrstuvwxyz",1,y,1); y += 8 + 1       
			bfb.text_proportional("0123456789.",1,y,1); y += 8 + 1       
	
			e.display_frame(buf_b, buf_r)

