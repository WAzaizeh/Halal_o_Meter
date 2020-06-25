'''Scraping restaurant list from my yelp collection'''

from selenium import webdriver as Webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os, sys
from dotenv import load_dotenv
import time, random
import pandas as pd

# add personal scripts to sys.path
modules_path = [os.path.abspath(os.path.join('.')+'/src/data/data_collection')] #, os.path.abspath(os.path.join('.')+'/web/pages')
for module in modules_path:
    if module not in sys.path:
        sys.path.append(module)
from database import Database
from review_scraper import _get_webdriver, _close_webdriver

def scrape_yelp_collection(collection_url):
    try:
        webdriver = _get_webdriver()
        webdriver.get(collection_url)

        account_name_xpath = '//a[@class="user-display-name js-analytics-click"]'
        account_name = WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, account_name_xpath))).text
        scrollable_pane_css = 'div.collection-content.collection-left-pane.u-inline-block'
        scrollable = WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, scrollable_pane_css)))
        _yelp_infinite_scroll(scrollable) # scroll to reveal all results
        rest_list = webdriver.find_elements_by_xpath('//li[@class="collection-item"]')

        df = pd.DataFrame(columns=['name', 'address', 'tags'])
        for rest in rest_list:
            name = rest.find_element_by_xpath('.//*/a[@class="biz-name js-analytics-click"]/span').text
            addr_city = rest.find_element_by_xpath('.//*/small/span[@class="addr-city"]').text
            tags_elements = rest.find_elements_by_xpath('.//*/span[@class="category-str-list"]/a')
            tags = [tag.text for tag in tags_elements]
            row = {'name' : name,
                    'address' : addr_city,
                    'tags' : tags}
            df = df.append(row, ignore_index=True)
        print("found {0} restaurants in {1}'s' Yelp collection list".format(len(rest_list), account_name))
        df.to_csv("/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_feature/wesam's_yelp_collection.csv", index=False)
    finally:
        _close_webdriver(webdriver)

def _yelp_infinite_scroll(element):
    element._parent.execute_script("""
        var element = arguments[0];
        function scroll(element) {
        element.scrollTo(0, element.scrollHeight);
        }

        var oldHeight = element.scrollHeight;
        for(var i = 0; i<100; i++) {
            setTimeout(scroll(element), 5000);
            await new Promise(resolve => setTimeout(resolve, 2000));
            if (element.scrollHeight > oldHeight) {
                oldHeight = element.scrollHeight;
            } else {
                i = 100;
            }
        }
        """, element)

def main():
    my_collection_url = 'https://www.yelp.com/collection/UciUoQ1AvCrJ8Hoo3rHZGg'
    scrape_yelp_collection(my_collection_url)

main()
