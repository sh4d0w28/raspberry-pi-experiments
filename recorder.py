import sys
import time
from threading import Thread
from gdep.LCD144 import LCD_LCD144, KEY1_PIN, KEY3_PIN
import subprocess;
import RPi.GPIO as GPIO
import fcntl
import os

ON_POSIX = 'posix' in sys.builtin_module_names

def non_block_read():
    proc = subprocess.Popen(['adb shell getevent -lt | grep EV_'], shell=True, stdout=subprocess.PIPE)
    print('HERE!')
    fd = proc.stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    while True:
        try:
            print(proc.stdout.read())
        except:
            a = 1

def enqueue_output(out):
    print('RG',runFlag)
    while runFlag:
        line = out.readline()
        command = transform(line)
        process(command)
    out.close()

lcd = LCD_LCD144()
thread = None
proc = None
runFlag = False

actions = []
action = {}

event = 1

def process(line):
    global event 
    global action
    global actions

    if line['event'] == 'ABS_MT_POSITION_X' or line['event'] == 'ABS_MT_POSITION_Y' or line['event'] == 'BTN_TOUCH':
        print(line)

    # press screen or release, lock time
    if line['event'] == 'ABS_MT_POSITION_X':
        data = int(line['data'],16)
        if event == 1:
            action['x1'] = data
        elif event == 2:
            action['x2'] = data
    elif line['event'] == 'ABS_MT_POSITION_Y':
        data = int(line['data'],16)
        if event == 1:
            action['y1'] = data
        elif event == 2:
            action['y2'] = data
    elif line['event'] == 'BTN_TOUCH':
        if event == 1:
            event = 2
        else: 
            event = 1

        if line['data'] == 'DOWN':
            action['time'] = line['time']
        if line['data'] == 'UP':
            print(action)
            actions.append(action)
            action = {}

def transform(line):
    splitLine = str(line).split(' ')
    linedata = []
    for part in splitLine:
        if part == "b'[":
          continue
        if part == "\\n'":
          continue
        if part == '':
          continue
        linedata.append(part.replace(']',''))

    event = {
        "time": float(linedata[0]),
        "source": linedata[1],
        "type": linedata[2],
        "event": linedata[3],
        "data": linedata[4]
    }
    return event

# while 1:
#     if GPIO.input(KEY1_PIN) == 0:

runFlag = True  
thread = Thread(target=non_block_read)
thread.daemon = True # thread dies with the program
thread.start()

while True:
    time.sleep(1)

    # if GPIO.input(KEY3_PIN) == 0:
    #     proc.terminate()
    #     runFlag = False
    #     print('stop')

    # lcd.clear()

    # time.sleep(0.5)
