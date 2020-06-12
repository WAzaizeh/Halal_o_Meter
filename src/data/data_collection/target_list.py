''' A script to scrape a list of 744 confirmed Halal restaurants in
  NYC area from Zabiha.com
'''

import review_scraper
import pandas as pd


def target_to_csv(url_dict):

    webdriver = review_scraper._get_webdriver()

    res_names_xpath = '//div[@class="titleBS"]'
    res_address_xpath = '//div[@class="titleBS"]/../div[@class="tinyLink"]'
    df = pd.DataFrame(columns=['restaurant_name', 'restaurant_address', 'borough'])

    for key in url_dict:
        webdriver.get(url_dict[key])
        names = webdriver.find_elements_by_xpath(res_names_xpath)
        addresses = webdriver.find_elements_by_xpath(res_address_xpath)
        for name, address in zip(names, addresses):
            row = {'restaurant_name' : name.text,
                    'restaurant_address' : address.text,
                    'borough' : key}
            df = df.append(row, ignore_index=True)
    review_scraper._close_webdriver(webdriver)
    df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv', index=False)


if __name__ == "__main__":
    borough_urls = {'Manhattan' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Manhattan/NEwhtS6OzN',
                            'Brooklyn' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Brooklyn/3avrh3Cth4',
                            'Queens' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Queens/9Gku594eh7',
                            'The Bronx' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/The-Bronx/eIqsntUUuI',
                            'Staten Island' : 'https://www.zabihah.com/sub/United-States/New-York/New-York-City/Staten-Island/84zPaAaBZd'}
    target_to_csv(borough_urls)
