'''
streamlit classes to enable custom grid styling
'''

import streamlit as st
from typing import List, Optional
import markdown
import pandas as pd

# move to config file
COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'

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
        self.inner_html = ''

    def _to_style(self) -> str:
        return f"""
        .{self.class_} {{
        grid-column-start: {self.grid_column_start};
        grid-column-end: {self.grid_column_end};
        grid-row-start: {self.grid_row_start};
        grid-row-end: {self.grid_row_end};
        }}"""

    def text(self, text: str = ''):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)

    def dataframe(self, dataframe: pd.DataFrame):
        self.inner_html = dataframe.to_html()

    def image(self, url):
        self.inner_html = '<img src ="' + url +'"/>'

    def image_card(self, name, address, score, image_url, url):
        crescent = ''
        for i in range(int(score)): crescent += '<img src="https://cdn.onlinewebfonts.com/svg/img_39469.png"/>'
        self.inner_html = '<div class="flex">'\
        +'<div class="main-image" style="backgroundImage: url(' + image_url +');"></div>'\
        + '<div class="main-body">'\
        + '<h3><a href="'+ url +'">'+ name +'</a></h3>'\
        + '<p class="crescent">'+ crescent + '</p>'\
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
        template_columns='1 1 1',
        gap='10px',
        background_color=BACKGROUND_COLOR,
        color=COLOR,
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
                    width: 200px;
                    height: 200px;
                    background-size: cover;
                    border-radius: 10px;
                    margin-right: 12px;
                }}
                .box .crescent {{
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
                .box .main-body h3 a{{
                    color: #000;
                    text-decoration: none;
                }}
                .box .address {{
                    width: 150px;
                }}
                .box .crescent img {{
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
                    background-color: #ff8b9c !important;
                    border: 1px solid #ff8b9c;
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
