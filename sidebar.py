import streamlit as st
from streamlit.errors import StreamlitAPIException
from collections import defaultdict
from translations import _, set_language
import read_data


def render_date(dataframe):
    # date UI
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
    """
    Resets widgets with Session State API
    """
    st.session_state['granularity'] = []
    st.session_state['dealerships'] = []
    st.session_state['channels'] = []
    st.session_state['formats'] = []
    st.session_state['products'] = []
    return


def create_multiselect(label, key, options) -> list:
    """
    Creates multiselect with the 'Check all' checkbox underneath
    label (string): label of the multiselect and the key of the checkbox
    key (string): unique key for multiselect element
    options (list): options for the multiselect
    """
    container = st.sidebar.container()
    # create Select All checkbox
    if key + '_checkbox' in st.session_state:
        checkbox_value = st.session_state[key + '_checkbox']
    else:
        checkbox_value = False
    select_all = st.sidebar.checkbox(_('Select all'), value=checkbox_value, key=key + '_checkbox')

    # create multiselect object
    # if language has changed, keep the values and translate them
    if key in st.session_state:
        if st.session_state['language'] == 'English':
            selected_options = [_(option, get_original=True) for option in st.session_state[key]]
        else:
            selected_options = [_(option) for option in st.session_state[key]]
    else:
        selected_options = []
    try:
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
                default=selected_options,
                key=key
            )
        return ms
    except StreamlitAPIException:
        return st.sidebar.write(_('This specification is impossible. Pick a new one.'))


def render_sidebar(dataframe):
    """Renders the sidebar and returns a dictionary of user selections """
    languages = {'Русский': 0, 'English': 1}
    # set up the translation selection
    if 'language' in st.session_state:
        index = languages[st.session_state['language']]
    else:
        index = languages['Русский']
    st.sidebar.selectbox(_('Language'), index=index, options=languages, key='language', on_change=set_language)

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

    # create filters
    granularity_levels = [_(level) for level in read_data.granularity_levels]

    granularity = create_multiselect(_('Select granularity'), 'granularity', granularity_levels)

    if _('Dealership') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe, _('Dealership'))
        dealerships = create_multiselect(_('Select dealerships'), 'dealerships', granularity_list)
        selection_dict[_('Dealership')] = dealerships

    if _('Channel') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Channel'),
                                                              selection_dict
                                                              )
        selection_dict[_('Channel')] = create_multiselect(_('Select channels'), 'channels', granularity_list)

    if _('Format') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Format'),
                                                              selection_dict
                                                              )
        selection_dict[_('Format')] = create_multiselect(_('Select formats'), 'formats', granularity_list)

    if _('Product') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Product'),
                                                              selection_dict
                                                              )
        selection_dict[_('Product')] = create_multiselect(_('Select products'), 'products', granularity_list)

    return selection_dict
