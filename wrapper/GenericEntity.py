from time import sleep
from queue import Queue
from threading import Thread


class GenericEntity:
    def __init__(self):
        self._actionQueue = Queue()
        self.thread = None
        self.success = list()
        self.browser = None

    def _exec(self):
        while not self._actionQueue.empty():
            action, args = self._actionQueue.get()
            self.success.append((action, action(*args)))

    def addAction(self, action, args):
        self._actionQueue.put((action, args))
        if not self.thread or not self.thread.is_alive():
            self.thread = Thread(target=self._exec)
            self.thread.start()

    def stop(self):
        if self.thread.is_alive():
            self.thread.join()
