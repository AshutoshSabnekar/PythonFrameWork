import pytest
from page.HomePage import HomePage
from page.ConnectorsPage import ConnectorsPage
from page.InsightsPage import InsightsPage
from utilities.ConfigReader import get_config_value
from utilities.TestStatus import TestStatus
import unittest
from tests.conftest import *

@pytest.mark.usefixtures("oneTimeSetUp")
class InsightsPageTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetUp(self):
        self.Hp = HomePage(self.driver)
        self.Cp = ConnectorsPage(self.driver)
        self.Ts = TestStatus(self.driver)
        self.Ip = InsightsPage(self.driver)

    # def test_navigateToInsightsPage(self):
    #       self.Hp.verifyNavigatedToPage("Insights")

    def test_verifyInsurancePrompts(self):
        # Read test data inside the method
        test_data_list = read_test_data("testdata/InsurancePrompts.xlsx")
        test_data = test_data_list[0]  # Use first row

        print("Test Data:", test_data)
        self.Ip.verifyPrompts(test_data)  # Pass the row to your page method

    def test_verifyPrompts(self):
        test_data_list = read_test_data("testdata/InsurancePrompts.xlsx")
        test_data = test_data_list[1]  # Use second row

        print("Test Data for Prompts:", test_data)
        self.Ip.verifyPrompts(test_data)

    def test_verifyInsurancePrompts2(self):
        print("Insurance file path:", get_config_value("Paths", "insurance_data_file"))
        print("Insurance sheet:", get_config_value("Sheets", "insurance_sheet"))
        file_path = get_config_value("Paths", "insurance_data_file")
        sheet_name = get_config_value("Sheets", "insurance_sheet")
        test_data_list = read_test_data(file_path, sheet_name)

        for idx, test_data in enumerate(test_data_list):
            with self.subTest(f"InsurancePrompt_Row_{idx + 1}"):
                self.Ip.verifyPrompts(test_data)
