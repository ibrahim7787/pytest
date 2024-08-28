from utils import sel_utils
from utils.log_setup import getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


logger = getLogger(__name__)


def test_what_we_offer(f_driver):
    browser = f_driver
    sel_utils.launch_url(browser)
    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")

    hover = browser.find_element(By.XPATH, "//p[@onclick='whatweoffer()']")
    action = ActionChains(browser)
    action.move_to_element(hover).perform()

    drop_down_options = sel_utils.find_elements_by_xpath(
        browser, "(//div[@class='dropdown'])[1]//li"
    )
    logger.info(f"drop_down_options = {len(drop_down_options)}")
    assert drop_down_options is not None
    dd_options = [element.text.strip() for element in drop_down_options]
    assert (
        False if all(not x for x in dd_options) else True is True
    ), f"Dropdown Options for what_we_offer is {dd_options}. "
    sel_utils.click_by_xpath(browser, "//p[@onclick='whatweoffer()']")
    h5_elements = sel_utils.find_elements_by_xpath(browser, "//h5")
    cards_names = [element.text.strip() for element in h5_elements]
    card_contents = {}

    def validate_cards(card_name, card_contents, readmore=True):
        scrollht = 700
        if not readmore:
            scrollht = 900
        text_len_before = len(
            sel_utils.get_text_by_xpath(
                browser, f"//h5[contains(text(),'{card_name}')]//following-sibling::p"
            )
        )
        logger.info(
            f"Length of text before clicking on read more in {card_name}= {text_len_before}"
        )
        readmore_flg = True
        # FIXME: Read more button should be clicked only if it exists. else move on.
        if card_name in ["OSHA", "Human Resources"]:
            scrollht += 700

        browser.execute_script(f"window.scrollTo(0,{scrollht});")

        sel_utils.wait(1, f" After page down and before Read More link.")
        try:
            sel_utils.click_by_xpath(
                browser, f"//h5[contains(text(),'{card_name}')]//following-sibling::button", 5
            )
            sel_utils.wait(2, f" After Read More link to get updated content.")
        except:
            logger.info(f"No Read more link for {card_name}")
            readmore_flg = False

        text_len_after = len(
            sel_utils.get_text_by_xpath(
                browser, f"//h5[contains(text(),'{card_name}')]//following-sibling::p"
            )
        )
        logger.info(f"Length of text after clicking on read more in {card_name}= {text_len_after}")
        if readmore_flg:
            assert (
                text_len_before < text_len_after
            ), f"Expected: Before Read more {text_len_before} < After Readmore {text_len_after}"
        else:
            assert (
                text_len_before == text_len_after
            ), f"Expected: Before Read more {text_len_before} = After Readmore {text_len_after}"
        if readmore:
            card_contents[card_name] = [text_len_before, text_len_after]

        if not readmore:
            assert card_contents[card_name][0] == text_len_after

    for card in cards_names:
        logger.info(f"working on card: {card}")
        assert card in dd_options, f"{card} is not present in {dd_options}"
        validate_cards(card, card_contents, readmore=True)

    # for card in cards_names:
    #     logger.info(f"working on card: {card}")
    #     assert card in dd_options, f"{card} is not present in {dd_options}"
    #     validate_cards(card, card_contents, readmore=False)
    # {"OSHA": [100, 200], "Human resources": [200, 300], ...}
    logger.info("Successfully validated all Card contents")
