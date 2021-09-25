import os
from modules.update.githubutil import githubutil
from gdep.LCD144 import KEY1_PIN, KEY2_PIN
from modules.basemodule import basemodule

class moduleUpdate(basemodule):
    
    def title(self):
        return "Update"

    def button_key_1_pin_handler(self):
        githubutil.fullUpdate();

    def button_key_2_pin_handler(self):
        os.execv()

    def init(self):
        self.buttonPressHandlers[KEY1_PIN] = self.button_key_1_pin_handler
        self.buttonPressHandlers[KEY2_PIN] = self.button_key_2_pin_handler

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.lcd.draw.text((80,27), "Download" ,fill=(255,255,255,128))
        self.lcd.draw.text((85,58), "Restart" ,fill=(255,255,255,128))
        self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)