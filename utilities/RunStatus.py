import utilities.Customlogger as cl
import logging
from base.SeleniumDriver import SeleniumDriver
from traceback import print_stack

class RunStatus(SeleniumDriver):

    log = cl.customLogger(logging.WARNING)

    def __init__(self, driver):
        super(RunStatus, self).__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage):
        try:
            if result is not None:
                if result:
                    self.resultList.append("PASS")

                else:
                    self.resultList.append("FAIL")
                    self.screenShot()
            else:
                self.resultList.append("FAIL")
                self.screenShot()
        except:
            self.resultList.append("FAIL")
            self.log.error("### Exception Occurred !!!")
            self.screenShot()
            print_stack()

    def mark(self, result, resultMessage):
        """
        Mark the result of the verification point in a test case
        """
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        """
        Mark the final result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be final test status of the test case
        """
        self.setResult(result, resultMessage)

        if "FAIL" in self.resultList:
            self.resultList.clear()
            assert True == False
        else:
            self.resultList.clear()
            assert True == True