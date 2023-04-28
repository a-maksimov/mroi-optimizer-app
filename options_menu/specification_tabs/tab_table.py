import streamlit as st
import pandas as pd
from translations import _
import read_data


def spec_table_tab(dataframe):
    # format date strings and translate
    if dataframe.index.name == _('Weekly'):
        dataframe.index = dataframe.index.strftime('%d-%m-%Y')
    elif dataframe.index.name == _('Monthly'):
        dataframe.index = dataframe.index.strftime('%m-%Y')
    else:
        dataframe.index = dataframe.index.strftime('%Y')

    # round numeric variables
    numeric_variables = [_(variable) for variable in read_data.numeric_variables]
    dataframe[numeric_variables] = dataframe[numeric_variables].round(0)

    # add dimensions to the numeric columns names
    column_dimensions = {
        _('Contribution'): _('Contribution') + ', ' + _('kg'),
        _('Spend'): _('Spend') + ', ' + ' €',
        _('Revenue_Calculated'): _('Revenue_Calculated') + ', ' + '€',
        _('Marginal_Contribution'): _('Marginal_Contribution') + ', ' + _('kg'),
    }
    dataframe = dataframe.rename(columns=column_dimensions)

    # display dataframe
    st.dataframe(dataframe, height=600, use_container_width=True)

    # create button to export the table
    csv = dataframe.to_csv(index=False).encode('utf-8')
    st.download_button(
        _('Export table'),
        csv,
        'dataframe.csv',
        'text/csv',
        key='download-csv'
    )
