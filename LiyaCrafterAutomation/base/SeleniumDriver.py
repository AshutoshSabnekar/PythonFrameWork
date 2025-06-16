import logging
import os
import time
from traceback import print_stack

from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import utilities.Customlogger as cL
import logging

class SeleniumDriver:

    log = cL.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    # Get ByType for different element locators
    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktext":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    # Get Element Generic method
    #Params: locator and locator type
    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
        except NoSuchElementException:
            self.log.info("Element not found with locator: " + locator + " locatorType: " + locatorType)
        return element

    # Get Elements Generic method
    # Params: locator and locator type
    def getElements(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator)
        except NoSuchElementException:
            self.log.info("Element not found with locator: " + locator + " locatorType: " + locatorType)
        return element

    #Get Elements Count Generic Method
    def getElementsLength(self,locator, locatorType="id"):
        elementsList = self.getElements(locator, locatorType)
        return len(elementsList)

    # Verify if element is present
    def isElementPresent(self, locator,locatorType):
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            if element is not None:
                return True
            else:
                return False
        except NoSuchElementException:
            self.log.info("Element not present with locator: " + locator + " locatorType: " + locatorType)
            return False


    #Click on an Element
    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
        #    self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)

    # Check for Presence of an Element
    def elementPresenceCheck(self, locator, locatorType):
        try:
            elementList = self.driver.find_elements(locatorType, locator)
            if len(elementList) > 0:
                return True
            else:
                return False
        except NoSuchElementException:
            self.log.info("Element not found with locator:"+locator+" and locator type:"+locatorType)
            return False


    #Takes screenshot of the current open web page
    #param: driver
    #return:
    def screenShot(self):
        fileName = "Screenshot_" + datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3] + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
         #   self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()

    #Wait For Element to be present
    #Params: locator and locator type
    def waitForElement(self, locator, locatorType="id",
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
        #    self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be visible")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
         #   self.log.info("Element appeared on the web page with locator:"+locator+" and locator type:"+locatorType)
        except ElementNotVisibleException:
            self.log.info("Waited for maximum :: " + str(timeout) + " :: seconds for element to be visible")
            self.log.info("Element not appeared on the web page with locator:"+locator+" and locator type:"+locatorType)
        self.driver.implicitly_wait(2)
        return element

    def getTitle(self):
        return self.driver.title

    def pageRefresh(self):
        return self.driver.refresh()
