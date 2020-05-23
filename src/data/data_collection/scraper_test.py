import review_scraper

google_test_url = 'https://maps.google.com/?cid=4988939335835406517'
yelp_test_url = 'https://www.yelp.com/biz/mia-halal-food-ozone-park?adjust_creative=xl_eXoprFhB3R9K5U7OxqQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xl_eXoprFhB3R9K5U7OxqQ'

# data = review_scraper.scrape_google_reviews(google_test_url)
# print(data)

data = review_scraper.scrape_yelp_reviews(yelp_test_url)
print(len(data))
