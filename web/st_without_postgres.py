"""This application experiments with the (grid) layout and some styling

Can we make a compact dashboard across several columns and with a dark theme?"""
# import io
from typing import List, Optional
import os, sys, re
import markdown
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import pydeck as pdk



# for testing
import numpy as np

# add path to database
modules_path = [os.path.abspath(os.path.join('.')+'/src/data/data_collection/')] #, os.path.abspath(os.path.join('.')+'/web/pages')
for module in modules_path:
    print(module)
    if module not in sys.path:
        sys.path.append(module)

from database import Database
# import pages.home as home

# matplotlib.use("Agg")
COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'
COUNT = 0

# extension to sidebar
# def add_resources_section():
#     """Adds a resources section to the sidebar"""
#     st.sidebar.header("Add_resources_section")
#     st.sidebar.markdown(
#         """
# - [gridbyexample.com] (https://gridbyexample.com/examples/)
# """
#     )


class Cell:
    """A Cell can hold text, markdown, plots etc."""

    def __init__(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        self.class_ = class_
        self.grid_column_start = grid_column_start
        self.grid_column_end = grid_column_end
        self.grid_row_start = grid_row_start
        self.grid_row_end = grid_row_end
        self.inner_html = ""

    def _to_style(self) -> str:
        return f"""
.{self.class_} {{
    grid-column-start: {self.grid_column_start};
    grid-column-end: {self.grid_column_end};
    grid-row-start: {self.grid_row_start};
    grid-row-end: {self.grid_row_end};
}}
"""

    def text(self, text: str = ""):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)

    def dataframe(self, dataframe: pd.DataFrame):
        self.inner_html = dataframe.to_html()

    def image(self, url):
        self.inner_html = '<img src ="' + url +'"/>'

    def image_card(self, name, address, score, image_url):
        stars = ""
        for i in range(int(score)): stars += '<img src="https://cdn.onlinewebfonts.com/svg/img_39469.png"/>'
        self.inner_html = '<div class="flex">'\
        +'<img class="main-image" src ="' + image_url +'"/>'\
        + '<div class="main-body">'\
        + '<h3>'+ name +'</h3>'\
        + '<p class="stars">'+ stars + '</p>'\
        + '<p class="location"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" class="icon_svg"><path d="M12 1.04a9.25 9.25 0 0 1 6.54 15.79l-5.83 5.84A1 1 0 0 1 12 23a1 1 0 0 1-.71-.29l-5.83-5.88A9.25 9.25 0 0 1 12 1.04zm0 2.01a7.25 7.25 0 0 0-5.13 12.37L12 20.54l5.13-5.12A7.25 7.25 0 0 0 12 3.05zm0 3.2a4 4 0 1 1 0 8 4 4 0 0 1 0-8zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"></path></svg> 0.2 miles </p>' \
        + '<p class="light">Summer drinks are back at Starbucks. Order today. </p>'\
        + '</div>'\
        + '<div class="address">'\
        + '<p class="light">' + address + '</p>'\
        + '</div>'\
        + '</div>'


    def _to_html(self):
        return f"""<div class="box {self.class_}">{self.inner_html}</div>"""

class Grid:
    """A (CSS) Grid"""

    def __init__(
        self,
        template_columns="1 1 1",
        gap="10px",
        background_color=COLOR,
        color=BACKGROUND_COLOR,
        df=None,
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []
        self.df = df

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
<style>
    .wrapper {{
    display: grid;
    grid-template-columns: {self.template_columns};
    grid-gap: {self.gap};
    background-color: {self.background_color};
    color: {self.color};
    }}
    .box {{
    border-radius: 5px;
    padding: 20px;
    font-size: 150%;
    background: none;
    border: 1px solid #a9abaf;
    color: #000;
    background: #fbfafa;
    }}
    .box .main-image {{
        width: auto;
        height: 200px;
        border-radius: 10px;
        margin-right: 12px;
    }}
    .box .stars {{
        height: 15px;
    }}
    .box .location {{
        font-weight: bold;
    }}
    .box .light {{
            color: #a0a0a0;
            font-weight: 100;
            font-size: 14px;
    }}
    .box .main-body {{
        flex: 1;
    }}
    .box .address {{
        width: 150px;
    }}
    .box .stars img {{
        height: 100%;
        margin-right: 2px;
    }}
    table {{
        color: {self.color}
    }}
    .flex {{
        display: flex;
    }}
    .stSelectbox div {{
        background: #fff;
    }}
    .st-at {{
        background-color:none;
        border: 1px solid #fb919d;
    }}
    .reportview-container .image-container img {{
        width:100px !important;
        margin: auto;
    }}
    .sidebar .sidebar-content {{
    width: 14rem;
    }}
</style>
"""

    def _get_cells_style(self):
        return (
            "<style>"
            + "\n".join([cell._to_style() for cell in self.cells])
            + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell._to_html() for cell in self.cells])
            + "</div>"
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell

def _set_block_container_style(
    # max_width: int = 1200,
    # max_width_100_percent: bool = False,
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 5,
):
    # if max_width_100_percent:
    #     max_width_str = f"max-width: 100%;"
    # else:
    #     max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        width: 67%;
        padding-top: 20px;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: 0;
        max-width: 814px;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
        align-items: flex-start;
    }}

    .reportview-container .main .block-container .element-container:nth-child(9) {{
        width: 28% !important;
        position: fixed;
        top: 110px;
        right: 0;
        border-radius: 5px;
        overflow: hidden;
        height: 100vh;
        padding-right: 10px;
    }}

    .sidebar-content {{
        background-color: #e5e7ea;
        background-image: none;
    }}
    @media (max-width: 960px) {{
        .reportview-container .main .block-container{{
            width: 100%;
            max-width: 100%;
        }}
        .reportview-container .main .block-container .element-container:nth-child(9) {{
            display: none;
        }}
    }}

</style>
""",
        unsafe_allow_html=True,
    )
