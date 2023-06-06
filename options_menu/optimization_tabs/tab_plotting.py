import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from translations import _
from utils import create_checkbox
import read_data
from functions import timeseries_data, bar_data, stacked_bar_data, mroi_plot


def opt_plotting_tab(dataframe):
    # drop unnecessary columns
    dataframe = dataframe.drop([_('Marginal Contribution')], axis='columns')
    # get granularity levels
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    # get numeric variables
    simulated_numeric_variables = [_('Simulated Spend'), _('Simulated Contribution'), _('Simulated Revenue')]
    simulated_numeric_variables = [variable for variable in simulated_numeric_variables
                                   if variable in dataframe.columns]
    optimized_numeric_variables = [_('Optimized Spend'), _('Optimized Contribution'), _('Optimized Revenue')]
    optimized_numeric_variables = [variable for variable in optimized_numeric_variables
                                   if variable in dataframe.columns]
    
    #color's sequence: orange, yellow, red, blue, green, violet, pink
    base_colors_timeseries=['#eb6e21','#f7db05','#d62b2b','#1e3ac7','#13bd21','#7308c4','#d936c6']

    colors_contribution=['#F7A15B','#FFEC5E','#F76F6F','#8554F7','#4AF77B', '#C64AF7', '#F763F7']
    colors_spend=['#C25F0E', '#EBD110', '#C21D1D', '#4008C2', '#00C237', '#8B00C2', '#C213C2']
    colors_revenue=['#F57811','#F5F231','#F52525','#5109F4','#00F545', '#B000F5', '#F518F5']

    colors_optimization=['#ff8317', '#fcf40d', '#fc1e2d', '#1938fc', '#19fa19', '#7611f2', '#fc17e5']

    colors_revenue_optimization=['#DB6B0F', '#FFE312', '#DB2121', '#760CF5', '#00DB3E', '#9D00DB', '#DB16DB']
    colors_spend_optimization=['#B5580D', '#CCB60E', '#B51B1B', '#260575', '#00B533', '#540075', '#750C75']
    colors_contribution_optimization=['#FA825D', '#FFDA65', '#F76266', '#BA9FF9', '#95F9B1', '#DC95F9', '#F9AEF9']


    spend_colors_mroi_list=[]
    revenue_colors_mroi_list=[] 
    contribution_colors_mroi_list=[]
    optimization_contribution_colors_mroi_list=[]
    optimization_revenue_colors_mroi_list=[]
    optimization_spend_colors_mroi_list=[]
    mroi_color_list=[]
    optimization_mroi_color_list=[]

    granularity_colors ={}
    contribution_colors ={}
    spend_colors ={}
    revenue_colors ={}
    optimization_colors={}
    contribution_optimization_colors={}
    spend_optimization_colors={}
    revenue_optimization_colors={}
    mroi_colors={}

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
                                                   options=simulated_numeric_variables + optimized_numeric_variables,
                                                   default=[variable for variable
                                                            in simulated_numeric_variables + optimized_numeric_variables
                                                            if _('Contribution').lower() not in variable.lower()])
    with col_2:
        granularity_to_plot = st.multiselect(_('Select variables'),
                                             options=granularity_options,
                                             default=granularity_options)

    # create percents switch
    create_checkbox('opt_percents_checkbox')
    percents = st.session_state['tracking']['opt_percents_checkbox_track']
    # bar plots ticks dimensions
    prefix, suffix = '€ ', ''
    contribution_dim = _('kg')
    pct = ''
    if percents:
        prefix, suffix = '', '%'
        contribution_dim = '%'
        pct = '_pct'
    
    for i in range(len(granularity_to_plot)):
        granularity_colors[granularity_to_plot[i]] = base_colors_timeseries[i]
        contribution_colors[granularity_to_plot[i]] = colors_contribution[i]
        spend_colors[granularity_to_plot[i]] = colors_spend[i]
        revenue_colors[granularity_to_plot[i]] = colors_revenue[i]
        revenue_optimization_colors[granularity_to_plot[i]]=colors_revenue_optimization[i]
        spend_optimization_colors[granularity_to_plot[i]]=colors_spend_optimization[i]
        contribution_optimization_colors[granularity_to_plot[i]]=colors_contribution_optimization[i]


    # Time series plot
    fig = go.Figure()
    for numeric_variable in [variable for variable in numeric_variables_to_plot
                             if _('Simulated').lower() in variable.lower()]:
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
                                         offsetgroup=0,
                                         marker_color=spend_colors[granularity],
                                         base=base
                                         )
                                  )
                    base += ts[numeric_variable]
                elif _('Revenue').lower() in numeric_variable.lower():
                    fig.add_trace(go.Scatter(x=ts.index,
                                             y=ts[numeric_variable],
                                             name=f'{numeric_variable}, {granularity}',
                                             mode='markers+lines',
                                             marker_color=revenue_colors[granularity]
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
    # after optimization
    if 'df_optimized' in st.session_state['tracking']:
        for numeric_variable in [variable for variable in numeric_variables_to_plot
                                 if _('Optimized').lower() in variable.lower()]:
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
            dict(dtickrange=[604800000, 'M1'], value='%d-%m-%Y'),
            dict(dtickrange=['M1', 'M12'], value='%m-%Y'),
            dict(dtickrange=['M12', None], value='%Y')
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
            tickformat=',.0f'
        ),
        yaxis2=dict(
            title=dict(text=f'{_("Contribution")}, {contribution_dim}'),
            side='right',
            overlaying='y',
            tickmode='sync',
            tickprefix='',
            tickformat=',.0f'
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    # MROI plot
    fig = go.Figure()
    # calculate mroi data
    labels_for_colors=[]
    data = mroi_plot(dataframe, level, simulated_numeric_variables, percents=percents)
    if data is not None:
        for i in range(len(data.index)):
            labels_for_colors.append(data.index[i])

        for label in labels_for_colors:
            contribution_colors_mroi_list.append(contribution_colors[label])
            spend_colors_mroi_list.append(spend_colors[label])
            revenue_colors_mroi_list.append(revenue_colors[label])
        mroi_color_list.append(spend_colors_mroi_list)
        mroi_color_list.append(revenue_colors_mroi_list)
        mroi_color_list.append(contribution_colors_mroi_list)
            
        k=0
        for variable in sorted(set(numeric_variables_to_plot).intersection(simulated_numeric_variables)):
            mroi_colors[variable] = mroi_color_list[k]
            k=k+1

        for variable in sorted(set(numeric_variables_to_plot).intersection(simulated_numeric_variables)):
            fig.add_trace(go.Bar(x=data.index,
                                 y=data[variable + pct],
                                 name=f'{data[variable].name}',
                                 opacity=0.6,
                                 marker_color=mroi_colors[variable],
                                 xperiodalignment='middle'
                                 )
                          )
        mroi_data = data[_('Simulated Revenue')] / data[_('Simulated Spend')]
        fig.add_trace(go.Scatter(x=data.index,
                                 y=mroi_data,
                                 name=_('Simulated') + ' MROI',
                                 xperiodalignment='middle',
                                 mode='markers',
                                 marker=dict(
                                     size=10,
                                     color=mroi_colors[variable]
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
        # after optimization
        if 'df_optimized' in st.session_state['tracking']:
            data = mroi_plot(dataframe, level, optimized_numeric_variables, percents=percents)
            if data is not None:
                for i in range(len(data.index)):
                    labels_for_colors.append(data.index[i])

                for label in labels_for_colors:
                    optimization_spend_colors_mroi_list.append(spend_optimization_colors[label])
                    optimization_revenue_colors_mroi_list.append(revenue_optimization_colors[label])
                    optimization_contribution_colors_mroi_list.append(contribution_optimization_colors[label])
                optimization_mroi_color_list.append(optimization_spend_colors_mroi_list)
                optimization_mroi_color_list.append(optimization_revenue_colors_mroi_list)
                optimization_mroi_color_list.append(optimization_contribution_colors_mroi_list)
            
                k=0
                for variable in sorted(set(numeric_variables_to_plot).intersection(optimized_numeric_variables)):
                    optimization_colors[variable] = optimization_mroi_color_list[k]
                    k=k+1

                for variable in sorted(set(numeric_variables_to_plot).intersection(optimized_numeric_variables)):
                    fig.add_trace(go.Bar(x=data.index,
                                         y=data[variable + pct],
                                         name=f'{data[variable].name}',
                                         opacity=0.6,
                                         marker_color=optimization_colors[variable],
                                         xperiodalignment='middle'
                                         )
                                  )
                mroi_data = data[_('Optimized Revenue')] / data[_('Optimized Spend')]
                fig.add_trace(go.Scatter(x=data.index,
                                         y=mroi_data,
                                         name=_('Optimized') + ' MROI',
                                         xperiodalignment='middle',
                                         mode='markers',
                                         marker=dict(
                                             size=10,
                                             color=optimization_colors[variable]
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

        title = f'{", ".join([variable for variable in simulated_numeric_variables + optimized_numeric_variables if not _("Contribution").lower() in variable.lower()] + ["MROI"])}'
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

    # Bar charts
    # calculate data for bar plot
    data = bar_data(dataframe, level, granularity_to_plot, numeric_variables_to_plot, percents=percents)
    if data is not None:
        color_bar={}
        color_bar.update(optimization_colors)
        color_bar.update(mroi_colors)
        col_1, col_2 = st.columns(2)
        # plot spends
        spends_to_plot = [numeric_variable for numeric_variable in numeric_variables_to_plot
                          if _('Spend').lower() in numeric_variable.lower()]
        revenues_to_plot = [numeric_variable for numeric_variable in numeric_variables_to_plot
                            if _('Revenue').lower() in numeric_variable.lower()]

        with col_1:
            fig = go.Figure()
            for spend in spends_to_plot:
                fig.add_trace(go.Bar(
                    y=data.index,
                    x=data[spend],
                    name=data[spend].name,
                    orientation='h',
                    marker_color=color_bar[spend],
                    opacity=0.6))
            fig.update_layout(
                title=_('Spends before and after optimization'),
                xaxis_title=_('Spend'),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    tickprefix=prefix,
                    ticksuffix=suffix),
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.5,
                    xanchor='right',
                    x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

            # plot revenues
            with col_2:
                fig = go.Figure()
                for revenue in revenues_to_plot:
                    fig.add_trace(go.Bar(
                        y=data.index,
                        x=data[revenue],
                        name=data[revenue].name,
                        orientation='h',
                        marker_color=color_bar[revenue],
                        opacity=0.6))
                fig.update_layout(
                    title=_('Revenues before and after optimization'),
                    xaxis_title=_('Revenue'),
                    xaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        tickprefix=prefix,
                        ticksuffix=suffix),
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=-0.5,
                        xanchor='right',
                        x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

        # Stacked charts
        # calculate stacked bar data
        data = stacked_bar_data(dataframe, level, granularity_to_plot, spends_to_plot, percents=percents)
        fig = px.bar(data,
                     x=_('Spend'),
                     y='value',
                     color=level,
                     title=_('Budget Allocation'),
                     text=data['value'].apply(lambda n: f'{prefix} {n:.0f}{suffix}'),
                     color_discrete_map=spend_colors,
                     opacity=0.5)
        fig.update_traces(hovertemplate='Value: %{text}<extra></extra>')
        fig.update_yaxes(visible=False)
        st.plotly_chart(fig, use_container_width=True)
