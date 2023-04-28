import streamlit as st
from collections import defaultdict
from translations import _, set_language
import read_data

languages = {'Русский': 'ru_RU', 'English': 'en_US'}


def render_date(dataframe):
    # Date UI
    start_date = dataframe['Date'].min()
    end_date = dataframe['Date'].max()
    date_range = st.sidebar.date_input(
        _('Select analysis date range'),
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        key='date_range'
    )
    return date_range


def clear_multi():
    """ Resets widgets with Session State API """
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
    select_all = st.sidebar.checkbox(_('Select all'), value=value, key=key + '_checkbox')

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
    # set up the translation selection
    language = st.sidebar.selectbox(_('Language'), languages, key='language')

    # update the translation object based on the selected language
    if language:
        set_language(languages[language])

    st.sidebar.header(_('User inputs'))

    selection_dict = defaultdict(list)

    # Create date range input widget
    start_date, end_date = render_date(dataframe)
    selection_dict.update({'Start_date': start_date, 'End_date': end_date})
    periodicity = st.sidebar.selectbox(
        _('Select Periodicity'),
        options=[_(periodicity) for periodicity in read_data.periodicity_list],
        index=0
    )
    selection_dict['Periodicity'] = periodicity

    # Create button to clear the multiselect widgets
    st.sidebar.button(_('Clear all'), on_click=clear_multi)

    # Create filters
    granularity = create_multiselect(_('Select granularity'), 'granularity', read_data.granularity_levels)

    if 'Dealership' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe, 'Dealership')
        dealerships = create_multiselect(_('Select dealerships'), 'dealerships', granularity_list)
        selection_dict['Dealership'] = dealerships

    if 'Channel' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Channel',
                                                              selection_dict
                                                              )
        selection_dict['Channel'] = create_multiselect(_('Select channels'), 'channels', granularity_list)

    if 'Format' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Format',
                                                              selection_dict
                                                              )
        selection_dict['Format'] = create_multiselect(_('Select_formats'), 'formats', granularity_list)

    if 'Product' in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              'Product',
                                                              selection_dict
                                                              )
        selection_dict['Product'] = create_multiselect(_('Select products'), 'products', granularity_list)

    return selection_dict
