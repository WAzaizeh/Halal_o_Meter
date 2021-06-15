"""Streamlit app with grid layout to display restaurant information with 'halal-reliability' score
The score is based on reviews scraped from Yelp & Google Maps"""

import streamlit as st
from styling.st_classes import Cell, Grid
from data.get_data_from_csv import get_restaurant_dataframe, get_neighborhoods_dataframe
from styling.style import _set_block_container_style
import os
import pandas as pd
import pydeck as pdk
from PIL import Image

COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'


def make_main_body(rest_df, ngbr_df, neighborhood):

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
            grid.cell(chr(i + 97), 1, 2, i+1, i+1).image_card(name='. '.join([str(i+1),row.name]), address=row.address, score=str(row.score), image_url=row.image_url, url=row.url, distance=str(round(row.distance,1)))

    # should be places in it's own function later
    # generate the map

    # Adding code so we can have map default to the center of the data
    midpoint = ((rest_df['lat'].mean()), (rest_df['lon'].mean()))

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
                data=rest_df,
                get_position=['lon', 'lat'],
                auto_highlight=True,
                get_radius=250,
                get_fill_color='[255 139 156]',
                pickable=True)]
            ))


def main():
    """Main function of the App"""
    st.sidebar.image(Image.open('web/data/logo/logo.png'), use_column_width=True)
    st.sidebar.markdown('---')
    st.sidebar.header('Filters')
    sort_flag = st.sidebar.radio('Sort by:', ('Halal Score', 'Most Reviewed', 'Distance'))
    halal_filter = st.sidebar.multiselect('Filter by Halal score',
                        ['1', '2', '3', '4', '5'])
    st.sidebar.markdown('---')

    # add list of neighborhoods to drop down menu
    ngbr_df = get_neighborhoods_dataframe()
    name_match = st.text_input('Restaurant Name :', '')
    neighborhood = st.selectbox('Near :', ngbr_df['name'])
    neighborhood_coords = ngbr_df.loc[ngbr_df['name'] == neighborhood][['lat', 'lon']]
    with st.spinner(f"Loading {sort_flag.lower()} ..."):
        rest_df = get_restaurant_dataframe(sort_flag, halal_filter,
                    neighborhood_coords['lat'], neighborhood_coords['lon'],
                    name_match=name_match)

        make_main_body(rest_df=rest_df, ngbr_df=ngbr_df, neighborhood=neighborhood)

    _set_block_container_style()


main()
