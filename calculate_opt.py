import streamlit as st
from translations import _, translate_table


def optimized_top_metrics(dataframe):
    """ Calculate optimized top metrics """
    optimized_total_spend = dataframe[_('Optimized Spend')].sum()
    optimized_total_contribution = dataframe[_('Optimized Contribution')].sum()
    optimized_total_revenue = dataframe[_('Optimized Revenue')].sum()
    optimized_total_mroi = optimized_total_revenue / optimized_total_spend

    # save top metrics for Planning calculations
    st.session_state['tracking'].update({
        'optimized_spend': optimized_total_spend,
        'optimized_contribution': optimized_total_contribution,
        'optimized_revenue': optimized_total_revenue,
        'optimized_mroi': optimized_total_mroi
    })


def calculate_opt(dataframe):
    """
    Adds Lower and Upper bounds into the dataframe
    returns dataframe with Lower and Upper boundaries for optimization
    """
    # clean table
    dataframe = dataframe.fillna(0)
    dataframe = dataframe[dataframe[_('Simulated Spend')] > 0]

    # calculate initial constraints
    # if sliders were changed on Optimization page
    if ('lower_bound_track' in st.session_state['tracking']) | ('upper_bound_track' in st.session_state['tracking']):
        # sliders are in percents and are initialized in the Optimization page
        lower_bound, upper_bound = (100 + st.session_state['lower_bound_slider']) / 100, \
            (100 + st.session_state['upper_bound_slider']) / 100
    # if sliders haven't been changed yet in the Optimization set
    else:
        lower_bound, upper_bound = 0.8, 1.2

    dataframe[_('Lower Spend Bound')] = lower_bound * dataframe[_('Simulated Spend')]
    dataframe[_('Upper Spend Bound')] = upper_bound * dataframe[_('Simulated Spend')]

    # after optimization
    if 'df_optimized' in st.session_state['tracking']:
        # translate because it is cached
        dataframe = translate_table(st.session_state['tracking']['df_optimized'],
                                    get_original=st.session_state['tracking']['language_switch'])
        optimized_top_metrics(dataframe)

    return dataframe
