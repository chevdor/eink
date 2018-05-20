# Based on MicroPython library for Waveshare 2.9" B/W/R e-paper display GDEW029Z10
# from https://github.com/mcauser/micropython-waveshare-epaper/blob/master/epaper2in9b.py

from micropython import const
from time import sleep_ms
import ustruct
import machine

# Display resolution
EPD_WIDTH  = const(128)
EPD_HEIGHT = const(296)

# Display commands
PANEL_SETTING                  = const(0x00)
POWER_SETTING                  = const(0x01)
POWER_OFF                      = const(0x02)
#POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON                       = const(0x04)
#POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START             = const(0x06)
#DEEP_SLEEP                     = const(0x07)
DATA_START_TRANSMISSION_1      = const(0x10)
#DATA_STOP                      = const(0x11)
DISPLAY_REFRESH                = const(0x12)
DATA_START_TRANSMISSION_2      = const(0x13)
#PLL_CONTROL                    = const(0x30)
#TEMPERATURE_SENSOR_COMMAND     = const(0x40)
#TEMPERATURE_SENSOR_CALIBRATION = const(0x41)
#TEMPERATURE_SENSOR_WRITE       = const(0x42)
#TEMPERATURE_SENSOR_READ        = const(0x43)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
#LOW_POWER_DETECTION            = const(0x51)
#TCON_SETTING                   = const(0x60)
TCON_RESOLUTION                = const(0x61)
#GET_STATUS                     = const(0x71)
#AUTO_MEASURE_VCOM              = const(0x80)
#VCOM_VALUE                     = const(0x81)
VCM_DC_SETTING_REGISTER        = const(0x82)
#PARTIAL_WINDOW                 = const(0x90)
#PARTIAL_IN                     = const(0x91)
#PARTIAL_OUT                    = const(0x92)
#PROGRAM_MODE                   = const(0xA0)
#ACTIVE_PROGRAM                 = const(0xA1)
#READ_OTP_DATA                  = const(0xA2)
#POWER_SAVING                   = const(0xE3)

# Display orientation
# ROTATE_0   = const(0) # 'portrait', connector up
# ROTATE_90  = const(1)
# ROTATE_180 = const(2)
# ROTATE_270 = const(3)

HIGH = const(1)
LOW = const(0)

class EPD:
    def __init__(self, spi, cs, dc, rst, busy, idle=HIGH):
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.dc = machine.Pin(dc, machine.Pin.OUT)
        self.rst = machine.Pin(rst, machine.Pin.OUT)
        self.busy = machine.Pin(busy, machine.Pin.IN)
        self.cs.value(HIGH)
        self.dc.value(LOW)
        self.rst.value(LOW)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        # self.rotate = ROTATE_0
        self.idle = idle

    def _command(self, command, data=None):
        self.dc.value(LOW) # write comment
        self.cs.value(LOW)
        self.spi.write(bytearray([command]))
        self.cs.value(HIGH)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc.value(HIGH) # write data
        self.cs.value(LOW)
        self.spi.write(data)
        self.cs.value(HIGH)

    def init(self):
        self.reset()
        self._command(BOOSTER_SOFT_START, b'\x17\x17\x17')
        self._command(POWER_ON)
        self.wait_until_idle()
        self._command(PANEL_SETTING, b'\x8F')
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x77')
        self._command(TCON_RESOLUTION, ustruct.pack(">BH", EPD_WIDTH, EPD_HEIGHT))
        self._command(VCM_DC_SETTING_REGISTER, b'\x0A')

    def wait_until_idle(self):
        while self.busy.value() == self.idle:
            sleep_ms(100)

    def reset(self):
        self.rst.value(LOW)
        sleep_ms(100)
        self.rst.value(HIGH)
        sleep_ms(100)

    def display_frame(self, frame_buffer_black, frame_buffer_red):
        print("display_frame")
        print("w", self.width)
        print("h", self.height)
        if (frame_buffer_black != None):
            self._command(DATA_START_TRANSMISSION_1)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                # print(i)
                self._data(bytearray([frame_buffer_black[i]]))
            sleep_ms(2)
        if (frame_buffer_red != None):
            self._command(DATA_START_TRANSMISSION_2)
            sleep_ms(2)
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([frame_buffer_red[i]]))
            sleep_ms(2)

        self._command(DISPLAY_REFRESH)
        self.wait_until_idle()

    # to wake call reset() or init()
    def sleep(self):
        self._command(VCOM_AND_DATA_INTERVAL_SETTING, b'\x37')
        self._command(VCM_DC_SETTING_REGISTER, b'\x00') # to solve Vcom drop
        self._command(POWER_SETTING, b'\x02\x00\x00\x00') # gate switch to external
        self.wait_until_idle()
        self._command(POWER_OFF)