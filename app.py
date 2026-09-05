"""
===============================================================================
SIMAK-KUNINGAN: Sistem Informasi & Dashboard Analitik Terpadu PDRB dan
Kesejahteraan Sosial Kabupaten Kuningan (2015–2025)
BPS Kabupaten Kuningan - Penilaian & Laporan Magang
===============================================================================
Main Application Entrypoint (Modular Architecture)
"""

import streamlit as st
import io
import importlib

# -----------------------------------------------------------------------------
# 1. IMPORT & AUTO-RELOAD MODULAR COMPONENTS
# -----------------------------------------------------------------------------
import modules.data_loader as mdl
import modules.ui_components as mui
import modules.tab1_makro as mtab1
import modules.tab2_kemiskinan as mtab2
import modules.tab3_inferensial as mtab3
import modules.tab4_proyeksi_klaster as mtab4
import modules.data_explorer as mexp

importlib.reload(mdl)
importlib.reload(mui)
importlib.reload(mtab1)
importlib.reload(mtab2)
importlib.reload(mtab3)
importlib.reload(mtab4)
importlib.reload(mexp)

from modules.data_loader import load_all_datasets
from modules.ui_components import (
    apply_custom_css,
    render_sidebar_header,
    render_header,
    render_kpi_cards,
    render_footer
)
from modules.tab1_makro import render_tab1
from modules.tab2_kemiskinan import render_tab2
from modules.tab3_inferensial import render_tab3
from modules.tab4_proyeksi_klaster import render_tab4
from modules.data_explorer import render_data_explorer

# -----------------------------------------------------------------------------
# 2. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SIMAK-KUNINGAN | Dashboard PDRB & Kesejahteraan Sosial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Terapkan Custom CSS Modern & Glassmorphic
apply_custom_css()

# -----------------------------------------------------------------------------
# 3. DATA LOADING
# -----------------------------------------------------------------------------
EXCEL_FILE = "PDRB_dan_Indikator_Sosial_Ekonomi_Kuningan_2015_2025_Final.xlsx"
try:
    data = load_all_datasets(EXCEL_FILE)
    df_ts = data['df_ts']
    raw_years = data['raw_years']
    int_years = data['int_years']
except Exception as e:
    st.error(f"⚠️ Terjadi kesalahan saat memuat berkas '{EXCEL_FILE}': {str(e)}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLLER
# -----------------------------------------------------------------------------
with st.sidebar:
    render_sidebar_header()
    
    st.markdown("### 🎛️ Panel Kontrol Analisis")
    
    # Selector Tahun Evaluasi
    selected_year = st.select_slider(
        "📅 Pilih Tahun Evaluasi:",
        options=int_years,
        value=2025,
        help="Pilih tahun evaluasi makroekonomi dan indikator sosial (2015–2025)."
    )
    
    # Basis Valuasi Harga
    price_basis = st.radio(
        "🏷️ Basis Valuasi PDRB:",
        options=["ADHB (Harga Berlaku)", "ADHK (Harga Konstan 2010)"],
        index=1,
        help="ADHB mencerminkan nilai nominal saat ini, ADHK mencerminkan nilai riil tanpa pengaruh inflasi."
    )
    
    st.markdown("---")
    
    # Info Box Seri Data
    st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.82rem; color: #94A3B8;'>
            <div style='font-weight: 700; color: #E2E8F0; margin-bottom: 4px;'>📌 Informasi Seri Data</div>
            <div>• Deret Waktu: <b>2015 – 2025</b></div>
            <div>• Status: <b>Final & Terintegrasi</b></div>
            <div>• Validasi: <b>BPS Kab. Kuningan</b></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Unduh Data Bersih
    csv_buffer = io.StringIO()
    df_ts.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Unduh Data Agregat (.CSV)",
        data=csv_buffer.getvalue(),
        file_name="SIMAK_Kuningan_Data_Makro_Sosial_2015_2025.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 5. HEADER & KPI CARDS SECTION
# -----------------------------------------------------------------------------
# Ambil Indeks Tahun Terpilih & Sebelumnya
idx = int_years.index(selected_year)
prev_idx = max(0, idx - 1)
prev_year = selected_year - 1 if idx > 0 else selected_year

row_curr = df_ts.iloc[idx]
row_prev = df_ts.iloc[prev_idx]

# Hitung Metrik Utama
curr_pdrb = row_curr['PDRB_ADHB'] if 'ADHB' in price_basis else row_curr['PDRB_ADHK']
prev_pdrb = row_prev['PDRB_ADHB'] if 'ADHB' in price_basis else row_prev['PDRB_ADHK']
delta_pdrb = ((curr_pdrb - prev_pdrb) / prev_pdrb * 100) if idx > 0 else 0.0

curr_lpe = row_curr['LPE']
prev_lpe = row_prev['LPE']
delta_lpe = curr_lpe - prev_lpe if idx > 0 else 0.0

curr_p0 = row_curr['Kemiskinan_P0']
prev_p0 = row_prev['Kemiskinan_P0']
delta_p0 = curr_p0 - prev_p0 if idx > 0 else 0.0

curr_tpt = row_curr['TPT']
prev_tpt = row_prev['TPT']
delta_tpt = curr_tpt - prev_tpt if idx > 0 else 0.0

basis_label = "ADHB" if "ADHB" in price_basis else "ADHK 2010"

# Render Banner & Kartu Metrik KPI
render_header()
render_kpi_cards(
    curr_pdrb=curr_pdrb, delta_pdrb=delta_pdrb,
    curr_lpe=curr_lpe, delta_lpe=delta_lpe,
    curr_p0=curr_p0, delta_p0=delta_p0,
    curr_tpt=curr_tpt, delta_tpt=delta_tpt,
    basis_label=basis_label, selected_year=selected_year, prev_year=prev_year
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. MODULAR TABS ORCHESTRATION
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Tab 1: Struktur Makroekonomi & Sektoral",
    "👥  Tab 2: Profil Kemiskinan & Sosial Ketenagakerjaan",
    "🔬  Tab 3: Analisis Silang, Korelasi & Elastisitas",
    "🔮  Tab 4: Klasterisasi ML & Proyeksi 2026–2030"
])

with tab1:
    render_tab1(data=data, selected_year=selected_year, idx=idx)

with tab2:
    render_tab2(data=data, selected_year=selected_year, idx=idx)

with tab3:
    render_tab3(data=data)

with tab4:
    render_tab4(data=data, selected_year=selected_year, idx=idx)

# -----------------------------------------------------------------------------
# 7. TABULAR DATA EXPLORER & FOOTER
# -----------------------------------------------------------------------------
render_data_explorer(data=data)
render_footer()


