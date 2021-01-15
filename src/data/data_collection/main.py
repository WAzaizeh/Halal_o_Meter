'''
Data collection script. Gathers businesses from yelp and google API searches
then scrapes the pages of the search results from both platforms to get all
review texts that include the word 'Halal' in them.
'''

from database import Database
import multiprocessing
from Google_business_search import get_google_places_by_location
from Yelp_business_search import get_yelp_places_by_location
from review_scraper import scrape_yelp_reviews, scrape_google_reviews, _close_webdriver
import sys
from datetime import datetime


def get_businesses():
    try:
        # searching for businesses and updating database
        coordinates = _get_coordinates_list()
        timestamped_print('Searching around', '|'.join([coord[0] for coord in coordinates]))
        agents = 3
        chunksize = 10
        businesses_list = []
        # with multiprocessing.Pool(processes=agents) as pool:
        #     businesses_list.extend(pool.map(get_google_places_by_location, coordinates, chunksize))
        #     # businesses_list.extend(pool.map(get_yelp_places_by_location, coordinates, chunksize))
        #     pool.close()
        #     pool.join()
        ## -Chunk and call search functions multiple times:
        ## -Have lat,lng limitation where if more than 10% of results are outside locality then stop search
        ## and eliminate results from lat/lng +/- threshold
        _update_businesses(businesses_list)
    except KeyboardInterrupt:
        _update_businesses(businesses_list)
        raise
        sys.exit(0)

def _get_coordinates_list():
    db = Database()
    # fetch the list of NYC neighborhoods' coordinates for the search
    get_lat_lng = '''SELECT neighborhood, lat, lng
                        FROM coordinates'''
    results = db.select_rows(get_lat_lng)
    coordinates_list = [coord for coord in results]
    coordinates_list = [[coord[0].replace('+', ' '), ','.join([str(coord[1]),str(coord[2])])] for coord in results]
    return coordinates_list


def _update_businesses(businesses_list):
    db = Database()
    # update database with API search results
    business_sql = """INSERT INTO businesses (name, platform_id, url, total_review_count, address, image_url, lat, lng)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING"""
    db_list = [item for sublist in businesses_list for item in sublist]
    db.insert_rows(business_sql, *db_list)

    # final print with total number of businesses in the database at the end
    count_sql = '''SELECT count(*)
                    FROM businesses
                    WHERE url LIKE %s '''
    google_count = db.select_rows(count_sql, ('%google%', ))[0][0]
    yelp_count = db.select_rows(count_sql, ('%yelp%'))[0][0]
    timestamped_print('{} total businesses found'.format(len(db_list)))
    timestamped_print('Have {0} google businesses and {1} yelp businesses'.format(google_count, yelp_count))
    # print('Successfully found {} yelp businesses'.format(yelp_count))


def scrape_reviews():
    yelp_urls, google_urls = _get_unscraped_urls()
    # scrape reviews info
    agents = 3
    chunksize = 10
    reviews_list = []
    print('\n\n#####################################################################')
    print('{} yelp restaurants and {} Google restaurants left to scrape'.format(len(yelp_urls), len(google_urls)))
    try:
        with multiprocessing.Pool(processes=agents) as pool:
            reviews_list.extend(pool.starmap(scrape_yelp_reviews, yelp_urls, chunksize=chunksize))
            # reviews_list.extend(pool.starmap(scrape_google_reviews, google_urls[:2], chunksize))
            pool.close()
            pool.join()
        _update_reviews(reviews_list)
    except (KeyboardInterrupt, SystemExit):
        _update_reviews(reviews_list)
        raise
        sys.exit(0)


def _get_unscraped_urls():
    db = Database()
    # get list of google and yelp urls
    get_urls = '''SELECT url, platform_id
                    FROM businesses
                    WHERE url LIKE %s '''
    yelp_urls = db.select_rows(get_urls, ('%yelp%', ))
    google_urls = db.select_rows(get_urls, ('%google%', ))

    # exclude businesses that have already been scraped
    scraped_ids = db.select_rows('''SELECT DISTINCT ON (restaurant_id) restaurant_id FROM reviews''')
    exclusion_list = [item[0] for item in scraped_ids]
    yelp_urls_keep = [t for t in yelp_urls if t[1] not in exclusion_list]
    google_urls_keep = [t for t in google_urls if t[1] not in exclusion_list]
    return yelp_urls_keep, google_urls_keep


def _update_reviews(reviews_list):
    '''
        get a nested list of individual review data. Each entry includes:
        - restaurant id
        - username
        - rating
        - review text
        - review date
        - helpful count
    '''
    db = Database()
    # update database with business scraping results
    reviews_sql = """INSERT INTO reviews (restaurant_id, username, rating, review_text, date, helpful_count)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (review_text) DO NOTHING"""
    db_list = [item for sublist in reviews_list for item in sublist]
    db.insert_rows(reviews_sql, *db_list)
    # missing the summary print statement
    timestamped_print('{} reviews found'.format(len(db_list)))

def timestamped_print(*args, **kwargs):
  print(datetime.now(), *args, **kwargs)

if __name__ == '__main__':
    try:
        log_file = open('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/logs/Yelp_scrapping.log','a+')
        sys.stdout = log_file

        # get_businesses()
        scrape_reviews()

        log_file.close()
    finally:
        sys.stdout = sys.__stdout__
