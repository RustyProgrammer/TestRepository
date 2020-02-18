import threading

from wrapper.Entities.Chef import *
from wrapper.Entities.Waiter import *
from wrapper.Entities.Client import *

class Test_1_Suite():

    def teardown_method(self, method):
        self.client.stop()
        self.waiter.stop()
        self.chef.stop()

    def test_Main(self):
        self.client = Client()
        self.waiter = Waiter()
        self.chef = Chef()

        self.chef.authenticate()
        self.waiter.authenticate()
        self.client.authenticate()

        self.tableNumber = self.client.getTableNumber()
        self.waiter.assignTable(self.tableNumber)
        self.client.orderSomethingRandom()
        self.chef.takeTask(self.tableNumber)
        self.chef.sendToWaiter(self.tableNumber)
        self.waiter.confirmTaskToChef(self.tableNumber)
        self.waiter.confirmTaskToClient(self.tableNumber)

        self.client.payTheOrder()

        self.waiter.confirmPayment(self.tableNumber)

        self.client.finishOrder()

        while threading.active_count() > 0:
            # ... look for new requests to handle ...
            time.sleep(1)
