# Get a set of business names
# by querying Google Places API according to
# a location, type of business, and search term.

import requests, json, time
#import database_func as db
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv('GOOGLE_API_KEY_3')

def get_corrdinates_from_name(location_name):
    URL = ('https://maps.googleapis.com/maps/api/geocode/json?address='
    + location_name + '&components=country:US|&key=' + API_key)
    headers = {
  'Authorization': 'Bearer ' + API_key
    }
    r = requests.get(URL, headers=headers)
    response = r.text
    json_obj = json.loads(response)
    results = json_obj["results"]
    if json_obj['status'] == 'OK':
        for result in results:
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
        return lat, lng
    else:
        print(json_obj)
        return 0, 0

def get_name_from_coordinates(lat, lng):
    URL = ('https://maps.googleapis.com/maps/api/geocode/json?latlng='
    + str(lat) + ',' + str(lng) + '&result_type=neighborhood&key=' + API_key)
    print(URL)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    if json_obj['status'] == 'OK':
        results = json_obj['results']
        neighborhood_name = results[0]['formatted_address']
        return neighborhood_name
    else:
        return None

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
    	+ str(coordinates) + '&radius=' + radius + 'query=' + search_term + '&type='
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
        try:
            image_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + result['photos'][0]['photo_reference'] + '&key='+ API_key
        except: # no image
            print('No image found for {}'.format(name))
            image_url = 'https://thumbs.dreamstime.com/b/food-line-icon-restaurant-sign-fork-knife-plate-symbol-geometric-shapes-random-cross-elements-linear-food-icon-design-vector-136546147.jpg'
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        businesses_list.append([name, google_id, google_url, review_count, address, image_url, lat, lng])
        # db.insert_row( update_sql, *(name, google_id, google_url, review_count, address))
    try:
        next_page_token = json_obj["next_page_token"]
        time.sleep(1)
        data = get_google_places_by_location(coordinates=coordinates, next_page=next_page_token)
        businesses_list.extend(data)
    except:
        #no next page
        pass
    return businesses_list
