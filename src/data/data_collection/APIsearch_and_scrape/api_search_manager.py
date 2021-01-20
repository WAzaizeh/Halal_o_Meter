from database import Database
from Google_business_search import get_google_places_by_location
from Yelp_business_search import get_yelp_places_by_location
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_businesses(yelp=True, google=True):
    coordinates = _get_coordinates_list()
    threads_max = 3
    businesses_list = []
    print('\n#####################################################################')
    timestamped_print('Starting search for restaurants in {}'.format('Yelp & Google' if yelp and google else 'Yelp' if yelp else 'Google'))
    try:
        with ThreadPoolExecutor(max_workers=threads_max) as executor:
            if yelp:
                futures = [executor.submit(get_yelp_places_by_location, *params) for params in coordinates]
                for future in as_completed(futures):
                    businesses_list.append(future.result())
            if google:
                futures = [executor.submit(get_google_places_by_location, *params) for params in coordinates]
                for future in as_completed(futures):
                    businesses_list.append(future.result())
        _update_businesses(businesses_list=businesses_list)

    except (KeyboardInterrupt, SystemExit):
        _update_businesses(businesses_list=businesses_list)
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


def timestamped_print(*args, **kwargs):
  print(datetime.now(), *args, **kwargs)
