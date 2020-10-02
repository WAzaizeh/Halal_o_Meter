# Get a set of businesses along with their full details
# by querying Yelp Fusion API according to
# a location, type of business, and search term.

import requests, json, time
from database import Database
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
API_key = os.getenv('YELP_API_KEY')


def get_yelp_places_by_location(coordinates, search_type='restaurant', search_term='halal'):
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        'location': coordinates[1],
        'type': search_type,
        'term': search_term,
        'offset': ''
    }
    headers = {
      'Authorization': 'Bearer %s' % API_key
    }

    businesses_list = []
    offset_max = 951
    while len(params['offset']) == 0 or int(params['offset']) < offset_max:
        response = requests.request("GET", url, headers=headers, params=params)
        json_obj = json.loads(response.text)
        results = json_obj['businesses']
        offset_max =json_obj['total']
        for result in results:
            name = result['name']
            yelp_id = result['id']
            yelp_url = result['url']
            review_count = result['review_count']
            address = ', '.join(result['location']['display_address'])
            image_url = result['image_url']
            lat = result['coordinates']['latitude']
            lng = result['coordinates']['longitude']
            businesses_list.append([name, yelp_id, yelp_url, review_count, address, image_url, lat, lng])
        # load more results using the offset param
        params['offset'] = str(int(params['offset']) + 20) if params['offset'] != '' else '20'
        time.sleep(1)

    print('Yelp search in {0} yielded {1} business'.format(coordinates[0], offset_max))
    return businesses_list
