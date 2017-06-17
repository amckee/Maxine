from gpiozero import Button
from signal import pause
import datetime
import time

def logit(msg=""):
    if msg == "":
        return

    dt = datetime.datetime.now()
    print("[%s] %s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), msg))

def btnpress():
    logit("Passenger door closed")

def btnrelease():
    logit("Passenger door opened")

btn = Button(13)

btn.when_pressed = btnpress
btn.when_released = btnrelease

logit("Door monitoring initialized")
pause()
logit("Door monitoring stopped")
