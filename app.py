import streamlit as st
from datetime import datetime
import read_data

date_format = '%d.%m.%Y'

st.set_page_config(page_title='mroi-optimizer-app', page_icon=':bar_chart:', layout='wide')

df = read_data.read_data()

# ---- SIDEBAR ----
st.sidebar.header('Пользовательский ввод')
# Date UI
# Create date range input widget
start_date = df[read_data.Date_var].min()
end_date = df[read_data.Date_var].max()

date_range = st.sidebar.date_input(
    'Выберите интервал анализа',
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    key='date_range'
)

# ---- SIDEBAR ----
granularity = st.sidebar.multiselect(
    'Выберите гранулярность',
    options=read_data.granularity_levels,
    default=read_data.granularity_levels
)

periodicity = st.sidebar.multiselect(
    'Выберите периодичность',
    options=['Weekly', 'Monthly', 'Yearly'],
    default='Weekly'
)

channel = st.sidebar.multiselect(
    'Выберите каналы',
    options=df['Channel'].unique(),
    default=df['Channel'].unique()
)

df_selection = df.query(
    'Channel in @channel & (@date_range[0] <= Date <= @date_range[1])'
)

st.dataframe(df_selection)
