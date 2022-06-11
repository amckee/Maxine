import obd, logging, os.path, subprocess, time, bluetooth, threading
from serial.serialutil import SerialException
from obd import OBDStatus
from bluetooth import *

## main logging mechanism
logger = logging.getLogger( "maxine.obd" )

obd_name = "FIXD"
obd_addr = None

class MaxOBD( object ):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')

    def __init__( self ):
        self.obd_name = obd_name
        self.obd_addr = obd_addr
        #self.obd_addr = "88:1B:99:1D:1F:5E" #uncomment for super debug override
        logger.info( "OBD Started" )

    def find_obd_device( self ):
        ## return bluetooth address if found, otherwise return None
        logger.info( "Looking for bluetooth devices..." )
        nearby_devices = bluetooth.discover_devices()
        logger.info( "Found %s bluetooth devices nearby" % len(nearby_devices) )
        
        for device in nearby_devices:
            if self.obd_name == bluetooth.lookup_name( device ):
                self.obd_addr = device
                return device
        return None

    def drop_bluetooth( self ):
        logger.warning( "Dropping all bluetooth everythings..." )
        logger.info( "# sudo rfcomm unbind 0" )
        subprocess.call( ['sudo', 'rfcomm', 'unbind', '0'] )
        logger.info( "# sudo hcitool dc %s" % self.obd_addr )
        subprocess.call( ['sudo', 'hcitool', 'dc', self.obd_addr] )
        self.obd_addr = None

    def stop( self ):
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
        logger.warning( "Bluetooth and OBD connections completely stopped." )

    def set_watchers( self ):
        logger.info( "Setting watchers..." )
        self.con.watch( obd.commands.COOLANT_TEMP, force=True ) #, callback=self.new_coolant_temp)
        self.con.watch( obd.commands.ENGINE_LOAD, force=True ) #, callback=self.new_load)
        self.con.watch( obd.commands.RPM, force=True ) #, callback=self.new_rpm)
        self.con.watch( obd.commands.THROTTLE_POS, force=True ) #, callback=self.new_tps)
        self.con.watch( obd.commands.SPEED, force=True )
        self.con.watch( obd.commands.TIMING_ADVANCE, force=True )

    def connect_bluetooth( self ):
        logger.info( "Connecting to %s at %s" % (self.obd_name, self.obd_addr) )
        if self.obd_addr is None:
            logger.error( "No device address given!? Bailing out" )
            return False

        ## old method, seems dumb
        subprocess.call( ['sudo', 'hcitool', 'cc', self.obd_addr] )
        subprocess.call( ['sudo', 'rfcomm', 'bind', '0', self.obd_addr] )
        #socket = BluetoothSocket( RFCOMM )
        #socket.connect((self.obd_addr,1))
        return True
    
    def connect_obd( self ):
        self.con = obd.Async()
        time.sleep(2)
        if self.con.is_connected():
            logger.info( "OBD Connection established. Starting services..." )
            self.set_watchers()
            self.con.start()
            logger.info( "Services started" )
            return True
        else:
            logger.info( "OBD Connection failed" )
        return False

    def restart( self ):
        logger.warning( "Restarting..." )
        self.stop()
        time.sleep(1) # driver is buggy. this helps.
        logger.info( "Stopped. Starting..." )
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
        logger.info( "OBD log loop started" )

        while True:
            try:
                mph = self._clean_input( self.con.query( obd.commands.SPEED ).value.to('mph') )
                rpm = self._clean_input( self.con.query( obd.commands.RPM ) )
                tps = format( self._clean_input( self.con.query( obd.commands.THROTTLE_POS ) ), '.2f' )
                temp = self._clean_input( self.con.query( obd.commands.COOLANT_TEMP ).value.to('f') )
                volt = self._clean_input( self.con.query( obd.commands.ELM_VOLTAGE ) )
                fuel = self._clean_input( self.con.query( obd.commands.FUEL_LEVEL ) )
                
                obdlog.info( "%s,%s,%s,%s,%s,%s" % (mph,rpm,tps,temp,volt,fuel) )
            except ValueError:
                logger.error( "OBD seems on but engine seems off" )
                time.sleep( 30 )
            except AttributeError:
                logger.error( "No OBD connection. Sleeping 30s" )
                time.sleep( 30 )
            except Exception as e:
                logger.error( "Failed to pull OBD data. Unhandled error is:\n%s" % str(e) )
                logger.info( "Sleeping 30s" )
                time.sleep( 30 )
                pass
            finally:
                time.sleep( 1 )
        logger.info( "OBD log loop stopped" )

    def start( self ):
        ## start logging thread
        logthread = threading.Thread( target=self.obd_log_loop )
        logthread.start()

        while True:
            dev = self.find_obd_device()
            
            if dev is not None:
                logger.info( "Found %s device at: %s" % (self.obd_name, self.obd_addr) )
                if self.connect_bluetooth():
                    logger.info( "connect_bluetooth() succeeded" )
                    if self.connect_obd():
                        logger.info( "connect_obd() succeeded" )
                    else:
                        logger.info( "connect_obd() failed" )
                else:
                    print( "connect_bluetooth() failed. Restarting and trying again..." )
                    self.stop()
            else:
                logger.info( "Failed to find OBD device. Looping..." )

        logger.info( "Start finished" )
