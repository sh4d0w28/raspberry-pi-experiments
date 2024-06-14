from wrappers.wrap_lcd import wrap_LCD

import time

class basemodule:
    
    # global values for module
    lcd: wrap_LCD = wrap_LCD()
    
    runFlag = None

    def __init__(self) -> None:
        self.init()

    def run(self):
        self.runFlag = 1
        while self.runFlag == 1:
            self.mainFlow()
            self.lcd.update()
            time.sleep(0.05)

    # will display in list of modules on the main screen
    def title(self):
        return "DEFINE TITLE():STRING"

    def init(self):
        pass

    # main loop of application
    def mainFlow(self):
        pass