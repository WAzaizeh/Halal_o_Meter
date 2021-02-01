import streamlit as st
import pandas as pd

# both files need to be updates
# better yet, pull the data from the database

@st.cache
def get_dataframe(sort_by='', page_num=0) -> pd.DataFrame():
    biz_data_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/data/external/businesses_database_clone.csv'
    df = pd.read_csv(biz_data_path, header=0)
    if sort_by != 'Halal Score':
        df.sort_values('total_review_count', inplace=True)
    return df[page_num*20 : (page_num*20) + 20]

@st.cache
def get_neighborhoods() -> pd.DataFrame():
    coord_data_path = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/data/external/coordinates_database_clone.csv'
    df = pd.read_csv(coord_data_path, header=0)
    return df
