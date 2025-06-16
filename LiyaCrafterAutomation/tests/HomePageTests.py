from selenium import webdriver
from base.SeleniumDriver import SeleniumDriver
class HomePageTests:

    def test_LaunchPage(self):
        baseURL = "https://victorious-wave-01f48010f.5.azurestaticapps.net/home"
        # chrome_service = Service(executable_path="C:\\Initiatives\\PythonProjects\\drivers\\chromedriver.exe")
        # driver = webdriver.Chrome(service=chrome_service)
        # svc = webdriver.ChromeService(executable_path=binary_path)
        # chrome_options = Options()
        # chrome_options.add_experimental_option("detach",True)
        # chrome_options.add_experimental_option("debuggerAddress","localHost:8989")
        # driver = webdriver.Chrome(service=svc,options=chrome_options)
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.implicitly_wait(3)
        driver.get(baseURL)
        driver.implicitly_wait(10)
        sD = SeleniumDriver(driver)
        emailLogin = sD.getElement("//input[@type='email']","xpath")
        driver.implicitly_wait(5)
        sD.screenShot()
        emailLogin.send_keys("ashutosh.sabnekar@neudesic.com")
        sD.screenShot()
        driver.implicitly_wait(5)
        sD.screenShot()
      #  emailLogin.send_keys(Keys.ENTER)
        driver.implicitly_wait(5)
        passwordLogin = sD.getElement("//input[@type='password']","xpath")
        passwordLogin.send_keys("Winterishere@2024")
        signInButton = sD.getElement("//input[@type='submit']","xpath")
        signInButton.submit()
        driver.implicitly_wait(30)

runTests = HomePageTests()
runTests.test_LaunchPage()



