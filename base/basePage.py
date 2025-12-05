from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from base.SeleniumDriver import SeleniumDriver
from traceback import print_stack
from utilities.ConfigReader import get_config_value
from utilities.excelReader import ExcelUtils
from utilities.utilities import Util
from selenium.webdriver.support import expected_conditions as EC


class BasePage(SeleniumDriver):

    def __init__(self, driver):
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    #Verify Page Title
    #Params: String
    def verifyPageTitle(self, titleToVerify):
        if titleToVerify.lower() == "insights":
            titleToVerify = "analyze"

        if titleToVerify.lower() == "consolidated insights":
            titleToVerify = "insight"

        try:
            self.log.info("Actual Page Title From Application Web UI --> :: " + self.driver.current_url)
            self.log.info("Expected Page Title From Application Web UI --> :: " + titleToVerify)
          ##  self.log.info("Page URL is:"+ self.driver.current_url)

            if titleToVerify.lower() in self.driver.current_url.lower():
                self.log.info("Page Title Verified Successfully as "+titleToVerify+" page")
                return True
            else:
                self.log.warning("Expected Title: "+titleToVerify.lower()+" and Actual Page Title :"+self.getTitle().lower()+" do not match")
                return False
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False

    def getTestDataList(self, file_config, sheet_config):
        file_path = get_config_value("Paths", file_config)
        sheet_name = get_config_value("Sheets", sheet_config)
        return ExcelUtils.read_test_data(file_path, sheet_name)

    def clickOnLabel(self, xpath):
        try:
            self.log.info(f"Clicking on prompt label: XPath='{xpath}'")
            self.getElement(xpath, "XPATH").click()
            return True
        except Exception as e:
            self.log.error(f"Failed to click on prompt label. Error: {e}")
            return False

    def clickOnDropdown(self, xpath):
        self.log.info(f"Waiting for dropdown arrow to become visible: XPath='{xpath}'")
      #  self.waitForElementToBeInteractable(xpath, "XPATH")  # Wait for interactability
        element = self.getElement(xpath, "XPATH")  # Re-fetch the element
        try:
            self.log.info("Clicking on dropdown arrow")
            element.click()
            return element
        except Exception as e:
            self.log.error(f"Failed to click dropdown arrow. Error: {e}")
            return None

    def selectDropdownOption(self, options_xpath, target_text):
        self.log.info("Fetching dropdown options")
        self.staticWait(3)
        options = self.getElements(options_xpath, "XPATH")
        for option in options:
            text = option.text.strip()
            self.log.debug(f"Found option: '{text}'")
            if text == target_text:
                self.log.info(f"Selecting matching option: '{text}'")
                try:
                    self.driver.execute_script("arguments[0].click();", option)
                    return True
                except Exception as e:
                    self.log.error(f"Failed to click on option '{text}'. Error: {e}")
                    return False
        return False

    #Switch driver context to iframe whose 'src' attribute contains the partial_src substring.
    def switch_to_iframe_by_partial_src(self):
        partial_src = "https://embedded.powerbi.com/ReportEmbed?uid="
        try:
            iframe_element = self.getElement(f"//iframe[contains(@src, '{partial_src}')]", "XPATH")
            self.driver.switch_to.frame(iframe_element)
            self.log.info(f"Switched to iframe with src containing '{partial_src}'")
            return True
        except NoSuchElementException:
            self.log.error(f"No iframe found with src containing '{partial_src}'")
            return False

