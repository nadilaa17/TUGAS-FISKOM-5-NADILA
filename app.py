import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Siswa", layout="wide")

# 2. Sidebar Navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.selectbox("Pilih Menu", ["Tabel Data", "Visualisasi Analisis", "Statistik Deskriptif"])

# 3. Judul Utama
st.title("📊 Dashboard Analisis Data Siswa")
st.write("Visualisasi dan Analisis Data 50 Siswa - 20 Soal")

# 4. Upload File
uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if menu == "Tabel Data":
        st.subheader("📋 Tabel Data Siswa")
        st.dataframe(df) # Menampilkan tabel interaktif
        
        # Tombol Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data (CSV)", data=csv, file_name="data_siswa.csv", mime="text/csv")

    elif menu == "Visualisasi Analisis":
        st.subheader("📈 Visualisasi Skor per Soal")
        
        # Menghitung rata-rata skor per soal
        avg_scores = df.mean().reset_index()
        avg_scores.columns = ['Soal', 'Rata-rata Skor']
        
        # Membuat Grafik Batang menggunakan Plotly
        fig = px.bar(avg_scores, x='Soal', y='Rata-rata Skor', 
                     title="Rata-rata Skor per Butir Soal",
                     color='Rata-rata Skor', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Statistik Deskriptif":
        st.subheader("🔢 Ringkasan Statistik")
        st.write(df.describe()) # Menampilkan Mean, Median, Min, Max secara otomatis

else:
    st.info("Silakan unggah file Excel (.xlsx) terlebih dahulu untuk melihat analisis.")



