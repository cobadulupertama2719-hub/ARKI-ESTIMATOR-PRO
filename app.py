# app.py - ARKI ESTIMATOR PRO (MODERN DESIGN - TANPA FPDF)

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
    initial_sidebar_state="expanded"
)

# ==================== MODERN UI CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0f172a; }
    
    .main-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    
    .hero-header {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        padding: 30px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    }

    .component-badge {
        background: #1e293b;
        color: #10b981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #10b981;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR INPUT ====================
with st.sidebar:
    st.markdown("### 🏗️ Parameter Proyek")
    panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5)
    tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1)
    lantai = st.select_slider("Jumlah Lantai", options=[1, 2, 3, 4, 5], value=1)
    
    with st.expander("🛏️ Ruangan & Fasilitas"):
        col1, col2 = st.columns(2)
        with col1:
            kamar = st.number_input("Kamar Tidur", min_value=0, max_value=10, value=3)
            ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1)
        with col2:
            km = st.number_input("Kamar Mandi", min_value=0, max_value=5, value=2)
            dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1)
        garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0)
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0)
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0)

    with st.expander("🛠️ Material & Spek"):
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
    
    with st.expander("👷 Tenaga Kerja"):
        col1, col2 = st.columns(2)
        with col1:
            upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000)
        with col2:
            upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000)


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

# KOMPONEN 19: KANOPI
komponen_kanopi = {'luas': kanopi, 'biaya': kanopi * 350000}

# KOMPONEN 20: PAGAR
komponen_pagar = {'panjang': pagar, 'biaya': pagar * 850000}

# TOTAL REKAP MATERIAL
total_semen = (komponen_pondasi['semen'] + komponen_struktur['semen'] + 
               cakar['semen_sak'] + dinding['semen_pasang'] + 
               dinding['semen_plester'] + komponen_keramik['semen'])
total_pasir = (komponen_pondasi['pasir'] + komponen_struktur['pasir'] + 
               cakar['pasir_m3'] + dinding['pasir_pasang'] + 
               dinding['pasir_plester'] + komponen_keramik['pasir'])
total_split = komponen_struktur['split'] + cakar['split_m3']
total_besi = komponen_struktur['besi_kg'] + cakar['besi_kg']

# TOTAL BIAYA RAB
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


# ==================== MAIN DISPLAY MODERN ====================
st.markdown("""
<div class="hero-header">
    <h1 style="color: white; margin:0; font-size: 28px;">🏗️ ARKI ESTIMATOR PRO</h1>
    <p style="color: #d1fae5; margin:5px 0 0 0;">Kalkulator Konstruksi Presisi - 20 Komponen Lengkap</p>
</div>
""", unsafe_allow_html=True)

