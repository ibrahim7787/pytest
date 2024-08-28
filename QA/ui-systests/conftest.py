import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from utils.log_setup import getLogger
from utils import conf_utils

log_level = os.getenv('LOG_LEVEL')
logger = getLogger(__name__, log_level)


@pytest.fixture
def f_driver(f_customOptions, f_browserstackOptions):
    headless, B, app_url = f_customOptions
    browser_stack_browser, browser_stack_version = f_browserstackOptions
    driver = None
    logger.info(f"browser: {B}")
    os.environ['BROWSER'] = B
    bs_user = "sanjivanibodke_iJk2rp"
    bs_key = "7ANDPRjmSBsaPmdWqYXP"
    secrets_dict = {
        "user": bs_user,
        "key": bs_key,
        "url": f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
    }
    cloud_mode = os.getenv('CLOUD_MODE', False)
    if B.strip() == 'browserstack':
        driver = conf_utils.browserstack_driver(
            browser_stack_browser, browser_stack_version, secrets_dict
        )
    if B.strip() == 'chrome':
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # driver = conf_utils.chrome_driver(headless, cloud_mode)
    elif B.strip() == 'firefox':
        options = webdriver.FirefoxOptions()
        options.headless = headless
        # options.add_argument("start-maximized")
        driver = webdriver.Firefox(options=options, executable_path="geckodriver")
    yield driver
    driver.quit()


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "e2e: mark test to run only on named e2e",
    )


# @pytest.fixture
# def f_testuserdetails():
#     return get_test_details()


# def get_test_details():
#     secrets_dict = aws.get_secret(f"{env}/testuser")
#     firstname = secrets_dict['FIRST_NAME']
#     lastname = secrets_dict['LAST_NAME']
#     phone = secrets_dict['PHONE']
#     email = secrets_dict['TEST_USER']
#     password = secrets_dict['TEST_USER_PW']
#     return firstname, lastname, phone, email, password


# class Options:
#     def __init__(self):
#         pass

#     def login(self, request):
#         self.site = request.config.getoption("-S")
#         self.email = request.config.getoption("-E")
#         self.password = request.config.getoption("-P")

#     def signup(self, request):
#         self.site = request.config.getoption("-S")
#         self.email = request.config.getoption("-E")
#         self.password = request.config.getoption("-P")
#         self.pn = request.config.getoption("-M")
#         self.fn = request.config.getoption("-F")


# @pytest.fixture
# def f_login(request):
#     options = Options()
#     options.login(request)
#     return options


# @pytest.fixture
# def f_signup(request):
#     options = Options()
#     options.signup(request)
#     return options


def pytest_addoption(parser):
    test_firstname, _test_lastname, test_phone, test_email, test_password = (
        "Vasu",
        "Amarapu",
        "1234567890",
        "vasu.amarapu@techraq.com",
        "abcd1234",
    )

    parser.addoption(
        "-H", "--headless", action="store_true", default=False, help="my option: True or False"
    )
    parser.addoption(
        "-S", "--site", action="store", default=None, help="provide complete url to site"
    )
    parser.addoption(
        "-A",
        "--app_url",
        action="store",
        default=None,
        help="provide mobile app url from browserstack",
    )
    parser.addoption(
        "-B",
        "--browser",
        action="store",
        default="chrome",
        help="options: chrome or firefox or browserstack",
    )
    parser.addoption("-E", "--email", action="store", default=test_email, help="provide email")
    parser.addoption(
        "-P", "--password", action="store", default=test_password, help="provide password"
    )
    parser.addoption(
        "-M", "--phonenumber", action="store", default=test_phone, help="provide phonenumber"
    )
    parser.addoption(
        "-F", "--firstname", action="store", default=test_firstname, help="provide firstname"
    )
    parser.addoption(
        "-N",
        "--browserstack",
        action="store",
        default="chrome",
        help="options: chrome or firefox",
    )
    parser.addoption(
        "-R",
        "--ver",
        action="store",
        default="latest",
        help="options: chrome(latest/94,95,..) or firefox or browserstack",
    )
    # parser.addoption(
    #     "-X",
    #     "--log_cli_format",
    #     action="store",
    #     default=fmt,
    #     help="provide complete url to site",
    # )


@pytest.fixture
def f_browserstackOptions(request):
    bs = request.config.getoption("-N")
    ver = request.config.getoption("-R")
    return (bs, ver)


@pytest.fixture
def f_customOptions(request):
    head = request.config.getoption("--headless")
    brow = request.config.getoption("-B")
    app_url = request.config.getoption("-A")
    return (head, brow, app_url)
