import smbus
import math
import time

class PCA_PCA9685:

    # Registers/etc.
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        if (self.debug):
            print("Reseting PCA9685")
        self.write(self.__MODE1, 0x00)

    def write(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        self.bus.write_byte_data(self.address, reg, value)
        if (self.debug):
            print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        result = self.bus.read_byte_data(self.address, reg)
        if (self.debug):
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)

        oldmode = self.read(self.__MODE1);
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H+4*channel, on >> 8)
        self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H+4*channel, off >> 8)
        if (self.debug):
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))

    def setServoPulse(self, channel, pulse):
        "Sets the Servo Pulse,The PWM frequency must be 50HZ"
        pulse = pulse*4096/20000        #PWM frequency is 50HZ,the period is 20000us
        self.setPWM(channel, 0, int(pulse))
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
#####################################

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