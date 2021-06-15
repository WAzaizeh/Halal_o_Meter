import streamlit as st

COLOR = 'black'
BACKGROUND_COLOR = '#fffafa'

def _set_block_container_style(
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 5,
    ):
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
        .reportview-container .markdown-text-container {{
            width: 40vw !important;
        }}
        .reportview-container .main .block-container .element-container:nth-child(10) {{
            width: 38% !important;
            position: fixed;
            top: 150px;
            left: 62vw;
            border-radius: 5px;
            overflow: hidden;
            height: 100vh;
            padding-right: 10px;
        }}
        .reportview-container hr {{
            margin: 0;
        }}
        .sidebar .sidebar-content {{
            background-color: #e5e7ea;
            background-image: none;
            padding: 12px 6px;
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
        unsafe_allow_html=True,)
