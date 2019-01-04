import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(12, GPIO.OUT)

pwm=GPIO.PWM(12,50)

pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)
#SetAngle(0)
#time.sleep(1)
#SetAngle(90)
#time.sleep(1)
pwm.stop()

GPIO.cleanup()
