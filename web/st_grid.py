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

# for testing
import random

# add path to database
module_path = os.path.abspath(os.path.join('.')+'/src/data/data_collection')
if module_path not in sys.path:
    sys.path.append(module_path)

from database import Database

# matplotlib.use("Agg")
COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'


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
        self.inner_html = '<div class="flex">'\
        +'<img src ="' + image_url +'"/>'\
        + '<div>'\
        +'<p>'+ name +'</p>'\
        +'<p> Halal score: '+ score + ' (will be converted to stars) </p>'\
        +'<p>description description description description description description description description</p>'\
        + '</div>'\
        + '<div>'\
        +'<p>' + address + '</p>'\
        + '</div>'\
        +'</div>'


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
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

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
    background-color: {self.color};
    color: {self.background_color};
    border-radius: 5px;
    padding: 20px;
    font-size: 150%;
    }}
    table {{
        color: {self.color}
    }}
    .flex {{
        display: flex;
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


def select_block_container_style():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""
    st.sidebar.header("Block Container Style")
    max_width_100_percent = st.sidebar.checkbox("Max-width: 100%?", False)
    if not max_width_100_percent:
        max_width = st.sidebar.slider("Select max-width in px", 100, 2000, 1200, 100)
    else:
        max_width = 1200
    dark_theme = st.sidebar.checkbox("Dark Theme?", False)
    padding_top = st.sidebar.number_input("Select padding top in rem", 0, 200, 5, 1)
    padding_right = st.sidebar.number_input("Select padding right in rem", 0, 200, 1, 1)
    padding_left = st.sidebar.number_input("Select padding left in rem", 0, 200, 1, 1)
    padding_bottom = st.sidebar.number_input(
        "Select padding bottom in rem", 0, 200, 10, 1
    )
    if dark_theme:
        global COLOR
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = "rgb(17,17,17)"
        COLOR = "#fff"

    _set_block_container_style(
        max_width,
        max_width_100_percent,
        padding_top,
        padding_right,
        padding_left,
        padding_bottom,
    )


def _set_block_container_style(
    max_width: int = 1200,
    max_width_100_percent: bool = False,
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 5,
):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        width: 65%;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
        align-items: flex-start;
    }}

    .reportview-container .main .block-container .element-container:nth-child(10) {{
    width: 28% !important;
    position: fixed;
    top: 110px;

    right: 0;
    border-radius: 5px;
    overflow: hidden;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


@st.cache
def get_dataframe() -> pd.DataFrame():
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
    df['score'] = random.randint(1,5)
    df['image_url'] = 'https://s3-media0.fl.yelpcdn.com/bphoto/h92NeXrAhC_SCM-Fa77J5A/258s.jpg'
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

def get_matplotlib_plt():
    get_dataframe().plot(kind="line", x="quantity", y="price", figsize=(5, 3))


def main():
    """Main function. Run this to run the app"""
    st.sidebar.image('/Users/wesamazaizeh/Downloads/logo_temp.png', use_column_width=True)
    st.sidebar.header("Search options")
    neighborhood = st.selectbox("NYC neighborhood:", get_neighborhoods()['neighborhood'])
    st.markdown(
        """
# Halal-o-meter (LOGO will go somewhere)

Are you wondering what halal options are around NYC neighborhoods?

We provide a halal-reliability scroe based on reviews of the restaurants.
We even have a dark theme?
"""
    )

    select_block_container_style()
    ## filters
    # repalce with radius setting that will use coordinate data cached in dataframe
    # add checkbox options in sidebar (open now, has delivery)
    # replace this one with reliability store cutoff selection
    ## sort
    # add sort bar to change order in grid
    ## functionality
    # add possibility to improve reliability score? feedback?
    # add_resources_section()

    # My preliminary idea of an API for generating a grid
    with Grid("1 1 1", color=COLOR, background_color=BACKGROUND_COLOR) as grid:
        for i, row in get_dataframe().iterrows():
            grid.cell(chr(i + 97), 1, 2, i+1, i+1).image_card(name='. '.join([str(i+1),row['name']]), address=row.address, score=str(row.score), image_url=row.image_url)
        # grid.cell('map', 2, 4, 1, 3).dataframe(get_neighborhoods[:10])
        # grid.cell("b", 2, 3, 2, 3).text("The cell to the left is a dataframe")
        # grid.cell("c", 3, 4, 2, 3).plotly_chart(get_plotly_fig())
        # grid.cell('e', 1, 2, 4, 4).dataframe(get_dataframe())

    df = get_neighborhoods().iloc[:, 2:]
    df.columns = ['lat', 'lon']
    st.map(df)
main()
