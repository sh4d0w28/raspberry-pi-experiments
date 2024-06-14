
from gdep.LCD144 import LCD_LCD144

class wrap_LCD:

    _lcd: LCD_LCD144 

    def __init__(self):
        self._lcd = LCD_LCD144()
    
    def text(self, xy, text, fill=None, font=None):
        self._lcd.draw.text(xy, text, fill, font)
    
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._lcd.draw.rectangle(xy, fill, outline, width)

    def update(self):
        self._lcd.disp.LCD_ShowImage(self._lcd.image,0,0)

    def clear(self):
        self._lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.update()