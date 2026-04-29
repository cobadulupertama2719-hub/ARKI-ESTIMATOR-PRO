# app.py - ARKIDIGITAL ESTIMATOR PRO (Login Wajib + Export PDF)

import streamlit as st
import math
import pandas as pd
from datetime import datetime
import json
import requests
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import base64

# ==================== KONFIGURASI ====================
st.set_page_config(
    page_title="ARKIDIGITAL ESTIMATOR PRO",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'hitung' not in st.session_state:
    st.session_state.hitung = False
if 'denah_modern' not in st.session_state:
    st.session_state.denah_modern = None
if 'denah_premium' not in st.session_state:
    st.session_state.denah_premium = None
if 'denah_ekonomis' not in st.session_state:
    st.session_state.denah_ekonomis = None

# ==================== MODERN CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #ffffff !important; }
    
    .hero-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        padding: 16px 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 15px;
    }
    .hero-left { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
    .logo-icon { font-size: 36px; }
    .hero-text h1 { color: white !important; margin: 0; font-size: 22px; font-weight: 700; }
    .hero-text p { color: #dbeafe; margin: 4px 0 0 0; font-size: 11px; }
    .hero-badge { background: rgba(255,255,255,0.2); padding: 6px 14px; border-radius: 30px; color: white; font-size: 11px; }
    
    .login-card {
        max-width: 420px;
        margin: 80px auto;
        background: white;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 20px 35px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .login-icon { font-size: 64px; margin-bottom: 16px; }
    
    .metric-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        border: 1px solid #bfdbfe;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15); }
    
    .component-card {
        background: #ffffff;
        border-radius: 14px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }
    .component-header {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 12px 16px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .component-num {
        background: #1e40af;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 12px;
    }
    .component-title { font-weight: 700; color: #1e293b; font-size: 14px; }
    .component-body { padding: 14px 16px; background: white; }
    
    .detail-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
    .detail-item { background: #f8fafc; padding: 8px 12px; border-radius: 10px; border-left: 3px solid #2563eb; }
    .detail-label { font-size: 10px; color: #64748b; text-transform: uppercase; }
    .detail-value { font-size: 14px; font-weight: 700; color: #1e293b; }
    
    .custom-divider { height: 2px; background: linear-gradient(90deg, #2563eb, #93c5fd, #2563eb); margin: 20px 0; border-radius: 2px; }
    
    .grand-total {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin-top: 24px;
    }
    
    .denah-card {
        background: #f8fafc;
        border-radius: 14px;
        padding: 16px;
        text-align: left;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
    .denah-content { background: white; padding: 16px; border-radius: 10px; font-size: 13px; line-height: 1.6; }
    
    .stButton button {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
    }
    
    @media (max-width: 768px) {
        .hero-header { flex-direction: column; text-align: center; }
        .detail-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNGSI LOGIN ====================
def do_login():
    if st.session_state.username == "Arkidigital" and st.session_state.password == "kontraktorarki":
        st.session_state.logged_in = True
    else:
        st.error("Username atau password salah!")

def do_logout():
    st.session_state.logged_in = False
    st.session_state.hitung = False
    st.rerun()

# ==================== FUNGSI GENERATE PDF ====================
def generate_pdf_report(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1e40af'), alignment=1, spaceAfter=20)
    story.append(Paragraph("ARKIDIGITAL ESTIMATOR PRO", title_style))
    story.append(Paragraph(f"Laporan Perhitungan RAB - {data['tanggal']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Data Proyek
    story.append(Paragraph("<b>DATA PROYEK</b>", styles['Heading2']))
    proyek_data = [
        ["Parameter", "Nilai"],
        ["Panjang", f"{data['panjang']} m"],
        ["Lebar", f"{data['lebar']} m"],
        ["Tinggi Dinding", f"{data['tinggi']} m"],
        ["Jumlah Lantai", f"{data['lantai']}"],
        ["Luas Bangunan", f"{data['luas_bangunan']} m²"],
        ["Kamar Tidur", f"{data['kamar']}"],
        ["Kamar Mandi", f"{data['km']}"],
        ["Dapur", f"{data['dapur']}"],
        ["Garasi", f"{data['garasi']}"],
    ]
    table = Table(proyek_data, colWidths=[4*cm, 8*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Ringkasan Material
    story.append(Paragraph("<b>RINGKASAN MATERIAL</b>", styles['Heading2']))
    material_data = [
        ["Material", "Total"],
        ["Semen", f"{data['total_semen']} sak"],
        ["Pasir", f"{data['total_pasir']} m³"],
        ["Split", f"{data['total_split']} m³"],
        ["Besi", f"{data['total_besi']} kg"],
        ["Bata", f"{data['total_bata']:,} pcs"],
    ]
    table2 = Table(material_data, colWidths=[6*cm, 6*cm])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table2)
    story.append(Spacer(1, 20))
    
    # Tenaga Kerja
    story.append(Paragraph("<b>TENAGA KERJA</b>", styles['Heading2']))
    tenaga_data = [
        ["Parameter", "Nilai"],
        ["Tukang", f"{data['tukang']} orang"],
        ["Kenek", f"{data['kenek']} orang"],
        ["Estimasi Waktu", f"{data['hari']} hari"],
        ["Biaya Upah", f"Rp {data['biaya_upah']:,.0f}"],
    ]
    table3 = Table(tenaga_data, colWidths=[6*cm, 6*cm])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table3)
    story.append(Spacer(1, 20))
    
    # Total Biaya
    story.append(Paragraph("<b>TOTAL RAB</b>", styles['Heading2']))
    total_style = ParagraphStyle('Total', parent=styles['Normal'], fontSize=16, textColor=colors.HexColor('#1e40af'), alignment=1, spaceAfter=10)
    story.append(Paragraph(f"<b>Rp {data['total_biaya']:,.0f}</b>", total_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==================== FUNGSI PERHITUNGAN ====================
def hitung_besi(panjang_total, ukuran_besi, lantai, jenis="sloof"):
    berat_per_meter = (ukuran_besi * ukuran_besi) / 162
    jumlah_besi_utama = 4
    faktor = 0.5 if jenis == "kolom" else 1
    panjang_besi_utama = panjang_total * jumlah_besi_utama * lantai * faktor
    berat_besi_utama = panjang_besi_utama * berat_per_meter
    batang_besi_utama = math.ceil(panjang_besi_utama / 12)
    jarak_begel = 0.15
    jumlah_begel = math.ceil(panjang_total / jarak_begel) * lantai
    panjang_per_begel = 0.7 if jenis == "sloof" else 0.6 if jenis == "ring" else 0.5
    panjang_begel = jumlah_begel * panjang_per_begel
    berat_besi_begel = panjang_begel * berat_per_meter
    batang_besi_begel = math.ceil(panjang_begel / 12)
    return {
        'utama_kg': round(berat_besi_utama, 1),
        'utama_batang': batang_besi_utama,
        'begel_kg': round(berat_besi_begel, 1),
        'begel_batang': batang_besi_begel,
        'total_kg': round(berat_besi_utama + berat_besi_begel, 1)
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
    panjang_dinding_luar = 2 * (p + l)
    panjang_dinding_internal = (p + l) * 0.8
    total_panjang_dinding = panjang_dinding_luar + panjang_dinding_internal
    luas_kotor = total_panjang_dinding * t
    luas_pintu = jumlah_pintu * (0.9 * 2.1)
    luas_jendela = jumlah_jendela * (1.2 * 1.0)
    luas_bersih = max(luas_kotor - luas_pintu - luas_jendela, luas_kotor * 0.6)
    return {
        'luas_kotor': round(luas_kotor, 2),
        'luas_bersih': round(luas_bersih, 2),
        'jumlah_pintu': jumlah_pintu,
        'jumlah_jendela': jumlah_jendela,
        'bata_merah': math.ceil(luas_bersih * 70),
        'bata_hebel': math.ceil(luas_bersih * 8.5),
        'semen_pasang': math.ceil(luas_bersih * 0.32),
        'pasir_pasang': round(luas_bersih * 0.045, 2),
        'semen_plester': math.ceil(luas_bersih * 2 * 0.22),
        'pasir_plester': round(luas_bersih * 2 * 0.028, 2),
        'acian': math.ceil(luas_bersih * 2 * 0.18)
    }

def generate_denah_prompt(panjang, lebar, kamar, km, ruang_tamu, dapur, garasi, gaya):
    gaya_desc = {
        "Modern": "desain modern dengan garis bersih, warna netral, banyak kaca, konsep open space",
        "Minimalis Premium": "desain minimalis mewah dengan material premium, aksen kayu, pencahayaan alami",
        "Ekonomis": "desain sederhana, efisien, layout praktis, biaya konstruksi rendah"
    }
    return f"""
    Buatkan sketsa denah rumah 2D dengan spesifikasi:
    Gaya: {gaya} - {gaya_desc[gaya]}
    Ukuran tanah: {panjang} m x {lebar} m
    Jumlah lantai: 1 lantai
    Ruangan: {kamar} KT, {km} KM, {ruang_tamu} RT, {dapur} Dapur, {garasi} Garasi
    Output: DESKRIPSI DETAIL dalam bahasa Indonesia mencakup tata letak, dimensi ruangan, dan posisi pintu jendela
    """

def call_gemini_api(prompt, api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}}
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
        return None
    except Exception as e:
        return None

# ==================== HALAMAN LOGIN ====================
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-card">
        <div class="login-icon">🏗️</div>
        <h2 style="color: #1e40af;">ARKIDIGITAL</h2>
        <h3 style="color: #1e293b; margin-bottom: 24px;">ESTIMATOR PRO</h3>
        <p style="color: #64748b; margin-bottom: 24px;">Aplikasi Hitung Kebutuhan Material Bangunan<br>20 Komponen Presisi + AI Denah Generator</p>
    """, unsafe_allow_html=True)
    
    st.text_input("Username", key="username", placeholder="Masukkan username")
    st.text_input("Password", type="password", key="password", placeholder="Masukkan password")
    st.button("🔓 Login", on_click=do_login, use_container_width=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #94a3b8; font-size: 12px;">Demo: Username: Arkidigital | Password: kontraktorarki</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==================== HEADER SETELAH LOGIN ====================
st.markdown(f"""
<div class="hero-header">
    <div class="hero-left">
        <div class="logo-icon">🏗️</div>
        <div class="hero-text">
            <h1>ARKIDIGITAL ESTIMATOR PRO</h1>
            <p>Aplikasi Hitung Cepat Kebutuhan Material Bangunan | 20 Komponen Presisi + AI Denah Generator</p>
        </div>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
        <div class="hero-badge">✨ AKTIF</div>
        <button onclick="location.href='?logout=true'" style="background: rgba(255,255,255,0.2); border: none; padding: 6px 14px; border-radius: 30px; color: white; cursor: pointer;">🚪 Logout</button>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🚪 Logout", key="logout_btn"):
    do_logout()

# ==================== FORM INPUT DATA ====================
st.markdown("### 📐 Input Data Proyek")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏠 Dimensi Bangunan**")
        panjang = st.number_input("Panjang (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5, key="p")
        lebar = st.number_input("Lebar (m)", min_value=5.0, max_value=50.0, value=8.0, step=0.5, key="l")
        tinggi = st.number_input("Tinggi Dinding (m)", min_value=2.5, max_value=5.0, value=3.5, step=0.1, key="t")
        lantai = st.select_slider("Jumlah Lantai", options=[1, 2, 3], value=1, key="lt")
    
    with col2:
        st.markdown("**🛏️ Ruangan**")
        kamar = st.number_input("Kamar Tidur", min_value=1, max_value=10, value=3, step=1, key="kamar")
        km = st.number_input("Kamar Mandi", min_value=1, max_value=5, value=2, step=1, key="km")
        ruang_tamu = st.number_input("Ruang Tamu", min_value=0, max_value=3, value=1, step=1, key="rt")
        dapur = st.number_input("Dapur", min_value=0, max_value=2, value=1, step=1, key="dapur")
        garasi = st.number_input("Garasi", min_value=0, max_value=2, value=0, step=1, key="garasi")
    
    with col3:
        st.markdown("**🚪 Pintu & Jendela**")
        jumlah_pintu_input = st.number_input("Jumlah Pintu", min_value=1, max_value=20, value=6, step=1, key="pintu")
        jumlah_jendela_input = st.number_input("Jumlah Jendela", min_value=0, max_value=20, value=5, step=1, key="jendela")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔧 Material & Spek**")
        jenis_atap = st.selectbox("Jenis Atap", ["metal", "tanah", "beton"], format_func=lambda x: "Metal" if x=="metal" else "Tanah" if x=="tanah" else "Beton", key="atap")
        rangka_atap = st.selectbox("Rangka Atap", ["baja", "kayu"], format_func=lambda x: "Baja Ringan" if x=="baja" else "Kayu", key="rangka")
        jenis_bata = st.selectbox("Jenis Bata", ["merah", "hebel"], format_func=lambda x: "Bata Merah" if x=="merah" else "Bata Ringan", key="bata")
        ukuran_besi = st.selectbox("Ukuran Besi Utama (mm)", [10, 12, 13, 16], index=2, format_func=lambda x: f"Ø{x} mm", key="besi")
    
    with col2:
        st.markdown("**👷 Tenaga Kerja**")
        upah_tukang = st.number_input("Upah Tukang/Hari", min_value=50000, max_value=500000, value=150000, step=10000, key="ut")
        upah_kenek = st.number_input("Upah Kenek/Hari", min_value=50000, max_value=500000, value=100000, step=10000, key="uk")
    
    with col3:
        st.markdown("**🏡 Opsional**")
        kanopi = st.number_input("Kanopi (m²)", min_value=0, max_value=100, value=0, step=1, key="kanopi")
        pagar = st.number_input("Pagar (m)", min_value=0, max_value=100, value=0, step=1, key="pagar")
    
    submitted = st.form_submit_button("🔨 HITUNG KEBUTUHAN", use_container_width=True)

if submitted:
    st.session_state.hitung = True

# ==================== PROSES PERHITUNGAN ====================
if st.session_state.hitung:
    
    luas_bangunan = panjang * lebar
    luas_total = luas_bangunan * lantai
    keliling = 2 * (panjang + lebar)
    
    # Komponen 1: Pondasi
    vol_pondasi = keliling * 0.7 * 0.8
    komponen1 = {'volume': round(vol_pondasi, 2), 'batu_belah': round(vol_pondasi * 1.25, 2), 'semen': math.ceil(vol_pondasi * 4.8), 'pasir': round(vol_pondasi * 0.6, 2)}
    
    # Komponen 2: Sloof
    vol_sloof = keliling * 0.2 * 0.25
    besi_sloof = hitung_besi(keliling, ukuran_besi, lantai, "sloof")
    komponen2 = {'volume': round(vol_sloof, 2), 'semen': math.ceil(vol_sloof * 8.5), 'pasir': round(vol_sloof * 0.7, 2), 'split': round(vol_sloof * 0.9, 2), 'besi_utama_kg': besi_sloof['utama_kg'], 'besi_utama_batang': besi_sloof['utama_batang'], 'besi_begel_kg': besi_sloof['begel_kg'], 'besi_begel_batang': besi_sloof['begel_batang']}
    
    # Komponen 3: Ring Balok
    vol_ring = keliling * 0.15 * 0.2
    besi_ring = hitung_besi(keliling, ukuran_besi, lantai, "ring")
    komponen3 = {'volume': round(vol_ring, 2), 'semen': math.ceil(vol_ring * 8.5), 'pasir': round(vol_ring * 0.7, 2), 'split': round(vol_ring * 0.9, 2), 'besi_utama_kg': besi_ring['utama_kg'], 'besi_utama_batang': besi_ring['utama_batang'], 'besi_begel_kg': besi_ring['begel_kg'], 'besi_begel_batang': besi_ring['begel_batang']}
    
    # Komponen 4: Kolom
    jumlah_kolom = math.ceil(keliling / 3) * lantai
    vol_kolom = jumlah_kolom * 0.13 * 0.13 * tinggi
    besi_kolom = hitung_besi(keliling, ukuran_besi, lantai, "kolom")
    komponen4 = {'jumlah': jumlah_kolom, 'volume': round(vol_kolom, 2), 'semen': math.ceil(vol_kolom * 9), 'pasir': round(vol_kolom * 0.72, 2), 'split': round(vol_kolom * 0.95, 2), 'besi_utama_kg': besi_kolom['utama_kg'], 'besi_utama_batang': besi_kolom['utama_batang'], 'besi_begel_kg': besi_kolom['begel_kg'], 'besi_begel_batang': besi_kolom['begel_batang']}
    
    # Komponen 5: Bekisting
    luas_bekisting = (vol_sloof * 8) + (vol_ring * 7) + (vol_kolom * 10)
    komponen5 = {'luas': round(luas_bekisting, 2), 'triplek': math.ceil(luas_bekisting * 0.4), 'kaso': math.ceil(luas_bekisting * 2.8), 'paku': round(luas_bekisting * 0.22, 1)}
    
    # Komponen 6: Cakar Ayam
    komponen6 = hitung_cakar_ayam(panjang, lebar, lantai, ukuran_besi)
    
    # Komponen 7: Dinding
    komponen7 = hitung_dinding_presisi(panjang, lebar, tinggi, jumlah_pintu_input, jumlah_jendela_input)
    jumlah_bata = komponen7['bata_merah'] if jenis_bata == "merah" else komponen7['bata_hebel']
    
    # Komponen 8: Plesteran
    komponen8 = {'luas_plester': round(komponen7['luas_bersih'] * 2, 2), 'semen_plester': komponen7['semen_plester'], 'semen_acian': komponen7['acian'], 'pasir_plester': komponen7['pasir_plester']}
    
    # Komponen 9: Atap
    sudut_atap = 30
    luas_atap = luas_bangunan * (1 / math.cos(math.radians(sudut_atap))) * 1.1
    genteng_per_m2 = {'metal': 1.6, 'tanah': 28, 'beton': 11}
    komponen9 = {'luas': round(luas_atap, 2), 'genteng': math.ceil(luas_atap * genteng_per_m2[jenis_atap]), 'jenis': jenis_atap}
    
    # Komponen 10: Rangka Atap
    if rangka_atap == 'baja':
        komponen10 = {'jenis': 'Baja Ringan', 'kanal_c': math.ceil(luas_atap * 4.8), 'reng': math.ceil(luas_atap * 2.8)}
    else:
        komponen10 = {'jenis': 'Kayu', 'kayu_kasau': math.ceil(luas_atap * 6), 'kayu_reng': math.ceil(luas_atap * 4)}
    
    # Komponen 11: Plafon
    komponen11 = {'luas': round(luas_bangunan, 2), 'gypsum': math.ceil(luas_bangunan * 0.4), 'hollow': math.ceil(luas_bangunan * 0.9), 'list': math.ceil(keliling * 1.3)}
    
    # Komponen 12: Keramik Lantai
    komponen12 = {'lantai': math.ceil(luas_bangunan * 1.08), 'dinding_km': km * 8, 'semen': math.ceil((luas_bangunan + km*8) * 0.35), 'pasir': round((luas_bangunan + km*8) * 0.035, 2)}
    
    # Komponen 13: Keramik Dinding KM
    komponen13 = {'luas': km * 8, 'semen': math.ceil(km * 8 * 0.25), 'pasir': round(km * 8 * 0.025, 2)}
    
    # Komponen 14: Listrik
    titik_listrik = kamar * 3 + km * 2 + ruang_tamu * 3 + dapur * 3 + garasi * 1 + 2
    komponen14 = {'titik_lampu': titik_listrik, 'saklar': math.ceil(titik_listrik * 0.6), 'stop_kontak': math.ceil(titik_listrik * 0.5), 'kabel_meter': titik_listrik * 12, 'mcb': 6 if lantai >= 2 else 4}
    
    # Komponen 15: Sanitasi
    komponen15 = {'closet': km, 'wastafel': km, 'pipa_air_bersih': km * 12, 'pipa_air_kotor': km * 8, 'septictank': 1 if km > 0 else 0}
    
    # Komponen 16: Pintu
    komponen16 = {'jumlah': jumlah_pintu_input, 'estimasi_biaya': jumlah_pintu_input * 500000}
    
    # Komponen 17: Jendela
    komponen17 = {'jumlah': jumlah_jendela_input, 'estimasi_biaya': jumlah_jendela_input * 300000}
    
    # Komponen 18: Cat
    komponen18 = {'tembok': math.ceil(komponen7['luas_bersih'] * 0.14), 'plafon': math.ceil(luas_bangunan * 0.12), 'total': math.ceil(komponen7['luas_bersih'] * 0.14 + luas_bangunan * 0.12)}
    
    # Komponen 19: Dapur
    komponen19 = {'tersedia': dapur > 0, 'kitchen_set': 3000000 if dapur > 0 else 0}
    
    # Komponen 20: Tenaga Kerja
    komponen20 = {'tukang': max(2, math.ceil(luas_total / 28)), 'kenek': max(2, math.ceil(luas_total / 35)), 'hari': max(30, math.ceil(luas_total / 2.8))}
    komponen20['biaya_tukang'] = komponen20['tukang'] * upah_tukang * komponen20['hari']
    komponen20['biaya_kenek'] = komponen20['kenek'] * upah_kenek * komponen20['hari']
    komponen20['total_upah'] = komponen20['biaya_tukang'] + komponen20['biaya_kenek']
    
    # Total Material
    total_semen = (komponen1['semen'] + komponen2['semen'] + komponen3['semen'] + komponen4['semen'] + komponen6['semen'] + komponen7['semen_pasang'] + komponen7['semen_plester'] + komponen12['semen'])
    total_pasir = (komponen1['pasir'] + komponen2['pasir'] + komponen3['pasir'] + komponen4['pasir'] + komponen6['pasir'] + komponen7['pasir_pasang'] + komponen7['pasir_plester'] + komponen12['pasir'])
    total_split = komponen2['split'] + komponen3['split'] + komponen4['split'] + komponen6['split']
    total_besi = besi_sloof['total_kg'] + besi_ring['total_kg'] + besi_kolom['total_kg'] + komponen6['besi_kg']
    
    # Total Biaya
    harga = {'semen': 65000, 'pasir': 300000, 'split': 320000, 'batu': 250000, 'bata_merah': 800, 'bata_hebel': 12000, 'besi': 15000, 'triplek': 180000, 'kaso': 25000, 'genteng_metal': 25000, 'genteng_tanah': 5000, 'genteng_beton': 12000, 'keramik': 90000, 'gypsum': 45000, 'hollow': 35000, 'list': 8000, 'kabel': 15000, 'saklar': 25000, 'lampu': 45000, 'mcb': 75000, 'closet': 800000, 'wastafel': 300000, 'pipa': 50000, 'cat': 35000, 'pintu': 500000, 'jendela': 300000, 'kitchen_set': 3000000, 'kanopi': 350000, 'pagar': 850000}
    
    total_biaya = (
        komponen1['batu_belah'] * harga['batu'] + komponen1['semen'] * harga['semen'] +
        (komponen2['semen'] + komponen3['semen'] + komponen4['semen'] + komponen6['semen']) * harga['semen'] +
        (komponen2['pasir'] + komponen3['pasir'] + komponen4['pasir'] + komponen6['pasir']) * harga['pasir'] +
        (komponen2['split'] + komponen3['split'] + komponen4['split'] + komponen6['split']) * harga['split'] +
        total_besi * harga['besi'] + komponen5['triplek'] * harga['triplek'] +
        jumlah_bata * (harga['bata_merah'] if jenis_bata == 'merah' else harga['bata_hebel']) +
        komponen7['semen_pasang'] * harga['semen'] + komponen7['semen_plester'] * harga['semen'] +
        komponen9['genteng'] * harga[f'genteng_{jenis_atap}'] + komponen12['lantai'] * harga['keramik'] +
        komponen11['gypsum'] * harga['gypsum'] + komponen14['titik_lampu'] * (harga['lampu'] + harga['saklar'] + harga['kabel']*2) +
        komponen16['estimasi_biaya'] + komponen17['estimasi_biaya'] + komponen18['total'] * harga['cat'] +
        (komponen19['kitchen_set'] if dapur > 0 else 0) + kanopi * harga['kanopi'] + pagar * harga['pagar'] + komponen20['total_upah']
    )
    
    # TAMPILAN HASIL
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Ringkasan Proyek")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><p style="color:#475569;">🏠 Luas Bangunan</p><h3 style="color:#1e40af;">{luas_bangunan} m²</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><p style="color:#475569;">🦶 Cakar Ayam</p><h3 style="color:#1e40af;">{komponen6["jumlah"]} titik</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><p style="color:#475569;">📅 Estimasi Waktu</p><h3 style="color:#1e40af;">{komponen20["hari"]} hari</h3></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><p style="color:#475569;">💰 Total RAB</p><h3 style="color:#1e40af;">Rp {total_biaya/1000000:.1f} Jt</h3></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # 20 KOMPONEN
    st.markdown("### 📋 Rincian 20 Komponen")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown(f"""
        <div class="component-card"><div class="component-header"><div><span class="component-num">1</span> <span class="component-title">Pondasi Batu Kali</span></div>🏗️</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{komponen1['volume']} m³</div></div><div class="detail-item"><div class="detail-label">Batu Belah</div><div class="detail-value">{komponen1['batu_belah']} m³</div></div><div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{komponen1['semen']} sak</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">2</span> <span class="component-title">Sloof</span></div>📏</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{komponen2['volume']} m³</div></div><div class="detail-item"><div class="detail-label">Besi Utama</div><div class="detail-value">{komponen2['besi_utama_kg']} kg ({komponen2['besi_utama_batang']} btg)</div></div><div class="detail-item"><div class="detail-label">Besi Begel</div><div class="detail-value">{komponen2['besi_begel_kg']} kg ({komponen2['besi_begel_batang']} btg)</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">3</span> <span class="component-title">Ring Balok</span></div>📏</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{komponen3['volume']} m³</div></div><div class="detail-item"><div class="detail-label">Besi Utama</div><div class="detail-value">{komponen3['besi_utama_kg']} kg</div></div><div class="detail-item"><div class="detail-label">Besi Begel</div><div class="detail-value">{komponen3['besi_begel_kg']} kg</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">4</span> <span class="component-title">Kolom Praktis</span></div>🏛️</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{komponen4['jumlah']} bh</div></div><div class="detail-item"><div class="detail-label">Volume</div><div class="detail-value">{komponen4['volume']} m³</div></div><div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{komponen4['besi_utama_kg'] + komponen4['besi_begel_kg']} kg</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">5</span> <span class="component-title">Bekisting</span></div>🪵</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{komponen5['luas']} m²</div></div><div class="detail-item"><div class="detail-label">Triplek</div><div class="detail-value">{komponen5['triplek']} lbr</div></div><div class="detail-item"><div class="detail-label">Kaso</div><div class="detail-value">{komponen5['kaso']} btg</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">6</span> <span class="component-title">Cakar Ayam</span></div>🦶</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{komponen6['jumlah']} titik</div></div><div class="detail-item"><div class="detail-label">Ukuran</div><div class="detail-value">{komponen6['ukuran_cm']:.0f}x{komponen6['ukuran_cm']:.0f} cm</div></div><div class="detail-item"><div class="detail-label">Besi</div><div class="detail-value">{komponen6['besi_kg']} kg</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">7</span> <span class="component-title">Dinding Bata</span></div>🧱</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas Bersih</div><div class="detail-value">{komponen7['luas_bersih']} m²</div></div><div class="detail-item"><div class="detail-label">Bata</div><div class="detail-value">{jumlah_bata:,} pcs</div></div><div class="detail-item"><div class="detail-label">Pintu/Jendela</div><div class="detail-value">{komponen7['jumlah_pintu']}/{komponen7['jumlah_jendela']}</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">8</span> <span class="component-title">Plesteran</span></div>🧱</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas Plester</div><div class="detail-value">{komponen8['luas_plester']} m²</div></div><div class="detail-item"><div class="detail-label">Semen Plester</div><div class="detail-value">{komponen8['semen_plester']} sak</div></div><div class="detail-item"><div class="detail-label">Semen Acian</div><div class="detail-value">{komponen8['semen_acian']} sak</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">9</span> <span class="component-title">Atap</span></div>🏠</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas Atap</div><div class="detail-value">{komponen9['luas']} m²</div></div><div class="detail-item"><div class="detail-label">Genteng</div><div class="detail-value">{komponen9['genteng']:,} pcs</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">10</span> <span class="component-title">Rangka Atap</span></div>🔧</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Jenis</div><div class="detail-value">{komponen10['jenis']}</div></div></div></div></div>
        """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown(f"""
        <div class="component-card"><div class="component-header"><div><span class="component-num">11</span> <span class="component-title">Plafon</span></div>✨</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{komponen11['luas']} m²</div></div><div class="detail-item"><div class="detail-label">Gypsum</div><div class="detail-value">{komponen11['gypsum']} lbr</div></div><div class="detail-item"><div class="detail-label">Hollow</div><div class="detail-value">{komponen11['hollow']} btg</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">12</span> <span class="component-title">Keramik Lantai</span></div>🪨</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas Lantai</div><div class="detail-value">{komponen12['lantai']} m²</div></div><div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{komponen12['semen']} sak</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">13</span> <span class="component-title">Keramik Dinding KM</span></div>🪨</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Luas</div><div class="detail-value">{komponen13['luas']} m²</div></div><div class="detail-item"><div class="detail-label">Semen</div><div class="detail-value">{komponen13['semen']} sak</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">14</span> <span class="component-title">Listrik</span></div>⚡</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Titik Lampu</div><div class="detail-value">{komponen14['titik_lampu']}</div></div><div class="detail-item"><div class="detail-label">Kabel</div><div class="detail-value">{komponen14['kabel_meter']} m</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">15</span> <span class="component-title">Sanitasi</span></div>🚽</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Closet</div><div class="detail-value">{komponen15['closet']} bh</div></div><div class="detail-item"><div class="detail-label">Wastafel</div><div class="detail-value">{komponen15['wastafel']} bh</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">16</span> <span class="component-title">Pintu</span></div>🚪</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{komponen16['jumlah']} unit</div></div><div class="detail-item"><div class="detail-label">Biaya</div><div class="detail-value">Rp {komponen16['estimasi_biaya']:,.0f}</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">17</span> <span class="component-title">Jendela</span></div>🪟</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Jumlah</div><div class="detail-value">{komponen17['jumlah']} unit</div></div><div class="detail-item"><div class="detail-label">Biaya</div><div class="detail-value">Rp {komponen17['estimasi_biaya']:,.0f}</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">18</span> <span class="component-title">Cat</span></div>🎨</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Cat Tembok</div><div class="detail-value">{komponen18['tembok']} ltr</div></div><div class="detail-item"><div class="detail-label">Total</div><div class="detail-value">{komponen18['total']} ltr</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">19</span> <span class="component-title">Dapur</span></div>🍳</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Kitchen Set</div><div class="detail-value">{'Ya' if komponen19['tersedia'] else 'Tidak'}</div></div><div class="detail-item"><div class="detail-label">Biaya</div><div class="detail-value">Rp {komponen19['kitchen_set']:,.0f}</div></div></div></div></div>
        
        <div class="component-card"><div class="component-header"><div><span class="component-num">20</span> <span class="component-title">Tenaga Kerja</span></div>👷</div><div class="component-body"><div class="detail-grid"><div class="detail-item"><div class="detail-label">Tukang</div><div class="detail-value">{komponen20['tukang']} org</div></div><div class="detail-item"><div class="detail-label">Kenek</div><div class="detail-value">{komponen20['kenek']} org</div></div><div class="detail-item"><div class="detail-label">Waktu</div><div class="detail-value">{komponen20['hari']} hari</div></div><div class="detail-item"><div class="detail-label">Total Upah</div><div class="detail-value">Rp {komponen20['total_upah']:,.0f}</div></div></div></div></div>
        """, unsafe_allow_html=True)
    
    # Ringkasan Material
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📦 Ringkasan Total Material")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Semen", f"{total_semen} sak")
    with col2: st.metric("Total Pasir", f"{total_pasir:.2f} m³")
    with col3: st.metric("Total Split", f"{total_split:.2f} m³")
    with col4: st.metric("Total Besi", f"{total_besi:.1f} kg")
    with col5: st.metric("Total Bata", f"{jumlah_bata:,} pcs")
    
    # Grand Total
    st.markdown(f"""
    <div class="grand-total">
        <p style="color: #dbeafe;">GRAND TOTAL RAB</p>
        <h2 style="color: white; font-size: 36px;">Rp {total_biaya:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # EXPORT PDF
    st.markdown("---")
    st.markdown("### 📄 Export Laporan PDF")
    
    pdf_data = {
        'tanggal': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'panjang': panjang, 'lebar': lebar, 'tinggi': tinggi, 'lantai': lantai,
        'luas_bangunan': luas_bangunan, 'kamar': kamar, 'km': km, 'dapur': dapur, 'garasi': garasi,
        'total_semen': total_semen, 'total_pasir': total_pasir, 'total_split': total_split,
        'total_besi': total_besi, 'total_bata': jumlah_bata,
        'tukang': komponen20['tukang'], 'kenek': komponen20['kenek'], 'hari': komponen20['hari'],
        'biaya_upah': komponen20['total_upah'], 'total_biaya': total_biaya
    }
    
    try:
        pdf_buffer = generate_pdf_report(pdf_data)
        st.download_button(
            label="📑 Download PDF",
            data=pdf_buffer,
            file_name=f"RAB_ARKIDIGITAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        st.info("Alternatif: Klik kanan halaman → Print → Save as PDF")

else:
    st.info("👆 Silakan isi data proyek di atas, lalu klik tombol **HITUNG KEBUTUHAN**")

# Footer
st.markdown("""
<div style="text-align: center; margin: 30px 0 20px;">
    <hr style="border-color: #e2e8f0;">
    <p style="color: #94a3b8;">🏗️ ARKIDIGITAL ESTIMATOR PRO | 20 Komponen Presisi | © 2024</p>
</div>
""", unsafe_allow_html=True)
