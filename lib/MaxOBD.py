import obd, time
from lib import Logger

# pip3 install obd
from obd import commands as obd_values

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.RPM).value.to('mph')
    # TODO: update commands.GET_CURRENT_DTC for each engine start

    def __init__(self):
        self.logger = Logger.Logger(self)
        #self.logger.log("Establishing OBD Connection...")
        #self.con = obd.OBD() #auto connects to rfcomm0
        self.logger.log("Establishing Async OBD Connection...")
        self.acon = obd.Async() # same as OBD() but with watchers

        self._set_watchers() #must set watchers while stopped
        self.acon.start()

        self.logger.log("OBD Status: %s" % self.acon.status())

    def _set_watchers(self):
        self.logger.log("Setting watchers...")
        # TODO: error handling (detect vehicle on or off)
        self.acon.watch(obd_values.THROTTLE_POS)
        self.acon.watch(obd_values.COOLANT_TEMP)
        self.acon.watch(obd_values.RPM)
        self.acon.watch(obd_values.SPEED)
        self.acon.watch(obd_values.ENGINE_LOAD)

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

    def reset(self):
        self.logger.log("Resetting ODB")
        self.acon.stop()
        time.sleep(.5)
        self.acon.start()
