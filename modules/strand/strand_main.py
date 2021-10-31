import time
from modules.basemodule import basemodule
from rpi_ws281x import *
from math import trunc
from gdep.LCD144 import KEY1_PIN, KEY_LEFT_PIN

class strand(basemodule):

    # LED strip configuration:
    __LED_COUNT      = 15      # Number of LED pixels.
    __LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    # __LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    __LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    __LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    __LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    __LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    __LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    strip = None

    mode = 0
    modes = ['warning', 'rainbow']

    def title(self):
        return "LEDs"

    def init(self):
        self.strip = Adafruit_NeoPixel(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL)
        self.strip.begin()
        return super().init()

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.lcd.draw.text((2,5), "LED" ,fill=(255,255,255,128))
        self.lcd.draw.text((2,20), self.modes[self.mode],fill=(255,255,255,128))
        if self.mode == 0:
            self.warning(0)
        else:
            self.rainbowCycle(1)
                
    def button_key_1_pin_handler(self):
        if self.mode == 0:
            self.mode = 1
        else:
            self.mode = 0
        print('mode:', self.mode)

    def button_key_left_pin_handler(self):
        self.mode = -1
        self.clean()
        self.runFlag = 0

    buttonPressHandlers = {
        KEY_LEFT_PIN: button_key_left_pin_handler,
        KEY1_PIN: button_key_1_pin_handler
    }

    def clean(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0,0,0))
        self.strip.show()

    def warning(self, mode, wait_ms=50):
        for r in range(50,10,-5):
            
            if self.mode != mode:
                return
            
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(trunc(255*r/400),trunc(60*r/400),0))
            self.strip.show();
            time.sleep(wait_ms/1000.0)
        for r in range(10,50,5):
            
            if self.mode != mode:
                return

            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(trunc(255*r/400),trunc(60*r/400),0))
            self.strip.show();
            time.sleep(wait_ms/1000.0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(trunc(pos * 3 / 2), trunc((255 - pos * 3) / 2), 0)
        elif pos < 170:
            pos -= 85
            return Color(trunc((255 - pos * 3)/2), 0, trunc((pos * 3)/2))
        else:
            pos -= 170
            return Color(0, trunc((pos * 3)/2), trunc((255 - pos * 3)/2))

    def rainbowCycle(self, mode, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        numPix = self.strip.numPixels()
        for j in range(256*iterations):
            
            if self.mode != mode:
                return

            for i in range(numPix):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / numPix) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)