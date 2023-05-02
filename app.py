import streamlit as st
from translations import _
from options_menu import menu, about, specification, planning
from read_data import read_data
from sidebar import render_sidebar
from calculate_spec import calculate_spec
from calculate_plan import calculate_plan

st.set_page_config(page_title='MROI Optimizer App',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')

st.title(':chart_with_upwards_trend: MROI Optimizer App')
st.markdown("##")

# results of MMM modeling
input_file = 'data/mmm_hierarchy.csv'

# load the transformed and translated dataframe
df = read_data(input_file)

# create sidebar
selection_dict = render_sidebar(df)

# create options menu
selected = menu.menu()

# create pages
if selected == _('About'):
    about.about_page()
if selected == _('Specification'):
    specification.spec_page(calculate_spec(df, selection_dict))
if selected == _('Planning'):
    planning.plan_page(calculate_plan(calculate_spec(df, selection_dict)))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
