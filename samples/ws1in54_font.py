from fbdrawing import FrameBufferExtended
from bitmapfont import BitmapFont
from machine import Pin, SPI
import time 
import framebuf
import epaper1in54

BLACK = 0
WHITE = 1

# SPI0 only on LoPy
spi = SPI(0, SPI.MASTER, baudrate=2000000, polarity=0, phase=0, firstbit=SPI.MSB, pins=('P23','P4','P19'))
cs = Pin('P3')
dc = Pin('P11')
rst =Pin('P10')
busy = Pin('P9')

e = epaper1in54.EPD(spi, cs, dc, rst, busy)
e.init()

WIDTH = e.width
HEIGHT = e.height

buf_b = bytearray(WIDTH * HEIGHT // 8)
#fb = framebuf.FrameBuffer(buf_b, WIDTH, HEIGHT, framebuf.MVLSB)
fb_black = FrameBufferExtended(buf_b, WIDTH, HEIGHT, framebuf.MVLSB)
fb_black.set_scale(2)
e.clear_frame_memory(b'\xFF')

#fb_red = FrameBufferExtended(buf_r, WIDTH, HEIGHT, framebuf.MONO_HLSB)

def test1():
	e.init()
	fb_black.fill(WHITE)
	#fb_red.fill(WHITE)
	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		for i in range (6):
			for j in range(45):
				val = i * 45 + j 
				if val < 256:
					# print("print char", val)
					bfb.draw_char(chr(val),j * (bfb._font_width +1 ),i * (bfb._font_height +1),BLACK)   

	mydisplay_frame(e, buf_b)

def test2():
	e.init()
	fb_black.fill(WHITE)
	#fb_red.fill(WHITE)
	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	#fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	MSG = 'It Works!'
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
			bfb.text("It Works!",1,0,BLACK)   
			bfb.text("Awesome, now we can have fun!",1,10,BLACK)       
			mydisplay_frame(e, buf_b)

def test3():
	""" Test char boundaries """
	e.init()
	fb_black.fill(WHITE)
	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		for c in ['A', '.', '-', ':', ' ']:
			print (c, '->',bfb.char_boundaries(c), bfb.char_width(c))   
				
# bfb = BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel); bfb.init()
# bfb.char_boundaries('.')

def test4():
	e.init()
	fb_black.fill(WHITE)
 	#fb_red.fill(WHITE)

	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
		MSG = "AA...-::ZBCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		bfb.text(MSG,0,0,BLACK)   		
		bfb.text_proportional(MSG,0,10,BLACK) 
		MSG = 'The quick brown fox jumps over the lazy dog'  
		bfb.text(MSG,0,20,BLACK)   		
		bfb.text_proportional(MSG,0,30,BLACK) 

	mydisplay_frame(e, buf_b)

def test5():
	e.init()
	fb_black.fill(WHITE)
	#fb_red.fill(WHITE)
	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	#fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
			bfb.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,0,BLACK)   
			bfb.text("abcdefghijklmnopqrstuvwxyz",1,10,BLACK)       
			bfb.text("0123456789.",1,20,1)       
			
			bfb.text_proportional("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,30,BLACK)   
			bfb.text_proportional("abcdefghijklmnopqrstuvwxyz",1,40,BLACK)       
			bfb.text_proportional("0123456789.",1,50,1)       
			mydisplay_frame(e, buf_b)

def test6():
	e.init()
	fb_black.fill(WHITE)
	#fb_red.fill(WHITE)
	#fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	#fb_red.set_rotate(FrameBufferExtended.ROTATE_270)
	with BitmapFont(fb_black.width, fb_black.height, fb_black.set_pixel) as bfb:	
			bfb.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,0,BLACK)   
			bfb.text("abcdefghijklmnopqrstuvwxyz",1,10,BLACK)       
			bfb.text("0123456789.",1,20,1)       
			
			bfb.text_proportional("ABCDEFGHIJKLMNOPQRSTUVWXYZ",1,30,BLACK)   
			bfb.text_proportional("abcdefghijklmnopqrstuvwxyz",1,40,BLACK)       
			bfb.text_proportional("0123456789.",1,50,1)       
	
			mydisplay_frame(e, buf_b)
			time.sleep(1)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)
			fb_black.scroll(0, 5)
			mydisplay_frame(e, buf_b)

def mydisplay_frame(epd, buf):
	#fb.fix_framebuffer_MVLSB()
	epd.set_frame_memory(buf, 0, 0, epd.width, epd.height)
	epd.display_frame()

