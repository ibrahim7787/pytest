import os, sys
from utils import sel_utils
from utils.log_setup import getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


logger = getLogger(__name__)


def test_why_comply_law(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")
    sel_utils.click_by_xpath(browser, "//a[@role='button']")
    options = sel_utils.get_text_by_xpath(browser, "//a[@role='button']/following-sibling::ul")
    logger.info(f"Dropdown Options: {options}")
    sel_utils.click_by_xpath(browser, "//a[text()='Our Team']")

    ourteam_page = sel_utils.get_text_by_xpath(browser, "//h3[contains(text(),'OUR TEAM')]")
    ourteam_head = sel_utils.get_text_by_xpath(browser, "//div[@class='team_head']")
    assert ourteam_page == ourteam_head, f"actual:{ourteam_page},expected:{ourteam_head}"
    logger.info("----Successfully Navigated to OUR TEAM page----")
    book_text = "Automotive Dealership Safeguard: Cybersecurity"
    sel_utils.wait(1, f"Clicking on amazon link for book {book_text}")
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'www.amazon.com. ')]")
    sel_utils.switch_to_window(browser, 1)
    head_text = sel_utils.get_text_by_xpath(
        browser,
        f"//span[contains(text(),'{book_text}')]",
    )
    assert head_text == book_text, f"Expected text:{head_text}, Actual text: {book_text}"
    logger.info("----Successfully Navigated to AMAZON page----")
    browser.close()
    sel_utils.switch_to_window(browser, 0)

    # About Comply.law

    sel_utils.click_by_xpath(browser, "//a[@role='button']")
    sel_utils.click_by_xpath(browser, "(//a[@href='https://uatlms.techraq.com/complyaboutus'])[1]")
    about_comply_page = sel_utils.get_text_by_xpath(
        browser, "//h3[contains(text(),'ABOUT COMPLY.LAW')]"
    )
    about_head = sel_utils.get_text_by_xpath(browser, "//b")
    assert about_comply_page == about_head, f"actual:{about_comply_page},Expected:{about_head}"
    logger.info("----Successfully Navigated to ABOUT COMPLY.LAW page----")
