import requests
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#scrolls to bottom of driver's page
def scroll_to_bottom(driver):
    print("Scrolling to bottom of page to load items...")
    # scroll to bottom of page to load all images
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     break
        try:
            print("waiting for button to load...")
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > section > div:nth-child(4) > an-root > ansrp-dtansearchresultspagelib > srp-root > div > div > an-search > div.ng-star-inserted > div.d-flex.row.filter-results-container > div.resultsCol.col.m-0 > div.col-12.px-0.resultsSRP > div:nth-child(2) > button"))
            )
            print("found the button!")
            break
        except:
            break
        last_height = new_height

# checks if there is a load more button, returns true if there is
def can_load_more(driver):
    # if it can not load more items, the text reads "Displaying n Results of n" and there is no button
    # if it CAN load more, text reads "Displaying n Results of m" and there is button with text "Load next x"
    button = driver.find_element_by_css_selector("body > section > div:nth-child(4) > an-root > ansrp-dtansearchresultspagelib > srp-root > div > div > an-search > div.ng-star-inserted > div.d-flex.row.filter-results-container > div.resultsCol.col.m-0 > div.col-12.px-0.resultsSRP > div:nth-child(2) > button")
    if button.is_displayed():
        button.click()
        return True

    return False



if __name__ == '__main__':
    # 1 open selenium
    homepg = "https://www.autonation.com/cars-for-sale?cnd=USED%7CCPO&dst=-1&pagesize=72"
    # File path to chromedriver.exe
    PATH = "./chromedriver.exe"

    # driver options
    options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_experimental_option("prefs", prefs)

    # create driver & open
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(homepg)  # open selenium driver to homepg
    time.sleep(10)
    # 2 scroll to bottom
    scroll_to_bottom(driver)
    time.sleep(10)

    while can_load_more(driver):
        # time.sleep(10)
        scroll_to_bottom(driver)
        # time.sleep(10)

    # driver.close()
    print("done")

# TODO: Bug: Scrolling to the bottom to load all vehicles leads to memory issue taking >10 min to load a page.
# TODO: Get the vehicle data
