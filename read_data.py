import pandas as pd
from translations import _

granularity_levels = ['Dealership', 'Channel', 'Format', 'Product']
numeric_variables = ['Contribution', 'Spend', 'Revenue_Calculated', 'Marginal_Contribution']
periodicity_list = ['Weekly', 'Monthly', 'Yearly']


def translate_table(df):
    # translate df for selection and display
    columns_translate = {'Product': _('Product'),
                         'Channel': _('Channel'),
                         'Dealership': _('Dealership'),
                         'Format': _('Format'),
                         'Contribution': _('Contribution'),
                         'Spend': _('Spend'),
                         'Revenue_Calculated': _('Revenue_Calculated'),
                         'Marginal_Contribution': _('Marginal_Contribution'),
                         'Weekly': _('Weekly'),
                         'Monthly': _('Monthly'),
                         'Yearly': _('Yearly')
                         }
    return df.rename(columns=columns_translate)


def read_data(filename):
    """ Loads results of MMM modeling and returns the transformed and translated dataframe """

    df = pd.read_csv(filename)

    df = df[df['Power'] > 0].copy()  # remove unspecified variables
    df['Contribution'] = df['Contribution'] * 1000  # original numbers are in thousands KG
    df['Revenue_Calculated'] = df['Contribution'] * df['Multiplier']  # calculate revenue
    df['Marginal_Contribution'] = df['Contribution'] * df['Power']  # calculate differential
    df = df[df[numeric_variables].sum(axis=1) != 0]  # remove zero sum rows

    df = df.reset_index(drop=True)

    df['Date'] = pd.to_datetime(df['Date'])

    # expand the Date by periodicity_list
    for periodicity in periodicity_list:
        # get frequency by the first letter of periodicity
        df[periodicity] = df['Date'].dt.to_period(periodicity[0])

    return translate_table(df)


def get_level_of_granularity(dataframe, current_level, prev_levels_dict=None):
    """ Gets a list of unique values in a current level of granularity of a filtered dataframe """
    if prev_levels_dict:
        # filter dataframe by selections
        for level in prev_levels_dict:
            if level in dataframe.columns:
                dataframe = dataframe[dataframe[level].isin(prev_levels_dict[level])]
    return [_(item) for item in pd.unique(dataframe[current_level])]
