import streamlit as st
from translations import _


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

    # after optimization
    if 'df_optimized' in st.session_state['tracking']:
        dataframe = st.session_state['tracking']['df_optimized']
        optimized_top_metrics(dataframe)

    # calculate initial boundaries
    if not (('lower_bound_track' in st.session_state['tracking']) | (
            'upper_bound_track' in st.session_state['tracking'])):
        # sliders are in percents
        # initialize boundaries tracking
        st.session_state['tracking']['lower_bound_track'] = -20
        st.session_state['tracking']['upper_bound_track'] = 20

    lower_bound = st.session_state['tracking']['lower_bound_track']
    upper_bound = st.session_state['tracking']['upper_bound_track']

    # calculate boundaries
    dataframe[_('Lower Spend Bound')] = dataframe[_('Simulated Spend')] * (100 + lower_bound) / 100
    dataframe[_('Upper Spend Bound')] = dataframe[_('Simulated Spend')] * (100 + upper_bound) / 100

    return dataframe
