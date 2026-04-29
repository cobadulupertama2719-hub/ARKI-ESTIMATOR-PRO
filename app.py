# app.py - ARKI ESTIMATOR PRO (LOGIC 1 - Streamlit Version)

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json

# Try-catch untuk matplotlib (fallback jika tidak terinstall)
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

st.set_page_config(
    page_title="ARKI ESTIMATOR PRO - LOGIC 1",
    page_icon="🏗️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .total-card {
        background: #1a3a5c;
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        min-width: 120px;
    }
    .success-box {
        background: #22c55e20;
        color: #22c55e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    .total-grid {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #1e293b;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: #22c55e; margin:0;">🏗️ ARKI ESTIMATOR PRO | LOGIC 1</h1>
    <p style="color: #94a3b8; margin:5px 0 0 0;">20 Komponen Lengkap | Perhitungan Presisi | Cakar Ayam 5-6m (1 Lantai)</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR INPUT ====================
with st.sidebar:
    st.markdown("## 📐 INPUT DATA BANGUNAN")
    
    st.markdown("### 🏠 Dimensi Bangunan")
    panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5)
    tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1)
    lantai = st.number_input("Jumlah Lantai", min_value=1, max_value=5, value=1, step=1)
    
    st.markdown("### 🛏️ Jumlah Ruangan")
    col1, col2 = st.columns(2)
    with col1:
        kamar = st.number_input("Kamar Tidur", min_value=1, max_value=10, value=3, step=1)
        ruang_tamu = st.number_input("Ruang Tamu", min_value=1, max_value=3, value=1, step=1)
    with col2:
        km = st.number_input("Kamar Mandi", min_value=1, max_value=5, value=2, step=1)
        dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1, step=1)
    garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1)
    
    st.markdown("### 🔧 Material & Spek")
    col1, col2 = st.columns(2)
    with col1:
        jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], 
                                   format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton")
        rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"],
                                    format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu")
    with col2:
        jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"],
                                   format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan")
        ukuran_besi = st.selectbox("Ukuran Besi", [10, 13, 16], format_func=lambda x: f"Ø{x} mm")
    
    st.markdown("### 👷 Tenaga Kerja")
    col1, col2 = st.columns(2)
    with col1:
        upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000)
    with col2:
        upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000)
    
    st.markdown("### 🏡 Opsional")
    col1, col2 = st.columns(2)
    with col1:
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1)
    with col2:
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1)


# ==================== FUNGSI PERHITUNGAN ====================

def hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi):
    """LOGIC 1: Cakar Ayam dengan jarak 5-6m untuk 1 lantai, 3m untuk 2+ lantai"""
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
        jarak = "3 meter (wajib untuk keamanan)"
    else:
        kp = math.floor(panjang / 3) + 1
        kl = math.floor(lebar / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.9
        tebal = 0.3
        jarak = "3 meter (bangunan tinggi)"
    
    volume_per_titik = ukuran * ukuran * tebal
    volume_total = jumlah_titik * volume_per_titik
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    panjang_besi_per_titik = (ukuran * 4) * 10
    berat_besi = (panjang_besi_per_titik * jumlah_titik) * berat_per_meter
    batang_besi = math.ceil((panjang_besi_per_titik * jumlah_titik) / 12)
    
    return {
        'jumlah_titik': jumlah_titik,
        'jarak': jarak,
        'ukuran_cm': ukuran * 100,
        'tebal_cm': tebal * 100,
        'volume_m3': round(volume_total, 2),
        'semen_sak': math.ceil(volume_total * 8),
        'pasir_m3': round(volume_total * 0.65, 2),
        'split_m3': round(volume_total * 0.85, 2),
        'besi_kg': round(berat_besi, 1),
        'besi_batang': batang_besi
    }


def get_layout(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi):
    """Layout ruangan otomatis"""
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
    """Dinding presisi - tidak double count"""
    sisi_dihitung = set()
    total_luas = 0
    jumlah_pintu = 0
    jumlah_jendela = 0
    
    for r in layout:
        kiri = r['x']
        kanan = r['x'] + r['w']
        atas = r['y']
        bawah = r['y'] + r['h']
        
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
        'luas_kotor': round(total_luas, 2),
        'luas_pintu': round(luas_pintu, 2),
        'luas_jendela': round(luas_jendela, 2),
        'luas_bersih': round(luas_bersih, 2),
        'jumlah_pintu': jumlah_pintu,
        'jumlah_jendela': jumlah_jendela,
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

# KOMPONEN 1: PONDASI BATU KALI
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

# KOMPONEN 4: TOTAL STRUKTUR (dengan faktor lantai)
faktor = 1.5 if lantai > 1 else 1.0
total_beton = (vol_sloof + vol_ring) * faktor
komponen_struktur = {
    'beton': round(total_beton, 2),
    'semen': math.ceil(total_beton * 8),
    'pasir': round(total_beton * 0.65, 2),
    'split': round(total_beton * 0.85, 2),
    'besi_kg': round(total_beton * 120, 1),
    'besi_batang': math.ceil((keliling * 8) / 12) if keliling > 0 else 0
}

# KOMPONEN 5: BEKISTING
luas_bekisting = (vol_sloof * 8) + (vol_ring * 6)
komponen_bekisting = {
    'triplek': math.ceil(luas_bekisting * 0.35),
    'kaso': math.ceil(luas_bekisting * 2.5),
    'paku': round(luas_bekisting * 0.2, 1)
}

# KOMPONEN 6: CAKAR AYAM (LOGIC 1)
cakar = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)

