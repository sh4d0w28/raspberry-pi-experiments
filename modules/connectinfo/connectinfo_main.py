import json
import time
import psutil
from datetime import datetime
from modules.basemodule import basemodule
from modules.connectinfo.network_helper import networkHelper
from modules.connectinfo.monitor_helper import monitorHelper
from gdep.LCD144 import KEY3_PIN

class connectInfo(basemodule):

    def init(self):
        self.lasttamp = datetime.now()

    def title(self):
        return "Connection status"

    def drawData(self, wifiSid, extId, cpuUtilization, memoryUtilization, cpuTemp, dockerStat):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        
        self.lcd.draw.text((2,5), "WiFi:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,5), wifiSid ,fill=(255,255,255,128))
        
        self.lcd.draw.text((2,15), "IP:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,15), extId ,fill=(255,255,255,128))

        self.lcd.draw.text((2,25), "C:" ,fill=(255,255,255,128))
        self.lcd.draw.text((20,25), str(cpuUtilization) + "%" ,fill=(255,255,255,128))

        self.lcd.draw.text((60,25), "M:" ,fill=(255,255,255,128))
        self.lcd.draw.text((80,25), str(memoryUtilization) + "%" ,fill=(255,255,255,128))

        self.lcd.draw.text((2,45), "Temp:", fill=(255,255,255,128))
        self.lcd.draw.text((33,45), str(cpuTemp) + " C", fill=(255,255,255,128))

        i = 0
        for obj in dockerStat:
            parsed_obj = json.loads(obj)
            self.lcd.draw.text((2,55 + i*20), parsed_obj.get('Name').replace('sonarqube',''))
            self.lcd.draw.text((5,65 + i*20),"C: " + parsed_obj.get('CPUPerc') + " M: " + parsed_obj.get('MemPerc'))
            i = i + 1

        self.lcd.draw.text((2,105), "Tm:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,105), datetime.now().strftime("%H:%M:%S") ,fill=(255,255,255,128))


    def mainFlow(self):
        wifisid = networkHelper.getWifiSsid()
        extIp = networkHelper.getExtIp()
        temp = monitorHelper.cpu_temp()
        dstat = monitorHelper.docker_stat()
        cpu_utilization = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        
        self.drawData(wifisid, extIp, cpu_utilization, memory_info.percent, temp, dstat)
        
        time.sleep(5)
