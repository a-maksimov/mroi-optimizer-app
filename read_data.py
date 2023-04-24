import pandas as pd

# user inputs
Date_var = 'Date'
numeric_var = ['Contribution', 'Spend', 'Revenue_Calculated', 'Marginal_Contribution']
granularity_levels = ['Channel', 'Dealership', 'Format', 'Product']
simulated_color_plot = 'teal'  # should be same as in CSS
optimised_color_plot = 'coral'  # should be same as in CSS
editable_columns_color = '#ECF0F1'
currency_symbol = '€ '


def read_data():
    # TODO: Add clean option
    cp_spend = pd.read_csv('data/mmm_hierarchy.csv')

    cp_spend = cp_spend[cp_spend['Power'] > 0].copy()  # remove unspecified variables

    cp_spend['Contribution'] = cp_spend['Contribution'] * 1000  # original numbers are in thousands KG

    cp_spend['Revenue_Calculated'] = cp_spend['Contribution'] * cp_spend['Multiplier']  # calculate revenue

    cp_spend['Marginal_Contribution'] = cp_spend['Contribution'] * cp_spend['Power']  # calculate differential

    cp_spend = cp_spend[cp_spend[numeric_var].sum(axis=1) != 0]  # remove zero sum rows

    # split weekly data to month and year granularity
    cp_spend[Date_var] = pd.to_datetime(cp_spend[Date_var])
    cp_spend['Weekly'] = cp_spend[Date_var].dt.to_period('W')
    cp_spend['Monthly'] = cp_spend[Date_var].dt.to_period('M')
    cp_spend['Yearly'] = cp_spend[Date_var].dt.to_period('Y')

    return cp_spend


def get_levels_of_granularity(dataframe):
    granularity_dict = {}
    for granularity in granularity_levels:
        granularity_dict[granularity] = list(pd.unique(dataframe[granularity]))
    return granularity_dict
