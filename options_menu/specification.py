import streamlit as st
from translations import _
import utils
from options_menu.specification_tabs import tab_table, tab_plotting


def spec_page(df_display):
    """
    Renders the Specification page by user selections in the sidebar
    returns tuple of top metrics
    """
    # top metrics
    total_spend = df_display[_('Spend')].sum()
    total_contribution = df_display[_('Contribution')].sum()
    total_revenue = df_display[_('Revenue Calculated')].sum()
    total_mroi = total_revenue / total_spend

    # save top metrics for planning calculations
    st.session_state.update({
        'budget': total_spend,
        'contribution': total_contribution,
        'revenue': total_revenue,
        'mroi': total_mroi
    })

    # render top metrics
    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        st.metric(_('Total budget'), value=utils.display_currency(total_spend))
    with middle_column1:
        st.metric(_('Total contribution'), value=utils.display_volume(total_contribution))
    with middle_column2:
        st.metric(_('Total calculated revenue'), value=utils.display_currency(total_revenue))
    with right_column:
        st.metric('MROI', value=f'{round(total_mroi, 2)}')

    st.markdown('''---''')

    # create a tab layout
    tabs = st.tabs([_('Table'), _('Plotting')])

    # define the content of the first tab: Table
    with tabs[0]:
        tab_table.spec_table_tab(df_display)

    # define the content of the second tab: Plotting
    with tabs[1]:
        tab_plotting.spec_plotting_tab(df_display)
