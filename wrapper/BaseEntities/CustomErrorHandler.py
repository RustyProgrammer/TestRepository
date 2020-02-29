import json

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.errorhandler import ErrorHandler


class MyHandler(ErrorHandler):
    def check_response(self, response):
        try:
            super(MyHandler, self).check_response(response)
        except NoSuchElementException as e:
            e.stacktrace = None
            # PhantomJS specific line:
            e.msg = json.loads(e.msg)['errorMessage']
