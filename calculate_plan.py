import streamlit as st
from translations import _


def get_planned_budget():
    # display_planned_budget is initialized in the session state after this
    if 'display_planned_budget' in st.session_state:
        planned_budget = st.session_state['display_planned_budget']
    # planned_budget is the key of the text input that is rendered on the Planning page
    elif 'planned_budget' in st.session_state:
        planned_budget = float(st.session_state['planned_budget'])
    # otherwise just use the current budget from the Specification page
    else:
        planned_budget = st.session_state['budget']

    # initialize or update display_planned_budget in the session state
    # this can be used to fill the default value for budget text input on Planning page
    st.session_state['display_planned_budget'] = planned_budget

    return planned_budget


def simulated_top_metrics(dataframe, planned_budget):
    """ Calculate simulated top metrics """
    simulated_total_contribution = dataframe[_('Simulated Contribution')].sum()
    simulated_total_revenue = dataframe[_('Simulated Revenue')].sum()
    simulated_total_mroi = simulated_total_revenue / planned_budget

    # save top metrics for Planning calculations
    st.session_state.update({
        'simulated_contribution': simulated_total_contribution,
        'simulated_revenue': simulated_total_revenue,
        'simulated_mroi': simulated_total_mroi
    })


def calculate_plan(dataframe):
    """ Transforms the specification dataframe by planned budget """
    # cleat table
    dataframe = dataframe.fillna(0)
    dataframe = dataframe[dataframe[_('Spend')] > 0]

    # get planned budget for calculations
    planned_budget = get_planned_budget()

    dataframe['Power'] = dataframe[_('Marginal Contribution')] / dataframe[_('Contribution')]
    dataframe['Coefficient'] = dataframe[_('Contribution')] / (dataframe[_('Spend')] ** dataframe['Power'])
    dataframe['Proportion'] = dataframe[_('Spend')] / dataframe[_('Spend')].sum()
    dataframe['Multiplier'] = dataframe[_('Revenue Calculated')] / dataframe[_('Contribution')]

    dataframe[_('Simulated Spend')] = dataframe['Proportion'] * planned_budget
    dataframe[_('Simulated Contribution')] = dataframe['Coefficient'] * (dataframe[_('Simulated Spend')] ** dataframe['Power'])
    dataframe[_('Simulated Revenue')] = dataframe['Multiplier'] * dataframe[_('Simulated Contribution')]

    # calculate simulated top metrics and save values in session state
    simulated_top_metrics(dataframe, planned_budget)

    return dataframe
