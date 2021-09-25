from modules.basemodule import basemodule
from gdep.LCD144 import KEY1_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_UP_PIN
from modules.servos.PCA9685 import PCA_PCA9685

class servos(basemodule):
    
    pwm = None
    
    servos = { 1: 'S1', 2: 'S2', 3: 'S3', 4: 'S4', 5: 'S5', 6: 'S6' }
    servos_values = { 1: 1000, 2: 1100, 3: 1200, 4: 1300, 5: 1400, 6: 1500 }
    servos_max_value = { 1: 1700, 2: 2600, 3: 3200, 4: 2500, 5: 2300, 6: 2700 }
    servos_min_value = {1: 1000, 2: 300, 3: 800, 4: 600, 5: 800, 6: 800 }
    enabled = 1

    def init(self):
        self.pwm = PCA_PCA9685(0x40, debug=False)
        self.pwm.setPWMFreq(50)

    def title(self):
        return "Servos"

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

    def move_up(self):
        self.servos_values[self.enabled] += 100

    def move_down(self):
        self.servos_values[self.enabled] -= 100

    def set_servos(self):
        self.pwm.setServoPulse(1,self.servos_values[1])
        self.pwm.setServoPulse(2,self.servos_values[2])
        self.pwm.setServoPulse(3,self.servos_values[3])
        self.pwm.setServoPulse(4,self.servos_values[4])
        self.pwm.setServoPulse(5,self.servos_values[5])
        self.pwm.setServoPulse(6,self.servos_values[6])

    def up_button_handler(self):
        self.lcd.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)  #Up        
        self.move_up()        

    def mainFlow(self):
        
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

        # with canvas(device) as draw:
        if self.buttonStates.get(KEY_UP_PIN) == 0: # button is released       
            self.lcd.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)  #Up        
            self.move_up()        

        else: # button is pressed:
            self.lcd.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up filled
            
        if self.buttonStates.get(KEY_LEFT_PIN) == 0: # button is released
            self.lcd.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)  #left
        else: # button is pressed:       
            self.lcd.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left filled
                        
        if self.buttonStates.get(KEY_DOWN_PIN) == 0: # button is released
            self.lcd.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00) #down
            self.move_down()
        else: # button is pressed:
            self.lcd.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down filled
            
        if self.buttonStates.get(KEY1_PIN) == 0: # button is released
            self.lcd.draw.ellipse((70,0,90,20), outline=255, fill=0xff00) #A button
            self.move_right()                         
        else: # button is pressed:
            self.lcd.draw.ellipse((70,0,90,20), outline=255, fill=0) #A button filled
            
        if self.buttonStates.get(KEY3_PIN) == 0: # button is released
            self.lcd.draw.ellipse((70,40,90,60), outline=255, fill=0xff00) #A button
            self.move_left()            
        else: # button is pressed:
            self.lcd.draw.ellipse((70,40,90,60), outline=255, fill=0) #A button filled
        
        for i in range(1,7):
            whitefill = (255,255,255,128)
            if(i == self.enabled):
                self.lcd.draw.text((10,50+10 * i), str(self.servos_values[i]), fill=(255,255,255,128))
            else:
                self.lcd.draw.text((10,50+10 * i), str(self.servos_values[i]), fill=(255,0,0,128))
        
        self.set_servos()