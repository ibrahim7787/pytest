from utils import sel_utils
from utils.log_setup import getLogger
from helpers import calendar

logger = getLogger(__name__)


def test_schedule_demo(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    logger.info("-----Verifying SCHEDULE A DEMO TODAY in the navbar section----")

    # schedule a demo today on navbar button
    sel_utils.click_by_xpath(browser, "//a[contains(text(),'SCHEDULE A DEMO TODAY!')]")
    calendar.handle_calendar(browser)

    # E- learning schedule a demo today
    browser.execute_script("window.scrollTo(0,400 );")
    sel_utils.wait(1, "To click the schedule demo today button present in the E- Learning section")
    sel_utils.click_by_xpath(browser, "//a[@class='anchor_clr']")
    calendar.handle_calendar(browser)
