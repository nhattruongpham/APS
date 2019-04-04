#!/usr/bin/python3
#-*- coding: utf8 -*-

from getImage import *
from insert_db import *
from mul_update_db_4 import *
from select_db import *
from mul_update_db_6 import *
from DetectChars import *
from DetectPlates import *
from PossiblePlate import *
from getPlate import *
from LCD import *
from MFRC522 import *
import time
import datetime
import RPi.GPIO as GPIO
import cv2
import numpy as np
import os


SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MIFAREReader = MFRC522()
connection = myconnutils.getConnection()
cursor = connection.cursor()

_number = 'ID1'

def main():

    blnKNNTrainingSuccessful = loadKNNDataAndTrainKNN()        

    if blnKNNTrainingSuccessful == False:                               
        print ("\nerror: KNN traning was not successful\n")               
                                                          
    _idx = 0
    while True:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if (status == MIFAREReader.MI_OK):
            start = time.time()
            _timeIn = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _uid = str(uid[0])+"." + str(uid[1]) + "." + str(uid[2]) +"." + str(uid[3])
            lcd_string("ID:" + _uid, LCD_LINE_1)
            _idx = _idx + 1
        InsertDB("ParkingSlot", "AutoPlate", "UID", _uid, "TimeIN", _timeIn)
        Mul_UpdateDB_4("ParkingSlot", "Slot", "INP", _idx, "Number", _number)
        _money = SelectDB("Money", "ParkingSlot", "DataSample", "UID", _uid)
        lcd_string("Balance: " + str(_money), LCD_LINE_1)
        #imgOriginalScene = cv2.imread("2.jpg")
        imgOriginalScene = GetImage()           
        _license_plate = GetPlate(imgOriginalScene)
        cv2.imwrite(os.path.join(os.path.join(os.getcwd(), "result/" + _license_plate + "_" + str(_idx) + ".png")), imgOriginalScene)
        lcd_string("Plate: " + _license_plate, LCD_LINE_2)
        Mul_UpdateDB_6("ParkingSlot", "AutoPlate", "PlateIN", _license_plate, "Balance", _money, "UID", _uid)
        _outp = SelectDB("OUTP", "ParkingSlot", "Slot", "Number", _number)
        _inp = SelectDB("INP", "ParkingSlot", "Slot", "Number", _number)
        available = 10 - int(inp1) + int(outp)
        lcd_string("Available:  " + str(available), LCD_LINE_2)
        if (available < 5):
            lcd_string("ParkingSlot Full", LCD_LINE_2)
        stop = time.time()
        print("Time: ", stop - start)


if __name__ == "__main__":
    main()
