from gdep.LCD144 import KEY1_PIN, KEY2_PIN
import time
import threading
import RPi.GPIO as GPIO

from wrappers.wrap_lcd import wrap_LCD
from event.event import Event, eventLoop, pinstate;

lcd = wrap_LCD()

runFlag = 1

def key_event(pin, state):
    if pin == KEY1_PIN and state == 1:
        runFlag = 0

event = Event()
event.register_listener(key_event)

thread = threading.Thread(target=eventLoop)

if __name__=='__main__':

    thread.start()
    while runFlag:

        lcd.rectangle((0,0,128,128), outline=0, fill=0)
        lcd.text((40,80), str(pinstate(KEY2_PIN)) ,fill=(255,255,255,128))

        lcd.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

        lcd.update()
        time.sleep(0.1)
        
    lcd.clear()