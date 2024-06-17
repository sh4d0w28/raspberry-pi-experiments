from wrappers.wrap_lcd import wrap_LCD
from gdep.LCD144_pins import PIN_KEY
from event.event import Event

import time

class basemodule:
    
    # global values for module
    lcd: wrap_LCD = wrap_LCD()
    runFlag = 1

    def __init__(self) -> None:
        self.init()

    def run(self):

        event = Event()
        event.reset()
        event.register_listener(self.key_event)

        while self.runFlag == 1:
            self.mainFlow()
            self.lcd.update()
            time.sleep(0.05)

    def key_event(self, pin, state):
        pass;

    # will display in list of modules on the main screen
    def title(self):
        return "DEFINE TITLE():STRING"

    def init(self):
        pass

    # main loop of application
    def mainFlow(self):
        pass