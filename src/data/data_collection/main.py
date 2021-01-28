'''
Data collection script. Gathers businesses from yelp and google API searches
then scrapes the pages of the search results from both platforms to get all
review texts that include the word 'Halal' in them.
'''

import sys
from search_and_scrape.scraping_manager import scrape_reviews
from search_and_scrape.api_search_manager import get_businesses

if __name__ == '__main__':
    try:
        log_file = open('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/logs/data_collection.log','a+')
        sys.stdout = log_file

        # get_businesses()
        scrape_reviews(yelp=False)

        log_file.close()
    finally:
        sys.stdout = sys.__stdout__