# Top Summary Metrics Modern
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#94a3b8; font-size:12px; margin:0;">TOTAL ESTIMASI</p>
        <h3 style="color:#10b981; margin:0;">Rp {total_biaya:,.0f}</h3>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#94a3b8; font-size:12px; margin:0;">LUAS TOTAL</p>
        <h3 style="color:white; margin:0;">{luas_total} m²</h3>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#94a3b8; font-size:12px; margin:0;">WAKTU KERJA</p>
        <h3 style="color:white; margin:0;">{hari} Hari</h3>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#94a3b8; font-size:12px; margin:0;">CAKAR AYAM</p>
        <h3 style="color:white; margin:0;">{cakar['jumlah_titik']} Titik</h3>
    </div>
    """, unsafe_allow_html=True)

# TABS
tabs = st.tabs(["📋 20 KOMPONEN", "💰 TABEL RAB", "📄 EXPORT DATA"])

with tabs[0]:
    st.markdown("### 🛠️ Rincian 20 Komponen Material & Struktur")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.expander("💎 1-5: STRUKTUR UTAMA", expanded=True):
            st.markdown(f"**1. Pondasi Batu Kali** → {komponen_pondasi['volume']} m³ (Semen: {komponen_pondasi['semen']} sak)")
            st.markdown(f"**2. Sloof (20x25)** → {komponen_sloof['volume']} m³ (Besi: {komponen_sloof['besi_kg']} kg)")
            st.markdown(f"**3. Ring Balok** → {komponen_ring['volume']} m³ (Besi: {komponen_ring['besi_kg']} kg)")
            st.markdown(f"**4. Cakar Ayam** → {cakar['jumlah_titik']} Titik, {cakar['jarak']}")
            st.markdown(f"**5. Bekisting** → {komponen_bekisting['triplek']} lbr triplek + {komponen_bekisting['kaso']} batang kaso")

        with st.expander("🧱 6-10: DINDING & BUKAAN"):
            st.markdown(f"**6. Bata {jenis_bata.upper()}** → {dinding['bata']:,} pcs")
            st.markdown(f"**7. Semen Pasang** → {dinding['semen_pasang']} sak")
            st.markdown(f"**8. Semen Plester** → {dinding['semen_plester']} sak")
            st.markdown(f"**9. Pintu** → {dinding['jumlah_pintu']} unit")
            st.markdown(f"**10. Jendela** → {dinding['jumlah_jendela']} unit")

        with st.expander("🏠 11-15: ATAP & FINISHING"):
            st.markdown(f"**11. Rangka Atap {komponen_rangka['jenis']}** → {luas_atap} m²")
            st.markdown(f"**12. Genteng {jenis_atap.upper()}** → {genteng:,} pcs")
            st.markdown(f"**13. Plafon Gypsum** → {komponen_plafon['gypsum']} lembar")
            st.markdown(f"**14. Keramik Lantai** → {komponen_keramik['lantai']} m²")
            st.markdown(f"**15. Cat** → {komponen_cat['total']} liter")
    
    with col_right:
        with st.expander("⚡ 16-20: MEKANIKAL & ELEKTRIKAL"):
            st.markdown(f"**16. Instalasi Listrik** → {komponen_listrik['lampu']} titik lampu")
            st.markdown(f"**17. Kabel** → {komponen_listrik['kabel']} meter")
            st.markdown(f"**18. Sanitasi** → {komponen_km['closet']} closet, {komponen_km['wastafel']} wastafel")
            st.markdown(f"**19. Kanopi** → {kanopi} m²")
            st.markdown(f"**20. Tenaga Kerja** → {komponen_tenaga['tukang']} tukang + {komponen_tenaga['kenek']} kenek")

    st.markdown("---")
    st.markdown("### 📊 Ringkasan Material Utama")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Total Semen", f"{total_semen} sak")
    with col_b:
        st.metric("Total Pasir", f"{total_pasir:.2f} m³")
    with col_c:
        st.metric("Total Split", f"{total_split:.2f} m³")
    with col_d:
        st.metric("Total Besi", f"{total_besi:.1f} kg")

with tabs[1]:
    st.markdown("### 💰 Rencana Anggaran Biaya (RAB)")
    
    rab_data = {
        "No": list(range(1, 21)),
        "Uraian Pekerjaan": [
            "1. Pondasi Batu Kali", "2. Sloof", "3. Ring Balok", "4. Total Struktur", "5. Bekisting",
            "6. Cakar Ayam", "7. Dinding Bata", "8. Plesteran & Acian", "9. Pintu", "10. Jendela",
            "11. Rangka Atap", "12. Genteng", "13. Plafon", "14. Keramik", "15. Cat",
            "16. Listrik", "17. Sanitasi", "18. Dapur", "19. Kanopi & Pagar", "20. Tenaga Kerja"
        ],
        "Volume": [
            f"{komponen_pondasi['volume']} m³", f"{komponen_sloof['volume']} m³", f"{komponen_ring['volume']} m³",
            f"{komponen_struktur['beton']} m³", f"{luas_bekisting:.1f} m²", f"{cakar['jumlah_titik']} titik",
            f"{dinding['bata']} pcs", f"{dinding['luas_bersih']} m²", f"{dinding['jumlah_pintu']} unit",
            f"{dinding['jumlah_jendela']} unit", f"{luas_atap} m²", f"{genteng} pcs",
            f"{komponen_plafon['gypsum']} lbr", f"{komponen_keramik['lantai']} m²", f"{komponen_cat['total']} ltr",
            f"{komponen_listrik['lampu']} titik", f"{km} unit", "1 set", f"{kanopi+pagar} m²", f"{hari} hari"
        ]
    }
    
    df_rab = pd.DataFrame(rab_data)
    st.dataframe(df_rab, use_container_width=True, hide_index=True)
    
    # Hitung total per komponen untuk ditampilkan
    biaya_per_komponen = [
        komponen_pondasi['semen']*65000 + komponen_pondasi['batu_belah']*250000,
        komponen_sloof['semen']*65000 + komponen_sloof['besi_kg']*15000,
        komponen_ring['semen']*65000 + komponen_ring['besi_kg']*15000,
        komponen_struktur['beton']*1500000,
        komponen_bekisting['triplek']*180000,
        cakar['semen_sak']*65000 + cakar['besi_kg']*15000,
        dinding['bata']*800,
        dinding['semen_pasang']*65000 + dinding['semen_plester']*65000,
        dinding['jumlah_pintu']*500000,
        dinding['jumlah_jendela']*300000,
        luas_atap*150000,
        genteng*25000,
        komponen_plafon['gypsum']*45000,
        komponen_keramik['lantai']*90000,
        komponen_cat['total']*35000,
        komponen_listrik['lampu']*45000 + komponen_listrik['saklar']*25000,
        km*800000 + km*8*50000,
        3000000 if dapur>0 else 0,
        kanopi*350000 + pagar*850000,
        komponen_tenaga['biaya']
    ]
    
    st.markdown("---")
    st.markdown("### 💵 Estimasi Biaya per Komponen")
    df_biaya = pd.DataFrame({
        "Komponen": rab_data["Uraian Pekerjaan"],
        "Estimasi Biaya": [f"Rp {x:,.0f}" for x in biaya_per_komponen]
    })
    st.dataframe(df_biaya, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); border-radius: 16px; padding: 25px; text-align: center;">
        <p style="color: white; font-size: 14px; margin: 0;">TOTAL RAB KESELURUHAN</p>
        <h2 style="color: white; margin: 10px 0 0 0; font-size: 42px;">Rp {total_biaya:,.0f}</h2>
        <p style="color: #d1fae5; margin-top: 10px; font-size: 12px;">*Termasuk Material + Upah + Overhead</p>
    </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 📄 Export Data")
    st.info("📊 Export data dalam format CSV atau JSON untuk dokumentasi")
    
    # Data export lengkap
    export_full_data = {
        'timestamp': datetime.now().isoformat(),
        'input_parameter': {
            'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai,
            'kamar': kamar, 'km': km, 'ruang_tamu': ruang_tamu, 'dapur': dapur, 'garasi': garasi,
            'jenis_atap': jenis_atap, 'rangka_atap': rangka_atap, 'jenis_bata': jenis_bata,
            'ukuran_besi': ukuran_besi, 'upah_tukang': upah_tukang, 'upah_kenek': upah_kenek,
            'kanopi': kanopi, 'pagar': pagar
        },
        'hasil_perhitungan': {
            'luas_bangunan': luas_bangunan,
            'luas_total': luas_total,
            'total_semen': total_semen,
            'total_pasir': total_pasir,
            'total_split': total_split,
            'total_besi': total_besi,
            'estimasi_hari': hari,
            'total_biaya': total_biaya
        },
        'detail_20_komponen': {
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
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export CSV
        df_export = pd.DataFrame([{
            'Tanggal': datetime.now().strftime('%Y-%m-%d'),
            'Panjang': panjang, 'Lebar': lebar, 'Tinggi': tinggi, 'Lantai': lantai,
            'Luas_Bangunan': luas_bangunan, 'Total_Semen': total_semen,
            'Total_Pasir': total_pasir, 'Total_Split': total_split,
            'Total_Besi': total_besi, 'Hari_Kerja': hari,
            'Total_Biaya': total_biaya
        }])
        
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"arki_estimator_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Export JSON
        json_str = json.dumps(export_full_data, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON (Lengkap)",
            data=json_str,
            file_name=f"arki_estimator_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### 📋 Preview Data Export (JSON)")
    st.json(export_full_data, expanded=False)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: #64748b;">🏗️ ARKI ESTIMATOR PRO | Full 20 Komponen Logic | © 2024</p>
    <p style="color: #475569; font-size: 12px;">*Harga bersifat estimasi, dapat berubah sesuai daerah dan waktu</p>
</div>
""", unsafe_allow_html=True)
