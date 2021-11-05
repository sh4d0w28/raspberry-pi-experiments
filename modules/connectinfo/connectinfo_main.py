import math
from datetime import datetime
from modules.basemodule import basemodule
from modules.connectinfo.network_helper import networkHelper

class connectInfo(basemodule):

    laststamp = None
    sincetime = "NONE"

    def init(self):
        self.lasttamp = datetime.now()

    def title(self):
        return "Connection status"

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

        wifisid = networkHelper.getWifiSsid()
        extIp = networkHelper.getExtIp()
        ngrokIps = networkHelper.getNgrokIp()
            
        self.lcd.draw.text((2,5), "WiFi:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,5), wifisid ,fill=(255,255,255,128))

        self.lcd.draw.text((2,15), "IP:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,15), extIp ,fill=(255,255,255,128))

        try:
            tcps = ngrokIps['tcpurl'].split(b':')
            self.lcd.draw.text((2,35), "TCP:" ,fill=(128,255,128,128))
            self.lcd.draw.text((33,35), tcps[1][2:] ,fill=(128,255,128,128))
            self.lcd.draw.text((2,45), "PORT:" ,fill=(128,255,128,128))
            self.lcd.draw.text((33,45), tcps[2] ,fill=(128,255,128,128))
        except Exception as e:
            print(e)

        try:
            hcps = ngrokIps['httpurl'].split(b':')
            self.lcd.draw.text((2,65), "HTTP:" ,fill=(128,255,128,128))
            self.lcd.draw.text((2,75), hcps[1][2:] ,fill=(128,255,128,128))
            self.lcd.draw.text((70,85), ".ngrok.io" ,fill=(128,255,128,128))
        except Exception as e:
            print(e)

        self.lcd.draw.text((2,105), "SYNC:" + str(self.sincetime) ,fill=(255,255,255,128))

    def netkey(self):
        return "connect"
    
    def netevent(self):
        if(self.laststamp == None):
            self.laststamp = datetime.now()

        timespan = (datetime.now() - self.laststamp).total_seconds()
        self.sincetime = str(round(timespan, 2)) + " sec ago";
        self.laststamp = datetime.now() 