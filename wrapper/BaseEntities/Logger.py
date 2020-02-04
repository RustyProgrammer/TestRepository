import pprint

class Logger():
    def __init__(self,logFile):
        self.file='./Logs/'+logFile
        
    def Log(self, string):
        f = open(self.file, "a+")
        pprint.pprint(string, f)
        f.close()
