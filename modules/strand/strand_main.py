import math
import time

from PIL import Image
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
    image = None
    mode = 0
    modes = ['warning', 'rainbow', 'network']

    def title(self):
        return "LEDs"

    def netkey(self):
        return "led_setting"

    def init(self):
        self.strip = Adafruit_NeoPixel(self.__LED_COUNT, self.__LED_PIN, self.__LED_FREQ_HZ, self.__LED_DMA, self.__LED_INVERT, self.__LED_BRIGHTNESS, self.__LED_CHANNEL)
        self.strip.begin()
        self.image = Image.open("/home/pi/robot/work/g1366.bmp")
        return super().init()

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.lcd.draw.text((2,5), "LED" ,fill=(255,255,255,128))
        
        self.lcd.draw.bitmap((34,34), self.image)    

        if self.mode == 0:
            self.warning(0)
        elif self.mode == 1:
            self.rainbowCycle(1)
        elif self.mode == 2:
            self.setNetColors()
        else:
            self.clear()

        self.lcd.draw.text((2,20), self.modes[self.mode],fill=(255,255,255,128))
                
    def button_key_1_pin_handler(self):
        if self.mode < 2:
            self.mode = self.mode + 1
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

    def setNetColors(self, wait_ms=100):
        colors = self.netsettings["colors"]

        range1 = len(colors)
        range2 = self.strip.numPixels()
        rangeN = range1
        restRange = range2-range1
        if range2 < range1:
            rangeN = range2
            restRange = range1-range2

        for i in range(rangeN):
            try: 
                h = colors[i].lstrip('#')
                tup = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                self.strip.setPixelColor(i, Color(tup[0], tup[1], tup[2]))
            except Exception:
                print('FAT CHANCE!')
        
        for i in range(restRange):
            self.strip.setPixelColor(rangeN + i, Color(0,0,0))

        self.strip.show()
        time.sleep(wait_ms/1000.0)

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