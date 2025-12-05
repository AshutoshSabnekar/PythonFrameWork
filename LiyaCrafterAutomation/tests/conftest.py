from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from utilities.excelReader import ExcelUtils
import pytest
import os
from datetime import datetime
from pytest_html import extras


#def pytest_generate_tests(metafunc):
#    if "test_data" in metafunc.fixture names:
#        data = read_test_data("testdata/InsurancePrompts.xlsx", "Sheet1")
#        metafunc.parametrize("test_data", data)


# @pytest.fixture(scope="module", params=read_test_data_from_excel("testdata/InsurancePrompts.xlsx", "Sheet1"))
# def test_data(request):
#     return request.param

TESTDATA_DIR = "TestData"

def get_excel_path_for_module(module_name):
    for file in os.listdir(TESTDATA_DIR):
        if file.endswith(".xlsx") and module_name.lower() in file.lower():
            return os.path.join(TESTDATA_DIR, file)
    return None

def pytest_generate_tests(metafunc):
    if "data_row" in metafunc.fixturenames:
        module_name = metafunc.module.__name__.split('.')[-1].replace("test_", "")
        excel_path = get_excel_path_for_module(module_name)

        if not excel_path:
            pytest.skip(f"No matching Excel data found for {module_name}")

        excel = ExcelUtils(excel_path)
        data = excel.get_test_data()
        metafunc.parametrize("data_row", data, ids=[d["TC_Name"] for d in data])

# Set dynamic HTML report path
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not os.path.exists('reports'):
        os.makedirs('reports')
    if not os.path.exists('assets'):
        os.makedirs('assets')


    report_name = f"Automation_Report_{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}.html"
    config.option.htmlpath = os.path.join('reports', report_name)

    # Add custom CSS to the report
    # config.option.css = custom_css

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


@pytest.fixture(scope="function", autouse=True)  # Runs automatically after every test
def check_soft_assertions(request):
    """
    This fixture runs after every test function.
    It checks if the test instance has a TestStatus object with any verification failures.
    If failures are found, it forces the test to fail.
    """
    yield  # Let the test run first

    # 1. Get the test instance
    test_instance = getattr(request.node, "instance", None)

    # 2. Check if this instance has a 'test_status' attribute with 'resultList'
    if test_instance and hasattr(test_instance, 'test_status'):
        test_status_obj = test_instance.test_status
        test_name = request.node.name

        if hasattr(test_status_obj, 'resultList') and "FAIL" in test_status_obj.resultList:
            test_status_obj.log.error(f"'{test_name}' ### TEST FAILED due to failed verification(s).")
            test_status_obj.resultList.clear()
            assert False, f"Test failed due to verification errors. Check logs for details."
        else:
            test_status_obj.log.info(f"'{test_name}' ### TEST SUCCESSFUL.")
            if hasattr(test_status_obj, 'resultList'):
                test_status_obj.resultList.clear()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        test_instance = getattr(item, "instance", None)
        if test_instance and hasattr(test_instance, "driver"):
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)

            test_instance.driver.save_screenshot(screenshot_path)

            # Relative path for HTML
            rel_path = os.path.relpath(screenshot_path, start=os.getcwd())

            # Embed thumbnail image (clickable for full size)
            html_img = (
                f'<a href="{rel_path}" target="_blank">'
                f'<img src="{rel_path}" style="width:250px;height:auto;border:1px solid #ccc;"/>'
                f'</a>'
            )

            if hasattr(report, "extra"):
                report.extra.append(extras.html(html_img))
            else:
                report.extra = [extras.html(html_img)]

            print(f" Embedded screenshot in report: {rel_path}")