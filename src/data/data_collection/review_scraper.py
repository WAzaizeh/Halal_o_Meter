# Scrape relevant reviews from a business webpage
# using Selenium


from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from database import Database
import os
from dotenv import load_dotenv
import time, random

def scrape_google_reviews(google_url, google_id):
    reviews_list = []
    try:
        webdriver = _get_webdriver()
        webdriver.get(google_url)
        _search_google_halal_review(webdriver) # a function that will carry the search and infinite scroll
        reviews_list = _scrape_google_reviews_text(webdriver) # a function that will retreive the list of reviews after clicking all the 'more'
        print('Scraped {0} reviews from google business id #{1}'.format(len(reviews_list), google_id))
    finally:
        _close_webdriver(webdriver)
    return reviews_list

    # # for testing compare count of added rows
    # final_row_num = db.select_rows('''SELECT COUNT(*) FROM reviews''')
    # print(final_row_num, start_row_num)


def scrape_yelp_reviews(yelp_url, yelp_id):
    webdriver = _get_webdriver()
    # get business url with halal-relevant reviews only
    webdriver.get(yelp_url + '&q=halal')
    review_num = _get_yelp_reviews_num(webdriver) # the total number of halal-relevant reviews to be scraped

    reviews_list = []
    if review_num > 0 :
        for i in range(1 ,int(review_num / 20) + (review_num % 20 > 0)):
            # get list of reviews text and dates and append to database
            reviews_list.extend(_scrape_yelp_reviews_text(webdriver, yelp_id))
            # call next page
            webdriver.get(yelp_url  + '&q=halal' + '&start='+str(i*20))
            time.sleep(random.randint(2,5))
        # scrape last page
        reviews_list.extend(_scrape_yelp_reviews_text(webdriver, yelp_id))
        print('Scraped {0} reviews from yelp business id {1}'.format(len(reviews_list), yelp_id))
    else:
        reviews_list = [[yelp_id, '', '', NULL, '', 0]] # review text is set to NULL to escape SQL insert ON CONFLICT based on review_text
        print('No reviews to scrape from yelp business id {1}'.format(len(reviews_list), yelp_id))

    _close_webdriver(webdriver)
    return reviews_list

def _get_webdriver():
    load_dotenv()
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
    options = ChromeOptions()
    # will need more configuration when deployed
    # options.add_experimental_option("detach", True) # uncomment for experimentation
    options.add_argument('--headless') # comment for experimentation
    options.add_argument("--incognito")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions") # to overcome _scroll_into_view failure in headless mode
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    return webdriver


def _close_webdriver(webdriver):
    webdriver.close()
    webdriver.quit()


def _infinite_scroll(element):
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


def _scroll_into_view(element):
    element._parent.execute_script("arguments[0].scrollIntoView(false)", element)


def _open_review_search_input(webdriver):
    # spcific javascript to click the button that's not accessible from selenium
    try:
        ## using Selenium
        # open_search_button_xpath = '//button[@aria-label="Search reviews"]'
        open_search_button_css = ' div.kt69ovbk911__expand-button.section-expandable-text-input-expand-button-container > div > div > button'
        WebDriverWait(webdriver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, open_search_button_css)))
    except TimeoutException:
        ## using javascript
        webdriver.execute_script("var button=document.body.getElementsByClassName('iRxY3GoUYUY__button gm2-hairline-border section-action-chip-button')[17]; button.click();")



