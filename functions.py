import pandas as pd
import numpy as np


def response_curves_data(data, granularity):
    input_data = data.copy()
    input_data['Power'] = input_data['Marginal_Contribution'] / input_data['Revenue']
    input_data['Estimate'] = input_data['Revenue'] / (input_data['Spend'] ** input_data['Power'])
    max_spend = np.max(input_data['Spend'])
    input_data['Max_spend'] = float(max_spend)
    input_data = input_data.reset_index(drop=True)

    for i in range(1, 21):
        input_data['var_val'] = i
        input_data['Spd'] = np.where(input_data['var_val'] < 11, input_data['Spend'] * (i / 10),
                                     input_data['Max_spend'] * (i / 10))
        input_data['Rev'] = input_data['Estimate'] * (input_data['Spd'] ** input_data['Power'])
        input_data = input_data.rename(columns={'Spd': 'Spend_{}'.format(i), 'Rev': 'Revenue_{}'.format(i)})

    input_data = input_data.drop(
        ['Revenue', 'Marginal_Contribution', 'Power', 'Spend', 'Estimate', 'Max_spend', 'var_val'], axis=1)
    input_data = pd.melt(input_data, id_vars=granularity, var_name='variable', value_name='value')
    input_data['Point'] = np.where(input_data['variable'].str.startswith('Spend'), input_data['variable'].str[-2:],
                                   input_data['variable'].str[-2:].str[-2:])
    input_data['Point'] = input_data['Point'].astype(float)
    input_data['Metric'] = np.where(input_data['variable'].str.startswith('Spend'), 'Spend', 'Revenue')
    input_data = pd.pivot_table(input_data, index=granularity + ['Point'], columns='Metric',
                                values='value').reset_index()

    return input_data
