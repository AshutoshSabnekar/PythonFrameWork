import pytest
from page.HomePage import HomePage
from page.ConnectorsPage import ConnectorsPage
from utilities.TestStatus import TestStatus
import unittest

## py.test -s -v tests/ConnectorsPageTests.py
## chrome.exe --remote-debugging-port=8989 --user-data-dir="C:\Initiatives\PythonProjects\chromeProfile"
## command to run chrome in debug mode
@pytest.mark.usefixtures("oneTimeSetUp")
class ConnectorsPageTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetUp(self):
        self.Hp = HomePage(self.driver)
        self.Cp = ConnectorsPage(self.driver)
        self.Ts = TestStatus(self.driver)


    def test_navigateToConnectorsPage(self):
        self.Hp.verifyNavigatedToPage("Connectors")

    def test_verifyConnectorButtonSeen(self):
        self.Cp.verifyConnectButtonPresent()

