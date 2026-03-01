import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Judul Utama
st.set_page_config(page_title="Dashboard Analisis Lengkap", layout="wide")
st.title("📊 Laporan Analisis Data Siswa Terpadu")

uploaded_file = st.file_uploader("Upload file Excel untuk Analisis Otomatis", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    total_skor = df.sum(axis=1) # Menghitung total skor per siswa

    # --- BAGIAN 1: TABEL DATA ---
    st.header("📋 1. Tabel Data Mentah")
    st.dataframe(df, use_container_width=True)
    st.divider()

    # --- BAGIAN 2: STATISTIK DESKRIPTIF ---
    st.header("🔢 2. Statistik Deskriptif")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Ringkasan Data:")
        st.write(df.describe())
    with col2:
        st.metric("Total Siswa", len(df))
        st.metric("Rata-rata Skor Total", round(total_skor.mean(), 2))
    st.divider()

    # --- BAGIAN 3: DISTRIBUSI NILAI & ANALISIS PER SISWA ---
    st.header("📈 3. Distribusi Nilai Total")
    fig_dist = px.histogram(total_skor, nbins=10, title="Distribusi Frekuensi Nilai Total Siswa",
                            labels={'value': 'Skor Total'}, color_discrete_sequence=['indianred'])
    st.plotly_chart(fig_dist, use_container_width=True)
    st.divider()

    # --- BAGIAN 4: ANALISIS PER SOAL ---
    st.header("📊 4. Analisis Per Butir Soal")
    avg_soal = df.mean().reset_index()
    avg_soal.columns = ['Soal', 'Rata-rata']
    fig_soal = px.bar(avg_soal, x='Soal', y='Rata-rata', color='Rata-rata', 
                      title="Rata-rata Skor per Soal (Tingkat Kesulitan)")
    st.plotly_chart(fig_soal, use_container_width=True)
    st.divider()

    # --- BAGIAN 5: KORELASI ANTAR SOAL ---
    st.header("🔗 5. Heatmap Korelasi Antar Soal")
    fig_corr, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=False, cmap='RdBu', ax=ax)
    st.pyplot(fig_corr)

else:
    st.warning("Silakan unggah file terlebih dahulu di bagian atas.")



