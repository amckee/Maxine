#!/usr/bin/python3

from gpiozero import LED
import time, os, signal, sys

# LED(4) == GPIO(7) == Physical(7)
fan = LED(4)
fan.off()
## probably good for my needs
maxtemp = 70
mintemp = 60
## testing values
#maxtemp = 55
#mintemp = 53

def getTemp():
    r = os.popen("vcgencmd measure_temp | grep -Eo '[0-9]{1,3}\.[0-9]'").readline()
    return float(r)
def controlFan(temp):
    #print("Tempurature: %s" % temp)
    #print("Fan Active: %s" % fan.is_active)
    #print("Fan Value: %s" % fan.value)
    if temp > maxtemp:
        fan.on()
    elif temp < mintemp:
        fan.off()
    print()


def main():
    print("main()")
    while True:
        controlFan(getTemp())
        time.sleep(1)


# start of program.
main()

print("Exiting due to end of script")
