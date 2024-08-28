from utils import sel_utils
from utils.log_setup import getLogger
from helpers import social_links

logger = getLogger(__name__)


def test_social_links(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    logger.info("-----Verifying Social Links in Header-----")
    social_links.verify_social_links(browser, "header")
    logger.info("-----Successfully verified Social Links in Header-----")

    # Scroll to the end of the page
    sel_utils.scroll_to_page_end(browser)

    logger.info("-----Verifying Social Links in Footer-----")
    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")
    social_links.verify_social_links(browser, "footer")
    logger.info("-----Successfully verified Social Links in Footer-----")
