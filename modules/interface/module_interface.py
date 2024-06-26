import io
import json
import os
import subprocess
from threading import Thread

from PIL import Image, ImageChops
import numpy

from fpdf.fpdf import FPDF

from gdep.LCD144 import KEY1_PIN, KEY2_PIN, KEY3_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_PRESS_PIN, KEY_RIGHT_PIN, KEY_UP_PIN, LCD_LCD144

import RPi.GPIO as GPIO
import time
from datetime import timedelta
from datetime import datetime
import math

class moduleInterface:

# global values for module
    lcd: LCD_LCD144
    runFlag = None
    buttonStates = {
        KEY1_PIN: 1,
        KEY2_PIN: 1,
        KEY3_PIN: 1,
        KEY_RIGHT_PIN: 1,
        KEY_DOWN_PIN: 1,
        KEY_UP_PIN: 1,
        KEY_PRESS_PIN: 1,
        KEY_LEFT_PIN: 1
    }

    def __init__(self, lcd) -> None:
        self.lcd = lcd
        self.init()

    lastbuttonpress = time.time();

    def buttonHandler(self):
        while self.runFlag == 1:
          for button in self.buttonStates:
            if GPIO.input(button) != self.buttonStates[button]:  
              self.buttonStates[button] = GPIO.input(button)
              if GPIO.input(button) == 0 and self.buttonPressHandlers.get(button):
                delay = time.time() - self.lastbuttonpress 
                self.lastbuttonpress = time.time();
                if delay > 0.25:
                    print(delay)
                    self.buttonPressHandlers.get(button)(self)
                else:
                    print('dribble')    

    def run(self):
        self.runFlag = 1
        process = Thread(target=self.buttonHandler)
        process.start();
        while self.runFlag == 1:
            self.mainFlow()
            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)
            time.sleep(0.05)

# end global values for module
# ##############################################################################################
# ##############################################################################################
# ##############################################################################################
# ##############################################################################################     

    recorderState = "idle" # idle / play / record / stop
    
    fileDir = "/home/pi/robot/adb_recs"
    reportsDir = "/home/pi/robot/reports"
    availableFiles = []
    page = 0 # starting from 0
    pageSize = 7
    selectedFile = 0 # select index on this page, first: 0 

    timecode = 0 # record or playback time

# variables related to command processing

    actions = [] # action list to replay
    timedActions = [] # actions with relative timings
    action = {} # single action handler
    event = 1  # which coordinates we are filling (x1 or x2)
    lasttimediff = 0

    playlog = []