x = 0

def make_main_body(res_df):
    df = get_neighborhoods()
    df.columns = ['name', 'id', 'lat', 'lon']
    neighborhood = st.selectbox("", df['name'])
    st.markdown(
        """
        <h1>Best Halal food near {0}</h1>

        Are you wondering what halal options are around NYC neighborhoods?

        We provide a halal-reliability scroe based on reviews of the restaurants.
        We even have a dark theme?
        """.format(neighborhood), unsafe_allow_html=True
    )
    # generate a grid of 2 image_cards
    grid = Grid("1 1 1", color=COLOR, background_color=BACKGROUND_COLOR, df=df)

    with grid:
        for i, row in zip(range(df.shape[0]), res_df.itertuples()):
            grid.cell(chr(i + 97), 1, 2, i+1, i+1).image_card(name='. '.join([str(i+1),row.name]), address=row.address, score=str(row.score), image_url=row.image_url)

    # should be places in it's own function later
    # generate the map

    # Adding code so we can have map default to the center of the data
    midpoint = ((df.loc[0, 'lat']), (df.loc[0, 'lon']))

    st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude = midpoint[0],
                longitude =  midpoint[1],
                zoom = 10,
                pitch = 10
            ),
            tooltip={
                'html': '<b>{name}</b>',
                'style': {
                    'color': 'white'
                }
            },
            layers=[ pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position=['lon', 'lat'],
                auto_highlight=True,
                get_radius=250,
                get_fill_color='[145, 196, 251]',
                pickable=True
            )]
            )
        )

@st.cache
def get_dataframe(sort_by='') -> pd.DataFrame():
    """A slice of yelp businesses dataframe for testing purposes"""
    db = Database()
    yelp_sql = '''SELECT *
                    FROM businesses
                    WHERE url LIKE %s '''
    data = db.select_rows(yelp_sql, ('%yelp%', ))
    # for testing
    df = pd.DataFrame(data)[:20]
    df.columns = ['name', 'platform_id', 'url', 'total_review_count', 'address', 'id']
    df.address = df.address.map(lambda address: re.sub(r'[^A-Za-z0-9, ]+', '', address).split(','))
    df.address = df.address.map(lambda address: ', '.join([str.strip() for str in address]))
    df['score'] = np.random.randint(1, 6, df.shape[0])
    df['image_url'] = 'https://s3-media0.fl.yelpcdn.com/bphoto/h92NeXrAhC_SCM-Fa77J5A/258s.jpg'
    if sort_by != 'Halal Score':
        df.sort_values('total_review_count', inplace=True)
    return df

@st.cache
def get_neighborhoods() -> pd.DataFrame():
    '''List of NYC neighborhoods to search in'''
    db = Database()
    neighborhoods_sql = '''SELECT *
                            FROM coordinates'''
    df = db.select_df(neighborhoods_sql)
    df['neighborhood'] = df['neighborhood'].str.replace('+', ' ').str.replace(',', ', ')
    return df

def main():
    """Main function of the App"""
    st.sidebar.image('/Users/wesamazaizeh/Downloads/logo.png', use_column_width=True)
    st.sidebar.header("Filter Options")
    sort_by = st.sidebar.radio('Filter by:', ('Halal Score', 'Most Reviwed', 'Distance'))

    with st.spinner(f"Loading {sort_by} ..."):
        res_df = get_dataframe(sort_by)
        make_main_body(res_df)

    _set_block_container_style()

main()
