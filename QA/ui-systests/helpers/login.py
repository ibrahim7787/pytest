from utils import sel_utils
from utils.log_setup import getLogger

logger = getLogger(__name__)


def login_complylaw(browser, username, password):
    sel_utils.send_keys_by_xpath(browser, '//input[@name="email"]', username)
    sel_utils.send_keys_by_xpath(browser, '//input[@name="password"]', password)
    sel_utils.click_by_xpath(browser, "//button[contains(text(),'Sign In')]")
