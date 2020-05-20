# Get a set of businesses along with their full deatils
# by querying Yelp Fusion API according to
# a location, type of business, and search term.

import requests, json, time

API_key = '9HyMSC_C3XTFMXp2XoqkN4IVTNC3KJh6guNLuoDxIra07urp-LaWF5lgOnRwPltadlUZWL-7t5YIhsQaOAltdlzbi1hmbpoHcim52j1kUt7ji962Kih3dCvhW8nCXnYx'


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

    total_results = []
    # offset limit needs to be changed to json_obj[total]
    while len(params['offset']) == 0 or int(params['offset']) < 951:
        print(params['offset'])
        response = requests.request("GET", url, headers=headers, params=params)
        json_obj = json.loads(response.text)
        results = json_obj['businesses']
        for result in results:
            name = result['name']
            yelp_id = result['id']
            yelp_url = result['url']
            review_count = result['review_count']
            address = result['location']['display_address']
            total_results.append([name, yelp_id, yelp_url, review_count, address])
            print(total_results[-1])
            print('\n', len(total_results),'\n')
        # iterate over results using the offset param
        params['offset'] = str(int(params['offset']) + 50) if params['offset'] != '' else '51'
        time.sleep(5)

    # print(total_results)
