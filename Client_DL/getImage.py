from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()

def GetImage():
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    camera.capture(rawCapture, format = "bgr")
    img = rawCapture.array
    return img