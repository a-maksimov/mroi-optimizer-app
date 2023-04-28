import streamlit as st
from translations import _
from options_menu.specification_tabs import tab_table, tab_plotting


def spec_page(df_display):
    """ Renders the specification page by user selections in the sidebar """
    # load the selected table and also render sidebar inside render_spec()

    # top KPIs
    total_spend = df_display[_('Spend')].sum()
    total_contribution = df_display[_('Contribution')].sum()
    total_revenue = df_display[_('Revenue_Calculated')].sum()
    total_romi = total_revenue / total_spend

    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        st.subheader(_('Total budget'))
        st.subheader(f'€ {round(total_spend / 1e6, 2)}' + ' ' + _('M'))
    with middle_column1:
        st.subheader(_('Total contribution'))
        st.subheader(f'{round(total_contribution / 1000, 2)}' + ' ' + _('k') + ' ' + _('kg'))
    with middle_column2:
        st.subheader(_('Total calculated revenue'))
        st.subheader(f'€ {round(total_revenue / 1e6, 2)}' + ' ' + _('M'))
    with right_column:
        st.subheader('MROI:')
        st.subheader(f'{round(total_romi, 2)}')

    st.markdown('''---''')

    # Create a tab layout
    tabs = st.tabs([_('Table'), _('Plotting')])

    # define the content of the first tab: Table
    with tabs[0]:
        tab_table.spec_table_tab(df_display)

    # define the content of the second tab: Plotting
    with tabs[1]:
        tab_plotting.spec_plotting_tab(df_display)

    return spec_page