def _search_google_halal_review(webdriver):
    # click button to open search input field
    open_search_button_xpath = '//button[@aria-label="Search reviews"]'
    # scroll to bring review search into focus
    try:
        WebDriverWait(webdriver, 5).until(EC.presence_of_element_located((By.XPATH, open_search_button_xpath)))
    except TimeoutException: # try again. Sometimes the script cannot find the button the first time around
        WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, open_search_button_xpath)))
    open_search_input = webdriver.find_element_by_xpath(open_search_button_xpath)
    _scroll_into_view(open_search_input)
    time.sleep(random.randint(3, 15))
    _open_review_search_input(webdriver)

    # insert 'halal' then RETURN
    search_input_xpath = '//input[@aria-label="Search reviews"]'
    try:
        WebDriverWait(webdriver, 3).until(EC.visibility_of_element_located((By.XPATH, search_input_xpath)))
    except TimeoutException:
        WebDriverWait(webdriver, 3).until(EC.visibility_of_element_located((By.XPATH, search_input_xpath)))
    search_input = webdriver.find_element_by_xpath(search_input_xpath)
    search_input.send_keys('Halal')
    search_input.send_keys(Keys.RETURN)

    # scroll to show all reviews
    scrollable_pane_css = '#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
    WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, scrollable_pane_css)))
    scrollable = webdriver.find_element_by_css_selector(scrollable_pane_css)
    _infinite_scroll(scrollable)

    # load all reviews' text by clicking all 'More' buttons
    try:
        more_button_xpath = '//button[@class="section-expand-review blue-link"]'
        buttons = webdriver.find_elements_by_xpath(more_button_xpath)
        for button in buttons:
            button.click()
    except:
        pass


def _scrape_google_reviews_text(webdriver):
    reviews_text_xpath = '//span[@class="section-review-text"]'
    reviews_dates_xpath = '//span[@class = "section-review-publish-date"]'
    reviews_rating_xpath = '//span[@class="section-review-stars"]'
    reviews_username_xpath = '//div[@class="section-review-title"]/span'
    reviews_helpful_xpath = '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/thumb_up_black_18dp.png"]//following-sibling::span/span[2]'
    reviews_texts = webdriver.find_elements_by_xpath(reviews_text_xpath)
    reviews_dates = webdriver.find_elements_by_xpath(reviews_dates_xpath)
    reviews_ratings = webdriver.find_elements_by_xpath(reviews_rating_xpath)
    reviews_usernames = webdriver.find_elements_by_xpath(reviews_username_xpath)
    reviews_helpful_count = webdriver.find_elements_by_xpath(reviews_helpful_xpath)
    reviews_list = []
    for review, review_date, review_rating, review_usr, review_help in zip(reviews_texts, reviews_dates, reviews_ratings, reviews_usernames, reviews_helpful_count):
        text = review.text
        date = review_date.text
        rating = review_rating.get_attribute('aria-label')
        username = review_usr.text
        help_count = review_help.text + ' likes'
        reviews_list.append([username, rating, text, date, help_count])
    return reviews_list


def _get_yelp_reviews_num(webdriver):
    review_num_xpath = '//span[contains(text(), " mentioning")]'
    WebDriverWait(webdriver, 20).until(EC.visibility_of_element_located((By.XPATH, review_num_xpath)))
    review_num_str = webdriver.find_element_by_xpath(review_num_xpath).text
    # returns 0 when no reviews are found
    return int(review_num_str.split()[0])


def _scrape_yelp_reviews_text(webdriver, yelp_id):
    reviews_text_xpath = '//span[@lang="en"]'
    reviews_dates_xpath = '//span[contains(text(), "/")]'
    reviews_rating_xpath = '//li/div/div//div[contains(@aria-label, "star rating") and starts-with(@class, " i-stars__373c0__1T6rz i-stars--regular")]'
    reviews_username_xpath = '//div[@role = "region"]//span/a[contains(@href, "user_details?userid")]'
    reviews_helpful_xpath = '//span[contains(text(), "Useful")]'

    reviews_texts = webdriver.find_elements_by_xpath(reviews_text_xpath)
    reviews_dates = webdriver.find_elements_by_xpath(reviews_dates_xpath)
    reviews_ratings = webdriver.find_elements_by_xpath(reviews_rating_xpath)
    reviews_usernames = webdriver.find_elements_by_xpath(reviews_username_xpath)
    reviews_helpful_count = webdriver.find_elements_by_xpath(reviews_helpful_xpath)
    reviews_list = []
    for review, review_date, review_rating, review_usr, review_help in zip(reviews_texts, reviews_dates, reviews_ratings, reviews_usernames, reviews_helpful_count):
        text = review.text
        date = review_date.text
        rating = review_rating.get_attribute('aria-label')
        username = review_usr.text
        try:
            helpful_count = int(review_help.find_element_by_xpath('.//span').text.split()[0]) # take only the number and convert to ineteger
        except:
            helpful_count = 0
        reviews_list.append([yelp_id, username, rating, text, date, helpful_count])
    return reviews_list
