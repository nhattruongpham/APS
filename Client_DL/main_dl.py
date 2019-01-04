#!/usr/bin/python3
#-*- coding: utf8 -*-

from getImage import *
from insert_db import *
from mul_update_db_4 import *
from select_db import *
from mul_update_db_6 import *
from mul_update_db_10 import *
from getPlate import *
from LCD import *
from MFRC522 import *
from myconnutils import *
from license_plate_recognize import *
import time
import datetime
import RPi.GPIO as GPIO
import cv2
import numpy as np
import os


GPIO.setup(12, GPIO.OUT)
pwm=GPIO.PWM(12,50)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MIFAREReader = MFRC522()
connection = getConnection()
cursor = connection.cursor()

_number = 'ID1'
_price = '5000'

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)

def TurnServo():
    pwm.start(0)
    SetAngle(0)
    time.sleep(2)
    SetAngle(90)
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()

def main():
                                                                
    _outp = 0

    while True:

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if (status == MIFAREReader.MI_OK):
            start = time.time()
            _timeOut = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _uid = str(uid[0])+"." + str(uid[1]) + "." + str(uid[2]) +"." + str(uid[3])
            lcd_string("ID:" + _uid, LCD_LINE_1)
        _balance = SelectDB("Balance", "ParkingSlot", "AutoPlate", "UID", _uid)
        imgOriginalScene = GetImage()
        _license_plate, _plate_image_full, _plate_image_low = getPlate_OCR(imgOriginalScene)
        cv2.imwrite(os.path.join(os.path.join(os.getcwd(), "result_full/" + _license_plate + "_" + str(_idx) + ".png")), _plate_image_full)
        cv2.imwrite(os.path.join(os.path.join(os.getcwd(), "result_low/" + _license_plate + "_" + str(_idx) + ".png")), _plate_image_low)
        Mul_UpdateDB_4("ParkingSlot", "AutoPlate", "PlateOUT", _license_plate, "UID", _uid)
        _plateIn = SelectDB("PlateIN", "ParkingSlot", "AutoPlate", "UID", _uid)        
        _uid_db = SelectDB("UID", "ParkingSlot", "AutoPlate", "UID", _uid)

        if((_plateIn == _license_plate) and (_uid_db == _uid)):
            _balance = int(_balance) - int(_price)
            Mul_UpdateDB_10("ParkingSlot", "AutoPlate", "TimeOUT", _timeOut, "Price", _price, "Money", _balance, "UID", _uid, "PlateIN", _plateIn)
            _outp = _outp + 1
            Mul_UpdateDB_4("ParkingSlot", "Slot", "OUTP", _outp, "Number", _number)

            lcd_string("Plate Correct!", LCD_LINE_2)
            lcd_string("Money: " + str(_balance), LCD_LINE_1)
            TurnServo()
        else:
            _outp= _outp
            Mul_UpdateDB_4("ParkingSlot", "Slot", "OUTP", _outp, "Number", _number)
            lcd_string("Plate Incorrect!", LCD_LINE_2)
        Mul_UpdateDB_4("ParkingSlot", "DataSample", "Money", _balance, "UID", _uid)
        print("Time: ", time.time() - start)

# end main

if __name__ == "__main__":
    main()
