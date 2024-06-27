from PIL import Image
from gdep.LCD144 import KEY1_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_UP_PIN
import RPi.GPIO as GPIO
import time
import subprocess

class modulePong:
    
    lcd = None
    runFlag = None
    
    pad1pos = 64
    pad2pos = 64
    ballposX = 64
    ballposY = 64
    balldx = 3
    balldy = 2
    win = 0

    wins1 = 0
    wins2 = 0


    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "PING-PONG"
    
    def drawpads(self, clear):
        if (clear == 1):
            self.lcd.draw.rectangle((1,self.pad1pos-20,5,self.pad1pos+20), outline=0, fill=0)
            self.lcd.draw.rectangle((123,self.pad2pos-20,128,self.pad2pos+20), outline=0, fill=0)
        else:
            self.lcd.draw.rectangle((1,self.pad1pos-20,5,self.pad1pos+20), outline=0xffffff, fill=0xffffff)
            self.lcd.draw.rectangle((123,self.pad2pos-20,128,self.pad2pos+20), outline=0xffffff, fill=0xffffff)

    def drawball(self, clear):
        if(clear == 1):
            self.lcd.draw.ellipse((self.ballposX-3,self.ballposY-3,self.ballposX+3,self.ballposY+3), outline=0, fill=0)  
        else:
            self.lcd.draw.ellipse((self.ballposX-3,self.ballposY-3,self.ballposX+3,self.ballposY+3), outline=0xffffff, fill=0xffffff)  

    def pongx(self):
        self.balldx = - self.balldx

    def step(self):
        
        if(self.ballposY > 121 or self.ballposY < 7):
            self.balldy = - self.balldy

        # if we catch the ball
        if(self.ballposX < 10):
            if (self.pad1pos + 20 > self.ballposY and self.ballposY > self.pad1pos - 20):
                self.pongx()
            else:
                self.win = 2

        # if we catch the ball
        if(self.ballposX > 118):
            if(self.pad2pos+20 > self.ballposY and self.ballposY > self.pad2pos - 20):
                self.pongx()
            else:
                self.win = 1

        self.ballposX += self.balldx
        self.ballposY += self.balldy

    def inputs(self):
        if GPIO.input(KEY_UP_PIN) == 1: # button is released       
            self.pad1pos += 2;
        if GPIO.input(KEY_DOWN_PIN) == 1: # button is released       
            self.pad1pos -= 2;
            
        if GPIO.input(KEY1_PIN) == 1: # button is released       
            self.pad2pos += 2;
        if GPIO.input(KEY3_PIN) == 1: # button is released       
            self.pad2pos -= 2;

    def drawScore(self):
        self.lcd.draw.text((50,20),str(self.wins1),fill=(255,255,255,128))
        self.lcd.draw.text((78,20),str(self.wins2),fill=(255,255,255,128))
        

    def reset(self):
        self.lcd.clear()
        self.pad1pos = 64
        self.pad2pos = 64
        self.ballposX = 64
        self.ballposY = 65
        self.balldx = 3
        self.balldy = 2
        self.win = 0

    def checkwin(self):
        if(self.win == 1 or self.win == 2):
            if(self.win == 1):
                self.wins1 += 1
            if(self.win == 2):
                self.wins2 += 1
            self.reset()

    def drawmidline(self):
        for y in range(0, 128, 6):
            self.lcd.draw.line([(64, y), (64, y+2)], fill=(170, 170, 170))

    def run(self):
        self.runFlag = 1

        image = Image.open("logo_128x128.bmp")
        self.lcd.disp.LCD_ShowImage(image,0,0)

        time.sleep(2);

        self.lcd.clear()

        while self.runFlag == 1:
            
            if GPIO.input(5) == 0: # press left - close  
                self.runFlag = 0

            self.drawpads(1)
            self.drawball(1)
            self.inputs()
            self.step()
            self.checkwin()
            self.drawpads(0)
            self.drawball(0)
            self.drawmidline()
            self.drawScore()
            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

            time.sleep(0.1)