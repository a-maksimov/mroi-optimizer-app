import streamlit as st
from translations import _
import utils
from options_menu.planning_tabs import tab_table, tab_plotting, tab_rc


def handle_plan_input():
    """ Callback for planned budget input text widget """
    # update display_planned_budget in the session state with the new value from the input text
    # display_planned_budget is initialized in calculate_plan
    if 'display_planned_budget' in st.session_state:
        st.session_state['display_planned_budget'] = float(st.session_state['planned_budget'])


def plan_input():
    """ Input for planned budget """
    # 'display_planned_budget' is in the session state after calculate_plan
    input_planned_budget = st.text_input(f'{_("Enter planned budget") + ", €"}',
                                         value=st.session_state['display_planned_budget'],
                                         key='planned_budget',
                                         on_change=handle_plan_input)
    return float(input_planned_budget)


def plan_page(df_plan):
    """
    Renders the Planning page based on the Specification page
    plan (tuple): a tuple of a planned budget and transformed dataframe
    """
    input_col, *padding = st.columns(4)
    with input_col:
        planned_budget = plan_input()

    # top metrics
    simulated_total_contribution = df_plan[_('Simulated Contribution')].sum()
    simulated_total_revenue = df_plan[_('Simulated Revenue')].sum()
    simulated_total_mroi = simulated_total_revenue / planned_budget

    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        # if Planning page was reloaded
        if 'budget' not in st.session_state:
            budget = planned_budget
        else:
            budget = st.session_state['budget']
        st.metric(_('Simulated Budget'),
                  value=utils.display_currency(planned_budget),
                  delta=utils.display_percent(budget, planned_budget))
        # to preserve value after the page switch
    with middle_column1:
        st.metric(_('Simulated Contribution'),
                  value=utils.display_volume(simulated_total_contribution),
                  delta=utils.display_percent(st.session_state['contribution'], simulated_total_contribution))
    with middle_column2:
        st.metric(_('Simulated Revenue'),
                  value=utils.display_currency(simulated_total_revenue),
                  delta=utils.display_percent(st.session_state['revenue'], simulated_total_revenue))
    with right_column:
        st.metric('MROI',
                  value=f'{round(simulated_total_mroi, 2)}',
                  delta=utils.display_percent(st.session_state['mroi'], simulated_total_mroi))

    # Create a tab layout
    tabs = st.tabs([_('Table'), _('Plotting'), _('Response Curves')])

    # define the content of the first tab: Table
    with tabs[0]:
        tab_table.plan_table_tab(df_plan)

    # define the content of the second tab: Plotting
    with tabs[1]:
        tab_plotting.plan_plotting_tab(df_plan)

    # define the content of the third tab: Response Curves
    with tabs[2]:
        tab_rc.plan_rc_tab(df_plan)
