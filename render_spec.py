import sidebar
import read_data


def render_spec(dataframe):
    # render initial table
    selection_dict = sidebar.render_sidebar(dataframe)  # render sidebar and get user selections
    granularity_levels = read_data.granularity_levels  # get granularity levels
    numeric_variables = read_data.numeric_variables  # get numeric variables

    # filter dates
    df_selection = dataframe.query('@selection_dict["Start_date"] <= Date <= @selection_dict["End_date"]')

    for granularity_level in granularity_levels:
        if selection_dict[granularity_level]:
            df_selection = df_selection[df_selection[granularity_level].isin(selection_dict[granularity_level])]

    for granularity_level in reversed(granularity_levels):
        if selection_dict[granularity_level]:
            df_selection = df_selection.groupby([granularity_level, selection_dict['Periodicity']])[numeric_variables].sum()
            break

    return df_selection.sort_values(selection_dict['Periodicity'])
