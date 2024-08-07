from sys import argv
import sys
from threading import Thread

import requests
from gdep.LCD144 import KEY_UP_PIN, KEY_DOWN_PIN, KEY_PRESS_PIN, KEY1_PIN, LCD_LCD144
import time
import RPi.GPIO as GPIO

from modules.connectinfo.connectinfo_main import connectInfo
# from modules.servos.servos_main import servos
# from modules.strand.strand_main import strand
# from modules.pong.module_pong import modulePong
# from modules.update.module_update import moduleUpdate
# from modules.interface.module_interface import moduleInterface

lcd = LCD_LCD144()

mode = -1
selected = 0

modules = [
    connectInfo(lcd),
    # servos(lcd),
    # strand(lcd),
    # modulePong(lcd),
    # moduleUpdate(lcd),
    # moduleInterface(lcd)
]

runFlag = 1

if __name__=='__main__':

    if sys.argv[1] == "3":
        mode = 3

    while runFlag:

        if mode == -1:
                    
            if GPIO.input(KEY1_PIN) == 0: # press pin1 - close  
                runFlag = 0

            if GPIO.input(KEY_UP_PIN) == 0:
                if selected > 0:
                    selected -= 1
            if GPIO.input(KEY_DOWN_PIN) == 0:
                if selected < len(modules) - 1:
                    selected += 1
            if GPIO.input(KEY_PRESS_PIN) == 0:
                mode = selected;

            lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
            lcd.draw.text((5,112), "(c)" ,fill=(255,255,255,128))
            lcd.draw.text((30,108), "Maksim Edush" ,fill=(255,255,255,128))
            lcd.draw.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

            i = 0
            for module in modules:
                if selected == i:
                    lcd.draw.text((5,5 + 10*i), module.title(), fill=(255,0,0,128))
                else:
                    lcd.draw.text((5,5 + 10*i), module.title(), fill=(255,255,255,128))
                i+=1

            lcd.disp.LCD_ShowImage(lcd.image,0,0)
            time.sleep(0.1)

        else:
            print('mode', mode)
            modules[mode].run();
            mode = -1;
        
    lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
    lcd.disp.LCD_ShowImage(lcd.image,0,0)