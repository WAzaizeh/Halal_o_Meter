# Get a set of business names
# by querying Google Places API according to
# a location, type of business, and search term.

import requests, json, time
#import database_func as db
from storage_managers.database import Database
from dotenv import load_dotenv
import os
from storage_managers.json_managment import json_to_file

load_dotenv()
API_key = os.getenv('GOOGLE_API_KEY')

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
        return 0, 0

def get_name_from_coordinates(lat, lng):
    URL = ('https://maps.googleapis.com/maps/api/geocode/json?latlng='
    + str(lat) + ',' + str(lng) + '&result_type=neighborhood&key=' + API_key)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    if json_obj['status'] == 'OK':
        results = json_obj['results']
        neighborhood_name = results[0]['formatted_address']
        return neighborhood_name
    else:
        return None

def _get_google_business_details(place_id, fields='url,price_level,rating,user_ratings_total'):
    URL = ('https://maps.googleapis.com/maps/api/place/details/json?placeid='
    + place_id + '&fields=' + fields + '&key='+API_key)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    place_details = json_obj["result"]
    res_dict = dict()
    for var in fields.split(','):
        try:
            res_dict[var] = place_details[var]
        except:
            res_dict[var] = 0
    return res_dict


def get_google_places_by_location(coordinates, business_type='restaurant', search_term='halal', radius = '16093', next_page='', save_json=False):
    URL = ('https://maps.googleapis.com/maps/api/place/textsearch/json?location='
    	+ str(coordinates[1]) + '&radius=' + radius + 'query=' + search_term + '&type='
    	+ business_type + '&pagetoken=' + next_page + '&key='+ API_key)
    response = requests.get(URL)
    json_obj = json.loads(response.text)
    results = json_obj["results"]

    businesses_list = []
    for result in results:
        name = result['name']
        google_id = result['place_id']
        # have to use Google fields options and variables have to be in same order as fields string
        google_url , review_count = _get_google_business_details(place_id=google_id, fields='url,user_ratings_total').values()
        address = result['formatted_address']
        try:
            image_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + result['photos'][0]['photo_reference'] + '&key='+ API_key
        except: # no image
            image_url = 'https://thumbs.dreamstime.com/b/food-line-icon-restaurant-sign-fork-knife-plate-symbol-geometric-shapes-random-cross-elements-linear-food-icon-design-vector-136546147.jpg'
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        businesses_list.append([name, google_id, google_url, review_count, address, image_url, lat, lng])
        # save json files for debgging and to avoid calling api too many times
        if save_json:
            json_to_file(businesses_id=google_id, json_ojb=result)
    try:
        next_page_token = json_obj["next_page_token"]
        time.sleep(1)
        data = get_google_places_by_location(coordinates=coordinates, next_page=next_page_token)
        businesses_list.extend(data)
    except:
        #no next page
        next_page_token = ''
    if (not len(next_page)) & (len(next_page_token)):
        print('Found {} businesses around {}'.format(len(businesses_list), coordinates[0]))
    return businesses_list
