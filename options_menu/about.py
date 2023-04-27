import os
import streamlit as st


def about_page():
    with open(os.getcwd() + '/options_menu/about_ru.txt', 'r', encoding='utf-8') as file:
        st.markdown(file.read())
    return about_page
