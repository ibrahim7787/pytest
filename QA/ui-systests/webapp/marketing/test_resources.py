import os
import sys
from utils import sel_utils
from utils.log_setup import getLogger
from helpers import resources
from helpers import resources
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

env = os.getenv('STAGE', 'dev')
sys.path.append(os.path.dirname(sys.path[0]))

logger = getLogger(__name__)


def test_resources(f_driver):
    browser = f_driver
    url = 'https://uatlms.techraq.com/'
    sel_utils.launch_url(browser, url)

    sel_utils.click_by_xpath(browser, "//button[normalize-space(text())='Allow cookies']")

    hover = browser.find_element(By.XPATH, "//p[@onclick='resources()']")
    action = ActionChains(browser)
    action.move_to_element(hover).perform()


    drop_down_resources=sel_utils.find_elements_by_xpath(browser,"(//div[@class='dropdown'])[3]//li")
    logger.info(f"drop_down_options = {len(drop_down_resources)}")
    assert drop_down_resources is not None
    dd_option = [element.text.strip() for element in drop_down_resources]
    assert (
        False if all(not x for x in dd_option) else True is True
    ), f"Dropdown Options for resouces is : {dd_option}. "
    sel_utils.click_by_xpath(browser, "//p[@onclick='resources()']")
    h5_elements = sel_utils.find_elements_by_xpath(browser, "//h5")
    cards_names = [element.text.strip() for element in h5_elements]
    logger.info(f"----Successfully validate dropdown options and cards, Both are same-----")


    # # Digital brochure


    card_count = sel_utils.find_elements_by_xpath(browser, "//div[@class='card']")
    logger.info(f"card count={len(card_count)}")
    for i in range(1, len(card_count) + 1):
        card_size = sel_utils.get_dimensions(browser, f"(//div[@class='card'])[{i}]")
        card_title = sel_utils.get_text_by_xpath(browser, f"(//div[@class='card'])[{i}]//h5")
        logger.info(f"card size of {card_title} is {card_size}")

    text_len_before = len(
        sel_utils.get_text_by_xpath(
            browser, "//h5[contains(text(),'DIGITAL BROCHURE ')]/..//following-sibling::p"
        )
    )
    logger.info(
        f"Length of text of DIGITAL BROCHURE before clicking on read more = {text_len_before}"
    )

    sel_utils.wait(3, "waiting to click on read more button in Digital brochure")
    browser.execute_script("window.scrollTo(0, 400);")
    sel_utils.wait(2,"to check scroll for digital")
    sel_utils.click_by_xpath(browser, "//button[@onclick='digitalRead()']")
    sel_utils.wait(3, "waiting to click on read more button in Digital brochure button")
    text_len_after = len(sel_utils.get_text_by_xpath(browser, "//span[@id='digitalMore']/.."))
    logger.info(f"Length of the text after clicking on read more is = {text_len_after}")
    browser.execute_script("window.scrollTo(0, 900);")

    download_link="//button[normalize-space(text())='Download']"
    resources.resources_cards_no_validation(browser,download_link,"Download")

    #INSIGHTS
    browser.execute_script("window.scrollTo(0, -200);")

    insight_leng = len(sel_utils.get_text_by_xpath(browser, "(//div[@class='card-body']//p)[2]"))
    logger.info(f"Length of text in Insights card : {insight_leng}")


    federal_business="//a[@href='https://www.ftc.gov/business-guidance/small-businesses']"
    nav_fed_business="//h1/span"
    resources.resources_cards(browser,federal_business,nav_fed_business,"Federal Trade Commission")

    nist_link="//a[@href='https://nist.gov/cyberframework']"
    nav_nist_link="//h1"
    resources.resources_cards(browser,nist_link,nav_nist_link,"NIST")

    browser.execute_script("window.scrollTo(0, 400);")

    nppd_link="//a[@href='https://dhs.gov/keywords/national-protection-and-programs-directorate-nppd']"
    nav_nppd_link="//h1//div"
    resources.resources_cards(browser,nppd_link,nav_nppd_link,"NPPD")

    # #MEDIA
    length_media=len(sel_utils.get_text_by_xpath(browser,"(//div[@class='card-body resource_equal'])[1]"))
    logger.info(f"Length of Media : {length_media}")
    sel_utils.browser_refresh(browser)
    browser.execute_script("window.scrollTo(0, 800);")
    sel_utils.wait(3,"to scroll")

    amazon_link="//a[normalize-space(text())='Amazon.']"
    nav_amzn="//span[contains(text(),'(Author)')]"
    resources.resources_cards(browser,amazon_link,nav_amzn,"Amazon")

    webseries_link="//a[@href=' https://play.vidyard.com/ZpKYow1tvYmE1SLTEQkJK8.html']"
    resources.resources_cards_no_validation(browser,webseries_link,"Webseries")

    media_link="//a[@href=' https://vimeo.com/931183132/0d7d26169e?share=copy']"
    nav_media="//h1"
    resources.resources_cards(browser,media_link,nav_media,"IASC webinar")

    #Comply.law Quarterly


    four_leng=len(sel_utils.get_text_by_xpath(browser,"//ul[@class='listoverride']"))
    logger.info(f"Length of Comply.law Quarterly : {four_leng}")

    claw_quarterly="//a[contains(text(),'Rise In Auto Dealership Cyberattacks')]"
    resources.resources_cards_no_validation(browser,claw_quarterly,"cyberattackers")
