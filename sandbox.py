from gpiozero import Button
from signal import pause
import datetime
import time

def btnPassengerClosed():
    dt = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    #t = time.time().strftime('%Y.%m.%d %H:%M:%S')
    print("[%s] Passenger door closed" % dt)

def btnPassengerOpened():
    dt = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    print("[%s] Passenger door opened" % dt)

btnPassengerDoor = Button(13)

dt = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
print(dt)

btnPassengerDoor.when_pressed = btnPassengerClosed
btnPassengerDoor.when_released = btnPassengerOpened
print("awaiting door events...")

pause()
