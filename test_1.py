from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Queue
from wrapper.Chef import Chef
from wrapper.Waiter import Waiter
from wrapper.Client import Client


class Test_1_Suite():

    def teardown_method(self, method):
        self.client.stop()
        self.waiter.stop()
        self.chef.stop()

    def test_Main(self):
        self.client = Client()
        self.waiter = Waiter()
        self.chef = Chef()

        ##self.client.orderAndPay()
        self.client.startSession()
        self.client.orderSomethingRandom()
        self.waiter.serve()
        self.chef.cook()
        self.client.payTheOrder()

        # self.client.stop()
        # self.waiter.stop()
        # self.chef.stop()
