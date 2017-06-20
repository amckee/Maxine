import obd
from lib import Logger

class MaxOBD(object):
    # Note to self: how to run a query
    # data = obd.OBD().query(obd.commands.RPM).value.to('mph')

    def __init__(self):
        self.logger = Logger.Logger(self)
        self.con = obd.OBD() #auto connects to rfcomm0
        self.logger.log("MaxOBD init completed")

    def get_data(self, obdcmd):
        return self.con.query(obdcmd)
