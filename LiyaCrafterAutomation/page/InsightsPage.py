import utilities.Customlogger as cL
import logging
from base.basePage import BasePage

class InsightsPage(BasePage):
    log = cL.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #Locators

    #Verfiy the Prompts is generated when user enter a prompt value and click on submit button
    def verifyPrompts(self,test_data):
        self.log.info("Verifying the Prompts Generation for "+test_data["TestCaseName"])
