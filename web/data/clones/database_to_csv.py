'''
A script to generate a csv from postgres businesses, which includes all restaurant information,
and coordinates, which includes neighborhoods data, tables.
'''
import os, sys
import pandas as pd
import numpy as np # for mock data

# add path to database script
modules_path = [os.path.abspath(os.path.join('.')+'/src/data/data_collection/')] #, os.path.abspath(os.path.join('.')+'/web/pages')
for module in modules_path:
    if module not in sys.path:
        sys.path.append(module)

from database import Database

############ businesses pg to pd.csv ############
# get data from postgres table as pandas DataFrame
db = Database()
get_businesses = '''SELECT *
                FROM businesses'''
biz_data = db.select_rows(get_businesses)

# convert to dataframe
biz_df = pd.DataFrame(biz_data)
biz_df.columns = ['name', 'platform_id', 'url', 'total_review_count', 'address', 'id', 'image_url', 'lat', 'lng']

# keep only entries with image_url
biz_df = biz_df.loc[~biz_df['image_url'].isnull()]
biz_df = biz_df.loc[~(biz_df['image_url'] == '')]

# format address properly
biz_df['address'] = biz_df['address'].apply(lambda address: ''.join(address.split('"')[1:-1]))

# assign random reliability score
biz_df['score'] = np.random.randint(1, 6, biz_df.shape[0])

# save as csv
biz_file_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/data/external/businesses_database_clone.csv'
biz_df.to_csv(biz_file_path, index=False)

############ coordinates pg to pd.csv ############
coord_sql = '''SELECT *
                FROM coordinates'''
coord_df = db.select_df(coord_sql)

# format neighborhood name
coord_df['neighborhood'] = coord_df['neighborhood'].str.replace('+', ' ').str.replace(',', ', ')

# sort neighborhood name alphabetically
coord_df = coord_df.sort_values('neighborhood')

# save as csv
coord_file_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/data/external/coordinates_database_clone.csv'
coord_df.to_csv(coord_file_path, index=False)
