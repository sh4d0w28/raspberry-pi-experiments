import time
import threading

from wrappers.wrap_lcd import wrap_LCD
from event.event import Event, eventLoop, pinstate;
from gdep.LCD144_pins import *

from modules.connectinfo.connectinfo import connectInfo

modules = [
    connectInfo()
]

lcd = wrap_LCD()

runFlag = 1
mode = -1
selected = 0


def key_event(pin, state):
    if pin == PIN_KEY.K1 and state == 1:
        runFlag = 0
    elif pin == PIN_KEY.UP and state == 1:
        if selected > 0:
            selected -= 1
    elif pin == PIN_KEY.DOWN and state == 1:
        if selected < len(modules) - 1:
            selected += 1
    elif pin == PIN_KEY.PRESS and state == 1:
        mode = selected;
    else:
        pass

event = Event()
event.reset()
event.register_listener(key_event)
thread = threading.Thread(target=eventLoop)


if __name__=='__main__':

    thread.start()
    
    while runFlag:

        if mode == -1:
            lcd.rectangle((0,0,128,128), outline=0, fill=0)

            lcd.rectangle((0,0,128,128), outline=0, fill=0)
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
            print('mode', mode)
            modules[mode].run()
            mode = -1
        
    lcd.clear()