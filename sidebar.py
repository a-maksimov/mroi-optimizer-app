import streamlit as st
from collections import defaultdict
from translations import _, set_language
import read_data
from calculate_spec import top_metrics
from calculate_spec import calculate_spec


def multiselect_callback(key):
    """
    Callback function of multiselect widgets in the sidebar.

    This function updates the value of the planned budget on change of sidebar widgets.
    The purpose of this function is to "reset" the top metrics on the Optimisation page if sidebar changes.

    It also changes the value of corresponding Select All checkbox to False
    """
    # do if Planning page is selected
    if st.session_state['menu_tracker'] == 2:
        # dictionary for updating selection_dict in st.session state
        level_to_key = {
            _('Dealership'): 'dealership',
            _('Channel'): 'channel',
            _('Format'): 'format',
            _('Product'): 'product'
        }
        # update plan
        # results of MMM modeling
        input_file = 'data/mmm_hierarchy.csv'

        # load the transformed and translated dataframe
        df = read_data.read_data(input_file)

        # get granularity levels
        granularity_levels = [_(level) for level in read_data.granularity_levels]

        # get the old selection_dict
        selection_dict = st.session_state['selection_dict']

        # update selection dict based on new selections in the sidebar
        selection_dict.update({level: st.session_state[level_to_key[level]] for level in granularity_levels
                               if level_to_key[level] in st.session_state})

        # calculate top metrics
        updated_budget, updated_contribution, updated_revenue, updated_mroi = top_metrics(calculate_spec(df, selection_dict))

        # update values in the session_state to display them in the Optimisation page
        st.session_state['budget'] = updated_budget
        st.session_state['contribution'] = updated_contribution
        st.session_state['revenue'] = updated_revenue
        st.session_state['mroi'] = updated_mroi
        if 'display_planned_budget' in st.session_state:
            st.session_state['display_planned_budget'] = updated_budget

    # uncheck Select All checkbox
    st.session_state[key + '_checkbox' + '_track'] = False

    # track selected options
    st.session_state[key + '_track'] = st.session_state[key]


def render_language():
    # language UI
    languages = ['Русский', 'English']
    # set the default value after re-render of widget
    # 'language_switch_counter' value changes after set_language() callback
    if 'language_switch_counter' in st.session_state:
        default = st.session_state['language_switch_counter'] % 2
    else:
        default = 0
    # set up the translation selection
    return st.sidebar.selectbox(_('Language'), index=default, options=languages, key='language', on_change=set_language)


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
    """ Callback function of Clear All button. Resets multiselect widgets and checkboxes """
    keys = ['product', 'format', 'channel', 'dealership', 'granularity']
    for key in keys:
        # clear all multiselect widgets
        st.session_state[key + '_track'] = []
        # uncheck Select all checkboxes
        st.session_state[key + '_checkbox_track'] = False


def flip_checkbox_track(key, options):
    """ Callback function that is called on sidebar checkboxes change and tracks its values in between re-rendering """
    key_checkbox_track = key + '_checkbox' + '_track'

    # flip the checkbox tracked value
    st.session_state[key_checkbox_track] = not st.session_state[key_checkbox_track]

    # if Select All is checked
    if st.session_state[key_checkbox_track]:
        key_track = key + '_track'
        # update multiselect selected options to all
        st.session_state[key_track] = options


def create_checkbox(key, options):
    """ Create Select All checkbox """
    # initiate checkbox value tracking
    key_checkbox = key + '_checkbox'
    key_checkbox_track = key_checkbox + '_track'
    if key_checkbox_track not in st.session_state:
        st.session_state[key_checkbox_track] = False

    if key_checkbox in st.session_state:
        if st.session_state[key_checkbox] != st.session_state[key_checkbox_track]:
            # delete the old checkbox before creating a new one, because it's value glitches inbetween re-rendering
            del st.session_state[key_checkbox]

    # create Select All checkbox
    st.sidebar.checkbox(_('Select all'),
                        value=st.session_state[key_checkbox_track],
                        key=key_checkbox,
                        on_change=flip_checkbox_track,
                        args=(key, options))


def create_multiselect(label, key, options):
    """
    Creates multiselect with the 'Check all' checkbox underneath
    label (string): label of the multiselect and the key of the checkbox
    key (string): unique key for multiselect element
    options (list): options for the multiselect
    """
    # create container for multiselect
    container = st.sidebar.container()

    # create Select All checkbox widget
    create_checkbox(key, options)

    # initiate multiselect selected options tracking
    key_track = key + '_track'
    if key_track not in st.session_state:
        st.session_state[key_track] = []

    # if Select all is checked, use all options
    if st.session_state[key + '_checkbox_track']:
        default = options
    else:
        default = st.session_state[key_track]

    with container:
        # create multiselect widget
        ms = st.multiselect(label,
                            options=options,
                            default=default,
                            key=key,
                            on_change=multiselect_callback,
                            args=(key,))

    return ms


def render_sidebar(dataframe):
    """ Renders the sidebar and returns a dictionary of user selections """

    # render language selection widget
    render_language()

    st.sidebar.header(_('User inputs'))

    selection_dict = defaultdict(list)

    # create date range input widget
    start_date, end_date = render_date(dataframe)
    selection_dict.update({'Start_date': start_date, 'End_date': end_date})

    # create periodicity selection widget
    periodicity = st.sidebar.selectbox(
        _('Select Periodicity'),
        options=[_(periodicity) for periodicity in read_data.periodicity_list],
        index=0,
        key='periodicity'
    )
    selection_dict['Periodicity'] = periodicity

    # create button to clear the multiselect widgets
    st.sidebar.button(_('Clear all'), on_click=clear_multi)

    # create multiselect filters widgets
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    granularity = create_multiselect(label=_('Select granularity level'),
                                     key='granularity',
                                     options=granularity_levels)
    selection_dict['granularity'] = granularity

    if _('Dealership') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Dealership'),
                                                              selection_dict
                                                              )
        selection_dict[_('Dealership')] = create_multiselect(label=_('Select dealerships'),
                                                             key='dealership',
                                                             options=granularity_list)

    if _('Channel') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Channel'),
                                                              selection_dict
                                                              )
        selection_dict[_('Channel')] = create_multiselect(label=_('Select channels'),
                                                          key='channel',
                                                          options=granularity_list)

    if _('Format') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Format'),
                                                              selection_dict
                                                              )
        selection_dict[_('Format')] = create_multiselect(label=_('Select formats'),
                                                         key='format',
                                                         options=granularity_list)

    if _('Product') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Product'),
                                                              selection_dict
                                                              )
        selection_dict[_('Product')] = create_multiselect(label=_('Select products'),
                                                          key='product',
                                                          options=granularity_list)

    # save selection dict to the session state for future uses
    st.session_state['selection_dict'] = selection_dict

    return selection_dict
