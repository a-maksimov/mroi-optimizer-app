import streamlit as st
from translations import _
from options_menu import menu, about, specification, planning, optimization
from config import data
from read_data import read_data
from sidebar import render_sidebar
from calculate_spec import calculate_spec
from calculate_plan import calculate_plan
from calculate_opt import calculate_opt

st.set_page_config(page_title='MROI Optimizer App',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')

st.title(':chart_with_upwards_trend: MROI Optimizer App')

st.divider()

# initialize dictionary in session state for app state tracking
if 'tracking' not in st.session_state:
    st.session_state['tracking'] = dict()

# load the transformed and translated dataframe
df = read_data(data)

# create options menu
selected = menu.menu()

# initialize tracking menu
if 'menu_track' not in st.session_state['tracking']:
    st.session_state['tracking']['menu_track'] = _('Specification')
st.session_state['tracking']['menu_track'] = selected

# create sidebar
selection_dict = render_sidebar(df)

# create pages
if selected == _('About'):
    about.about_page()

if selected == _('Specification'):
    with st.spinner(f'{_("Loading")}...'):
        specification.spec_page(
            calculate_spec(df, selection_dict))

if selected == _('Analyze'):
    with st.spinner(f'{_("Loading")}...'):
        planning.plan_page(
            calculate_plan(
                calculate_spec(df, selection_dict)))

if selected == _('Optimization'):
    with st.spinner(f'{_("Loading")}...'):
        optimization.opt_page(
            calculate_opt(
                calculate_plan(
                    calculate_spec(df, selection_dict))))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
