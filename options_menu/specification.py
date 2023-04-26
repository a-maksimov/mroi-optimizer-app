import streamlit as st
import read_data
import render_spec


def spec_page():
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
        st.subheader('Рассчитанный доход')
        st.subheader(f'€ {round(total_revenue / 1e6, 2)} M')
    with right_column:
        st.subheader('ROMI:')
        st.subheader(f'{round(total_romi, 2)}')

    st.markdown('''---''')

    # transform df for display
    df_display = df.rename(columns={'Product': 'Продукт',
                                    'Channel': 'Медиа-канал',
                                    'Dealership': 'Источник данных',
                                    'Format': 'Медиа-формат',
                                    'Contribution': 'Вклад',
                                    'Spend': 'Расход',
                                    'Revenue_Calculated': 'Рассчитанный доход',
                                    'Marginal_Contribution': 'Предельный вклад'
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
    periodicity_dict = {'Weekly': 'Неделя',
                        'Monthly': 'Месяц',
                        'Yearly': 'Год'
                        }
    df_display.index.name = periodicity_dict[df_display.index.name]

    # display df
    st.dataframe(df_display, height=600, use_container_width=True)

    return spec_page
