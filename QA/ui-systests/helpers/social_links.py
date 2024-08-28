from utils import sel_utils
from utils.log_setup import getLogger


logger = getLogger(__name__)


def verify_social_links(browser, location):
    # Facebook Button
    logger.info(f"Verifying Facebook Button")
    if location == "header":
        sel_utils.click_by_xpath(browser, "//a[@href='https://www.facebook.com/COMPLY.LAW1 ']")
    elif location == "footer":
        sel_utils.click_by_xpath(browser, "//a[@href='https://www.facebook.com/COMPLY.LAW1']//img")
    sel_utils.switch_to_window(browser, 1)
    sel_utils.click_by_xpath(browser, "//div[@aria-label='Close']")
    facebook_text = sel_utils.get_text_by_xpath(
        browser, "//span//h1[contains(text(),'Comply.Law')]"
    )
    assert (
        facebook_text.strip() == "Comply.Law"
    ), f"Actual: {facebook_text.strip()} Expected: 'Comply.Law'"
    browser.close()
    logger.info(f"Facebook Button verification successful")

    # Twitter Button
    logger.info(f"Verifying Twitter Button")
    sel_utils.switch_to_window(browser, 0)
    if location == "header":
        sel_utils.click_by_xpath(browser, "//li[@class='twitr_resl']//a")
    elif location == "footer":
        sel_utils.click_by_xpath(
            browser,
            "(//a[@href='https://www.facebook.com/COMPLY.LAW1']//following-sibling::a//img)[1]",
        )
    sel_utils.switch_to_window(browser, 1)
    X_text = sel_utils.get_text_by_xpath(browser, "//span[contains(text(),'Sign in to X')]", 30)
    assert X_text == "Sign in to X", f"Actual:{X_text} Expected:'Sign in to X'"
    browser.close()
    logger.info(f"Twitter Button verification successful")

    # LinkedIn Button
    logger.info(f"Verifying LinkedIn Button")
    sel_utils.switch_to_window(browser, 0)
    if location == "header":
        sel_utils.click_by_xpath(browser, "//li[@class='twitr_resl']//following-sibling::li[1]//a")
    elif location == "footer":
        sel_utils.click_by_xpath(
            browser,
            "(//a[@href='https://www.facebook.com/COMPLY.LAW1']//following-sibling::a//img)[2]",
        )
    sel_utils.switch_to_window(browser, 1)
    signin_text = sel_utils.get_text_by_xpath(browser, "//button[@type='submit']")
    logger.info(signin_text)
    assert signin_text == "Sign in", f"Actual:{signin_text} Expected:'Sign in'"
    browser.close()
    logger.info(f"LinkedIn Button verification successful")

    # Youtube Button
    logger.info(f"Verifying Youtube Button")
    sel_utils.switch_to_window(browser, 0)
    if location == "header":
        sel_utils.click_by_xpath(browser, "//li[@class='twitr_resl']//following-sibling::li[2]//a")
    elif location == "footer":
        sel_utils.click_by_xpath(
            browser,
            "(//a[@href='https://www.facebook.com/COMPLY.LAW1']//following-sibling::a//img)[3]",
        )
    sel_utils.switch_to_window(browser, 1)
    youtube_text = sel_utils.get_text_by_xpath(browser, "//div[text()='Subscribe']", 10)
    assert youtube_text == "Subscribe", f"Actual:{youtube_text} Expected:'Subbscribe'"
    browser.close()
    sel_utils.switch_to_window(browser, 0)
    logger.info(f"Youtube Button verification successful")
