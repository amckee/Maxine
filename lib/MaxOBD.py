from obd import OBDStatus
import obd, logging, os.path, subprocess, time
from serial.serialutil import SerialException
from bluetooth import *
import bluetooth

logger = logging.getLogger("maxine.obd")
logger.setLevel(logging.INFO)

naptime = 1 #seconds to sleep between reconnection attempts

obd_name = "OBDII"
obd_addr = None

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')

    def __init__(self):
        self.obd_name = obd_name
        self.obd_addr = obd_addr
        self.naptime  = naptime
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

    def reset_bluetooth(self):
        ## can anyone find a way to do this in python natively!?
        ## pybluez sucks (if only with documentation)
        self.drop_bluetooth()
        time.sleep(1) # give it a moment. the driver is crashy
        self.connect_bluetooth()

    def drop_bluetooth(self):
        logger.info("Dropping all bluetooth everythings...")
        subprocess.call(['sudo', 'rfcomm', 'unbind', '0'])
        subprocess.call(['sudo', 'hcitool', 'dc', self.obd_addr])
        self.obd_addr = None
        
    def bind_bluetooth(self):
        if self.obd_addr is not None:   # we've found the device before
            self.connect_bluetooth()    # so reconnect with it
        else:
            return False
        return True
    
        # find device and open connection
        if self.obd_addr is None:
            logger.info("Do not have %s address" % self.obd_name)
            btaddr = self.find_obd_device()
            if btaddr is None:
                logger.info("Could not find %s device" % self.obd_name)
                return False
            else:
                logger.info("Found %s device at %s" % (self.obd_name, btaddr))
                self.obd_addr = btaddr
        else:
            logger.info("%s device known to be at %s" % (self.obd_name,self.obd_addr))

        try:
            logger.info("Connecting to %s at %s" % (self.obd_name, self.obd_addr))
            self.reset_bluetooth()
        except Exception as e:
            logger.info("Failed to connect to %s device at %s" % (self.obd_name,self.obd_addr))
            logger.info("Error details: %s" % e)
            return False
        return True

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

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
    
    def ensure_obd_device(self):
        # ensure OBD device exists and is connected
        ## return True for success, False for failure
        self.show_status()


        #### working prototype (no auto-find device)
        ####logger.info("running hcitool...")
        ####subprocess.call(['sudo', 'hcitool', 'cc', self.obd_addr])
        ####logger.info("running rfcomm...")
        ####subprocess.call(['sudo', 'rfcomm', 'bind', '0', self.obd_addr])
        ####logger.info("creating async obd object...")
        ####self.con = obd.Async()
        ####logger.info("creating a watcher...")
        ####self.con.watch(obd.commands.COOLANT_TEMP, force=True, callback=self.new_coolant_temp)
        ####logger.info("starting connection...")
        ####self.con.start()
        ####

        ## bluetooth loop
        # if we don't know the obd bluetooth address then this is first run
        while self.obd_addr is None:
            if not self.find_obd_device():
                logger.error("No OBD bluetooth device found. Sleeping...")
                time.sleep( self.naptime )
        while not self.bind_bluetooth():
            logger.error("Failed to bind to OBD bluetooth device at %s." % self.obd_addr)
            time.sleep( self.naptime )
            
        ## obd loop
        connected = False
        while not connected:
            try:
                if self.con.is_connected():
                    logger.info("OBD has a connection")
                else:
                    logger.info("OBD is not connected")
                    self.con = obd.Async()
            except AttributeError as e:
                ## known to happen before initial connection occurs
                logger.error("self.con.is_connected() threw AttributeError:")
                logger.error(e)
                return False
            except Exception as e:
                logger.error("self.con.is_connected() threw Exception:")
                logger.error(e)
                return False #so we can try again on the next loop
        return True

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
                logger.error(e)
                time.sleep(1)
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
                logger.error(e)
                time.sleep(1)
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
                logger.error(e)
                time.sleep(1)
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
                logger.error(e)
                time.sleep(1)
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
        if self.find_obd_device() is None:
            logger.info("nothing found")
            return False
        self.connect_bluetooth()
        self.connect_obd()        
