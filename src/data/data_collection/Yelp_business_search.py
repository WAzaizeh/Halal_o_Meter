# Get a set of businesses along with their full details
# by querying Yelp Fusion API according to
# a location, type of business, and search term.

import requests, json, time
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()
API_key = os.getenv('YELP_API_KEY')


def get_yelp_places_by_location(search_location, search_type, search_term):
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        'location': search_location,
        'type': search_type,
        'term': search_term,
        'offset': ''
    }
    headers = {
      'Authorization': 'Bearer %s' % API_key
    }

    offset_max = 951
    # initialize database functions
    db = Database()
    update_sql = """INSERT INTO businesses (name, platform_id, url, total_review_count, address)
                    VALUES (%s, %s, %s, %s, %s)"""

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
            address = result['location']['display_address']
            db.insert_row(update_sql, *(name, yelp_id, yelp_url, review_count, address))
        # load more results using the offset param
        params['offset'] = str(int(params['offset']) + 50) if params['offset'] != '' else '51'
        time.sleep(5)
