import streamlit as st
from translations import _
import utils
from options_menu.specification_tabs import tab_table, tab_plotting


def spec_page(df_display):
    """ Renders the Specification page by user selections in the sidebar """
    # access top metrics calculated and saved in the session state by top_metrics() function call inside
    # calculate_spec
    total_spend = st.session_state['tracking']['budget']
    total_contribution = st.session_state['tracking']['contribution']
    total_revenue = st.session_state['tracking']['revenue']
    total_mroi = st.session_state['tracking']['mroi']

    # render top metrics
    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        st.metric(_('Total Budget'), value=utils.display_currency(total_spend))
    with middle_column1:
        st.metric(_('Total Contribution'), value=utils.display_volume(total_contribution))
    with middle_column2:
        st.metric(_('Total Calculated Revenue'), value=utils.display_currency(total_revenue))
    with right_column:
        st.metric('MROI', value=f'{round(total_mroi, 2)}')

    # create a tab layout
    tabs = st.tabs([_('Plotting'), _('Table')])

    # define the content of the first tab: Plotting
    with tabs[0]:
        tab_plotting.spec_plotting_tab(df_display)

    # define the content of the second tab: Table
    with tabs[1]:
        tab_table.spec_table_tab(df_display)
