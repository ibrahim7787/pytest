from utils import sel_utils
from utils.log_setup import getLogger
from helpers import calendar
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


logger = getLogger(__name__)


def test_footer_links(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    logger.info("Clicking Allow Cookies")
    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")
    logger.info("-----Verifying Links in Footer Section-----")

    # Home
    logger.info(f"Verifying link:Home")
    sel_utils.scroll_to_page_end(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'Home')]")

    def click_footer_link(link):
        logger.info(f"Verifying link: {link}")
        sel_utils.scroll_to_page_end(browser)
        sel_utils.click_by_xpath(browser, f"//a[contains(text(), '{link}')]")
        validation_txt = sel_utils.get_text_by_xpath(browser, f"//h3[contains(text(), '{link}')]")
        return validation_txt

    # What We Offer
    whatwe_offer = click_footer_link("What We Offer")
    assert whatwe_offer == "WHAT WE OFFER", f"Expected: WHAT WE OFFER Actual:{whatwe_offer}"

    # Why Comply.law
    logger.info("Verifying link: Why COMPLY.LAW")
    sel_utils.scroll_to_page_end(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(), 'Why COMPLY.LAW')]")
    why_complylaw = sel_utils.get_text_by_xpath(
        browser, "//h3[contains(text(), 'ABOUT COMPLY.LAW')]"
    )
    assert why_complylaw is not None, "Whycomplylaw screen is not displayed"

    # Privacy Policy
    privacy_policy = click_footer_link("Privacy Policy")
    assert (
        privacy_policy == "Privacy Policy".upper()
    ), f"Expected:{'Privacy Policy'.upper()} Actual:{privacy_policy}"

    # Cookie Policy
    cookie_policy = click_footer_link("Cookie Policy")
    assert (
        cookie_policy == "Cookie Policy".upper()
    ), f"Expected:{'Cookie Policy'.upper()} Actual:{cookie_policy}"

    #Contact
    logger.info("Verifying contact link")
    sel_utils.scroll_to_page_end(browser)
    sel_utils.click_by_xpath(browser,"//a[contains(text(),'Contact')]")
    sel_utils.wait(5, "to Show the email popup")
    action = ActionChains(browser)
    action.send_keys(Keys.ESCAPE).perform()

    # Blogs & News
    logger.info("Verifying link: Blogs & News")
    sel_utils.scroll_to_page_end(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(), 'Blogs & News')]")
    blogs_news = sel_utils.get_text_by_xpath(browser, "//h3[contains(text(), 'Resources')]")
    assert blogs_news is not None, "Resources screen is not displayed"

    # Terms & Conditions
    terms_conditions = click_footer_link("Terms & Conditions")
    assert (
        terms_conditions == "Terms & Conditions".upper()
    ), f"Expected:{'Terms & Conditions'.upper()} Actual:{terms_conditions}"

    # Request A Demo
    logger.info("Verifying link: Request A Demo")
    sel_utils.scroll_to_page_end(browser)
    sel_utils.click_by_xpath(browser, "//a[contains(text(), 'Request A Demo')]")
    calendar.handle_calendar(browser)

    logger.info("-----Successfully verified all the links in footer --------")

    sel_utils.scroll_to_page_end(browser)
    sel_utils.wait_for_xpath_until(browser, "//button[contains(text(),'Submit')]")

    def email_error_msg(expected_msg):
        logger.info(f"Verifying error messgae: {expected_msg}")
        sel_utils.scroll_to_page_end(browser)
        sel_utils.click_by_xpath(browser, "//button[contains(text(),'Submit')]")
        error_txt = sel_utils.get_text_by_xpath(browser, f"//p[contains(text(),'{expected_msg}')]")
        return error_txt

    # no data on email field
    no_text_mail = email_error_msg("Please Enter Email")
    assert (
        no_text_mail == "Please Enter Email"
    ), f"Expected: Please Enter Email Actual:{no_text_mail}"
    logger.info("-----Successfully validated to error text for no data on field-------")

    # Invalid data
    sel_utils.send_keys_by_xpath(browser, "//input[@id='email']", "111")
    invalid_text_mail = email_error_msg("Please Enter A Valid Email Address")
    assert (
        invalid_text_mail == "Please Enter A Valid Email Address"
    ), f"Expected: Please Enter A Valid Email Address Actual:{invalid_text_mail}"
    logger.info("-----Successfully validated to error text for invalid data-------")

    # valid Data
    sel_utils.send_keys_by_xpath(browser, "//input[@id='email']", "bandana@gmail.com")
    valid_text_mail = email_error_msg("Mail Sent Successfully")
    assert (
        valid_text_mail == "Mail Sent Successfully"
    ), f"Expected: Mail Sent Successfully Address Actual:{valid_text_mail}"
    logger.info("-----Successfully validated to success message for valid data-------")
