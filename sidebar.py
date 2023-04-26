import streamlit as st
from datetime import datetime
from collections import defaultdict
import read_data

date_format = '%d.%m.%Y'


def render_date(dataframe):
    # Date UI
    start_date = dataframe['Date'].min()
    end_date = dataframe['Date'].max()
    date_range = st.sidebar.date_input(
        'Выберите интервал анализа',
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        key='date_range'
    )
    return date_range


def render_sidebar(dataframe):
    st.sidebar.header('Пользовательский ввод')
    selection_dict = defaultdict(list)

    # Create date range input widget
    start_date, end_date = render_date(dataframe)
    selection_dict.update({'Start_date': start_date, 'End_date': end_date})

    # Create filters
    granularity_dict = read_data.get_levels_of_granularity(dataframe)
    periodicity = st.sidebar.selectbox(
        'Выберите периодичность',
        options=['Weekly', 'Monthly', 'Yearly'],
        index=0
    )
    selection_dict['Periodicity'] = periodicity

    granularity = st.sidebar.multiselect(
        'Выберите гранулярность',
        options=granularity_dict,
        default='Channel'
    )

    if 'Channel' in granularity:
        channels = st.sidebar.multiselect(
            'Выберите медиа-каналы',
            options=granularity_dict['Channel'],
        )
        selection_dict['Channel'] = channels

    if 'Dealership' in granularity:
        dealerships = st.sidebar.multiselect(
            'Выберите источники данных',
            options=granularity_dict['Dealership'],
        )
        selection_dict['Dealership'] = dealerships

    if 'Format' in granularity:
        formats = st.sidebar.multiselect(
            'Выберите медиа-форматы',
            options=granularity_dict['Format'],
        )
        selection_dict['Format'] = formats

    if 'Product' in granularity:
        products = st.sidebar.multiselect(
            'Выберите продукты',
            options=granularity_dict['Product'],
        )
        selection_dict['Product'] = products

    return selection_dict
