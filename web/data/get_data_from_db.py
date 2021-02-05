coimport streamlit as st
import pandas as pd
import numpy as np
import sys
sys.path.append('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src')
from data.data_collection.storage_managers.database import Database

@st.cache
def get_restaurant_data() -> pd.DataFrame():
    res_df = _get_restaurant_db()
    # format address properly
    res_df['address'] = res_df['address'].apply(lambda address: ''.join(address.split('"')[1:-1]))
    # assign random halal score
    res_df['score'] = np.random.randint(1, 6, res_df.shape[0])
    #rename longitude column for map func
    res_df.rename({'lng': 'lon'}, axis=1, inplace=True)
    return res_df


@st.cache
def _get_restaurant_db() -> pd.DataFrame():
    db = Database()
    get_rests_sql = '''
                    SELECT name, url, total_review_count, address, image_url, lat, lng
                    FROM businesses
                    WHERE NOT (lat is NULL AND lng is NULL)
                    '''
    res_df = db.get_df(get_rests_sql)
    return res_df


@st.cache
def get_neighborhoods_dataframe() -> pd.DataFrame():
    res_df = _get_neighborhoods_db()
    # format neighborhood name
    res_df['neighborhood'] = res_df['neighborhood'].str.replace('+', ' ').str.replace(',', ', ')
    #rename longitude column for map func
    res_df.rename({'lng': 'lon'}, axis=1, inplace=True)
    return res_df

@st.cache
def _get_neighborhoods_db() -> pd.DataFrame():
    db = Database()
    get_rests_sql = '''
                    SELECT neighborhood, lat, lng
                    FROM coordinates
                    '''
    res_df = db.get_df(get_rests_sql)
    return res_df
