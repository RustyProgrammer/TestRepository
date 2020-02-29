from wrapper.BaseEntities.Logger import Logger
from wrapper.BaseEntities.Common import Common
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from wrapper.BaseEntities.CustomErrorHandler import *

import sys

sys.path.append(".")

ABSENT = 0
EXIST = 1


class WaiterSelenium:
    def __init__(self):
        self._setBrowser()
        self.logger = Logger('Test1_Waiter.log')
        self.common = Common(self.browser)
        self.username = "waiter"
        self.password = "pass"

    def _setBrowser(self):
        self.options = Options()
        self.options.headless = False
        self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=self.options)
        self.browser.set_window_size(500, 500)
        # self.browser.error_handler = MyHandler()

    def _SetUsername(self, username):
        time.sleep(1)
        elementId = 'waiter_login_username'
        if self.common.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId + "- Waiting to be clickable")
            WebDriverWait(self.browser, 30).until(expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(username)
            time.sleep(1)
        else:
            self.logger.Log(elementId + " does not exist")
        return None

    def _SetPassword(self, password):
        time.sleep(1)
        elementId = 'waiter_login_password'
        if self.common.CheckIfElementExists(elementId) is not ABSENT:
            self.logger.Log(elementId + "- Waiting to be clickable")
            WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.ID, elementId)))
            element = self.browser.find_element_by_id(elementId)
            time.sleep(1)
            element.find_element_by_tag_name("input").send_keys(password)
            time.sleep(1)
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
        time.sleep(1)

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

    def getAllTableNumbers(self):
        # task_assign_to_me
        tableNumbers_innerHtml = {}
        tableNumber = self.common.GetAllElementsWhichContains('taskTableNumber_')
        for table in tableNumber:
            id = table.get_attribute('id')
            taskCardId = id.replace("taskTableNumber", "taskCardDiv")
            tableNumbers_innerHtml[id] =  self.browser.find_element_by_id(taskCardId).get_attribute('innerHTML')

        return tableNumbers_innerHtml

    def checkIfTaskCardContains(self, taskCardId, dataToSearch):
        time.sleep(2)
        taskCard = self.common.getElementById(taskCardId)
        self.logger.Log('Found TaskCardId -> ' + taskCardId + '  ->Searching for #' + dataToSearch)
        innerHtml = taskCard.get_attribute('innerHTML')
        if dataToSearch in innerHtml:
            self.logger.Log('Found ' + dataToSearch)
            return True
        return False

    def checkAndClick(self, tableNumber, action, activity=""):
        """
              :param tableNumber: (ex) 11
              :param action: could be
              task_assign_to_me_  OR
              task_verified_      OR
              task_acknowledge_   OR
              task_done_
              """
        self.logger.Log('Checking and clicking table number -> ' + str(tableNumber) + " and action -> " + action)
        time.sleep(1)
        retry = 15
        while retry > 0:
            self.logger.Log('Try to Check and click ')
            # This method aim to get         ##action## type task from specified table
            taskCard = self._getTaskCardFromTable(tableNumber, activity)
            if taskCard is not None:
                buttonId = action + taskCard.replace('taskCardDiv_', '')
            if taskCard is not None and self.checkIfTaskCardContains(taskCard, buttonId):
                goToTableResult = self.checkIfTaskCardContains(taskCard, 'GO_TO_TABLE')
                self.logger.Log('Found ' + buttonId + ' => clicking on it')
                self.common.ClickOn(buttonId)
                self.logger.Log('Clicked ' + buttonId + ' => assigned')
                if goToTableResult is False:
                    return True
            self.logger.Log('Checking and clicking ' + str(16 - retry) + '/15')
            retry -= 1
            time.sleep(2)
        assert 'Action don\'t exist. Action searched for ' + action

    # search for specific tables
    def _getTaskCardFromTable(self, tableNumber, activity=""):
        time.sleep(1)
        # get all tasks to iterate through them
        tableNumbers = self.getAllTableNumbers()
        if tableNumbers is not None:
            self.logger.Log("availableTasks -> ")
            self.logger.Log(len(tableNumbers))
            # take action for every task type
            try:
                for key, value in tableNumbers.items():
                    tableId = key
                    self.logger.Log('Waiter TableID 1 ' + tableId)
                    id = tableId.replace('taskTableNumber_', '')
                    self.logger.Log('Waiter TableID 2 ' + tableId)
                    innerHtml = value
                    self.logger.Log('Waiter TableID 3 ' + tableId)
                    self.logger.Log(innerHtml)

                    if str(tableNumber) in innerHtml and activity in innerHtml:
                        self.logger.Log('Found task for table' + str(tableNumber) + ' # Task -> ' + id)
                        return 'taskCardDiv_' + id
            except ValueError:
                self.logger.Log('----===----[Exception] ' + ValueError.message)
                return None
        else:
            self.logger.Log('AvailableTasks is None  {_getTaskCardFromTable}')
        return None

    def _clickOnTaskForATable(self, taskType, taskCardNumber):
        """
            :param taskType: could be
            task_assign_to_me_  OR
            task_verified_      OR
            task_acknowledge_   OR
            task_done_
            """
        # Checking if the task wanted to be clicked is associated with a specific table number
        time.sleep(3)
        taskCard = self.common.getElementById(taskCardNumber)
        self.logger.Log(taskCard.get_attribute('id'))
        id = taskCard.get_attribute('id').replace('taskCardDiv_', '')
        fullTaskId = 'task_' + taskType + '_' + id
        if fullTaskId in taskCard.get_attribute('innerHTML'):
            self.logger.Log('Found ' + fullTaskId)
            self.common.ClickOn(fullTaskId)

    def _clickOnTask(self, taskType):
        """
        :param taskType: could be
        task_assign_to_me_  OR
        task_verified_      OR
        task_acknowledge_   OR
        task_done_
        """
        time.sleep(3)
        # get all tasks to iterate through them
        availableTasks = self.getAllTasks()
        if availableTasks is not None:
            self.logger.Log("availableTasks -> ")
            self.logger.Log(len(availableTasks))
            # take action for every task type
            for taskCard in availableTasks:
                self.logger.Log(taskCard.get_attribute('id'))
                id = taskCard.get_attribute('id').replace('taskCardDiv_', '')
                fullTaskId = 'task_' + taskType + '_' + id
                if fullTaskId in taskCard.get_attribute('innerHTML'):
                    self.logger.Log('Found ' + fullTaskId)
                    self.common.ClickOn(fullTaskId)
        else:
            self.logger.Log('AvailableTasks is None')

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
