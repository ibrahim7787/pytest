from utils import sel_utils
from utils.log_setup import getLogger


logger = getLogger(__name__)


def handle_calendar(browser):
    sel_utils.switch_to_iframe(browser, "//iframe[@title='Select a Date & Time - Calendly']")
    try:
        sel_utils.click_by_id(browser, "onetrust-accept-btn-handler")
        logger.info("clicking on I understand button.")
    except:
        pass
    sel_utils.switch_to_default(browser)
    sel_utils.click_by_xpath(browser, "//div[@class='calendly-popup-close']")
    logger.info("Closed the calendly window")
