import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv("day.csv")

st.header('Bike Sharing Dataset (Day) Dashboard :sparkles:')
st.subheader("Pertanyaan Bisnis")

st.markdown(
    """
    1. Bagaimana performa persewaan sepeda di tahun 2011 dan 2012?
    2. Bagaimana pengaruh perbedaan musim terhadap jumlah sepeda yang disewa?
    3. Seperti apa hubungan temperatur udara dengan jumlah persewaan sepeda dalam satu hari?
    """
)

#Mengganti tipe data pada variabel dteday yang semuala object menjadi datetime
day_datetime_columns = ["dteday"]
for column in day_datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])
day_df.info()

day_df["yr"] = day_df["yr"].apply(lambda x: "2011" if x == 0 else "2012")
day_df["season"] = day_df["season"].apply(lambda x: "springer" if x == 1 else("summer" if x==2 else("fall" if x==3 else "winter")))

Y2011_df = day_df[day_df.yr=="2011"] #mengambil data tahun 2011

monthly_cnt_df = Y2011_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_cnt_df.index = monthly_cnt_df.index.strftime('%B') #mengubah format order date menjadi nama bulan

monthly_cnt_df = monthly_cnt_df.reset_index()
monthly_cnt_df.rename(columns={
    "cnt": "Jumlah Sepeda Disewa"
}, inplace=True)

st.subheader("Visualisasi Pertanyaan 1")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_cnt_df["dteday"],
    monthly_cnt_df["Jumlah Sepeda Disewa"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Jumlah Sepeda Disewa tiap bulan (2011)", loc="center", fontsize=30)
ax.tick_params(axis='x', labelsize=10, rotation=-30)
ax.tick_params(axis='y', labelsize=10)
 
st.pyplot(fig)

Y2012_df = day_df[day_df.yr=="2012"] #mengambil data tahun 2012

monthly_cnt_df2 = Y2012_df.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})
monthly_cnt_df2.index = monthly_cnt_df2.index.strftime('%B') #mengubah format order date menjadi nama bulan

monthly_cnt_df2 = monthly_cnt_df2.reset_index()
monthly_cnt_df2.rename(columns={
    "cnt": "Jumlah Sepeda Disewa"
}, inplace=True)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_cnt_df2["dteday"],
    monthly_cnt_df2["Jumlah Sepeda Disewa"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Jumlah Sepeda Disewa tiap bulan (2012)", loc="center", fontsize=30)
ax.tick_params(axis='x', labelsize=10, rotation=-30)
ax.tick_params(axis='y', labelsize=10)
 
st.pyplot(fig)

st.markdown(
    """
    Jika dilihat dari kedua grafik time-series antara performa jumlah sepeda disewa tahun 2011 dan tahun 2012, dapat disimpulkan bahwa setiap awal semester dalam satu tahun jumlah sepeda disewa cenderung naik secara signifikan dan mencapai puncak pada pertengahan tahun. Namun mulai terjadi penurunan ketika memasuki semester kedua, walaupun kondisi diakhir tahun masih lebih tinggi daripada kondisi di awal tahun.
    """
)


st.subheader("Visualisasi Pertanyaan 2")

season_df=day_df.groupby(by="season").cnt.sum().sort_values(ascending=False) #mengelompokkan cnt berdasarkan musim

fig, ax = plt.subplots(figsize=(16, 8))
ax.pie(
    x=season_df.values,
    labels=["Fall","Summer","Winter","Springer"],
    autopct='%1.1f%%'
)
ax.set_title("Jumlah Sepeda Disewa pada tiap musim", loc="center", fontsize=30)
 
st.pyplot(fig)

st.markdown(
    """
    Jika dilihat dari pie chart peminat persewaan sepeda terbanyak ada pada musim fall dan summer dengan proporsi 32,2% dan 27,9%. Sedangkan pada musim winter dan springer peminat persewaan sepeda cenderung sedikit dengan proporsi 25,6% dan 14,3%. Hasil ini juga berhubungan dengan pertanyaan 1 dimana peminat persewaaan sepeda tinggi di musim fall dan summer yang merupakan musim-musim di pertengahan tahun.
    """
)

st.subheader("Visualisasi Pertanyaan 3")

fig, ax = plt.subplots(figsize=(16, 8))

ax.scatter(x=day_df["temp"], y=day_df["cnt"])
ax.set_title("Hubungan Temperatur Udara dengan Jumlah Sepeda Disewa", loc="center", fontsize=30)

st.pyplot(fig)

st.markdown(
    """
    Berdasarkan grafik scatterplot antara variabel temperatur udara (Celcius) dan Jumlah sepeda disewa, terlihat bahwa kedua variabel berkorelasi positif mendekati nilai 1. Hal tersebut dapat diartikan bahwa tingginya suhu udara membuat peminat persewaaan sepeda tinggi, sebaliknya jika suhu udara rendah maka peminat persewaan sepeda juga rendah.
    """
)






