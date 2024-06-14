import math
from datetime import datetime
from modules.basemodule import basemodule
from modules.connectinfo.network_helper import networkHelper

class connectInfo(basemodule):

    def init(self):
        self.lasttamp = datetime.now()

    def title(self):
        return "Connection status"

    def mainFlow(self):
        self.lcd.rectangle((0,0,128,128), outline=0, fill=0)

        wifisid = networkHelper.getWifiSsid()
        extIp = networkHelper.getExtIp()
            
        self.lcd.text((2,5), "WiFi:" ,fill=(255,255,255,128))
        self.lcd.text((33,5), wifisid ,fill=(255,255,255,128))

        self.lcd.text((2,15), "IP:" ,fill=(255,255,255,128))
        self.lcd.text((33,15), extIp ,fill=(255,255,255,128))

        self.lcd.text((2,105), "SYNC:" + str(self.sincetime) ,fill=(255,255,255,128))