import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency
import seaborn as sns
sns.set(style='dark')

day_df = pd.read_csv('/content/day.csv')
hour_df = pd.read_csv('/content/hour.csv')
datetime_columns = ["dteday"]

for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])
  hour_df[column] = pd.to_datetime(hour_df[column])

day_df['season'] = day_df['season'].astype(str)
hour_df['season'] = hour_df['season'].astype(str)

season_map = {
    '1': 'spring',
    '2': 'summer',
    '3': 'fall',
    '4': 'winter'
}
day_df['season'] = day_df['season'].map(season_map)
hour_df['season'] = hour_df['season'].map(season_map)

def categorize_hour(hr):
    if 0 <= hr < 5:
        return 'Dawn'
    elif 5 <= hr < 10:
        return 'Morning'
    elif 10 <= hr < 15:
        return 'Noon'
    elif 15 <= hr < 19:
        return 'Afternoon'
    else:
        return 'Evening'

# Menambahkan kolom 'sesi_waktu'
hour_df['time_session'] = hour_df['hr'].apply(categorize_hour)

hour_df.head(25)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("/content/bike_rent.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

def create_monthly_rents_df(df):
    monthly_rents_df = df.resample(rule='M', on='dteday').agg({
    "instant": "nunique",

    })
    monthly_rents_df = monthly_rents_df.reset_index()
    monthly_rents_df.rename(columns={
        "instant": "rent_count",

}, inplace=True)
    
    return monthly_rents_df


def create_bytimeS_df(df):
    bytimeS_df = df.groupby(by="time_session").instant.nunique().reset_index()
    bytimeS_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return bytimeS_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").instant.nunique().reset_index()
    byseason_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byseason_df

day_date_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

hour_date_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

monthly_rents_df = create_monthly_rents_df(day_date_df)
bytimeS_df = create_bytimeS_df(hour_date_df)
byseason_df = create_byseason_df(day_date_df)

st.header('Radit Bike Rental Dashboard :sparkles:')

st.subheader('Monthly Rents')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rents = monthly_rents_df.rent_count.sum()
    st.metric("Total rents", value=total_rents)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rents_df["dteday"],
    monthly_rents_df["rent_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Clustering Number of Bike Rentals")
 
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
  
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="customer_count", 
        x="time_session",
        data=bytimeS_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Time Session", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="customer_count", 
        x="season",
        data=byseason_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Season", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)