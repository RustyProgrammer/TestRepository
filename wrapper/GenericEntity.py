from queue import Queue
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from wrapper.CustomErrorHandler import *


class GenericEntity:
    def __init__(self):
        self._actionQueue = Queue()
        self.thread = None
        self.success = list()
        self.options = Options()
        self.options.headless = False
        self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.browser.set_window_size(1200, 1000)
        self.browser.error_handler = MyHandler()

    def _exec(self):
        while not self._actionQueue.empty():
            action, args = self._actionQueue.get()
            self.success.append((action, action(*args)))

    def addAction(self, action, args):
        self._actionQueue.put((action, args))
        if self.thread is not None and not self.thread.is_alive():
            self.thread = Thread(target=self._exec)
            self.thread.start()

    def stop(self):
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        self.browser.quit()
