from modules.basemodule import basemodule
from gdep.LCD144 import KEY1_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_UP_PIN
from modules.servos.PCA9685 import PCA_PCA9685
import json, time

class servos(basemodule):
    pwm = None

    servos = {1: 'S1', 2: 'S2', 3: 'S3', 4: 'S4', 5: 'S5', 6: 'S6'}
    servos_values = {1: 1000, 2: 800, 3: 1200, 4: 1300, 5: 1400, 6: 1500}
    servos_max_value = {1: 1700, 2: 800, 3: 3200, 4: 2500, 5: 2300, 6: 2700}
    servos_min_value = {1: 1000, 2: 300, 3: 800, 4: 600, 5: 800, 6: 800}
    enabled = 1

    def init(self):
        self.pwm = PCA_PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)

    def title(self):
        return "Servos"

    def moveTo(self, servos_goal = {}, timetoreach = 5, delay = 0):
        sleeptime = 0.1
        dx = {1:0,2:0,3:0,4:0,5:0,6:0}
        steps = int(timetoreach / sleeptime)
        for i in range(1,7):
            if servos_goal.get(i):
                dx[i] = ( servos_goal.get(i) - self.servos.get(i) ) / steps
            else:
                dx[i] = 0
                servos_goal[i] = self.servos[i]

        for i in range(0, steps):
            for i in range(1,7):
                self.servos[i] += dx.get(i)
            self.set_servos()
            time.sleep(sleeptime)
        for i in range(1,7):
            self.servos[i] = servos_goal.get(i)
        self.set_servos()

    def button_key_1_pin_handler(self):
        self.move_left()
        return

    def button_key_3_pin_handler(self):
        self.move_right()
        return

    def button_up_handler(self):
        self.servos_values[self.enabled] += 100

    def button_down_handler(self):
        self.servos_values[self.enabled] -= 100

    def button_key_2_pin_handler(self):
        self.moveTo({1: 1700, 2: 300}, 10)
        self.moveTo({1: 1000, 2: 300}, 10)

    buttonPressHandlers = {
        KEY1_PIN: button_key_1_pin_handler,
        KEY3_PIN: button_key_3_pin_handler,
        KEY_DOWN_PIN: button_down_handler,
        KEY_UP_PIN: button_up_handler
    }

    def move_right(self):
        if self.enabled > 1:
            self.enabled -= 1
        else:
            self.enabled = 6

    def move_left(self):
        if self.enabled < 6:
            self.enabled += 1
        else:
            self.enabled = 1

    def set_servos(self):
        for x in range(1, 7):
            self.pwm.setServoPulse(x, self.servos_values[x])

    def mainFlow(self):

        self.lcd.draw.rectangle((0, 0, 128, 128), outline=0, fill=0)

        for i in range(1, 7):
            if i == self.enabled:
                self.lcd.draw.text((10, 50 + 10 * i), str(self.servos_values[i]), fill=(255, 255, 255, 128))
            else:
                self.lcd.draw.text((10, 50 + 10 * i), str(self.servos_values[i]), fill=(255, 0, 0, 128))

        self.set_servos()
