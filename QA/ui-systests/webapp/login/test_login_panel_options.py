import os
from utils import sel_utils
from utils.log_setup import getLogger
from helpers import login

logger = getLogger(__name__)


def test_login_panel(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'LOGIN')]")
    login.login_complylaw(browser, os.getenv("ADMIN_USER"), f'{os.getenv("ADMIN_PASS")}111')
    expected_msg = "Ops! You have entered invalid credentials"
    toast_error_msg = sel_utils.get_text_by_xpath(
        browser, f'//div[contains(text(),"{expected_msg}")]'
    )
    assert toast_error_msg == expected_msg, f"Expected : {expected_msg} , Actual:{toast_error_msg}"
    logger.info("-----Successfully displayed error message for invalid credentials-----")

    # validate forgot password link is clickable and navigate to forgot password page or not
    sel_utils.click_by_xpath(browser, f'//a[contains(text(),"Forgot Password")]')
    sel_utils.send_keys_by_xpath(browser, "//input[@name='email']", os.getenv("ADMIN_USER"))
    sel_utils.click_by_xpath(browser, f'//button[contains(text(),"Send Reset Instructions")]')
    reset_txt_exp = "Reset Password"
    reset_txt = sel_utils.get_text_by_xpath(browser, f"//h5[contains(text(),'{reset_txt_exp}')]")
    assert reset_txt == "Reset Password", f"Expected text:{reset_txt_exp}, Actual text: {reset_txt}"
    logger.info("-----Successfully navigated to Reset Password page-----")

    # Navigating to marketing page from forgot password screen
    sel_utils.click_by_xpath(browser, "//a[@class='navbar-brand']//img[@alt='Logo']")
    logger.info("-----Successfully navigated to Marketing page-----")

    sel_utils.click_by_xpath(browser, "//a[contains(text(),'LOGIN')]")
    login.login_complylaw(browser, os.getenv("ADMIN_USER"), "")
    expected_error_msg = 'This field is required.'
    toast_error_msg = sel_utils.get_text_by_xpath(
        browser, f'//div[contains(text(),"{expected_error_msg}")]'
    )
    assert (
        toast_error_msg == expected_error_msg
    ), f"Expected : {expected_error_msg} , Actual:{toast_error_msg}"
    logger.info("-----Successfully displayed error message for Missing password-----")
