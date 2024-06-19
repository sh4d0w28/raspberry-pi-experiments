import time
from datetime import datetime
from enums.PinKey import PinKey
from modules.basemodule import basemodule
from modules.connectinfo.network_helper import networkHelper

class connectInfo(basemodule):

    def key_event(self, pin, state):
        if pin == PinKey.K1 and state == 1:
            self.runFlag = 0

    def init(self):
        self.lasttamp = datetime.now()

    def title(self):
        return "Connection status"

    def mainFlow(self):
        self.lcd.rectangle((0,0,128,128), outline=0, fill=0)

        wifisid = networkHelper.getWifiSsid()
        extIp = networkHelper.getExtIp()
        sshString = networkHelper.autossh()
            
        self.lcd.text((2,5), "WiFi:")
        self.lcd.text((33,5), wifisid)

        self.lcd.text((2,15), "IP:")
        self.lcd.text((33,15), extIp)

        self.lcd.text((2,25), "SSH: " + sshString)

        self.lcd.text((2,105), "SYNC:" + str(datetime.now().time()))

        time.sleep(1)