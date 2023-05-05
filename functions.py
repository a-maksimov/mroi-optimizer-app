import pandas as pd
import numpy as np
from translations import _


def response_curves_data(dataframe, granularity_level, granularity):
    # remove rows with zero spend
    dataframe = dataframe[dataframe[_('Spend')] > 0].copy()

    dataframe['Estimate'] = dataframe[_('Contribution')] / (dataframe[_('Spend')] ** dataframe['Power'])
    dataframe['Max_spend'] = np.max(dataframe[_('Spend')])
    dataframe = dataframe.reset_index(drop=True)

    for i in range(1, 21):
        dataframe['var_val'] = i
        dataframe['Spd'] = np.where(dataframe['var_val'] < 11, dataframe[_('Spend')] * (i / 10),
                                    dataframe['Max_spend'] * (i / 10))
        dataframe['Rev'] = dataframe['Estimate'] * (dataframe['Spd'] ** dataframe['Power']) * dataframe['Multiplier']
        dataframe = dataframe.rename(columns={'Spd': 'Spend_{}'.format(i), 'Rev': 'Revenue_{}'.format(i)})

    dataframe = dataframe.drop(
        [_('Contribution'), _('Spend'), _('Revenue Calculated'),
         _('Marginal Contribution'), 'Power', 'Coefficient', 'Proportion', 'Multiplier',
         _('Simulated Spend'), _('Simulated Contribution'),
         _('Simulated Revenue'), 'Estimate', 'Max_spend', 'var_val', ], axis='columns')

    # filter dataframe for single variable
    dataframe = dataframe[dataframe[granularity_level] == granularity]

    dataframe = pd.melt(dataframe, id_vars=granularity_level, var_name='variable', value_name='value')

    dataframe['Point'] = dataframe['variable'].str.split('_').map(lambda x: x[1]).astype(float)

    dataframe['Metric'] = np.where(dataframe['variable'].str.startswith('Spend'), 'Spend', 'Revenue')

    dataframe = pd.pivot_table(dataframe, index=[granularity_level] + ['Point'], columns='Metric',
                               values='value').reset_index()

    dataframe = dataframe.reset_index(drop=True)

    return dataframe
