import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path                 

BASE_DIR = Path(__file__).parent          

@st.cache_data
def load_data():
    df = pd.read_csv(BASE_DIR / "main_data.csv")
    df["dteday"]    = pd.to_datetime(df["dteday"])
    df["day_type"]  = df["workingday"].map({1: "Hari Kerja", 0: "Akhir Pekan/Libur"})
    df["year_label"]= df["yr"].map({0: "2011", 1: "2012"})
    df["season_label"] = df["season"].map({1:"Spring",2:"Summer",3:"Fall",4:"Winter"})
    df["weather_label"] = df["weathersit"].map({1:"Clear",2:"Misty",3:"Light Rain/Snow",4:"Heavy Rain/Snow"})
    if "temp_celcius" not in df.columns:
        df["temp_celcius"] = df["temp"] * 41
    return df

df = load_data()

st.sidebar.title("Filter Data")
sel_year    = st.sidebar.multiselect("Tahun",  sorted(df["year_label"].unique()), default=sorted(df["year_label"].unique()))
sel_season  = st.sidebar.multiselect("Musim",  ["Spring","Summer","Fall","Winter"], default=["Spring","Summer","Fall","Winter"])
sel_weather = st.sidebar.multiselect("Cuaca",  sorted(df["weather_label"].unique()), default=sorted(df["weather_label"].unique()))
st.sidebar.caption("Dashboard oleh Eka Novia Ai'zatul Ulya")

fdf = df[df["year_label"].isin(sel_year) & df["season_label"].isin(sel_season) & df["weather_label"].isin(sel_weather)].copy()

st.title("🚲 Bike-Sharing Analytics Dashboard")

if fdf.empty:
    st.warning("⚠️ Tidak ada data sesuai filter."); st.stop()

tab1, tab2, tab3, tab4 = st.tabs([
    "Statistik Deskriptif",
    "Rata-rata per Kondisi Cuaca",
    "Rata-rata Penyewaan per Jam",
    "Matriks Korelasi"
])

with tab1:
    st.markdown("**Statistik Deskriptif Variabel Numerik**")
    day_agg = fdf.groupby("dteday").agg(temp=("temp","mean"), hum=("hum","mean"), windspeed=("windspeed","mean"), cnt=("cnt","sum")).reset_index()
    st.dataframe(day_agg[["temp","hum","windspeed","cnt"]].describe().round(4), use_container_width=True)

with tab2:
    st.markdown("**Rata-rata Penyewaan Harian berdasarkan Kondisi Cuaca**")
    day_agg2 = fdf.groupby(["dteday","weather_label"]).agg(cnt=("cnt","sum")).reset_index()
    weather_mean = day_agg2.groupby("weather_label")["cnt"].mean().reset_index()
    weather_mean.columns = ["Kondisi Cuaca", "Rata-rata Penyewaan Harian"]
    weather_mean["Rata-rata Penyewaan Harian"] = weather_mean["Rata-rata Penyewaan Harian"].round(2)
    st.dataframe(weather_mean, use_container_width=True)

with tab3:
    st.markdown("**Rata-rata Penyewaan per Jam**")
    hourly_stats = fdf.groupby("hr")["cnt"].mean().reset_index()
    hourly_stats.columns = ["Jam", "Rata-rata Penyewaan"]
    hourly_stats["Rata-rata Penyewaan"] = hourly_stats["Rata-rata Penyewaan"].round(2)
    st.dataframe(hourly_stats, use_container_width=True, height=300)

with tab4:
    st.markdown("**Matriks Korelasi Variabel Numerik**")
    day_agg3 = fdf.groupby("dteday").agg(temp=("temp","mean"), atemp=("atemp","mean"), hum=("hum","mean"), windspeed=("windspeed","mean"), cnt=("cnt","sum")).reset_index()
    corr_matrix = day_agg3[["temp","atemp","hum","windspeed","cnt"]].corr().round(4)
    st.dataframe(corr_matrix, use_container_width=True)

st.subheader("Pertanyaan 1")
st.markdown("*Bagaimana perbedaan jumlah rata-rata penyewaan sepeda per jam antara hari kerja (workingday) dan akhir pekan (weekend) pada jam sibuk (07:00-09:00 dan 17:00-19:00) selama tahun 2012?*")

hour_2012 = fdf[fdf["yr"] == 1].copy()

if hour_2012.empty:
    st.warning("Tidak ada data tahun 2012 pada filter saat ini. Pilih tahun 2012 di sidebar.")
