import streamlit as st
from translations import _
import read_data


def plan_table_tab(dataframe):
    # drop columns unnecessary for display
    dataframe = dataframe.drop(['Power', 'Coefficient', 'Proportion', 'Multiplier', _('Marginal Contribution')],
                               axis='columns')

    # round numeric variables
    numeric_variables = [_(variable) for variable in read_data.numeric_variables if _(variable) in dataframe.columns]
    numeric_variables = numeric_variables + [_('Simulated Spend'), _('Simulated Contribution'), _('Simulated Revenue')]
    dataframe[numeric_variables] = dataframe[numeric_variables].round(0)

    # format date strings and translate
    if dataframe.index.name == _('Weekly'):
        dataframe.index = dataframe.index.strftime('%d-%m-%Y')
    elif dataframe.index.name == _('Monthly'):
        dataframe.index = dataframe.index.strftime('%m-%Y')
    else:
        dataframe.index = dataframe.index.strftime('%Y')

    # add dimensions to the numeric columns names
    column_dimensions = {
        _('Contribution'): f'{_("Contribution")}, {_("kg")}',
        _('Spend'): f'{_("Spend")}, €',
        _('Revenue Calculated'): f'{_("Revenue Calculated")}, €',
        _('Simulated Spend'): f'{_("Simulated Spend")}, €',
        _('Simulated Contribution'): f'{_("Simulated Contribution")}, {_("kg")}',
        _('Simulated Revenue'): f'{_("Simulated Revenue")}, €'
    }
    dataframe = dataframe.rename(columns=column_dimensions)

    # display dataframe
    st.dataframe(dataframe, height=600, use_container_width=True)

    # create button to export the table
    csv = dataframe.to_csv().encode('utf-8')
    st.download_button(
        _('Export table'),
        csv,
        'dataframe.csv',
        'text/csv',
        key='download-csv'
    )
