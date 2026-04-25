import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# KONFIGURASI HALAMAN WEB STREAMLIT

st.set_page_config(page_title="Simulasi ROE Polisi", page_icon="🚓", layout="centered")

st.title("🚓 Kalkulator Eskalasi Taktis (Rules of Engagement)")
st.write("Sistem inferensi fuzzy untuk menentukan tingkat respon kepolisian berdasarkan tingkat ancaman dan SOP keselamatan publik.")
st.markdown("---")


# 1. DEFINISI VARIABEL FUZZY

agresi = ctrl.Antecedent(np.arange(0, 101, 1), 'agresi')
jarak = ctrl.Antecedent(np.arange(0, 51, 1), 'jarak')
sipil = ctrl.Antecedent(np.arange(0, 101, 1), 'sipil')
tindakan = ctrl.Consequent(np.arange(0, 101, 1), 'tindakan')


# 2. FUNGSI KEANGGOTAAN (MEMBERSHIP FUNCTIONS)

agresi['pasif'] = fuzz.trapmf(agresi.universe, [0, 0, 30, 50])
agresi['tangan_kosong'] = fuzz.trimf(agresi.universe, [30, 50, 70])
agresi['bersenjata'] = fuzz.trapmf(agresi.universe, [50, 70, 100, 100])

jarak['dekat'] = fuzz.trapmf(jarak.universe, [0, 0, 5, 15])
jarak['menengah'] = fuzz.trimf(jarak.universe, [5, 15, 30])
jarak['jauh'] = fuzz.trapmf(jarak.universe, [15, 30, 50, 50])

sipil['sepi'] = fuzz.trapmf(sipil.universe, [0, 0, 20, 40])
sipil['sedang'] = fuzz.trimf(sipil.universe, [20, 50, 80])
sipil['ramai'] = fuzz.trapmf(sipil.universe, [60, 80, 100, 100])

tindakan['verbal'] = fuzz.trapmf(tindakan.universe, [0, 0, 30, 50])
tindakan['less_lethal'] = fuzz.trimf(tindakan.universe, [30, 50, 80])
tindakan['lethal'] = fuzz.trapmf(tindakan.universe, [60, 80, 100, 100])


# 3. ATURAN FUZZY (RULES) - Mencegah Salah Tembak

rule1 = ctrl.Rule(agresi['pasif'], tindakan['verbal'])
rule2 = ctrl.Rule(agresi['tangan_kosong'] & jarak['jauh'], tindakan['verbal'])
rule3 = ctrl.Rule(agresi['tangan_kosong'] & jarak['dekat'], tindakan['less_lethal'])
# Jika tersangka bersenjata tapi area sangat ramai warga sipil, tahan tembakan mematikan
rule4 = ctrl.Rule(agresi['bersenjata'] & sipil['ramai'], tindakan['less_lethal']) 
rule5 = ctrl.Rule(agresi['bersenjata'] & jarak['dekat'] & ~sipil['ramai'], tindakan['lethal'])
rule6 = ctrl.Rule(agresi['bersenjata'] & jarak['jauh'], tindakan['less_lethal'])

tindakan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
simulasi = ctrl.ControlSystemSimulation(tindakan_ctrl)


# 4. ANTARMUKA STREAMLIT (UI)

st.sidebar.header("🎛️ Panel Parameter Situasi")
st.sidebar.write("Geser slider untuk mengubah kondisi di lapangan:")

val_agresi = st.sidebar.slider("Agresivitas Tersangka (0-100)", 0, 100, 50, help="0 = Diam/Pasif, 100 = Mengancam dengan senjata mematikan")
val_jarak = st.sidebar.slider("Jarak Tersangka (Meter)", 0, 50, 15, help="Jarak fisik antara petugas dan tersangka")
val_sipil = st.sidebar.slider("Kepadatan Warga Sipil (0-100)", 0, 100, 20, help="0 = Sepi/Kosong, 100 = Kerumunan padat")

st.sidebar.markdown("---")
proses = st.sidebar.button("Hitung Eskalasi Keputusan", type="primary", use_container_width=True)

if proses:
    # Memasukkan nilai ke mesin fuzzy
    simulasi.input['agresi'] = val_agresi
    simulasi.input['jarak'] = val_jarak
    simulasi.input['sipil'] = val_sipil
    
    # Eksekusi Perhitungan
    simulasi.compute()
    hasil_skor = simulasi.output['tindakan']
    
    
    # 5. TAMPILAN HASIL ANALISIS
    
    st.subheader("📊 Hasil Analisis Taktis")
    
    col1, col2 = st.columns(2)
    col1.metric("Skor Tingkat Tindakan", f"{hasil_skor:.1f} / 100")
    
    # Logika Penentuan Status
    if hasil_skor < 40:
        status = "Negotiation"
        warna = "success"
        pesan = "Situasi terkendali. Lakukan negosiasi verbal atau borgol tersangka dengan tangan kosong."
    elif hasil_skor < 70:
        status = "Less Lethal"
        warna = "warning"
        pesan = "Ancaman menengah. Gunakan Taser atau Pepper Spray untuk melumpuhkan tanpa resiko fatal."
    else:
        status = "Lethal Force"
        warna = "error"
        pesan = "ANCAMAN TINGGI! Petugas diizinkan mencabut dan menggunakan senjata api. Pastikan arah tembakan aman dari warga sipil."
        
    col2.metric("Rekomendasi SOP", status)
    
    # Progress Bar berwarna
    st.progress(int(hasil_skor))
    
    # Menampilkan alert/notifikasi sesuai warna
    if warna == "success":
        st.success(f"**Protokol Hijau:** {pesan}")
    elif warna == "warning":
        st.warning(f"**Protokol Kuning:** {pesan}")
    else:
        st.error(f"**Protokol Merah:** {pesan}")
        
else:
    st.info("👈 Silakan atur parameter di panel sebelah kiri dan klik tombol untuk melihat rekomendasi tindakan.")