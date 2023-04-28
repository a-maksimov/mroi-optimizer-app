import os
from translations import translation
import streamlit as st


def about_page():
    try:
        if translation.lang == 'ru':
            with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
                st.markdown(file.read())
    except AttributeError:
        with open(os.getcwd() + '/options_menu/about_en.txt', 'r', encoding='utf-8') as file:
            st.markdown(file.read())
    return about_page
