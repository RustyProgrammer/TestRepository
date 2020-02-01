# Generated by Selenium IDE

import pytest
import time
import json
import logging
import sys
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from multiprocessing import Queue

from wrapper.Chef import Chef
from wrapper.Waiter import Waiter



class Test_1_Suite():
    def setup_method(self, method):
        self.options = Options()
        #self.options.headless = True
        self.client_chrome = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.waiter_chrome = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.chef_chrome = webdriver.Chrome(
            '/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.client_chrome.set_window_size(1200, 1000)
        self.waiter_chrome.set_window_size(1200, 1000)
        self.chef_chrome.set_window_size(1200, 1000)
        self.vars = {}

    def teardown_method(self, method):
        self.client_chrome.quit()
        self.waiter_chrome.quit()
        self.chef_chrome.quit()

    def test_Main(self):
        from wrapper.Client import Client
        self.client = Client(self.client_chrome)
        self.waiter = Waiter(self.waiter_chrome)
        self.chef = Chef(self.chef_chrome)
        self.q = Queue()
        t1 = Thread(target=self.client.commandAndPay, args=(self.q, ) )
        t2 = Thread(target=self.waiter.serve, args=(self.q, ) )
        t3 = Thread(target=self.chef.cook, args=(self.q, ) )

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()
