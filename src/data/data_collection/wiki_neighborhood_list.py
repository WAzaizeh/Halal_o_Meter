'''Scraping a list of neighborhoods from wikipedia page
https://en.wikipedia.org/wiki/Neighborhoods_in_New_York_City
'''
from review_scraper import _get_webdriver, _close_webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import pandas as pd
from Google_business_search import get_corrdinates_from_name, get_name_from_coordinates
from database import Database

WIKI_URL = 'https://en.wikipedia.org/wiki/Neighborhoods_in_New_York_City'

def scrape_wiki_list(url):
    webdriver = _get_webdriver()
    webdriver.get(url)
    table_xpath = '//table[@class="wikitable sortable jquery-tablesorter"]'
    WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    rows = webdriver.find_elements_by_xpath(table_xpath + '/tbody/tr')
    neighborhood_table = pd.read_csv(os.getcwd()+'/NYC_neighborhood.csv', keep_default_na=False)

    # add borough name to neighborhood name and return as a flat list
    neighborhood_table = neighborhood_table.apply(lambda x: x+','+x.name)
    neighborhood_list = neighborhood_table.values.flatten()
    neighborhood_list = list(filter(lambda x: not x.startswith(','), neighborhood_list))
    neighborhood_list = [neighborhood.replace(' ','+') for neighborhood in neighborhood_list]

    # convert neighborhood_list to neighborhood_coordinates and update database
    db = Database()
    update_sql = """INSERT INTO coordinates (neighborhood, lat, lng)
                    VALUES (%s, %s, %s)"""
    for neighborhood in neighborhood_list:
        # print(neighborhood)
        lat, lng = get_corrdinates_from_name(neighborhood)
        db.insert_row(update_sql, *(neighborhood, lat, lng))

def confirm_neighborhoods():
    db = Database()
    neighborhoods = db.select_df('''SELECT * FROM coordinates''')
    neighborhoods['reversed_name'] = neighborhoods.apply(lambda row: get_name_from_coordinates(row.lat, row.lng), axis=1)
