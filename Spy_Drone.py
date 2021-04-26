import KeyPressModule as kp
from djitellopy import tello
import time
import cv2

kp.init()
me = tello.Tello()
me.connect()
me.streamon()
global img
print(me.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey('LEFT'): lr = -speed
    elif kp.getKey('RIGHT'): lr = speed

    if kp.getKey('UP'): fb = speed
    elif kp.getKey('DOWN'): fb = -speed

    if kp.getKey('w'): ud = speed
    elif kp.getKey('s'): ud = -speed

    if kp.getKey('a'): yv = -speed
    elif kp.getKey('d'): yv = speed

    if kp.getKey('q'): me.land(); time.sleep(3)
    if kp.getKey('e'): me.takeoff()

    if kp.getKey('z'):
        if not cv2.imwrite(fr'C:\Users\benbr\PycharmProjects\openCVPython\Resources\Images\{time.time()}.jpg', img):
            raise Exception("Could not write image")
        time.sleep(0.3)

    return [lr, fb, ud, yv]



while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    img = me.get_frame_read().frame
    cv2.waitKey(1)
