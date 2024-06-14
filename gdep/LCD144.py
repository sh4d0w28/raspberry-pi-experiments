from gdep.LCD_1in44 import LCD, SCAN_DIR_DFT
import RPi.GPIO as GPIO
from PIL import Image,ImageDraw,ImageFont,ImageColor
from LCD144_pins import PIN_KEY

class LCD_LCD144:

    def __init__(self):
        #init GPIO
        GPIO.setmode(GPIO.BCM) 
        GPIO.cleanup()
        GPIO.setup(PIN_KEY.UP,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
        GPIO.setup(PIN_KEY.DOWN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(PIN_KEY.LEFT,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
        GPIO.setup(PIN_KEY.RIGHT,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(PIN_KEY.PRESS,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
        GPIO.setup(PIN_KEY.K1,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(PIN_KEY.K2,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
        GPIO.setup(PIN_KEY.K3,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

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