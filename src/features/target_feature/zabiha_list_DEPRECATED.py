''' A script to scrape a list of 744 confirmed Halal restaurants in
  NYC area from Zabiha.com
  As well as, requesting 338 halal tagged restaurants in NYC from Zomato.com
'''

import review_scraper
import pandas as pd
import os, requests, json
from dotenv import load_dotenv


def _zabiha_to_csv(url_dict):

    webdriver = review_scraper._get_webdriver()

    res_names_xpath = '//div[@class="titleBS"]'
    res_address_xpath = '//div[@class="titleBS"]/../div[@class="tinyLink"]'
    df = pd.DataFrame(columns=['name', 'address', 'borough'])

    for key in url_dict:
        print('scraping {} results from Zabiha.com'.format(key))
        webdriver.get(url_dict[key])
        names = webdriver.find_elements_by_xpath(res_names_xpath)
        addresses = webdriver.find_elements_by_xpath(res_address_xpath)
        for name, address in zip(names, addresses):
            row = {'name' : name.text,
                    'address' : address.text,
                    'borough' : key,
                    'source' : 'Zabiha'}
            df = df.append(row, ignore_index=True)
    review_scraper._close_webdriver(webdriver)
    df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv', mode='a', index=False)
    print('\n{} rows added from Zabiha\n'.format(df.shape[0]))

def _zomato_to_csv(city_id):
    load_dotenv()
    API_KEY = os.getenv('ZOMATO_API_KEY')
    offset = 0
    url = 'https://developers.zomato.com/api/v2.1/search?entity_id='\
    + str(city_id) + '&entity_type=city&q=halal&start=' + str(offset)
    headers = {'user-key': '488f11265c3bf28f5d563dfd98697ad2'}
    r = requests.request("GET", url, headers=headers)
    response = r.text
    json_obj = json.loads(response)

    # get total number of results
    offset_max = json_obj['results_found']
    print('Found {} results in Zomato.com'.format(offset_max))

    df = pd.DataFrame(columns=['name', 'address', 'borough'])
    while offset < offset_max:
        # request next page
        r = requests.request("GET", url, headers=headers)
        response = r.text
        json_obj = json.loads(response)
        # get info and append to dataframe
        for restaurant in json_obj['restaurants']:
            restaurant = restaurant['restaurant']
            row = {'name' : restaurant['name'],
                    'address' : restaurant['location']['address'],
                    'borough' : restaurant['location']['city'],
                    'source' : 'Zomato'}
            df = df.append(row, ignore_index=True)
        # advance offset
        print('Progress: {0}/{1}'.format(offset+20, offset_max), end='\r', flush=True)
        offset += 20
    df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv', mode='a', index=False)
    print('\n{} rows added from Zomato\n'.format(df.shape[0]))


if __name__ == "__main__":
    borough_urls = {'Manhattan' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Manhattan/NEwhtS6OzN',
                            'Brooklyn' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Brooklyn/3avrh3Cth4',
                            'Queens' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Queens/9Gku594eh7',
                            'The Bronx' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/The-Bronx/eIqsntUUuI',
                            'Staten Island' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Staten-Island/84zPaAaBZd'}
    _zabiha_to_csv(borough_urls)
    _zomato_to_csv(280) # city_id for NYC from Zomato cities API