# KOMPONEN 7: DINDING (PRESISI)
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
komponen_km = {
    'closet': km,
    'pipa': km * 8,
    'wastafel': km
}

# KOMPONEN 14: DAPUR
komponen_dapur = {
    'kitchen_set': 1 if dapur > 0 else 0
}

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
komponen_pintu = {
    'jumlah': dinding['jumlah_pintu'],
    'biaya': dinding['jumlah_pintu'] * 500000
}

# KOMPONEN 18: JENDELA
komponen_jendela = {
    'jumlah': dinding['jumlah_jendela'],
    'biaya': dinding['jumlah_jendela'] * 300000
}

# KOMPONEN 19: KANOPI
komponen_kanopi = {
    'luas': kanopi,
    'biaya': kanopi * 350000
}

# KOMPONEN 20: PAGAR
komponen_pagar = {
    'panjang': pagar,
    'biaya': pagar * 850000
}

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


# ==================== TAMPILAN UTAMA ====================

# Total Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏠 Luas Bangunan", f"{luas_bangunan} m²")
with col2:
    st.metric("🦶 Cakar Ayam", f"{cakar['jumlah_titik']} titik")
with col3:
    st.metric("📅 Estimasi Waktu", f"{hari} hari")
with col4:
    st.metric("💰 Grand Total", f"Rp {total_biaya:,.0f}")

st.markdown("---")

# TABS untuk 20 Komponen
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 20 KOMPONEN", "🏠 DENAH", "📊 RINGKASAN", "💾 EXPORT", "📈 VISUALISASI"])

