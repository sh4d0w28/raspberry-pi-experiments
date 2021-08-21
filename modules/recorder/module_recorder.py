import RPi.GPIO as GPIO
import time
import subprocess

class moduleRecorder:
    
    lcd = None
    runFlag = None

    def __init__(self, lcd) -> None:
        self.lcd = lcd

    def title(self):
        return "Recorder"

    def record(self):
        return subprocess.Popen(['adb shell getevent -lt | grep EV_ > /home/pi/robot/work/log.txt'], shell=True)

    def play(self):
        file1 = open('log.txt', 'r')
        count = 0

        actions = []

        curr = {}
        
        while True:
            count += 1
        
            # Get next line from file
            line = file1.readline()
        
            # if line is empty
            # end of file is reached
            if not line:
                break

            els = line.split(' ')
            nonnull = []
            for el in els:
                if el != '':
                    nonnull.append(el.replace(']','').strip())

            if len(nonnull) != 7:
                #donothing
                i = 200000
            elif nonnull[4] == 'SYN_REPORT':
                actions.append(curr)
                curr = {'btn':''}
            elif nonnull[4] == 'ABS_MT_POSITION_X':
                curr['x'] = int(nonnull[5],16)
            elif nonnull[4] == 'ABS_MT_POSITION_Y':
                curr['y'] = int(nonnull[5],16)
            elif nonnull[4] == 'BTN_TOUCH':
                curr['btn'] = nonnull[5]
                curr['time'] = nonnull[1]

        file1.close()

        # print('ACTIONS', actions)

        commands = []
        command = {}

        for action in actions:
            if action['btn'] == 'DOWN' :  # start swipe / click
                command['x1'] = action['x']
                command['y1'] = action['y']
                command['time1'] = float(action['time'])

            elif action['btn'] == 'UP' : # end swipe / click
                command['time2'] = float(action['time'])

                if 'x2' in command:
                  commands.append({
                    'text':'swipe' + ' ' + str(command['x1']) + ' ' + str(command['y1']) + ' ' + str(command['x2']) + ' ' + str(command['y2']),
                    'time1': command['time1'],
                    'time2': command['time2']
                })
                else:
                  commands.append({
                    'text': 'tap' + ' ' + str(command['x1']) + ' ' + str(command['y1']),
                    'time1': command['time1'],
                    'time2': command['time2']
                })
                command = {}
            else:
                if 'x' in action:
                  command['x2'] = action['x']
                if 'y' in action:
                  command['y2'] = action['y']

        # print('COMMANDS', commands)

        timed_commands = []

        prev_time = 0

        for command in commands:
          if prev_time == 0:
            prev_time = command['time1']

          timed_commands.append({
            'sleep': command['time1'] - prev_time,
            'text': command['text']
          })

          prev_time = command['time2']

        print('TIMED COMMANDS', timed_commands)

        cmd = 0


        for command in timed_commands:
            cmd = cmd + 1
            print('adb shell input ' + command['text'])
            time.sleep(command['sleep'])
            subprocess.Popen(['adb', 'shell', 'input', command['text']])
            
            png = subprocess.check_output(['adb', 'shell', 'screencap', '-p'])
            f = open('screen' + str(cmd) + '.png', 'wb')
            f.write(png)
            f.close()

    mode = ''
    process = None

    def run(self):
        self.runFlag = 1
        while self.runFlag == 1:
            
            if GPIO.input(5) == 0: # press left - close  
                self.runFlag = 0

            if GPIO.input(21) == 0:
                print(139)
                if self.mode != 'record':
                    self.mode = 'record'
                    self.process = self.record()
                else:
                    print(146)
                    print(148)
                    self.process.terminate()
                    retcode = self.process.wait()

            if GPIO.input(20) == 0:
                print('play?')
                if self.mode != 'play':
                    self.mode = 'play'
                    self.process = self.play()
                    self.mode = ''

            self.lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)
            self.lcd.draw.text((5,5), "RECORDER",fill=(255,255,255,128))
            self.lcd.draw.text((5,15), "MODE: " + self.mode,fill=(255,255,255,128))
            self.lcd.disp.LCD_ShowImage(self.lcd.image,0,0)
            time.sleep(0.1)