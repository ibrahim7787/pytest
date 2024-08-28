import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.log_setup import getLogger
from utils import conf_utils

log_level = os.getenv('LOG_LEVEL', 'INFO')
logger = getLogger(__name__, log_level)

@pytest.fixture
def f_driver(f_customOptions, f_browserstackOptions):
    headless, browser, app_url = f_customOptions
    browser_stack_browser, browser_stack_version = f_browserstackOptions
    driver = None
    logger.info(f"browser: {browser}")
    os.environ['BROWSER'] = browser
    bs_user = "sanjivanibodke_iJk2rp"
    bs_key = "7ANDPRjmSBsaPmdWqYXP"
    secrets_dict = {
        "user": bs_user,
        "key": bs_key,
        "url": f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
    }
    cloud_mode = os.getenv('CLOUD_MODE', 'False') == 'True'
    
    if browser.strip() == 'browserstack':
        driver = conf_utils.browserstack_driver(
            browser_stack_browser, browser_stack_version, secrets_dict
        )
    elif browser.strip() == 'chrome':
        driver = conf_utils.chrome_driver(headless, cloud_mode)
    elif browser.strip() == 'firefox':
        options = webdriver.FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

@pytest.fixture
def chrome_driver(request):
    headless = request.config.getoption("--headless")
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

@pytest.fixture
def firefox_driver(request):
    headless = request.config.getoption("--headless")
    options = webdriver.FirefoxOptions()
    options.headless = headless
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    yield driver
    driver.quit()

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "e2e: mark test to run only on named e2e",
    )

def pytest_addoption(parser):
    test_firstname, test_lastname, test_phone, test_email, test_password = (
        "Vasu",
        "Amarapu",
        "1234567890",
        "vasu.amarapu@techraq.com",
        "abcd1234",
    )

    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )
    parser.addoption(
        "--site", action="store", default=None, help="Provide complete URL to site"
    )
    parser.addoption(
        "--app_url", action="store", default=None, help="Provide mobile app URL from BrowserStack"
    )
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser options: chrome, firefox, or browserstack"
    )
    parser.addoption(
        "--email", action="store", default=test_email, help="Provide email"
    )
    parser.addoption(
        "--password", action="store", default=test_password, help="Provide password"
    )
    parser.addoption(
        "--phonenumber", action="store", default=test_phone, help="Provide phone number"
    )
    parser.addoption(
        "--firstname", action="store", default=test_firstname, help="Provide first name"
    )
    parser.addoption(
        "--browserstack", action="store", default="chrome", help="Browser options for BrowserStack: chrome, firefox"
    )
    parser.addoption(
        "--ver", action="store", default="latest", help="Version options: chrome(latest/94,95,..), firefox, or browserstack"
    )
