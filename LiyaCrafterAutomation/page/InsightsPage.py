import utilities.Customlogger as cL
import logging
from base.basePage import BasePage
import pytest

class InsightsPage(BasePage):
    log = cL.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #Locators
    _drpDownPromptSelectConnection = "//mat-select[@id='select_connection']"
    _drpDownPromptSelectConnectionOption = "//mat-option/span"
    _drpDownPromptSelectConnectionArrow = "//div[@class='mat-mdc-select-arrow']"
    _dropdownvalues = "//div[@role='listbox']/mat-option"
    _lbl_Prompt = "//span[text()='Prompt']"
    _txtboxPromptInput = "//textarea[@placeholder='Enter prompt here']"
    _lbl_Semantics = "//span[text()='Semantic Views']"
    _btn_submitPrompt = "//button[@mattooltip='Submit Prompt']"
    _btn_clearPromptSearch = "//button[@mattooltip='Clear Search']"
    _btn_deletePromptSearch = "//button[@mattooltip='Delete']"
    _InsightsContainer = "//div[@data-testid='display-area']"
    _dropDownSemanticViews = "//mat-select[@id='select_data_products']//div[@class='mat-mdc-select-arrow']"

    #
    def verifyAllInsurancePrompts(self, test_data):
        self.verifyPrompts(test_data)
        self.enterPromptInput(test_data)

    #Verfiy the Prompts is generated when user enter a prompt value and click on submit button
    # Verify the Prompts are generated when user enters a prompt value and clicks the submit button
    def verifyPrompts(self, test_data):
        self.log.info(f"Starting prompt verification for test case: {test_data['TestCaseName']}")
        self.log.info(f"Expected connection name: {test_data['ConnectionName']}")
        self.staticWait(5)
        if not self.clickOnLabel(self._lbl_Prompt):
            return

        dropdown_element = self.clickOnDropdown(self._drpDownPromptSelectConnectionArrow)
        if not dropdown_element:
            return

        if not self.selectDropdownOption(self._drpDownPromptSelectConnectionOption, test_data["ConnectionName"]):
            self.log.warning(f"Connection option '{test_data['ConnectionName']}' not found in dropdown.")

    #To enter prompt from the testdata sheet
    def enterPromptInput(self, test_data):
        self.log.info(f"Entering prompt input for test case: {test_data['TestCaseName']}")
        prompt_input_element = self.getElement(self._txtboxPromptInput, "XPATH")
        prompt_input_element.clear()
        prompt_input_element.send_keys(test_data.get("Prompt1", ""))
        self.log.info(f"Entered prompt input: {test_data.get('Prompt1', '')}")
        self.clickToSubmitPrompt()
        self.verifyInsightsDisplayed(test_data)
        self.clickOnDeletePromptSearch()

    # To click on submit prompt button
    def clickToSubmitPrompt(self, timeout=15):
        self.log.info("Clicking to submit the prompt")
        try:
            # Wait until the element is clickable
            self.waitForElementToBeInteractable(self._btn_submitPrompt, timeout)
            self.elementClick(self._btn_submitPrompt,"XPATH")
            self.log.info("Prompt submitted successfully")
        except Exception as e:
            self.log.warning(f"Normal click failed: {e}")
            # Fallback to JavaScript click
            try:
                submit_button = self.getElement(self._btn_submitPrompt,"XPATH")
                self.driver.execute_script("arguments[0].click();", submit_button)
                self.log.info("Prompt submitted successfully via JS click")
            except Exception as js_e:
                self.log.error(f"Failed to click submit button: {js_e}")

    # To click on clear prompt search button
    def clickOnClearPromptSearch(self):
        self.log.info("Clicking to clear the prompt search")
        if self.elementClick(self._btn_clearPromptSearch, "XPATH"):
            self.log.info("Prompt search cleared successfully")
        else:
            self.log.error("Failed to clear the prompt search")

    # To click on clear prompt search button
    def clickOnDeletePromptSearch(self, timeout=15):
        self.log.info("Clicking to delete the prompt search")
        try:
            self.waitTillElementClickable(self._btn_deletePromptSearch, timeout)
            self.elementClick(self._btn_deletePromptSearch,"XPATH")
            self.log.info("Prompt search deleted successfully")
        except Exception as e:
            self.log.warning(f"Normal click failed: {e}")
            # Fallback to JavaScript click
            try:
                delete_button = self.getElements(self._btn_deletePromptSearch, "XPATH")  # Get the last delete button
                self.driver.execute_script("arguments[0].click();", delete_button)
                self.log.info("Prompt search deleted successfully via JS click")
            except Exception as js_e:
                self.log.error(f"Failed to delete the prompt search: {js_e}")


    #verify Semantic Views
    def verifyAllInsuranceSemantics(self, test_data_list, test_case):
        for idx, test_data in enumerate(test_data_list):
            with test_case.subTest(f"InsuranceSemantic_Row_{idx + 1}"):
                self.verifySemantics(test_data)
                self.clickToSubmitPrompt()

    #Verfiy the Semantic Views is generated when user select a connection name and semantic from the dropdown
    def verifySemantics(self, test_data):
        self.log.info(f"Starting semantic verification for test case: {test_data['TestCaseName']}")
        self.log.info(f"Expected connection name: {test_data['ConnectionName']}")
        self.staticWait(5)
        if not self.clickOnLabel(self._lbl_Semantics):
            return

        dropdown_element = self.clickOnDropdown(self._drpDownPromptSelectConnectionArrow)
        if not dropdown_element:
            return

        if not self.selectDropdownOption(self._drpDownPromptSelectConnectionOption, test_data["ConnectionName"]):
            self.log.warning(f"Connection option '{test_data['ConnectionName']}' not found in dropdown.")

        if not self.waitForElementVisible(self._drpDownPromptSelectConnectionOption, 20):
            if not self.selectDropdownOption(self._dropDownSemanticViews, test_data["Semantic Views"]):
                self.log.warning(f"Semantic option '{test_data['Semantic Views']}' not found in dropdown.")

    def verifyInsightsDisplayed(self, test_data):
        self.staticWait(20,"Awaiting insights to be displayed.")
        self.switch_to_iframe_by_partial_src()
        if not self.waitForElementVisible(self._InsightsContainer,10):
            self.log.warning(f"Insights for '{test_data['Prompt1']}' not displayed.")
        self.screenShot()
        self.driver.switch_to.default_content()

