import streamlit as st
import pandas as pd
import sys
# sys.path.append('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src')
from data.distance_calc import Haversine


@st.cache
def get_restaurant_dataframe(sort_by, ngbr_lat, ngbr_lon, page_num=0) -> pd.DataFrame():
    biz_data_path = 'web/data/clones/businesses_database_clone.csv'
    df = pd.read_csv(biz_data_path, header=0)
    df.rename({'lng': 'lon'}, axis=1, inplace=True)
    df['distance'] = df.apply(lambda row: Haversine(ngbr_lat, ngbr_lon, row.lat, row.lon), axis=1)
    df.sort_values('distance', inplace=True)

    if sort_by == 'Most Reviewed':
        df.sort_values('total_review_count', ascending=False, inplace=True)
    # elif sort_by == 'Distance':
    #     df.sort_values('distance', inplace=True)
    elif sort_by == 'Halal Score':
        df.sort_values('score', ascending=False, inplace=True)
    return df[page_num*20 : (page_num*20) + 20]

@st.cache
def get_neighborhoods_dataframe() -> pd.DataFrame():
    coord_data_path = 'web/data/clones/coordinates_database_clone.csv'
    df = pd.read_csv(coord_data_path, header=0)
    df.columns = ['name', 'id', 'lat', 'lon']
    return df
