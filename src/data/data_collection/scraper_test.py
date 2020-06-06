from review_scraper import scrape_yelp_reviews, scrape_google_reviews

google_test_url = 'https://maps.google.com/?cid=4988939335835406517'
google_id = 'randomID8083rpoeu'
yelp_test_url = 'https://www.yelp.com/biz/mia-halal-food-ozone-park?adjust_creative=xl_eXoprFhB3R9K5U7OxqQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xl_eXoprFhB3R9K5U7OxqQ'

data = scrape_google_reviews(google_url=google_test_url, google_id=google_id)
print(len(data)) # should be 11

# data = scrape_yelp_reviews(yelp_test_url)
# print(len(data)) # should be 52
