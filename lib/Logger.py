import datetime

class Logger:
    # main logging class
    # for now, just dump shit to screen
    # TODO: log to file

    def __init__(self, parent=""):
        # with the parent variable, we can better log details
        if type(parent) == str:
            self.parent = parent
        else:
            self.parent = type(parent).__name__
        
    def log(self, msg=""):
        if msg == "":
            return
        dt = datetime.datetime.now()
        print("[%s] [%s]:\t%s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), self.parent, msg))
