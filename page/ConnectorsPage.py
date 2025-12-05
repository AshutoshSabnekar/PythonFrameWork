import utilities.Customlogger as cL
import logging
from base.basePage import BasePage
from utilities.RunStatus import RunStatus

class ConnectorsPage(BasePage):
    log = cL.customLogger(logging.DEBUG)

    def __init__(self, driver, test_status=None):
        super().__init__(driver)
        self.driver = driver
        self.test_status = test_status or RunStatus(self.driver)

    #Locators
    _btn_connectors = "//button//span[text()='Connect']"

    # Verify the Connections Page title for LIYA Crafter
    # Params : pageTitle
    def validConnectorsPageTitle(self, pageTitle):
        self.pageRefresh()
        self.verifyPageTitle(pageTitle)
        self.screenShot()

    # Verify the presence of Connect button in the page
    # Params :
    def verifyConnectButtonPresent(self):
        if self.isElementPresent(self._btn_connectors,"XPATH"):
            self.log.info("Verified the presence of Connect button")
            return True
        else:
            self.log.info("Connect button is not found")
            return False





