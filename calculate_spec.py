from translations import _
import read_data


def calculate_spec(dataframe, selection_dict):
    """
    Transforms the dataframe by user selections in the sidebar
    """
    # get granularity levels and translate
    granularity_levels = [_(level) for level in read_data.granularity_levels]
    # get numeric variables and translate
    numeric_variables = [_(variable) for variable in read_data.numeric_variables]

    # filter dataframe dates
    df_selection = dataframe.query('@selection_dict["Start_date"] <= Date <= @selection_dict["End_date"]')

    # filter dataframe by selected granularity levels
    for granularity_level in granularity_levels:
        if selection_dict[granularity_level]:
            df_selection = df_selection[df_selection[granularity_level].isin(selection_dict[granularity_level])]

    # group by the last of non-empty granularity levels
    for granularity_level in reversed(granularity_levels):
        if selection_dict[granularity_level]:
            df_selection = df_selection.groupby([selection_dict['Periodicity'],
                                                 granularity_level])[numeric_variables].sum()
            break
    # the else block will NOT be executed if the loop is stopped by a break statement
    else:
        df_selection = df_selection.groupby([selection_dict['Periodicity']] +
                                            granularity_levels)[numeric_variables].sum()

    # reset index after group by
    df_selection = df_selection.reset_index()

    # set index according to selected periodicity
    df_selection = df_selection.set_index(selection_dict['Periodicity'], drop=True)

    # sort values according to set index
    df_selection = df_selection.sort_index()

    # convert period object to timestamp
    df_selection.index = df_selection.index.to_timestamp()

    return df_selection
