from utils import sel_utils
from utils.log_setup import getLogger


logger = getLogger(__name__)

def resources_cards(browser,link_xpath,navigated_xpath,text):
    sel_utils.click_by_xpath(
        browser, link_xpath
    )
    sel_utils.switch_to_window(browser, 1)
    Navigated_link = sel_utils.get_text_by_xpath(browser, navigated_xpath)
    assert Navigated_link is not None, f"it is not navigated to {text}"
    logger.info(f"----Successfully navigated to {text}----")
    browser.close()
    sel_utils.switch_to_window(browser,0)
    logger.info(f"--- Successfully closed the {text} window and navigate to resources screen---")

def resources_cards_no_validation(browser,link_xpath,text):
    sel_utils.click_by_xpath(browser,link_xpath)
    sel_utils.switch_to_window(browser,1)
    logger.info(f"-----Successfully validated the {text} link -----")
    browser.close()
    sel_utils.switch_to_window(browser,0)
    logger.info(f"--- Successfully closed the {text} tab and navigated to resources screen---")