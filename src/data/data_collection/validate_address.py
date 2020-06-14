import os
from dotenv import load_dotenv
from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup
import pandas as pd


def run(address_list, key=1):
    auth_id = "Your SmartyStreets Auth ID here"
    auth_token = "Your SmartyStreets Auth Token here"

    # We recommend storing your secret keys in environment variables instead---it's safer!
    load_dotenv()
    auth_id = os.environ['SMARTY_AUTH_ID_'+str(key)]
    auth_token = os.environ['SMARTY_AUTH_TOKEN_'+str(key)]

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()
    batch = Batch()

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields

    # batch.add(StreetLookup())
    # batch[0].input_id = "24601"  # Optional ID from your system
    # batch[0].addressee = "John Doe"
    # batch[0].street = "1600 amphitheatre parkway"
    # batch[0].street2 = "closet under the stairs"
    # batch[0].secondary = "APT 2"
    # batch[0].urbanization = ""  # Only applies to Puerto Rico addresses
    # batch[0].lastline = "Mountain view, california"
    # batch[0].candidates = 5
    # batch[0].match = "invalid"  # "invalid" is the most permissive match,
    #                             # this will always return at least one result even if the address is invalid.
    #                             # Refer to the documentation for additional Match Strategy options.
    #
    # batch.add(StreetLookup("1 Rosedale, Baltimore, Maryland"))  # Freeform addresses work too.
    # batch[1].candidates = 10  # Allows up to ten possible matches to be returned (default is 1).
    #
    # batch.add(StreetLookup("123 Bogus Street, Pretend Lake, Oklahoma"))


    for address in address_list:
        batch.add(StreetLookup(address))
        # batch[i].input_id = address[0]


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


if __name__ == "__main__":
    target_df = pd.read_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv')

    for i, address in enumerate(target_df.restaurant_address):
        parts = address.split(',')
        parts[1] = target_df.borough[i]
        target_df.restaurant_address[i] = ', '.join(parts)

    n=5
    target_df['validated_address'] = None
    for i in range(0, len(target_df.restaurant_address), n):
        if i < 250:
            key = 1
        elif i < 500:
            key = 2
        else:
            key = 3
        res = run(target_df.restaurant_address[i:i + n], key)
        target_df['validated_address'][i:i + n] = res

    # update csv
    target_df.to_csv('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/target_list.csv', index=False)
