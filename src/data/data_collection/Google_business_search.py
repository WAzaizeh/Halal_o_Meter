# Get a set of business names
# by querying Google Places API according to
# a location, type of business, and search term.

import requests, json, time
#import database_func as db
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv('GOOGLE_API_KEY_2')

def get_corrdinates_from_name(location_name):
    URL = ('https://maps.googleapis.com/maps/api/geocode/json?address='
    + location_name + 'components=country:US&key=' + API_key)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    results = json_obj["results"]
    for result in results:
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
    return [lat, lng]

def get_google_place_url_and_review_count(place_id):
    URL = ('https://maps.googleapis.com/maps/api/place/details/json?placeid='
    +place_id+'&key='+API_key)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    place_details = json_obj["result"]
    google_url = place_details['url']
    try:
        review_count = place_details['user_ratings_total']
    except:
        review_count = 0
    return google_url, review_count


def get_google_places_by_location(coordinates, business_type='restaurant', search_term='halal', radius = '16093', next_page=''):
    URL = ('https://maps.googleapis.com/maps/api/place/textsearch/json?location='
    	+ coordinates + '&radius=' + radius + 'query=' + search_term + '&type='
    	+ business_type + '&pagetoken=' + next_page + '&key='+ API_key)
    response = requests.get(URL)
    json_obj = json.loads(response.text)
    results = json_obj["results"]

    # # SQL query to add business to table
    # db = Database()
    # update_sql = """INSERT INTO businesses (name, platform_id, url, total_review_count, address)
    #                 VALUES (%s, %s, %s, %s, %s)
    #                 ON CONFLICT (url) DO NOTHING"""
    businesses_list = []
    for result in results:
        name = result['name']
        google_id = result['place_id']
        google_url , review_count = get_google_place_url_and_review_count(google_id)
        address = result['formatted_address']
        businesses_list.append([name, google_id, google_url, review_count, address])
        # db.insert_row( update_sql, *(name, google_id, google_url, review_count, address))
    try:
        next_page_token = json_obj["next_page_token"]
    except:
        #no next page
        print('Found {} businesses near coordinates {}'.format(len(businesses_list), coordinates))
        return businesses_list
    time.sleep(1)
    data = get_google_places_by_location(coordinates=coordinates, next_page=next_page_token)
    businesses_list.extend(data)
    return businesses_list
