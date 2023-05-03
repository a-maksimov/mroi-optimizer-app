import streamlit as st
from translations import _


def plan_input():
    """
    Input for planned budget
    """
    if 'display_planned_budget' not in st.session_state:
        input_planned_budget = st.text_input(f'{_("Enter planned budget") + ", €"}',
                                             value=st.session_state['budget'],
                                             key='planned_budget')
    else:
        input_planned_budget = st.text_input(f'{_("Enter planned budget") + ", €"}',
                                             value=st.session_state['display_planned_budget'],
                                             key='planned_budget')
    return float(input_planned_budget)


def calculate_plan(df):
    """
    Transforms the specification dataframe by planned budget
    returns a tuple of entered by user planned budget and transformed dataframe based on planned budget
    """
    input_col, *padding = st.columns(4)
    with input_col:
        planned_budget = plan_input()

    df_plan = df.copy()

    df_plan['Power'] = df_plan[_('Marginal Contribution')] / df_plan[_('Contribution')]
    df_plan['Coefficient'] = df_plan[_('Contribution')] / (df[_('Spend')] ** df_plan['Power'])
    df_plan['Proportion'] = df_plan[_('Spend')] / df_plan[_('Spend')].sum()
    df_plan['Multiplier'] = df_plan[_('Revenue Calculated')] / df_plan[_('Contribution')]

    df_plan[_('Simulated Spend')] = df_plan['Proportion'] * planned_budget
    df_plan[_('Simulated Contribution')] = df_plan['Coefficient'] * (df_plan[_('Simulated Spend')] ** df_plan['Power'])
    df_plan[_('Simulated Revenue')] = df_plan['Multiplier'] * df_plan[_('Simulated Contribution')]

    return planned_budget, df_plan
