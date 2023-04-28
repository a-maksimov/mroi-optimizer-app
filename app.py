import streamlit as st
from translations import _
from options_menu import menu, about, specification

st.set_page_config(page_title='MROI Optimizer App',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')

st.title(':chart_with_upwards_trend: MROI Optimizer App')
st.markdown("##")

# create options menu
selected = menu.menu()

# create pages
if selected == _('About'):
    about.about_page()
if selected == _('Specification'):
    specification.spec_page()
if selected == _('Planning'):
    st.title(f'{selected}')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
