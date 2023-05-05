import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from translations import _
import read_data
from functions import response_curves_data


def plan_rc_tab(dataframe):
    # create a list of column names to plot
    col_1, buff = st.columns(2)
    with col_1:
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
        granularity_to_plot = st.multiselect(_('Select variable'),
                                             options=granularity,
                                             default=granularity,
                                             key='granularity_to_rc_plot')
        granularity_level = [_(level) for level in read_data.granularity_levels if _(level) in dataframe.columns]
        fig = go.Figure()
        for granularity in granularity_to_plot:
            df = response_curves_data(dataframe, *granularity_level, granularity)
            fig.add_trace(go.Scatter(x=df['Spend'], y=df['Revenue'], name=f'{granularity}'))

    fig.update_layout(
        title=f'{", ".join(granularity_to_plot)}',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")}'),
            side='left',
            tickprefix='€ ',
            tickformat=',.2f'
        ),
    )

    fig.update_xaxes(
        title=f'{_("Spend")}',
        showgrid=True,
        tickprefix='€ ',
        tickformat=',.2f'
    )

    st.plotly_chart(fig, use_container_width=True)
