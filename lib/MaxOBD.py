from obd import OBDStatus
import obd, logging, os.path, subprocess, time
from serial.serialutil import SerialException
from bluetooth import *
import bluetooth

logger = logging.getLogger("maxine.obd")
logger.setLevel(logging.INFO)

obd_name = "OBDII"
obd_addr = None

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')

    def __init__(self):
        self.obd_name = obd_name
        self.obd_addr = obd_addr
        #self.obd_addr = "00:1D:A5:00:01:EB" #uncomment for super debug override

    def show_status(self):
        logger.info("===================")
        logger.info("|  Current Status |")
        logger.info("-------------------")
        try:
            logger.info( "| OBD: %s" % self.con.status() )
        except:
            logger.info( "| OBD: failed" )
        try:
            logger.info( "| /dev/rfcomm0: %s" % os.path.exists("/dev/rfcomm0") )
        except:
            logger.info( "| /dev/rfcomm0: failed" )
        logger.info("=========================================")

    def find_obd_device(self):
        ## scan for devices with 'OBDII' as the name
        ## return bluetooth address if found, return None if not found
        logger.info("Scanning for all nearby bluetooth devices...")
        nearby_devices = bluetooth.discover_devices()
        logger.info("Found %s devices nearby" % len(nearby_devices))
        if len(nearby_devices) > 0:
            for device in nearby_devices:
                if self.obd_name == bluetooth.lookup_name(device):
                    logger.info("Found %s at %s" % (self.obd_name, device))
                    self.obd_addr = device
                    return device
        return None

    def drop_bluetooth(self):
        logger.info("Dropping all bluetooth everythings...")
        subprocess.call(['sudo', 'rfcomm', 'unbind', '0'])
        subprocess.call(['sudo', 'hcitool', 'dc', self.obd_addr])
        self.obd_addr = None
        
    def stop(self):
        #this is ugly. is there a better way?
        try:
            self.con.stop()
        except:
            pass
        try:
            self.con.unwatch_all()
        except:
            pass
        try:
            self.con.close()
        except:
            pass
        self.drop_bluetooth()
        logger.info("Completely stopped.")
    
    ## callbacks
    def new_coolant_temp(self, temp):
        if temp is None:
            logger.info("temp is none!")
        else:
            tval = 0
            try:
                tval = temp.value.to('degF').magnitude
                logger.info("Coolant temp: %s" % tval)
            except TypeError:
                logger.error("Caught TypeError. Is the engine on?")
            except Exception as e:
                logger.error("Caught other error in new_coolant_temp()")
                self.restart()
    def new_load(self, load):
        if load is None:
            logger.info("load is none!")
        else:
            lval = 0
            try:
                lval = load.value.magnitude
                logger.info("Engine load: %s" % lval)
            except TypeError:
                logger.error("Caught TypeError. Is the engine on?")
            except Exception as e:
                logger.error("Caught other error in new_load()")
                self.restart()
    def new_rpm(self, rpm):
        if rpm is None:
            logger.info("RPM is none!")
        else:
            rval = 0
            try:
                rval = rpm.value.magnitude
                logger.info("RPM: %s" % rval)
            except TypeError:
                logger.error("Caught TypeError. Is the engine on?")
            except Exception as e:
                logger.error("Caught other error in new_rpm()")
                self.restart()
    def new_tps(self, tps):
        if tps is None:
            logger.info("TPS is none!")
        else:
            tval = 0
            try:
                tval = tps.value.magnitude
                logger.info("TPS: %s" % tval)
            except TypeError:
                logger.error("Caught TypeError. Is the engine on?")
            except Exception as e:
                logger.error("Caught other error in new_tps()")
                self.restart()
    ## end callbacks

    def set_watchers(self):
        logger.info("Setting watchers...")
        self.con.watch(obd.commands.COOLANT_TEMP, force=True, callback=self.new_coolant_temp)
        #self.con.watch(obd.commands.ENGINE_LOAD, force=True, callback=self.new_load)
        #self.con.watch(obd.commands.RPM, force=True, callback=self.new_rpm)
        self.con.watch(obd.commands.THROTTLE_POS, force=True, callback=self.new_tps)
        #self.con.watch(obd.commands.SPEED, force=True)
        #self.con.watch(obd.commands.TIMING_ADVANCE, force=True)

    def connect_bluetooth(self):
        if self.obd_addr is None:
            if self.find_obd_device() is None:
                logger.error("Could not find OBD device.")
                return False

        logger.info("Connecting to %s at %s" % (self.obd_name, self.obd_addr))
        logger.info("Running hcitool and rfcomm activation...")
        subprocess.call(['sudo', 'hcitool', 'cc', self.obd_addr])
        subprocess.call(['sudo', 'rfcomm', 'bind', '0', self.obd_addr])
        return True
    def connect_obd(self):
        self.con = obd.Async()

        if self.con.is_connected():
            logger.info("OBD Connection established.")
            self.set_watchers()
            self.con.start()
            return True
        return False

    def restart(self):
        logger.info("Restarting...")
        self.stop()
        time.sleep(1) # driver is buggy. this helps.
        self.start()

    def start(self):
        if self.find_obd_device() is not None:
            self.connect_bluetooth()
            self.connect_obd()
        else:
            logger.info("Did not find OBD device.")
