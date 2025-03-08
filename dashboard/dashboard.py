import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load dataset
def load_data():
    df = pd.read_csv("all_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

all_df = load_data()

# Helper Functions
def create_user_count_df(df):
    return df[['date', 'casual', 'registered', 'total_count']].groupby('date').sum().reset_index()

def create_days_count_df(df):
    return df[['weekday', 'total_count']].groupby('weekday').sum().reset_index()

def create_season_df(df):
    return df[['musim', 'total_count']].groupby('musim').sum().reset_index()

def create_weather_df(df):
    return df[['cuaca', 'total_count']].groupby('cuaca').sum().reset_index()

def create_user_hour_df(df):
    return df[['hour', 'total_count']].groupby('hour').sum().reset_index()

# Sidebar Filters
st.sidebar.image("sepeda.jpg", use_container_width=True)
st.sidebar.header("Filter Data")

# Date Range Selection
min_date, max_date = all_df["date"].min(), all_df["date"].max()


# Add option for users to select which analysis to view
analysis_option = st.sidebar.selectbox(
    "Pilih Analisis",
    ["Tren Penggunaan per Bulan", "Pengaruh Musim dan Cuaca", "Tren Pengguna per Jam"]
)

# Filter Data
main_df = all_df

# Data Preparation
user_count = create_user_count_df(main_df)
days_count = create_days_count_df(main_df)
season = create_season_df(main_df)
weather = create_weather_df(main_df)
user_hour = create_user_hour_df(main_df)

# Dashboard Layout
st.title('Bike Sharing System Dashboard 🚴')

# Conditional Analysis Display
if analysis_option == "Tren Penggunaan per Bulan":
    st.subheader("Tren Penggunaan per Bulan")
    
    # Mengonversi tahun dari 0,1 menjadi 2011,2012
    all_df["year"] = all_df["year"].map({0: 2011, 1: 2012})
    
    # Filter data hanya berdasarkan tahun yang dipilih
    trend_df = all_df[all_df["year"].isin([2011, 2012])].groupby(["year", "month"])['total_count'].sum().reset_index()

    # Visualisasi dengan Plotly
    fig_trend = px.line(
        trend_df, 
        x="month", 
        y="total_count", 
        color="year", 
        markers=True, 
        labels={"month": "Bulan", "total_count": "Jumlah Pengguna", "year": "Tahun"},
        title="Trend Penggunaan Bike Sharing"
    )

    # Menampilkan plot pada Streamlit
    st.plotly_chart(fig_trend, use_container_width=True)



elif analysis_option == "Pengaruh Musim dan Cuaca":
    st.subheader("Pengaruh Musim dan Cuaca")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(season, names='musim', values='total_count', title='Users by Season')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(weather, names='cuaca', values='total_count', title='Users by Weather Condition')
        st.plotly_chart(fig, use_container_width=True)

elif analysis_option == "Tren Pengguna per Jam":
    st.subheader("Tren Pengguna per Jam")
    
    fig = px.line(user_hour, x="hour", y="total_count", markers=True, title="Users Per Hour")
    st.plotly_chart(fig, use_container_width=True)

# Final message
st.write("Dashboard ini membantu menganalisis tren penggunaan bike-sharing berdasarkan waktu, musim, dan cuaca.")
st.caption('Copyright (c) Ahmad Radesta')
