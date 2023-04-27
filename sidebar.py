import streamlit as st
from collections import defaultdict
import read_data


def render_date(dataframe):
    # Date UI
    start_date = dataframe['Date'].min()
    end_date = dataframe['Date'].max()
    if read_data.language == 'ru':
        label = 'Выберите интервал анализа'
    else:
        label = 'Select analysis date range'
    date_range = st.sidebar.date_input(
        label,
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        key='date_range'
    )
    return date_range


def clear_multi():
    """Resets widgets with Session State API"""
    st.session_state['granularity'] = []
    st.session_state['granularity_checkbox'] = False
    st.session_state['dealerships'] = []
    st.session_state['channels'] = []
    st.session_state['formats'] = []
    st.session_state['products'] = []
    return


def create_multiselect(label, key, options, default=None, value=False) -> list:
    """
    Creates multiselect with the 'Check all' checkbox underneath
    label (string): label of the multiselect and the key of the checkbox
    options (list): options for the multiselect
    default (list): default options for the multiselect
    value (bool): default value of the checkbox
    """
    container = st.sidebar.container()
    if read_data.language == 'ru':
        inner_label = 'Выбрать все'
    else:
        inner_label = 'Select all'
    select_all = st.sidebar.checkbox(inner_label, value=value, key=key + '_checkbox')

    if select_all:
        ms = container.multiselect(
            label,
            options=options,
            default=options,
            key=key
        )
    else:
        ms = container.multiselect(
            label,
            options=options,
            default=default,
            key=key
        )
    return ms


def render_sidebar(dataframe):
    if read_data.language == 'ru':
        label = 'Пользовательский ввод'
    else:
        label = 'User inputs'
    st.sidebar.header(label)
    selection_dict = defaultdict(list)

    # Create date range input widget
    start_date, end_date = render_date(dataframe)
    selection_dict.update({'Start_date': start_date, 'End_date': end_date})
    if read_data.language == 'ru':
        options = read_data.periodicity_dict.keys()
        label = 'Выберите периодичность'
    else:
        options = read_data.periodicity_dict.values()
        label = 'Select Periodicity'
    periodicity = st.sidebar.selectbox(
        label,
        options=options,
        index=0
    )
    selection_dict['Periodicity'] = periodicity

    # Create button to clear the multiselect widgets
    if read_data.language == 'ru':
        label = 'Очистить все'
    else:
        label = 'Clear all'
    st.sidebar.button(label, on_click=clear_multi)

    # Create filters
    granularity = create_multiselect('Выберите гранулярность', 'granularity', read_data.granularity_levels)

    if 'Dealership' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe, 'Dealership')
        if read_data.language == 'ru':
            label = 'Выберите источники данных'
        else:
            label = 'Select dealerships'
        dealerships = create_multiselect(label, 'dealerships', granularity_list)
        selection_dict['Dealership'] = dealerships

    if 'Channel' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Channel',
                                                              selection_dict
                                                              )
        if read_data.language == 'ru':
            label = 'Выберите медиа-каналы'
        else:
            label = 'Select channels'
        selection_dict['Channel'] = create_multiselect(label, 'channels', granularity_list)

    if 'Format' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Format',
                                                              selection_dict
                                                              )
        if read_data.language == 'ru':
            label = 'Выберите медиа-форматы'
        else:
            label = 'Select formats'
        selection_dict['Format'] = create_multiselect(label, 'formats', granularity_list)

    if 'Product' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Product',
                                                              selection_dict
                                                              )
        if read_data.language == 'ru':
            label = 'Выберите продукты'
        else:
            label = 'Select products'
        selection_dict['Product'] = create_multiselect(label, 'products', granularity_list)

    return selection_dict