with tab1:
    st.markdown("## 📋 20 KOMPONEN LENGKAP")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("🪨 1. PONDASI BATU KALI", expanded=True):
            st.metric("Volume", f"{komponen_pondasi['volume']} m³")
            st.metric("Batu Belah", f"{komponen_pondasi['batu_belah']} m³")
            st.metric("Semen", f"{komponen_pondasi['semen']} sak")
            st.metric("Pasir", f"{komponen_pondasi['pasir']} m³")
        
        with st.expander("🏗️ 2. SLOOF"):
            st.metric("Volume", f"{komponen_sloof['volume']} m³")
            st.metric("Semen", f"{komponen_sloof['semen']} sak")
            st.metric("Besi", f"{komponen_sloof['besi_kg']} kg")
        
        with st.expander("🏗️ 3. RING BALOK"):
            st.metric("Volume", f"{komponen_ring['volume']} m³")
            st.metric("Semen", f"{komponen_ring['semen']} sak")
            st.metric("Besi", f"{komponen_ring['besi_kg']} kg")
        
        with st.expander("📦 4. TOTAL STRUKTUR"):
            st.metric("Beton", f"{komponen_struktur['beton']} m³")
            st.metric("Semen", f"{komponen_struktur['semen']} sak")
            st.metric("Besi", f"{komponen_struktur['besi_kg']} kg ({komponen_struktur['besi_batang']} batang)")
        
        with st.expander("🪵 5. BEKISTING"):
            st.metric("Triplek", f"{komponen_bekisting['triplek']} lembar")
            st.metric("Kaso", f"{komponen_bekisting['kaso']} batang")
            st.metric("Paku", f"{komponen_bekisting['paku']} kg")
        
        with st.expander("🦶 6. CAKAR AYAM (LOGIC 1)", expanded=True):
            st.metric("Jumlah Titik", f"{cakar['jumlah_titik']} titik")
            st.caption(f"Jarak: {cakar['jarak']}")
            st.metric("Ukuran", f"{cakar['ukuran_cm']}x{cakar['ukuran_cm']} cm")
            st.metric("Volume", f"{cakar['volume_m3']} m³")
            st.metric("Semen", f"{cakar['semen_sak']} sak")
            st.metric("Besi", f"{cakar['besi_kg']} kg ({cakar['besi_batang']} batang)")
        
        with st.expander("🧱 7. DINDING (PRESISI)"):
            st.metric("Luas Bersih", f"{dinding['luas_bersih']} m²")
            st.metric(f"Pintu ({dinding['jumlah_pintu']} bh)", f"-{dinding['luas_pintu']} m²")
            st.metric(f"Jendela ({dinding['jumlah_jendela']} bh)", f"-{dinding['luas_jendela']} m²")
            st.metric("Bata", f"{dinding['bata']:,} pcs")
            st.metric("Semen Pasang", f"{dinding['semen_pasang']} sak")
            st.metric("Semen Plester", f"{dinding['semen_plester']} sak")
    
    with col2:
        with st.expander("🏠 8. ATAP"):
            st.metric("Luas Atap", f"{luas_atap:.2f} m²")
            st.metric("Genteng", f"{genteng:,} pcs")
        
        with st.expander("🔧 9. RANGKA ATAP"):
            st.markdown(f"**Jenis: {komponen_rangka['jenis']}**")
            if komponen_rangka['jenis'] == 'Baja Ringan':
                st.metric("Kanal C", f"{komponen_rangka['kanal_c']} kg")
                st.metric("Reng", f"{komponen_rangka['reng']} kg")
                st.metric("Sekrup", f"{komponen_rangka['sekrup']:,} pcs")
            else:
                st.metric("Kuda-kuda", f"{komponen_rangka['kuda2']} batang")
                st.metric("Gording", f"{komponen_rangka['gording']} batang")
        
        with st.expander("✨ 10. PLAFON"):
            st.metric("Gypsum", f"{komponen_plafon['gypsum']} lembar")
            st.metric("Hollow", f"{komponen_plafon['hollow']} batang")
            st.metric("List", f"{komponen_plafon['list']} m")
        
        with st.expander("🪨 11. KERAMIK"):
            st.metric("Lantai", f"{komponen_keramik['lantai']} m²")
            st.metric("Dinding KM", f"{komponen_keramik['dinding_km']} m²")
        
        with st.expander("⚡ 12. LISTRIK"):
            st.metric("Lampu", f"{komponen_listrik['lampu']} titik")
            st.metric("Saklar", f"{komponen_listrik['saklar']} titik")
            st.metric("Kabel", f"{komponen_listrik['kabel']} m")
            st.metric("MCB", f"{komponen_listrik['mcb']} A")
        
        with st.expander("🚽 13-20. LAINNYA"):
            st.metric("Closet", f"{komponen_km['closet']} buah")
            st.metric("Kitchen Set", f"{komponen_dapur['kitchen_set']} set")
            st.metric("Cat", f"{komponen_cat['total']} liter")
            st.metric("Kanopi", f"{kanopi} m²")
            st.metric("Pagar", f"{pagar} m")
        
        with st.expander("👷 TENAGA KERJA"):
            st.metric("Tukang", f"{komponen_tenaga['tukang']} orang")
            st.metric("Kenek", f"{komponen_tenaga['kenek']} orang")
            st.metric("Hari Kerja", f"{komponen_tenaga['hari']} hari")
            st.metric("Biaya Upah", f"Rp {komponen_tenaga['biaya']:,.0f}")

