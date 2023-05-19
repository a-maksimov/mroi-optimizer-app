import os
import streamlit as st


# TODO: Write about periodicity and hint on planning with higher periodicity.
#       Write about Optimization.
#       Write hint and warning about optimizing outside +/- 30% of current spends.
def about_page():
    # if Russian
    if st.session_state['language'] == 'Русский' or not st.session_state['language_switch']:
        with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
    else:
        with open(os.getcwd() + '/options_menu/about_en.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
