from wrapper.Logger import Logger
import pytest
import time
import json
import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from random import randint
import random
import struct
import string
from pprint import pprint
sys.path.append('.')

ABSENT = 0
EXIST = 1


class Common():
    def __init__(self, browser):
        self.logger = Logger('Common.log')
        self.browser = browser

    def CheckIfElementExists(self, elementID):
        try:
            self.browser.find_element_by_id(elementID)
            return EXIST
        except:
            return ABSENT
        
    def CheckIfElementIsDisplayed(self, elementID):
        try:
            if self.browser.find_element_by_id(elementID).is_displayed():
                return EXIST
            else: 
                return ABSENT
        except:
            return ABSENT

    def GetAllElementsWhichContains(self, PartOfId):
        try:
            elements = self.browser.find_elements_by_css_selector(
                '[id*="%s"]' % PartOfId)
            return elements
        except:
            self.logger.Log("GetAllElementsWhichContains- NONE")
            return None

    def GetRandomOneOfAllElementsWhichContains(self, PartOfId):
        try:
            elements = self.browser.find_elements_by_css_selector(
                '[id*="%s"]' % PartOfId)
            self.logger.Log(json.dumps(elements) +
                            " Elements dumped - Menu_Item")
            return elements
        except:
            self.logger.Log("GetRandomOneOfAllElementsWhichContains- NONE")
            return None

    def GetRandomOneMenuItem(self, PartOfId):
        retry = 0
        while retry < 3:
            elements = self.GetRandomOneOfAllElementsWhichContains(PartOfId)
            if elements is not None:
                element = elements[randint(0, len(elements)-1)]
                self.logger.Log(json.dumps(element) +
                                " Element randomly selected - Menu_Item")
                return element
            else:
                retry += 1
                self.logger.Log(json.dumps(
                    PartOfId)+" does not exist in menu_item_\{some_id\} - retry number " + str(retry)+"/3")
                time.sleep(5)
        return None

    def ClickOn(self, elementId, times=1):
        if elementId is None:
            return None

        retry = 0

        while retry < 3:
            time.sleep(1)
            if self.CheckIfElementExists(elementId) is not ABSENT:
                self.logger.Log(
                    '[Action] [Waiting to be clickable] on ' + elementId)
                # WebDriverWait(self.browser, 30).until(
                #     expected_conditions.element_to_be_clickable((By.ID, elementId)))
                while times > 0:
                    self.logger.Log('[Action] [Click] on '+elementId)
                    self.browser.find_element_by_id(elementId).click()
                    times -= 1
                    time.sleep(1)
                break
            else:
                retry += 1
                if elementId is not None:
                    self.logger.Log(json.dumps(
                        elementId) + " does not exist - retry number " + str(retry)+"/3")
                else:
                    self.logger.Log("NONE- does not exist - retry number " +
                                    str(retry)+"/3")
                time.sleep(5)
        return None

    def SetUsername(self, username):
        elementId = 'waiter_login_username'
        if self.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId+"- Waiting to be clickable")
            WebDriverWait(self.browser, 30).until(
                expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(username)
            time.sleep(2)
        else:
            self.logger.Log(elementId+" does not exist")
            return None

    def SetPassword(self, password):
        elementId = 'waiter_login_password'
        if self.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId+"- Waiting to be clickable")
            WebDriverWait(self.browser, 30).until(
                expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(password)
            time.sleep(2)
        else:
            self.logger.Log(elementId+" does not exist")
            return None

    def LogoutWaiter(self):
        self.ClickOn('tasks_menu_toggle')
        self.ClickOn('waiter_sidebar_Logout')

    def LoginWaiter(self, username):
        password = "pass"
        self.SetUsername(username)
        self.SetPassword(password)
        self.ClickOn("waiter_login_submit")

    def test_getAllElements(self):
        time.sleep(2)
        ids = self.browser.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            # print ii.tag_name
            self.logger.Log(ii.get_attribute('id') +
                            " Element randomly selected - Menu_Item")
           # print ii.get_attribute('id')
        return ids

    def getElementsWhichContains(self, partOfId):
        elements = self.browser.find_elements_by_xpath('//*[@id]')
        found = []
        for element in elements:
            id = element.get_attribute("id")
            if partOfId in id:
                self.logger.Log('[Action] [getElementsWhichContains ] '+id +
                            " IDs Found")
                found.append(id)
        return found

    def getChildrenWhichContains(self, parent, partOfId):
        parentEl = self.browser.find_element_by_id(parent)
        childs = self.getElementsWhichContains(partOfId) 
               
        self.logger.Log('#####[parent has]##### - '+parentEl.text + ' #id# '+parentEl.get_property(
            "id") + ' # len # '+str(len(childs)) + ' #partOfId# '+partOfId)

        found = []
        for element in childs:
            self.logger.Log('[Action] [getElementsWhichContains ] [Parent]'+parentEl.text +' [child] '+element +
                            " IDs Found - need to be checked if it is child")
            if partOfId in element and self.CheckIfElementIsDisplayed(element) is EXIST:
                self.logger.Log('[Action] [getElementsWhichContains ] [Parent]'+parentEl.text +' [child] '+element +
                            " IDs Found")
                found.append(element)
        return found

    def randomString(stringLength=10):
        letters = string.ascii_lowercase
        return 'Random String : '.join(random.choice(letters) for i in range(stringLength))
