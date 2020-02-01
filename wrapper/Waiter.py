from random import randint
from wrapper.Logger import Logger
from wrapper.Common import Common
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import sys

sys.path.append(".")

from wrapper.GenericEntity import *

ABSENT = 0
EXIST = 1


class Waiter(GenericEntity):
    def __init__(self):
        super(Waiter, self).__init__()
        self.logger = Logger('Test1_Waiter.log')
        self.common = Common(self.browser)
        self.username = "waiter"
        self.password = "pass"

    def _SetUsername(self, username):
        time.sleep(2)
        elementId = 'waiter_login_username'
        if self.common.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId + "- Waiting to be clickable")
            WebDriverWait(self.browser, 30).until(expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(username)
            time.sleep(2)
        else:
            self.logger.Log(elementId + " does not exist")
        return None

    def _SetPassword(self, password):
        time.sleep(2)
        elementId = 'waiter_login_password'
        if self.common.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId + "- Waiting to be clickable")
            WebDriverWait(self.browser, 30).until(expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(password)
            time.sleep(2)
        else:
            self.logger.Log(elementId + " does not exist")
        return None

    def _LogoutWaiter(self):
        self.common.ClickOn('tasks_menu_toggle')
        self.common.ClickOn('waiter_sidebar_Logout')

    def _LoginWaiter(self, username):
        self._SetUsername(self.username)
        self._SetPassword(self.password)
        self.common.ClickOn("waiter_login_submit")

    def logIn(self):

        self.browser.get("http://localhost:8101")
        time.sleep(3)
        if self.common.CheckIfElementExists("tasks_menu_toggle") is not ABSENT:
            loggedUser = self.browser.find_element_by_id("app_user_role")
            if self.username not in loggedUser.text:
                self._LogoutWaiter()
                self._LoginWaiter(self.username)
        else:
            self._LoginWaiter(self.username)
        time.sleep(5)

    # step 1 - Assign a table but keep table number
    def getUnassignedTables(self):
        # task_assign_to_me
        unassigned = self.common.GetAllElementsWhichContains('task_assign_to_me')
        if len(unassigned) > 0:
            return unassigned
        return None

    def getTableOrders(self, tableId):
        tableOrders = self.common.GetAllElementsWhichContains('task_verified')
        # task_verified
        toVerify = self.common.GetAllElementsWhichContains('task_verified')
        if len(toVerify) > 0:
            return toVerify
        return None

    def acknowledgeAllTasks(self):
        # task_acknowledge
        acknowledge = self.common.GetAllElementsWhichContains('task_acknowledge')
        if len(acknowledge) > 0:
            for task in acknowledge:
                task.click()
                time.sleep(2)

    def getAllTasks(self):
        # task_assign_to_me
        tasks = self.common.GetAllElementsWhichContains('taskCardDiv_')
        if len(tasks) > 0:
            return tasks
        return None

    def parseTasks(self):
        time.sleep(3)
        # get all tasks to iterate through them
        availableTasks = self.getAllTasks()
        if availableTasks is not None:
            self.logger.Log("availableTasks -> ")
            self.logger.Log(len(availableTasks))

            # take action for every task type
            for task in availableTasks:
                self.logger.Log(task.get_attribute('id'))
                id = task.get_attribute('id').replace('taskCardDiv_', '')

                taskAssignToMeId = 'task_assign_to_me_' + id
                taskVerifiedId = 'task_verified_' + id
                taskAcknowledgeId = 'task_acknowledge_' + id
                taskDoneId = 'task_done_' + id

                if taskAssignToMeId in task.get_attribute('innerHTML'):
                    self.logger.Log('Found ' + taskAssignToMeId)
                    self.common.ClickOn(taskAssignToMeId)
                elif taskVerifiedId in task.get_attribute('innerHTML'):
                    self.logger.Log('Found ' + taskVerifiedId)
                    self.common.ClickOn(taskVerifiedId)
                elif taskAcknowledgeId in task.get_attribute('innerHTML'):
                    self.logger.Log('Found ' + taskAcknowledgeId)
                    self.common.ClickOn(taskAcknowledgeId)
                elif taskDoneId in task.get_attribute('innerHTML'):
                    self.logger.Log('Found ' + taskDoneId)
                    self.common.ClickOn(taskDoneId)
        else:
            self.logger.Log('AvailableTasks is None')

    def _serve(self):
        self.logIn()
        # ar putea fi un loop aici pentru thread
        count = 10
        while count > 0:
            self.logger.Log('Check count -> V')
            self.logger.Log(200 - count)
            self.parseTasks()
            count -= 1
            time.sleep(5)

    def serve(self):
        self.addAction(self._serve(), [])
