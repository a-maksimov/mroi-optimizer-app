import streamlit as st
from collections import defaultdict
import read_data

periodicity_dict = {
    'Неделя': 'Weekly',
    'Месяц': 'Monthly',
    'Год': 'Yearly',
}


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


def clear_multi():
    """Resets widgets with Session State API"""
    st.session_state['Выберите гранулярность'] = []
    st.session_state['Выберите гранулярность_checkbox'] = False
    st.session_state['Выберите источники данных'] = []
    st.session_state['Выберите медиа-каналы'] = []
    st.session_state['Выберите медиа-форматы'] = []
    st.session_state['Выберите продукты'] = []
    return


def create_multiselect(label, options, default=None, value=False) -> list:
    """
    Creates multiselect with the 'Check all' checkbox underneath
    label (string): label of the multiselect and the key of the checkbox
    options (list): options for the multiselect
    default (list): default options for the multiselect
    value (bool): default value of the checkbox
    """
    container = st.sidebar.container()
    select_all = st.sidebar.checkbox('Выбрать все', value=value, key=label + '_checkbox')

    if select_all:
        ms = container.multiselect(
            label,
            options=options,
            default=options,
            key=label
        )
    else:
        ms = container.multiselect(
            label,
            options=options,
            default=default,
            key=label
        )
    return ms


def render_sidebar(dataframe):
    st.sidebar.header('Пользовательский ввод')
    selection_dict = defaultdict(list)

    # Create date range input widget
    start_date, end_date = render_date(dataframe)
    selection_dict.update({'Start_date': start_date, 'End_date': end_date})
    periodicity = st.sidebar.selectbox(
        'Выберите периодичность',
        options=['Неделя', 'Месяц', 'Год'],
        index=0
    )
    selection_dict['Periodicity'] = periodicity_dict[periodicity]

    # Create button to clear the multiselect widgets
    st.sidebar.button('Очистить все', on_click=clear_multi)

    # Create filters
    granularity = create_multiselect('Выберите гранулярность', read_data.granularity_levels)

    if 'Dealership' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe, 'Dealership')
        dealerships = create_multiselect('Выберите источники данных', granularity_list)
        selection_dict['Dealership'] = dealerships

    if 'Channel' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Channel',
                                                              selection_dict
                                                              )
        selection_dict['Channel'] = create_multiselect('Выберите медиа-каналы', granularity_list)

    if 'Format' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Format',
                                                              selection_dict
                                                              )
        selection_dict['Format'] = create_multiselect('Выберите медиа-форматы', granularity_list)

    if 'Product' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Product',
                                                              selection_dict
                                                              )
        selection_dict['Product'] = create_multiselect('Выберите продукты', granularity_list)

    return selection_dict
