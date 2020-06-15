import os
from dotenv import load_dotenv
from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
import pandas as pd


def _validate(address_list):
    auth_id = "Your SmartyStreets Auth ID here"
    auth_token = "Your SmartyStreets Auth Token here"

    # We recommend storing your secret keys in environment variables instead---it's safer!
    load_dotenv()
    auth_id = os.environ['SMARTY_AUTH_ID']
    auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()
    batch = Batch()

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields

    for i, key in enumerate(address_list): # key of the dict are indicies form target_df
    batch.add(StreetLookup())
    #  batch[i].business = address_list[index]['restaurant_name']
    batch[i].street = address_list[key]['street']
    batch[i].city = address_list[key]['city']
    batch[i].state = address_list[key]['state']
    batch[i].match = "strict"


    assert len(batch) == 5

    try:
        client.send_batch(batch)
    except exceptions.SmartyException as err:
        print(err)
        return

    results = []
    for i, lookup in enumerate(batch):
        candidates = lookup.result

        if len(candidates) == 0:
            print("Address {} is invalid".format(i))
            results.append(None)
            continue

        print("Address {} is valid. (There is at least one candidate)".format(i))

        for candidate in candidates:
            line_1 = candidate.delivery_line_1
            last_line = candidate.last_line
            address = ', '.join([line_1, last_line])
            results.append(address)
        #     components = candidate.components
        #     metadata = candidate.metadata
        #     print("\nCandidate {} : ".format(candidate.candidate_index))
        #     print("Delivery line 1: {}".format(candidate.delivery_line_1))
        #     print("Last line:       {}".format(candidate.last_line))
        #     print("ZIP Code:        {}-{}".format(components.zipcode, components.plus4_code))
        #     print("County:          {}".format(metadata.county_name))
        #     print("Latitude:        {}".format(metadata.latitude))
        #     print("Longitude:       {}".format(metadata.longitude))
        # print("")
    print(results)
    return results

def _validate_zabiha():
    target_df = pd.read_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv')

    street = []
    city = []
    state = []
    for i, row in target_df.iterrows():
        text = row.restaurant_address.split(',')
        street.append(text[0])
        city.append(text[1])
        state.append(text[2])

    target_df['street'] = street
    target_df['city'] = city
    target_df['state'] = state

    n=5
    validated_address = []
    for i in range(0, len(target_df.restaurant_address), n):
        res = _validate(target_df.restaurant_address[i:i + n])
        validated_address.extend(res)

    # update csv
    target_df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/validated_target_list.csv', index=False)

def _validate_zomato():


if __name__ == "__main__":
    _validate_zabiha()
    _validate_zomato()
