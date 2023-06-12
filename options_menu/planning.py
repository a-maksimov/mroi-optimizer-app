import streamlit as st
from translations import _
import utils
from options_menu.planning_tabs import tab_table, tab_plotting, tab_rc


def reset_planning():
    """
    Resets optimization by flipping the 'simulated' in session state to False.
    This function is called when user makes changes in the sidebar.
    """
    # this trigger is first set to True on a callback with changing the planned budget field on the Planning page
    if 'simulated' in st.session_state['tracking']:
        st.session_state['tracking']['simulated'] = False


def handle_plan_input():
    """
    Callback for planned budget input text widget
    Validates input on the edit of field and if correct, saves new value to the session state
    """
    # flip trigger for simulated spend to add markers on the response curves
    st.session_state['tracking']['simulated'] = True

    parsed_planned_budget = utils.parse_input(st.session_state['planned_budget'])

    # display_planned_budget is initialized in the calculate_plan
    if 'display_planned_budget' in st.session_state['tracking']:
        st.session_state['tracking']['display_planned_budget'] = parsed_planned_budget

    # reset optimization by deleting the optimized dataframe from session state
    if 'df_optimized' in st.session_state['tracking']:
        del st.session_state['tracking']['df_optimized']


# TODO: Make planned budget input widget more user friendly: scaling and validation.
def plan_input():
    """
    Input for planned budget.
    Validates user input and returns the value.
    """
    # display_planned_budget is initialized in the calculate_plan
    default_value = st.session_state['tracking']['display_planned_budget']
    default_value = '{:.2f}'.format(default_value)

    st.text_input(f'{_("Enter planned budget") + ", €"}',
                  value=default_value,
                  key='planned_budget',
                  on_change=handle_plan_input)

    default_value = float(default_value)

    if default_value > st.session_state['tracking']['display_planned_budget'] * 2:
        st.error(_('Error: Number too large.'))
        return 0

    return default_value


# TODO: Add reset button to fallback to Specification budget.
#  Now everything resets by user manipulations with sidebar.
def plan_page(dataframe):
    """ Renders the Planning page based on the Specification page """
    # access simulated top metrics calculated and saved in the session state by simulated_top_metrics() function
    # call inside calculate_plan
    simulated_total_contribution = st.session_state['tracking']['simulated_contribution']
    simulated_total_revenue = st.session_state['tracking']['simulated_revenue']
    simulated_total_mroi = st.session_state['tracking']['simulated_mroi']

    # display text input for simulated budget
    input_col, *padding = st.columns(4)
    with input_col:
        planned_budget = plan_input()

    # display simulated top metrics
    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        # if Planning page was reloaded
        if 'budget' not in st.session_state['tracking']:
            budget = planned_budget
        else:
            budget = st.session_state['tracking']['budget']
        st.metric(_('Simulated Budget'),
                  value=utils.display_currency(planned_budget),
                  delta=utils.display_percent(budget, planned_budget))
    with middle_column1:
        st.metric(_('Simulated Contribution'),
                  value=utils.display_volume(simulated_total_contribution),
                  delta=utils.display_percent(st.session_state['tracking']['contribution'],
                                              simulated_total_contribution))
    with middle_column2:
        st.metric(_('Simulated Revenue'),
                  value=utils.display_currency(simulated_total_revenue),
                  delta=utils.display_percent(st.session_state['tracking']['revenue'], simulated_total_revenue))
    with right_column:
        st.metric('MROI',
                  value=f'{round(simulated_total_mroi, 2)}',
                  delta=utils.display_percent(st.session_state['tracking']['mroi'], simulated_total_mroi))

    # create a tab layout
    tabs = st.tabs([_('Plotting'), _('Response Curves'), _('Table')])

    # define the content of the third tab: Response Curves
    #  TODO: Guarantee colors for plots and markers (define palette)
    # define the content of the first tab: Plotting
    with tabs[0]:
        tab_plotting.plan_plotting_tab(dataframe)

    # define the content of the first tab: Response Curves
    with tabs[1]:
        tab_rc.plan_rc_tab(dataframe)

    # define the content of the third tab: Table
    with tabs[2]:
        tab_table.plan_table_tab(dataframe)
