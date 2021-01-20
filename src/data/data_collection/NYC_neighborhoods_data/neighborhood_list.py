# Refers to a locally saved csv file,
# copied from https://www.baruch.cuny.edu/nycdata/population-geography/neighborhoods.htm
# and reurns a flat list with "neighborhood, borough" format

import pandas as pd
import os
from search_and_scrape.Google_business_search import get_corrdinates_from_name, get_name_from_coordinates
from storage_managers.database import Database

def custom_csv_to_db():
    neighborhood_table = pd.read_csv(os.getcwd()+'/NYC_neighborhood.csv', keep_default_na=False)

    # add borough name to neighborhood name and return as a flat list
    neighborhood_table = neighborhood_table.apply(lambda x: x+','+x.name)
    neighborhood_list = neighborhood_table.values.flatten()
    neighborhood_list = list(filter(lambda x: not x.startswith(','), neighborhood_list))
    neighborhood_list = [neighborhood.replace(' ','+') for neighborhood in neighborhood_list]

    # convert neighborhood_list to neighborhood_coordinates and update database
    db = Database()
    update_sql = """INSERT INTO coordinates (neighborhood, lat, lng)
                    VALUES (%s, %s, %s)"""
    for neighborhood in neighborhood_list:
        # print(neighborhood)
        lat, lng = get_corrdinates_from_name(neighborhood)
        db.insert_row(update_sql, *(neighborhood, lat, lng))

def confirm_neighborhoods():
    db = Database()
    neighborhoods = db.select_df('''SELECT * FROM coordinates''')
    neighborhoods['reversed_name'] = neighborhoods.apply(lambda row: get_name_from_coordinates(row.lat, row.lng), axis=1)