with tab2:
    st.markdown("## 🏠 DENAH RUMAH OTOMATIS")
    
    if MATPLOTLIB_AVAILABLE:
        try:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.set_xlim(0, max(panjang + 1, 1))
            ax.set_ylim(0, max(lebar + 1, 1))
            ax.set_facecolor('#f8fafc')
            warna = ['#fcd34d', '#86efac', '#67e8f9', '#fde047', '#c4b5fd', '#fdba74']
            for i, r in enumerate(layout):
                rect = patches.Rectangle((r['x'], r['y']), r['w'], r['h'], 
                                          linewidth=2, edgecolor='#1e293b', 
                                          facecolor=warna[i % len(warna)], alpha=0.8)
                ax.add_patch(rect)
                ax.text(r['x'] + r['w']/2, r['y'] + r['h']/2, r['nama'], 
                        ha='center', va='center', fontsize=10, fontweight='bold')
            ax.set_xlabel("Panjang (m)", fontsize=12)
            ax.set_ylabel("Lebar (m)", fontsize=12)
            ax.set_title(f"Denah Rumah ({panjang}m x {lebar}m) - {kamar} KT + {km} KM", fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)
            
            # Tabel layout
            st.markdown("### 📐 Detail Layout Ruangan")
            layout_df = pd.DataFrame(layout)
            layout_df['x'] = layout_df['x'].round(2)
            layout_df['y'] = layout_df['y'].round(2)
            layout_df['w'] = layout_df['w'].round(2)
            layout_df['h'] = layout_df['h'].round(2)
            st.dataframe(layout_df, use_container_width=True)
            
        except Exception as e:
            st.warning(f"Gagal menampilkan denah: {str(e)}")
    else:
        st.info("📐 Install matplotlib untuk melihat denah: `pip install matplotlib`")
        
        # Tampilkan layout dalam bentuk teks
        st.markdown("### 📐 Layout Ruangan (Text Mode)")
        for r in layout:
            st.write(f"- **{r['nama']}**: {r['w']:.1f}m x {r['h']:.1f}m")

