import utilities.Customlogger as cL
import logging
from base.basePage import BasePage
from utilities.RunStatus import RunStatus

class HomePage(BasePage):
    log = cL.customLogger(logging.DEBUG)

    def __init__(self, driver, test_status=None):
        super().__init__(driver)
        self.driver = driver
        self.test_status = test_status or RunStatus(self.driver)


    #Locators
    _btn_menuBar = "//mat-drawer"
    _btn_menuBarCollapse = "//mat-drawer[contains(@class='sidenav-collapsed')]"
    _btn_menuBarExpanded = "//mat-drawer[contains(@class,'sidenav-expanded')]"
    _lbl_welcomeCard = "//mat-card[@class='mat-mdc-card mdc-card top-div']/div/div"
    _crd_widgetCards = "//div[contains(@class,'nav-cards')]/mat-card"
    _txt_expectedWelcomeCard = "Welcome to LIYA - Insight CrafterYour AI powered Reporting ToolExplore your data, find actionable insights, and report on business outcomes 10x faster than traditional methods."
    _txt_welcomeCard = ""
    _lbl_userNameHeader = "//span[@class='userNameheader']"
    _icon_menuBarCollapsed = "//mat-drawer[@ng-reflect-ng-class='sidenav-collapsed'] //mat-list/mat-list-item"
    _icon_menuBarItemsCollapsed = "//mat-drawer[@ng-reflect-ng-class='sidenav-collapsed']//mat-list/mat-list-item/span/a"
    _icon_menuBarLinksExpanded = "//mat-drawer[@ng-reflect-ng-class='sidenav-expanded']//mat-list/mat-list-item/span/a//span"
    _icon_MatIcon = "//mat-icon[text()='menu']"
    _icon_HomeButton = "//mat-icon[contains(text(),'home')]"
    _icon_ConnectorsIcon = "//a[@href='/connectors']"
    _icon_HomeIcon = "//a[@href='/home']"
    _icon_Insights = "//a[@href='/analyze']"
    _icon_ConsolidatedInsights = "//a[@href='/insight']"
    _icon_Dashboard = "//a[@href='/dashboard']"
    _icon_UserManagement = "//a[@href='/user-management']"
    

    #Verify the Home Page title for LIYA Crafter
    #Params : pageTitle
    def validHomePageTitle(self,pageTitle):
        self.elementClick(self._icon_HomeIcon, "XPATH")
        self.verifyPageTitle(pageTitle)
        self.screenShot()

    ##Verify the menu bar is collapsed by default
    def verifyMenuBarCollapsed(self):
        menu = self.getElement(self._btn_menuBar,"XPATH")
        if "sidenav-collapsed" in menu.get_attribute("class"):
            self.log.info("Verified Menu bar is collapsed by default")
        else:
            self.log.info("Menu bar is not collapsed by default")
            self.elementClick(self._btn_menuBar)


    # Verify the Welcome Card Text at Home Page
    def verifyWelcomeCardText(self):
        self.elementClick(self._icon_HomeButton,"XPATH")
        welcomeCard = self.getElements(self._lbl_welcomeCard,"XPATH")
        for welcomeCardDivs in welcomeCard:
            self._txt_welcomeCard = self._txt_welcomeCard + welcomeCardDivs.text

        if self._txt_welcomeCard == self._txt_expectedWelcomeCard:
            self.log.info("Actual Text '"+self._txt_welcomeCard+ "' matches the expected text value")

        else:
            self.log.info("Actual Text :"+self._txt_welcomeCard+" does not match expected text : "
                  +self._txt_expectedWelcomeCard)

    #Verify the number of Widget Cards
    #Param: numberOfWidgetCards
    def verifyWidgetCardsCount(self,numberOfWidgetCards):
        result_message = f"Verifying widget cards count is {numberOfWidgetCards}."
        try:
            widgetCount = self.getElementsLength(self._crd_widgetCards, "XPATH")
            if widgetCount == numberOfWidgetCards:
                self.log.info("SUCCESS: " + result_message + f" Found: {widgetCount}")
                # Use the test_status_obj instance
                self.test_status.mark(True, result_message)
            else:
                error_message = f"FAILURE: {result_message} Expected {numberOfWidgetCards}, but found {widgetCount}."
                self.log.error(error_message)
                # Use the test_status_obj instance
                self.test_status.mark(False, error_message)
        except Exception as e:
            error_message = f"EXCEPTION during {result_message}: {str(e)}"
            self.log.error(error_message)
            # Use the test_status_obj instance
            self.test_status.mark(False, error_message)


    # Verify the menu bar expands on click
    # Param:
    def verifyTheMenuButtonExpandsOnClick(self):
        self.verifyMenuBarCollapsed()
        self.elementClick(self._icon_MatIcon,"XPATH")
        if self.waitForElement(self._btn_menuBarExpanded,"XPATH"):
            self.log.info("Verified Menu bar is expanded")
            self.screenShot()
            self.elementClick(self._icon_MatIcon,"XPATH")
            self.verifyMenuBarCollapsed()

            RunStatus.mark(self.test_status, True, "Verified Menu button expands and collapses on click.")

        else:
            self.log.info("Verified Menu bar is not expanded")
            RunStatus.mark(self.test_status, False, "Verified Menu button does expands and collapses on click.")

    # Verify the menu bar items present
    # Param:
    def verifyMenuBarItems(self):
        self.verifyTheMenuButtonExpandsOnClick()
        MenuItem = self.getElements(self._icon_menuBarLinksExpanded,"XPATH")
        for Menu in MenuItem:
            self.log.info("The Menu Option at position : "+str(MenuItem.index(Menu)+1)+" is "+Menu.text)

    # Verify the navigation to respective pag name from menu bar items present
    # Param: Page name
    def verifyNavigatedToPage(self, pageName):
        self.log.info("Page name is : " + pageName.lower())
        if pageName.lower() == "connectors":
            self.elementClick(self._icon_ConnectorsIcon,"XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        elif pageName.lower() == "home":
            self.elementClick(self._icon_HomeIcon, "XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        elif pageName.lower() == "insights":
            self.elementClick(self._icon_Insights, "XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        elif pageName.lower() == "consolidated insights":
            self.elementClick(self._icon_ConsolidatedInsights, "XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        elif pageName.lower() == "dashboard":
            self.elementClick(self._icon_Dashboard, "XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        elif pageName.lower() == "user management":
            self.elementClick(self._icon_Dashboard, "XPATH")
            RunStatus.mark(self.test_status, True, f"Navigated to {pageName} page successfully.")
        else:
            self.log.info("No Page Exists with Page Name :"+pageName)
            self.screenShot()

        if self.verifyPageTitle(pageName):
            self.screenShot()
            return True
        else:
            self.screenShot()
            return False
        
        
                           
