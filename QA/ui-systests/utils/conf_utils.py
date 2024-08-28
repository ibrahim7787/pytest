import os
from selenium import webdriver
from tempfile import mkdtemp
from datetime import date
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service
from utils.errors import decor_handle_exc
from utils.log_setup import getLogger


log_level = os.getenv('LOG_LEVEL')
logger = getLogger(__name__, log_level)
env = os.getenv('CL_STAGE')


@decor_handle_exc
def chrome_driver(headless, cloud_mode):
    options = ChromeOptions()
    if headless:
        options.add_argument('--headless')
    # options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if cloud_mode:
        logger.info("Running in Cloud")
        # BASED ON: https://github.com/umihico/docker-selenium-lambda/blob/main/test.py
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-gpu-sandbox')
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(
            service=Service(executable_path="/opt/chromedriver"), options=options
        )
    else:
        # LOCAL MODE
        logger.info(f"Running locally in env: {env}")
        driver = webdriver.Chrome(options=options)
    return driver


@decor_handle_exc
def browserstack_driver(browser_stack_browser, browser_stack_version, browser_stack):
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
    capabilities = {
        "iphone": {
            "browserName": "safari",
            "deviceOrientation": "portrait",
            "deviceName": "iPhone 15 Pro Max",
            "osVersion": "17",
            "sessionName": f"{env}_{test_name}",
            "buildName": f"{env}_UITestsIOS_{date.today()}",
        },
        "android": {
            "browserName": "Chrome",
            "deviceOrientation": "portrait",
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "10",
            "sessionName": f"{env}_{test_name}",
            "buildName": f"{env}_UITestsIOS_{date.today()}",
        },
        "chrome": {
            "browserName": "Chrome",
            "browserVersion": browser_stack_version or "latest",
            "os": "Windows",
            "osVersion": "11",
            "sessionName": f"{env}_{test_name}",
            "buildName": f"{env}_UITests_{date.today()}",
        },
        "firefox": {
            "browserName": "Firefox",
            "browserVersion": browser_stack_version or "102.0",
            "os": "Windows",
            "osVersion": "10",
            "sessionName": f"{env}_{test_name}",
            "buildName": f"{env}_UITests_{date.today()}",
        },
        "safari": {
            "browserName": "Safari",
            "browserVersion": browser_stack_version or "14.1",
            "os": "OS X",
            "osVersion": "Big Sur",
            "sessionName": f"{env}_{test_name}",
            "buildName": f"{env}_UITests_{date.today()}",
        },
    }

    def get_browser_option(browser):
        switcher = {
            "chrome": ChromeOptions(),
            "firefox": FirefoxOptions(),
            "edge": EdgeOptions(),
            "safari": SafariOptions(),
            "iphone": SafariOptions(),
            "android": ChromeOptions(),
        }
        return switcher.get(browser, ChromeOptions())

    options = get_browser_option(browser_stack_browser.lower())
    cap = capabilities[browser_stack_browser.lower()]
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": browser_stack['user'],
        "accessKey": browser_stack['key'],
    }
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    if "deviceName" in cap:
        bstack_options['deviceName'] = cap["deviceName"]
    if "deviceOrientation" in cap:
        bstack_options["deviceOrientation"] = cap["deviceOrientation"]
    if cap['browserName'] in ['ios']:
        cap['browserName'] = 'safari'
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]

    options.set_capability('bstack:options', bstack_options)
    options.add_argument("start-maximized")
    driver = webdriver.Remote(command_executor=browser_stack['url'], options=options)
    return driver
