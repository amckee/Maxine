#!/usr/bin/python3
from gpiozero import LED
import time, os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.basicConfig( filename='/dev/shm/jeepobd.log' )

class FanControl(object):
    def __init__(self):
        logger.info("FanControl::init()")
        self.fan = LED( 4 )
        self.fan.off()
        self.maxtemp = 52
        self.mintemp = 52

    def getTemp(self):
        temp = os.popen("vcgencmd measure_temp | grep -Eo '[0-9]{1,3}\.[0-9]'").readline()
        return float( temp )

    def controlFan(self, temp):
        print("Temperature: %s" % temp)
        if temp > maxtemp:
            logger.info("Activating fan")
            self.fan.on()
        elif temp <= mintemp:
            logger.info("Deactivating fan")
            self.fan.off()

    def start(self):
        logger.info("FanControl::start()")
        while True:
            controlFan( getTemp() )
            time.sleep( 1 )

if __name__ == "__main__":
    fc = FanControl()
    fc.start()


    
