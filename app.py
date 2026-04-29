# app.py - ARKIDIGITAL ESTIMATOR PRO (PRECISION 20 COMPONENTS)

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="ARKIDIGITAL ESTIMATOR PRO",
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
    
    /* Header utama dengan logo */
    .hero-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        padding: 20px 32px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.15);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .logo-icon {
        font-size: 48px;
    }
    .hero-text h1 {
        color: white !important;
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }
    .hero-text p {
        color: #dbeafe;
        margin: 5px 0 0 0;
        font-size: 13px;
    }
    .hero-badge {
        background: rgba(255,255,255,0.2);
        padding: 8px 16px;
        border-radius: 30px;
        color: white;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Cards untuk metrics */
    .metric-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bfdbfe;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
    }
    
    /* Komponen Card */
    .component-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 0;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        transition: all 0.2s;
    }
    .component-card:hover {
        border-color: #bfdbfe;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .component-header {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 14px 20px;
        border-bottom: 1px solid #e2e8f0;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .component-num {
        background: #1e40af;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
    }
    .component-title {
        font-weight: 700;
        color: #1e293b;
        font-size: 16px;
    }
    .component-body {
        padding: 16px 20px;
        background: white;
    }
    
    /* Grid untuk detail komponen */
    .detail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
    }
    .detail-item {
        background: #f8fafc;
        padding: 10px 14px;
        border-radius: 12px;
        border-left: 3px solid #2563eb;
    }
    .detail-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .detail-value {
        font-size: 16px;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* Custom divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, #2563eb, #93c5fd, #2563eb);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* Input styling */
    .stNumberInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Grand Total */
    .grand-total {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER WITH LOGO ====================
st.markdown("""
<div class="hero-header">
    <div class="hero-left">
        <div class="logo-icon">🏗️</div>
        <div class="hero-text">
            <h1>ARKIDIGITAL ESTIMATOR PRO</h1>
            <p>Aplikasi Hitung Cepat Kebutuhan Material Bangunan | Presisi 20 Komponen</p>
        </div>
    </div>
    <div class="hero-badge">PREMIUM CALCULATOR</div>
</div>
""", unsafe_allow_html=True)

# ==================== SESSION STATE UNTUK TOMBOL HITUNG ====================
if 'hitung' not in st.session_state:
    st.session_state.hitung = False

def proses_perhitungan():
    st.session_state.hitung = True

# ==================== FORM INPUT DATA ====================
st.markdown("### 📐 Input Data Proyek")

with st.form("input_form"):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**🏠 Dimensi Bangunan**")
        panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
        lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5)
        tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1)
        lantai = st.select_slider("Jumlah Lantai", options=[1, 2, 3], value=1)
    
    with col2:
        st.markdown("**🛏️ Ruangan**")
        kamar = st.number_input("Kamar Tidur", min_value=1, max_value=10, value=3, step=1)
        km = st.number_input("Kamar Mandi", min_value=1, max_value=5, value=2, step=1)
        ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1, step=1)
        dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1, step=1)
    
    with col3:
        st.markdown("**🔧 Material & Spek**")
        jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], 
                                   format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton")
        rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"],
                                    format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu")
        jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"],
                                   format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan")
        ukuran_besi = st.selectbox("Ukuran Besi Utama", [10, 13, 16], format_func=lambda x: f"Ø{x} mm")
    
    with col4:
        st.markdown("**👷 Tenaga & Opsional**")
        upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000)
        upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000)
        garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1)
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1)
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1)
    
    # Tombol Submit
    col_button = st.columns([1, 2, 1])
    with col_button[1]:
        submitted = st.form_submit_button("🔨 HITUNG KEBUTUHAN", use_container_width=True, on_click=proses_perhitungan)

# ==================== FUNGSI PERHITUNGAN PRESISI ====================

