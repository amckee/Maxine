#!/usr/bin/python3

from gpiozero import LED
import time, os

# LED(4) == GPIO(7) == Physical(7)
fan = LED(4)
fan.off()

#temp at which we turn the fan on
maxtemp = 70

#temp at which we turn the fan off
mintemp = 55

def getTemp():
    cmd = "vcgencmd measure_temp | grep -Eo '[0-9]{1,3}\.[0-9]'"
    r = os.popen( cmd ).readline()
    return float(r)

# for some reason, fan.on turns the fan off, and fan.off turns the fan on
# to keep the code readable i've made these functions to handle this shit
def fanOn():
    if fan.is_active:
        print("Turning fan on.")
        fan.off()
def fanOff():
    if not fan.is_active:
        print("Turning fan off.")
        fan.on()

def controlFan(temp):
    print("Tempurature: %s" % temp)
    print("Fan Value: %s" % fan.value)
    print("Is active: %s" % fan.is_active)
    if temp >= maxtemp:
        fanOn()
    elif temp <= mintemp:
        fanOff()

def main():
    #print("main()")
    while True:
        controlFan(getTemp())
        time.sleep(1)


# start of program.
main()

print("Exiting due to end of script")
