
from gdep.LCD144 import LCD_LCD144

#singleton
class wrap_LCD:

    _instance = None
    _lcd: LCD_LCD144 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(wrap_LCD, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # prevent constuctor from call several time
        if not hasattr(self, 'initialized'):
            self._lcd = LCD_LCD144()
            self.initialized = True
        
    def text(self, xy, text, fill=(255,255,255,128), font=None):
        self._lcd.draw.text(xy, text, fill, font)
    
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._lcd.draw.rectangle(xy, fill, outline, width)

    def update(self):
        self._lcd.disp.LCD_ShowImage(self._lcd.image,0,0)

    def clear(self):
        self._lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.update()