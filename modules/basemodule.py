from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_PRESS_PIN, KEY_RIGHT_PIN, KEY_UP_PIN, LCD_LCD144
import RPi.GPIO as GPIO
import threading
import time

class basemodule:
    
    # global values for module
    lcd: LCD_LCD144
    runFlag = None
    buttonStates = {
        KEY1_PIN: 1,
        KEY2_PIN: 1,
        KEY3_PIN: 1,
        KEY_RIGHT_PIN: 1,
        KEY_DOWN_PIN: 1,
        KEY_UP_PIN: 1,
        KEY_PRESS_PIN: 1,
        KEY_LEFT_PIN: 1
    }
    
    def default_exit_on_press_left(self):
        self.runFlag = 0

    buttonPressHandlers = {
        KEY_LEFT_PIN: default_exit_on_press_left
    }

    def __init__(self, lcd) -> None:
        self.lcd = lcd
        self.init()

    def buttonHandler(self):
        while self.runFlag == 1:
          for button in self.buttonStates:
            if GPIO.input(button) != self.buttonStates[button]:  
              self.buttonStates[button] = GPIO.input(button)
              if GPIO.input(button) == 0 and self.buttonPressHandlers.get(button):
                self.buttonPressHandlers.get(button)(self)

    def run(self):
        self.runFlag = 1
        process = threading.Thread(target=self.buttonHandler)
        process.start();
        while self.runFlag == 1:
            self.mainFlow()
            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)
            time.sleep(0.05)

    def title(self):
        return "DEFINE TITLE():STRING"

    def init(self):
        pass

    def mainFlow(self):
        pass