else:
    hourly_trend = hour_2012.groupby(["day_type","hr"])["cnt"].mean().reset_index()

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=hourly_trend, x="hr", y="cnt", hue="day_type", marker="o",
        palette={"Hari Kerja": "red", "Akhir Pekan/Libur": "blue"}, ax=ax1
    )
    ax1.axvspan(7, 9,  color="green",  alpha=0.15, label="Jam Sibuk Pagi")
    ax1.axvspan(17,19, color="orange", alpha=0.15, label="Jam Sibuk Sore")
    ax1.set_title("Pola Penyewaan Sepeda", fontsize=12)
    ax1.set_xlabel("Jam")
    ax1.set_ylabel("Jumlah Penyewaan")
    ax1.set_xticks(range(0, 24))
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left")
    st.pyplot(fig1); plt.close()

    st.info("**Conclusion:** Hasil analisis menunjukkan adanya perbedaan pola penggunaan sepeda yang cukup signifikan antara hari kerja dan akhir pekan. Pada hari kerja, penggunaan sepeda cenderung mengikuti jadwal aktivitas perkantoran, yang ditandai dengan peningkatan jumlah penyewaan secara tajam pada pukul 08.00 dan 17.00. Kondisi ini mengindikasikan bahwa sepeda dimanfaatkan sebagai sarana transportasi utama oleh para pekerja (komuter).Sebaliknya, pada akhir pekan, pola penggunaan sepeda terlihat lebih fleksibel dan tidak terikat waktu tertentu. Permintaan mulai meningkat secara bertahap sejak sekitar pukul 10.00 dan mencapai puncaknya pada siang hari. Hal ini menunjukkan bahwa pada hari libur, sepeda lebih banyak digunakan untuk keperluan rekreasi atau aktivitas santai.")

    with st.expander("Lihat Tabel Rata-rata per Jam & Tipe Hari"):
        tbl = hourly_trend.pivot(index="hr", columns="day_type", values="cnt").round(2).reset_index()
        tbl.columns.name = None
        tbl = tbl.rename(columns={"hr": "Jam"})
        st.dataframe(tbl, use_container_width=True)

st.subheader("Pertanyaan 2")
st.markdown("*Sejauh mana pengaruh suhu ekstrem (temp > 30°C) terhadap total penyewaan harian oleh pengguna kasual dibandingkan pengguna terdaftar pada musim panas (Summer) tahun 2011 dan 2012?*")

summer_daily = fdf[fdf["season_label"] == "Summer"].groupby("dteday").agg(
    temp_celcius=("temp_celcius","mean"), casual=("casual","sum"), registered=("registered","sum")
).reset_index()

if summer_daily.empty:
    st.warning("Tidak ada data musim Summer pada filter saat ini.")
else:
    hot_summer_days = summer_daily[summer_daily["temp_celcius"] > 30]

    if hot_summer_days.empty:
        st.warning("Tidak ada hari dengan suhu >30°C pada data yang difilter.")
    else:
        mean_rentals = hot_summer_days[["casual","registered"]].mean().reset_index()
        mean_rentals.columns = ["User_Type", "Avg_Rentals"]

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.barplot(data=mean_rentals, x="User_Type", y="Avg_Rentals",
                    hue="User_Type", palette="YlOrRd", legend=False, ax=ax2)
        for idx, row in mean_rentals.iterrows():
            ax2.text(idx, row.Avg_Rentals + 50, f"{int(row.Avg_Rentals)}", ha="center", va="bottom")
        ax2.set_title("Penyewaan saat Suhu Ekstrem (>30°C) di Musim Panas")
        ax2.set_xlabel("Tipe Pengguna")
        ax2.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig2); plt.close()

        st.info("**Conclusion:** Analisis terhadap variabel suhu menunjukkan perbedaan respons antara dua kelompok pengguna. Ketika suhu udara berada pada tingkat yang tinggi (di atas 30°C), pengguna Registered (pelanggan terdaftar) cenderung tetap menggunakan sepeda dengan tingkat penggunaan yang relatif stabil. Hal ini mengindikasikan adanya kebutuhan mobilitas yang bersifat rutin, sehingga mereka tetap menggunakan layanan meskipun kondisi cuaca kurang mendukung. Di sisi lain, pengguna Casual menunjukkan tingkat sensitivitas yang lebih tinggi terhadap suhu. Pada kondisi panas yang ekstrem, jumlah penyewaan dari kelompok ini mengalami penurunan yang cukup signifikan. Hal ini dapat dipahami karena bagi pengguna kasual, bersepeda lebih bersifat pilihan aktivitas santai yang dapat ditunda atau dibatalkan ketika kondisi lingkungan tidak nyaman.")

        with st.expander("Lihat Tabel Rata-rata Penyewaan saat Suhu Ekstrem"):
            tbl2 = mean_rentals.copy()
            tbl2["Avg_Rentals"] = tbl2["Avg_Rentals"].round(2)
            tbl2.columns = ["Tipe Pengguna","Rata-rata Penyewaan (Suhu >30°C)"]
            st.dataframe(tbl2, use_container_width=True)

st.subheader("Matriks Korelasi Faktor Lingkungan")
st.markdown("*Korelasi antara suhu, kelembapan, kecepatan angin, dan total penyewaan.*")

day_corr = fdf.groupby("dteday").agg(temp=("temp","mean"), hum=("hum","mean"), windspeed=("windspeed","mean"), cnt=("cnt","sum")).reset_index()
corr = day_corr[["temp","hum","windspeed","cnt"]].corr()

fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
ax3.set_title("Matriks Korelasi Faktor Lingkungan")
st.pyplot(fig3); plt.close()

st.subheader("Rekomendasi Action Item")
st.markdown("""
**Rekomendasi Action Item:**
- Mengalokasikan lebih banyak sepeda di lokasi dengan permintaan tinggi pada jam sibuk untuk memaksimalkan potensi pendapatan harian.
- Menawarkan paket langganan atau membership yang lebih menarik guna mempertahankan dan meningkatkan jumlah pengguna *registered*.
- Mengurangi biaya operasional dengan membatasi distribusi sepeda pada jam dan kondisi dengan permintaan rendah.
""")