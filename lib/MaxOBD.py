from obd import OBDStatus
import obd, logging, os.path, subprocess, time
from serial.serialutil import SerialException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async = False # run with async setup / set to false for comparing to non async method
stop = False # set this to true at any time to stop the main loop

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.RPM).value.to('mph')
    # TODO: update commands.GET_CURRENT_DTC for each engine start

    def __init__(self):
        logger.info("MaxOBD::init()")

    def bind_bluetooth(self):
        logger.info("MaxOBD::bind_bluetooth()")
        logger.info("TODO: implement device connection management in python")
        subprocess.call("/home/pi/bin/Maxine/utils/connect_obd.sh")

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

    def stop(self):
        logger.info("MaxOBD::stop()")
        stop = True
        if self.con is not False:
            self.con.stop()
            self.con.unwatch_all()
            self.con.close()
            logger.info("MaxOBD stopped")
        else:
            logger.info("MaxOBD has no connection")

    def ensure_obd_device(self):
        logger.info("MaxOBD::ensure_obd_device()")
        #ensure OBD device exists and is connected
        ## return true for success, false for failure
        if not os.path.exists( '/dev/rfcomm0' ):
            logger.warning("/dev/rfcomm0 not found. Attempting to bind...")
            self.bind_bluetooth()

        if os.path.exists( '/dev/rfcomm0' ):
            try:
                logger.info("/dev/rfcomm0 found; opening connection...")
                self.con = obd.Async() #actually start obd communications
                return True
            except SerialException:
                logger.error("Device reports readiness to read but returned no data.")
            except:
                logger.error("Failed to connect to OBD.")
                return False

            ## lets get picky later
            #if self.con.status() == OBDStatus.CAR_CONNECTED:
            #    logger.info("Connection to car successful")
            #    return True
            #elif self.con.status() == OBDStatus.ELM_CONNECTED:
            #    logger.error("Connection to ELM succeeded, connection to car failed")
            #else:
            #    logger.error("Failed to connect to anything. Is car on?")
        else:
            logger.error("/dev/rfcomm0 does not exist!")
            self.con = False
        return False

    def set_watchers(self):
        logger.info("MaxOBD::set_watchers()")
        self.con.watch(obd.commands.COOLANT_TEMP, force=True)
        self.con.watch(obd.commands.ENGINE_LOAD, force=True)
        self.con.watch(obd.commands.OIL_TEMP, force=True)
        self.con.watch(obd.commands.RPM, force=True)
        self.con.watch(obd.commands.SPEED, force=True)
        self.con.watch(obd.commands.THROTTLE_POS, force=True)
        self.con.watch(obd.commands.TIMING_ADVANCE, force=True)

    def start(self):
        logger.info("MaxOBD::start()")
        naptime = 10

        while not stop:
            if not self.ensure_obd_device():
                logger.info("Assuming engine is off. Taking a %ds long nap, then trying again." % naptime)
                try:
                    # if there's no 'con' object, this throws an AttributeError
                    # doing this anyways to be sure this thing is done
                    time.sleep(1)
                    self.con.stop()
                except:
                    logger.warning("Attempted to stop undefined obd connection.")
                time.sleep(naptime)
                continue
            else:
                self.set_watchers()
                self.con.start()
                
        logger.info("MaxOBD started")
