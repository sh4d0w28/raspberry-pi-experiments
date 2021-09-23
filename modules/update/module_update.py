import os
import sys
import RPi.GPIO as GPIO
from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY_LEFT_PIN

import json
import time
import subprocess

class moduleUpdate:
    
    def update(self):
        self.status = "downloading..."
        try:
            output = subprocess.check_output(['cd /home/pi/robot/work && git pull'], shell=True)
            if str(output) == 'b\'Already up to date.\\n\'':
                self.status = "no new data"
            else:
                self.status = "download ok"
        except subprocess.CalledProcessError as e:
            print(e.output)
            self.status = "download failed"

        

    lcd = None
    runFlag = None
    status = ""

    downloading = False

    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "UPDATE"

    def run(self):

        self.runFlag = 1
        while self.runFlag == 1:

            self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
            
            if GPIO.input(5) == 0: # press left - close  
                self.runFlag = 0

            if GPIO.input(KEY1_PIN) == 0: # update
                self.update()

            if GPIO.input(KEY2_PIN) == 0: # restart
                os.execv(sys.executable, ['python3'] + [os.path.abspath(sys.argv[0])])

            self.lcd.draw.text((80,27), "Download" ,fill=(255,255,255,128))
            
            self.lcd.draw.text((85,58), "Restart" ,fill=(255,255,255,128))

            self.lcd.draw.text((5,90), self.status ,fill=(255,0,0,128))

            
            self.lcd.draw.text((5,112), "(c)" ,fill=(255,255,255,128))
            self.lcd.draw.text((30,108), "Maksim Edush" ,fill=(255,255,255,128))
            self.lcd.draw.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

            time.sleep(0.1)