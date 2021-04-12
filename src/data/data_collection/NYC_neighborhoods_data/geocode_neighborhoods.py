import requests, json
from dotenv import load_dotenv
import pandas as pd


## Position Stack goecode neighborhood name to coordinates
def PS_geocode(nghbr_name, API_KEY=''):
    # fetch api_key from .env file if not supplied to function
    if not API_KEY:
        load_dotenv()
        API_KEY = os.getenv('PS_API_KEY')

    URL = ('http://api.positionstack.com/v1/forward?access_key='
            + API_KEY + '&query=' + nghbr.replace(',', ' ') + ',NY')
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    if len(json_obj['data']):
        json_obj2 = json_obj['data'][0]
        if json_obj2['type'] == 'neighbourhood' and json_obj2['region'] == 'New York':
            lat, lon = json_obj2['latitude'], json_obj2['longitude']
            return lat, lon
        else:
            print(json_obj2)
            print('Could not find coordinates for {}'.format(nghbr))