with tab3:
    st.markdown("## 📊 RINGKASAN MATERIAL & BIAYA")
    
    # Total material grid
    st.markdown("### 🧱 TOTAL MATERIAL")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Semen", f"{total_semen} sak", help=f"Pondasi: {komponen_pondasi['semen']} + Struktur: {komponen_struktur['semen']} + Cakar: {cakar['semen_sak']} + Dinding: {dinding['semen_pasang'] + dinding['semen_plester']}")
    with col2:
        st.metric("Total Pasir", f"{total_pasir:.2f} m³")
    with col3:
        st.metric("Total Split", f"{total_split:.2f} m³")
    with col4:
        st.metric("Total Besi", f"{total_besi:.1f} kg")
    with col5:
        st.metric("Total Bata", f"{dinding['bata']:,} pcs")
    
    st.markdown("---")
    
    # Rincian Biaya
    st.markdown("### 💰 RINCIAN BIAYA")
    
    biaya_detail = {
        'Material Pondasi': komponen_pondasi['semen'] * harga['semen'] + komponen_pondasi['batu_belah'] * harga['batu_belah'] + komponen_pondasi['pasir'] * harga['pasir'],
        'Material Struktur': komponen_struktur['semen'] * harga['semen'] + komponen_struktur['pasir'] * harga['pasir'] + komponen_struktur['split'] * harga['split'] + komponen_struktur['besi_kg'] * harga['besi'],
        'Cakar Ayam': cakar['semen_sak'] * harga['semen'] + cakar['pasir_m3'] * harga['pasir'] + cakar['split_m3'] * harga['split'] + cakar['besi_kg'] * harga['besi'],
        'Bekisting': komponen_bekisting['triplek'] * harga['triplek'] + komponen_bekisting['kaso'] * harga['kaso'] + komponen_bekisting['paku'] * harga['paku'],
        'Dinding & Plester': dinding['bata'] * harga['bata'] + dinding['semen_pasang'] * harga['semen'] + dinding['semen_plester'] * harga['semen'] + dinding['pasir_pasang'] * harga['pasir'] + dinding['pasir_plester'] * harga['pasir'],
        'Atap & Rangka': genteng * harga[f'genteng_{jenis_atap}'],
        'Plafon': komponen_plafon['gypsum'] * harga['gypsum'] + komponen_plafon['hollow'] * harga['hollow'] + komponen_plafon['list'] * harga['list'],
        'Keramik': (komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik'],
        'Listrik': komponen_listrik['lampu'] * harga['lampu'] + komponen_listrik['saklar'] * harga['saklar'] + komponen_listrik['kabel'] * harga['kabel'] + komponen_listrik['mcb'] * harga['mcb'],
        'Pintu & Jendela': dinding['jumlah_pintu'] * harga['pintu'] + dinding['jumlah_jendela'] * 300000,
        'Sanitasi': km * harga['closet'] + km*8 * harga['pipa'] + km * harga['wastafel'],
        'Cat': komponen_cat['total'] * harga['cat'],
        'Kitchen Set': komponen_dapur['kitchen_set'] * harga['kitchen_set'],
        'Kanopi & Pagar': kanopi * harga['kanopi'] + pagar * harga['pagar'],
        'Tenaga Kerja': komponen_tenaga['biaya']
    }
    
    df_biaya = pd.DataFrame(list(biaya_detail.items()), columns=['Komponen', 'Biaya'])
    df_biaya['Biaya'] = df_biaya['Biaya'].apply(lambda x: f"Rp {x:,.0f}")
    st.dataframe(df_biaya, use_container_width=True)
    
    st.markdown("---")
    
    # Grand Total
    st.markdown(f"""
    <div class="success-box">
        <h2>💰 GRAND TOTAL RAB</h2>
        <h1 style="font-size: 48px;">Rp {total_biaya:,.0f}</h1>
        <p>Termasuk Material + Bekisting + Upah Tukang + Kenek</p>
        <p style="font-size: 12px;">*Harga bersifat estimasi, dapat berubah sesuai daerah dan waktu</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 💾 EXPORT DATA")
    
    # Data untuk export
    export_data = {
        'Parameter': [
            'Tanggal', 'Panjang (m)', 'Lebar (m)', 'Tinggi Dinding (m)', 'Jumlah Lantai',
            'Luas Bangunan (m²)', 'Kamar Tidur', 'Kamar Mandi', 'Ruang Tamu', 'Dapur', 'Garasi',
            'Jenis Atap', 'Rangka Atap', 'Ukuran Besi (mm)', 'Cakar Ayam (titik)', 'Jarak Cakar',
            'Total Semen (sak)', 'Total Pasir (m³)', 'Total Split (m³)', 'Total Besi (kg)',
            'Estimasi Hari', 'Upah Tukang/Hari', 'Upah Kenek/Hari', 'Total Biaya'
        ],
        'Nilai': [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), panjang, lebar, tinggi, lantai,
            luas_bangunan, kamar, km, ruang_tamu, dapur, garasi,
            jenis_atap, rangka_atap, ukuran_besi, cakar['jumlah_titik'], cakar['jarak'],
            total_semen, f"{total_pasir:.2f}", f"{total_split:.2f}", f"{total_besi:.1f}",
            hari, f"Rp {upah_tukang:,.0f}", f"Rp {upah_kenek:,.0f}", f"Rp {total_biaya:,.0f}"
        ]
    }
    
    df_export = pd.DataFrame(export_data)
    st.dataframe(df_export, use_container_width=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"arki_estimator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    
    with col2:
        # Export lengkap 20 komponen ke JSON
        full_data = {
            'input': {
                'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai,
                'kamar': kamar, 'km': km, 'ruang_tamu': ruang_tamu, 'dapur': dapur, 'garasi': garasi,
                'jenis_atap': jenis_atap, 'rangka_atap': rangka_atap, 'ukuran_besi': ukuran_besi,
                'upah_tukang': upah_tukang, 'upah_kenek': upah_kenek, 'kanopi': kanopi, 'pagar': pagar
            },
            'komponen': {
                'pondasi': komponen_pondasi,
                'sloof': komponen_sloof,
                'ring_balok': komponen_ring,
                'total_struktur': komponen_struktur,
                'bekisting': komponen_bekisting,
                'cakar_ayam': cakar,
                'dinding': dinding,
                'atap': {'luas': luas_atap, 'genteng': genteng},
                'rangka_atap': komponen_rangka,
                'plafon': komponen_plafon,
                'keramik': komponen_keramik,
                'listrik': komponen_listrik,
                'kamar_mandi': komponen_km,
                'dapur': komponen_dapur,
                'cat': komponen_cat,
                'tenaga_kerja': komponen_tenaga
            },
            'total': {
                'semen': total_semen,
                'pasir_m3': total_pasir,
                'split_m3': total_split,
                'besi_kg': total_besi,
                'total_biaya': total_biaya
            }
        }
        
        json_str = json.dumps(full_data, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON (Lengkap)",
            data=json_str,
            file_name=f"arki_estimator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )
    
    st.markdown("---")
    st.markdown("### 📋 Preview 20 Komponen")
    st.json(full_data, expanded=False)

with tab5:
    st.markdown("## 📈 VISUALISASI DATA")
    
    if MATPLOTLIB_AVAILABLE:
        try:
            # Chart 1: Breakdown Biaya
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            categories = list(biaya_detail.keys())
            values = [komponen_pondasi['semen'] * harga['semen'] + komponen_pondasi['batu_belah'] * harga['batu_belah'] + komponen_pondasi['pasir'] * harga['pasir'],
                      komponen_struktur['semen'] * harga['semen'] + komponen_struktur['pasir'] * harga['pasir'] + komponen_struktur['split'] * harga['split'] + komponen_struktur['besi_kg'] * harga['besi'],
                      cakar['semen_sak'] * harga['semen'] + cakar['pasir_m3'] * harga['pasir'] + cakar['split_m3'] * harga['split'] + cakar['besi_kg'] * harga['besi'],
                      komponen_bekisting['triplek'] * harga['triplek'] + komponen_bekisting['kaso'] * harga['kaso'] + komponen_bekisting['paku'] * harga['paku'],
                      dinding['bata'] * harga['bata'] + dinding['semen_pasang'] * harga['semen'] + dinding['semen_plester'] * harga['semen'] + dinding['pasir_pasang'] * harga['pasir'] + dinding['pasir_plester'] * harga['pasir'],
                      genteng * harga[f'genteng_{jenis_atap}'],
                      komponen_plafon['gypsum'] * harga['gypsum'] + komponen_plafon['hollow'] * harga['hollow'] + komponen_plafon['list'] * harga['list'],
                      (komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik'],
                      komponen_listrik['lampu'] * harga['lampu'] + komponen_listrik['saklar'] * harga['saklar'] + komponen_listrik['kabel'] * harga['kabel'] + komponen_listrik['mcb'] * harga['mcb'],
                      komponen_tenaga['biaya']]
            
            bars = ax1.barh(categories, values, color='#22c55e')
            ax1.set_xlabel('Biaya (Rp)', fontsize=12)
            ax1.set_title('Breakdown Biaya per Komponen', fontsize=14, fontweight='bold')
            ax1.tick_params(axis='y', labelsize=9)
            
            # Format x-axis dengan Rupiah
            def format_rupiah(x, p):
                return f'Rp {x/1000000:.1f}M' if x >= 1000000 else f'Rp {x:,.0f}'
            ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
            
            plt.tight_layout()
            st.pyplot(fig1)
            
            # Chart 2: Material Comparison
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            material_labels = ['Semen (sak)', 'Pasir (m³)', 'Split (m³)', 'Besi (kg/10)', 'Bata (rb pcs)']
            material_values = [total_semen, total_pasir, total_split, total_besi/10, dinding['bata']/1000]
            colors2 = ['#ef4444', '#3b82f6', '#f97316', '#8b5cf6', '#10b981']
            ax2.bar(material_labels, material_values, color=colors2, edgecolor='black')
            ax2.set_ylabel('Jumlah', fontsize=12)
            ax2.set_title('Perbandingan Total Material', fontsize=14, fontweight='bold')
            for i, v in enumerate(material_values):
                ax2.text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')
            st.pyplot(fig2)
            
        except Exception as e:
            st.warning(f"Gagal menampilkan chart: {str(e)}")
    else:
        st.info("📊 Install matplotlib untuk melihat visualisasi: `pip install matplotlib`")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 20px;">
    <p>🏗️ ARKI ESTIMATOR PRO | LOGIC 1 | © 2024</p>
    <p style="font-size: 12px;">* Cakar Ayam: Jarak 5-6m untuk 1 lantai (penghematan), jarak 3m untuk 2+ lantai (keamanan)</p>
    <p style="font-size: 12px;">* Harga bersifat estimasi, dapat berubah sesuai daerah dan waktu</p>
</div>
""", unsafe_allow_html=True)
