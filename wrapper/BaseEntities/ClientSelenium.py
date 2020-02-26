from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from wrapper.BaseEntities.Logger import Logger
from wrapper.BaseEntities.Common import Common

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from wrapper.BaseEntities.CustomErrorHandler import *
from wrapper.config import *
import time

import sys

sys.path.append(".")


class ClientSelenium:
    def __init__(self):
        self._setBrowser()
        self.logger = Logger('Test1_Client.log')
        self.common = Common(self.browser)
        self.clientTable = None

    def _setBrowser(self):
        self.options = Options()
        self.options.headless = False
        self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.browser.set_window_size(1200, 1000)
        self.browser.error_handler = MyHandler()

    def removeElementsWhichAreNoChildsFor(self, elements, parent):
        if parent is '' or parent is None:
            return elements
        newList = []
        for element in elements:
            aux = self.browser.find_element_by_id(element)
            if aux is parent:
                newList.append(element)
        return newList

    def getRandomTab(self):
        tabs = self.common.getElementsWhichContains('tab-t0-')

        if len(tabs) > 1:
            self.logger.Log(str(len(tabs)) + " Len Tabs")
            index = randint(0, len(tabs) - 1)
            self.logger.Log('[Action] - getRandomTab [Tab]:' + tabs[index])
            return tabs[index]
        return None

    def getRandomSubtab(self, parent=''):
        subtabs = self.common.getChildrenWhichContains(parent, 'subtab_')
        self.logger.Log('[Action] - getRandomSubtab  [parent]-' + parent)
        if len(subtabs) > 1:
            index = randint(0, len(subtabs) - 1)
            self.logger.Log(
                '[Action] - getRandomSubtab [subtab]:' + subtabs[index])
            return subtabs[index]
        return None

    def getRandomMenuItem(self, parent=''):
        menuItems = self.common.getChildrenWhichContains(parent, 'menu_item_')

        self.logger.Log('[Action] - getRandomMenuItem [parent]-' + parent)
        if len(menuItems) > 1:
            index = randint(0, len(menuItems) - 1)
            self.logger.Log(
                '[Action] - getRandomMenuItem [MenuItem]:' + menuItems[index])
            return menuItems[index]
        return None

    def getRandomItemCustomization(self):
        cust = self.common.getElementsWhichContains(
            'order_item_customization_group_')
        if len(cust) > 1:
            index = randint(0, len(cust) - 1)
            self.logger.Log(
                '[Action] - getRandomItemCustomization [order_item_customization_group_]:' + cust[index])
            return cust[index]
        return None

    def increaseQuantity(self, quantity=0):
        if quantity is 0:
            quantity = randint(0, 10)
        self.common.ClickOn(
            "oder_item_customization_increase_quantity", quantity)
        self.logger.Log('[Action] - increaseQuantity ')

    def decreaseQuantity(self, quantity=0):
        if quantity is 0:
            quantity = randint(0, 10)
        self.common.ClickOn(
            "oder_item_customization_decrease_quantity", quantity)
        self.logger.Log('[Action] - decreaseQuantity ')

    def addCommentToOrder(self, comment=''):
        if comment is '':
            comment = "This Is a String Added For Test"

        element = self.browser.find_element_by_id(
            "oder_item_customization_instructions")
        element.find_element_by_tag_name("textarea").send_keys(comment)
        self.logger.Log(
            '[Action] - addCommentToOrder - [Comment added]: ' + comment)

    def hideSidebar(self):
        if self.common.CheckIfElementIsDisplayed('restaurant_swipe_right') is 1:
            self.common.ClickOn('restaurant_swipe_right')
            self.logger.Log('[Action] - hide Siderbar ')
        else:
            self.logger.Log('[Error - Action] - hide sidebar is not posible  ')

    def showSidebar(self):
        if self.common.CheckIfElementIsDisplayed('restaurant_swipe_left') is 1:
            self.common.ClickOn('restaurant_swipe_left')
            self.logger.Log('[Action] - show sidebar ')
        else:
            self.logger.Log('[Error - Action] - show sidebar is not posible  ')

    def sendOrder(self):
        self.common.ClickOn('order_button_update_order')
        self.logger.Log('[Action] - send order ')

    def addToOrder(self):
        self.common.ClickOn('oder_item_customization_add_to_order')
        self.logger.Log('[Action] - add to order ')

    def _payTheOrder(self):
        self.result = self.common.waitForElementToBeDisplayed('order_button_pay_button')
        if self.result is True:
            self.common.ClickOn('order_button_pay_button')
            self.logger.Log('[Action] - payTheOrder ')
        else:
            self.logger.Log('[Error - Action] - payTheOrder is not possible ')

    def selectPaymentType(self, paymentType='Cash'):
        time.sleep(2)
        if paymentType is 'Cash':
            self.common.ClickOn('payment_radio_Cash')
        elif paymentType is 'Card':
            self.common.ClickOn('payment_radio_Card')

        self.logger.Log('[Action] - selectPaymentType [Type] ' + paymentType)

    def confirmPayment(self):
        retry = 10
        while self.common.CheckIfElementIsDisplayed('payment_confirm') is 0 and retry > 0:
            time.sleep(3)
            retry -= 1

        if self.common.CheckIfElementIsDisplayed('payment_confirm') is 1:
            self.common.ClickOn('payment_confirm')
            self.logger.Log('[Action] - confirmPayment ')
        else:
            self.logger.Log('[Error - Action] - confirmPayment is not possible ')

    def _finishOrder(self):
        retry = 10
        while self.common.CheckIfElementIsDisplayed('finish_order') is 0 and retry > 0:
            time.sleep(1)
            retry -= 1

        if self.common.CheckIfElementIsDisplayed('finish_order') is 1:
            self.common.ClickOn('finish_order')
            self.logger.Log('[Action] - finish_order ')
        else:
            self.logger.Log('[Error - Action] - finish_order is not possible ')

    def endClientSession(self):
        self.browser.get("http://localhost:8100")
        self.browser.set_window_size(945, 1031)
        WebDriverWait(self.browser, 30).until(
            expected_conditions.element_to_be_clickable((By.ID, "welcome-abandon-button")))
        self.browser.find_element_by_id("welcome-abandon-button").click()
        self.logger.Log('[Action] - endClientSession')

    def startClientSession(self):
        self.browser.get("http://localhost:8100")

        self.common.ClickOn("welcome-start-button")
        self.logger.Log('[Action] - startClientSession')


    def setTableNumber(self):
        time.sleep(1)
        self.showSidebar()
        time.sleep(1)
        elements = self.common.getElementsWhichContains('orderTableNumber_')
        self.logger.Log('Found OrderTableNumber elements -> ')
        self.logger.Log(len(elements))
        if len(elements) == 1:
            self.logger.Log('Table found ' + elements[0])
            self.clientTable = int(elements[0].replace('orderTableNumber_', ''))
            Config.currentTableNumber = self.clientTable
            self.logger.Log('Client Table is  -> ')
            self.logger.Log(self.clientTable)

    def getTableNumber(self):
        time.sleep(3)
        self.logger.Log('Active Table Number is  -> ' + str(self.clientTable))
        return self.clientTable

    def randomizeMenuSelection(self, maxNrItems=3):
        iterations = 0

        self.logger.Log(maxNrItems)
        while iterations < maxNrItems:
            self.logger.Log('Number Of Iterations ' + str(iterations) + '/' + str(maxNrItems))
            time.sleep(3)
            tabId = self.getRandomTab()
            self.common.ClickOn(tabId)

            subtabId = self.getRandomSubtab(tabId)
            self.common.ClickOn(subtabId)

            menuItemId = self.getRandomMenuItem(subtabId if subtabId is not None else tabId)
            self.common.ClickOn(menuItemId)

            self.increaseQuantity()

            customizationsMenuItemId = self.getRandomItemCustomization()
            self.common.ClickOn(customizationsMenuItemId)

            self.addCommentToOrder()

            self.addToOrder()
            iterations = iterations + 1

        time.sleep(3)
        self.sendOrder()
        time.sleep(2)

    def pay(self):

        self.showSidebar()
        self._payTheOrder()
        self.selectPaymentType('Cash')
        self.confirmPayment()
        #self.finishOrder()

    def _orderAndPay(self):
        self.startClientSession()
        self.randomizeMenuSelection(1)
        self.pay()

