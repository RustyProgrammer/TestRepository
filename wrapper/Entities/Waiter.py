from wrapper.BaseEntities.WaiterSelenium import *
from wrapper.BaseEntities.GenericEntity import *


class Waiter(WaiterSelenium, GenericEntity):
    def __init__(self):
        WaiterSelenium.__init__(self)
        GenericEntity.__init__(self)

    def startSession(self):
        self.logIn()
        #self.addAction(self.logIn, [])

    def endSession(self):
        self._LogoutWaiter()
        #self.addAction(self._LogoutWaiter, [])

    def authenticate(self):
        self.logIn()
        #self.addAction(self.logIn, [])

    def _serve(self, tableNumber):
        # ar putea fi un loop aici pentru thread
        count = 10
        while count > 0:
            self.logger.Log('Check count -> V')
            self.logger.Log(200 - count)
            self.parseTasks()
            count -= 1
            time.sleep(5)

    def serve(self, tableNumber):
        self._serve(tableNumber)
        #self.addAction(self._serve, [tableNumber])

    def _assignTable(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_assign_to_me_')

    def assignTable(self, tableNumber):
        self._assignTable(tableNumber)
        #self.addAction(self._assignTable, [tableNumber])

    def sendToChef(self, tableNumber):
        self._sendToChef(tableNumber)
        #self.addAction(self._sendToChef, [tableNumber])

    def _sendToChef(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_verified_')

    def _confirmTaskToChef(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_acknowledge_')

    def _confirmTaskToClient(self, tableNumber):
        self.checkAndClick(tableNumber, 'task_done_')

    def confirmTaskToChef(self, tableNumber):
        self._confirmTaskToChef(tableNumber)
        #self.addAction(self._confirmTaskToChef, [tableNumber])

    def confirmPayment(self, tableNumber):
        self._confirmTaskToChef(tableNumber)
        #self.addAction(self._confirmTaskToChef, [tableNumber])

    def confirmTaskToClient(self, tableNumber):
        self._confirmTaskToClient(tableNumber)
        #self.addAction(self._confirmTaskToClient, [tableNumber])
