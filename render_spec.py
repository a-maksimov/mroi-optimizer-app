import sidebar
import read_data


def render_spec(dataframe):
    # render initial table
    selection_dict = sidebar.render_sidebar(dataframe)  # render sidebar and get user selections
    granularity_levels = read_data.granularity_levels  # get granularity levels
    numeric_variables = read_data.numeric_variables  # get numeric variables

    # filter dataframe dates
    df_selection = dataframe.query('@selection_dict["Start_date"] <= Date <= @selection_dict["End_date"]')

    # filter dataframe by selected granularity levels
    for granularity_level in granularity_levels:
        if selection_dict[granularity_level]:
            df_selection = df_selection[df_selection[granularity_level].isin(selection_dict[granularity_level])]

    # group by the last of non-empty granularity levels
    for granularity_level in reversed(granularity_levels):
        if selection_dict[granularity_level]:
            df_selection = df_selection.groupby([selection_dict['Periodicity'], granularity_level])[numeric_variables].sum()
            break
    else:
        df_selection = df_selection.groupby([selection_dict['Periodicity']] + granularity_levels)[numeric_variables].sum()

    df_selection = df_selection.reset_index()  # reset index after groupby()

    df_selection = df_selection.set_index(selection_dict['Periodicity'])  # set index according to selected periodicity

    df_selection = df_selection.sort_index()  # sort values according to set index

    return df_selection
