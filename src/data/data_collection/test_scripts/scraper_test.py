import sys
# add parent system path
sys.path.append('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection')

from review_scraper import scrape_yelp_reviews, scrape_google_reviews

google_test_url = 'https://maps.google.com/?cid=4988939335835406517'
google_id = 'randomID8083rpoeu'
yelp_test_url = 'https://www.yelp.com/biz/mia-halal-food-ozone-park?adjust_creative=xl_eXoprFhB3R9K5U7OxqQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xl_eXoprFhB3R9K5U7OxqQ'
yelp_id = 'randomID9004'

data = scrape_google_reviews(google_url=google_test_url, google_id=google_id)
print(*data[:3], sep='\n') # should be 11 as of 9/17/2020

data = scrape_yelp_reviews(yelp_url=yelp_test_url, yelp_id=yelp_id)
print(*data[:3], sep='\n') # should be 53 as of 9/17/2020
