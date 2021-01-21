from storage_managers.database import Database
from search_and_scrape.review_scraper import scrape_yelp_reviews, scrape_google_reviews
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_reviews(yelp=True, google=True):
    yelp_urls, google_urls = _get_unscraped_urls()
    # scrape reviews info
    threads_max = 3
    chunk_size = 50
    reviews_list = []
    print('\n#####################################################################')
    timestamped_print('{} yelp restaurants and {} Google restaurants left to scrape'.format(len(yelp_urls), len(google_urls)))

    try:
        with ThreadPoolExecutor(max_workers=threads_max) as executor:
            if yelp:
                for i in range(0, len(yelp_urls), chunk_size):
                    futures = [executor.submit(scrape_yelp_reviews, *params) for params in yelp_urls[i : i+n]]
                    for future in as_completed(futures):
                        reviews_list.append(future.result())
            if google:
                for i in range(0, len(google_urls), chunk_size):
                    futures = [executor.submit(scrape_google_reviews, *params) for params in google_urls[i : i+n]]
                    for future in as_completed(futures):
                        reviews_list.append(future.result())
    finally:
        _update_reviews(reviews_list=reviews_list)


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
        - restaurant id, username, rating, review text, review date, helpful count
        Restaurants without reviews get an empty entry with platform_id only
    '''
    db = Database()
    # update database with reviews scraping results
    reviews_sql = """INSERT INTO reviews (restaurant_id, username, rating, review_text, date, helpful_count)
                    VALUES (%s, %s, %s, %s, %s, %s )
                    ON CONFLICT (review_text) DO NOTHING"""
    db_list = [item for sublist in reviews_list for item in sublist]
    db.insert_rows(reviews_sql, *db_list)

    #print summary statement
    timestamped_print('Attempted to insert {} reviews'.format(len(db_list)))

def timestamped_print(*args, **kwargs):
  print(datetime.now(), *args, **kwargs)
