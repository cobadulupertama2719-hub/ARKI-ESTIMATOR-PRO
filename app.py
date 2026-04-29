
import streamlit as st

# Kode sakti untuk full screen & tanpa atribut Streamlit
hide_st_style = """
            <style>
            /* Menghilangkan Main Menu (tiga garis di kanan atas) */
            #MainMenu {visibility: hidden;}
            
            /* Menghilangkan Header transparan bawaan */
            header {visibility: hidden;}
            
            /* Menghilangkan Footer "Made with Streamlit" */
            footer {visibility: hidden;}
            
            /* Menghilangkan tombol 'Deploy' di versi terbaru */
            .stAppDeployButton {display:none;}

            /* MENGHILANGKAN JARAK PUTIH DI ATAS (Sangat Penting) */
            .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
            }
            
            /* Menghilangkan status bar saat proses running */
            [data-testid="stStatusWidget"] {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# app.py - ARKI ESTIMATOR PRO (MODERN WHITE DESIGN)

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="ARKI ESTIMATOR PRO",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== MODERN CSS ====================
st.markdown("""
<style>
    /* Import Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main background putih */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Header utama */
    .hero-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.15);
    }
    
    /* Sidebar styled modern */
    .sidebar-modern {
        background-color: #f8fafc;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    
    /* Cards untuk metrics */
    .metric-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bfdbfe;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.1);
    }
    
    /* Tabel Modern */
    .modern-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .modern-table th {
        background-color: #1e40af;
        color: white;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 13px;
    }
    .modern-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #e2e8f0;
        color: #1e293b;
        font-size: 13px;
    }
    .modern-table tr:hover td {
        background-color: #f1f5f9;
    }
    
    /* Expander modern */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        color: #1e40af;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, #2563eb, #93c5fd, #2563eb);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    /* Input styling */
    .stNumberInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Title */
    h1, h2, h3 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 12px 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="hero-header">
    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">🏗️ ARKI ESTIMATOR PRO</h1>
    <p style="color: #dbeafe; margin: 8px 0 0 0; font-size: 14px;">Kalkulator Konstruksi Presisi | 20 Komponen Lengkap</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR INPUT DI DASHBOARD UTAMA ====================
st.markdown("### 📐 Input Data Proyek")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**🏠 Dimensi Bangunan**")
    panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5, key="panjang")
    lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5, key="lebar")
    tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1, key="tinggi")
    lantai = st.select_slider("Jumlah Lantai", options=[1, 2, 3, 4, 5], value=1, key="lantai")

with col2:
    st.markdown("**🛏️ Ruangan**")
    kamar = st.number_input("Kamar Tidur", min_value=0, max_value=10, value=3, step=1, key="kamar")
    km = st.number_input("Kamar Mandi", min_value=0, max_value=5, value=2, step=1, key="km")
    ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1, step=1, key="ruang_tamu")
    dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1, step=1, key="dapur")

with col3:
    st.markdown("**🔧 Material & Spek**")
    jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], 
                               format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton", key="atap")
    rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"],
                                format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu", key="rangka")
    jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"],
                               format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan", key="bata")
    ukuran_besi = st.selectbox("Ukuran Besi", [10, 13, 16], format_func=lambda x: f"Ø{x} mm", key="besi")

with col4:
    st.markdown("**👷 Tenaga & Opsional**")
    upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000, key="upah_tukang")
    upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000, key="upah_kenek")
    garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1, key="garasi")
    kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1, key="kanopi")
    pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1, key="pagar")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ==================== FUNGSI PERHITUNGAN ====================

def hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi):
    if lantai == 1:
        kp = math.ceil(panjang / 5.5) + 1
        kl = math.ceil(lebar / 5.5) + 1
        jumlah_titik = kp * kl
        ukuran = 0.5
        tebal = 0.2
        jarak = "5-6 meter (penghematan)"
    elif lantai == 2:
        kp = math.floor(panjang / 3) + 1
        kl = math.floor(lebar / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.7
        tebal = 0.25
        jarak = "3 meter (wajib)"
    else:
        kp = math.floor(panjang / 3) + 1
        kl = math.floor(lebar / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.9
        tebal = 0.3
        jarak = "3 meter"
    
    volume_per_titik = ukuran * ukuran * tebal
    volume_total = jumlah_titik * volume_per_titik
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    panjang_besi_per_titik = (ukuran * 4) * 10
    berat_besi = (panjang_besi_per_titik * jumlah_titik) * berat_per_meter
    batang_besi = math.ceil((panjang_besi_per_titik * jumlah_titik) / 12)
    
    return {
        'jumlah_titik': jumlah_titik, 'jarak': jarak,
        'ukuran_cm': ukuran * 100, 'tebal_cm': tebal * 100,
        'volume_m3': round(volume_total, 2),
        'semen_sak': math.ceil(volume_total * 8),
        'pasir_m3': round(volume_total * 0.65, 2),
        'split_m3': round(volume_total * 0.85, 2),
        'besi_kg': round(berat_besi, 1),
        'besi_batang': batang_besi
    }


def get_layout(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi):
    layout = []
    y = 0.5
    
    if kamar > 0:
        lebar_kt = (panjang - 1) / kamar if kamar > 0 else 0
        for i in range(1, kamar + 1):
            layout.append({'nama': f'KT {i}', 'x': 0.5 + (i-1)*lebar_kt, 'y': y, 'w': lebar_kt, 'h': 3})
    
    y += 3.2
    if ruang_tamu > 0:
        layout.append({'nama': 'Ruang Tamu', 'x': 0.5, 'y': y, 'w': panjang/2, 'h': 3})
    if dapur > 0:
        layout.append({'nama': 'Dapur', 'x': panjang/2 + 0.5, 'y': y, 'w': panjang/2 - 1, 'h': 3})
    
    y += 3.2
    for i in range(1, km + 1):
        layout.append({'nama': f'KM {i}', 'x': 0.5 + (i-1)*2.5, 'y': y, 'w': 2, 'h': 2})
    
    if garasi > 0:
        layout.append({'nama': 'Garasi', 'x': panjang - 3.5, 'y': y, 'w': 3, 'h': 2.5})
    
    return layout


def hitung_dinding_presisi(layout, tinggi):
    sisi_dihitung = set()
    total_luas = 0
    jumlah_pintu = 0
    jumlah_jendela = 0
    
    for r in layout:
        kiri = r['x']; kanan = r['x'] + r['w']; atas = r['y']; bawah = r['y'] + r['h']
        
        sisi_kiri = f"kiri,{kiri},{atas},{bawah}"
        if sisi_kiri not in sisi_dihitung:
            total_luas += r['h'] * tinggi
            sisi_dihitung.add(sisi_kiri)
        
        sisi_kanan = f"kanan,{kanan},{atas},{bawah}"
        if sisi_kanan not in sisi_dihitung:
            total_luas += r['h'] * tinggi
            sisi_dihitung.add(sisi_kanan)
        
        sisi_atas = f"atas,{atas},{kiri},{kanan}"
        if sisi_atas not in sisi_dihitung:
            total_luas += r['w'] * tinggi
            sisi_dihitung.add(sisi_atas)
        
        sisi_bawah = f"bawah,{bawah},{kiri},{kanan}"
        if sisi_bawah not in sisi_dihitung:
            total_luas += r['w'] * tinggi
            sisi_dihitung.add(sisi_bawah)
        
        jumlah_pintu += 1
        if "KM" not in r['nama'] and "Garasi" not in r['nama']:
            jumlah_jendela += 1
    
    luas_pintu = jumlah_pintu * (0.9 * 2.1)
    luas_jendela = jumlah_jendela * (1.2 * 1.0)
    luas_bersih = total_luas - luas_pintu - luas_jendela
    
    return {
        'luas_kotor': round(total_luas, 2), 'luas_pintu': round(luas_pintu, 2),
        'luas_jendela': round(luas_jendela, 2), 'luas_bersih': round(luas_bersih, 2),
        'jumlah_pintu': jumlah_pintu, 'jumlah_jendela': jumlah_jendela,
        'bata': math.ceil(luas_bersih * 70),
        'semen_pasang': math.ceil(luas_bersih * 0.3),
        'pasir_pasang': round(luas_bersih * 0.04, 2),
        'semen_plester': math.ceil(luas_bersih * 2 * 0.2),
        'pasir_plester': round(luas_bersih * 2 * 0.025, 2),
        'acian': math.ceil(luas_bersih * 2 * 0.15)
    }


# ==================== MAIN PERHITUNGAN ====================
layout = get_layout(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi)
keliling = 2 * (panjang + lebar)
luas_bangunan = panjang * lebar
luas_total = luas_bangunan * lantai

# KOMPONEN 1: PONDASI
vol_pondasi = keliling * 0.6 * 0.8
komponen_pondasi = {
    'volume': round(vol_pondasi, 2),
    'batu_belah': round(vol_pondasi * 1.2, 2),
    'semen': math.ceil(vol_pondasi * 4.5),
    'pasir': round(vol_pondasi * 0.55, 2)
}

# KOMPONEN 2: SLOOF
vol_sloof = keliling * 0.2 * 0.25
komponen_sloof = {
    'volume': round(vol_sloof, 2),
    'semen': math.ceil(vol_sloof * 8),
    'pasir': round(vol_sloof * 0.65, 2),
    'split': round(vol_sloof * 0.85, 2),
    'besi_kg': round(vol_sloof * 120, 1)
}

# KOMPONEN 3: RING BALOK
vol_ring = keliling * 0.15 * 0.2
komponen_ring = {
    'volume': round(vol_ring, 2),
    'semen': math.ceil(vol_ring * 8),
    'pasir': round(vol_ring * 0.65, 2),
    'split': round(vol_ring * 0.85, 2),
    'besi_kg': round(vol_ring * 120, 1)
}

# KOMPONEN 4: TOTAL STRUKTUR
faktor = 1.3 if (lantai > 1 or jenis_atap != 'metal') else 1
total_beton = (vol_sloof + vol_ring) * faktor
komponen_struktur = {
    'beton': round(total_beton, 2),
    'semen': math.ceil(total_beton * 8),
    'pasir': round(total_beton * 0.65, 2),
    'split': round(total_beton * 0.85, 2),
    'besi_kg': round(total_beton * 120, 1),
    'besi_batang': math.ceil((total_beton * 120) / (12 * (13*13/162))) if total_beton > 0 else 0
}

# KOMPONEN 5: BEKISTING
luas_bekisting = (vol_sloof * 8) + (vol_ring * 6)
komponen_bekisting = {
    'triplek': math.ceil(luas_bekisting * 0.35),
    'kaso': math.ceil(luas_bekisting * 2.5),
    'paku': round(luas_bekisting * 0.2, 1)
}

# KOMPONEN 6: CAKAR AYAM
cakar = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)

# KOMPONEN 7: DINDING
dinding = hitung_dinding_presisi(layout, tinggi)

# KOMPONEN 8: ATAP
luas_atap = luas_bangunan * 1.3
genteng_per_m2 = {'metal': 16, 'tanah': 28, 'beton': 10}
genteng = math.ceil(luas_atap * genteng_per_m2[jenis_atap])

# KOMPONEN 9: RANGKA ATAP
if rangka_atap == 'baja':
    komponen_rangka = {
        'jenis': 'Baja Ringan',
        'kanal_c': math.ceil(luas_atap * 4.5) if luas_atap > 0 else 0,
        'reng': math.ceil(luas_atap * 2.5) if luas_atap > 0 else 0,
        'sekrup': math.ceil(luas_atap * 12) if luas_atap > 0 else 0
    }
else:
    komponen_rangka = {
        'jenis': 'Kayu',
        'kuda2': math.ceil(panjang / 1.5) * 4 if panjang > 0 else 0,
        'gording': math.ceil(panjang * 3) if panjang > 0 else 0,
        'reng': math.ceil(luas_atap * 1.5) if luas_atap > 0 else 0
    }

# KOMPONEN 10: PLAFON
komponen_plafon = {
    'gypsum': math.ceil(luas_bangunan * 0.35) if luas_bangunan > 0 else 0,
    'hollow': math.ceil(luas_bangunan * 0.8) if luas_bangunan > 0 else 0,
    'list': math.ceil(keliling * 1.2) if keliling > 0 else 0
}

# KOMPONEN 11: KERAMIK
komponen_keramik = {
    'lantai': math.ceil(luas_bangunan * 1.05) if luas_bangunan > 0 else 0,
    'dinding_km': km * 6,
    'semen': math.ceil((luas_bangunan + km*6) * 0.3) if luas_bangunan > 0 else 0,
    'pasir': round((luas_bangunan + km*6) * 0.03, 2) if luas_bangunan > 0 else 0
}

# KOMPONEN 12: LISTRIK
titik_lampu = len(layout) + 3
komponen_listrik = {
    'lampu': titik_lampu,
    'saklar': math.ceil(titik_lampu * 0.7),
    'kabel': titik_lampu * 8,
    'mcb': 6 if lantai >= 2 else 4
}

# KOMPONEN 13: KAMAR MANDI
komponen_km = {'closet': km, 'pipa': km * 8, 'wastafel': km}

# KOMPONEN 14: DAPUR
komponen_dapur = {'kitchen_set': 1 if dapur > 0 else 0}

# KOMPONEN 15: CAT
komponen_cat = {
    'tembok': math.ceil(dinding['luas_bersih'] * 0.12) if dinding['luas_bersih'] > 0 else 0,
    'plafon': math.ceil(luas_bangunan * 0.1) if luas_bangunan > 0 else 0,
    'total': math.ceil((dinding['luas_bersih'] * 0.12) + (luas_bangunan * 0.1)) if dinding['luas_bersih'] > 0 else 0
}

# KOMPONEN 16: TENAGA KERJA
tukang = max(2, math.ceil(luas_total / 25)) if luas_total > 0 else 2
kenek = math.ceil(tukang * 1.2) if luas_total > 0 else 2
hari = max(25, math.ceil(luas_total / 3)) if luas_total > 0 else 25
komponen_tenaga = {
    'tukang': tukang,
    'kenek': kenek,
    'hari': hari,
    'biaya': (tukang * upah_tukang + kenek * upah_kenek) * hari if luas_total > 0 else 0
}

# KOMPONEN 17: PINTU
komponen_pintu = {'jumlah': dinding['jumlah_pintu'], 'biaya': dinding['jumlah_pintu'] * 500000}

# KOMPONEN 18: JENDELA
komponen_jendela = {'jumlah': dinding['jumlah_jendela'], 'biaya': dinding['jumlah_jendela'] * 300000}

# KOMPONEN 19: OPSIONAL - KANOPI
komponen_kanopi = {'luas': kanopi, 'biaya': kanopi * 350000}

# KOMPONEN 20: OPSIONAL - PAGAR
komponen_pagar = {'panjang': pagar, 'biaya': pagar * 850000}

# TOTAL REKAP
total_semen = (komponen_pondasi['semen'] + komponen_struktur['semen'] + 
               cakar['semen_sak'] + dinding['semen_pasang'] + 
               dinding['semen_plester'] + komponen_keramik['semen'])
total_pasir = (komponen_pondasi['pasir'] + komponen_struktur['pasir'] + 
               cakar['pasir_m3'] + dinding['pasir_pasang'] + 
               dinding['pasir_plester'] + komponen_keramik['pasir'])
total_split = komponen_struktur['split'] + cakar['split_m3']
total_besi = komponen_struktur['besi_kg'] + cakar['besi_kg']

# TOTAL BIAYA
harga = {
    'semen': 65000, 'pasir': 300000, 'split': 320000, 'bata': 800, 'besi': 15000,
    'triplek': 180000, 'kaso': 25000, 'paku': 18000, 'genteng_metal': 25000,
    'genteng_tanah': 5000, 'genteng_beton': 12000, 'keramik': 90000, 'batu_belah': 250000,
    'gypsum': 45000, 'hollow': 35000, 'list': 8000, 'kabel': 15000, 'saklar': 25000,
    'lampu': 45000, 'mcb': 75000, 'pintu': 500000, 'closet': 800000, 'pipa': 50000,
    'wastafel': 300000, 'cat': 35000, 'kitchen_set': 3000000, 'kanopi': 350000, 'pagar': 850000
}

total_biaya = (total_semen * harga['semen']) + \
              (total_pasir * harga['pasir']) + \
              (total_split * harga['split']) + \
              (komponen_pondasi['batu_belah'] * harga['batu_belah']) + \
              (total_besi * harga['besi']) + \
              (komponen_bekisting['triplek'] * harga['triplek']) + \
              (komponen_bekisting['kaso'] * harga['kaso']) + \
              (komponen_bekisting['paku'] * harga['paku']) + \
              (dinding['bata'] * harga['bata']) + \
              (genteng * harga[f'genteng_{jenis_atap}']) + \
              ((komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik']) + \
              (komponen_plafon['gypsum'] * harga['gypsum']) + \
              (komponen_plafon['hollow'] * harga['hollow']) + \
              (komponen_plafon['list'] * harga['list']) + \
              (komponen_listrik['lampu'] * harga['lampu']) + \
              (komponen_listrik['saklar'] * harga['saklar']) + \
              (komponen_listrik['kabel'] * harga['kabel']) + \
              (komponen_listrik['mcb'] * harga['mcb']) + \
              (dinding['jumlah_pintu'] * harga['pintu']) + \
              (km * harga['closet']) + (km*8 * harga['pipa']) + (km * harga['wastafel']) + \
              (komponen_cat['total'] * harga['cat']) + \
              (komponen_dapur['kitchen_set'] * harga['kitchen_set']) + \
              (kanopi * harga['kanopi']) + (pagar * harga['pagar']) + \
              komponen_tenaga['biaya']


# ==================== TAMPILAN METRIK ====================
st.markdown("### 📊 Ringkasan Proyek")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#475569; font-size:13px; margin:0;">🏠 Luas Bangunan</p>
        <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">{luas_bangunan} m²</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#475569; font-size:13px; margin:0;">🦶 Cakar Ayam</p>
        <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">{cakar['jumlah_titik']} titik</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#475569; font-size:13px; margin:0;">📅 Estimasi Waktu</p>
        <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">{hari} hari</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#475569; font-size:13px; margin:0;">💰 Total RAB</p>
        <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">Rp {total_biaya:,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ==================== TABEL 20 KOMPONEN ====================
st.markdown("### 📋 Rincian 20 Komponen")

# Membuat data untuk tabel 20 komponen
komponen_data = []

# 1. Pondasi Batu Kali
komponen_data.append({
    "No": 1, "Komponen": "Pondasi Batu Kali", 
    "Volume/Satuan": f"{komponen_pondasi['volume']} m³",
    "Detail Material": f"Batu: {komponen_pondasi['batu_belah']} m³, Semen: {komponen_pondasi['semen']} sak, Pasir: {komponen_pondasi['pasir']} m³",
    "Estimasi Biaya": f"Rp {komponen_pondasi['semen']*65000 + komponen_pondasi['batu_belah']*250000:,.0f}"
})

# 2. Sloof
komponen_data.append({
    "No": 2, "Komponen": "Sloof (20x25 cm)", 
    "Volume/Satuan": f"{komponen_sloof['volume']} m³",
    "Detail Material": f"Semen: {komponen_sloof['semen']} sak, Pasir: {komponen_sloof['pasir']} m³, Split: {komponen_sloof['split']} m³, Besi: {komponen_sloof['besi_kg']} kg",
    "Estimasi Biaya": f"Rp {komponen_sloof['semen']*65000 + komponen_sloof['besi_kg']*15000:,.0f}"
})

# 3. Ring Balok
komponen_data.append({
    "No": 3, "Komponen": "Ring Balok (15x20 cm)", 
    "Volume/Satuan": f"{komponen_ring['volume']} m³",
    "Detail Material": f"Semen: {komponen_ring['semen']} sak, Pasir: {komponen_ring['pasir']} m³, Split: {komponen_ring['split']} m³, Besi: {komponen_ring['besi_kg']} kg",
    "Estimasi Biaya": f"Rp {komponen_ring['semen']*65000 + komponen_ring['besi_kg']*15000:,.0f}"
})

# 4. Total Struktur
komponen_data.append({
    "No": 4, "Komponen": "Total Struktur Beton", 
    "Volume/Satuan": f"{komponen_struktur['beton']} m³",
    "Detail Material": f"Semen: {komponen_struktur['semen']} sak, Besi: {komponen_struktur['besi_kg']} kg ({komponen_struktur['besi_batang']} batang)",
    "Estimasi Biaya": f"Rp {komponen_struktur['beton']*1500000:,.0f}"
})

# 5. Bekisting
komponen_data.append({
    "No": 5, "Komponen": "Bekisting", 
    "Volume/Satuan": f"{luas_bekisting:.1f} m²",
    "Detail Material": f"Triplek: {komponen_bekisting['triplek']} lbr, Kaso: {komponen_bekisting['kaso']} btg, Paku: {komponen_bekisting['paku']} kg",
    "Estimasi Biaya": f"Rp {komponen_bekisting['triplek']*180000:,.0f}"
})

# 6. Cakar Ayam
komponen_data.append({
    "No": 6, "Komponen": "Cakar Ayam", 
    "Volume/Satuan": f"{cakar['jumlah_titik']} titik ({cakar['jarak']})",
    "Detail Material": f"Volume: {cakar['volume_m3']} m³, Semen: {cakar['semen_sak']} sak, Besi: {cakar['besi_kg']} kg",
    "Estimasi Biaya": f"Rp {cakar['semen_sak']*65000 + cakar['besi_kg']*15000:,.0f}"
})

# 7. Dinding Bata
komponen_data.append({
    "No": 7, "Komponen": "Dinding Bata", 
    "Volume/Satuan": f"{dinding['luas_bersih']} m²",
    "Detail Material": f"Bata: {dinding['bata']:,} pcs, Semen: {dinding['semen_pasang']} sak",
    "Estimasi Biaya": f"Rp {dinding['bata']*800:,.0f}"
})

# 8. Plesteran & Acian
komponen_data.append({
    "No": 8, "Komponen": "Plesteran + Acian", 
    "Volume/Satuan": f"{dinding['luas_bersih']*2:.0f} m²",
    "Detail Material": f"Semen Plester: {dinding['semen_plester']} sak, Semen Acian: {dinding['acian']} sak",
    "Estimasi Biaya": f"Rp {(dinding['semen_plester'] + dinding['acian'])*65000:,.0f}"
})

# 9. Pintu
komponen_data.append({
    "No": 9, "Komponen": "Pintu", 
    "Volume/Satuan": f"{dinding['jumlah_pintu']} unit",
    "Detail Material": "Pintu standar + kusen",
    "Estimasi Biaya": f"Rp {dinding['jumlah_pintu']*500000:,.0f}"
})

# 10. Jendela
komponen_data.append({
    "No": 10, "Komponen": "Jendela", 
    "Volume/Satuan": f"{dinding['jumlah_jendela']} unit",
    "Detail Material": "Jendela standar + kusen",
    "Estimasi Biaya": f"Rp {dinding['jumlah_jendela']*300000:,.0f}"
})

# 11. Rangka Atap
komponen_data.append({
    "No": 11, "Komponen": f"Rangka Atap ({komponen_rangka['jenis']})", 
    "Volume/Satuan": f"{luas_atap} m²",
    "Detail Material": f"Luas atap: {luas_atap} m²",
    "Estimasi Biaya": f"Rp {luas_atap*150000:,.0f}"
})

# 12. Genteng
komponen_data.append({
    "No": 12, "Komponen": f"Genteng {jenis_atap.title()}", 
    "Volume/Satuan": f"{genteng} pcs",
    "Detail Material": f"Kebutuhan genteng untuk luas atap {luas_atap} m²",
    "Estimasi Biaya": f"Rp {genteng*25000:,.0f}"
})

# 13. Plafon
komponen_data.append({
    "No": 13, "Komponen": "Plafon Gypsum", 
    "Volume/Satuan": f"{komponen_plafon['gypsum']} lbr",
    "Detail Material": f"Hollow: {komponen_plafon['hollow']} btg, List: {komponen_plafon['list']} m",
    "Estimasi Biaya": f"Rp {komponen_plafon['gypsum']*45000:,.0f}"
})

# 14. Keramik
komponen_data.append({
    "No": 14, "Komponen": "Keramik Lantai", 
    "Volume/Satuan": f"{komponen_keramik['lantai']} m²",
    "Detail Material": f"Keramik lantai + dinding KM: {komponen_keramik['dinding_km']} m²",
    "Estimasi Biaya": f"Rp {komponen_keramik['lantai']*90000:,.0f}"
})

# 15. Cat
komponen_data.append({
    "No": 15, "Komponen": "Cat Dinding & Plafon", 
    "Volume/Satuan": f"{komponen_cat['total']} liter",
    "Detail Material": f"Cat tembok: {komponen_cat['tembok']} ltr, Cat plafon: {komponen_cat['plafon']} ltr",
    "Estimasi Biaya": f"Rp {komponen_cat['total']*35000:,.0f}"
})

# 16. Instalasi Listrik
komponen_data.append({
    "No": 16, "Komponen": "Instalasi Listrik", 
    "Volume/Satuan": f"{komponen_listrik['lampu']} titik",
    "Detail Material": f"Saklar: {komponen_listrik['saklar']}, Kabel: {komponen_listrik['kabel']} m, MCB: {komponen_listrik['mcb']} A",
    "Estimasi Biaya": f"Rp {(komponen_listrik['lampu']*45000) + (komponen_listrik['saklar']*25000):,.0f}"
})

# 17. Sanitasi
komponen_data.append({
    "No": 17, "Komponen": "Sanitasi (KM)", 
    "Volume/Satuan": f"{km} unit",
    "Detail Material": f"Closet: {komponen_km['closet']}, Pipa: {komponen_km['pipa']} m, Wastafel: {komponen_km['wastafel']}",
    "Estimasi Biaya": f"Rp {(km*800000) + (km*8*50000):,.0f}"
})

# 18. Dapur
komponen_data.append({
    "No": 18, "Komponen": "Kitchen Set", 
    "Volume/Satuan": "1 set" if dapur > 0 else "-",
    "Detail Material": "Kitchen set standar + kompor",
    "Estimasi Biaya": f"Rp {3000000 if dapur > 0 else 0:,.0f}"
})

# 19. Kanopi
komponen_data.append({
    "No": 19, "Komponen": "Kanopi", 
    "Volume/Satuan": f"{kanopi} m²",
    "Detail Material": "Kanopi baja ringan + atap polycarbonate",
    "Estimasi Biaya": f"Rp {kanopi*350000:,.0f}"
})

# 20. Pagar
komponen_data.append({
    "No": 20, "Komponen": "Pagar", 
    "Volume/Satuan": f"{pagar} m",
    "Detail Material": "Pagar besi minimalis + cat",
    "Estimasi Biaya": f"Rp {pagar*850000:,.0f}"
})

# Menampilkan tabel
df_komponen = pd.DataFrame(komponen_data)
st.dataframe(
    df_komponen,
    use_container_width=True,
    hide_index=True,
    column_config={
        "No": st.column_config.NumberColumn("No", width="small"),
        "Komponen": st.column_config.TextColumn("Komponen", width="medium"),
        "Volume/Satuan": st.column_config.TextColumn("Volume / Satuan", width="small"),
        "Detail Material": st.column_config.TextColumn("Detail Material", width="large"),
        "Estimasi Biaya": st.column_config.TextColumn("Estimasi Biaya", width="medium")
    }
)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ==================== TOTAL KESELURUHAN ====================
st.markdown("### 💰 Ringkasan Total Material & Biaya")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Semen", f"{total_semen} sak")
with col2:
    st.metric("Total Pasir", f"{total_pasir:.2f} m³")
with col3:
    st.metric("Total Split", f"{total_split:.2f} m³")
with col4:
    st.metric("Total Besi", f"{total_besi:.1f} kg")
with col5:
    st.metric("Tenaga Kerja", f"{tukang} Tukang + {kenek} Kenek")

st.markdown("---")

# Grand Total
st.markdown(f"""
<div style="background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%); border-radius: 16px; padding: 25px; text-align: center; margin-top: 20px;">
    <p style="color: #dbeafe; font-size: 14px; margin: 0;">GRAND TOTAL RENCANA ANGGARAN BIAYA (RAB)</p>
    <h2 style="color: white; margin: 10px 0 0 0; font-size: 42px;">Rp {total_biaya:,.0f}</h2>
    <p style="color: #bfdbfe; margin-top: 10px; font-size: 12px;">*Sudah termasuk material, upah tukang, dan overhead</p>
</div>
""", unsafe_allow_html=True)

# ==================== EXPORT DATA ====================
st.markdown("---")
st.markdown("### 📄 Export Data")

col1, col2 = st.columns(2)

with col1:
    # Export CSV
    csv = df_komponen.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV (20 Komponen)",
        data=csv,
        file_name=f"arki_estimator_20_komponen_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    # Export JSON
    export_json = {
        'timestamp': datetime.now().isoformat(),
        'input_parameter': {
            'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai,
            'kamar': kamar, 'km': km, 'garasi': garasi, 'kanopi': kanopi, 'pagar': pagar
        },
        'total': {
            'total_biaya': total_biaya,
            'total_semen': total_semen,
            'total_pasir': total_pasir,
            'total_split': total_split,
            'total_besi': total_besi,
            'estimasi_hari': hari
        },
        'detail_20_komponen': komponen_data
    }
    json_str = json.dumps(export_json, indent=2, default=str)
    st.download_button(
        label="📥 Download JSON (Lengkap)",
        data=json_str,
        file_name=f"arki_estimator_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px;">
    <hr style="border-color: #e2e8f0;">
    <p style="color: #94a3b8;">🏗️ ARKI ESTIMATOR PRO | 20 Komponen Lengkap | © 2024</p>
    <p style="color: #cbd5e1; font-size: 12px;">*Harga bersifat estimasi, dapat berubah sesuai daerah dan waktu</p>
</div>
""", unsafe_allow_html=True)
