import RPi.GPIO as GPIO
import json
import time
import subprocess

class moduleTitle:
    
    def getWifiSsid(self):
        try:
            output = subprocess.check_output(['/usr/sbin/iwgetid'])
            ssid = str(output).split('"')[1]
            return ssid
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def getNgrokIp(self):
        try:
            output = subprocess.check_output(['curl http://127.0.0.1:4040/api/tunnels | jq ".tunnels[0].public_url"'], shell=True)
            url = str(output).split('"')[1]
            return url
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def getExtIp(self):
        try:
            output = subprocess.check_output(['hostname', '-I'])
            ip = str(output).split(' ')[0].split("'")[1]
            return ip
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    lcd = None
    runFlag = None

    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "Information"

    def run(self):
        self.runFlag = 1
        while self.runFlag == 1:
            
            if GPIO.input(5) == 0: # press left - close  
                self.runFlag = 0

            self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

            wifisid = self.getWifiSsid()
            extIp = self.getExtIp()
            ngrokUrl = self.getNgrokIp()
            
            self.lcd.draw.text((5,5), "WiFi: " + wifisid ,fill=(255,255,255,128))
            self.lcd.draw.text((5,15), "IP: " + extIp ,fill=(255,255,255,128))
            
            try:
                urls = ngrokUrl.split(":")
                self.lcd.draw.text((5,25), "NGROK" ,fill=(128,255,128,128))
                self.lcd.draw.text((5,35), urls[1] ,fill=(128,255,128,128))
                self.lcd.draw.text((5,45), "port: " + urls[2] ,fill=(128,255,128,128))
            except Exception as e:
                print(e)

            self.lcd.draw.text((5,112), "(c)" ,fill=(255,255,255,128))
            self.lcd.draw.text((30,108), "Maksim Edush" ,fill=(255,255,255,128))
            self.lcd.draw.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

            time.sleep(0.1)