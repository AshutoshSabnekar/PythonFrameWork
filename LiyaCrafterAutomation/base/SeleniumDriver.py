import os
import time
from selenium.common.exceptions import TimeoutException
from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import utilities.Customlogger as cL
import logging
import traceback
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
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
        except NoSuchElementException:
            self.log.info("Element not found with locator: " + locator + " locatorType: " + locatorType)
        return elements

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
        except Exception as e:
            self.log.info(
                f"Cannot click on the element with locator: {locator}, locatorType: {locatorType}. Error: {e}")

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
        except Exception:
            self.log.error("Exception occurred when taking screenshot", exc_info=True)

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
        self.log.info("Getting page title")
        return self.driver.title

    def pageRefresh(self):
        self.log.info("Refreshing the current web page")
        return self.driver.refresh()

    def waitTillElementClickable(self, xpath, timeout=30):
        self.log.info(f"Waiting for element to be clickable: XPath='{xpath}', Timeout={timeout} seconds")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.log.info(f"Element is clickable: XPath='{xpath}'")

            self.log.debug("Scrolling element into view")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # Let any animations or overlays settle

            try:
                self.log.info("Attempting to click element using standard click")
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element.click()
                self.log.info("Element clicked successfully using standard click")
            except Exception as e:
                self.log.warning(f"Standard click failed. Trying JavaScript click. Error: {e}")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    self.log.info("Element clicked successfully using JavaScript")
                except Exception as js_error:
                    self.log.error(f"JavaScript click also failed for XPath='{xpath}'. Error: {js_error}")

        except Exception as e:
            self.log.error(f"Element not clickable or not found: XPath='{xpath}' | Error: {e}")

    #Waits for element to be clickable and clicks using ActionChains
    def waitTillElementClickableActions(self, xpath, timeout=10):
        self.log.info(f"Waiting for element to be clickable: XPath='{xpath}', Timeout={timeout} seconds")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.log.info(f"Element located in DOM: XPath='{xpath}'")

            self.log.debug("Scrolling element into view")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # Let animations or overlays settle

            try:
                self.log.info("Waiting for element to be interactable (clickable)")
                wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

                self.log.info("Attempting to click element using ActionChains")
                actions = ActionChains(self.driver)
                self.isElementPresent(xpath, "XPATH")  # Optional: log inside this method too
                actions.move_to_element_with_offset(element, 10, 0).click().perform()
                self.log.info("Element clicked successfully using ActionChains")

            except Exception as e:
                self.log.warning(f"ActionChains click failed. Falling back to JavaScript click. Error: {e}")
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    self.log.info("Element clicked successfully using JavaScript")
                except Exception as js_error:
                    self.log.error(f"JavaScript click also failed for XPath='{xpath}'. Error: {js_error}")

        except Exception as e:
            self.log.error(f"Element not clickable or not found: XPath='{xpath}' | Error: {e}")


    #Highlights a Selenium WebDriver element with a border only.
    def highlightElement(self, xpath, effect_time=2, border="2px solid red"):
        self.log.info(
            f"Attempting to highlight element: XPath='{xpath}' with border='{border}' for {effect_time} seconds")
        try:
            element = self.getElement(xpath, "XPATH")
            original_style = element.get_attribute('style')
            self.log.debug(f"Original style of element: '{original_style}'")

            self.log.info("Applying highlight style to element")
            self.driver.execute_script(
                f"arguments[0].setAttribute('style', arguments[0].getAttribute('style') + '; border: {border};')",
                element
            )

            self.log.debug("Pausing to keep highlight visible")
            time.sleep(effect_time)

            self.log.info("Reverting element to original style")
            self.driver.execute_script(
                f"arguments[0].setAttribute('style', '{original_style}')",
                element
            )
        except Exception as e:
            self.log.error(f"Failed to highlight element: XPath='{xpath}' | Error: {e}")

    # waits for element to be visible waits till timeout given. default is 10 seconds
    def waitForElementVisible(self, xpath, timeout=10):
        self.log.info(f"Waiting for element to be visible: XPath='{xpath}', Timeout={timeout} seconds")
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.log.info(f"Element became visible: XPath='{xpath}'")

            self.log.debug(f"Scrolling element into view: XPath='{xpath}'")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            self.log.debug("Pausing briefly to allow animations or overlays to settle")
            time.sleep(0.5)

            return element
        except Exception as e:
            self.log.error(f"Element not visible or not found: XPath='{xpath}' | Error: {e}")
            return None

    # Wait for an element to be visible and interactable. This helps when there we need to wait for element to interact with it
    def waitForElementToBeInteractable(self, xpath, timeout=30):
        self.log.info(f"Waiting for element to be interactable: XPath='{xpath}'")

        try:
            wait = WebDriverWait(self.driver, timeout)

            # Step 1: Wait for visibility and clickability
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # Let overlays/animations settle

            # Step 2: Ensure it's not covered by another element
            if self.isElementObstructed(element):
                self.log.warning(f"Element is visible but obstructed: XPath='{xpath}'")
                return None

            self.log.info(f"Element is interactable: XPath='{xpath}'")
            return element

        except TimeoutException:
            self.log.error(f"Timeout: Element not interactable within {timeout} seconds: XPath='{xpath}'")
            return None
        except Exception as e:
            self.log.error(f"Error while waiting for interactable element: XPath='{xpath}' | Error: {e}")
            return None

    # To check if an element is obstructed by another overlay element preventing it to be clicked
    def isElementObstructed(self, element):
        try:
            # Get element's center point
            location = element.location_once_scrolled_into_view
            size = element.size
            center_x = location['x'] + size['width'] / 2
            center_y = location['y'] + size['height'] / 2

            # Get topmost element at that point
            top_element = self.driver.execute_script(
                "return document.elementFromPoint(arguments[0], arguments[1]);",
                center_x, center_y
            )

            return top_element != element
        except Exception as e:
            self.log.warning(f"Could not determine if element is obstructed. Error: {e}")
            return False

    #Static wait for given seconds. Used a Front End object are not loading even after they are interactable.
    def staticWait(self, seconds, reason=""):
        if reason:
            self.log.info(f"Static wait for {seconds} seconds: {reason}")
        else:
            self.log.info(f"Static wait for {seconds} seconds")
        time.sleep(seconds)
