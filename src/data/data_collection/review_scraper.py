# Scrape relevant reviews from a business webpage
# using Selenium


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
    _search_google_halal_review(webdriver) # a function that will carry the search and infinite scroll
    data = _scrape_google_halal_reviews(webdriver) # a function that will retreive the list of reviews after clicking all the 'more'
    _close_webdriver(webdriver)
    return data


def scrape_yelp_reviews(yelp_url):
    webdriver = _get_webdriver()
    # get business url with halal-relevant reviews only
    webdriver.get(yelp_url + '&q=halal')
    review_num = _get_yelp_reviews_num(webdriver) # a function that will return number of reviews
    data = []
    for i in range(1 ,int(review_num / 20) + (review_num % 20 > 0)):
        data.extend(_scrape_yelp_halal_reviews(webdriver))
        webdriver.get(yelp_url + '&start='+str(i*20) + '&q=halal')
    data.extend(_scrape_yelp_halal_reviews(webdriver))
    _close_webdriver(webdriver)
    return data

def _get_webdriver():
    chromedriver_path = '/Users/wesamazaizeh/Desktop/Projects/Chrome_driver/chromedriver_83'
    options = ChromeOptions()
    # will need more configuration when deployed
    options.add_argument('headless')
    options.add_argument('--disable-infobars --disable-extensions')
    webdriver = Webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
    return webdriver


def _close_webdriver(webdriver):
    webdriver.close()


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

def _search_google_halal_review(webdriver):
    # click button to open search input field
    open_search_button_xpath = '//button[@aria-label="Search reviews"]'
    # scroll to bring review seatch into focus
    WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, open_search_button_xpath)))
    open_search_input = webdriver.find_element_by_xpath(open_search_button_xpath)
    _scroll_into_view(open_search_input)
    time.sleep(2)
    open_search_input.click()

    # insert input then RETURN
    search_input_xpath = '//input[@aria-label="Search reviews"]'
    WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, search_input_xpath)))
    search_input = webdriver.find_element_by_xpath(search_input_xpath)
    search_input.send_keys('Halal')
    search_input.send_keys(Keys.RETURN)

    ##  add error handling
    # except NoSuchElementException:
    #     return('Failed to open search input field')

    # scroll to show all reviews
    scrollable_pane_css = '#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
    WebDriverWait(webdriver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, scrollable_pane_css)))
    scrollable = webdriver.find_element_by_css_selector(scrollable_pane_css)
    _infinite_scroll(scrollable)


def _scrape_google_halal_reviews(webdriver):
    reviews_xpath = '//span[@class="section-review-text"]'
    reviews = webdriver.find_elements_by_xpath(reviews_xpath)
    reviews_list = []
    for review in reviews:
        text = review.text
        reviews_list.append(text)
        # append to database instead
    return reviews_list


def _get_yelp_reviews_num(webdriver):
    review_num_xpath = '//span[contains(text(), "reviews mentioning")]'
    WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.XPATH, review_num_xpath)))
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
    return reviews_list
        # append to database instead
