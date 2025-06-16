import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
from utilities.excelReader import read_test_data

def pytest_generate_tests(metafunc):
    if "test_data" in metafunc.fixturenames:
        data = read_test_data("testdata/InsurancePrompts.xlsx", "Sheet1")
        metafunc.parametrize("test_data", data)


# @pytest.fixture(scope="module", params=read_test_data_from_excel("testdata/InsurancePrompts.xlsx", "Sheet1"))
# def test_data(request):
#     return request.param


# Set dynamic HTML report path
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    report_name = f"Automation_Report_{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}.html"
    config.option.htmlpath = os.path.join('reports', report_name)


# Add custom metadata and remove unwanted keys
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    # Add project metadata
    metadata["Project"] = "LIYA Insight Crafter"
    metadata["Report Generated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Remove unwanted default metadata
    for key in ["JAVA_HOME", "Plugins", "Platform", "Packages"]:
        metadata.pop(key, None)


# Optional: Customize HTML report title
def pytest_html_report_title(report):
    report.title = "LIYA Automation Report"

# Selenium WebDriver setup
@pytest.fixture(scope="class", autouse=True)
def oneTimeSetUp(request):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localHost:8989")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    request.cls.driver = driver
    yield driver
    driver.quit()