#########################################################################

    def title(self):
        return "Interface"

    def init(self):
        self.recorderState = "idle";
        self.getFiles()

    def timecodeStart(self):
        startdate = time.time()
        while self.recorderState == "record":
            curdate = time.time() - startdate
            self.timecode = curdate
            time.sleep(0.1)
  
    def getPageCount(self):
        return int(math.ceil(len(self.availableFiles)/self.pageSize))

    def getFiles(self):
        try:
            self.availableFiles = os.listdir(self.fileDir)
        except Exception as e:
            print(e)
            self.availableFiles = []        

    # replay
    def replay(self, fileToPlay, doReport):
        if fileToPlay != '':
            with open(self.fileDir + "/"+fileToPlay, 'r') as f:
                self.timedActions = json.load(f)
        shotTimes = 0

        screenshots = []

        for action in self.timedActions:

            if self.recorderState != "play":
                return;

            # self.currentProgress += 1
            # self.updateScreen()
            time.sleep(action['sleep'])
            if action['command'] == 'SCREENSHOT':
                # need to save screenshot
                shotTimes += 1
                screenFileName = datetime.now().strftime("%H%M%S") + "-" + str(shotTimes) + ".png";
                
                if doReport:
                    p = subprocess.Popen(['adb', 'shell', 'screencap', '-p', '/sdcard/' + screenFileName])
                    # p.wait()
                    screenshots.append(screenFileName);
                    self.playlog.append('SHOT ' + screenFileName)
                    print('captured')
                else:
                    self.playlog.append('NOSHOT ' + screenFileName)
                    print('test mode')
            else:
                #log here
                self.playlog.append(action['command'][:10])
                
                p = subprocess.Popen(['adb', 'shell', 'input', action['command']])
                p.wait()

        if doReport:
            self.playlog.append('[R] GET_IMAGES..')
            for screenshot in screenshots:
                    p = subprocess.Popen(['adb', 'pull', '/sdcard/' + screenshot, self.reportsDir + "/" + screenshot])
                    p.wait()
                    p = subprocess.Popen(['adb', 'shell', 'rm -f', '/sdcard/' + screenshot])
                    p.wait()
            self.playlog.append('[R] DONE')

            #GENERATE PDF
            pdf = FPDF()
            pdf.set_font("Arial", "B", 14)

            pdf.add_page()
            pdf.text(20,30, 'REPORT AT ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            
            prevImage = None

            for image in screenshots:
                self.playlog.append('[R]PDF+' + image)

                im1 = Image.open(self.reportsDir + "/" + image)

                if prevImage != None:
                    difference = self.diff_images(prevImage, im1)
                    print('diff ' + image + ' : ' + str(difference))
                    if difference < 3:
                        self.playlog.append('[R]SKIP+' + image)
                        continue
                prevImage = im1

                pdf.add_page()
                rgbim = im1.convert('RGB')
                rgbim.save(self.reportsDir + "/" + image + ".jpg")
                pdf.image(self.reportsDir + "/" + image + ".jpg", 50,20, 100)
                pdf.text(20,10, image)
                
            pdfFileName = datetime.now().strftime("%H%M%S") + ".pdf"
            pdf.output(self.reportsDir + "/"+ pdfFileName, "F")

            for image in screenshots:
                os.remove(self.reportsDir + "/" + image + ".jpg")
                os.remove(self.reportsDir + "/" + image)

            self.playlog.append('[R]SAVED' + pdfFileName)

        self.recorderState = 'stop'


# read event from ADB
    def non_block_read(self):
        proc = subprocess.Popen(['adb', 'shell', 'getevent', '-lt'], stdout=subprocess.PIPE)
        while self.recorderState == "record":
            line = proc.stdout.readline()
            if line.find(b'EV_') != -1:
                command = self.transform(line)
                self.process(command)

# transform string command to object and extract information 
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
        self.lasttimediff = datetime.now().timestamp() - event.get('time')
        return event

# transform command to adb actions
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

# transform action to "ADB TAP X Y" command prepared to replay 
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

    def compare(im1,im2):
        ImageChops

#transform adb actions to script
    def finalize(self):
        if len(self.actions) > 0:
            lastActionStart = self.actions[0]['time']
            for action in self.actions:
                actionSleep = action['time'] - lastActionStart
                self.timedActions.append({
                    "sleep": actionSleep,
                    "command": action['text']
                })
                lastActionStart = action['time']

# check connected devices
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

    def diff_images(self, imgA, imgB):
        res = ImageChops.difference(imgA, imgB)
        total_pixels = imgA.height * imgA.width
        diff_pixels = numpy.count_nonzero(res)
        return diff_pixels * 100 / total_pixels


    #button handlers
    def button_key_left_pin_handler(self):
        self.runFlag = 0

    def button_key_down_pin_handler(self):
        if self.selectedFile >= self.pageSize - 1:
            if self.page < self.getPageCount()-1:    # try go to next page
                self.page += 1
                self.selectedFile = 0
            else:                                  # else stay where you are
                self.selectedFile = self.pageSize-1
        else: # move down
            if self.page == self.getPageCount()-1:
                lastPageCount = len(self.availableFiles) % self.pageSize
                if lastPageCount == 0:
                    lastPageCount = self.pageSize
                if self.selectedFile < lastPageCount - 1:
                    self.selectedFile += 1
                else:
                    self.selectedFile += 0
            else:
                self.selectedFile += 1

    def button_key_up_pin_handler(self):
        if self.selectedFile <=  0:
            if self.page > 0:                      # try go to prev page
                self.page -= 1
                self.selectedFile = self.pageSize - 1
            else:                                  # else stay where you are
                self.selectedFile = 0
        else: # move up
            self.selectedFile -= 1

    def button_key_1_pin_handler(self):
        if self.recorderState == "idle":
            self.recorderState = "record"
            self.actions = []
            self.timedActions = []
            self.event = 1

            process = Thread(target=self.timecodeStart)
            process2 = Thread(target=self.non_block_read)

            process.start()
            process2.start()
        elif self.recorderState == "stop":
            self.recorderState = "idle"

        elif self.recorderState == "play":
            self.recorderState = "idle"
        
        else:
            self.recorderState = "idle"
            self.finalize()
            if len(self.timedActions) > 0:
                with open(self.fileDir + '/' + datetime.now().strftime("%H%M%S") + ".json", 'w') as f:
                    json.dump(self.timedActions, f, indent=2)
                self.getFiles()

    def button_key_2_pin_handler(self):
        if self.recorderState == "record":
            abdAction = {"time": datetime.now().timestamp() - self.lasttimediff, "text":"SCREENSHOT"}
            self.actions.append(abdAction)
            print(abdAction)
        elif self.recorderState == "idle":
            self.playlog = []
            selectedFileName = self.availableFiles[self.page*self.pageSize + self.selectedFile]
            process = Thread(target=self.replay, args=[selectedFileName, False])
            self.recorderState = "play"
            process.start()

    def button_key_3_pin_handler(self):
        if self.recorderState == "idle":
            self.playlog = []
            selectedFileName = self.availableFiles[self.page*self.pageSize + self.selectedFile]
            process = Thread(target=self.replay, args=[selectedFileName, True])
            self.recorderState = "play"
            process.start()

    buttonPressHandlers = {
        KEY_LEFT_PIN: button_key_left_pin_handler,
        KEY_DOWN_PIN: button_key_down_pin_handler,
        KEY_UP_PIN: button_key_up_pin_handler,
        KEY1_PIN: button_key_1_pin_handler,
        KEY2_PIN: button_key_2_pin_handler,
        KEY3_PIN: button_key_3_pin_handler
    }

#render functions

    def playbackStopStateRender(self):
        #stop button
        self.lcd.draw.text((102,30), "BACK", fill=(255,0,0,128))

        #play button
        self.lcd.draw.text((92, 90), "REPEAT", fill=(0,255,0,128))
        
        #scrollpane
        self.lcd.draw.rectangle((0,16,85,110), fill=(0,0,0,128), outline=(255,255,255,0))
        if len(self.playlog) > 0:
            lastActions = self.playlog[-8:]
            actionIndex = 0
            for action in lastActions:
                self.lcd.draw.text((3,16+11*actionIndex), action[:13], fill=(255,255,255,0))
                actionIndex += 1

    def playbackStateRender(self):
        #stop button
        self.lcd.draw.rectangle((88,30,98,40), fill=(255,0,0,128))
        self.lcd.draw.text((102,30), "STOP", fill=(255,0,0,128))

        #shot button
        self.lcd.draw.text((92, 60), "PAUSE", fill=(0,255,0,128))
 
        #play button
        self.lcd.draw.text((102, 90), "PLAY", fill=(0,255,0,128))
        self.lcd.draw.regular_polygon((93,95,5), n_sides=3, rotation=30, fill=(0,255,0,128))

        #timecode
        self.lcd.draw.regular_polygon((63,10,3), n_sides=3, rotation=30, fill=(0,255,0,128))
        timecode = str(timedelta(seconds=self.timecode))[:-5]
        self.lcd.draw.text((70,5), timecode, fill=(255,255,255,128))

        #scrollpane
        self.lcd.draw.rectangle((0,16,85,110), fill=(0,0,0,128), outline=(255,255,255,0))
        if len(self.playlog) > 0:
            lastActions = self.playlog[-8:]
            actionIndex = 0
            for action in lastActions:
                self.lcd.draw.text((3,16+11*actionIndex), action[:13], fill=(255,255,255,0))
                actionIndex += 1

    def recordStateRender(self):
        #stop button
        self.lcd.draw.rectangle((88,30,98,40), fill=(255,0,0,128))
        self.lcd.draw.text((102,30), "STOP", fill=(255,0,0,128))

        #shot button
        self.lcd.draw.text((102, 60), "SHOT", fill=(0,255,0,128))

        #timecode
        self.lcd.draw.ellipse((60,7,66,13), fill=(255,0,0,128))
        timecode = str(timedelta(seconds=self.timecode))[:-5]
        self.lcd.draw.text((70,5), timecode, fill=(255,255,255,128))

        #scrollpane
        self.lcd.draw.rectangle((0,16,85,110), fill=(0,0,0,128), outline=(255,255,255,0))
        if len(self.actions) > 0:
            lastActions = self.actions[-8:]
            actionIndex = 0
            for action in lastActions:
                self.lcd.draw.text((3,16+11*actionIndex), action.get('text')[:13], fill=(255,255,255,0))
                actionIndex += 1

    def idleStateRender(self):
        #rec button
        self.lcd.draw.ellipse((95,30,105,40), fill=(255,0,0,128))
        self.lcd.draw.text((108,30), "REC", fill=(255,0,0,128))

        #play button
        self.lcd.draw.text((102, 60), "PLAY", fill=(0,255,0,128))
        self.lcd.draw.regular_polygon((93,65,5), n_sides=3, rotation=30, fill=(0,255,0,128))
    
        #scrollpane
        self.lcd.draw.rectangle((0,16,85,110), fill=(0,0,0,128), outline=(255,255,255,0))
        visibleFiles = self.availableFiles[self.page*self.pageSize:(self.page+1)*self.pageSize] 
        fileIndex = 0
        for file in visibleFiles:
            if fileIndex == self.selectedFile:
                self.lcd.draw.rectangle((1,16+11*fileIndex,85,27+11*fileIndex), fill=(255,255,255,0))
                self.lcd.draw.text((3,16+11*fileIndex), file[0:13], fill=(0,0,0,0))
            else:
                self.lcd.draw.text((3,16+11*fileIndex), file[0:13], fill=(255,255,255,0))
            fileIndex += 1

        #pageIndicator
        self.lcd.draw.rectangle((0,95,83,110), fill=(0,0,0,128), outline=(255,255,255,0))
        self.lcd.draw.text((3,98), "page " + str(self.page+1) + "/" + str(self.getPageCount()), fill=(255,255,255,128))

    def mainFlow(self):
        self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
        self.lcd.draw.text((5,5),"Recorder", fill=(255,255,255,128))

        self.check_devices()
        if len(self.devices) > 0:
            activeDevice = self.devices[0]
            if activeDevice['status'] == 'unauthorized':
                self.lcd.draw.text((5,117), activeDevice['name'] ,fill=(255,0,0,128))
            else:
                self.lcd.draw.text((5,117), activeDevice['name'] ,fill=(0,255,0,128))
        else:
            self.lcd.draw.text((5,117), 'NO DEVICE CONNECTED' ,fill=(255,0,0,128))

        if self.recorderState == "idle":
            self.idleStateRender()        
        elif self.recorderState == "record":
            self.recordStateRender()
        elif self.recorderState == "play":
            self.playbackStateRender()
        elif self.recorderState == "stop":
            self.playbackStopStateRender()

    def serve(self, path):
        print("serve", path)

    def netkey(self):
        return None;