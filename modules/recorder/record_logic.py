import subprocess;

class actionRecord:

 def record(self):
    return subprocess.Popen(['adb shell getevent -lt | grep EV_ > /home/pi/robot/work/log.txt'], shell=True)
