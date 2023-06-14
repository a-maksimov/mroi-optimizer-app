import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from translations import _
from utils import create_checkbox
import read_data
from functions import timeseries_data, mroi_plot


def plan_plotting_tab(dataframe):
    # drop unnecessary columns
    dataframe = dataframe.drop([_('Marginal Contribution')], axis='columns')
    # get granularity levels
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    # get numeric variables
    numeric_variables = [_(variable) for variable in read_data.numeric_variables if _(variable) in dataframe.columns]
    simulated_numeric_variables = [_('Simulated Spend'), _('Simulated Contribution'), _('Simulated Revenue')]
    simulated_numeric_variables = [variable for variable in simulated_numeric_variables
                                   if variable in dataframe.columns]

    #color's sequence: peach, teal, red, ice, tealgrn, violet, pink
    colors_contribution=['#F8BF97','#9DD4D4','#EC939D','#63A9C7','#85E6AB', '#E0C2F0', '#ECAABF']
    colors_spend=['#F6A479', '#78B9C1', '#D87187', '#4175B5', '#61D7A5', '#C7A5E3', '#D682B5']
    colors_revenue=['#F28A61','#5799AC','#B74F72','#3C488F','#42BDA3', '#AC8DD5', '#B263AE']

    colors_revenue_optimization=['#EB4C41', '#2B5876', '#6E2348', '#191934', '#268199', '#675BA3', '#623F8E']
    colors_spend_optimization=['#EF6F4F', '#3B7490', '#96375E', '#2E2C5B', '#32A5A1', '#8D75C2', '#8E50A4']
    colors_contribution_optimization=['#FCDCBF', '#C9EAE7', '#FBBBBB', '#C2E6E9', '#A9F0B9', '#F1DDF7', '#F8D9D8']

    contribution_colors ={}
    spend_colors ={}
    revenue_colors ={}
 
    contribution_optimization_colors={}
    spend_optimization_colors={}
    revenue_optimization_colors={}

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
                                                   options=numeric_variables + simulated_numeric_variables,
                                                   default=[variable for variable
                                                            in simulated_numeric_variables
                                                            if _('Contribution').lower() not in variable.lower()])
    with col_2:
        granularity_to_plot = st.multiselect(_('Select variables'),
                                             options=granularity_options,
                                             default=granularity_options)

    # create percents switch
    create_checkbox('plan_percents_checkbox')
    percents = st.session_state['tracking']['plan_percents_checkbox_track']
    # bar plots ticks dimensions
    prefix, suffix = '€ ', ''
    contribution_dim = _('kg')
    pct = ''
    if percents:
        prefix, suffix = '', '%'
        contribution_dim = '%'
        pct = '_pct'

    for i in range(len(granularity_to_plot)):
        contribution_colors[granularity_to_plot[i]] = colors_contribution[i]
        spend_colors[granularity_to_plot[i]] = colors_spend[i]
        revenue_colors[granularity_to_plot[i]] = colors_revenue[i]
        revenue_optimization_colors[granularity_to_plot[i]]=colors_revenue_optimization[i]
        spend_optimization_colors[granularity_to_plot[i]]=colors_spend_optimization[i]
        contribution_optimization_colors[granularity_to_plot[i]]=colors_contribution_optimization[i]

    # MROI plot
    fig = go.Figure()
    # calculate mroi data
    labels_for_colors=['#0068C9','lightskyblue','deepskyblue']
    labels_for_opt_colors=['darkcyan','darkturquoise','cyan']
    dict_for_colors={}
    dict_for_opt_colors={}
    data = mroi_plot(dataframe, level, numeric_variables, percents=percents)
    if data is not None:
        k=0
        for variable in sorted(set(numeric_variables_to_plot).intersection(numeric_variables)):
            dict_for_colors[variable] = labels_for_colors[k]
            k=k+1

        for variable in sorted(set(numeric_variables_to_plot).intersection(numeric_variables)):
            fig.add_trace(go.Bar(x=data.index,
                                 y=data[variable + pct],
                                 name=data[variable].name,
                                 opacity=0.6,
                                 xperiodalignment='middle',
                                 marker_color=dict_for_colors[variable]
                                 )
                          )
        mroi_data = data[_('Revenue Calculated')] / data[_('Spend')]
        # for variable in sorted(set(numeric_variables_to_plot).intersection(numeric_variables)):
        fig.add_trace(go.Scatter(x=data.index,
                                    y=mroi_data,
                                    name='MROI',
                                    xperiodalignment='middle',
                                    mode='markers',
                                    marker=dict(
                                        size=10,
                                        color='red'
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
                yshift=10,
                xshift=-20,
                yref='y2',
                opacity=0.6

            )
        if 'simulated' in st.session_state['tracking'] and st.session_state['tracking']['simulated']:
            data = mroi_plot(dataframe, level, simulated_numeric_variables, percents=percents)
            if data is not None:
                k=0
                for variable in sorted(set(numeric_variables_to_plot).intersection(simulated_numeric_variables)):
                    dict_for_opt_colors[variable] = labels_for_opt_colors[k]
                    k=k+1

                for variable in sorted(set(numeric_variables_to_plot).intersection(simulated_numeric_variables)):
                    fig.add_trace(go.Bar(x=data.index,
                                         y=data[variable + pct],
                                         name=data[variable].name,
                                         opacity=0.6,
                                         xperiodalignment='middle',
                                        marker_color=dict_for_opt_colors[variable]
                                         )
                                  )
                mroi_data = data[_('Simulated Revenue')] / data[_('Simulated Spend')]
                fig.add_trace(go.Scatter(x=data.index,
                                         y=mroi_data,
                                         name=_('Simulated') + ' MROI',
                                         xperiodalignment='middle',
                                         mode='markers',
                                         opacity=0.6,
                                         marker=dict(
                                             size=13,
                                             color='darkslategray'
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
                        yshift=10,
                        xshift=20,
                        yref='y2',
                        opacity=0.6
                    )

        title = f'{", ".join([variable for variable in numeric_variables + simulated_numeric_variables if not _("Contribution").lower() in variable.lower()] + ["MROI"])}'
        fig.update_layout(
            height=600,
            title=title,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.5,
                xanchor='right',
                x=1
            ),
            yaxis=dict(
                title=dict(text=f'{_("Spend")}, {_("Revenue")}'),
                side='left',
                tickprefix=prefix,
                ticksuffix=suffix,
                # tickformat=',.0f',
            ),
            yaxis2=dict(
                title=dict(text='MROI'),
                side='right',
                overlaying='y',
                tickmode='sync',
                # tickformat=',.2f'
            )
        )
        fig.update_xaxes(showgrid=True)
        st.plotly_chart(fig, use_container_width=True)

    # Time series plot
    fig = go.Figure()
    for numeric_variable in [variable for variable in numeric_variables_to_plot
                             if not _('Simulated').lower() in variable.lower()]:
        granularity_to_plot = sorted(granularity_to_plot,
                                     key=lambda g: dataframe[dataframe[level] == g][numeric_variable].sum(),
                                     reverse=True)
        # https://dev.to/fronkan/stacked-and-grouped-bar-charts-using-plotly-python-a4p
        timeseries = timeseries_data(dataframe, level, numeric_variable, percents=percents)
        if timeseries is not None:
            base = 0
            for granularity in granularity_to_plot:
                # create a new DataFrame called ts and initialize it with zeros
                # using the same index as the timeseries DataFrame.
                ts = pd.DataFrame(0, index=timeseries.index.unique(), columns=[numeric_variable])
                # filter the timeseries DataFrame based on the condition `timeseries[level] == granularity`
                # and assign the filtered values to ts.
                ts.loc[timeseries.index[timeseries[level] == granularity], [numeric_variable]] = \
                    timeseries.loc[timeseries[level] == granularity, [numeric_variable]]
                if _('Spend').lower() in numeric_variable.lower():
                    fig.add_trace(go.Bar(x=ts.index,
                                         y=ts[numeric_variable],
                                         name=f'{numeric_variable}, {granularity}',
                                         opacity=0.6,
                                         marker_color=spend_colors[granularity],
                                         offsetgroup=0,
                                         base=base
                                         )
                                  )
                    base += ts[numeric_variable]
                elif _('Revenue').lower() in numeric_variable.lower():
                    fig.add_trace(go.Scatter(x=ts.index,
                                             y=ts[numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             marker_color=revenue_colors[granularity],
                                             mode='markers+lines'
                                             )
                                  )
                else:  # Contribution
                    fig.add_trace(go.Scatter(x=ts.index,
                                             y=ts[numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             mode='markers+lines',
                                             marker_color=contribution_colors[granularity],
                                             yaxis='y2'
                                             )
                                  )
    # after simulation
    if 'simulated' in st.session_state['tracking'] and st.session_state['tracking']['simulated']:
        for numeric_variable in [variable for variable in numeric_variables_to_plot
                                 if _('Simulated').lower() in variable.lower()]:
            granularity_to_plot = sorted(granularity_to_plot,
                                         key=lambda g: dataframe[dataframe[level] == g][numeric_variable].sum(),
                                         reverse=True)
            timeseries = timeseries_data(dataframe, level, numeric_variable, percents=percents)
            if timeseries is not None:
                base = 0
                for granularity in granularity_to_plot:
                    # create a new DataFrame called ts and initialize it with zeros
                    # using the same index as the timeseries DataFrame.
                    ts = pd.DataFrame(0, index=timeseries.index.unique(), columns=[numeric_variable])
                    # filter the timeseries DataFrame based on the condition `timeseries[level] == granularity`
                    # and assign the filtered values to ts.
                    ts.loc[timeseries.index[timeseries[level] == granularity], [numeric_variable]] = \
                        timeseries.loc[timeseries[level] == granularity, [numeric_variable]]
                    if _('Spend').lower() in numeric_variable.lower():
                        fig.add_trace(go.Bar(x=ts.index,
                                             y=ts[numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             opacity=0.6,
                                             offsetgroup=1,
                                             marker_color=spend_optimization_colors[granularity],
                                             base=base
                                             )
                                      )
                        base += ts[numeric_variable]
                    elif _('Revenue').lower() in numeric_variable.lower():
                        fig.add_trace(go.Scatter(x=ts.index,
                                                 y=ts[numeric_variable],
                                                 name=f'{numeric_variable}, {granularity}',
                                                 marker_color=revenue_optimization_colors[granularity],
                                                 mode='markers+lines'
                                                 )
                                      )
                    else:  # Contribution
                        fig.add_trace(go.Scatter(x=ts.index,
                                                 y=ts[numeric_variable],
                                                 name=f'{numeric_variable}, {granularity}',
                                                 marker_color=contribution_optimization_colors[granularity],
                                                 mode='markers+lines',
                                                 yaxis='y2',
                                                 )
                                      )
    fig.update_layout(
        height=600,
        title=f'{", ".join(numeric_variables_to_plot)}',
        xaxis=dict(
            type='date',
            ticklabelmode='period',
            showgrid=True
        ),
        xaxis_tickformatstops=[
            dict(dtickrange=[604800000, 'M1'], value='Месяц %m'),
            dict(dtickrange=['M1', 'M12'], value='Месяц %m'),
            dict(dtickrange=['M12', None], value='Год %Y')
        ],
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-1,
            xanchor='right',
            x=1
        ),
        yaxis=dict(
            title=dict(text=f'{_("Revenue")}, {_("Spend")}'),
            side='left',
            tickprefix=prefix,
            ticksuffix=suffix,
            # tickformat=',.0f'
        ),
        yaxis2=dict(
            title=dict(text=f'{_("Contribution")}, {contribution_dim}'),
            side='right',
            overlaying='y',
            tickmode='sync',
            tickprefix='',
            # tickformat=',.0f'
        )
    )
    st.plotly_chart(fig, use_container_width=True)
