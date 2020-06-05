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
from review_scraper import


if __name__ == "__main__":
    get_businesses()
    scrape_reviews()


def get_businesses():
    # fetch the list of NYC neighborhoods' coordinates for the search
    db = Database()
    get_lat_lng_list = '''SELECT lat, lng
                        FROM coordinates'''
    results = db.select_rows(get_lat_lng_list)
    coordinates_list = [coord for coord in results]
    coordinates = [','.join(map(str, coordinates)) for coordinates in coordinates_list]

    # searching for businesses and updating database
    with multiprocessing.Pool(processes=3) as pool:
        pool.map_async(get_google_places_by_location, coordinates)
        pool.map_async(get_yelp_places_by_location, coordinates)
        pool.close()
        pool.join()

    count_sql = '''SELECT count(*)
                    FROM businesses
                    WHERE url LIKE %s '''
    google_count = db.select_rows(count_sql, ('%google%', ))[0][0]
    yelp_count = db.select_rows(count_sql, ('%yelp%'))[0][0]
    print('Successfully found {0} google businesses and {1} yelp businesses'.format(google_count, yelp_count))


def scrape_reviews():
    # get list of google and yelp urls
    db = Database()
    get_urls = '''SELECT url, platform_id
                    FROM businesses
                    WHERE url LIKE %s '''
    yelp_urls = db.select_rows(get_urls, ('%yelp%', ))
    # google_urls = db.select_rows(get_urls, ('%google%', ))

    # scrape reviews info
    with multiprocessing.Pool(processes=3) as pool:
        pool.map_async(scrape_yelp_reviews, yelp_urls)
        # pool.map_async(scrape_google_reviews, google_urls)
        pool.close()
        pool.join()
