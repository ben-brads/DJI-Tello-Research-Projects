import djitellopy as tello
import cv2
import time
from time import sleep
from threading import Event, Thread

class RepeatedTimer:
    stopped = False
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self. args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()
    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)
    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)
    def stop(self):
        self.stopped = True
        self.event.set()
        self.thread.join()


me = tello.Tello()
me.connect()
w,h = 360, 240
thresh = 0.5# Threshold to detect object

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

sleep(.5)
print(me.get_battery())
me.streamon()
sleep(.5)
me.mon()
me.mdirection(2)
sleep(.5)
me.takeoff()
sleep(8)

def CircularMotion():
    me.go(0, 0, 100, 50, 4)
    sleep(8)
    me.jump(100, 0, 100, 30, 0, 4, 1)
    sleep(8)
    me.jump(100, 0, 100, 30, 0, 1, 2)
    sleep(8)
    me.jump(100, 0, 100, 30, 0, 2, 3)
    sleep(8)
    me.jump(100, 0, 100, 30, 0, 3, 4)

timer = RepeatedTimer(1, CircularMotion)


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))

    classIds, confs, bbox = net.detect(img, confThreshold=thresh)
    print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 255, 0), 2)

    if len(classIds) != 0:
        if classIds[0] == 44:
            print(classIds[0])
            break

    cv2.imshow("Output", img)
    cv2.waitKey(1)

timer.stop()
me.land()