# Scrape relevant reviews from a business webpage
# using Selenium


'''
Scraping Google Reviews
Steps
1. open google maps page of business (from database)
2. click review search button (xpath = //button[@aria-label="Search reviews"])
3. find review search input (xpath = //input[@aria-label="Search reviews"]), use explicit wait
4. insert 'halal'
5. insert Key.Return
6. figure out how to scrol to show all results
7. scrape all reviews and save to DB


Scrape Yelp reviews
Steps
1. open yelp business url (from database)
2. find "search within reviews input" (xpath = //input[@name="query"])
3. insert 'halal'
4. insert Keys.Return
5. scrape reviews ( xpath = //span[@lang="en"]) -> nested in multiple 'span'
6. go to next page by clicking '>'
'''

from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def scrape_google_reviews(google_url):
    webdriver = _get_webdriver()
    webdriver.get(google_url)
    _search_google_halal_review(webdriver) # a function that will carry the search and infinity scroll
    data = _scrape_google_halal_reviews(webdriver) # a function that will retreive the list of reviews after clicking all the 'more'
    _close_webdriver(webdriver)


def scrape_yelp_reviews(yelp_url):
    webdriver = _get_webdriver()
    # get business url with halal-relevant reviews only
    webdriver.get(yelp_url + '&q=halal')
    review_num = _search_yelp_halal_reviews(webdriver) # a function that will return number of reviews
    for i in range(1 ,int(review_num / 20) + (review_num % 20 > 0))
        data = _scrape_yelp_halal_reviews(webdriver)
        webdriver.get(yelp_url + '&start='+str(i*20) + '&q=halal')
    _close_webdriver(webdriver)


def _get_webdriver():
    chromedriver_path = Constants.CHROME_DRIVER_PATH
    opts = ChromeOptions()
    # will need more configuration when deployed
    options.add_argument('headless')
    options.add_argument('--disable-infobars --disable-extensions')
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    return webdriver


def _close_webdriver(webdriver):
    webdriver.close()


def _infinity_scroll(element):
    element._parent.execute_script("""
        var element = arguments[0];
        var oldHeight = element.scrollHeight;
        for(var i = 0; i<100; i++) {
            element.scrollTo(0, element.scrollHeight);
            await new Promise(resolve => setTimeout(resolve, 2000));
            if (element.scrollHeight > oldHeight) {
                oldHeight = element.scrollHeight;
            } else {
                i = 100;
            }
        }
        """, element)


def _search_google_halal_review(webdriver):
    # click button to open search input field
    open_search_button_xpath = '//button[@aria-label="Search reviews"]'
    WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.XPATH, open_search_button_xpath)))
    webdriver.find_element_by_xpath(open_search_button_xpath).click()

    # insert input then RETURN
    search_input_xpath = '//input[@aria-label="Search reviews"]'
    WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.XAPTH, search_input_xpath)))
    search_input = webdriver.find_element_by_xpath(search_input_xpath)
    search_input.send_keys('Halal')
    search_input.send_keys(Keys.RETURN)

    ##  add error handling
    # except NoSuchElementException:
    #     return('Failed to open search input field')

    # scroll to show all reviews
    scrollable_pane_css = '#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
    WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located(BY.CSS_SELECTOR, scrollable_pane_css))
    scrollable = driver.find_element_by_css_selector(scrollable_pane_css)
    scroll_element(scrollable)


def _scrape_google_halal_reviews(webdriver):
    reviews_xpath = '//span[@class="section-review-text"]'
    reviews = webdriver.find_elements_by_xpath(reviews_xpath)
    reviews_list = []
    for review in reviews:
        text = review.text
        reviews_list.append(text)
        # append to database instead


def _search_yelp_halal_reviews(webdriver):
    review_num_xpath = '//span[contains(text(), "reviews mentioning")]'
    review_num_str = webdriver.find_element_by_xpath(review_num_xpath).text
    # returns 0 when no reviews are found
    return int(review_num_str.split()[0])


def _scrape_yelp_halal_reviews(webdriver):
    reviews_xpath = '//span[@lang="en"]'
    reviews = webdriver.find_elements_by_xpath(reviews_xpath)
    reviews_list = []
    for review in reviews:
        text = review.text
        reviews_list.append(text)
        # append to database instead
