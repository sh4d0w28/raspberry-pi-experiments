from gdep.LCD_1in44 import LCD, SCAN_DIR_DFT
import RPi.GPIO as GPIO
from PIL import Image,ImageDraw,ImageFont,ImageColor

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

class LCD_LCD144:

    def __init__(self):
        #init GPIO
        GPIO.setmode(GPIO.BCM) 
        GPIO.cleanup()
        GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
        GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

        # 240x240 display with hardware SPI:
        disp = LCD()
        Lcd_ScanDir = SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
        disp.LCD_Init(Lcd_ScanDir)
        disp.LCD_Clear()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = 128
        self.height = 128
        image = Image.new('RGB', (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        disp.LCD_ShowImage(image,0,0)

        self.disp = disp;
        self.draw = draw;
        self.image = image;

    def clear(self):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.disp.LCD_ShowImage(self.image,0,0)