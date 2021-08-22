from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY3_PIN, KEY_LEFT_PIN
import RPi.GPIO as GPIO
import time
import subprocess
import threading

class moduleRecorder:
    
    lcd = None
    runFlag = None
    recFlag = None
    
    thread = None
    proc = None 
    actions = [] # action list to replay
    action = {} # single action handler
    event = 1  # which coordinates we are filling (x1 or x2)

    timedActions = []

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

    def replay(self):
        self.state['status'] = 'playback'
        self.updateScreen()
        for action in self.timedActions:
            time.sleep(action['sleep'])
            p = subprocess.Popen(['adb', 'shell', 'input', action['command']])
            p.wait()
        
        self.state['status'] = 'idle'
        self.updateScreen()

    def updateScreen(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

        self.lcd.draw.text((5,15), "Recorder: " + self.state['status'],fill=(255,255,255,128))
        if len(self.timedActions) > 0:
            i = 0
            for action in self.timedActions:
                i += 1
                self.lcd.draw.text((5,15+10*i), str(round(action['sleep'],3)) + " : " + action['command'],fill=(255,255,255,128))

        self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)

    def run(self):
        self.runFlag = 1
        while self.runFlag == 1:
            
            if GPIO.input(KEY_LEFT_PIN) == 0: # press left - close  
                self.runFlag = 0

            if GPIO.input(KEY1_PIN) == 0:
                self.recFlag = True  
                thread = threading.Thread(target=self.non_block_read)
                thread.daemon = True # thread dies with the program
                thread.start()

            if GPIO.input(KEY2_PIN) == 0:
                self.replay()

            self.updateScreen()
        
            time.sleep(0.1)