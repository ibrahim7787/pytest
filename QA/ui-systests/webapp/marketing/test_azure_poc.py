import os
import sys
from utils import sel_utils
from utils.log_setup import getLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import resources
from helpers import resources
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

env = os.getenv('STAGE', 'dev')
sys.path.append(os.path.dirname(sys.path[0]))

logger = getLogger(__name__)


# e-book
def test_ebook(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser, 'https://uatlms.techraq.com/')
    sel_utils.wait(10, "Page is launching..")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'E-BOOK')]"))
    )
    text = browser.find_element(By.XPATH, "//a[contains(text(),'E-BOOK')]").text
    logger.info(f"text = {text}")
    text_on_screen = sel_utils.get_text_by_xpath(browser, "//a[contains(text(),'E-BOOK')]")
    logger.info(f"text_on_screen = {text_on_screen}")

    sel_utils.click_by_xpath(browser, "//a[contains(text(),'E-BOOK')]")
    sel_utils.switch_to_window(browser, 1)
    sel_utils.click_by_xpath(browser, "//input[@value='Redeem']")
    expected_msg = "Please Provide bookstub code"
    toast_error_msg = sel_utils.get_text_by_xpath(
        browser, f'//li[normalize-space(text())="{expected_msg}"]'
    )
    assert toast_error_msg == expected_msg, f"Expected: {expected_msg}, Actual:{toast_error_msg}"
    logger.info("------Successfully navigated to E-book and Invalid Redeem validation ------")
