import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from translations import _
import read_data
from functions import response_curves_data

number_of_steps = 85


def plan_rc_tab(dataframe):
    # create a list of column names to plot
    col_1, buff = st.columns(2)
    with col_1:
        # check if user has selected any granularity in sidebar
        # plot only if he has
        if any([st.session_state['tracking']['selection_dict'][_('Dealership')],
                st.session_state['tracking']['selection_dict'][_('Channel')],
                st.session_state['tracking']['selection_dict'][_('Format')],
                st.session_state['tracking']['selection_dict'][_('Product')]
                ]):
            granularity = list(pd.unique(dataframe.iloc[:, 0]))
        else:
            granularity = []
        granularity_to_plot = st.multiselect(_('Select variables'),
                                             options=granularity,
                                             default=granularity,
                                             key='granularity_to_rc_plot')
        # get the lowest granularity level from the selected
        granularity_level = [_(level) for level in read_data.granularity_levels if _(level) in dataframe.columns].pop()
        # upper limit is twice maximum spend
        max_spend = np.max(dataframe.groupby(granularity_level)[_('Spend')].sum()) * 2
        fig = go.Figure()
        for granularity in granularity_to_plot:
            # get curve data with current spend marker
            curve_data, marker_loc = response_curves_data(dataframe, granularity_level,
                                                          granularity, max_spend, number_of_steps)
            fig.add_trace(go.Scatter(x=curve_data['Spend'],
                                     y=curve_data['Revenue'],
                                     name=f'{granularity}',
                                     mode='lines'))
            current_spend = curve_data.iloc[marker_loc]['Spend']
            current_revenue = curve_data.iloc[marker_loc]['Revenue']
            fig.add_trace(go.Scatter(x=[current_spend],
                                     y=[current_revenue],
                                     name=f'{_("Factual Spend")} {_("on")} {granularity}',
                                     mode='markers',
                                     marker=dict(size=15,
                                                 opacity=0.5)))
            if 'simulated' in st.session_state['tracking'] and st.session_state['tracking']['simulated']:
                # data for simulated spend marker
                simulated_spend = dataframe[dataframe[granularity_level] == granularity][_('Simulated Spend')].sum()
                simulated_revenue = dataframe[dataframe[granularity_level] == granularity][
                    _('Simulated Revenue')].sum()
                if simulated_revenue >= current_revenue:
                    marker = 'triangle-right'
                else:
                    marker = 'triangle-left'
                fig.add_trace(go.Scatter(x=[simulated_spend],
                                         y=[simulated_revenue],
                                         name=f'{_("Simulated Spend")} {_("on")} {granularity}',
                                         mode='markers',
                                         marker=dict(size=15,
                                                     symbol=marker,
                                                     opacity=0.5)))
    fig.update_layout(
        height=600,
        title=f'{", ".join(granularity_to_plot)}',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")}'),
            side='left',
            tickprefix='€ ',
            tickformat=',.2f'
        ),
        hovermode='x unified'
    )

    fig.update_xaxes(
        title=f'{_("Spend")}',
        showgrid=True,
        tickprefix='€ ',
        tickformat=',.2f'
    )

    st.plotly_chart(fig, use_container_width=True)
