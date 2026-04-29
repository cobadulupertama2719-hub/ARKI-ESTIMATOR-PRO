# app.py - ARKI ESTIMATOR PRO (Streamlit Version)
# 20 Komponen Lengkap | Tanpa Denah

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="ARKI ESTIMATOR PRO",
    page_icon="🏗️",
    layout="wide"
)

# ==================== CSS CUSTOM ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    .success-box {
        background: #22c55e20;
        color: #22c55e;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 20px;
    }
    .total-card {
        background: #1a3a5c;
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    .komponen-box {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #22c55e;
    }
    .komponen-title {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        color: #1e293b;
    }
    .komponen-detail {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .detail-item {
        background: white;
        padding: 8px 12px;
        border-radius: 8px;
        flex: 1;
        min-width: 100px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .detail-label {
        font-size: 11px;
        color: #64748b;
    }
    .detail-value {
        font-size: 16px;
        font-weight: bold;
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: #22c55e; margin:0;">🏗️ ARKI ESTIMATOR PRO</h1>
    <p style="color: #94a3b8; margin:5px 0 0 0;">20 Komponen Lengkap | Perhitungan Presisi</p>
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR INPUT ====================
with st.sidebar:
    st.markdown("## 📐 INPUT DATA")
    
    st.markdown("### 🏠 Dimensi Bangunan")
    panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5)
    tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1)
    lantai = st.number_input("Jumlah Lantai", min_value=1, max_value=5, value=1, step=1)
    
    st.markdown("### 🛏️ Jumlah Ruangan")
    col1, col2 = st.columns(2)
    with col1:
        kamar = st.number_input("Kamar Tidur", min_value=0, max_value=10, value=3, step=1)
        ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1, step=1)
    with col2:
        km = st.number_input("Kamar Mandi", min_value=0, max_value=5, value=2, step=1)
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

def hitung_cakar_ayam(p, l, lantai, ukuran_besi):
    if lantai == 1:
        kp = math.ceil(p / 5.5) + 1
        kl = math.ceil(l / 5.5) + 1
        jumlah_titik = kp * kl
        ukuran = 0.5
        tebal = 0.2
        jarak = "5-6 meter (penghematan)"
    elif lantai == 2:
        kp = math.floor(p / 3) + 1
        kl = math.floor(l / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.7
        tebal = 0.25
        jarak = "3 meter (wajib)"
    else:
        kp = math.floor(p / 3) + 1
        kl = math.floor(l / 3) + 1
        jumlah_titik = kp * kl
        ukuran = 0.9
        tebal = 0.3
        jarak = "3 meter"
    
    vol_per_titik = ukuran * ukuran * tebal
    vol_total = jumlah_titik * vol_per_titik
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    panjang_besi_per_titik = (ukuran * 4) * 10
    berat_besi = (panjang_besi_per_titik * jumlah_titik) * berat_per_meter
    batang_besi = math.ceil((panjang_besi_per_titik * jumlah_titik) / 12)
    
    return {
        'jumlah_titik': jumlah_titik,
        'jarak': jarak,
        'ukuran_cm': ukuran * 100,
        'tebal_cm': tebal * 100,
        'volume_m3': round(vol_total, 2),
        'semen_sak': math.ceil(vol_total * 8),
        'pasir_m3': round(vol_total * 0.65, 2),
        'split_m3': round(vol_total * 0.85, 2),
        'besi_kg': round(berat_besi, 1),
        'besi_batang': batang_besi
    }


def get_layout(p, l, kamar, km, rt, dapur, garasi):
    layout = []
    y = 0.5
    
    if kamar > 0:
        lebar_kt = (p - 1) / kamar if kamar > 0 else 0
        for i in range(1, kamar + 1):
            layout.append({'nama': f'KT {i}', 'x': 0.5 + (i-1)*lebar_kt, 'y': y, 'w': lebar_kt, 'h': 3})
    
    y += 3.2
    if rt > 0:
        layout.append({'nama': 'Ruang Tamu', 'x': 0.5, 'y': y, 'w': p/2, 'h': 3})
    if dapur > 0:
        layout.append({'nama': 'Dapur', 'x': p/2 + 0.5, 'y': y, 'w': p/2 - 1, 'h': 3})
    
    y += 3.2
    for i in range(1, km + 1):
        layout.append({'nama': f'KM {i}', 'x': 0.5 + (i-1)*2.5, 'y': y, 'w': 2, 'h': 2})
    
    if garasi > 0:
        layout.append({'nama': 'Garasi', 'x': p - 3.5, 'y': y, 'w': 3, 'h': 2.5})
    
    return layout


def hitung_dinding_presisi(layout, tinggi):
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
komponen_atap = {'luas': round(luas_atap, 2), 'genteng': genteng}

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
kenek = math.ceil(tukang * 1.2)
hari = max(25, math.ceil(luas_total / 3)) if luas_total > 0 else 25
biaya_tukang = (tukang * upah_tukang + kenek * upah_kenek) * hari if luas_total > 0 else 0
komponen_tenaga = {'tukang': tukang, 'kenek': kenek, 'hari': hari, 'biaya': biaya_tukang}

# KOMPONEN 17: KANOPI
komponen_kanopi = {
    'ada': kanopi > 0,
    'luas': kanopi,
    'rangka': math.ceil(kanopi * 3.5) if kanopi > 0 else 0,
    'atap': math.ceil(kanopi * 1.05) if kanopi > 0 else 0
}

# KOMPONEN 18: PAGAR
komponen_pagar = {
    'ada': pagar > 0,
    'panjang': pagar,
    'besi_hollow': math.ceil(pagar * 2) if pagar > 0 else 0,
    'cat': round(pagar * 0.1, 1) if pagar > 0 else 0
}

# KOMPONEN 19: INSTALASI AIR
komponen_air = {
    'pipa_air_bersih': (km + (1 if dapur > 0 else 0) + 1) * 5,
    'kran': km + (1 if dapur > 0 else 0) + 1,
    'pipa_air_kotor': km * 6,
    'floor_drain': km,
    'septictank': 1
}

# KOMPONEN 20: PINTU & JENDELA DETAIL
komponen_pintu_jendela = {
    'pintu': dinding['jumlah_pintu'],
    'engsel_pintu': dinding['jumlah_pintu'] * 3,
    'gagang_pintu': dinding['jumlah_pintu'],
    'kunci_pintu': dinding['jumlah_pintu'],
    'kusen_pintu': round(dinding['jumlah_pintu'] * (0.9 + 2.1 + 2.1) * 1.2, 1),
    'jendela': dinding['jumlah_jendela'],
    'engsel_jendela': dinding['jumlah_jendela'] * 2,
    'kaca': round(dinding['jumlah_jendela'] * 1.2, 1)
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

# HARGA MATERIAL
harga = {
    'semen': 65000, 'pasir': 300000, 'split': 320000, 'bata': 800, 'besi': 15000,
    'triplek': 180000, 'kaso': 25000, 'paku': 18000, 'genteng_metal': 25000,
    'genteng_tanah': 5000, 'genteng_beton': 12000, 'keramik': 90000, 'batu_belah': 250000,
    'gypsum': 45000, 'hollow': 35000, 'list': 8000, 'kabel': 15000, 'saklar': 25000,
    'lampu': 45000, 'mcb': 75000, 'pintu': 500000, 'closet': 800000, 'pipa': 50000,
    'wastafel': 300000, 'cat': 35000, 'kitchen_set': 3000000, 'kanopi': 350000, 'pagar': 850000,
    'kran': 150000, 'floor_drain': 100000, 'septictank': 3000000
}

total_biaya = (total_semen * harga['semen']) + (total_pasir * harga['pasir']) + \
              (total_split * harga['split']) + (komponen_pondasi['batu_belah'] * harga['batu_belah']) + \
              (total_besi * harga['besi']) + (komponen_bekisting['triplek'] * harga['triplek']) + \
              (komponen_bekisting['kaso'] * harga['kaso']) + (komponen_bekisting['paku'] * harga['paku']) + \
              (dinding['bata'] * harga['bata']) + (genteng * harga[f'genteng_{jenis_atap}']) + \
              ((komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik']) + \
              (komponen_plafon['gypsum'] * harga['gypsum']) + (komponen_plafon['hollow'] * harga['hollow']) + \
              (komponen_plafon['list'] * harga['list']) + (komponen_listrik['lampu'] * harga['lampu']) + \
              (komponen_listrik['saklar'] * harga['saklar']) + (komponen_listrik['kabel'] * harga['kabel']) + \
              (komponen_listrik['mcb'] * harga['mcb']) + (dinding['jumlah_pintu'] * harga['pintu']) + \
              (km * harga['closet']) + (km*8 * harga['pipa']) + (km * harga['wastafel']) + \
              (komponen_cat['total'] * harga['cat']) + (komponen_dapur['kitchen_set'] * harga['kitchen_set']) + \
              (kanopi * harga['kanopi']) + (pagar * harga['pagar']) + \
              (komponen_air['kran'] * harga['kran']) + (komponen_air['floor_drain'] * harga['floor_drain']) + \
              (komponen_air['septictank'] * harga['septictank']) + biaya_tukang


# ==================== TAMPILAN ====================

st.markdown(f"""
<div style="display: flex; gap: 20px; margin-bottom: 20px;">
    <div class="total-card"><h3>{luas_bangunan} m²</h3><p>Luas Bangunan</p></div>
    <div class="total-card"><h3>{cakar['jumlah_titik']} titik</h3><p>Cakar Ayam</p></div>
    <div class="total-card"><h3>{hari} hari</h3><p>Estimasi Waktu</p></div>
</div>
""", unsafe_allow_html=True)

# TABS untuk 20 Komponen
tab1, tab2, tab3, tab4 = st.tabs(["📋 20 KOMPONEN", "📊 RINGKASAN", "💰 RAB", "💾 EXPORT"])

with tab1:
    st.markdown("## 📋 20 KOMPONEN PERHITUNGAN")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # KOMPONEN 1
        with st.expander("🪨 1. PONDASI BATU KALI", expanded=True):
            st.metric("Volume", f"{komponen_pondasi['volume']} m³")
            st.metric("Batu Belah", f"{komponen_pondasi['batu_belah']} m³")
            st.metric("Semen", f"{komponen_pondasi['semen']} sak")
            st.metric("Pasir", f"{komponen_pondasi['pasir']} m³")
        
        # KOMPONEN 2
        with st.expander("🏗️ 2. SLOOF (20x25 cm)"):
            st.metric("Volume", f"{komponen_sloof['volume']} m³")
            st.metric("Semen", f"{komponen_sloof['semen']} sak")
            st.metric("Pasir", f"{komponen_sloof['pasir']} m³")
            st.metric("Split", f"{komponen_sloof['split']} m³")
            st.metric("Besi", f"{komponen_sloof['besi_kg']} kg")
        
        # KOMPONEN 3
        with st.expander("🏗️ 3. RING BALOK (15x20 cm)"):
            st.metric("Volume", f"{komponen_ring['volume']} m³")
            st.metric("Semen", f"{komponen_ring['semen']} sak")
            st.metric("Pasir", f"{komponen_ring['pasir']} m³")
            st.metric("Split", f"{komponen_ring['split']} m³")
            st.metric("Besi", f"{komponen_ring['besi_kg']} kg")
        
        # KOMPONEN 4
        with st.expander("📦 4. TOTAL STRUKTUR"):
            st.metric("Total Beton", f"{komponen_struktur['beton']} m³")
            st.metric("Semen", f"{komponen_struktur['semen']} sak")
            st.metric("Pasir", f"{komponen_struktur['pasir']} m³")
            st.metric("Split", f"{komponen_struktur['split']} m³")
            st.metric("Besi", f"{komponen_struktur['besi_kg']} kg ({komponen_struktur['besi_batang']} batang)")
        
        # KOMPONEN 5
        with st.expander("🪵 5. BEKISTING"):
            st.metric("Triplek 12mm", f"{komponen_bekisting['triplek']} lembar")
            st.metric("Kayu Kaso 5/7", f"{komponen_bekisting['kaso']} batang")
            st.metric("Paku", f"{komponen_bekisting['paku']} kg")
        
        # KOMPONEN 6
        with st.expander("🦶 6. CAKAR AYAM"):
            st.metric("Jumlah Titik", f"{cakar['jumlah_titik']} titik")
            st.caption(f"Jarak: {cakar['jarak']}")
            st.metric("Ukuran", f"{cakar['ukuran_cm']}x{cakar['ukuran_cm']} cm")
            st.metric("Volume", f"{cakar['volume_m3']} m³")
            st.metric("Semen", f"{cakar['semen_sak']} sak")
            st.metric("Pasir", f"{cakar['pasir_m3']} m³")
            st.metric("Split", f"{cakar['split_m3']} m³")
            st.metric("Besi", f"{cakar['besi_kg']} kg ({cakar['besi_batang']} batang)")
        
        # KOMPONEN 7
        with st.expander("🧱 7. DINDING (PRESISI)"):
            st.metric("Luas Kotor", f"{dinding['luas_kotor']} m²")
            st.metric(f"Pintu ({dinding['jumlah_pintu']} bh)", f"-{dinding['luas_pintu']} m²")
            st.metric(f"Jendela ({dinding['jumlah_jendela']} bh)", f"-{dinding['luas_jendela']} m²")
            st.metric("Luas Bersih", f"{dinding['luas_bersih']} m²", delta="WAJIB")
            st.metric("Bata", f"{dinding['bata']:,} pcs")
            st.metric("Semen Pasang", f"{dinding['semen_pasang']} sak")
            st.metric("Pasir Pasang", f"{dinding['pasir_pasang']} m³")
            st.metric("Semen Plester", f"{dinding['semen_plester']} sak")
            st.metric("Pasir Plester", f"{dinding['pasir_plester']} m³")
            st.metric("Acian", f"{dinding['acian']} sak")
        
        # KOMPONEN 8
        with st.expander("🏠 8. ATAP"):
            st.metric("Luas Atap", f"{komponen_atap['luas']} m²")
            st.metric("Genteng", f"{komponen_atap['genteng']:,} pcs")
    
    with col2:
        # KOMPONEN 9
        with st.expander("🏗️ 9. RANGKA ATAP"):
            st.markdown(f"**Jenis: {komponen_rangka['jenis']}**")
            if komponen_rangka['jenis'] == 'Baja Ringan':
                st.metric("Kanal C", f"{komponen_rangka['kanal_c']} kg")
                st.metric("Reng", f"{komponen_rangka['reng']} batang")
                st.metric("Sekrup", f"{komponen_rangka['sekrup']:,} pcs")
            else:
                st.metric("Kuda-kuda", f"{komponen_rangka['kuda2']} batang")
                st.metric("Gording", f"{komponen_rangka['gording']} batang")
                st.metric("Reng", f"{komponen_rangka['reng']} batang")
        
        # KOMPONEN 10
        with st.expander("✨ 10. PLAFON"):
            st.metric("Gypsum", f"{komponen_plafon['gypsum']} lembar")
            st.metric("Hollow", f"{komponen_plafon['hollow']} batang")
            st.metric("List Profil", f"{komponen_plafon['list']} meter")
        
        # KOMPONEN 11
        with st.expander("🪨 11. KERAMIK"):
            st.metric("Lantai", f"{komponen_keramik['lantai']} m²")
            st.metric("Dinding KM", f"{komponen_keramik['dinding_km']} m²")
            st.metric("Semen Keramik", f"{komponen_keramik['semen']} sak")
            st.metric("Pasir Keramik", f"{komponen_keramik['pasir']} m³")
        
        # KOMPONEN 12
        with st.expander("⚡ 12. LISTRIK"):
            st.metric("Titik Lampu", f"{komponen_listrik['lampu']} titik")
            st.metric("Saklar", f"{komponen_listrik['saklar']} buah")
            st.metric("Kabel", f"{komponen_listrik['kabel']} meter")
            st.metric("MCB", f"{komponen_listrik['mcb']} buah")
        
        # KOMPONEN 13
        with st.expander("🚽 13. KAMAR MANDI"):
            st.metric("Closet", f"{komponen_km['closet']} buah")
            st.metric("Pipa", f"{komponen_km['pipa']} meter")
            st.metric("Wastafel", f"{komponen_km['wastafel']} buah")
        
        # KOMPONEN 14
        with st.expander("🍳 14. DAPUR"):
            st.metric("Kitchen Set", "Ya" if komponen_dapur['kitchen_set'] else "Tidak")
        
        # KOMPONEN 15
        with st.expander("🎨 15. CAT"):
            st.metric("Cat Tembok", f"{komponen_cat['tembok']} liter")
            st.metric("Cat Plafon", f"{komponen_cat['plafon']} liter")
            st.metric("Total Cat", f"{komponen_cat['total']} liter")
        
        # KOMPONEN 16
        with st.expander("👷 16. TENAGA KERJA"):
            st.metric("Tukang", f"{komponen_tenaga['tukang']} orang")
            st.metric("Kenek", f"{komponen_tenaga['kenek']} orang")
            st.metric("Estimasi Hari", f"{komponen_tenaga['hari']} hari")
            st.metric("Biaya Upah", f"Rp {komponen_tenaga['biaya']:,.0f}")
        
        # KOMPONEN 17
        with st.expander("🪞 17. KANOPI"):
            if komponen_kanopi['ada']:
                st.metric("Luas", f"{komponen_kanopi['luas']} m²")
                st.metric("Rangka", f"{komponen_kanopi['rangka']} kg")
                st.metric("Atap", f"{komponen_kanopi['atap']} m²")
            else:
                st.info("Tidak ada kanopi")
        
        # KOMPONEN 18
        with st.expander("🚪 18. PAGAR"):
            if komponen_pagar['ada']:
                st.metric("Panjang", f"{komponen_pagar['panjang']} meter")
                st.metric("Besi Hollow", f"{komponen_pagar['besi_hollow']} batang")
                st.metric("Cat", f"{komponen_pagar['cat']} kg")
            else:
                st.info("Tidak ada pagar")
        
        # KOMPONEN 19
        with st.expander("💧 19. INSTALASI AIR"):
            st.metric("Pipa Air Bersih", f"{komponen_air['pipa_air_bersih']} meter")
            st.metric("Kran", f"{komponen_air['kran']} buah")
            st.metric("Pipa Air Kotor", f"{komponen_air['pipa_air_kotor']} meter")
            st.metric("Floor Drain", f"{komponen_air['floor_drain']} buah")
            st.metric("Septictank", f"{komponen_air['septictank']} unit")
        
        # KOMPONEN 20
        with st.expander("🚪 20. PINTU & JENDELA DETAIL"):
            st.metric("Pintu", f"{komponen_pintu_jendela['pintu']} buah")
            st.metric("Engsel Pintu", f"{komponen_pintu_jendela['engsel_pintu']} buah")
            st.metric("Gagang Pintu", f"{komponen_pintu_jendela['gagang_pintu']} buah")
            st.metric("Kunci Pintu", f"{komponen_pintu_jendela['kunci_pintu']} buah")
            st.metric("Kusen Pintu", f"{komponen_pintu_jendela['kusen_pintu']} meter")
            st.metric("Jendela", f"{komponen_pintu_jendela['jendela']} buah")
            st.metric("Kaca", f"{komponen_pintu_jendela['kaca']} m²")

with tab2:
    st.markdown("## 📊 RINGKASAN MATERIAL")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏗️ Semen", f"{total_semen} sak")
        st.metric("🪨 Pasir", f"{total_pasir:.2f} m³")
        st.metric("🔩 Split", f"{total_split:.2f} m³")
    with col2:
        st.metric("⚙️ Besi", f"{total_besi:.1f} kg")
        st.metric("🧱 Bata", f"{dinding['bata']:,} pcs")
        st.metric("🏠 Genteng", f"{genteng:,} pcs")
    with col3:
        st.metric("🪨 Keramik Lantai", f"{komponen_keramik['lantai']} m²")
        st.metric("🚽 Keramik KM", f"{komponen_keramik['dinding_km']} m²")
        st.metric("✨ Plafon", f"{komponen_plafon['gypsum']} lbr")
    
    st.markdown("---")
    st.markdown("### 👷 TENAGA KERJA")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tukang", f"{tukang} orang")
    with col2:
        st.metric("Kenek", f"{kenek} orang")
    with col3:
        st.metric("Estimasi Hari", f"{hari} hari")

with tab3:
    st.markdown("## 💰 RENCANA ANGGARAN BIAYA (RAB)")
    
    # Tabel RAB
    rab_data = [
        {"Komponen": "1. Pondasi Batu Kali", "Volume": f"{komponen_pondasi['batu_belah']} m³", "Estimasi": f"Rp {(komponen_pondasi['batu_belah'] * harga['batu_belah']):,.0f}"},
        {"Komponen": "2. Sloof & Ring Balok", "Volume": f"{komponen_struktur['beton']} m³", "Estimasi": f"Rp {(komponen_struktur['beton'] * 1000000):,.0f}"},
        {"Komponen": "3. Cakar Ayam", "Volume": f"{cakar['volume_m3']} m³", "Estimasi": f"Rp {(cakar['volume_m3'] * 1500000):,.0f}"},
        {"Komponen": "4. Bekisting", "Volume": f"{komponen_bekisting['triplek']} lbr", "Estimasi": f"Rp {(komponen_bekisting['triplek'] * harga['triplek']):,.0f}"},
        {"Komponen": "5. Dinding Bata", "Volume": f"{dinding['bata']:,} pcs", "Estimasi": f"Rp {(dinding['bata'] * harga['bata']):,.0f}"},
        {"Komponen": "6. Atap & Genteng", "Volume": f"{genteng:,} pcs", "Estimasi": f"Rp {(genteng * harga[f'genteng_{jenis_atap}']):,.0f}"},
        {"Komponen": "7. Plafon", "Volume": f"{komponen_plafon['gypsum']} lbr", "Estimasi": f"Rp {(komponen_plafon['gypsum'] * harga['gypsum']):,.0f}"},
        {"Komponen": "8. Keramik", "Volume": f"{komponen_keramik['lantai']} m²", "Estimasi": f"Rp {((komponen_keramik['lantai'] + komponen_keramik['dinding_km']) * harga['keramik']):,.0f}"},
        {"Komponen": "9. Listrik", "Volume": f"{komponen_listrik['lampu']} titik", "Estimasi": f"Rp {(komponen_listrik['lampu'] * harga['lampu']):,.0f}"},
        {"Komponen": "10. Kamar Mandi", "Volume": f"{km} unit", "Estimasi": f"Rp {(km * harga['closet'] + km*8 * harga['pipa']):,.0f}"},
        {"Komponen": "11. Cat", "Volume": f"{komponen_cat['total']} liter", "Estimasi": f"Rp {(komponen_cat['total'] * harga['cat']):,.0f}"},
    ]
    
    df_rab = pd.DataFrame(rab_data)
    st.dataframe(df_rab, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div class="success-box">
        <h2 style="margin:0;">Rp {total_biaya:,.0f}</h2>
        <p>💰 TOTAL RAB (Material + Bekisting + Upah Tukang)</p>
        <p style="font-size:12px; margin-top:5px;">✅ Termasuk: 20 Komponen Lengkap</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 💾 EXPORT LAPORAN")
    
    laporan_txt = f"""
ARKI ESTIMATOR PRO - LAPORAN PERHITUNGAN
========================================
Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATA BANGUNAN:
- Panjang: {panjang} m
- Lebar: {lebar} m
- Tinggi: {tinggi} m
- Lantai: {lantai}
- Luas: {luas_bangunan} m²

HASIL PERHITUNGAN 20 KOMPONEN:
========================================
1. PONDASI BATU KALI:
   - Volume: {komponen_pondasi['volume']} m³
   - Batu Belah: {komponen_pondasi['batu_belah']} m³
   - Semen: {komponen_pondasi['semen']} sak
   - Pasir: {komponen_pondasi['pasir']} m³

2. SLOOF:
   - Volume: {komponen_sloof['volume']} m³
   - Semen: {komponen_sloof['semen']} sak
   - Pasir: {komponen_sloof['pasir']} m³
   - Split: {komponen_sloof['split']} m³
   - Besi: {komponen_sloof['besi_kg']} kg

3. RING BALOK:
   - Volume: {komponen_ring['volume']} m³
   - Semen: {komponen_ring['semen']} sak
   - Pasir: {komponen_ring['pasir']} m³
   - Split: {komponen_ring['split']} m³
   - Besi: {komponen_ring['besi_kg']} kg

4. TOTAL STRUKTUR:
   - Beton: {komponen_struktur['beton']} m³
   - Semen: {komponen_struktur['semen']} sak
   - Pasir: {komponen_struktur['pasir']} m³
   - Split: {komponen_struktur['split']} m³
   - Besi: {komponen_struktur['besi_kg']} kg ({komponen_struktur['besi_batang']} batang)

5. BEKISTING:
   - Triplek: {komponen_bekisting['triplek']} lembar
   - Kaso: {komponen_bekisting['kaso']} batang
   - Paku: {komponen_bekisting['paku']} kg

6. CAKAR AYAM:
   - Jumlah Titik: {cakar['jumlah_titik']} titik
   - Ukuran: {cakar['ukuran_cm']}x{cakar['ukuran_cm']} cm
   - Volume: {cakar['volume_m3']} m³
   - Semen: {cakar['semen_sak']} sak
   - Pasir: {cakar['pasir_m3']} m³
   - Split: {cakar['split_m3']} m³
   - Besi: {cakar['besi_kg']} kg

7. DINDING:
   - Luas Bersih: {dinding['luas_bersih']} m²
   - Bata: {dinding['bata']:,} pcs
   - Semen Pasang: {dinding['semen_pasang']} sak
   - Pasir Pasang: {dinding['pasir_pasang']} m³
   - Semen Plester: {dinding['semen_plester']} sak
   - Pasir Plester: {dinding['pasir_plester']} m³
   - Acian: {dinding['acian']} sak

8. ATAP:
   - Luas Atap: {komponen_atap['luas']} m²
   - Genteng: {komponen_atap['genteng']:,} pcs

9. RANGKA ATAP:
   - Jenis: {komponen_rangka['jenis']}

10. PLAFON:
    - Gypsum: {komponen_plafon['gypsum']} lembar
    - Hollow: {komponen_plafon['hollow']} batang

11. KERAMIK:
    - Lantai: {komponen_keramik['lantai']} m²
    - Dinding KM: {komponen_keramik['dinding_km']} m²

12. LISTRIK:
    - Lampu: {komponen_listrik['lampu']} titik
    - Saklar: {komponen_listrik['saklar']} buah
    - Kabel: {komponen_listrik['kabel']} meter
    - MCB: {komponen_listrik['mcb']} buah

13. KAMAR MANDI:
    - Closet: {komponen_km['closet']} buah
    - Pipa: {komponen_km['pipa']} meter
    - Wastafel: {komponen_km['wastafel']} buah

14. DAPUR:
    - Kitchen Set: {'Ya' if komponen_dapur['kitchen_set'] else 'Tidak'}

15. CAT:
    - Total Cat: {komponen_cat['total']} liter

16. TENAGA KERJA:
    - Tukang: {tukang} orang
    - Kenek: {kenek} orang
    - Hari: {hari} hari
    - Biaya: Rp {biaya_tukang:,.0f}

TOTAL REKAP:
- Semen: {total_semen} sak
- Pasir: {total_pasir:.2f} m³
- Split: {total_split:.2f} m³
- Besi: {total_besi:.1f} kg
- Bata: {dinding['bata']:,} pcs
- Genteng: {genteng:,} pcs

TOTAL RAB: Rp {total_biaya:,.0f}
========================================
ARKI ESTIMATOR PRO
    """
    
    st.download_button("📥 Download Laporan TXT", laporan_txt, f"laporan_{datetime.now().strftime('%Y%m%d')}.txt")
    
    st.download_button("📥 Download Laporan JSON", 
                       json.dumps({
                           'tanggal': str(datetime.now()),
                           'data_bangunan': {
                               'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai
                           },
                           'total_biaya': total_biaya,
                           'total_semen': total_semen,
                           'total_pasir': total_pasir,
                           'total_split': total_split,
                           'total_besi': total_besi
                       }, indent=2),
                       f"laporan_{datetime.now().strftime('%Y%m%d')}.json")

# Footer
st.markdown("""
<hr>
<p style="text-align:center; color:#64748b; font-size:12px;">
    🏗️ ARKI ESTIMATOR PRO | 20 Komponen Lengkap | Perhitungan Presisi Standar SNI
</p>
""", unsafe_allow_html=True)
