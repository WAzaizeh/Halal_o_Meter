# Get a set of business names
# by querying Google Places API according to
# a location, type of business, and search term.

import requests, json, time

API_key = 'AIzaSyAvKIZu8zOpq5FIANy5bA14zovrUPbNmWw'

# initilization of variables used in functions
total_results = []
next_page = ''


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
    review_count = place_details['user_ratings_total']
    return google_url, review_count
    ## get website - omitted for now
    # try:
	# 	if 'url' in place_details:
	# 		website = place_details['website']
	# 	else:
	# 		website = "no website listed in API"
	# except:
	# 	print("err getting place details")


def get_google_places_by_location(business_type, search_term, location_name = '', coordinates =None, next_page=''):
    if len(location_name):
        coordinates = ','.join(map(str, get_corrdinates_from_name(location_name=location_name)))
    elif not len(coordinates):
        # change to raise an error
        print('Must provide an area name or coordinates for the search')
    URL = ('https://maps.googleapis.com/maps/api/place/textsearch/json?location='
    	+ coordinates + '&radius=16093' + 'query=' + search_term + '&type='
    	+ business_type + '&pagetoken=' + next_page + '&key='+ API_key)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    results = json_obj["results"]
    for result in results:
        name = result['name']
        google_id = result['place_id']
        address = result['formatted_address']
        google_url , review_count = get_google_place_url_and_review_count(google_id)
        total_results.append([name, google_id, google_url, review_count, address])
        print(total_results[-1])
    try:
        next_page_token = json_obj["next_page_token"]
    except KeyError:
        #no next page
        return
    time.sleep(1)
    get_google_places_by_location(business_type, search_term, coordinates=coordinates, next_page=next_page_token)
