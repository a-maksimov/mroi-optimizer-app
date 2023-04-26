import streamlit as st
from options_menu import menu, about, specification

st.set_page_config(page_title='MROI Optimizer App',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')

st.title(':chart_with_upwards_trend: MROI Optimizer App')
st.markdown("##")

selected = menu.menu()

if selected == 'О приложении':
    about.about_page()
if selected == 'Спецификация':
    specification.spec_page()
if selected == 'Планирование':
    st.title(f'Вы выбрали "{selected}"')