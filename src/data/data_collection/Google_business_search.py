# Get a set of business names
# by querying Google Places API according to
# a location, type of business, and search term.

import requests, json, time
#import database_func as db
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv('GOOGLE_API_KEY')

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
    url = ('https://maps.googleapis.com/maps/api/place/details/json?placeid='
    +place_id+'&key='+API_key)
    r = requests.get(url)
    response = r.text
    json_obj = json.loads(response)
    place_details = json_obj["result"]
    google_url = place_details['url']
    try:
        review_count = place_details['user_ratings_total']
    except:
        review_count = 0
    return google_url, review_count


def get_google_places_by_location(business_type, search_term, location_name = '', coordinates =None, radius = '16093', next_page=''):
    # Google places API request requires coordinates
    if len(location_name):
        coordinates = ','.join(map(str, get_corrdinates_from_name(location_name=location_name)))
    elif not len(coordinates):
        # change to raise an error
        print('Must provide an area name or coordinates for the search')
    URL = ('https://maps.googleapis.com/maps/api/place/textsearch/json?location='
    	+ coordinates + '&radius=' + radius + 'query=' + search_term + '&type='
    	+ business_type + '&pagetoken=' + next_page + '&key='+ API_key)
    response = requests.get(URL)
    json_obj = json.loads(response.text)
    results = json_obj["results"]

    # initialize database functions
    db = Database()
    update_sql = """INSERT INTO businesses (name, platform_id, url, total_review_count, address)
                    VALUES (%s, %s, %s, %s, %s)"""

    for result in results:
        name = result['name']
        google_id = result['place_id']
        address = result['formatted_address']
        google_url , review_count = get_google_place_url_and_review_count(google_id)
        db.update_rows( update_sql, *(name, id, url, review_count, address))
    try:
        next_page_token = json_obj["next_page_token"]
    except:
        #no next page
        return
    time.sleep(1)
    get_google_places_by_location(business_type, search_term, coordinates=coordinates, next_page=next_page_token)
