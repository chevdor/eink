# MicroPython basic bitmap font renderer.
# Author: Tony DiCola & Wilfried Kopp
# License: MIT License (https://opensource.org/licenses/MIT)
import ustruct

class BitmapFont:
    def __init__(self, width, height, pixel, font_name='font5x8.bin'):
        # Specify the drawing area width and height, and the pixel function to
        # call when drawing pixels (should take an x and y param at least).
        # Optionally specify font_name to override the font file to use (default
        # is font5x8.bin).  The font format is a binary file with the following
        # format:
        # - 1 unsigned byte: font character width in pixels
        # - 1 unsigned byte: font character height in pixels
        # - x bytes: font data, in ASCII order covering all 255 characters.
        #            Each character should have a byte for each pixel column of
        #            data (i.e. a 5x8 font has 5 bytes per character).
        self._width = width
        self._height = height
        self._pixel = pixel
        self._font_name = font_name

    def init(self):
        # Open the font file and grab the character width and height values.
        # Note that only fonts up to 8 pixels tall are currently supported.
        self._font = open(self._font_name, 'rb')
        self._font_width, self._font_height = ustruct.unpack('BB', self._font.read(2))

    def deinit(self):
        # Close the font file as cleanup.
        self._font.close()

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def get_char(self, ch):
        char_data = []
        for char_x in range(self._font_width):
            self._font.seek(2 + (ord(ch) * self._font_width) + char_x)
            line = ustruct.unpack('B', self._font.read(1))[0]
            char_data.append(line)
        return char_data

    def draw_char(self, ch, x, y, *args, **kwargs):
        """ Draw a single char """
        # Don't draw the character if it will be clipped off the visible area.
        if x < -self._font_width or x >= self._width or \
           y < -self._font_height or y >= self._height:
            return

        data = self.get_char(ch)
        boundaries = self.char_boundaries(ch)

        # print("printing {} at x={}-{}".format(ch, x+boundaries[0], x+boundaries[1]))
        # Go through each column of the character that contains pixels to draw
        i = 0
        for char_x in range(boundaries[0], boundaries[1] + 1):
            # Grab the byte for the current column of font data.
            line = data[char_x]
            
            # Go through each non null row in the column byte.
            for char_y in range(self._font_height):
                # Draw a pixel for each bit that's flipped on.
                if (line >> char_y) & 0x1:
                    self._pixel(x + i, y + char_y, *args, **kwargs)
            i += 1

    def text(self, text, x, y, *args, **kwargs):
        """ Draw the specified text at the specified location """
        for i in range(len(text)):
            self.draw_char(text[i], x + (i * (self._font_width + 1)), y,
                           *args, **kwargs)

    # The goal here is to have less blank spaces when the chars take less room
    # for instance, ... should be much narrower than WWW 
    def text_proportional(self, text, x, y, *args, **kwargs):
        """ Draw the specified text at the specified location """
        pos = x
        for i in range(len(text)):
            ch = text[i]
            # boundaries = self.char_boundaries(ch)
            self.draw_char(ch, pos, y, *args, **kwargs)
            pos += self.char_width(ch) + 1

    def text_width(self, text):
        """ Return the pixel width of the specified text message assuming non proportional font """
        return len(text) * (self._font_width + 1)

    def char_boundaries(self, ch):
        """ Returns the boundaries of a char """

        index_start = index_end = -1
        line = self.get_char(ch)
        # Go through each column of the character.
        for char_x in range(self._font_width):
            # Grab the byte for the current column of font data.
            if (line[char_x] > 0 and index_start == -1): index_start = char_x
            if (line[char_x] > 0 and char_x > index_end):  index_end = char_x

        return (index_start, index_end)

    def char_width(self, ch):
        """ Return the pixel width of the specified caracter """

        boundaries = self.char_boundaries(ch)
        if boundaries[0] < 0: return 2 # special case to increase slightly the spaces
        return boundaries[1] - boundaries[0] +1
