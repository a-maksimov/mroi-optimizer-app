import streamlit as st
import plotly.graph_objects as go
from translations import _
import read_data
from functions import timeseries_data


def opt_plotting_tab(dataframe):
    # get granularity levels
    granularity_levels = [_(level) for level in read_data.granularity_levels]

    # create a list of column names to plot
    col_1, col_2 = st.columns(2)
    with col_1:
        numeric_variables = [_('Simulated Spend'),
                             _('Optimized Spend')]
        numeric_variables = [numeric_variable for numeric_variable in numeric_variables
                             if numeric_variable in dataframe.columns]
        numeric_variables_to_plot = st.multiselect(_('Select indicators'), numeric_variables, numeric_variables)
    with col_2:
        # check if user has selected any granularity in sidebar
        # plot only if he has
        if any([st.session_state['selection_dict'][level] for level in granularity_levels]):
            # iterate backwards through the granularity levels and use the first one that is not empty
            for level in reversed(granularity_levels):
                if st.session_state['selection_dict'][level]:
                    granularity_options = st.session_state['selection_dict'][level]
                    break
        else:
            granularity_options = []
        granularity_to_plot = st.multiselect(_('Select variables'),
                                             options=granularity_options,
                                             default=granularity_options)

    fig = go.Figure()
    for numeric_variable in numeric_variables_to_plot:
        for granularity in granularity_to_plot:
            timeseries = timeseries_data(dataframe, level, granularity, numeric_variable)
            if _('Spend').lower() in numeric_variable.lower():
                fig.add_trace(go.Bar(x=timeseries.index,
                                     y=timeseries[numeric_variable],
                                     name=f'{numeric_variable}, {granularity}',
                                     opacity=0.6,
                                     xperiodalignment='middle'
                                     )
                              )
            elif _('Revenue').lower() in numeric_variable.lower():
                fig.add_trace(go.Scatter(x=timeseries.index,
                                         y=timeseries[numeric_variable],
                                         name=f'{numeric_variable}, {granularity}',
                                         xperiodalignment='middle',
                                         mode='markers+lines'
                                         )
                              )
            else:
                fig.add_trace(go.Scatter(x=timeseries.index,
                                         y=timeseries[numeric_variable],
                                         name=f'{numeric_variable}, {granularity}',
                                         xperiodalignment='middle',
                                         mode='markers+lines',
                                         yaxis='y2'
                                         )
                              )

    fig.update_layout(
        title=f'{", ".join(numeric_variables_to_plot)}',
        xaxis_tickformatstops=[
            dict(dtickrange=[604800000, 'M1'], value='%d-%m-%Y'),
            dict(dtickrange=['M1', 'M12'], value='%m-%Y'),
            dict(dtickrange=['M12', None], value='%Y')
        ],
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-1.02,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")} / {_("Spend")}'),
            side='left',
            tickprefix='€ ',
            tickformat=',.2f'

        ),
        yaxis2=dict(
            title=dict(text=f'{_("Contribution")}, {_("kg")}'),
            side='right',
            overlaying='y',
            tickmode='sync',
            tickprefix='',
            tickformat=',.2f'
        )
    )

    fig.update_xaxes(showgrid=True)

    st.plotly_chart(fig, use_container_width=True)
