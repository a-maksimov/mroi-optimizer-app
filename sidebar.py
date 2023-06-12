import streamlit as st
from collections import defaultdict
import translations
from translations import _, set_language
from config import data
import read_data
from calculate_spec import top_metrics
from calculate_spec import calculate_spec
from options_menu.planning import reset_planning
from options_menu.optimization import reset_optimization


def handle_periodicity():
    """ Callback function on change of periodicity multiselect """
    # reset simulated data trigger in session state
    reset_planning()

    # update displayed value in planned budget input textbox widget
    if 'display_planned_budget' in st.session_state['tracking']:
        st.session_state['tracking']['display_planned_budget'] = st.session_state['tracking']['budget']

    # delete optimized dataframe if it is in the session state
    reset_optimization()

    # save selected periodicity index
    periodicity_list = [_(periodicity) for periodicity in read_data.periodicity_list]
    st.session_state['tracking']['periodicity_track'] = periodicity_list.index(st.session_state['periodicity'])


def multiselect_callback(key, options, by_checkbox=False):
    """
    Callback function of multiselect widgets in the sidebar.
    This function recalculates the top metrics after user interactions with sidebar.
    The Planning and Optimization become reset.
    It also changes the value of corresponding Select All checkbox to False.
    """
    # reset specification and delete optimized dataframe kept in session state
    # after changing selections in sidebar

    # reset simulated data trigger in session state
    reset_planning()

    # delete optimized dataframe if it is in the session state
    reset_optimization()

    # load the transformed and translated dataframe
    dataframe = read_data.read_data(data)

    # get granularity levels
    granularity_levels = [_(level) for level in read_data.granularity_levels]

    # get the old selection_dict
    selection_dict = st.session_state['tracking']['selection_dict']

    if not by_checkbox:
        # if called by multiselect
        level_to_key = {
            _('Dealership'): 'dealership',
            _('Channel'): 'channel',
            _('Format'): 'format',
            _('Product'): 'product'
        }
        # update selection dict based on new selections in the sidebar
        selection_dict.update({level: st.session_state[level_to_key[level]] for level in granularity_levels
                               if level_to_key[level] in st.session_state})
    else:
        # if called by checkbox
        key_to_level = {
            'dealership': _('Dealership'),
            'channel': _('Channel'),
            'format': _('Format'),
            'product': _('Product')
        }
        if key in key_to_level:
            selection_dict.update({key_to_level[key]: options})

    # calculate top metrics
    updated_budget, updated_contribution, updated_revenue, updated_mroi = top_metrics(
        calculate_spec(dataframe, selection_dict))

    # update values in the session_state to display them in the Optimisation page
    st.session_state['tracking']['budget'] = updated_budget
    st.session_state['tracking']['contribution'] = updated_contribution
    st.session_state['tracking']['revenue'] = updated_revenue
    st.session_state['tracking']['mroi'] = updated_mroi

    # update displayed value in planned budget input textbox widget
    if 'display_planned_budget' in st.session_state['tracking']:
        st.session_state['tracking']['display_planned_budget'] = updated_budget

    # if called by multiselect
    if not by_checkbox:
        # uncheck Select All checkbox
        st.session_state['tracking'][key + '_checkbox' + '_track'] = False

        # if the widget wasn't deleted after some sidebar manipulations
        if key in st.session_state:
            # update multiselect traker
            st.session_state['tracking'][key + '_track'] = st.session_state[key]
        else:
            st.session_state['tracking'][key + '_track'] = []


def render_language():
    # language UI
    # set the default value after re-render of widget
    # 'language_switch' value changes after set_language() callback
    if 'language_switch' not in st.session_state['tracking']:
        st.session_state['tracking']['language_switch'] = 0
    # set up the translation selection
    return st.sidebar.selectbox(_('Language'),
                                index=st.session_state['tracking']['language_switch'],
                                options=translations.languages,
                                key='language',
                                on_change=set_language)


def create_date_range(selected_date_range, full_date_range, key='date_range'):
    start_date, end_date = full_date_range
    date_range = st.sidebar.date_input(
        _('Select analysis date range'),
        min_value=start_date,
        max_value=end_date,
        value=selected_date_range,
        key=key
    )
    if len(date_range) != 2:
        st.stop()
    else:
        return date_range


def render_date(dataframe):
    # get full date range
    # cast to datetime for comparison
    start_date = dataframe['Date'].min().date()
    end_date = dataframe['Date'].max().date()
    full_date_range = start_date, end_date

    # initialize date range tracking
    if 'date_range_track' not in st.session_state['tracking']:
        st.session_state['tracking']['date_range_track'] = full_date_range

    # create initial date_range input widget
    date_range_placeholder = st.sidebar.empty()
    with date_range_placeholder:
        date_range = create_date_range(st.session_state['tracking']['date_range_track'], full_date_range)

    # if selected date range is different from the one that stored in session state
    if sorted(st.session_state['tracking']['date_range_track']) != sorted(date_range):
        # save newly selected date range in session state
        st.session_state['tracking']['date_range_track'] = date_range
        # reset planning
        reset_planning()
        # reset optimization
        reset_optimization()
        # delete the old date input widget
        del st.session_state['date_range']
        date_range_placeholder.empty()
        # need a rerun before the old date input gets deleted
        st.experimental_rerun()
        # create new date range widget with the default value from the output of the old date range input
        # this will maintain the selected date in between re-renderings
        date_range = create_date_range(date_range, full_date_range, key='new_date_range')

    return date_range


