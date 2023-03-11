import obd, logging, os.path, subprocess, time, threading
from serial.serialutil import SerialException
from obd import OBDStatus

## main logging mechanism
logger = logging.getLogger( "maxine.obd" )

class MaxOBD( object ):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')
    con = None

    def __init__( self ):
        if not os.path.exists( "/dev/rfcomm0" ):
            proc = subprocess.Popen(['sudo', 'rfcomm', 'bind', 'rfcomm0', '88:1B:99:1D:1F:5E'])
            logger.info( "Created rfcomm0 device" )

        logger.info( "OBD Started" )

    def set_watchers( self ):
        logger.info( "Setting watchers..." )
        self.con.watch( obd.commands.COOLANT_TEMP, force=True ) #, callback=self.new_coolant_temp)
        self.con.watch( obd.commands.ENGINE_LOAD, force=True ) #, callback=self.new_load)
        self.con.watch( obd.commands.RPM, force=True ) #, callback=self.new_rpm)
        self.con.watch( obd.commands.THROTTLE_POS, force=True ) #, callback=self.new_tps)
        self.con.watch( obd.commands.SPEED, force=True )
        self.con.watch( obd.commands.TIMING_ADVANCE, force=True )

    def _clean_input( self, resp ):
        #logger.info( "resp: %s" % resp )
        if not resp.is_null():
            return resp.magnitude
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
            mph, rpm, tps, temp, volt = -1

            tmph = self.con.query( obd.commands.SPEED )
            if tmph is not None:
                mph = tmph.value.to('mph').magnitude

            ttemp = self.con.query( obd.commands.COOLANT_TEMP )
            if ttemp is not None:
                temp = ttemp.value.to('degF').magnitude

            trpm = self.con.query( obd.commands.RPM )
            if trpm is not None:
                rpm = trpm.value.magnitude
            
            ttps = self.con.query( obd.commands.THROTTLE_POS )
            if ttps is not None:
                tps = format( ttps.value.magnitude, '.2f' )
            
            tvolt = self.con.query( obd.commands.ELM_VOLTAGE )
            if tvolt is not None:
                volt = tvolt.value.magnitude

            obdlog.info( "%s,%s,%s,%s,%s" % (mph,rpm,tps,temp,volt) )

        logger.info( "OBD log loop stopped" )

    def start( self ):
        logthread = threading.Thread( target=self.obd_log_loop )

        while True:
            #self.con = obd.Async()
            try:
                self.con = obd.OBD()

                if self.con.is_connected():
                    logger.info( "OBD Connection established.")
                    logthread.start()
                else:
                    logger.info( "Failed to connect to OBD device. Looping..." )
            except:
                logger.info( "Connection failed. Delaying next loop attempt 5s..." )
            finally:
                time.sleep( 5 )

        logger.info( "MaxOBD::start() finished" )
