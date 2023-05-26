import pandas as pd
from translations import _, translate_table

granularity_levels = ['Dealership', 'Channel', 'Format', 'Product']
numeric_variables = ['Contribution', 'Spend', 'Revenue Calculated', 'Marginal Contribution']
periodicity_list = ['Weekly', 'Monthly', 'Yearly']
target_products = [
    'Brand',
    'Product_1',
    'Product_2',
    'Product_3',
    'Product_4',
    'Product_5',
    'Category_1',
    'Category_2'
]


def read_data(filename):
    """
    Loads results of MMM modeling and returns the transformed and translated dataframe
    """
    dataframe = pd.read_csv(filename)

    # keep only products related to target variable
    dataframe = dataframe[dataframe['Product'].isin(target_products)]

    dataframe = dataframe[dataframe['Power'] > 0].copy()  # remove unspecified variables
    dataframe['Contribution'] = dataframe['Contribution'] * 1000  # original numbers are in thousands kgs
    dataframe['Revenue Calculated'] = dataframe['Contribution'] * dataframe['Multiplier']  # calculate revenue
    dataframe['Marginal Contribution'] = dataframe['Contribution'] * dataframe['Power']
    dataframe = dataframe[dataframe[numeric_variables].sum(axis=1) != 0]  # remove zero sum rows

    dataframe = dataframe.reset_index(drop=True)

    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

    # expand the Date by periodicity_list
    for periodicity in periodicity_list:
        # get frequency by the first letter of periodicity
        dataframe[periodicity] = dataframe['Date'].dt.to_period(periodicity[0])

    return translate_table(dataframe)


def get_level_of_granularity(dataframe, current_level, prev_levels_dict=None):
    """
    Gets a list of unique values in a current level of granularity of a filtered dataframe
    """
    if prev_levels_dict:
        # filter dataframe by selections
        for level in prev_levels_dict:
            if level in dataframe.columns:
                dataframe = dataframe[dataframe[level].isin(prev_levels_dict[level])]
    return [_(item) for item in pd.unique(dataframe[current_level])]
