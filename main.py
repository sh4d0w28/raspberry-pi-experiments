# import time
# import math

# import LCD144
# import PCA9685
# import RPi.GPIO as GPIO

# servos = { 1: 'S1', 2: 'S2', 3: 'S3', 4: 'S4', 5: 'S5', 6: 'S6' }

# servos_values = { 1: 1000, 2: 1100, 3: 1200, 4: 1300, 5: 1400, 6: 1500 }

# servos_max_value = { 1: 1700, 2: 2600, 3: 3200, 4: 2500, 5: 2300, 6: 2700 }

# servos_min_value = {1: 1000, 2: 300, 3: 800, 4: 600, 5: 800, 6: 800 }

# enabled = 1

# def move_right():
#     global enabled
#     if enabled > 1:
#         enabled -= 1
#     else:
#         enabled = 6
    
# def move_left():
#     global enabled

#     if enabled < 6:
#         enabled += 1
#     else:
#         enabled = 1


# def move_up():
#     global enabled
#     servos_values[enabled] += 100


# def move_down():
#     global enabled
#     servos_values[enabled] -= 100

# def set_servos():
#     pwm.setServoPulse(1,servos_values[1])
#     pwm.setServoPulse(2,servos_values[2])
#     pwm.setServoPulse(3,servos_values[3])
#     pwm.setServoPulse(4,servos_values[4])
#     pwm.setServoPulse(5,servos_values[5])
#     pwm.setServoPulse(6,servos_values[6])

# if __name__=='__main__':

#     pwm = PCA9685.PCA_PCA9685(0x40, debug=False)
#     pwm.setPWMFreq(50)

#     lcd = LCD144.LCD_LCD144()

#     prev_button = -1

#     while 1:

#         lcd.draw.rectangle((0,0,128,128), outline=0, fill=0)

#         # with canvas(device) as draw:
#         if GPIO.input(LCD144.KEY_UP_PIN) == 0: # button is released       
#             lcd.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)  #Up        
#             # print("Up")
#             move_up()        

#         else: # button is pressed:
#             lcd.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up filled
            
#         if GPIO.input(LCD144.KEY_LEFT_PIN) == 0: # button is released
#             lcd.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)  #left
#             # print("left")    
            
#         else: # button is pressed:       
#             lcd.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left filled
            
#         if GPIO.input(LCD144.KEY_RIGHT_PIN) == 0: # button is released
#             lcd.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0xff00) #right
#             # print("right")

#         else: # button is pressed:
#             lcd.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right filled       
            
#         if GPIO.input(LCD144.KEY_DOWN_PIN) == 0: # button is released
#             lcd.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00) #down
#             # print("down")
#             move_down()
#         else: # button is pressed:
#             lcd.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down filled
            
#         if GPIO.input(LCD144.KEY_PRESS_PIN) == 0: # button is released
#             lcd.draw.rectangle((20, 22,40,40), outline=255, fill=0xff00) #center 
#             # print("center")
#         else: # button is pressed:
#             lcd.draw.rectangle((20, 22,40,40), outline=255, fill=0) #center filled
            
#         if GPIO.input(LCD144.KEY1_PIN) == 0: # button is released
#             lcd.draw.ellipse((70,0,90,20), outline=255, fill=0xff00) #A button
#             # print("KEY1")
#             move_right()             
            
#         else: # button is pressed:
#             lcd.draw.ellipse((70,0,90,20), outline=255, fill=0) #A button filled
            
#         if GPIO.input(LCD144.KEY2_PIN) == 0: # button is released
#             lcd.draw.ellipse((100,20,120,40), outline=255, fill=0xff00) #B button]
#             # print("KEY2")
#         else: # button is pressed:
#             lcd.draw.ellipse((100,20,120,40), outline=255, fill=0) #B button filled
            
#         if GPIO.input(LCD144.KEY3_PIN) == 0: # button is released
#             lcd.draw.ellipse((70,40,90,60), outline=255, fill=0xff00) #A button
#             # print("KEY3")
#             move_left()            
#         else: # button is pressed:
#             lcd.draw.ellipse((70,40,90,60), outline=255, fill=0) #A button filled
        
#         for i in range(1,7):
#             whitefill = (255,255,255,128)
#             if(i == enabled):
#                 lcd.draw.text((10,50+10 * i), str(servos_values[i]), fill=(255,255,255,128))
#             else:
#                 lcd.draw.text((10,50+10 * i), str(servos_values[i]), fill=(255,0,0,128))
        
#         lcd.disp.LCD_ShowImage(lcd.image,0,0)

#         set_servos()