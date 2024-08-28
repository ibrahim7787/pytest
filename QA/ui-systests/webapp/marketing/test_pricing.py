from utils import sel_utils
from utils.log_setup import getLogger
from helpers import calendar
from selenium.webdriver.common.by import By

logger = getLogger(__name__)


def test_pricing(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)

    # Enroll Today at Navbar Section
    logger.info("-----Verifying Enroll Today Button in NavBar-----")
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'ENROLL TODAY')]")
    pricing_section = sel_utils.get_text_by_xpath(browser, "//h4[contains(text(),'Premium')]")
    assert (
        pricing_section is not None
    ), "after clicking on enroll today button it is not navigated to pricing section"
    logger.info(
        "--------Successfully navigated to pricing section after clicking enroll today in the navbar-------"
    )

    logger.info("-----Verifying pricing Section-----")

    # Clickable functionality of  "Individual" and "Dealerships" toggle buttons
    def subscribe_text(marketing):
        logger.info(f"validating {marketing} card Subscriptions")
        browser.execute_script("window.scrollTo(0, 2000);")
        if marketing == "FREE":
            sel_utils.wait(1, "Clicking on START 7 DAY FREE TRIAL Button")
            sel_utils.click_by_xpath(browser, "//button[contains(text(),'start 7 day free trial')]")
        else:
            sel_utils.wait(1, "Clicking SUBSCRIBE button")
            sel_utils.click_by_xpath(browser, "//button[contains(text(),'Subscribe')]")
        sub_page_text = sel_utils.get_text_by_xpath(browser, "//h5")
        text_on_ui = "Create An Account"
        assert sub_page_text == text_on_ui, f"Actual:{sub_page_text} Expected: {text_on_ui}"
        sel_utils.click_by_xpath(browser, "//nav[@id='mainNav']//img[@alt='Logo']")
        logger.info(f"------Successfully validated {marketing} card------")

    # verifying Dealerships section
    sel_utils.wait(1, "Toggle to Dealerships tab")
    sel_utils.click_by_xpath(browser, "//div[@id='nav-dealergroup-tab']")
    sel_utils.wait(1, "------Validating Premium Card------")
    premium_val = sel_utils.get_text_by_xpath(browser, "//h6//span[@id='original_price_info']")
    assert premium_val is not None and float(premium_val) > 0.0, "There is no premium value"
    subscribe_text("PREMIUM")

    # Dealership Free card
    browser.execute_script("window.scrollTo(0, 1400);")
    sel_utils.wait(1, "Toggle to Dealerships tab")
    sel_utils.click_by_xpath(browser, "//div[@id='nav-dealergroup-tab']")
    sel_utils.wait(1, "------Validating Free Card------")
    browser.execute_script("window.scrollTo(0, 2000);")
    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")
    browser.execute_script("window.scrollTo(0, 2000);")
    subscribe_text("FREE")
    browser.execute_script("window.scrollTo(0, 1400);")
    sel_utils.wait(1, "Toggle to Dealerships tab")
    sel_utils.click_by_xpath(browser, "//div[@id='nav-dealergroup-tab']")
    sel_utils.wait(2, "to load all the cards")
    browser.execute_script("window.scrollTo(0, 2000);")
    sel_utils.wait(1, "SCHEDULE ONE ON ONE DEMO Button of PREMIUM Card")
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'SCHEDULE ONE ON ONE DEMO')]")
    calendar.handle_calendar(browser)
    sel_utils.wait(1, "------Successfully validated Schedule One on One Demo of PREMIUM Card------")

    # verify Enterprise section
    browser.execute_script("window.scrollTo(0, 1400);")
    sel_utils.wait(1, "Toggle to Dealerships tab")
    sel_utils.click_by_xpath(browser, "//div[@id='nav-dealergroup-tab']")
    sel_utils.wait(1, "------Validating ENTERPRISE Card------")
    browser.execute_script("window.scrollTo(0, 2000);")
    sel_utils.wait(2, "Contact Sales Button of ENTERPRISE Card")
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'CONTACT SALES')]")
    calendar.handle_calendar(browser)
    sel_utils.wait(1, "------Successfully Validated ENTERPRISE Card------")

    # drop down for Emp Count
    browser.execute_script("window.scrollTo(0, 1500);")
    sel_utils.wait(2, "------Validating Employee count drop down button------")
    sel_utils.click_by_xpath(browser, "//select[@id='users_count']")
    dd_ele = sel_utils.find_elements_by_xpath(browser, "//select[@id='users_count']//option")
    assert len(dd_ele) == 10, "Dropdown Values are missing. Please double check"
    for i in range(1, len(dd_ele) + 1):

        sel_utils.click_by_xpath(browser, f"//select[@id='users_count']//option[{i}]")
        selected_value = sel_utils.get_text_by_xpath(
            browser, f"//select[@id='users_count']//option[{i}]"
        )
        logger.info(f"Selecting Option from dropdown: {selected_value}")
        if i == 10:
            logger.info(
                "Checking if Subscribe button is diabled when Value = 100 selected in dropdown"
            )
            subscribe_button = browser.find_element(
                By.XPATH, "(//button[@disabled='disabled'])[contains(text(),'Subscribe')]"
            )
            trial_btn = browser.find_element(
                By.XPATH,
                "(//button[@disabled='disabled'])[contains(text(),'start 7 day free trial')]",
            )
            assert (
                subscribe_button is not None
            ), "Subscribe button should be DISABLED when Value = 100 in dropdown"
            assert (
                trial_btn is not None
            ), "START 7 DAY FREE TRIAL button should be DISABLED when Value = 100 in dropdown"
    logger.info("------Successfully Validated Employee count drop down------")

    # verifying individual section
    browser.execute_script("window.scrollTo(0, 1600);")
    sel_utils.wait(1, "------Validating INDIVIDUAL Tab------")
    # after navigating from subscribe to marketing,default selection is Individual so we are clicking Delaership and then Individual to verify Individual button is clickable
    sel_utils.click_by_xpath(browser, "//div[@id='nav-dealergroup-tab']")
    sel_utils.click_by_xpath(browser, "//div[@id='nav-individual-tab']")
    browser.execute_script("window.scrollTo(0, 1600);")

    # yearly
    sel_utils.wait(2, "Toggle to Yearly Radio Button")
    sel_utils.click_by_xpath(browser, "//input[@id='radio1']")
    sel_utils.wait_for_xpath_until(
        browser, "(//h6//following-sibling::span[@class='home_billed'])[1]"
    )
    ind_yearly_val = sel_utils.get_text_by_xpath(browser, "(//h6//span)[1]")
    assert float(ind_yearly_val) == 39.99, f"Expected: 39.99 Actual:{float(ind_yearly_val)}"
    subscribe_text("Individual Yearly PREMIUM")

    # monthly
    browser.execute_script("window.scrollTo(0, 1600);")
    sel_utils.wait(1, "Default Monthly Radio Button")
    # after navigating from subscribe to marketing,default selection is montly so we are clicking yearly and then monthly to verify montly button is clickable
    sel_utils.click_by_xpath(browser, "//input[@id='radio1']")
    sel_utils.click_by_xpath(browser, "//input[@id='radio0']")
    ind_mon_val = sel_utils.get_text_by_xpath(browser, "//span[@id='original_price_info']")
    assert float(ind_mon_val) == 49.99, f"Expected: 49.99 Actual:{float(ind_mon_val)}"
    subscribe_text("Individual Monthly PREMIUM")