def clear_all():
    """ Callback function of Clear All button. Resets multiselect widgets and checkboxes """
    keys = ['product', 'format', 'channel', 'dealership', 'granularity']
    for key in keys:
        # clear all multiselect widgets
        st.session_state['tracking'][key + '_track'] = []
        # uncheck Select all checkboxes
        st.session_state['tracking'][key + '_checkbox_track'] = False


def clear_all_button():
    """ Creates Clear All button"""
    # create button to clear the multiselect widgets
    st.sidebar.button(_('Clear all'), key='clear_all', on_click=clear_all)


def flip_checkbox_track(key, options):
    """ Callback function that is called on sidebar checkboxes change and tracks its values in between re-rendering """
    key_checkbox_track = key + '_checkbox' + '_track'

    # flip the checkbox tracked value
    st.session_state['tracking'][key_checkbox_track] = not st.session_state['tracking'][key_checkbox_track]

    # if Select All is checked
    if st.session_state['tracking'][key_checkbox_track]:
        key_track = key + '_track'
        st.session_state['tracking'][key_track] = options

        # recalculate spec if multiselect changed after Select All was checked
        if not st.session_state[key] == st.session_state['tracking'][key_track]:
            multiselect_callback(key, options, by_checkbox=True)


def create_checkbox(key, options):
    """ Create Select All checkbox """
    # initialize checkbox value tracking
    key_checkbox = key + '_checkbox'
    key_checkbox_track = key_checkbox + '_track'
    if key_checkbox_track not in st.session_state['tracking']:
        st.session_state['tracking'][key_checkbox_track] = False

    # create Select All checkbox
    st.sidebar.checkbox(_('Select all'),
                        value=st.session_state['tracking'][key_checkbox_track],
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

    # initialize multiselect selected options tracking
    key_track = key + '_track'
    if key_track not in st.session_state['tracking']:
        st.session_state['tracking'][key_track] = []

    key_checkbox_track = key + '_checkbox_track'
    # if select all is checked
    if st.session_state['tracking'][key_checkbox_track]:
        default = options
    else:
        # options is what CAN be selected after interactions with other multiselect widgets
        # st.session_state[key_track] is what was selected and saved in the session state before
        default = list(set(st.session_state['tracking'][key_track]).intersection(options))
    with container:
        ms = st.multiselect(label,
                            options=options,
                            default=default,
                            key=key,
                            on_change=multiselect_callback,
                            args=(key, options))
    # ensure multiselect tracking
    st.session_state['tracking'][key_track] = ms
    return ms


def render_sidebar(dataframe):
    """ Renders the sidebar and returns a dictionary of user selections """

    # render language selection widget
    render_language()

    st.sidebar.header(_('User inputs'))

    selection_dict = defaultdict(list)

    # create date range input widget
    date_range = render_date(dataframe)
    selection_dict.update({'date_range': date_range})

    # TODO: reset planning and optimization on change of periodicity
    # create periodicity selection widget
    if 'periodicity_track' not in st.session_state['tracking']:
        st.session_state['tracking']['periodicity_track'] = 2
    periodicity = st.sidebar.selectbox(
        _('Select periodicity'),
        options=[_(periodicity) for periodicity in read_data.periodicity_list],
        index=st.session_state['tracking']['periodicity_track'],
        key='periodicity',
        on_change=handle_periodicity
    )
    selection_dict['Periodicity'] = periodicity

    clear_all_button()

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
        if granularity_list:
            selection_dict[_('Dealership')] = create_multiselect(label=_('Select dealerships'),
                                                                 key='dealership',
                                                                 options=granularity_list)

    if _('Channel') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Channel'),
                                                              selection_dict
                                                              )
        if granularity_list:
            selection_dict[_('Channel')] = create_multiselect(label=_('Select channels'),
                                                              key='channel',
                                                              options=granularity_list)

    if _('Format') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Format'),
                                                              selection_dict
                                                              )
        if granularity_list:
            selection_dict[_('Format')] = create_multiselect(label=_('Select formats'),
                                                             key='format',
                                                             options=granularity_list)

    if _('Product') in granularity:
        granularity_list = read_data.get_level_of_granularity(dataframe,
                                                              _('Product'),
                                                              selection_dict
                                                              )
        if granularity_list:
            selection_dict[_('Product')] = create_multiselect(label=_('Select products'),
                                                              key='product',
                                                              options=granularity_list)

    # save selection dict to the session state for future uses
    st.session_state['tracking']['selection_dict'] = selection_dict

    return selection_dict
