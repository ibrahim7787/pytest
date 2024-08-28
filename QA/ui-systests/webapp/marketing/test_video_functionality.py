import os, sys
from utils import sel_utils
from utils.log_setup import getLogger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

env = os.getenv('STAGE', 'dev')
sys.path.append(os.path.dirname(sys.path[0]))

logger = getLogger(__name__)


def test_video_functionality(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser,"https://uatlms.techraq.com/")
    logger.info("-----Verifying video functionality on marketing----")
    video= browser.find_element(By.XPATH,"//video")
    sel_utils.wait(5,"PAUSE after 5 sec")
    browser.execute_script("arguments[0].pause();", video)
    sel_utils.wait(5,"PLAY after 5 sec")
    browser.execute_script("arguments[0].play();", video)
    sel_utils.wait(5,"UNMUTE after 5 sec")
    browser.execute_script("arguments[0].muted = false;", video)
    sel_utils.wait(5,"MUTE after 5 sec")
    browser.execute_script("arguments[0].muted = true;", video)
    sel_utils.wait(5,"Fullscreen after 5 sec")
    ActionChains(browser).move_to_element(video).click().perform()
    browser.execute_script("arguments[0].requestFullscreen()", video)
    sel_utils.wait(5,"Exit Fullscreen after 5 sec")
    browser.execute_script("document.exitFullscreen()", video)
    sel_utils.wait(5,"Exit Fullscreen after 5 sec")
    logger.info("---Successfully validated the video functionality in marketing----")