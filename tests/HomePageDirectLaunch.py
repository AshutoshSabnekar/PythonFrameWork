import pytest
from behave import fixture
from page.HomePage import HomePage
from page.ConnectorsPage import ConnectorsPage
import unittest
from utilities.excelReader import ExcelUtils
from utilities.RunStatus import RunStatus


##
##
@pytest.mark.usefixtures("oneTimeSetUp")
class HomePageDirectLaunch(unittest.TestCase):


    @pytest.fixture(scope="module")
    def excel(self):
        return ExcelUtils("TestData/login_data.xlsx")

    @pytest.fixture(autouse=True)
    def classSetUp(self):
        self.test_status = RunStatus(self.driver)
        self.Hp = HomePage(self.driver, self.test_status)
        self.Cp = ConnectorsPage(self.driver, self.test_status)

    def test_navigateToHomePage(self):
        self.Hp.verifyNavigatedToPage("Home")
        self.Hp.validHomePageTitle("Home")
        self.Hp.verifyMenuBarCollapsed()
        self.Hp.verifyWelcomeCardText()
        self.Hp.verifyWidgetCardsCount(3)
        self.test_status.markFinal("test_navigateToHomePage", True, "Navigated to Home Page and verified all elements.")    

    def test_verifyMenuButtonExpandsOnClick(self):
        self.Hp.verifyTheMenuButtonExpandsOnClick()
        self.test_status.markFinal("test_verifyMenuButtonExpandsOnClick", True, "Verified Menu button expands on click.")

    def test_verifyMenuBarItems(self):
        self.Hp.verifyMenuBarItems()
        self.test_status.markFinal("test_verifyMenuBarItems", True, "Verified Menu bar items present.")

    def test_verifyNavigateToConnectionsPage(self):
        self.Hp.verifyNavigatedToPage("Connectors")
        self.test_status.markFinal("test_verifyNavigateToConnectionsPage", True, "Navigated to Connectors Page.")

    def test_verifyNavigateToInsightsPage(self):
        self.Hp.verifyNavigatedToPage("Insights")
        self.test_status.markFinal("test_verifyNavigateToInsightsPage", True, "Navigated to Insights Page.")

    def test_verifyNavigateToConsolidatedInsightsPage(self):
        self.Hp.verifyNavigatedToPage("Consolidated Insights")
        self.test_status.markFinal("test_verifyNavigateToConsolidatedInsightsPage", True, "Navigated to Consolidated Insights Page.")

    def test_verifyNavigateToUserManagementPage(self):
        self.Hp.verifyNavigatedToPage("User Management")
        self.test_status.markFinal("test_verifyNavigateToUserManagementPage", True, "Navigated to User Management Page.")

    def test_verifyNavigateToDashboardsPage(self):
        self.Hp.verifyNavigatedToPage("Dashboard")
        self.test_status.markFinal("test_verifyNavigateToDashboardsPage", True, "Navigated to Dashboards Page.")





