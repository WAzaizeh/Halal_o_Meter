import streamlit as st
import pandas as pd
import sys
# sys.path.append('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src')
from data.distance_calc import Haversine
from fuzzywuzzy import fuzz


@st.cache
def get_restaurant_dataframe(sort_flag, halal_filter, ngbr_lat, ngbr_lon, name_match='', page_num=0) -> pd.DataFrame():
    biz_data_path = './data/processed/businesses_database_clone.csv'
    df = pd.read_csv(biz_data_path, header=0)
    df.rename({'lng': 'lon'}, axis=1, inplace=True)
    df['distance'] = df.apply(lambda row: Haversine(ngbr_lat, ngbr_lon, row.lat, row.lon), axis=1)
    df.sort_values('distance', inplace=True)

    # filter dataframe by halal score mask
    if halal_filter:
        try:
            halal_mask = [int(score) for score in halal_filter]
            df = df[ df['score'].isin(halal_mask)]
        except:
            st.error('Please enter a valid halal score. {} is not a valid halal score'.format(halal_filter))

    # filter by restaurant name similarity to entered text
    if len(name_match):
        try:
            # fuzzy name match with arbitrary threshold of 75
            fuzzy_threshold = 50
            fuzzy_name_mask = [fuzz.partial_ratio(name, name_match)>fuzzy_threshold for name in df.name]
            df = df[fuzzy_name_mask]
        except:
            st.error('No restaurants match your entered text! Try another input.')

    if sort_flag == 'Most Reviewed':
        df.sort_values('total_review_count', ascending=False, inplace=True)
    # elif sort_flag == 'Distance':
    #     df.sort_values('distance', inplace=True)
    elif sort_flag == 'Halal Score':
        df.sort_values('score', ascending=False, inplace=True)
    return df[page_num*20 : (page_num*20) + 20]

@st.cache
def get_neighborhoods_dataframe() -> pd.DataFrame():
    coord_data_path = './data/processed/coordinates_database_clone.csv'
    df = pd.read_csv(coord_data_path, header=0)
    df.columns = ['name', 'id', 'lat', 'lon']
    return df
