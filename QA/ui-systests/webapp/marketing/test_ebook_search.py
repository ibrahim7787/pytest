from utils import sel_utils
from utils.log_setup import getLogger


logger = getLogger(__name__)


# e-book
def test_ebook(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'E-BOOK')]")
    sel_utils.switch_to_window(browser, 1)
    sel_utils.click_by_xpath(browser, "//input[@value='Redeem']")
    expected_msg = "Please Provide bookstub code"
    toast_error_msg = sel_utils.get_text_by_xpath(
        browser, f'//li[normalize-space(text())="{expected_msg}"]'
    )
    assert toast_error_msg == expected_msg, f"Expected: {expected_msg}, Actual:{toast_error_msg}"
    logger.info("------Successfully navigated to E-book and Invalid Redeem validation ------")


# Search
def test_search_option(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//p[contains(text(),'SEARCH')]")
    search_icon = sel_utils.get_text_by_xpath(browser, "//img[@alt='Search']")
    assert search_icon is not None, "Search bar is not displayed"

    # Invalid Search Data
    sel_utils.send_keys_by_xpath(browser, "//input[@id='searchCourse__chnaged']", "atttt")
    sel_utils.click_by_xpath(browser, "//img[@alt='Search']")
    expected_msg = "Searched Courses Not Found"
    error_msg = sel_utils.get_text_by_xpath(browser, f'//h5[contains(text(),"{expected_msg}")]')
    assert error_msg == expected_msg, f"Expected: {expected_msg}, Actual:{error_msg}"
    logger.info("-----Successfully validating to navigate to search and text on search-------")

    # Valid Search Data
    sel_utils.click_by_xpath(browser, "//p[contains(text(),'SEARCH')]")
    search_text = "Cybersecurity"
    sel_utils.send_keys_by_xpath(browser, "//input[@id='searchCourse__chnaged']", {search_text})
    sel_utils.click_by_xpath(browser, "//img[@alt='Search']")
    text_on_card = sel_utils.get_text_by_xpath(browser, "//div[@class='card-body']//span")
    # TODO: Loop over every search result and find text to validate.
    assert text_on_card == search_text, f"Expected:{search_text}, Actual:{text_on_card}"
    logger.info(f"------Successfullly validated Search criteria for keyword: {search_text}------")
