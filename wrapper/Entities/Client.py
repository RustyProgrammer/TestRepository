from wrapper.BaseEntities.ClientSelenium import *
from wrapper.BaseEntities.GenericEntity import *


class Client(ClientSelenium, GenericEntity):
    def __init__(self):
        ClientSelenium.__init__(self)
        GenericEntity.__init__(self)

    # def startSession(self):
    #     self.addAction(self.startClientSession(), [])

    def authenticate(self):
        self.addAction(self.startClientSession, [])

    def orderAndPay(self):
        self.addAction(self._orderAndPay, [])

    def orderSomethingRandom(self):
        self.addAction(self.randomizeMenuSelection, [1])

    def payTheOrder(self):
        self.pay()
        #self.addAction(self.pay, [])

    def finishOrder(self):
        self.addAction(self._finishOrder, [])

    def SaveTableNumber(self):
        self.addAction(self.getTableNumber(),[])
