import obd, logging, os.path, subprocess, time, bluetooth, threading
from serial.serialutil import SerialException
from obd import OBDStatus
from bluetooth import *

## main logging mechanism
logger = logging.getLogger( "maxine.obd" )

obd_name = "OBDII"
obd_addr = None

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')

    def __init__(self):
        self.obd_name = obd_name
        self.obd_addr = obd_addr
        #self.obd_addr = "00:1D:A5:00:01:EB" #uncomment for super debug override

    def find_obd_device(self):
        ## scan for devices with 'OBDII' as the name
        ## return bluetooth address if found, otherwise return None
        logger.info("Scanning for all nearby bluetooth devices...")
        nearby_devices = bluetooth.discover_devices()
        logger.info("Found %s bluetooth devices nearby" % len(nearby_devices))
        if len(nearby_devices) > 0:
            for device in nearby_devices:
                if self.obd_name == bluetooth.lookup_name(device):
                    logger.info("Found %s at %s" % (self.obd_name, device))
                    self.obd_addr = device
                    return device
        return None

    def drop_bluetooth(self):
        logger.warning("Dropping all bluetooth everythings...")
        subprocess.call(['sudo', 'rfcomm', 'unbind', '0'])
        subprocess.call(['sudo', 'hcitool', 'dc', self.obd_addr])
        self.obd_addr = None
        
    def stop(self):
        #this feels ugly. there has to be a better way
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
        logger.warning("Bluetooth and OBD connections completely stopped.")
    
    def set_watchers(self):
        logger.info("Setting watchers...")
        self.con.watch(obd.commands.COOLANT_TEMP, force=True) #, callback=self.new_coolant_temp)
        self.con.watch(obd.commands.ENGINE_LOAD, force=True) #, callback=self.new_load)
        self.con.watch(obd.commands.RPM, force=True) #, callback=self.new_rpm)
        self.con.watch(obd.commands.THROTTLE_POS, force=True) #, callback=self.new_tps)
        self.con.watch(obd.commands.SPEED, force=True)
        self.con.watch(obd.commands.TIMING_ADVANCE, force=True)

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
        logger.warning("Restarting...")
        self.stop()
        time.sleep(1) # driver is buggy. this helps.
        self.start()

    def _clean_input( self, value ):
        #logger.info( "value: %s" % value )
        if not value.is_null():
            return value.value.magnitude
        return 0
    
    def obd_log_loop(self):
        obdlog = logging.getLogger( 'obdstat' )
        formatter = logging.Formatter( '%(asctime)s,%(message)s' )
        fhandler = logging.FileHandler( "/dev/shm/obdstat.dat", mode='w' )
        fhandler.setFormatter( formatter )
        shandler = logging.StreamHandler()
        shandler.setFormatter( formatter )
        
        obdlog.setLevel( logging.INFO )
        obdlog.addHandler( fhandler )
        obdlog.addHandler( shandler )
        #self.obdlog.propagate = False
        logger.info( "obd log loop started" )

        while True:
            try:
                mph = self._clean_input( self.con.query( obd.commands.SPEED ) )
                rpm = self._clean_input( self.con.query( obd.commands.RPM ) )
                tps = self._clean_input( self.con.query( obd.commands.THROTTLE_POS ) )
                temp = self._clean_input( self.con.query( obd.commands.COOLANT_TEMP ) )
                
                obdlog.info("%s,%s,%s,%s" % (mph,rpm,tps,temp))
            except Exception as e:
                logger.error( "Failed to pull OBD data:\n%s" % str(e) )
                logger.error( "Exiting..." )
                break
                #pass
            finally:
                time.sleep( 1 )
        logger.info( "obd log loop stopped" )

    def start(self):
        ## start logging thread
        logthread = threading.Thread( target=self.obd_log_loop )

        while True:
            if self.find_obd_device() is not None:
                self.connect_bluetooth()
                if self.connect_obd():
                    logthread.start()
                    logger.info("OBD Started")
