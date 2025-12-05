import time
import traceback
import random, string
import utilities.Customlogger as cl
import logging

class Util(object):

    log = cl.customLogger(logging.INFO)

    # Put the program to wait for the specified amount of time
    def sleep(self, sec, info=""):
        if info is not None:
            self.log.info("Wait :: '" + str(sec) + "' seconds for " + info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    # Get random string of characters
    def getAlphaNumeric(self, length, type='letters'):
        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    # get a random unique name
    def getUniqueName(self, charCount=10):
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, listSize=5, itemLength=None):
        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
        return nameList

    #Verify if the actual text contains expected text
    def verifyTextContains(self, actualText, expectedText):
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT CONTAINS !!!")
            return False

    #Verify if the expected matches with the actual text match
    def verifyTextMatch(self, actualText, expectedText):
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if actualText.lower() == expectedText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCHED !!!")
            return False

    #Verify two list matches
    def verifyListMatch(self, expectedList, actualList):
        return set(expectedList) == set(actualList)

    #Verify actual list contains elements of expected list
    def verifyListContains(self, expectedList, actualList):
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True