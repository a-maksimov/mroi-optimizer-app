import pandas as pd

granularity_levels = ['Dealership', 'Channel', 'Format', 'Product']
numeric_variables = ['Contribution', 'Spend', 'Revenue_Calculated', 'Marginal_Contribution']
periodicity_list = ['Weekly', 'Monthly', 'Yearly']


def read_data():
    cp_spend = pd.read_csv('data/mmm_hierarchy.csv')
    cp_spend = cp_spend[cp_spend['Power'] > 0].copy()  # remove unspecified variables
    cp_spend['Contribution'] = cp_spend['Contribution'] * 1000  # original numbers are in thousands KG
    cp_spend['Revenue_Calculated'] = cp_spend['Contribution'] * cp_spend['Multiplier']  # calculate revenue
    cp_spend['Marginal_Contribution'] = cp_spend['Contribution'] * cp_spend['Power']  # calculate differential
    cp_spend = cp_spend[cp_spend[numeric_variables].sum(axis=1) != 0]  # remove zero sum rows

    cp_spend = cp_spend.reset_index(drop=True)

    # split weekly data to month and year granularity
    cp_spend['Date'] = pd.to_datetime(cp_spend['Date'])
    for periodicity in periodicity_list:
        # get frequency by the first letter of periodicity
        cp_spend[periodicity] = cp_spend['Date'].dt.to_period(periodicity[0])

    return cp_spend


def get_level_of_granularity(dataframe, current_level, prev_levels_dict=None):
    if prev_levels_dict:
        # filter dataframe by selections
        for level in prev_levels_dict:
            if level in dataframe.columns:
                dataframe = dataframe[dataframe[level].isin(prev_levels_dict[level])]
    return list(pd.unique(dataframe[current_level]))  # create a list of unique values in filtered dataframe
