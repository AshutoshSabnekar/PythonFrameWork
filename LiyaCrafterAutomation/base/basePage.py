from base.SeleniumDriver import SeleniumDriver
from traceback import print_stack
from utilities.utilities import Util

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
