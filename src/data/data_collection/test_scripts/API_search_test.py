# add /src/data/data_collection to sys.path so scripts can be imported
import sys, os
sys.path.append( os.getcwd() + '/src/data/data_collection/')

import Yelp_business_search
import  Google_business_search


# Yelp_business_search.get_yelp_places_by_location('OzonePark', 'restaurant', 'Halal')

# test google restaurant search around a location
coords = Google_business_search.get_corrdinates_from_name('ozone park, New York')
Google_business_search.get_google_places_by_location(coordinates=coords)

# Google_business_search.get_google_place_url_and_review_count('ChIJ-3xl7b9dwokRkpGWWIbh0ow')
