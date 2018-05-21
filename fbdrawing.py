from micropython import const
import framebuf

class FrameBufferExtended(framebuf.FrameBuffer):
	ROTATE_0   = const(0) # 'portrait', connector up
	ROTATE_90  = const(1)
	ROTATE_180 = const(2)
	ROTATE_270 = const(3)

	def __init__(self, buf, w, h, enc):
		self._buffer = buf
		self._width = w # 'physical' width
		self.width = w # processing width
		self._height = h
		self.height = h
		self._rotate = ROTATE_0

		super(FrameBufferExtended, self).__init__(buf, w, h, enc)

	@property
	def buffer(self):
		return self._buffer

	def get_absolute_pixel(self, x, y):
		if (x < 0 or x >= self._width or y < 0 or y >= self._height):
			return
		
		return self._buffer[(x + y * self._width) // 8]
		
	def set_absolute_pixel(self, x, y, colored):
		print("set_absolute_pixel", x, y, colored)
		# print(" A: w x h: ", self._width , self._height )
		if (x < 0 or x >= self._width or y < 0 or y >= self._height):
			print("A: skipped", x, y)
			return
		if (colored):
			self._buffer[(x + y * self._width) // 8] &= ~(0x80 >> (x % 8))
		else:
			self._buffer[(x + y * self._width) // 8] |= 0x80 >> (x % 8)

	def get_pixel(self, x, y):
		if (x < 0 or x >= self.width or y < 0 or y >= self.height):
			return
		if (self._rotate == ROTATE_0):
			return self.get_absolute_pixel(x, y)
		elif (self._rotate == ROTATE_90):
			return self.get_absolute_pixel(self.height -y -1, x)
		elif (self._rotate == ROTATE_180):
			return self.get_absolute_pixel(self.width -1 - x, self.height -1 - y)
		elif (self._rotate == ROTATE_270):
			return self.get_absolute_pixel(y, self.width -1 - x)

	def set_pixel(self, x, y, colored):
		print("set_pixel", x, y, colored)
		# print(" R: w x h:", self.width, self.height )
		if (x < 0 or x >= self.width or y < 0 or y >= self.height):
			print("R: skipped", x, y)
			return
		if (self._rotate == ROTATE_0):
			self.set_absolute_pixel(x, y, colored)
		elif (self._rotate == ROTATE_90):
			self.set_absolute_pixel(self.height -y -1, x, colored)
		elif (self._rotate == ROTATE_180):
			self.set_absolute_pixel(self.width -1 - x, self.height -1 - y, colored)
		elif (self._rotate == ROTATE_270):
			self.set_absolute_pixel(y, self.width -1 - x, colored)

	def get_rotate(self):
		return self._rotate

	def set_rotate(self, rotate):
		if (rotate == ROTATE_0):
			self._rotate = ROTATE_0
			self.width = self._width
			self.height = self._height
		elif (rotate == ROTATE_90):
			self._rotate = ROTATE_90
			self.width = self._height 
			self.height = self._width
		elif (rotate == ROTATE_180):
			self._rotate = ROTATE_180
			self.width = self._width
			self.height = self._height 
		elif (rotate == ROTATE_270):
			self._rotate = ROTATE_270
			self.width = self._height 
			self.height = self._width
		else:
			raise ValueError('Invalid rotation value')
		print("Display is now: {} x {}", self.width, self.height)

	def draw_line(self, x0, y0, x1, y1, colored):
		# Bresenham algorithm
		dx = abs(x1 - x0)
		sx = 1 if x0 < x1 else -1
		dy = -abs(y1 - y0)
		sy = 1 if y0 < y1 else -1
		err = dx + dy
		while((x0 != x1) and (y0 != y1)):
			self.set_pixel(x0, y0 , colored)
			if (2 * err >= dy):
				 err += dy
				 x0 += sx
			if (2 * err <= dx):
				 err += dx
				 y0 += sy

	def draw_horizontal_line(self, x, y, width, colored):
		for i in range(x, x + width):
			self.set_pixel(i, y, colored)

	def draw_vertical_line(self, x, y, height, colored):
		for i in range(y, y + height):
			self.set_pixel(x, i, colored)

	def draw_rectangle(self, x0, y0, x1, y1, colored):
		min_x = x0 if x1 > x0 else x1
		max_x = x1 if x1 > x0 else x0
		min_y = y0 if y1 > y0 else y1
		max_y = y1 if y1 > y0 else y0
		self.draw_horizontal_line(min_x, min_y, max_x - min_x + 1, colored)
		self.draw_horizontal_line(min_x, max_y, max_x - min_x + 1, colored)
		self.draw_vertical_line(min_x, min_y, max_y - min_y + 1, colored)
		self.draw_vertical_line(max_x, min_y, max_y - min_y + 1, colored)

	def draw_filled_rectangle(self, x0, y0, x1, y1, colored):
		min_x = x0 if x1 > x0 else x1
		max_x = x1 if x1 > x0 else x0
		min_y = y0 if y1 > y0 else y1
		max_y = y1 if y1 > y0 else y0
		for i in range(min_x, max_x + 1):
			self.draw_vertical_line(i, min_y, max_y - min_y + 1, colored)

	def draw_circle(self, x, y, radius, colored):
		# Bresenham algorithm
		x_pos = -radius
		y_pos = 0
		err = 2 - 2 * radius
		if (x >= self.width or y >= self.height):
			return
		while True:
			self.set_pixel(x - x_pos, y + y_pos, colored)
			self.set_pixel(x + x_pos, y + y_pos, colored)
			self.set_pixel(x + x_pos, y - y_pos, colored)
			self.set_pixel(x - x_pos, y - y_pos, colored)
			e2 = err
			if (e2 <= y_pos):
				 y_pos += 1
				 err += y_pos * 2 + 1
				 if(-x_pos == y_pos and e2 <= x_pos):
					  e2 = 0
			if (e2 > x_pos):
				 x_pos += 1
				 err += x_pos * 2 + 1
			if x_pos > 0:
				 break

	def draw_filled_circle(self, x, y, radius, colored):
		# Bresenham algorithm
		x_pos = -radius
		y_pos = 0
		err = 2 - 2 * radius
		if (x >= self.width or y >= self.height):
			return
		while True:
			self.set_pixel(x - x_pos, y + y_pos, colored)
			self.set_pixel(x + x_pos, y + y_pos, colored)
			self.set_pixel(x + x_pos, y - y_pos, colored)
			self.set_pixel(x - x_pos, y - y_pos, colored)
			self.draw_horizontal_line(x + x_pos, y + y_pos, 2 * (-x_pos) + 1, colored)
			self.draw_horizontal_line(x + x_pos, y - y_pos, 2 * (-x_pos) + 1, colored)
			e2 = err
			if (e2 <= y_pos):
				 y_pos += 1
				 err += y_pos * 2 + 1
				 if(-x_pos == y_pos and e2 <= x_pos):
					  e2 = 0
			if (e2 > x_pos):
				 x_pos  += 1
				 err += x_pos * 2 + 1
			if x_pos > 0:
				 break

	def draw_string_at(self, x, y, text, font, colored):
		image = Image.new('1', (self.width, self.height))
		draw = ImageDraw.Draw(image)
		draw.text((x, y), text, font = font, fill = 255)
		# Set buffer to value of Python Imaging Library image.
		# Image must be in mode 1.
		pixels = image.load()
		for y in range(self.height):
			for x in range(self.width):
				 # Set the bits for the column of pixels at the current position.
				 if pixels[x, y] != 0:
					  self.set_pixel(x, y, colored)
