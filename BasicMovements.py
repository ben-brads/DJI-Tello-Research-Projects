from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print(me.get_battery())
t_end = time.time() + 10

me.takeoff()

while time.time() < t_end:
    me.move_forward(me, 15)

print(me.get_distance_tof())

me.land()