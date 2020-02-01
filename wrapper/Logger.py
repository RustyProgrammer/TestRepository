import pprint

class Logger():
    def __init__(self,logFile):
        self.file=logFile
        
    def Log(self, string):
        f = open(self.file, "a+")
        #f.write(string+"\n")
        pprint.pprint(string, f)
        f.close()
