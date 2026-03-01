import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(page_title="Analisis Data Simulasi Siswa", layout="wide")

st.title("📊 Dashboard Analisis Jawaban Siswa")
st.markdown("Dashboard ini menampilkan visualisasi dari data simulasi 50 siswa dan 20 soal.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel('data_simulasi_50_siswa_20_soal.xlsx')
    return df

df = load_data()

# Sidebar untuk Filter
st.sidebar.header("Filter & Pengaturan")
selected_soal = st.sidebar.multiselect("Pilih Soal untuk Detail:", df.columns.tolist(), default=df.columns[:5].tolist())

# Kalkulasi Skor Total (Asumsi skor adalah angka yang tertera)
df['Total_Skor'] = df.sum(axis=1)

# Layout Utama
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Cuplikan Data")
    st.dataframe(df.head(10))

with col2:
    st.subheader("📈 Distribusi Total Skor")
    fig_hist = px.histogram(df, x="Total_Skor", nbins=15, 
                           title="Penyebaran Skor Total Siswa",
                           color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# Bar Chart untuk Rata-rata Skor per Soal
st.subheader("🎯 Rata-rata Skor per Soal")
avg_scores = df.drop(columns=['Total_Skor']).mean().reset_index()
avg_scores.columns = ['Soal', 'Rata-rata Skor']
fig_bar = px.bar(avg_scores, x='Soal', y='Rata-rata Skor', 
                 color='Rata-rata Skor', color_continuous_scale='Viridis')
st.plotly_chart(fig_bar, use_container_width=True)

# Heatmap Korelasi antar Soal
st.subheader("🔗 Heatmap Korelasi Jawaban")
st.write("Melihat apakah ada pola jawaban yang mirip antar satu soal dengan soal lainnya.")
corr = df.drop(columns=['Total_Skor']).corr()
fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto", 
                         color_continuous_scale='RdBu_r', title="Matriks Korelasi Soal")
st.plotly_chart(fig_heatmap, use_container_width=True)

# Analisis Detail per Soal
if selected_soal:
    st.divider()
    st.subheader("🧐 Detail Distribusi Jawaban (Soal Terpilih)")
    
    # Melt data untuk visualisasi kategori
    df_melted = df[selected_soal].melt(var_name='Soal', value_name='Skor')
    fig_box = px.box(df_melted, x='Soal', y='Skor', points="all", color='Soal')
    st.plotly_chart(fig_box, use_container_width=True)

st.sidebar.info(f"Total Siswa: {len(df)}")
st.sidebar.info(f"Total Soal: {len(df.columns) - 1}")


