import pytest
from page.HomePage import HomePage
from page.ConnectorsPage import ConnectorsPage
import unittest

##
# "
## command to run chrome in debug mode
@pytest.mark.usefixtures("oneTimeSetUp")
class HomePageDirectLaunch(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetUp(self):
        self.Hp = HomePage(self.driver)
        self.Cp = ConnectorsPage(self.driver)

    def test_navigateToHomePage(self):
        self.Hp.validHomePageTitle("Home")
        self.Hp.verifyMenuBarCollapsed()
        self.Hp.verifyWelcomeCardText()
        self.Hp.verifyWidgetCardsCount(2)

    def test_verifyMenuButtonExpandsOnClick(self):
        self.Hp.verifyTheMenuButtonExpandsOnClick()

    def test_verifyMenuBarItems(self):
        self.Hp.verifyMenuBarItems()

    def test_verifyNavigateToConnectionsPage(self):
        self.Hp.verifyNavigatedToPage("Connectors")

    def test_verifyNavigateToInsightsPage(self):
        self.Hp.verifyNavigatedToPage("Insights")

    def test_verifyNavigateToConsolidatedInsightsPage(self):
        self.Hp.verifyNavigatedToPage("Consolidated Insights")

    def test_verifyNavigateToUserManagementPage(self):
        self.Hp.verifyNavigatedToPage("User Management")

    def test_verifyNavigateToDashboardsPage(self):
        self.Hp.verifyNavigatedToPage("Dashboard")





