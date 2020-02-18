from wrapper.BaseEntities.WaiterSelenium import *
from wrapper.BaseEntities.GenericEntity import GenericEntity


class Chef(WaiterSelenium, GenericEntity):
    def __init__(self):
        WaiterSelenium.__init__(self)
        GenericEntity.__init__(self)
        self.username = "chef"

    def startSession(self):
        self.addAction(self.logIn, [])

    def endSession(self):
        self.addAction(self._LogoutWaiter, [])

    def authenticate(self):
        self.addAction(self.logIn, [])

    def _cook(self):
        self._logIn()
        # ar putea fi un loop aici pentru thread
        count = 200
        while count > 0:
            self._logger.Log('Check count -> V')
            self._logger.Log(200 - count)
            self._parseTasks()
            count -= 1
            time.sleep(5)

    # Threaded Method
    def cook(self):
        self.addAction(self._cook, [])

    def _takeTask(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_acknowledge_')

    def _sendToWaiter(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_done_')

    def takeTask(self, tableNumber):
        self.addAction(self._takeTask, [tableNumber])

    def sendToWaiter(self, tableNumber):
        self.addAction(self._sendToWaiter, [tableNumber])
