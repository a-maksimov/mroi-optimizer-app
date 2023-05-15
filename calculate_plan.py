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


def calculate_plan(df):
    """
    Transforms the specification dataframe by planned budget
    returns a tuple of entered by user planned budget and transformed dataframe based on planned budget
    """
    # get planned budget for calculations
    planned_budget = get_planned_budget()

    df_plan = df.copy()

    df_plan['Power'] = df_plan[_('Marginal Contribution')] / df_plan[_('Contribution')]
    df_plan['Coefficient'] = df_plan[_('Contribution')] / (df[_('Spend')] ** df_plan['Power'])
    df_plan['Proportion'] = df_plan[_('Spend')] / df_plan[_('Spend')].sum()
    df_plan['Multiplier'] = df_plan[_('Revenue Calculated')] / df_plan[_('Contribution')]

    df_plan[_('Simulated Spend')] = df_plan['Proportion'] * planned_budget
    df_plan[_('Simulated Contribution')] = df_plan['Coefficient'] * (df_plan[_('Simulated Spend')] ** df_plan['Power'])
    df_plan[_('Simulated Revenue')] = df_plan['Multiplier'] * df_plan[_('Simulated Contribution')]

    return df_plan
