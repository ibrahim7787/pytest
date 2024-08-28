import os
from utils import sel_utils
from utils.log_setup import getLogger
from helpers import login

logger = getLogger(__name__)


def test_succesful_login(f_driver):
    browser = f_driver

    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'LOGIN')]")
    login.login_complylaw(browser, os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS"))
    validation_text = sel_utils.get_text_by_xpath(
        browser, '//span[contains(text(),"Dashboard")]', 20
    )
    if not validation_text:
        sel_utils.click_by_xpath(browser, "//button[@class='sidebar-toggler']//img")
        sel_utils.wait(1, "to check dashboard")

        validation_text = sel_utils.get_text_by_xpath(
            browser, '//span[contains(text(),"Dashboard")]', 20
        )

    logger.info(f"validation text = {validation_text}")
    assert validation_text == "Dashboard", "Login Failed"
    logger.info(f"-----Successfully Logged in-----")
