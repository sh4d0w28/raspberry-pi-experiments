import json
import psutil
import subprocess
import time
from datetime import datetime
from modules.basemodule import basemodule
from modules.connectinfo.network_helper import networkHelper
from modules.connectinfo.ngrok_helper import get_ngrok_status, start_ngrok, stop_ngrok, toggle_ngrok
from gdep.LCD144 import KEY3_PIN

class connectInfo(basemodule):

    def switch_ngrok(self):
        toggle_ngrok()

    def init(self):
        self.lasttamp = datetime.now()

    buttonPressHandlers = {
        KEY3_PIN: switch_ngrok
    }

    def title(self):
        return "Connection status"

    def cpu_temp(self):
        try:
            output = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
            temp = int(output)
            return round(temp / 1000, 1)
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def docker_stat(self):
        try:
            output = subprocess.check_output(['docker', 'stats', '--no-stream', '--format', 'json'])
            decoded_data = output.decode('utf-8')
            json_objects = decoded_data.strip().split('\n')
            return json_objects
        except IndexError as e:
            return ""
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

        wifisid = networkHelper.getWifiSsid()
        extIp = networkHelper.getExtIp()
        temp = self.cpu_temp()
        dstat = self.docker_stat()

        cpu_utilization = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        self.lcd.draw.text((2,5), "WiFi:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,5), wifisid ,fill=(255,255,255,128))

        self.lcd.draw.text((2,15), "IP:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,15), extIp ,fill=(255,255,255,128))

        self.lcd.draw.text((2,25), "C:" ,fill=(255,255,255,128))
        self.lcd.draw.text((20,25), str(cpu_utilization) + "%" ,fill=(255,255,255,128))

        self.lcd.draw.text((60,25), "M:" ,fill=(255,255,255,128))
        self.lcd.draw.text((80,25), str(memory_info.percent) + "%" ,fill=(255,255,255,128))

        self.lcd.draw.text((2,45), "Temp:", fill=(255,255,255,128))
        self.lcd.draw.text((33,45), str(temp) + " C", fill=(255,255,255,128))

        i = 0
        for obj in dstat:
            parsed_obj = json.loads(obj)
            self.lcd.draw.text((2,55 + i*20), parsed_obj.get('Name').replace('sonarqube',''))
            self.lcd.draw.text((5,65 + i*20),"C: " + parsed_obj.get('CPUPerc') + " M: " + parsed_obj.get('MemPerc'))
            i = i + 1

        self.lcd.draw.text((2,105), "Tm:" ,fill=(255,255,255,128))
        self.lcd.draw.text((33,105), datetime.now().strftime("%H:%M:%S") ,fill=(255,255,255,128))

        time.sleep(5)
