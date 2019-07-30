#!/usr/bin/python3

from gpiozero import LED
import time, os

# LED(4) == GPIO(7) == Physical(7)
fan = LED(4)
fan.off()

#temp at which we turn the fan on
maxtemp = 56

#temp at which we turn the fan off
mintemp = 50

def getTemp():
    cmd = "vcgencmd measure_temp | grep -Eo '[0-9]{1,3}\.[0-9]'"
    r = os.popen( cmd ).readline()
    return float(r)

# for some reason, fan.on turns the fan off, and fan.off turns the fan on
# to keep the code readable i've made these functions to handle this shit
def fanOn():
    if not fan.is_active:
        print("Turning fan on.")
        fan.on()
def fanOff():
    if fan.is_active:
        print("Turning fan off.")
        fan.off()

def controlFan(temp):
    print("Temperature: %s - %s/%s" % (temp, mintemp, maxtemp))
    print("fan.value: %s" % fan.value)
    print("fan.is_active: %s" % fan.is_active)

    if int(temp) >= int(maxtemp):
        fanOn()
    elif int(temp) <= int(mintemp):
        fanOff()
    else:
        print("Skipping this poll.")

def main():
    while True:
        controlFan(getTemp())
        time.sleep(1)

# start of program.
main()

print("Exiting due to end of script")
