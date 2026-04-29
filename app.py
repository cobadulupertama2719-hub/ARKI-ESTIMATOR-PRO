# app.py - ARKIDIGITAL ESTIMATOR PRO (Dengan AI Denah Generator)

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json
import requests
from PIL import Image
import io
import base64

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #ffffff !important; }
    
    .hero-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        padding: 20px 32px;
        border-radius: 20px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-left { display: flex; align-items: center; gap: 15px; }
    .logo-icon { font-size: 48px; }
    .hero-text h1 { color: white !important; margin: 0; font-size: 28px; font-weight: 700; }
    .hero-text p { color: #dbeafe; margin: 5px 0 0 0; font-size: 13px; }
    .hero-badge { background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 30px; color: white; font-size: 12px; }
    
    .metric-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bfdbfe;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15); }
    
    .component-card {
        background: #ffffff;
        border-radius: 16px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }
    .component-header {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 14px 20px;
        border-bottom: 1px solid #e2e8f0;
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
    .component-title { font-weight: 700; color: #1e293b; font-size: 16px; }
    .component-body { padding: 16px 20px; background: white; }
    
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
    .detail-label { font-size: 11px; color: #64748b; text-transform: uppercase; }
    .detail-value { font-size: 16px; font-weight: 700; color: #1e293b; }
    
    .denah-card {
        background: #f8fafc;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
    }
    .denah-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #2563eb;
    }
    .denah-image {
        width: 100%;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, #2563eb, #93c5fd, #2563eb);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    .grand-total {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 30px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="hero-header">
    <div class="hero-left">
        <div class="logo-icon">🏗️</div>
        <div class="hero-text">
            <h1>ARKIDIGITAL ESTIMATOR PRO</h1>
            <p>Aplikasi Hitung Cepat Kebutuhan Material Bangunan + AI Denah Generator</p>
        </div>
    </div>
    <div class="hero-badge">PREMIUM CALCULATOR</div>
</div>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'hitung' not in st.session_state:
    st.session_state.hitung = False
if 'denah_generated' not in st.session_state:
    st.session_state.denah_generated = False

def proses_perhitungan():
    st.session_state.hitung = True

# ==================== FORM INPUT DATA ====================
st.markdown("### 📐 Input Data Proyek")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    
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
        garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1)
    
    with col3:
        st.markdown("**🚪 Pintu & Jendela**")
        jumlah_pintu_input = st.number_input("Jumlah Pintu", min_value=1, max_value=20, value=6, step=1)
        jumlah_jendela_input = st.number_input("Jumlah Jendela", min_value=0, max_value=20, value=5, step=1)
        
        st.markdown("**🔧 Material & Spek**")
        jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], 
                                   format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton")
        rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"],
                                    format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu")
        jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"],
                                   format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan")
        ukuran_besi = st.selectbox("Ukuran Besi Utama (mm)", [10, 12, 13, 16], index=2, format_func=lambda x: f"Ø{x} mm")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👷 Tenaga Kerja**")
        upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000)
        upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000)
    
    with col2:
        st.markdown("**🏡 Opsional**")
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1)
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1)
    
    submitted = st.form_submit_button("🔨 HITUNG KEBUTUHAN", use_container_width=True, on_click=proses_perhitungan)

# ==================== FUNGSI PERHITUNGAN PRESISI ====================

