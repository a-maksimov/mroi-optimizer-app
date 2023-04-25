import streamlit as st
from read_data import read_data
from render_spec import render_spec

st.set_page_config(page_title='MROI Optimizer App',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')

df = render_spec(read_data())

# ---- MAINPAGE ----
st.title(':chart_with_upwards_trend: MROI Optimizer App')
st.markdown("##")

# TOP KPI's
total_spend = df['Spend'].sum()
total_contribution = df['Contribution'].sum()
total_revenue = df['Revenue_Calculated'].sum()
total_romi = total_revenue/total_spend

left_column, middle_column1, middle_column2, right_column = st.columns(4)
with left_column:
    st.subheader('Затраты на медиа:')
    st.subheader(f'€ {round(total_spend / 1e6, 2)} M')
with middle_column1:
    st.subheader('Общий вклад:')
    st.subheader(f'{round(total_contribution / 1000, 2)}k KG')
with middle_column2:
    st.subheader(' Рассчитанный доход')
    st.subheader(f'€ {round(total_revenue / 1e6, 2)} M')
with right_column:
    st.subheader('ROMI:')
    st.subheader(f'{round(total_romi, 2)}')

st.markdown("""---""")

st.dataframe(df, height=600, use_container_width=True)


