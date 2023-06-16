import os
import streamlit as st


def about_page():
    # if Russian
    if not st.session_state['tracking']['language_switch']:
        with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
    else:
        with open(os.getcwd() + '/options_menu/about_en.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
