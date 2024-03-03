import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt_x": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt_x": "order_count"
    }, inplace=True)
    
    return daily_orders_df

all_df = pd.read_csv("all_data.csv")    

all_df["dteday"] = pd.to_datetime(all_df["dteday"], format="%Y-%m-%d")

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()


with st.sidebar:
    st.markdown("""
    <style>
        .hitam-text {
            color: #000000;
            text-align: center; 
            font-size: 32px; 
            font-weight: bold; 
        }
    </style>
""", unsafe_allow_html=True)

    st.markdown('<p class="hitam-text">Bike Orders</p>', unsafe_allow_html=True)

    st.image("https://github.com/audreynaila/visualization_bike/blob/main/bike.png?raw=true")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

main_df = all_df[(all_df["dteday"] >= start_date) & 
                 (all_df["dteday"] <= end_date)]

daily_orders_df = create_daily_orders_df(main_df)

st.header('Dashboard Penggunaan Sepeda :bike:')

pola_penggunaan_sepeda_berubah = all_df.groupby('mnth_x')['cnt_x'].sum().reset_index()

bulan_tertinggi = pola_penggunaan_sepeda_berubah.loc[pola_penggunaan_sepeda_berubah['cnt_x'].idxmax(), 'mnth_x']

colors = ['skyblue' if bulan == bulan_tertinggi else 'lightgrey' for bulan in pola_penggunaan_sepeda_berubah['mnth_x']]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(pola_penggunaan_sepeda_berubah['mnth_x'], pola_penggunaan_sepeda_berubah['cnt_x'], color=colors)
ax.set_xlabel('Bulan (mnth)')
ax.set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
ax.set_title('Pola Penggunaan Sepeda Berubah Sepanjang Tahun')
st.pyplot(fig)

pola_penggunaan_sepeda_hari = all_df.groupby(['workingday_x', 'weekday_x', 'holiday_x'])['cnt_x'].sum().reset_index()

indeks_max = pola_penggunaan_sepeda_hari['cnt_x'].idxmax()

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.barh(pola_penggunaan_sepeda_hari.index, pola_penggunaan_sepeda_hari['cnt_x'], color='lightgrey')
bars[indeks_max].set_color('skyblue')

ax.set_xlabel('Jumlah Penggunaan Sepeda (cnt)')
ax.set_ylabel('(0: Non-Workday, 1: Work day), (0-6: WeekDay, 0-10: Weekend)')
ax.set_title('Pola Penggunaan Sepeda antara Work Day , Week Day, dan Weekend')
# ax.set_yticklabels(pola_penggunaan_sepeda_hari.index, rotation=45)
st.pyplot(fig)

penggunaan_sepeda_cuaca_x = all_df.groupby('weathersit_x')['cnt_x'].sum().reset_index()

penggunaan_sepeda_cuaca_y = all_df.groupby('weathersit_y')['cnt_y'].sum().reset_index()

indeks_max_x = penggunaan_sepeda_cuaca_x['cnt_x'].idxmax()
indeks_max_y = penggunaan_sepeda_cuaca_y['cnt_y'].idxmax()

fig, axs = plt.subplots(1, 2, figsize=(16, 6))

bars_x = axs[0].bar(penggunaan_sepeda_cuaca_x['weathersit_x'], penggunaan_sepeda_cuaca_x['cnt_x'], color='lightgrey')
bars_x[indeks_max_x].set_color('skyblue')
axs[0].set_xlabel('(weathersit)')
axs[0].set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
axs[0].set_title('Penggunaan Sepeda berdasarkan Kondisi Cuaca pada Days')

bars_y = axs[1].bar(penggunaan_sepeda_cuaca_y['weathersit_y'], penggunaan_sepeda_cuaca_y['cnt_y'], color='lightgrey')
bars_y[indeks_max_y].set_color('skyblue')
axs[1].set_xlabel('(weathersit)')
axs[1].set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
axs[1].set_title('Penggunaan Sepeda berdasarkan Kondisi Cuaca pada Hours')

plt.tight_layout()
st.pyplot(fig)

distribusi_penggunaan_sepeda = all_df.groupby(['season_x', 'weathersit_x'])['cnt_x'].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(distribusi_penggunaan_sepeda.index, distribusi_penggunaan_sepeda['cnt_x'], color='skyblue')
ax.set_xlabel('Kombinasi Musim dan Jenis Cuaca')
ax.set_ylabel('Jumlah Penggunaan Sepeda (cnt)')
ax.set_title('Distribusi Penggunaan Sepeda berdasarkan Musim dan Jenis Cuaca')

labels = [f"Season {s}, Weather {w}" for s, w in zip(distribusi_penggunaan_sepeda['season_x'], distribusi_penggunaan_sepeda['weathersit_x'])]
ax.set_xticks(distribusi_penggunaan_sepeda.index)
ax.set_xticklabels(labels, rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)


all_df['dteday'] = pd.to_datetime(all_df['dteday'])

monthly_days_recency = all_df.groupby(all_df['dteday'].dt.month)['cnt_x'].mean()

monthly_hours_frequency = all_df.groupby(all_df['dteday'].dt.month)['cnt_x'].mean()

monthly_days_monetary = all_df.groupby(all_df['dteday'].dt.month)['cnt_x'].sum()

fig, axs = plt.subplots(3, 1, figsize=(12, 10))

axs[0].bar(monthly_days_recency.index, monthly_days_recency.values, color='skyblue')
axs[0].set_xlabel('Bulan')
axs[0].set_ylabel('Rata-rata Penggunaan Sepeda (Recency) per Hari')
axs[0].set_title('Recency: Pola Penggunaan Sepeda Sepanjang Tahun (per Hari)')

axs[1].bar(monthly_hours_frequency.index, monthly_hours_frequency.values, color='skyblue')
axs[1].set_xlabel('Bulan')
axs[1].set_ylabel('Rata-rata Penggunaan Sepeda (Frequency) per Jam')
axs[1].set_title('Frequency: Pola Penggunaan Sepeda Sepanjang Tahun (per Jam)')

axs[2].bar(monthly_days_monetary.index, monthly_days_monetary.values, color='skyblue')
axs[2].set_xlabel('Bulan')
axs[2].set_ylabel('Total Penggunaan Sepeda (Monetary) per Bulan')
axs[2].set_title('Monetary: Pola Penggunaan Sepeda Sepanjang Tahun (per Bulan)')

plt.tight_layout()
st.pyplot(fig)

st.caption('Copyright © Audrey Naila 2024')