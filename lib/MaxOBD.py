from obd import OBDStatus
import obd, logging, os.path, subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        if self.con is not False:
            self.con.stop()
            self.con.unwatch_all()
            self.con.close()
            logger.info("MaxOBD stopped")
        else:
            logger.info("MaxOBD has no connection")

    def ensure_obd_device(self):
        logger.info("MaxOBD::ensure_obd_device()")
        #ensure OBD device
        if not os.path.exists( '/dev/rfcomm0' ):
            logger.warning("/dev/rfcomm0 not found. Attempting to bind...")
            self.bind_bluetooth()

        if os.path.exists( '/dev/rfcomm0' ):
            try:
                self.con = obd.Async()
            except:
                logger.error("Failed to connect to OBD.")
                return
            if self.con.status() == OBDStatus.CAR_CONNECTED:
                logger.info("Connection to car successful")
                return True
            elif self.con.status() == OBDStatus.ELM_CONNECTED:
                logger.error("Connection to ELM succeeded, connection to car failed")
            else:
                logger.error("Failed to connect to anything. Is car on?")
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

        if not self.ensure_obd_device():
            logger.error("Failed to connect to OBD.")
            return False

        self.set_watchers()
        
        self.con.start()
        logger.info("MaxOBD started")
