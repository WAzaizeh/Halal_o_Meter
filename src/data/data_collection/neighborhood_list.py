# Refers to a locally saved csv file,
# copied from https://www.baruch.cuny.edu/nycdata/population-geography/neighborhoods.htm
# and reurns a flat list with "neighborhood, borough" format

import pandas as pd
import os

def get_list():
    neighborhood_table = pd.read_csv(os.getcwd()+'/NYC_neighborhood.csv', keep_default_na=False)

    # add borough name to neighborhood name and return as a flat list
    neighborhood_table = neighborhood_table.apply(lambda x: x+','+x.name)
    neighborhood_list = neighborhood_table.values.flatten()
    neighborhood_list = list(filter(lambda x: not x.startswith(','), neighborhood_list))
    return neighborhood_list

    # make this upload the final result to postgres
