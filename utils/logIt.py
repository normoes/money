import os

class logIt():
    def __init__(self, path, filename, debug = False):
        self.filename = filename
        self.path = path
        self.debug = debug
        self.fh = None
    def log(self, toLog):
        if self.debug:
            ## terminal output
            print toLog
            ## log file output
            self.fh = open(os.path.join(self.path,self.filename), 'a')
            try:            
                self.fh.write(toLog+'\n')
            except IOERROR as e:
                print 'no access to log file:', self.filename
                print e
            finally:
                self.fh.close()
