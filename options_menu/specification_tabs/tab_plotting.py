import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from translations import _
import read_data


def spec_plotting_tab(dataframe):
    # drop unnecessary columns
    dataframe = dataframe.drop([_('Marginal Contribution')], axis='columns')

    # create a list of column names to plot
    col_1, col_2 = st.columns(2)
    with col_1:
        numeric_variables = [_(variable) for variable in read_data.numeric_variables if
                             _(variable) in dataframe.columns]
        columns_to_plot = st.multiselect(_('Select indicators'), options=numeric_variables, default=numeric_variables)
    with col_2:
        # check if user has selected any granularity in sidebar
        # plot only if he has
        if any([st.session_state['selection_dict'][_('Dealership')],
                st.session_state['selection_dict'][_('Channel')],
                st.session_state['selection_dict'][_('Format')],
                st.session_state['selection_dict'][_('Product')]
                ]):
            granularity = list(pd.unique(dataframe.iloc[:, 0]))
        else:
            granularity = []
        granularity_to_plot = st.multiselect(_('Select granularity'), options=granularity, default=granularity)

    fig = go.Figure()
    for column in columns_to_plot:
        for granularity in granularity_to_plot:
            if _('Spend').lower() in column.lower():
                fig.add_trace(go.Bar(x=dataframe.index,
                                     y=dataframe[dataframe.iloc[:, 0] == granularity][column],
                                     name=f'{column}, {granularity}'
                                     )
                              )
            elif _('Revenue').lower() in column.lower():
                fig.add_trace(go.Scatter(x=dataframe.index,
                                         y=dataframe[dataframe.iloc[:, 0] == granularity][column],
                                         name=f'{column}, {granularity}'
                                         )
                              )
            else:
                fig.add_trace(go.Scatter(x=dataframe.index,
                                         y=dataframe[dataframe.iloc[:, 0] == granularity][column],
                                         name=f'{column}, {granularity}',
                                         yaxis='y2'
                                         )
                              )

    fig.update_layout(
        title=f'{", ".join(columns_to_plot)}',
        xaxis_tickformatstops=[
            dict(dtickrange=[604800000, 'M1'], value='%d-%m-%Y'),
            dict(dtickrange=['M1', 'M12'], value='%m-%Y'),
            dict(dtickrange=['M12', None], value='%Y')
        ],
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")} / {_("Spend")}, {_("€")}'),
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
