##3 Libraries
import random

# add /src/data/data_collection to sys.path to import custom scripts
import sys, os
sys.path.append( os.getcwd() + '/src/data/data_collection/')

from database import Database

import Yelp_business_search
import  Google_business_search

### sample location
db = Database()
# fetch the list of NYC neighborhoods' coordinates
get_lat_lng = '''SELECT neighborhood, lat, lng
                    FROM coordinates'''
results = db.select_rows(get_lat_lng)
coordinates_list = [coord for coord in results]
coordinates_list = [[coord[0].replace('+', ' '), ','.join([str(coord[1]),str(coord[2])])] for coord in results]
sample_coord = random.sample(coordinates_list, 1)
coordinates = sample_coord[0]
# Yelp_business_search.get_yelp_places_by_location('OzonePark', 'restaurant', 'Halal')

# # test google restaurant search around a location
# biz_list = Google_business_search.get_google_places_by_location(coordinates=coordinates)
# print('Found {} businesses in {}'.format(len(biz_list), coordinates[0]))

# test yelp restaurant search around a location
biz_list = Yelp_business_search.get_yelp_places_by_location(coordinates=coordinates)
print('Found {} businesses in {}'.format(len(biz_list), coordinates[0]))
