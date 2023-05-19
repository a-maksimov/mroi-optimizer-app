import streamlit as st
from translations import _


def opt_table_tab(dataframe):
    # drop columns unnecessary for display
    dataframe = dataframe.drop(['Power',
                                'Coefficient',
                                'Proportion',
                                'Multiplier',
                                _('Contribution'),
                                _('Spend'),
                                _('Revenue Calculated'),
                                _('Marginal Contribution')],
                               axis='columns')

    # round numeric variables
    numeric_variables = [_('Simulated Spend'), _('Simulated Contribution'), _('Simulated Revenue'),
                         _('Lower Spend Bound'), _('Upper Spend Bound')]
    if 'df_optimized' in st.session_state:
        numeric_variables = numeric_variables + [_('Optimized Spend'),
                                                 _('Optimized Contribution'),
                                                 _('Optimized Revenue')]

    dataframe[numeric_variables] = dataframe[numeric_variables].round(0)

    # format date strings and translate
    if dataframe.index.name == _('Weekly'):
        dataframe.index = dataframe.index.strftime('%d-%m-%Y')
    elif dataframe.index.name == _('Monthly'):
        dataframe.index = dataframe.index.strftime('%m-%Y')
    else:
        dataframe.index = dataframe.index.strftime('%Y')

    # move bounds columns to the end
    dataframe = dataframe[[column for column in dataframe
                           if column not in [_('Lower Spend Bound'), _('Upper Spend Bound')]] +
                          [_('Lower Spend Bound'), _('Upper Spend Bound')]]

    # add dimensions to the numeric columns names
    column_dimensions = {
        _('Simulated Spend'): f'{_("Simulated Spend")}, €',
        _('Simulated Contribution'): f'{_("Simulated Contribution")}, {_("kg")}',
        _('Simulated Revenue'): f'{_("Simulated Revenue")}, €',
        _('Optimized Spend'): f'{_("Optimized Spend")}, €',
        _('Optimized Contribution'): f'{_("Optimized Contribution")}, {_("kg")}',
        _('Optimized Revenue'): f'{_("Optimized Revenue")}, €',
        _('Lower Spend Bound'): f'{_("Lower Spend Bound")}, €',
        _('Upper Spend Bound'): f'{_("Upper Spend Bound")}, €'
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
