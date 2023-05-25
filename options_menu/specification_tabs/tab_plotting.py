import streamlit as st
import plotly.graph_objects as go
from translations import _
from utils import create_checkbox
import read_data
from functions import timeseries_data_stacked, mroi_plot


def spec_plotting_tab(dataframe):
    # drop unnecessary columns
    dataframe = dataframe.drop([_('Marginal Contribution')], axis='columns')
    # get granularity levels
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    numeric_variables = [_(variable) for variable in read_data.numeric_variables if
                         _(variable) in dataframe.columns]

    # check if user has selected any granularity in sidebar
    # iterate backwards through the granularity levels and use the first one that is not empty
    for level in reversed(granularity_levels):
        if st.session_state['tracking']['selection_dict'][level]:
            granularity_options = st.session_state['tracking']['selection_dict'][level]
            break
    # the else block will NOT be executed if the loop is stopped by a break statement
    else:
        granularity_options = []
        level = None

    # create a list of column names to plot
    col_1, col_2 = st.columns(2)
    with col_1:
        numeric_variables_to_plot = st.multiselect(_('Select indicators'),
                                                   options=numeric_variables,
                                                   default=[variable for variable in numeric_variables
                                                            if not variable == _('Contribution')])
    with col_2:
        granularity_to_plot = st.multiselect(_('Select variables'),
                                             options=granularity_options,
                                             default=granularity_options)

    # create percents switch
    create_checkbox('spec_percents_checkbox')
    percents = st.session_state['tracking']['spec_percents_checkbox_track']
    # bar plots ticks dimensions
    prefix, suffix = '€ ', ''
    contribution_dim = _('kg')
    pct = ''
    if percents:
        prefix, suffix = '', '%'
        contribution_dim = '%'
        pct = '_pct'

    # Timeseries plot
    fig = go.Figure()
    for numeric_variable in numeric_variables_to_plot:
        granularity_to_plot = sorted(granularity_to_plot,
                                     key=lambda g: dataframe[dataframe[level] == g][numeric_variable].sum(),
                                     reverse=True)
        for granularity in granularity_to_plot:
            timeseries = timeseries_data_stacked(dataframe, level, granularity, numeric_variable, percents=percents)
            if timeseries is not None:
                if _('Spend').lower() in numeric_variable.lower():
                    fig.add_trace(go.Bar(x=timeseries.index,
                                         y=timeseries[timeseries[level] == granularity][numeric_variable],
                                         name=f'{numeric_variable}, {granularity}',
                                         opacity=0.6,
                                         )
                                  )
                elif _('Revenue').lower() in numeric_variable.lower():
                    fig.add_trace(go.Scatter(x=timeseries.index,
                                             y=timeseries[timeseries[level] == granularity][numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             mode='markers+lines'
                                             )
                                  )
                else:  # Contribution
                    fig.add_trace(go.Scatter(x=timeseries.index,
                                             y=timeseries[timeseries[level] == granularity][numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             mode='markers+lines',
                                             yaxis='y2'
                                             )
                                  )
    fig.update_layout(
        barmode='stack',
        height=600,
        title=f'{", ".join(numeric_variables_to_plot)}',
        xaxis_tickformatstops=[
            dict(dtickrange=[604800000, 'M1'], value='%d-%m-%Y'),
            dict(dtickrange=['M1', 'M12'], value='%m-%Y'),
            dict(dtickrange=['M12', None], value='%Y')
        ],
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")}, {_("Spend")}'),
            side='left',
            tickprefix=prefix,
            ticksuffix=suffix,
            tickformat=',.0f',
        ),
        yaxis2=dict(
            title=dict(text=f'{_("Contribution")}, {contribution_dim}'),
            side='right',
            overlaying='y',
            tickmode='sync',
            ticksuffix=suffix,
            tickformat=',.0f'
        )
    )
    fig.update_xaxes(showgrid=True)
    st.plotly_chart(fig, use_container_width=True)

    # MROI plot
    fig = go.Figure()
    # calculate mroi data
    data = mroi_plot(dataframe, level, numeric_variables, percents=percents)
    if data is not None:
        for variable in sorted(set(numeric_variables_to_plot).intersection(numeric_variables)):
            fig.add_trace(go.Bar(x=data.index,
                                 y=data[variable + pct],
                                 name=data[variable].name,
                                 opacity=0.6,
                                 xperiodalignment='middle',
                                 )
                          )
        mroi_data = data[_('Revenue Calculated')] / data[_('Spend')]
        fig.add_trace(go.Scatter(x=data.index,
                                 y=mroi_data,
                                 name='MROI',
                                 xperiodalignment='middle',
                                 mode='markers',
                                 marker=dict(
                                     size=10,
                                 ),
                                 yaxis='y2',
                                 text=mroi_data,  # Include Y values in marker text
                                 textposition='bottom center'
                                 )
                      )
        # add annotations for each mroi marker
        for x, y, text in zip(data.index, mroi_data, mroi_data):
            fig.add_annotation(
                x=x,
                y=y,
                text=round(text, 2),
                showarrow=False,
                font=dict(color='black'),
                yshift=20,
                yref='y2'
            )
        fig.update_layout(
            height=600,
            title=f'{", ".join([variable for variable in numeric_variables if not variable == _("Contribution")] + ["MROI"])}',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.5,
                xanchor='right',
                x=1
            ),
            yaxis=dict(
                title=dict(text=f'{_("Spend")}, {_("Revenue Calculated")}'),
                side='left',
                tickprefix=prefix,
                ticksuffix=suffix,
                tickformat=',.0f',
            ),
            yaxis2=dict(
                title=dict(text='MROI'),
                side='right',
                overlaying='y',
                tickmode='sync',
                tickformat=',.2f'
            )
        )
        fig.update_xaxes(showgrid=True)
        st.plotly_chart(fig, use_container_width=True)
