import streamlit as st
from translations import _
import utils
from options_menu.planning_tabs import tab_table, tab_plotting


def plan_page(plan):
    """
    Renders the Planning page based on the Specification page
    plan (tuple): a tuple of a planned budget and transformed dataframe
    """
    planned_budget, df_plan = plan

    # top metrics
    simulated_total_contribution = df_plan[_('Simulated Contribution')].sum()
    simulated_total_revenue = df_plan[_('Simulated Revenue')].sum()
    simulated_total_mroi = simulated_total_revenue / planned_budget

    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        st.metric(_('Simulated Budget'),
                  value=utils.display_currency(planned_budget),
                  delta=utils.display_percent(st.session_state['budget'], planned_budget))
        # to preserve value after the page switch
        st.session_state['display_planned_budget'] = planned_budget
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

    st.markdown('''---''')

    # Create a tab layout
    tabs = st.tabs([_('Table'), _('Plotting')])

    # define the content of the first tab: Table
    with tabs[0]:
        tab_table.plan_table_tab(df_plan)

    # define the content of the second tab: Plotting
    with tabs[1]:
        pass
