'''
Data collection script. Gathers businesses from yelp and google API searches
then scrapes the pages of the search results from both platforms to get all
review texts that include the word 'Halal' in them.
'''

from database import Database
import multiprocessing
from Google_business_search import get_google_places_by_location
from Yelp_business_search import get_yelp_places_by_location
from review_scraper import scrape_yelp_reviews, scrape_google_reviews


def get_businesses():
    # fetch the list of NYC neighborhoods' coordinates for the search
    db = Database()
    get_lat_lng_list = '''SELECT lat, lng
                        FROM coordinates'''
    results = db.select_rows(get_lat_lng_list)
    coordinates_list = [coord for coord in results]
    coordinates = [','.join(map(str, coordinates)) for coordinates in coordinates_list]
    # adjust to only what haven't gotten called bc of network outage
    last_call = '34.9843176,-80.4492319'
    last_call_index = coordinates.index(last_call)

    # searching for businesses and updating database
    agents = 3
    chunksize = 10
    with multiprocessing.Pool(processes=agents) as pool:
        # pool.map_async(get_google_places_by_location, coordinates)
        pool.map(get_yelp_places_by_location, coordinates[last_call_index+1:], chunksize)
        pool.close()
        pool.join()

    count_sql = '''SELECT count(*)
                    FROM businesses
                    WHERE url LIKE %s '''
    # google_count = db.select_rows(count_sql, ('%google%', ))[0][0]
    yelp_count = db.select_rows(count_sql, ('%yelp%'))[0][0]
    # print('Successfully found {0} google businesses and {1} yelp businesses'.format(google_count, yelp_count))
    print('Successfully found {} yelp businesses'.format(yelp_count))

def scrape_reviews():
    # get list of google and yelp urls
    db = Database()
    get_urls = '''SELECT url, platform_id
                    FROM businesses
                    WHERE url LIKE %s '''
    yelp_urls = db.select_rows(get_urls, ('%yelp%', ))
    # google_urls = db.select_rows(get_urls, ('%google%', ))

    # exclude businesses that have already been scraped
    scraped_ids = db.select_rows('''SELECT DISTINCT ON (restaurant_id) restaurant_id FROM reviews''')
    exclusion_list = [item[0] for item in scraped_ids]
    yelp_urls_keep = [t for t in yelp_urls if t[1] not in exclusion_list]

    # scrape reviews info
    agents = 3
    chunksize = 10
    with multiprocessing.Pool(processes=agents) as pool:
        pool.starmap(scrape_yelp_reviews, yelp_urls_keep, chunksize)
        # pool.map_async(scrape_google_reviews, google_urls)
        pool.close()
        pool.join()

if __name__ == "__main__":
    # get_businesses()
    scrape_reviews()
