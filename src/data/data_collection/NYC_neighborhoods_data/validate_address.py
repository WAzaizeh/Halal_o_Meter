import os, re, requests, json
from dotenv import load_dotenv
from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
from usps import USPSApi, Address
import pandas as pd


def smarty_validate(address):
    load_dotenv()
    auth_id = os.environ['SMARTY_AUTH_ID']
    auth_token = os.environ['SMARTY_AUTH_TOKEN']
    write_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/invalid_address.txt'
    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_street_api_client()

    lookup = StreetLookup()
    lookup.street = address
    lookup.match = "strict"
    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result
    if not result:
        print("\nInvalid address.")
        print(address)
        # with open(write_path, 'a+') as myfile:
        #     myfile.write("{}\n".format(address))
        return
    return result

def google_validate(address):
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_API_KEY_3')

    URL = ('https://maps.googleapis.com/maps/api/geocode/json?address='
    + address + '&key=' + API_KEY)
    r = requests.get(URL)
    response = r.text
    json_obj = json.loads(response)
    try:
        results = json_obj["results"][0]
        return results['formatted_address']
    except:
        print('\n{} could not be standarized from Google'.format(address))
        return

def usps_validate(address):
    text = address.split(',')
    usps_address = Address(
        name = '',
        address_1= text[0],
        city= text[1],
        state= text[2],
        zipcode= ''
    )
    usps = USPSApi('686NONE02749', test=True)
    validation = usps.validate_address(usps_address)
    print(validation.result)

if __name__ == "__main__":
    target_df = pd.read_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv')
    target_df['validated_address'] = None

    # # for testing
    # address_df = target_df.sample(n=10)
    # for i, address in address_df['address'].iteritems():

    for i, address in target_df['address'].iteritems():
        address = address.lower()
        res = google_validate(address)
        target_df['validated_address'][i] = res
        print('Progress: {0}/{1}'.format(i, target_df.shape[0]), end='\r', flush=True)

    # update csv file
    # address_df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/test_target_list.csv')
    target_df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv')
