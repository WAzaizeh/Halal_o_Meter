"""Streamlit app with grid layout to display restaurant information with 'halal-reliability' score
The score is based on reviews scraped from Yelp & Google Maps"""

import streamlit as st
from styling.st_classes import Cell, Grid
from dataframes.get_data import get_dataframe, get_neighborhoods
from styling.style import _set_block_container_style
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import pathlib
import bs4

COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'


def make_main_body(rest_df, ngbr_df):
    # add list of neighborhoods to drop down menu
    neighborhood = st.selectbox('Select search neighborhood', ngbr_df['name'])

    # intro and header
    st.markdown(
        """
        <h1>Best Halal food near {0}</h1>

        Are you wondering what halal options are around NYC neighborhoods?

        We provide a halal-reliability score based on reviews of the restaurants.
        """.format(neighborhood), unsafe_allow_html=True)

    # generate a grid of image_cards
    grid = Grid("1 1 1", color=COLOR, background_color=BACKGROUND_COLOR, df=ngbr_df)

    # generate grid cells from dataframe
    with grid:
        for i, row in zip(range(ngbr_df.shape[0]), rest_df.itertuples()):
            grid.cell(chr(i + 97), 1, 2, i+1, i+1).image_card(name='. '.join([str(i+1),row.name]), address=row.address, score=str(row.score), image_url=row.image_url, url=row.url)

    # should be places in it's own function later
    # generate the map

    # Adding code so we can have map default to the center of the data
    midpoint = ((ngbr_df.loc[0, 'lat']), (ngbr_df.loc[0, 'lon']))

    st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude = midpoint[0],
                longitude =  midpoint[1],
                zoom = 10,
                pitch = 10,
                height = 700,
            ),
            tooltip={
                'html': '<b>{name}</b>',
                'style': {
                    'color': 'white'
                }
            },
            layers=[ pdk.Layer(
                'ScatterplotLayer',
                data=ngbr_df,
                get_position=['lon', 'lat'],
                auto_highlight=True,
                get_radius=250,
                get_fill_color='[255 139 156]',
                pickable=True)]
            ))


def main():
    """Main function of the App"""
    st.sidebar.image('/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/logo/logo.png', use_column_width=True)
    st.sidebar.markdown('---')
    st.sidebar.header('Filters')
    sort_by = st.sidebar.radio('Sort by:', ('Halal Score', 'Most Reviewed', 'Distance'))
    st.sidebar.markdown('---')

    with st.spinner(f"Loading {sort_by.lower()} ..."):
        rest_df = get_dataframe(sort_by)
        ngbr_df = get_neighborhoods()
        ngbr_df.columns = ['name', 'id', 'lat', 'lon']

        make_main_body(rest_df=rest_df, ngbr_df=ngbr_df)

    _set_block_container_style()

    GA_JS = """Hello world!"""

    # Insert the script in the head tag of the static template inside your virtual environement
    # index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    index_path = pathlib.Path('/Users/wesamazaizeh/miniconda3/envs/sm-project/lib/python3.8/site-packages/streamlit/static/index.html')
    soup = bs4.BeautifulSoup(index_path.read_text(), features="lxml")
    if not soup.find(id='custom-js'):
        script_tag = soup.new_tag("script", id='custom-js')
        script_tag.string = GA_JS
        soup.head.append(script_tag)
        index_path.write_text(str(soup))

main()
