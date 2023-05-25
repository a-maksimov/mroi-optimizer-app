import pandas as pd
import numpy as np
from translations import _


def timeseries_data_stacked(dataframe, granularity_level, granularity, numeric_variable, percents=False):
    if granularity_level:
        # drop unnecessary columns
        dataframe = dataframe[dataframe.columns.intersection([granularity_level, numeric_variable])].copy()

        if percents:
            # group by date index and calculate the sum of numeric variable
            df_grouped = dataframe.groupby(dataframe.index)[numeric_variable].sum()

            # merge original DataFrame with grouped DataFrame
            df_merged = dataframe.merge(df_grouped, left_index=True, right_on=df_grouped.index, suffixes=('', '_sum'))

            # calculate percents
            dataframe[numeric_variable] = 100 * (df_merged[numeric_variable] / df_merged[numeric_variable + '_sum'])

        # filter for single granularity
        dataframe = dataframe[dataframe[granularity_level] == granularity]

        return dataframe


def timeseries_data(dataframe, granularity_level, numeric_variable, percents=False):
    if granularity_level:
        # drop unnecessary columns
        dataframe = dataframe[dataframe.columns.intersection([granularity_level, numeric_variable])].copy()

        if percents:
            # group by date index and calculate the sum of numeric variable
            df_grouped = dataframe.groupby(dataframe.index)[numeric_variable].sum()

            # merge original DataFrame with grouped DataFrame
            df_merged = dataframe.merge(df_grouped, left_index=True, right_on=df_grouped.index, suffixes=('', '_sum'))

            # calculate percents
            dataframe[numeric_variable] = 100 * (df_merged[numeric_variable] / df_merged[numeric_variable + '_sum'])

        return dataframe


def mroi_plot(dataframe, granularity_level, numeric_variables, percents=False):
    if granularity_level:
        # drop unnecessary columns
        dataframe = dataframe[dataframe.columns.intersection([granularity_level] + numeric_variables)].copy()

        # calculate percents
        percent_variables = []
        if percents:
            pct = '_pct'
            percent_variables = [variable + pct for variable in numeric_variables]
            dataframe[percent_variables] = (100 * (dataframe[numeric_variables] / dataframe[numeric_variables].sum()))

        # get aggregated data
        dataframe = dataframe.groupby(granularity_level)[numeric_variables + percent_variables].sum()

        return dataframe


def response_curves_data(dataframe, granularity_level, granularity, max_spend, number_of_steps):
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
    i = 0
    dataframe['Spd'] = 0
    mult = (max_spend / dataframe[_('Spend')].sum()) / number_of_steps
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


def bar_data(dataframe, granularity_level, granularity_to_plot, numeric_variables, percents=False):
    if granularity_level:
        # filter out variables that are unselected
        dataframe = dataframe[dataframe[granularity_level].isin(granularity_to_plot)].copy()

        # calculate percents
        if percents:
            dataframe[numeric_variables] = (100 * (dataframe[numeric_variables] /
                                                   dataframe[numeric_variables].sum()))

        # get aggregated data
        dataframe = dataframe.groupby(granularity_level)[numeric_variables].sum()

        return dataframe


def stacked_bar_data(dataframe, granularity_level, granularity_to_plot, numeric_variables, percents=False):
    # filter out variables that are unselected
    dataframe = dataframe[dataframe[granularity_level].isin(granularity_to_plot)]

    # filter out columns
    dataframe = dataframe[dataframe.columns.intersection([granularity_level] + numeric_variables)]

    # calculate percents
    if percents:
        dataframe[numeric_variables] = (100 * (dataframe[numeric_variables] /
                                               dataframe[numeric_variables].sum())).copy()

    # get aggregated data
    dataframe = dataframe.groupby(granularity_level)[numeric_variables].sum().reset_index()
    if numeric_variables:
        dataframe = dataframe.sort_values(numeric_variables[0], ascending=False)

    # melt spends
    dataframe = pd.melt(dataframe, id_vars=granularity_level, var_name=_('Spend'), value_name='value')

    return dataframe
