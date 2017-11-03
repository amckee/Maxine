#!/usr/bin/python3

from gpiozero import LED
import time, os

# LED(4) == GPIO(7) == Physical(7)
fan = LED(4)
fan.off()

#temp at which we turn the fan on
maxtemp = 55

#temp at which we turn the fan off
mintemp = 52

def getTemp():
    cmd = "vcgencmd measure_temp | grep -Eo '[0-9]{1,3}\.[0-9]'"
    r = os.popen( cmd ).readline()
    return float(r)

# to keep the code readable i've made these functions to handle this shit
def fanOff():
    ## which one is it!?!?!??
    #if not fan.is_active:
    if fan.is_active:
        print("Turning fan off.")
        fan.off()
def fanOn():
    if not fan.is_active:
        print("Turning fan on.")
        fan.on()

def controlFan(temp):
    print("Tempurature: %s \t Running: %s" % (temp, fan.is_active))
    #print("Fan Value: %s" % fan.value)
    #print("Is active: %s" % fan.is_active)
    if temp >= maxtemp:
        fanOn()
    elif temp <= mintemp:
        fanOff()

def main():
    #print("main()")
    log = open("/tmp/fan.log", 'w')
    log.write("Began")
    while True:
        controlFan(getTemp())
        time.sleep(1)
    log.write("Ended")
    log.close()


# start of program.
main()

print("Exiting due to end of script")
