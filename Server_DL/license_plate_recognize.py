import glob
import os
import shutil
import sys
import time
import cv2
import numpy as np
import tensorflow as tf
from lib.detect.text_2_line_detector import *
from lib.detect.plateDetector import *
from lib.lprNet.run_lprnet import *

sys.path.append('.')

def get_low_box(coods):
    temp = []
    for i in range(0, len(coods)):
        box = coods[i]
        y_max = max(int(box[1]), int(box[3]))
        temp.append(y_max)
    if temp:
        return temp.index(max(temp))
    return temp


def getPlate_OCR(img):
    
    detect_output_full = get_license_plate_full(img, detection_graph_full)
    for coordinate_full, label in detect_output_full.items():
        license_plate_image_full = img[int(coordinate_full[1]):int(coordinate_full[3]), int(coordinate_full[0]):int(coordinate_full[2])]

    detect_output_low = get_license_plate_low(img, detection_graph_low)

    if len(detect_output_low.values()) == 2:
        multi_box = []

        for coordinate_low, label in detect_output_low.items():
            start = time.time()
            multi_box.append(coordinate_low)
        low_box = get_low_box(multi_box)
        box_new = multi_box[low_box]
        license_plate_image_low = img[int(box_new[1]):int(box_new[3]), int(box_new[0]):int(box_new[2])]
        detected_list = extract_license_number(license_plate_image_low)

    return detected_list, full_license_plate_image, license_plate_image_low