def hitung_cakar_ayam(p, l, lt, ukuran_besi):
    """Perhitungan cakar ayam presisi"""
    if lt == 1:
        kp = math.ceil(p / 5.0) + 1
        kl = math.ceil(l / 5.0) + 1
        jumlah = kp * kl
        ukuran = 0.6
        tebal = 0.25
        jarak = "5 meter (standar rumah 1 lantai)"
    elif lt == 2:
        kp = math.ceil(p / 3.5) + 1
        kl = math.ceil(l / 3.5) + 1
        jumlah = kp * kl
        ukuran = 0.8
        tebal = 0.30
        jarak = "3.5 meter (standar rumah 2 lantai)"
    else:
        kp = math.ceil(p / 3.0) + 1
        kl = math.ceil(l / 3.0) + 1
        jumlah = kp * kl
        ukuran = 1.0
        tebal = 0.35
        jarak = "3 meter (rumah 3+ lantai)"
    
    vol_per_titik = ukuran * ukuran * tebal
    vol_total = jumlah * vol_per_titik
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    panjang_besi_per_titik = (ukuran * 4) * 8
    berat_besi = (panjang_besi_per_titik * jumlah) * berat_per_meter
    batang_besi = math.ceil((panjang_besi_per_titik * jumlah) / 12)
    
    return {
        'jumlah': jumlah, 'jarak': jarak, 'ukuran_cm': ukuran * 100,
        'tebal_cm': tebal * 100, 'volume': round(vol_total, 2),
        'semen': math.ceil(vol_total * 8.5),
        'pasir': round(vol_total * 0.7, 2),
        'split': round(vol_total * 0.9, 2),
        'besi_kg': round(berat_besi, 1),
        'besi_batang': batang_besi
    }


def hitung_dinding_presisi(p, l, t, kamar, km, ruang_tamu, dapur, garasi):
    """Perhitungan dinding presisi tidak double count"""
    # Panjang dinding luar
    panjang_dinding_luar = 2 * (p + l)
    
    # Panjang dinding internal (perkiraan berdasarkan ruangan)
    panjang_internal = (kamar * 3.5) + (km * 2.5) + (ruang_tamu * 3) + (dapur * 3) + (garasi * 2)
    
    total_panjang_dinding = panjang_dinding_luar + panjang_internal
    luas_kotor = total_panjang_dinding * t
    
    # Estimasi bukaan (pintu + jendela)
    jumlah_pintu = kamar + km + ruang_tamu + (1 if dapur > 0 else 0) + (1 if garasi > 0 else 0)
    jumlah_jendela = kamar + ruang_tamu + (1 if dapur > 0 else 0)
    
    luas_pintu = jumlah_pintu * (0.9 * 2.1)
    luas_jendela = jumlah_jendela * (1.2 * 1.0)
    luas_bersih = luas_kotor - luas_pintu - luas_jendela
    
    # Pastikan tidak negatif
    luas_bersih = max(luas_bersih, luas_kotor * 0.6)
    
    return {
        'luas_kotor': round(luas_kotor, 2),
        'luas_bersih': round(luas_bersih, 2),
        'jumlah_pintu': jumlah_pintu,
        'jumlah_jendela': jumlah_jendela,
        'luas_pintu': round(luas_pintu, 2),
        'luas_jendela': round(luas_jendela, 2),
        'bata_merah': math.ceil(luas_bersih * 70),
        'bata_hebel': math.ceil(luas_bersih * 8.5),
        'semen_pasang': math.ceil(luas_bersih * 0.32),
        'pasir_pasang': round(luas_bersih * 0.045, 2),
        'semen_plester': math.ceil(luas_bersih * 2 * 0.22),
        'pasir_plester': round(luas_bersih * 2 * 0.028, 2),
        'acian': math.ceil(luas_bersih * 2 * 0.18)
    }


