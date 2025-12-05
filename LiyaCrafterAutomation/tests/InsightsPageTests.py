import pytest
from page.HomePage import HomePage
from page.ConnectorsPage import ConnectorsPage
from page.InsightsPage import InsightsPage
from utilities.ConfigReader import get_config_value
from utilities.RunStatus import RunStatus
import unittest
from utilities.excelReader import ExcelUtils
from tests.conftest import *
from base.basePage import BasePage
from utilities.DataProvider import DataProvider

data_provider = DataProvider()

# Load data once for pytest parametrize before test class definition
insurance_prompt_data = data_provider.getTestDataList('insurance_data_file', 'sheet1')
insurance_semantic_data = data_provider.getTestDataList('insurance_data_file', 'sheet2')

@pytest.mark.usefixtures("oneTimeSetUp")
class InsightsPageTests(unittest.TestCase, BasePage):

    @pytest.fixture(autouse=True)
    def classSetUp(self):
        self.Hp = HomePage(self.driver)
        self.Cp = ConnectorsPage(self.driver)
        self.Ts = RunStatus(self.driver)
        self.Ip = InsightsPage(self.driver)

    def test_navigateToInsightsPage(self):
        self.Hp.verifyNavigatedToPage("Insights")

    @pytest.mark.parametrize("test_data", insurance_prompt_data)
    def test_verifyInsurancePrompts(self, test_data):
        self.Hp.verifyNavigatedToPage("Home")
        self.Hp.verifyNavigatedToPage("Insights")

        self.Ip.verifyAllInsurancePrompts([test_data] )

    # @pytest.mark.parametrize("test_data", [insurance_semantic_data])
    # def test_verifySemanticViews(self,test_data):
    #     self.Hp.verifyNavigatedToPage("Home")
    #     self.Hp.verifyNavigatedToPage("Insights")
    #
    #     # Get the data list from the excelsheet
    #     test_data_list = self.getTestDataList("insurance_data_file", "sheet2")
    #
    #     # Get all prompt results
    #     self.Ip.verifyAllInsuranceSemantics(test_data_list, self)