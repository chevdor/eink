from machine import Pin, SPI
from fbdrawing import FrameBufferExtended
import time 
import framebuf
import epaper1in54

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
e.clear_frame_memory(b'\xFF')

#fb_red = FrameBufferExtended(buf_r, WIDTH, HEIGHT, framebuf.MONO_HLSB)

black = 0
white = 1

def getDate():
	date = [i for i in time.localtime()]
	printformat = "{:02d}:{:02d}:{:02d} {:02d}-{:02d}-{:4d}"
	return printformat.format(date[3],date[4], date[5], date[2], date[1], date[0])

def test1():
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	fb_black.text('! IT WORKS !',10, 0, black)

	for x in range(0,100):
		fb_black.set_absolute_pixel(x,x, 1)

	mydisplay_frame(e,fb_black, buf_b)

def test2():
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	fb_black.text('! IT WORKS !',10, 0, black)
	fb_black.text('Chevdor',10, 10, black)
	fb_black.text('2018-05-20',10, 20, black)
	fb_black.text(getDate(),10, 30, black)

	fb_black.draw_rectangle(10, 50 , 110, 150, 1)
	mydisplay_frame(e,fb_black, buf_b)

def test3():
	""" Draw rectangles at origin and accross diagonal """
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	fb_black.fill_rect(0, 0, 10, 10, black)
	fb_black.fill_rect(WIDTH-10, HEIGHT-10, 10, 10, black)
	mydisplay_frame(e,fb_black, buf_b)

def test4():
	""" Basic pixel drawing without rotation """
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	
	fb_black.set_absolute_pixel(0,0,1)
	fb_black.set_absolute_pixel(WIDTH-1,0,1)
	fb_black.set_absolute_pixel(0,HEIGHT-1,1)
	fb_black.set_absolute_pixel(WIDTH-1,HEIGHT-1,1)
	fb_black.set_absolute_pixel(WIDTH//2,HEIGHT//2,1)
	
	mydisplay_frame(e,fb_black, buf_b)

def test5():
	""" Basic pixel drawing with rotation """
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)

	fb_black.set_pixel(0,0,1)
	fb_black.set_pixel(1,1,1)
	fb_black.set_pixel(10,10,1)
	fb_black.set_pixel(11,11,1)

	mydisplay_frame(e,fb_black, buf_b)

def test6():
	""" Test Rotation """
	e.init()
	fb_black.fill(white)
	fb_black.fill(white)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	fb_black.set_rotate(FrameBufferExtended.ROTATE_270)
	print("x from 0 to ", HEIGHT-1)
	print("y from 0 to ", WIDTH-1)
	for x in range(0, HEIGHT-1):
		for y in range(0, WIDTH-1):
			if (x % 2 == 0): 
				fb_black.set_pixel(x,y, 1)
			#if (y % 2 == 1):
				#fb_black.set_pixel(x+1,y+1, 1)
	mydisplay_frame(e,fb_black, buf_b)

def mydisplay_frame(epd, fb, buf):
	fb.fix_framebuffer_MVLSB()
	e.set_frame_memory(buf, 0, 0, epd.width, epd.height)
	e.display_frame()
	
	