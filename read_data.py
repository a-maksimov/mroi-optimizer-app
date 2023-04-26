import pandas as pd

# user inputs
numeric_variables = ['Contribution', 'Spend', 'Revenue_Calculated', 'Marginal_Contribution']
granularity_levels = ['Channel', 'Dealership', 'Format', 'Product']
periodicity_list = ['Weekly', 'Monthly', 'Yearly']
simulated_color_plot = 'teal'  # should be same as in CSS
optimised_color_plot = 'coral'  # should be same as in CSS
editable_columns_color = '#ECF0F1'


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
        cp_spend[periodicity] = cp_spend['Date'].dt.to_period(periodicity[0])

    return cp_spend


def get_levels_of_granularity(dataframe):
    granularity_dict = {}
    for granularity in granularity_levels:
        granularity_dict[granularity] = list(pd.unique(dataframe[granularity]))
    return granularity_dict
