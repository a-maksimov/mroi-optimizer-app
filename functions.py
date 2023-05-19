import streamlit as st
import pandas as pd
import numpy as np
import config
from translations import _


@st.cache_data(show_spinner=False)
def timeseries_data(dataframe, granularity_level, granularity, numeric_variable):
    # drop unnecessary columns
    dataframe = dataframe[dataframe.columns.intersection([granularity_level, numeric_variable])]

    # filter dataframe for single variable
    dataframe = dataframe[dataframe[granularity_level] == granularity]

    return dataframe


@st.cache_data(show_spinner=False)
def response_curves_data(dataframe, granularity_level, granularity):
    """
    Returns a tuple of dataframe with spend and calculated revenue data points for a granularity under granularity level
    and an index of a point with current spend and corresponding revenue.
    """
    # filter dataframe for single granularity under granularity level
    dataframe = dataframe[dataframe[granularity_level] == granularity]

    # remove rows with zero spend
    dataframe = dataframe[dataframe[_('Spend')] > 0].copy()
    dataframe['Estimate'] = dataframe[_('Contribution')] / (dataframe[_('Spend')] ** dataframe['Power'])
    dataframe = dataframe.reset_index(drop=True)

    # drop unnecessary columns
    dataframe = dataframe[dataframe.columns.intersection([granularity_level, _('Spend'), 'Estimate', 'Power',
                                                          'Multiplier', 'Estimate'])]
    # In order to calculate the same number of points (100) for a wide range of spend values, we calculate the step.
    # We also want the step to be a multiple of current spend value to put it on a curve plot.
    max_spend = config.maximum_total_spend
    num_of_steps = 85
    i = 0
    dataframe['Spd'] = 0
    mult = (max_spend / dataframe[_('Spend')].sum()) / num_of_steps
    if mult >= 1:
        dataframe['step'] = dataframe[_('Spend')] * int(mult)
    else:
        dataframe['step'] = dataframe[_('Spend')] * round(mult, 2)
    while dataframe['Spd'].sum() <= max_spend:
        # Calculate spend and revenue sets of data for every week.
        # After pivot table aggregation we will get the current total spend and total revenue for this granularity.
        # We will put this point on a curve plot.
        dataframe['Spd'] = dataframe['step'].multiply(i)
        dataframe['Rev'] = dataframe['Estimate'] * (dataframe['Spd'] ** dataframe['Power']) * dataframe['Multiplier']
        dataframe = dataframe.rename(columns={'Spd': f'Spend_{i}', 'Rev': f'Revenue_{i}'})
        dataframe['Spd'] = dataframe[f'Spend_{i}']
        i += 1

    dataframe = dataframe.drop([_('Spend'), 'Power', 'Spd', 'Estimate', 'step', 'Multiplier'], axis='columns')

    dataframe = pd.melt(dataframe, id_vars=granularity_level, var_name='variable', value_name='value')

    dataframe['metric'] = np.where(dataframe['variable'].str.contains('Spend'), 'Spend', 'Revenue')

    dataframe['point'] = dataframe['variable'].map(lambda v: v.split('_')[1])

    curve_data = dataframe.pivot_table(values='value',
                                       index=dataframe['point'].astype(int),
                                       columns='metric',
                                       aggfunc=sum)
    # calculate the index of a point marking the current spend and revenue
    if mult >= 1:
        marker_loc = int(mult)
    else:
        marker_loc = int(1 / round(mult, 2))
    return curve_data, marker_loc
