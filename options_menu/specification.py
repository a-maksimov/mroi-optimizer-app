import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from translations import _
import read_data
import render_spec


def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')


def spec_page():
    # load the selected table and also render sidebar inside render_spec()
    df_display = render_spec.render_spec(read_data.read_data())

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

    # Define the content of the first tab - Dataframe
    with tabs[0]:

        # format date strings and translate
        if df_display.index.name == _('Weekly'):
            df_display.index = df_display.index.strftime('%d-%m-%Y')
        elif df_display.index.name == _('Monthly'):
            df_display.index = df_display.index.strftime('%m-%Y')
        else:
            df_display.index = df_display.index.strftime('%Y')

        # round numeric variables
        numeric_variables = [_(variable) for variable in read_data.numeric_variables]
        df_display[numeric_variables] = df_display[numeric_variables].round(0)

        # add dimensions to the numeric columns names
        column_dimensions = {
            _('Contribution'): _('Contribution') + ', ' + _('kg'),
            _('Spend'): _('Spend') + ', ' + ' €',
            _('Revenue_Calculated'): _('Revenue_Calculated') + ', ' + '€',
            _('Marginal_Contribution'): _('Marginal_Contribution') + ', ' + _('kg'),
        }
        df_display = df_display.rename(columns=column_dimensions)

        # translate products if Product granularity level is chosen
        if _('Product') in df_display.columns:
            df_display[_('Product')] = df_display[_('Product')].map(lambda p: _(p))

        # display dataframe
        st.dataframe(df_display, height=600, use_container_width=True)

        # create button to export the table
        csv = convert_df(df_display)
        st.download_button(
            _('Export table'),
            csv,
            'df_display.csv',
            'text/csv',
            key='download-csv'
        )

    # Define the content of the second tab - Plot
    with tabs[1]:
        # Create a list of column names to plot
        columns_to_plot = st.multiselect(_('Select variables'),
                                         [_(variable) for variable in read_data.numeric_variables])
        granularity_to_plot = st.multiselect(_('Select granularity'), list(pd.unique(df_display.iloc[:, 0])))

        fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
        for column in columns_to_plot:
            for granularity in granularity_to_plot:
                if 'доход' in column.lower() or 'расход' in column.lower():
                    fig.add_trace(go.Scatter(x=df_display.index,
                                             y=df_display[df_display.iloc[:, 0] == granularity][column],
                                             name=column + ', ' + granularity,
                                             yaxis='y1'),
                                  secondary_y=False)
                elif 'вклад' in column.lower():
                    fig.add_trace(go.Scatter(x=df_display.index,
                                             y=df_display[df_display.iloc[:, 0] == granularity][column],
                                             name=column + ', ' + granularity,
                                             yaxis='y2'),
                                  secondary_y=True)

        # Set plot title, adjust size and axes labels
        fig.update_layout(title=f'{", ".join(columns_to_plot)}',
                          yaxis_title=_('Revenue') + '/' + _('Spend') + ', ' + _('€'),
                          yaxis2_title=_('Contribution') + ', ' + _('kg'))

        st.plotly_chart(fig, use_container_width=True)

    return spec_page
