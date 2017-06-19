import datetime

class Logger:
    # main logging class
    # for now, just dump shit to screen
    # TODO: log to file

    def __init__(self, parent=""):
        # with the parent variable, we can better log details
        if parent == "":
            self.parent = parent
        else:
            self.parent = type(parent).__name__
        
    def log(self, msg=""):
        if msg == "":
            return
        dt = datetime.datetime.now()
        if self.parent == "":
            print("[%s] %s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), msg))
        else:
            print("[%s] %s: %s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), self.parent, msg))
