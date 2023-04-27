import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import read_data
import render_spec

kpis_dict = {''}


def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')


def spec_page():
    # Load the table
    df = render_spec.render_spec(read_data.read_data())

    # Top KPIs
    total_spend = df['Spend'].sum()
    total_contribution = df['Contribution'].sum()
    total_revenue = df['Revenue_Calculated'].sum()
    total_romi = total_revenue / total_spend

    left_column, middle_column1, middle_column2, right_column = st.columns(4)
    with left_column:
        st.subheader('Затраты на медиа:')
        st.subheader(f'€ {round(total_spend / 1e6, 2)} M')
    with middle_column1:
        st.subheader('Общий вклад:')
        st.subheader(f'{round(total_contribution / 1000, 2)}k KG')
    with middle_column2:
        st.subheader('Рассчитанный доход:')
        st.subheader(f'€ {round(total_revenue / 1e6, 2)} M')
    with right_column:
        st.subheader('MROI:')
        st.subheader(f'{round(total_romi, 2)}')

    st.markdown('''---''')

    # Create a tab layout
    tabs = st.tabs(['Таблица', 'Графики'])

    df_display = df.copy()

    # transform df for display
    if read_data.language == 'ru':
        df_display = df_display.rename(columns={'Product': 'Продукт',
                                                'Channel': 'Медиа-канал',
                                                'Dealership': 'Источник данных',
                                                'Format': 'Медиа-формат',
                                                'Contribution': 'Вклад, кг',
                                                'Spend': 'Расход, €',
                                                'Revenue_Calculated': 'Рассчитанный доход, €',
                                                'Marginal_Contribution': 'Предельный вклад, кг'
                                                }
                                       )
    else:
        df_display = df_display.rename(columns={'Contribution': 'Contribution, kg',
                                                'Spend': 'Spend, €',
                                                'Revenue_Calculated': 'Revenue Calculated, €',
                                                'Marginal_Contribution': 'Marginal Contribution, kg'
                                                }
                                       )

    df_display.index = df_display.index.to_timestamp()  # convert period object to timestamp

    # format date strings
    if df_display.index.name == 'Weekly':
        df_display.index = df_display.index.strftime('%d-%m-%Y')
    elif df_display.index.name == 'Monthly':
        df_display.index = df_display.index.strftime('%m-%Y')
    else:
        df_display.index = df_display.index.strftime('%Y')

    # translate index name
    df_display.index.name = read_data.periodicity_dict[df_display.index.name]

    # Define the content of the first tab - Dataframe
    with tabs[0]:
        # display df
        st.dataframe(df_display, height=600, use_container_width=True)

        # create button to export the table
        csv = convert_df(df_display)
        if read_data.language == 'ru':
            label = 'Экспорт таблицы'
        else:
            label = 'Export table'
        st.download_button(
            label,
            csv,
            'df_display.csv',
            'text/csv',
            key='download-csv'
        )

    # Define the content of the second tab - Plot
    with tabs[1]:
        # Create a list of column names to plot
        if read_data.language == 'ru':
            label_var = 'Выберите переменные'
            label_gran = 'Выберите гранулярность'
            numeric_variables = read_data.numeric_variables.values()
        else:
            label_var = 'Select variables'
            label_gran = 'Select granularity'
            numeric_variables = read_data.numeric_variables.keys()
        columns_to_plot = st.multiselect(label_var, numeric_variables)
        granularity_to_plot = st.multiselect(label_gran, list(pd.unique(df_display.iloc[:, 0])))

        fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
        for column in columns_to_plot:
            for granularity in granularity_to_plot:
                if 'доход' in column.lower() or 'расход' in column.lower():
                    fig.add_trace(go.Scatter(x=df_display.index,
                                             y=df_display[df_display.iloc[:, 0] == granularity][column],
                                             name=column + ', ' + granularity,
                                             yaxis='y1'),
                                  secondary_y=False)
                elif 'вклад' in column.lower():
                    fig.add_trace(go.Scatter(x=df_display.index,
                                             y=df_display[df_display.iloc[:, 0] == granularity][column],
                                             name=column + ', ' + granularity,
                                             yaxis='y2'),
                                  secondary_y=True)

        # Set plot title, adjust size and axes labels
        fig.update_layout(title=f'{", ".join(columns_to_plot)}', yaxis_title='Доход/Расход', yaxis2_title='Вклад')

        st.plotly_chart(fig, use_container_width=True)

    return spec_page
