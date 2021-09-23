import RPi.GPIO as GPIO
import json
import time
import subprocess

class moduleTitle:
    
    tcpUrl = ""
    httpUrl = ""

    def getWifiSsid(self):
        try:
            output = subprocess.check_output(['/usr/sbin/iwgetid'])
            ssid = str(output).split('"')[1]
            return ssid
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def getNgrokIp(self):
        try:
            output = subprocess.check_output(['curl http://127.0.0.1:4040/api/tunnels | jq ".tunnels[].public_url"'], shell=True)
            urls = output.splitlines()
            for url in urls:
                cleanurl = url.strip(b'"') 
                if cleanurl.startswith(b'tcp'):
                    self.tcpUrl = cleanurl
                if cleanurl.startswith(b'https'):
                    self.httpUrl = cleanurl.replace(b".ngrok.io", b"")
        except IndexError as e:
            return
        except subprocess.CalledProcessError as e:
            print(e.output)
            return

    def getExtIp(self):
        try:
            output = subprocess.check_output(['hostname', '-I'])
            ip = str(output).split(' ')[0].split("'")[1]
            return ip
        except IndexError as e:
            return ""
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
            self.getNgrokIp()
            
            self.lcd.draw.text((2,5), "WiFi:" ,fill=(255,255,255,128))
            self.lcd.draw.text((33,5), wifisid ,fill=(255,255,255,128))

            self.lcd.draw.text((2,15), "IP:" ,fill=(255,255,255,128))
            self.lcd.draw.text((33,15), extIp ,fill=(255,255,255,128))
            
            try:
                tcps = self.tcpUrl.split(b':')
                hcps = self.httpUrl.split(b':')
                
                self.lcd.draw.text((2,35), "TCP:" ,fill=(128,255,128,128))
                self.lcd.draw.text((33,35), tcps[1][2:] ,fill=(128,255,128,128))
                self.lcd.draw.text((2,45), "PORT:" ,fill=(128,255,128,128))
                self.lcd.draw.text((33,45), tcps[2] ,fill=(128,255,128,128))

                self.lcd.draw.text((2,65), "HTTP:" ,fill=(128,255,128,128))
                self.lcd.draw.text((2,75), hcps[1][2:] ,fill=(128,255,128,128))
                self.lcd.draw.text((70,85), ".ngrok.io" ,fill=(128,255,128,128))
                
            except Exception as e:
                print(e)

            self.lcd.draw.text((5,112), "(c)" ,fill=(255,255,255,128))
            self.lcd.draw.text((30,108), "Maksim Edush" ,fill=(255,255,255,128))
            self.lcd.draw.text((40,118), "sh4d0w28" ,fill=(255,255,255,128))

            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

            time.sleep(0.1)