import time

import threading

from enums.PinKey import PinKey;
from glbl.EventManager import EventManager

from glbl.LcdEmulator import LcdEmulator
#from wrappers.wrap_lcd import wrap_LCD
#lcd = wrap_LCD()

lcd = LcdEmulator()

modules = []

runFlag = 1
mode = -1
selected = 0

def key_event(pin, state):
    global runFlag
    global selected
    global mode
        
    if pin == PinKey.K1 and state == 1:
        runFlag = 0
    elif pin == PinKey.UP and state == 1:
        if selected > 0:
            selected -= 1
    elif pin == PinKey.DOWN and state == 1:
        if selected < len(modules) - 1:
            selected += 1
    elif pin == PinKey.PRESS and state == 1:
        mode = selected
    else:
        pass


def titleThread():
    
    global runFlag
    global mode
    global selected
    
    eventManager = EventManager()
    eventManager.dropHandlers()
    eventManager.registerHandler(key_event)
    eventManager.start()
    
    while runFlag:

        if mode == -1:
            lcd.clear()
            lcd.text((5,112), "(c)" ,fill=(255,255,255,128))
            lcd.text((30,108), "Maksim Edush" ,fill=(255,255,255,128))
            lcd.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

            i = 0
            for module in modules:
                if selected == i:
                    lcd.text((5,5 + 10*i), module.title(), fill=(255,0,0,128))
                else:
                    lcd.text((5,5 + 10*i), module.title(), fill=(255,255,255,128))
                i+=1

            lcd.update()
            time.sleep(0.1)
        else:
            # start module in blocking thread. Title screen pause processing
            print('mode', mode)
            modules[mode].run()
            print('module done', mode)
            
            # return runFlags and control to title screen flow
            mode = -1
            runFlag = 1

            # restore event binding
            eventManager.dropHandlers()
            eventManager.registerHandler(key_event)
        
    eventManager.stop()
    lcd.clear()


if __name__=='__main__':

    t = threading.Thread(target= titleThread)
    t.start()
    lcd.start()
    
    