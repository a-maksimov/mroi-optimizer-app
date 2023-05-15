import os
import streamlit as st


def about_page():
    # if Russian
    if st.session_state['language'] == 'Русский' or st.session_state['language_switch_counter'] % 2 == 0:
        with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
    else:
        with open(os.getcwd() + '/options_menu/about_en.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
