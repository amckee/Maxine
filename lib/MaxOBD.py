from obd import OBDStatus
import obd, logging

logger = logging.getLogger(__name__)

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.RPM).value.to('mph')
    # TODO: update commands.GET_CURRENT_DTC for each engine start

    def __init__(self):
        self.con = obd.Async()
        if self.con.status() == OBDStatus.CAR_CONNECTED:
            logger.info("Connection to car successfull")
        elif self.con.status() == OBDStatus.ELM_CONNECTED:
            logger.error("Connection to ELM succeeded, connection to car failed")
        else:
            logger.error("Failed to connect to anything. Is car on?")

    #def reset(self): #TODO: do we need this, or is there another way?

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

    def stop(self):
        self.con.stop()
        self.con.unwatch_all()
        self.con.close()
        logger.info("MaxOBD stopped")

    def start(self):
        self.con.watch(obd.commands.COOLANT_TEMP)
        self.con.watch(obd.commands.ENGINE_LOAD)
        self.con.watch(obd.commands.OIL_TEMP)
        self.con.watch(obd.commands.RPM)
        self.con.watch(obd.commands.SPEED)
        self.con.watch(obd.commands.THROTTLE_POS)
        self.con.watch(obd.commands.TIMING_ADVANCE)

        self.con.start()
        logger.info("MaxOBD started")