def hitung_besi(volume_beton, ukuran_besi, panjang_total):
    """Hitung kebutuhan besi utama dan begel"""
    # Besi utama (memanjang)
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    jumlah_besi_utama = 4  # 4 batang per bentang
    panjang_besi_utama = panjang_total * jumlah_besi_utama * lantai
    berat_besi_utama = panjang_besi_utama * berat_per_meter
    batang_besi_utama = math.ceil(panjang_besi_utama / 12)
    
    # Besi begel (cincin) - jarak 15cm
    jarak_begel = 0.15
    jumlah_begel = math.ceil(panjang_total / jarak_begel) * lantai
    panjang_per_begel = 0.6  # (0.15+0.2)*2 = 0.7m untuk sloof 20x25
    panjang_begel = jumlah_begel * panjang_per_begel
    berat_besi_begel = panjang_begel * berat_per_meter
    batang_besi_begel = math.ceil(panjang_begel / 12)
    
    return {
        'utama_kg': round(berat_besi_utama, 1),
        'utama_batang': batang_besi_utama,
        'begel_kg': round(berat_besi_begel, 1),
        'begel_batang': batang_besi_begel,
        'total_kg': round(berat_besi_utama + berat_besi_begel, 1),
        'total_batang': batang_besi_utama + batang_besi_begel
    }


def hitung_cakar_ayam(p, l, lt, ukuran_besi):
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
    
    # Besi untuk cakar ayam
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


def hitung_dinding_presisi(p, l, t, jumlah_pintu, jumlah_jendela):
    """Perhitungan dinding presisi dengan input manual pintu & jendela"""
    panjang_dinding_luar = 2 * (p + l)
    panjang_dinding_internal = (p + l) * 0.8  # Estimasi dinding internal
    total_panjang_dinding = panjang_dinding_luar + panjang_dinding_internal
    luas_kotor = total_panjang_dinding * t
    
    luas_pintu = jumlah_pintu * (0.9 * 2.1)
    luas_jendela = jumlah_jendela * (1.2 * 1.0)
    luas_bersih = luas_kotor - luas_pintu - luas_jendela
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


# ==================== FUNGSI GENERATOR DENAH AI ====================

def generate_denah_prompt(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi, gaya):
    """Membuat prompt untuk AI Gemini"""
    
    gaya_desc = {
        "Modern": "desain modern dengan garis bersih, warna netral, banyak kaca, konsep open space",
        "Minimalis Premium": "desain minimalis mewah dengan material premium, aksen kayu, pencahayaan alami",
        "Ekonomis": "desain sederhana, efisien, layout praktis, biaya konstruksi rendah"
    }
    
    prompt = f"""
    Buatkan sketsa denah rumah 2D profesional dengan spesifikasi:
    
    - Tipe: {gaya}
    - Gaya: {gaya_desc[gaya]}
    - Ukuran tanah: {panjang} m x {lebar} m
    - Jumlah lantai: 1 lantai
    
    Ruangan yang harus ada:
    - {kamar} kamar tidur
    - {km} kamar mandi
    - {ruang_tamu if ruang_tamu>0 else 1} ruang tamu
    - {dapur if dapur>0 else 1} dapur
    - {garasi if garasi>0 else 0} garasi mobil
    
    Fitur yang diminta:
    1. Semua ruangan diberi label (KT1, KT2, KM, Ruang Tamu, Dapur, Garasi)
    2. Sertakan dimensi ukuran (panjang x lebar) setiap ruangan
    3. Tampilkan arah mata angin (Utara)
    4. Sertakan skala (misal 1:100)
    5. Desain layout yang fungsional dan efisien
    6. Sertakan sirkulasi udara dan pencahayaan alami
    
    Format output: DESKRIPSI DETAIL DENAH dalam bentuk teks, mencakup:
    - Tata letak dan posisi setiap ruangan
    - Dimensi setiap ruangan
    - Posisi pintu dan jendela
    - Orientasi bangunan
    - Rekomendasi material fasad sesuai gaya {gaya}
    """
    return prompt


