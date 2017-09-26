from obd import OBDStatus
import obd, logging, os.path, subprocess, time
from serial.serialutil import SerialException
from bluetooth import *
import bluetooth

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.basicConfig( filename='/dev/shm/jeepobd.log' )

async = False # run with async setup / set to false for comparing to non async method
stop = False # set this to true at any time to stop the main loop

obd_name = "OBDII"
obd_addr = None
#obd_addr = "00:1D:A5:00:01:EB"

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')

    def __init__(self):
        logger.info("MaxOBD::init()")
        self.obd_name = obd_name
        self.obd_addr = obd_addr

    def find_obd_device(self):
        logger.info("MaxOBD::find_obd_device()")
        ## scan for devices with 'OBDII' as the name
        ## return bluetooth address if found, return None if not found
        addr = None
        logger.info("Scanning for all nearby bluetooth devices...")
        nearby_devices = bluetooth.discover_devices()
        logger.info("Found %s devices nearby" % len(nearby_devices))
        if len(nearby_devices) == 0:
            logger.info("No devices found of any kind")
        else:
            for device in nearby_devices:
                if self.obd_name == bluetooth.lookup_name(device):
                    addr = device
                    break
        ## TODO: check for /dev/rfcomm0 and run these commands if not found:
        ## sudo hcitool cc <btaddr>
        ## sudo rfcomm bind 0 <btaddr>
        return addr

    def bind_bluetooth(self):
        logger.info("MaxOBD::bind_bluetooth()")
        try:
            # ensure clean slate before we begin
            self.btsock.close()
        except:
            pass
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
            self.btsock = BluetoothSocket( RFCOMM )
            # 0 = 'Invalid argument'
            # 1 = <no message>
            # 2 = 'Connection reset by peer'
            # 3 = 'Connection reset by peer'
            # 4 = 'Connection reset by peer'
            # 5 = 'Connection reset by peer'
            self.btsock.connect((self.obd_addr, 1))
            self.con = obd.Async()
        except Exception as e:
            logger.info("Failed to connect to %s device at %s" % (self.obd_name,self.obd_addr))
            logger.info("Error details: %s" % e)
            return False
        logger.info("Should be connected to %s at %s" % (self.obd_name,self.obd_addr))
        return True
        

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

    def stop(self):
        logger.info("MaxOBD::stop()")

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
        try:
            self.btsock.close()
        except:
            pass

        logger.info("MaxOBD stopped")
        
    def ensure_obd_device(self):
        logger.info("MaxOBD::ensure_obd_device()")
        # ensure OBD device exists and is connected
        ## return true for success, false for failure

        # if this fails, we need to do a reconnect
        try:
            if self.con.is_connected():
                logger.info("OBD has a connection")
                return True
            else:
                logger.info("OBD is not connected")
                self.con = obd.Async()
        except AttributeError as e:
            ## known to happen when vehicle is shutoff
            logger.error("self.con.is_connected() threw AttributeError:")
            logger.error(e)
            return False
        except Exception as e:
            logger.error("self.con.is_connected() threw Exception:")
            logger.error(e)
            ## commenting out to see what happens
##            if self.bind_bluetooth():
##                logger.info("Opening OBD connection...")
##                self.con = obd.Async()
            return False #so we can try again on the next loop
                
        constat = None
        try:
            constat = self.con.status()
        except Exception as e:
            logger.info("Failed to pull connection status:")
            logger.info(e)
            logger.info("Attempting re-bind...")
            if self.bind_bluetooth():
                logger.info("Opening OBD connection...")
                time.sleep(2)
                self.con = obd.Async()
            return False #so we can try again on the next loop

        try:
            # handle the various connection states
            ## running this in try block due to self.con
            ## not always existing, so failback to reconnecting
            if constat == obd.OBDStatus.CAR_CONNECTED:
                logger.info("Existing connection detected")
                return True
            elif self.con.status() == obd.OBDStatus.ELM_CONNECTED:
                logger.info("Connected to ELM but not car")
                return False
            elif self.con.status() == obd.OBDStatus.NOT_CONNECTED:
                #logger.info("No Connection found. Attempting to create one...")
                logger.info("No Connection found")
                return False
##                if os.path.exists( '/dev/rfcomm0' ):
##                    logger.info("Found /dev/rfcomm0 so attempting to bind...")
##                    self.con = obd.Async()
##                    self.ensure_obd_device()
##                else:
##                    logger.info("Did not find /dev/rfcomm0 so attempting bluetooth rebind...")
##                    self.bind_bluetooth()
##                    self.con = obd.Async()
##                    self.ensure_obd_device()
        except Exception as e:
            logger.info("Caught exception: %s" % e)
            return False
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
            except Exception as e:
                logger.error("Caught NoneType in new_coolant_temp():")
                logger.error(e)
                ## NoneType indicates the engine is now off.
                #self.reset_connection() #i don't think this belongs here

    def new_load(self, load):
        if load is None:
            logger.info("load is none!")
        else:
            lval = 0
            try:
                lval = load.value.magnitude
                logger.info("Engine load: %s" % lval)
            except Exception as e:
                logger.error("Caught NoneType in new_load():")
                logger.error(e)
                ## NoneType indicates the engine is now off.
                #self.reset_connection() #i don't think this belongs here            
    def new_rpm(self, rpm):
        if rpm is None:
            logger.info("RPM is none!")
        else:
            rval = 0
            try:
                rval = rpm.value.magnitude
                logger.info("RPM: %s" % rval)
            except Exception as e:
                logger.error("Error in new_rpm():")
                logger.error(e)
                ## NoneType indicates the engine is now off.
                #self.reset_connection() #i don't think this belongs here
    def new_tps(self, tps):
        if tps is None:
            logger.info("TPS is none!")
        else:
            tval = 0
            try:
                tval = tps.value.magnitude
                logger.info("TPS: %s" % tval)
            except Exception as e:
                logger.error("Caught NoneType in new_tps():")
                logger.error(e)
                ## NoneType indicates the engine is now off.
                #self.reset_connection() #i don't think this belongs here
    ## end callbacks

    def set_watchers(self):
        logger.info("MaxOBD::set_watchers()")
        self.con.watch(obd.commands.COOLANT_TEMP, force=True, callback=self.new_coolant_temp)
        self.con.watch(obd.commands.ENGINE_LOAD, force=True, callback=self.new_load)
        self.con.watch(obd.commands.RPM, force=True, callback=self.new_rpm)
        self.con.watch(obd.commands.THROTTLE_POS, force=True, callback=self.new_tps)
        #self.con.watch(obd.commands.SPEED, force=True)
        #self.con.watch(obd.commands.TIMING_ADVANCE, force=True)

    def reset_connection(self):
        logger.info("MaxOBD::reset_connection()")
        self.stop()
        naptime = 10
        while not self.ensure_obd_device():
                logger.info("Assuming engine is off. Taking a %ds long nap, then trying again." % naptime)
                self.stop()
                time.sleep(naptime)

    def start(self):
        logger.info("MaxOBD::start()")
        self.reset_connection()
        logger.info("MaxOBD::start()::Finally got connection. Starting OBD...")
        self.set_watchers()
        self.con.start()
                
        logger.info("MaxOBD started")
