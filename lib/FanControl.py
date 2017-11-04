#!/usr/bin/python3
from gpiozero import LED, CPUTemperature
import time, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.basicConfig( filename='/dev/shm/jeepobd.log' )

class FanControl(object):
    def __init__(self):
        logger.info("FanControl::init()")
        self.fan = LED( 4 )
        self.fan.off()
        self.fanon = False # can't trust fan.is_active to report correctly
        self.maxtemp = 65
        self.mintemp = 60

    def getTemp(self):
        temp = CPUTemperature()
        return float( temp.temperature )

    def controlFan(self, temp):
        #print("[Debug] :: Temp[%s] :: Fanon[%s] " % ( temp, self.fanon ))
        if temp > self.maxtemp:
            if not self.fanon:
                logger.info("Temp: %s :: Activating fan" % temp)
                self.fan.on()
                self.fanon = True
        elif temp <= self.mintemp:
            if self.fanon:
                logger.info("Temp: %s :: Deactivating fan" % temp)
                self.fan.off()
                self.fanon = False

    def start(self):
        logger.info("FanControl::start()")
        while True:
            self.controlFan( self.getTemp() )
            time.sleep( 1 )

if __name__ == "__main__":
    fc = FanControl()
    fc.start()
