import obd
from lib import Logger

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.RPM).value.to('mph')
    # TODO: update commands.GET_CURRENT_DTC for each engine start

    def __init__(self):
        self.logger = Logger.Logger(self)
        self.con = obd.OBD() #auto connects to rfcomm0
        self.logger.log("MaxOBD init completed")

    #def reset(self): #TODO: do we need this, or is there another way?

    def get_data(self, obdcmd):
        dat = self.con.query(obdcmd)
        if dat.value is None:
            dat.value = "0"
        return dat

