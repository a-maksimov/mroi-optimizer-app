import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from translations import _
import read_data


def spec_plotting_tab(dataframe):
    # create a list of column names to plot
    col_1, col_2 = st.columns(2)
    with col_1:
        numeric_variables = [_(variable) for variable in read_data.numeric_variables if _(variable) in dataframe.columns]
        columns_to_plot = st.multiselect(_('Select indicators'), numeric_variables)
    with col_2:
        granularity_to_plot = st.multiselect(_('Select granularity'), list(pd.unique(dataframe.iloc[:, 0])))

    fig = sp.make_subplots(specs=[[{'secondary_y': True}]])
    for column in columns_to_plot:
        for granularity in granularity_to_plot:
            if _('Revenue').lower() in column.lower() or _('Spend').lower() in column.lower():
                fig.add_trace(go.Scatter(x=dataframe.index,
                                         y=dataframe[dataframe.iloc[:, 0] == granularity][column],
                                         name=column + ', ' + granularity,
                                         yaxis='y1'),
                              secondary_y=False)
            elif _('Contribution').lower() in column.lower():
                fig.add_trace(go.Scatter(x=dataframe.index,
                                         y=dataframe[dataframe.iloc[:, 0] == granularity][column],
                                         name=column + ', ' + granularity,
                                         yaxis='y2'),
                              secondary_y=True)
    # rotate x ticks
    fig.update_xaxes(tickangle=45)

    # set plot title, adjust size and axes labels
    fig.update_layout(title=f'{", ".join(columns_to_plot)}',
                      yaxis_title=_('Revenue') + '/' + _('Spend') + ', ' + _('€'),
                      yaxis2_title=_('Contribution') + ', ' + _('kg'))

    st.plotly_chart(fig, use_container_width=True)
