import time, os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.log_setup import getLogger


logger = getLogger(__name__)


def wait(sec, place):
    logger.info(f"  wait for {sec} sec @ {place}")
    time.sleep(int(sec))


def wait_for_xpath_until(driver, xpath, sec=10):
    WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.XPATH, xpath)))


def wait_for_id_until(driver, xpath, sec=10):
    WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.ID, xpath)))


def wait_for_name_until(driver, xpath, sec=10):
    WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.NAME, xpath)))


def wait_for_tagname_until(driver, xpath, sec=10):
    WebDriverWait(driver, sec).until(EC.presence_of_element_located((By.TAG_NAME, xpath)))


def get_text_by_xpath(driver, xpath, sec=10):
    wait_for_xpath_until(driver, xpath, sec)
    text = driver.find_element(By.XPATH, xpath).text
    return text


def get_text_by_ID(driver, id, sec=10):
    wait_for_id_until(driver, id, sec)
    text = driver.find_element(By.ID, id).text
    return text


def get_attribute_by_id(driver, id, attr_name, sec=10):
    wait_for_id_until(driver, id, sec)
    text = driver.find_element(By.ID, id).get_attribute(attr_name)
    return text


def get_attribute_by_name(driver, name, attr_name, sec=10):
    wait_for_name_until(driver, name, sec)
    text = driver.find_element(By.NAME, name).get_attribute(attr_name)
    return text


def click_by_xpath(driver, xpath, sec=10):
    wait_for_xpath_until(driver, xpath, sec)
    driver.find_element(By.XPATH, xpath).click()


def click_by_id(driver, id, sec=10):
    wait_for_id_until(driver, id, sec)
    driver.find_element(By.ID, id).click()


def click_by_name(driver, name, sec=10):
    wait_for_name_until(driver, name, sec)
    driver.find_element(By.NAME, name).click()


def click_by_css_selector(driver, css_path, sec=10):
    driver.find_element(By.CSS_SELECTOR, css_path).click()


def select_link_by_xpath(driver, xpath, sec=10):
    wait_for_xpath_until(driver, xpath, sec)
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)


def select_link_by_id(driver, id, sec=10):
    wait(1, id)
    wait_for_id_until(driver, id, sec)
    element = driver.find_element_by_id(id)
    driver.execute_script("arguments[0].click();", element)


def find_elements_by_xpath(driver, xpath, sec=20):
    cntr = 1
    options = []
    while cntr <= sec:
        try:
            options = driver.find_elements(By.XPATH, xpath)
            if len(options) == 0:
                wait(1, f"--> waiting to fetch data {cntr}")
                cntr = cntr + 1
            else:
                wait(1, f" Options listed")
                return options
        except:
            wait(1, f"--> waiting to fetch data {cntr}")
            cntr = cntr + 1

    return options


def select_from_native_dropdown(driver, menu_item, opt_value):
    logger.info(f"opt_value: {opt_value}")
    wait_for_xpath_until(
        driver, f"//select[@name='{menu_item}']//" + f'option[contains(text(),"{opt_value}")]'
    )
    Select(driver.find_element(By.NAME, menu_item)).select_by_visible_text(opt_value)


def send_keys_by_name(driver, name_attribute, value, sec=10):
    wait_for_name_until(driver, name_attribute, sec)
    driver.find_element(By.NAME, name_attribute).send_keys(value)


def send_keys_by_id(driver, id_attribute, value, sec=10):
    wait_for_id_until(driver, id_attribute, sec)
    driver.find_element(By.ID, id_attribute).send_keys(value)


def send_keys_by_xpath(driver, xpath, value, sec=10):
    wait_for_xpath_until(driver, xpath, sec)
    driver.find_element(By.XPATH, xpath).send_keys(value)


def send_keys_by_tagname(driver, tagname_attribute, value, sec=10):
    wait_for_tagname_until(driver, tagname_attribute, sec)
    driver.find_element(By.TAG_NAME, tagname_attribute).send_keys(value)


def launch_url(driver, url):
    if not url:
        url = os.getenv("CL_URL")
    logger.info(f"Launching URL: {url}")
    driver.get(url)
    logger.info(f"BROWSER is Launched succcessfully with URL: {url}")


def switch_to_window(driver, window_index):
    wait(1, f"Switching to newly opened window")
    driver.switch_to.window(driver.window_handles[window_index])
    wait(1, f"Switched to window: {driver.title}")


def switch_to_iframe(driver, xpath):
    logger.info(f"Switching to iframe: {xpath}")
    iframe_element = driver.find_element(
        By.XPATH, "//iframe[@title='Select a Date & Time - Calendly']"
    )
    driver.switch_to.frame(iframe_element)


def switch_to_default(driver):
    logger.info(f"Switching to default window")
    driver.switch_to.default_content()


def scroll_to_page_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait(2, "Scrolling down to reach page end..")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    wait(1, "Scrolled to page end")


def get_dimensions(driver, xpath):
    ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    dimensions = ele.size
    logger.info(f"dimensions = {dimensions}")
    return dimensions


def browser_refresh(driver):
    driver.refresh()
    wait(2, "to refresh the browser")
