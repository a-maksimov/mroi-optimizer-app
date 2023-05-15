import os
import streamlit as st


def about_page():
    if st.session_state['language'] == 'Русский':
        with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
    else:
        with open(os.getcwd() + '/options_menu/about_en.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
