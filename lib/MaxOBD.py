import obd, logging, os.path, subprocess, time, threading
from serial.serialutil import SerialException
from obd import OBDStatus

class MaxOBD( object ):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.SPEED).value.to('mph')
    con = None
    obdlog = None
    logger = logging.getLogger( "maxine.obd" )

    def __init__( self ):
        fhandler = logging.FileHandler( "/dev/shm/obdstat.dat", mode='a' )
        fhandler.setFormatter( logging.Formatter( '%(asctime)s,%(message)s' ) )

        self.obdlog = logging.getLogger( 'obdstat' )
        self.obdlog.setLevel( logging.INFO )
        self.obdlog.addHandler( fhandler )

    def set_watchers( self ):
        logger.info( "Setting watchers..." )
        self.con.watch( obd.commands.COOLANT_TEMP, force=True ) #, callback=self.new_coolant_temp)
        self.con.watch( obd.commands.ENGINE_LOAD, force=True ) #, callback=self.new_load)
        self.con.watch( obd.commands.RPM, force=True ) #, callback=self.new_rpm)
        self.con.watch( obd.commands.THROTTLE_POS, force=True ) #, callback=self.new_tps)
        self.con.watch( obd.commands.SPEED, force=True )
        self.con.watch( obd.commands.TIMING_ADVANCE, force=True )

    def obd_log_loop(self):
        while True:
            mph = rpm = tps = temp = volt = -1

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
            time.sleep(1)

        self.logger.info( "OBD log loop stopped" )

    def start( self ):
        logthread = threading.Thread( target=self.obd_log_loop )

        while True:
            self.con = obd.OBD()

            if self.con.is_connected():
                logthread.start()
            else:
                self.logger.error('Failed to connect to OBD device')

            time.sleep( 5 )

        if self.con is not None:
            self.con.close()
        self.logger.info( "MaxOBD::start() finished" )
