import os
import sys
import RPi.GPIO as GPIO
import json
import time
import subprocess

class moduleUpdate:
    
    def update(self):
        try:
            output = subprocess.run(['cd /home/pi/robot/work && git pull'], shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
            return ""

    lcd = None
    runFlag = None

    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "UPDATE"

    def run(self):
        self.runFlag = 1
        self.update()
        os.execv(sys.executable, ['python3'] + [os.path.abspath(sys.argv[0])])