"""
Driver Factory for LIYA Crafter Automation
Handles browser initialization and configuration
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
import utilities.Customlogger as cl


class DriverFactory:
    """
    Factory class to create and configure WebDriver instances
    """

    log = cl.customLogger(logging.INFO)

    def __init__(self):
        self.driver = None

    def get_driver(self, browser_name="chrome", mode="normal", debug_port=None):
        """
        Create and return WebDriver instance

        Args:
            browser_name (str): Browser to use - chrome, firefox, edge
            mode (str): Execution mode - normal, headless, debug
            debug_port (int): Port for debug mode (default: 8989)

        Returns:
            WebDriver: Configured browser driver instance
        """
        browser_name = browser_name.lower()

        try:
            if browser_name == "chrome":
                self.driver = self._get_chrome_driver(mode, debug_port)
            elif browser_name == "firefox":
                self.driver = self._get_firefox_driver(mode)
            elif browser_name == "edge":
                self.driver = self._get_edge_driver(mode)
            else:
                raise ValueError(f"Unsupported browser: {browser_name}")

            # Common driver configuration
            self._configure_driver()
            self.log.info(f"Successfully initialized {browser_name} driver in {mode} mode")
            return self.driver

        except Exception as e:
            self.log.error(f"Error creating {browser_name} driver: {str(e)}")
            raise

    def _get_chrome_driver(self, mode, debug_port):
        """Configure and return Chrome driver"""
        options = ChromeOptions()

        if mode == "debug":
            # Connect to existing Chrome instance
            port = debug_port if debug_port else 8989
            options.add_experimental_option("debuggerAddress", f"localhost:{port}")
            self.log.info(f"Connecting to Chrome debug session on port {port}")
            service = ChromeService(ChromeDriverManager().install())

        elif mode == "headless":
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            service = ChromeService(ChromeDriverManager().install())

        else:  # normal mode
            options.add_experimental_option("detach", True)
            options.add_argument("--start-maximized")
            service = ChromeService(ChromeDriverManager().install())

        # Common Chrome options (removed excludeSwitches for compatibility)
        options.add_argument("--disable-blink-features=AutomationControlled")

        return webdriver.Chrome(service=service, options=options)

    def _get_firefox_driver(self, mode):
        """Configure and return Firefox driver"""
        options = FirefoxOptions()

        if mode == "headless":
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def _get_edge_driver(self, mode):
        """Configure and return Edge driver"""
        options = EdgeOptions()

        if mode == "headless":
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        options.add_argument("--start-maximized")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    def _configure_driver(self):
        """Apply common configuration to driver"""
        if self.driver:
            try:
                # Only maximize if not already maximized (avoid error in debug mode)
                if self.driver.get_window_size()['width'] < 1920:
                    self.driver.maximize_window()
            except Exception as e:
                self.log.warning(f"Could not maximize window: {str(e)}")

            self.driver.implicitly_wait(3)

    def quit_driver(self):
        """Safely quit the driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.log.info("Driver closed successfully")
            except Exception as e:
                self.log.error(f"Error closing driver: {str(e)}")