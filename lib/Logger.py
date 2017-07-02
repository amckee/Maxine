import datetime

class Logger:
    # main logging class
    # for now, just dump shit to screen
    # TODO: log to file
    logfile = None

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
        logline = "[%s] [%s]:\t%s" % (dt.strftime("%Y.%m.%d %H:%M:%S"), self.parent, msg)
        print(logline)
        if self.logfile:
            self.logfile.write(logline)

    def log_to_file(self, fn=None):
        if fn is None:
            self.log("ERROR: No file name given for external log. External logging disabled.")
            #close the logfile if it exists
            if self.logfile is not None:
                self.logfile.close()            
            return
        self.logfile = open(fn, 'a')