# ==================== PROSES PERHITUNGAN ====================
if st.session_state.hitung:
    
    # Variabel dasar
    luas_bangunan = panjang * lebar
    luas_total = luas_bangunan * lantai
    keliling = 2 * (panjang + lebar)
    
    # ========== KOMPONEN 1: PONDASI BATU KALI ==========
    vol_pondasi = keliling * 0.7 * 0.8
    pondasi = {
        'volume': round(vol_pondasi, 2),
        'batu_belah': round(vol_pondasi * 1.25, 2),
        'semen': math.ceil(vol_pondasi * 4.8),
        'pasir': round(vol_pondasi * 0.6, 2)
    }
    
    # ========== KOMPONEN 2: SLOOF ==========
    vol_sloof = keliling * 0.2 * 0.25
    sloof = {
        'volume': round(vol_sloof, 2),
        'semen': math.ceil(vol_sloof * 8.5),
        'pasir': round(vol_sloof * 0.7, 2),
        'split': round(vol_sloof * 0.9, 2),
        'besi_kg': round(vol_sloof * 130, 1)
    }
    
    # ========== KOMPONEN 3: RING BALOK ==========
    vol_ring = keliling * 0.15 * 0.2
    ring = {
        'volume': round(vol_ring, 2),
        'semen': math.ceil(vol_ring * 8.5),
        'pasir': round(vol_ring * 0.7, 2),
        'split': round(vol_ring * 0.9, 2),
        'besi_kg': round(vol_ring * 130, 1)
    }
    
    # ========== KOMPONEN 4: KOLOM PRAKTIS ==========
    jumlah_kolom = math.ceil(keliling / 3) * lantai
    vol_kolom = jumlah_kolom * 0.13 * 0.13 * tinggi
    kolom = {
        'jumlah': jumlah_kolom,
        'volume': round(vol_kolom, 2),
        'semen': math.ceil(vol_kolom * 9),
        'pasir': round(vol_kolom * 0.72, 2),
        'split': round(vol_kolom * 0.95, 2),
        'besi_kg': round(vol_kolom * 160, 1)
    }
    
    # ========== KOMPONEN 5: BEKISTING ==========
    luas_bekisting = (vol_sloof * 8) + (vol_ring * 7) + (vol_kolom * 10)
    bekisting = {
        'luas': round(luas_bekisting, 2),
        'triplek': math.ceil(luas_bekisting * 0.4),
        'kaso': math.ceil(luas_bekisting * 2.8),
        'paku': round(luas_bekisting * 0.22, 1)
    }
    
    # ========== KOMPONEN 6: CAKAR AYAM ==========
    cakar = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)
    
    # ========== KOMPONEN 7: DINDING ==========
    dinding = hitung_dinding_presisi(panjang, lebar, tinggi, kamar, km, ruang_tamu, dapur, garasi)
    
    # Pilih jenis bata
    if jenis_bata == "merah":
        jumlah_bata = dinding['bata_merah']
    else:
        jumlah_bata = dinding['bata_hebel']
    
    # ========== KOMPONEN 8: ATAP ==========
    sudut_atap = 30
    luas_atap = luas_bangunan * (1 / math.cos(math.radians(sudut_atap))) * 1.1
    genteng_per_m2 = {'metal': 1.6, 'tanah': 28, 'beton': 11}
    genteng = math.ceil(luas_atap * genteng_per_m2[jenis_atap])
    
    # ========== KOMPONEN 9: RANGKA ATAP ==========
    if rangka_atap == 'baja':
        rangka = {
            'jenis': 'Baja Ringan',
            'kanal_c': math.ceil(luas_atap * 4.8),
            'reng': math.ceil(luas_atap * 2.8),
            'sekrup': math.ceil(luas_atap * 14)
        }
    else:
        rangka = {
            'jenis': 'Kayu',
            'kayu_kasau': math.ceil(luas_atap * 6),
            'kayu_reng': math.ceil(luas_atap * 4),
            'paku': math.ceil(luas_atap * 0.5)
        }
    
    # ========== KOMPONEN 10: PLAFON ==========
    plafon = {
        'luas': round(luas_bangunan, 2),
        'gypsum': math.ceil(luas_bangunan * 0.4),
        'hollow': math.ceil(luas_bangunan * 0.9),
        'list': math.ceil(keliling * 1.3)
    }
    
    # ========== KOMPONEN 11: KERAMIK ==========
    keramik = {
        'lantai': math.ceil(luas_bangunan * 1.08),
        'dinding_km': km * 8,
        'semen': math.ceil((luas_bangunan + km*8) * 0.35),
        'pasir': round((luas_bangunan + km*8) * 0.035, 2)
    }
    
    # ========== KOMPONEN 12: LISTRIK ==========
    titik_listrik = kamar * 3 + km * 2 + ruang_tamu * 3 + dapur * 3 + garasi * 1 + 2
    listrik = {
        'titik_lampu': titik_listrik,
        'saklar': math.ceil(titik_listrik * 0.6),
        'stop_kontak': math.ceil(titik_listrik * 0.5),
        'kabel_meter': titik_listrik * 12,
        'mcb': 6 if lantai >= 2 else 4
    }
    
    # ========== KOMPONEN 13: SANITASI ==========
    sanitasi = {
        'closet': km,
        'wastafel': km,
        'pipa_air_bersih': km * 12,
        'pipa_air_kotor': km * 8,
        'septictank': 1 if km > 0 else 0
    }
    
    # ========== KOMPONEN 14: PINTU ==========
    pintu = {
        'jumlah': dinding['jumlah_pintu'],
        'harga_satuan': 500000,
        'total': dinding['jumlah_pintu'] * 500000
    }
    
    # ========== KOMPONEN 15: JENDELA ==========
    jendela = {
        'jumlah': dinding['jumlah_jendela'],
        'harga_satuan': 300000,
        'total': dinding['jumlah_jendela'] * 300000
    }
    
    # ========== KOMPONEN 16: CAT ==========
    cat = {
        'tembok': math.ceil(dinding['luas_bersih'] * 0.14),
        'plafon': math.ceil(luas_bangunan * 0.12),
        'kayu_besi': math.ceil((dinding['jumlah_pintu'] + dinding['jumlah_jendela']) * 0.5),
        'total': math.ceil(dinding['luas_bersih'] * 0.14 + luas_bangunan * 0.12)
    }
    
    # ========== KOMPONEN 17: DAPUR ==========
    dapur_set = {
        'tersedia': dapur > 0,
        'kitchen_set': 3000000 if dapur > 0 else 0,
        'meja_dapur': 1500000 if dapur > 0 else 0,
        'total': 4500000 if dapur > 0 else 0
    }
    
    # ========== KOMPONEN 18: KANOPI ==========
    kanopi_comp = {
        'luas': kanopi,
        'harga_satuan': 350000,
        'total': kanopi * 350000
    }
    
    # ========== KOMPONEN 19: PAGAR ==========
    pagar_comp = {
        'panjang': pagar,
        'harga_satuan': 850000,
        'total': pagar * 850000
    }
    
    # ========== KOMPONEN 20: TENAGA KERJA ==========
    tenaga = {
        'tukang': max(2, math.ceil(luas_total / 28)),
        'kenek': max(2, math.ceil(luas_total / 35)),
        'hari': max(30, math.ceil(luas_total / 2.8)),
        'biaya_tukang': 0,
        'biaya_kenek': 0,
        'total': 0
    }
    tenaga['biaya_tukang'] = tenaga['tukang'] * upah_tukang * tenaga['hari']
    tenaga['biaya_kenek'] = tenaga['kenek'] * upah_kenek * tenaga['hari']
    tenaga['total'] = tenaga['biaya_tukang'] + tenaga['biaya_kenek']
    
    # ========== TOTAL REKAP MATERIAL ==========
    total_semen = (pondasi['semen'] + sloof['semen'] + ring['semen'] + 
                   kolom['semen'] + cakar['semen'] + dinding['semen_pasang'] + 
                   dinding['semen_plester'] + keramik['semen'])
    
    total_pasir = (pondasi['pasir'] + sloof['pasir'] + ring['pasir'] + 
                   kolom['pasir'] + cakar['pasir'] + dinding['pasir_pasang'] + 
                   dinding['pasir_plester'] + keramik['pasir'])
    
    total_split = (sloof['split'] + ring['split'] + kolom['split'] + cakar['split'])
    
    total_besi = (sloof['besi_kg'] + ring['besi_kg'] + kolom['besi_kg'] + cakar['besi_kg'])
    
    # ========== TOTAL BIAYA ==========
    harga_satuan = {
        'semen': 65000, 'pasir': 300000, 'split': 320000, 'batu': 250000,
        'bata_merah': 800, 'bata_hebel': 12000, 'besi': 15000,
        'triplek': 180000, 'kaso': 25000, 'paku': 18000,
        'genteng_metal': 25000, 'genteng_tanah': 5000, 'genteng_beton': 12000,
        'rangka_baja': 15000, 'rangka_kayu': 25000,
        'gypsum': 45000, 'hollow': 35000, 'list': 8000,
        'keramik': 90000, 'kabel': 15000, 'saklar': 25000,
        'lampu': 45000, 'mcb': 75000, 'closet': 800000,
        'wastafel': 300000, 'pipa': 50000, 'cat': 35000,
        'septictank': 2000000
    }
    
    total_biaya_material = (
        # Pondasi
        pondasi['batu_belah'] * harga_satuan['batu'] +
        pondasi['semen'] * harga_satuan['semen'] +
        pondasi['pasir'] * harga_satuan['pasir'] +
        # Sloof, Ring, Kolom, Cakar
        (sloof['semen'] + ring['semen'] + kolom['semen'] + cakar['semen']) * harga_satuan['semen'] +
        (sloof['pasir'] + ring['pasir'] + kolom['pasir'] + cakar['pasir']) * harga_satuan['pasir'] +
        (sloof['split'] + ring['split'] + kolom['split'] + cakar['split']) * harga_satuan['split'] +
        (sloof['besi_kg'] + ring['besi_kg'] + kolom['besi_kg'] + cakar['besi_kg']) * harga_satuan['besi'] +
        # Bekisting
        bekisting['triplek'] * harga_satuan['triplek'] +
        bekisting['kaso'] * harga_satuan['kaso'] +
        bekisting['paku'] * harga_satuan['paku'] +
        # Dinding
        jumlah_bata * (harga_satuan['bata_merah'] if jenis_bata == 'merah' else harga_satuan['bata_hebel']) +
        dinding['semen_pasang'] * harga_satuan['semen'] +
        dinding['semen_plester'] * harga_satuan['semen'] +
        dinding['pasir_pasang'] * harga_satuan['pasir'] +
        dinding['pasir_plester'] * harga_satuan['pasir'] +
        # Atap
        genteng * (harga_satuan[f'genteng_{jenis_atap}']) +
        (rangka['kanal_c'] * harga_satuan['rangka_baja'] if rangka_atap == 'baja' else rangka['kayu_kasau'] * harga_satuan['rangka_kayu']) +
        # Plafon
        plafon['gypsum'] * harga_satuan['gypsum'] +
        plafon['hollow'] * harga_satuan['hollow'] +
        plafon['list'] * harga_satuan['list'] +
        # Keramik
        (keramik['lantai'] + keramik['dinding_km']) * harga_satuan['keramik'] +
        keramik['semen'] * harga_satuan['semen'] +
        # Listrik
        listrik['kabel_meter'] * harga_satuan['kabel'] +
        listrik['saklar'] * harga_satuan['saklar'] +
        listrik['titik_lampu'] * harga_satuan['lampu'] +
        listrik['mcb'] * harga_satuan['mcb'] +
        # Sanitasi
        sanitasi['closet'] * harga_satuan['closet'] +
        sanitasi['wastafel'] * harga_satuan['wastafel'] +
        (sanitasi['pipa_air_bersih'] + sanitasi['pipa_air_kotor']) * harga_satuan['pipa'] +
        sanitasi['septictank'] * harga_satuan['septictank'] +
        # Pintu & Jendela
        pintu['total'] + jendela['total'] +
        # Cat
        cat['total'] * harga_satuan['cat'] +
        # Dapur
        dapur_set['total'] +
        # Kanopi & Pagar
        kanopi_comp['total'] + pagar_comp['total']
    )
    
    total_biaya = total_biaya_material + tenaga['total']
    
    # ============ TAMPILAN HASIL ============
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Ringkasan Proyek
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
            <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">{cakar['jumlah']} titik</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color:#475569; font-size:13px; margin:0;">📅 Estimasi Waktu</p>
            <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:28px;">{tenaga['hari']} hari</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color:#475569; font-size:13px; margin:0;">👷 Tenaga Kerja</p>
            <h3 style="color:#1e40af; margin:8px 0 0 0; font-size:24px;">{tenaga['tukang']} Tk + {tenaga['kenek']} Kn</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ============ 20 KOMPONEN ============
    st.markdown("### 📋 Rincian 20 Komponen")
    
    # Komponen 1-5: Struktur
    st.markdown("#### 🏗️ STRUKTUR UTAMA (1-5)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Komponen 1: Pondasi
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">1</span> <span class="component-title">Pondasi Batu Kali</span></div>
                <span>🏗️</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{pondasi['volume']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Batu Belah</div><div class="detail-value">{pondasi['batu_belah']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{pondasi['semen']} sak</div></div>
                    <div class="detail-item"><div class="detail-label">Pasir</div><div class="detail-value">{pondasi['pasir']} m³</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Komponen 2: Sloof
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">2</span> <span class="component-title">Sloof (20x25 cm)</span></div>
                <span>📏</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{sloof['volume']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{sloof['semen']} sak</div></div>
                    <div class="detail-item"><div class="detail-label">Pasir</div><div class="detail-value">{sloof['pasir']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Split</div><div class="detail-value">{sloof['split']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{sloof['besi_kg']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Komponen 3: Ring Balok
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">3</span> <span class="component-title">Ring Balok (15x20 cm)</span></div>
                <span>📏</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{ring['volume']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{ring['semen']} sak</div></div>
                    <div class="detail-item"><div class="detail-label">Pasir</div><div class="detail-value">{ring['pasir']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Split</div><div class="detail-value">{ring['split']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{ring['besi_kg']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Komponen 4: Kolom Praktis
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">4</span> <span class="component-title">Kolom Praktis (13x13 cm)</span></div>
                <span>🏛️</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{kolom['jumlah']} buah</div></div>
                    <div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{kolom['volume']} m³</div></div>
                    <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{kolom['semen']} sak</div></div>
                    <div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{kolom['besi_kg']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Komponen 5: Bekisting
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">5</span> <span class="component-title">Bekisting</span></div>
                <span>🪵</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{bekisting['luas']} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Triplek</div><div class="detail-value">{bekisting['triplek']} lbr</div></div>
                    <div class="detail-item"><div class="detail-label">Kaso</div><div class="detail-value">{bekisting['kaso']} btg</div></div>
                    <div class="detail-item"><div class="detail-label">Paku</div><div class="detail-value">{bekisting['paku']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Komponen 6: Cakar Ayam
    st.markdown("#### 🦶 PONDASI TITIK (6)")
    st.markdown(f"""
    <div class="component-card">
        <div class="component-header">
            <div><span class="component-num">6</span> <span class="component-title">Cakar Ayam</span></div>
            <span>🦶</span>
        </div>
        <div class="component-body">
            <div class="detail-grid">
                <div class="detail-item"><div class="detail-label">Jumlah Titik</div><div class="detail-value">{cakar['jumlah']} titik</div></div>
                <div class="detail-item"><div class="detail-label">Jarak</div><div class="detail-value">{cakar['jarak']}</div></div>
                <div class="detail-item"><div class="detail-label">Ukuran</div><div class="detail-value">{cakar['ukuran_cm']:.0f}x{cakar['ukuran_cm']:.0f} cm</div></div>
                <div class="detail-item"><div class="detail-label">Volume Beton</div><div class="detail-value">{cakar['volume']} m³</div></div>
                <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{cakar['semen']} sak</div></div>
                <div class="detail-item"><div class="detail-label">Pasir</div><div class="detail-value">{cakar['pasir']} m³</div></div>
                <div class="detail-item"><div class="detail-label">Split</div><div class="detail-value">{cakar['split']} m³</div></div>
                <div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{cakar['besi_kg']} kg ({cakar['besi_batang']} btg)</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Komponen 7: Dinding
    st.markdown("#### 🧱 DINDING (7)")
    st.markdown(f"""
    <div class="component-card">
        <div class="component-header">
            <div><span class="component-num">7</span> <span class="component-title">Dinding Bata</span></div>
            <span>🧱</span>
        </div>
        <div class="component-body">
            <div class="detail-grid">
                <div class="detail-item"><div class="detail-label">Luas Bersih</div><div class="detail-value">{dinding['luas_bersih']} m²</div></div>
                <div class="detail-item"><div class="detail-label">Pintu</div><div class="detail-value">{dinding['jumlah_pintu']} bh (-{dinding['luas_pintu']} m²)</div></div>
                <div class="detail-item"><div class="detail-label">Jendela</div><div class="detail-value">{dinding['jumlah_jendela']} bh (-{dinding['luas_jendela']} m²)</div></div>
                <div class="detail-item"><div class="detail-label">Bata</div><div class="detail-value">{jumlah_bata:,} pcs</div></div>
                <div class="detail-item"><div class="detail-label">Semen Pasang</div><div class="detail-value">{dinding['semen_pasang']} sak</div></div>
                <div class="detail-item"><div class="detail-label">Semen Plester</div><div class="detail-value">{dinding['semen_plester']} sak</div></div>
                <div class="detail-item"><div class="detail-label">Pasir Pasang</div><div class="detail-value">{dinding['pasir_pasang']} m³</div></div>
                <div class="detail-item"><div class="detail-label">Pasir Plester</div><div class="detail-value">{dinding['pasir_plester']} m³</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Komponen 8-10: Atap, Rangka, Plafon
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏠 ATAP & RANGKA (8-9)")
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">8</span> <span class="component-title">Atap & Genteng</span></div>
                <span>🏠</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Luas Atap</div><div class="detail-value">{luas_atap:.2f} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Genteng {jenis_atap.title()}</div><div class="detail-value">{genteng:,} pcs</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">9</span> <span class="component-title">Rangka Atap ({rangka['jenis']})</span></div>
                <span>🔧</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">{'Kanal C' if rangka_atap=='baja' else 'Kayu Kasau'}</div><div class="detail-value">{rangka['kanal_c'] if rangka_atap=='baja' else rangka['kayu_kasau']} {'kg' if rangka_atap=='baja' else 'btg'}</div></div>
                    <div class="detail-item"><div class="detail-label">Reng</div><div class="detail-value">{rangka['reng']} {'kg' if rangka_atap=='baja' else 'btg'}</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ✨ PLAFON & KERAMIK (10-11)")
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">10</span> <span class="component-title">Plafon Gypsum</span></div>
                <span>✨</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{plafon['luas']} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Gypsum</div><div class="detail-value">{plafon['gypsum']} lbr</div></div>
                    <div class="detail-item"><div class="detail-label">Hollow</div><div class="detail-value">{plafon['hollow']} btg</div></div>
                    <div class="detail-item"><div class="detail-label">List Gypsum</div><div class="detail-value">{plafon['list']} m</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">11</span> <span class="component-title">Keramik Lantai & Dinding</span></div>
                <span>🪨</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Keramik Lantai</div><div class="detail-value">{keramik['lantai']} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Keramik Dinding KM</div><div class="detail-value">{keramik['dinding_km']} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{keramik['semen']} sak</div></div>
                    <div class="detail-item"><div class="detail-label">Pasir</div><div class="detail-value">{keramik['pasir']} m³</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Komponen 12-15: Listrik, Sanitasi, Pintu, Jendela
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚡ MEKANIKAL & ELEKTRIKAL (12-13)")
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">12</span> <span class="component-title">Instalasi Listrik</span></div>
                <span>⚡</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Titik Lampu</div><div class="detail-value">{listrik['titik_lampu']} titik</div></div>
                    <div class="detail-item"><div class="detail-label">Saklar</div><div class="detail-value">{listrik['saklar']} bh</div></div>
                    <div class="detail-item"><div class="detail-label">Stop Kontak</div><div class="detail-value">{listrik['stop_kontak']} bh</div></div>
                    <div class="detail-item"><div class="detail-label">Kabel</div><div class="detail-value">{listrik['kabel_meter']} m</div></div>
                    <div class="detail-item"><div class="detail-label">MCB</div><div class="detail-value">{listrik['mcb']} A</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">13</span> <span class="component-title">Sanitasi</span></div>
                <span>🚽</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Closet</div><div class="detail-value">{sanitasi['closet']} bh</div></div>
                    <div class="detail-item"><div class="detail-label">Wastafel</div><div class="detail-value">{sanitasi['wastafel']} bh</div></div>
                    <div class="detail-item"><div class="detail-label">Pipa Air Bersih</div><div class="detail-value">{sanitasi['pipa_air_bersih']} m</div></div>
                    <div class="detail-item"><div class="detail-label">Pipa Air Kotor</div><div class="detail-value">{sanitasi['pipa_air_kotor']} m</div></div>
                    <div class="detail-item"><div class="detail-label">Septic Tank</div><div class="detail-value">{'Ya' if sanitasi['septictank']>0 else 'Tidak'}</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🚪 BUKAAN & FINISHING (14-16)")
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">14</span> <span class="component-title">Pintu</span></div>
                <span>🚪</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{pintu['jumlah']} unit</div></div>
                    <div class="detail-item"><div class="detail-label">Estimasi Biaya</div><div class="detail-value">Rp {pintu['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">15</span> <span class="component-title">Jendela</span></div>
                <span>🪟</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{jendela['jumlah']} unit</div></div>
                    <div class="detail-item"><div class="detail-label">Estimasi Biaya</div><div class="detail-value">Rp {jendela['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">16</span> <span class="component-title">Cat</span></div>
                <span>🎨</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Cat Tembok</div><div class="detail-value">{cat['tembok']} liter</div></div>
                    <div class="detail-item"><div class="detail-label">Cat Plafon</div><div class="detail-value">{cat['plafon']} liter</div></div>
                    <div class="detail-item"><div class="detail-label">Total</div><div class="detail-value">{cat['total']} liter</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Komponen 17-20: Dapur, Kanopi, Pagar, Tenaga
    st.markdown("#### 🍳 OPSIONAL & TENAGA KERJA (17-20)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">17</span> <span class="component-title">Kitchen Set</span></div>
                <span>🍳</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Status</div><div class="detail-value">{'Tersedia' if dapur_set['tersedia'] else 'Tidak'}</div></div>
                    <div class="detail-item"><div class="detail-label">Estimasi Biaya</div><div class="detail-value">Rp {dapur_set['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">18</span> <span class="component-title">Kanopi</span></div>
                <span>🏡</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{kanopi_comp['luas']} m²</div></div>
                    <div class="detail-item"><div class="detail-label">Estimasi Biaya</div><div class="detail-value">Rp {kanopi_comp['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">19</span> <span class="component-title">Pagar</span></div>
                <span>🚧</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Panjang</div><div class="detail-value">{pagar_comp['panjang']} m</div></div>
                    <div class="detail-item"><div class="detail-label">Estimasi Biaya</div><div class="detail-value">Rp {pagar_comp['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">20</span> <span class="component-title">Tenaga Kerja</span></div>
                <span>👷</span>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Tukang</div><div class="detail-value">{tenaga['tukang']} orang</div></div>
                    <div class="detail-item"><div class="detail-label">Kenek</div><div class="detail-value">{tenaga['kenek']} orang</div></div>
                    <div class="detail-item"><div class="detail-label">Waktu Pengerjaan</div><div class="detail-value">{tenaga['hari']} hari</div></div>
                    <div class="detail-item"><div class="detail-label">Biaya Tukang</div><div class="detail-value">Rp {tenaga['biaya_tukang']:,.0f}</div></div>
                    <div class="detail-item"><div class="detail-label">Biaya Kenek</div><div class="detail-value">Rp {tenaga['biaya_kenek']:,.0f}</div></div>
                    <div class="detail-item"><div class="detail-label">Total Upah</div><div class="detail-value">Rp {tenaga['total']:,.0f}</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ringkasan Material
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📦 Ringkasan Total Material")
    
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
        st.metric("Total Bata", f"{jumlah_bata:,} pcs")
    
    # Grand Total
    st.markdown(f"""
    <div class="grand-total">
        <p style="color: #dbeafe; font-size: 14px; margin: 0;">GRAND TOTAL RENCANA ANGGARAN BIAYA (RAB)</p>
        <h2 style="color: white; margin: 10px 0 0 0; font-size: 42px;">Rp {total_biaya:,.0f}</h2>
        <p style="color: #bfdbfe; margin-top: 10px; font-size: 12px;">*Sudah termasuk material, upah tukang, dan overhead</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Export Data
    st.markdown("---")
    st.markdown("### 📄 Export Data")
    
    # Buat data untuk export
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'dimensi': {'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai},
        'ruangan': {'kamar': kamar, 'km': km, 'dapur': dapur, 'garasi': garasi},
        'material': {
            'total_semen': total_semen, 'total_pasir': total_pasir,
            'total_split': total_split, 'total_besi': total_besi,
            'total_bata': jumlah_bata, 'total_genteng': genteng
        },
        'tenaga': {'tukang': tenaga['tukang'], 'kenek': tenaga['kenek'], 'hari': tenaga['hari']},
        'total_biaya': total_biaya
    }
    
    col1, col2 = st.columns(2)
    with col1:
        json_str = json.dumps(export_data, indent=2, default=str)
        st.download_button("📥 Download JSON", json_str, f"estimator_{datetime.now().strftime('%Y%m%d')}.json", "application/json")
    with col2:
        df_export = pd.DataFrame([{
            'Tanggal': datetime.now().strftime('%Y-%m-%d'),
            'Luas(m²)': luas_bangunan, 'Semen(sak)': total_semen,
            'Pasir(m³)': total_pasir, 'Split(m³)': total_split,
            'Besi(kg)': total_besi, 'Bata(pcs)': jumlah_bata,
            'Total Biaya': total_biaya
        }])
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"estimator_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

else:
    # Tampilkan pesan sebelum hitung
    st.info("👆 Silakan isi data proyek di atas, lalu klik tombol **HITUNG KEBUTUHAN** untuk melihat hasil perhitungan 20 komponen.")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px;">
    <hr style="border-color: #e2e8f0;">
    <p style="color: #94a3b8;">🏗️ ARKIDIGITAL ESTIMATOR PRO | Presisi 20 Komponen | © 2024</p>
    <p style="color: #cbd5e1; font-size: 12px;">Aplikasi hitung cepat kebutuhan material bangunan | Data bersifat estimasi</p>
</div>
""", unsafe_allow_html=True)