def call_gemini_api(prompt, api_key):
    """Memanggil API Gemini untuk generate deskripsi denah"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
                "topP": 0.95
            }
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
        return None
    except Exception as e:
        st.error(f"Error API: {str(e)}")
        return None


# ==================== PROSES PERHITUNGAN ====================
if st.session_state.hitung:
    
    luas_bangunan = panjang * lebar
    luas_total = luas_bangunan * lantai
    keliling = 2 * (panjang + lebar)
    
    # ========== KOMPONEN PERHITUNGAN ==========
    
    # Pondasi
    vol_pondasi = keliling * 0.7 * 0.8
    pondasi = {
        'volume': round(vol_pondasi, 2),
        'batu_belah': round(vol_pondasi * 1.25, 2),
        'semen': math.ceil(vol_pondasi * 4.8),
        'pasir': round(vol_pondasi * 0.6, 2)
    }
    
    # Sloof
    vol_sloof = keliling * 0.2 * 0.25
    besi_sloof = hitung_besi(vol_sloof, ukuran_besi, keliling)
    sloof = {
        'volume': round(vol_sloof, 2),
        'semen': math.ceil(vol_sloof * 8.5),
        'pasir': round(vol_sloof * 0.7, 2),
        'split': round(vol_sloof * 0.9, 2),
        'besi_utama_kg': besi_sloof['utama_kg'],
        'besi_utama_batang': besi_sloof['utama_batang'],
        'besi_begel_kg': besi_sloof['begel_kg'],
        'besi_begel_batang': besi_sloof['begel_batang'],
        'besi_total_kg': besi_sloof['total_kg']
    }
    
    # Ring Balok
    vol_ring = keliling * 0.15 * 0.2
    besi_ring = hitung_besi(vol_ring, ukuran_besi, keliling)
    ring = {
        'volume': round(vol_ring, 2),
        'semen': math.ceil(vol_ring * 8.5),
        'pasir': round(vol_ring * 0.7, 2),
        'split': round(vol_ring * 0.9, 2),
        'besi_utama_kg': besi_ring['utama_kg'],
        'besi_utama_batang': besi_ring['utama_batang'],
        'besi_begel_kg': besi_ring['begel_kg'],
        'besi_begel_batang': besi_ring['begel_batang'],
        'besi_total_kg': besi_ring['total_kg']
    }
    
    # Kolom Praktis
    jumlah_kolom = math.ceil(keliling / 3) * lantai
    vol_kolom = jumlah_kolom * 0.13 * 0.13 * tinggi
    besi_kolom = hitung_besi(vol_kolom, ukuran_besi, keliling * 0.5)
    kolom = {
        'jumlah': jumlah_kolom,
        'volume': round(vol_kolom, 2),
        'semen': math.ceil(vol_kolom * 9),
        'pasir': round(vol_kolom * 0.72, 2),
        'split': round(vol_kolom * 0.95, 2),
        'besi_utama_kg': besi_kolom['utama_kg'],
        'besi_utama_batang': besi_kolom['utama_batang'],
        'besi_begel_kg': besi_kolom['begel_kg'],
        'besi_begel_batang': besi_kolom['begel_batang'],
        'besi_total_kg': besi_kolom['total_kg']
    }
    
    # Cakar Ayam
    cakar = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)
    
    # Dinding
    dinding = hitung_dinding_presisi(panjang, lebar, tinggi, jumlah_pintu_input, jumlah_jendela_input)
    
    if jenis_bata == "merah":
        jumlah_bata = dinding['bata_merah']
    else:
        jumlah_bata = dinding['bata_hebel']
    
    # Atap
    sudut_atap = 30
    luas_atap = luas_bangunan * (1 / math.cos(math.radians(sudut_atap))) * 1.1
    genteng_per_m2 = {'metal': 1.6, 'tanah': 28, 'beton': 11}
    genteng = math.ceil(luas_atap * genteng_per_m2[jenis_atap])
    
    # Rangka Atap
    if rangka_atap == 'baja':
        rangka = {'jenis': 'Baja Ringan', 'kanal_c': math.ceil(luas_atap * 4.8), 'reng': math.ceil(luas_atap * 2.8)}
    else:
        rangka = {'jenis': 'Kayu', 'kayu_kasau': math.ceil(luas_atap * 6), 'kayu_reng': math.ceil(luas_atap * 4)}
    
    # Komponen lainnya
    plafon = {'luas': round(luas_bangunan, 2), 'gypsum': math.ceil(luas_bangunan * 0.4), 'hollow': math.ceil(luas_bangunan * 0.9)}
    keramik = {'lantai': math.ceil(luas_bangunan * 1.08), 'dinding_km': km * 8}
    listrik = {'titik_lampu': kamar * 3 + km * 2 + ruang_tamu * 3 + dapur * 3 + 2}
    cat = {'total': math.ceil(dinding['luas_bersih'] * 0.14 + luas_bangunan * 0.12)}
    
    # Tenaga Kerja
    tenaga = {
        'tukang': max(2, math.ceil(luas_total / 28)),
        'kenek': max(2, math.ceil(luas_total / 35)),
        'hari': max(30, math.ceil(luas_total / 2.8)),
    }
    tenaga['biaya_tukang'] = tenaga['tukang'] * upah_tukang * tenaga['hari']
    tenaga['biaya_kenek'] = tenaga['kenek'] * upah_kenek * tenaga['hari']
    tenaga['total'] = tenaga['biaya_tukang'] + tenaga['biaya_kenek']
    
    # Total Material
    total_semen = (pondasi['semen'] + sloof['semen'] + ring['semen'] + kolom['semen'] + 
                   cakar['semen'] + dinding['semen_pasang'] + dinding['semen_plester'])
    total_pasir = (pondasi['pasir'] + sloof['pasir'] + ring['pasir'] + kolom['pasir'] + 
                   cakar['pasir'] + dinding['pasir_pasang'] + dinding['pasir_plester'])
    total_split = sloof['split'] + ring['split'] + kolom['split'] + cakar['split']
    total_besi = sloof['besi_total_kg'] + ring['besi_total_kg'] + kolom['besi_total_kg'] + cakar['besi_kg']
    
    # ========== TOTAL BIAYA ==========
    harga_satuan = {
        'semen': 65000, 'pasir': 300000, 'split': 320000, 'batu': 250000,
        'bata_merah': 800, 'bata_hebel': 12000, 'besi': 15000,
        'triplek': 180000, 'kaso': 25000, 'genteng_metal': 25000,
        'genteng_tanah': 5000, 'genteng_beton': 12000, 'keramik': 90000,
        'gypsum': 45000, 'hollow': 35000, 'kabel': 15000, 'saklar': 25000,
        'lampu': 45000, 'mcb': 75000, 'closet': 800000, 'wastafel': 300000,
        'pipa': 50000, 'cat': 35000, 'kitchen_set': 4500000,
        'kanopi': 350000, 'pagar': 850000, 'pintu': 500000, 'jendela': 300000
    }
    
    total_biaya_material = (
        pondasi['batu_belah'] * harga_satuan['batu'] +
        pondasi['semen'] * harga_satuan['semen'] +
        (sloof['semen'] + ring['semen'] + kolom['semen'] + cakar['semen']) * harga_satuan['semen'] +
        (sloof['pasir'] + ring['pasir'] + kolom['pasir'] + cakar['pasir']) * harga_satuan['pasir'] +
        (sloof['split'] + ring['split'] + kolom['split'] + cakar['split']) * harga_satuan['split'] +
        total_besi * harga_satuan['besi'] +
        jumlah_bata * (harga_satuan['bata_merah'] if jenis_bata == 'merah' else harga_satuan['bata_hebel']) +
        dinding['semen_pasang'] * harga_satuan['semen'] +
        dinding['semen_plester'] * harga_satuan['semen'] +
        genteng * (harga_satuan[f'genteng_{jenis_atap}']) +
        keramik['lantai'] * harga_satuan['keramik'] +
        plafon['gypsum'] * harga_satuan['gypsum'] +
        listrik['titik_lampu'] * (harga_satuan['lampu'] + harga_satuan['saklar'] + harga_satuan['kabel']*2) +
        jumlah_pintu_input * harga_satuan['pintu'] +
        jumlah_jendela_input * harga_satuan['jendela'] +
        cat['total'] * harga_satuan['cat'] +
        (4500000 if dapur > 0 else 0) +
        kanopi * harga_satuan['kanopi'] +
        pagar * harga_satuan['pagar']
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
            <p style="color:#475569; font-size:13px;">🏠 Luas Bangunan</p>
            <h3 style="color:#1e40af; font-size:28px;">{luas_bangunan} m²</h3>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color:#475569; font-size:13px;">🦶 Cakar Ayam</p>
            <h3 style="color:#1e40af; font-size:28px;">{cakar['jumlah']} titik</h3>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color:#475569; font-size:13px;">📅 Estimasi Waktu</p>
            <h3 style="color:#1e40af; font-size:28px;">{tenaga['hari']} hari</h3>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color:#475569; font-size:13px;">👷 Tenaga Kerja</p>
            <h3 style="color:#1e40af; font-size:24px;">{tenaga['tukang']} Tk + {tenaga['kenek']} Kn</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # ============ KOMPONEN BESI DETAIL ============
    st.markdown("### 🦾 Detail Kebutuhan Besi (Per 12m Batang)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">📊</span> <span class="component-title">Sloof</span></div>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Besi Utama Ø{ukuran_besi}</div><div class="detail-value">{sloof['besi_utama_kg']} kg ({sloof['besi_utama_batang']} btg)</div></div>
                    <div class="detail-item"><div class="detail-label">Besi Begel Ø8</div><div class="detail-value">{sloof['besi_begel_kg']} kg ({sloof['besi_begel_batang']} btg)</div></div>
                    <div class="detail-item"><div class="detail-label">Total Sloof</div><div class="detail-value">{sloof['besi_total_kg']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="component-card">
            <div class="component-header">
                <div><span class="component-num">📊</span> <span class="component-title">Ring Balok</span></div>
            </div>
            <div class="component-body">
                <div class="detail-grid">
                    <div class="detail-item"><div class="detail-label">Besi Utama Ø{ukuran_besi}</div><div class="detail-value">{ring['besi_utama_kg']} kg ({ring['besi_utama_batang']} btg)</div></div>
                    <div class="detail-item"><div class="detail-label">Besi Begel Ø8</div><div class="detail-value">{ring['besi_begel_kg']} kg ({ring['besi_begel_batang']} btg)</div></div>
                    <div class="detail-item"><div class="detail-label">Total Ring</div><div class="detail-value">{ring['besi_total_kg']} kg</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Total Besi Keseluruhan
    st.markdown(f"""
    <div class="component-card">
        <div class="component-header">
            <div><span class="component-num">📊</span> <span class="component-title">Total Kebutuhan Besi Seluruh Struktur</span></div>
        </div>
        <div class="component-body">
            <div class="detail-grid">
                <div class="detail-item"><div class="detail-label">Total Besi (kg)</div><div class="detail-value">{total_besi} kg</div></div>
                <div class="detail-item"><div class="detail-label">Estimasi Batang @12m</div><div class="detail-value">{math.ceil(total_besi / (ukuran_besi*ukuran_besi/162 * 12))} batang</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============ GENERATOR DENAH AI ============
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🏠 AI Denah Generator")
    st.markdown("Generate 3 pilihan denah rumah berdasarkan data input Anda")
    
    # API Key input
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password", 
                            placeholder="Masukkan API Key untuk generate denah")
    st.caption("Dapatkan API Key gratis di [Google AI Studio](https://makersuite.google.com/app/apikey)")
    
    if api_key:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏘️ Modern", use_container_width=True):
                with st.spinner("Mengenerate denah gaya Modern..."):
                    prompt = generate_denah_prompt(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi, "Modern")
                    result = call_gemini_api(prompt, api_key)
                    if result:
                        st.session_state.denah_modern = result
                        st.session_state.denah_generated = True
        
        with col2:
            if st.button("✨ Minimalis Premium", use_container_width=True):
                with st.spinner("Mengenerate denah gaya Minimalis Premium..."):
                    prompt = generate_denah_prompt(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi, "Minimalis Premium")
                    result = call_gemini_api(prompt, api_key)
                    if result:
                        st.session_state.denah_premium = result
                        st.session_state.denah_generated = True
        
        with col3:
            if st.button("💰 Ekonomis", use_container_width=True):
                with st.spinner("Mengenerate denah gaya Ekonomis..."):
                    prompt = generate_denah_prompt(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi, "Ekonomis")
                    result = call_gemini_api(prompt, api_key)
                    if result:
                        st.session_state.denah_ekonomis = result
                        st.session_state.denah_generated = True
        
        # Tampilkan hasil denah
        if st.session_state.get('denah_generated', False):
            st.markdown("---")
            st.markdown("### 🎨 Hasil Generate Denah")
            
            tabs = st.tabs(["🏘️ Modern", "✨ Minimalis Premium", "💰 Ekonomis"])
            
            with tabs[0]:
                if 'denah_modern' in st.session_state:
                    st.markdown(f"""
                    <div class="denah-card">
                        <h4>🏘️ Denah Gaya Modern</h4>
                        <div style="text-align: left; background: white; padding: 20px; border-radius: 12px; margin-top: 10px;">
                            {st.session_state.denah_modern.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tabs[1]:
                if 'denah_premium' in st.session_state:
                    st.markdown(f"""
                    <div class="denah-card">
                        <h4>✨ Denah Gaya Minimalis Premium</h4>
                        <div style="text-align: left; background: white; padding: 20px; border-radius: 12px; margin-top: 10px;">
                            {st.session_state.denah_premium.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tabs[2]:
                if 'denah_ekonomis' in st.session_state:
                    st.markdown(f"""
                    <div class="denah-card">
                        <h4>💰 Denah Gaya Ekonomis</h4>
                        <div style="text-align: left; background: white; padding: 20px; border-radius: 12px; margin-top: 10px;">
                            {st.session_state.denah_ekonomis.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        st.info("🔑 Masukkan Google Gemini API Key untuk mengenerate 3 pilihan denah rumah sesuai data input Anda")
    
    # ============ RAB & TOTAL ============
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 💰 Rencana Anggaran Biaya")
    
    # Ringkasan Material
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
    
    st.markdown(f"""
    <div class="grand-total">
        <p style="color: #dbeafe; font-size: 14px;">GRAND TOTAL RENCANA ANGGARAN BIAYA (RAB)</p>
        <h2 style="color: white; font-size: 42px;">Rp {total_biaya:,.0f}</h2>
        <p style="color: #bfdbfe; margin-top: 10px;">*Sudah termasuk material + upah tukang + overhead</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Export
    st.markdown("---")
    st.markdown("### 📄 Export Data")
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'dimensi': {'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai},
        'ruangan': {'kamar': kamar, 'km': km, 'dapur': dapur, 'garasi': garasi},
        'pintu_jendela': {'pintu': jumlah_pintu_input, 'jendela': jumlah_jendela_input},
        'material': {'semen': total_semen, 'pasir': total_pasir, 'split': total_split, 'besi': total_besi, 'bata': jumlah_bata},
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
            'Luas(m²)': luas_bangunan, 'Semen': total_semen,
            'Pasir(m³)': total_pasir, 'Besi(kg)': total_besi,
            'Total Biaya': total_biaya
        }])
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"estimator_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

else:
    st.info("👆 Silakan isi data proyek di atas, lalu klik tombol **HITUNG KEBUTUHAN** untuk melihat hasil perhitungan.")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px;">
    <hr style="border-color: #e2e8f0;">
    <p style="color: #94a3b8;">🏗️ ARKIDIGITAL ESTIMATOR PRO | Presisi 20 Komponen + AI Denah Generator | © 2024</p>
    <p style="color: #cbd5e1; font-size: 12px;">Aplikasi hitung kebutuhan material + generate denah dengan AI</p>
</div>
""", unsafe_allow_html=True)
