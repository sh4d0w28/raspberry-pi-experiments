from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_UP_PIN
import RPi.GPIO as GPIO
import time
import subprocess
import threading
import os
import json

class moduleRecorder:
    
    lcd = None
    runFlag = None
    recFlag = None
    
    thread = None
    proc = None 
    actions = [] # action list to replay
    action = {} # single action handler
    event = 1  # which coordinates we are filling (x1 or x2)

    fileSelectedInd = 0
    files = []

    timedActions = []
    currentProgress = 0

    devices = []

    state = {
        "status": "idle" # idle # replay
    }

    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "Recorder"

    def non_block_read(self):
        proc = subprocess.Popen(['adb', 'shell', 'getevent', '-lt'], stdout=subprocess.PIPE)
        self.state['status'] = 'recording' # just to display
        while self.recFlag:
            if GPIO.input(KEY3_PIN) == 0:
                self.recFlag = False
                self.state['status'] = 'idle'
                self.finalize()
                self.state['actions'] = self.timedActions

                if self.fileToSave != '':
                    with open('/home/pi/robot/adb_recs/' + self.fileToSave, 'w') as f:
                        json.dump(self.timedActions, f, indent=2) 

            line = proc.stdout.readline()
            if line.find(b'EV_') != -1:
                command = self.transform(line)
                self.process(command)

    def finalize(self):
        lastActionStart = self.actions[0]['time']
        for action in self.actions:
            actionSleep = action['time'] - lastActionStart
            self.timedActions.append({
                "sleep": actionSleep,
                "command": action['text']
            })
            lastActionStart = action['time']

    def check_devices(self):       
        proc = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE)
        proc.wait()
        lines = proc.stdout.readlines()
        self.devices = [];
        if len(lines)>2:
            # have devices
            for line in lines:
                if line.startswith(b'List of devices'):
                    continue
                if line == b'\n':
                    continue
                data = line.split(b'\t')
                if(len(data)>1):
                    self.devices.append({
                        'name': str(data[0]).split("'")[1],
                        'status': str(data[1]).replace('\\n','').split("'")[1]
                    })

    def process(self, line):

        # press screen or release, lock time
        if line['event'] == 'ABS_MT_POSITION_X':
            data = int(line['data'],16)
            if self.event == 1:
                self.action['x1'] = data
            elif self.event == 2:
                self.action['x2'] = data
        elif line['event'] == 'ABS_MT_POSITION_Y':
            data = int(line['data'],16)
            if self.event == 1:
                self.action['y1'] = data
            elif self.event == 2:
                self.action['y2'] = data
        elif line['event'] == 'BTN_TOUCH':
            if self.event == 1:
                self.event = 2
            else: 
                self.event = 1

            if line['data'] == 'DOWN':
                self.action['time'] = line['time']
            if line['data'] == 'UP':
                abdAction = self.getAdbAction(self.action)
                self.actions.append(abdAction)
                print(abdAction)
                self.action = {}

    def getAdbAction(self, action):
        adbAction = {
            "time": action['time']
        }
        if 'x2' in action and 'y2' in action: 
            if abs(action['x2'] - action['x1']) < 10 and abs(action['y1'] - action['y2']) < 10:
                adbAction['text'] = ' '.join(['tap',
                str(action['x1']),str(action['y1'])
                ])
            else:  
                adbAction['text'] = ' '.join(['swipe', 
                    str(action['x1']),str(action['y1']),
                    str(action['x2']),str(action['y2'])
                ])
        else:
            adbAction['text'] = ' '.join([
                'tap',str(action['x1']),str(action['y1'])
            ])

        return adbAction


    def transform(self, line):
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

    def replay(self, fileToPlay):
        if fileToPlay != '':
            with open("/home/pi/robot/adb_recs/"+fileToPlay, 'r') as f:
                self.timedActions = json.load(f)

        self.state['status'] = 'playback'
        for action in self.timedActions:
            
            self.currentProgress += 1
            self.updateScreen()

            time.sleep(action['sleep'])
            p = subprocess.Popen(['adb', 'shell', 'input', action['command']])
            p.wait()
        
        self.state['status'] = 'idle'
        self.updateScreen()

    def updateScreen(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.lcd.draw.text((5,15), "Recorder: " + self.state['status'],fill=(255,255,255,128))
        
        # draw file selector if idle
        if self.state['status'] == 'idle':
            self.getFiles();
            if len(self.files) > 0:
                fileind = 0
                for file in self.files:
                    if self.fileSelectedInd == fileind:
                        self.lcd.draw.text((5,25+10*fileind), ">" + file + "<" ,fill=(255,255,255,128))
                    else: 
                        self.lcd.draw.text((5,25+10*fileind), " " + file ,fill=(255,0,0,128))
                    fileind += 1

            if len(self.devices) > 0:
                activeDevice = self.devices[0]
                if activeDevice['status'] == 'unauthorized':
                    self.lcd.draw.text((5,118), activeDevice['name'] ,fill=(255,0,0,128))
                else:
                    self.lcd.draw.text((5,118), activeDevice['name'] ,fill=(0,255,0,128))
            else:
                self.lcd.draw.text((5,118), 'NO DEVICE CONNECTED' ,fill=(255,0,0,128))
        
        if self.state['status'] == 'playback':
            self.lcd.draw.text((5,25), "Now playing: " + self.files[self.fileSelectedInd] ,fill=(255,255,255,128))
            self.lcd.draw.text((5,35), "Progress: " + str(self.currentProgress) + "/" + str(len(self.timedActions)) ,fill=(255,255,255,128))

        self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

    def getFiles(self):
        try:
            self.files = os.listdir('/home/pi/robot/adb_recs')
        except Exception as e:
            print(e)
            self.files = []
        

    def run(self):
                
        self.runFlag = 1
        while self.runFlag == 1:
            
            self.check_devices()

            if GPIO.input(KEY_LEFT_PIN) == 0: # press left - close  
                self.runFlag = 0

            if GPIO.input(KEY1_PIN) == 0: # start record
                self.recFlag = True  
                thread = threading.Thread(target=self.non_block_read)
                thread.daemon = True # thread dies with the program
                thread.start()

            if self.state['status'] == 'idle':
                if GPIO.input(KEY_DOWN_PIN) == 0: # file select
                    self.fileSelectedInd += 1
                if GPIO.input(KEY_UP_PIN) == 0: #file select
                    self.fileSelectedInd -= 1
                if GPIO.input(KEY2_PIN) == 0: # play file
                    if self.files[self.fileSelectedInd] != '':
                        self.currentProgress = 0
                        self.replay(self.files[self.fileSelectedInd])
                
            self.updateScreen()
        
            time.sleep(0.1)