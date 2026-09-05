"""
Modul UI Components SIMAK-KUNINGAN.
Menyediakan CSS modern glassmorphism, header banner, kartu metrik KPI, dan komponen antarmuka.
"""

import streamlit as st

def apply_custom_css():
    """Menginjeksikan CSS modern, tipografi Plus Jakarta Sans, dan gaya glassmorphic."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Main Background */
        .main {
            background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 0.98) 0%, rgba(10, 15, 30, 1) 90%);
            color: #F8FAFC;
        }
        
        /* Top Header Banner */
        .header-box {
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(15, 23, 42, 0.8) 50%, rgba(30, 27, 75, 0.4) 100%);
            border: 1px solid rgba(59, 130, 246, 0.25);
            border-radius: 20px;
            padding: 24px 30px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        
        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.35);
            color: #93C5FD;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .header-title {
            font-size: 2.1rem;
            font-weight: 800;
            background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 50%, #60A5FA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.2;
        }
        
        .header-desc {
            color: #94A3B8;
            font-size: 0.95rem;
            margin-top: 6px;
            margin-bottom: 0;
        }
        
        /* Modern Glassmorphic KPI Metric Card */
        .kpi-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(96, 165, 250, 0.4);
            box-shadow: 0 12px 28px -6px rgba(37, 99, 235, 0.25);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3B82F6, #10B981);
            border-radius: 16px 16px 0 0;
        }
        
        .kpi-title {
            color: #94A3B8;
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 8px;
        }
        
        .kpi-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: 10px;
        }
        
        .kpi-footer {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.82rem;
        }
        
        .delta-badge-pos {
            display: inline-flex;
            align-items: center;
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
        }
        
        .delta-badge-neg {
            display: inline-flex;
            align-items: center;
            background: rgba(239, 68, 68, 0.15);
            color: #F87171;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.78rem;
        }
        
        /* Section Containers */
        .content-box {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
        }
        
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #F1F5F9;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-subtitle {
            color: #64748B;
            font-size: 0.86rem;
            margin-bottom: 18px;
        }
        
        /* Stat Highlights in Narrative */
        .stat-highlight {
            background: rgba(59, 130, 246, 0.12);
            border-left: 4px solid #3B82F6;
            padding: 14px 18px;
            border-radius: 0 12px 12px 0;
            margin: 12px 0;
            color: #E2E8F0;
            font-size: 0.92rem;
            line-height: 1.6;
        }
        
        .stat-badge {
            font-family: monospace;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            color: #60A5FA;
            font-weight: 600;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0B1120;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.6);
            padding: 8px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 46px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 10px;
            color: #94A3B8;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 0 20px;
            border: none !important;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header():
    """Merender logo dan judul pada sidebar."""
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 20px 0;'>
            <div style='display: inline-block; background: linear-gradient(135deg, #3B82F6, #1D4ED8); padding: 12px; border-radius: 16px; box-shadow: 0 8px 20px rgba(37,99,235,0.4);'>
                <span style='font-size: 2rem;'>📊</span>
            </div>
            <h2 style='margin-top: 12px; font-size: 1.3rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;'>SIMAK-KUNINGAN</h2>
            <p style='font-size: 0.78rem; color: #94A3B8; margin-top: -4px;'>BPS & Bappeda Kab. Kuningan</p>
        </div>
    """, unsafe_allow_html=True)

def render_header():
    """Merender banner atas dashboard."""
    st.markdown("""
    <div class="header-box">
        <div class="badge-pill">
            <span>🏛️</span> KELUARAN RESMI MAGANG BPS KABUPATEN KUNINGAN (2015–2025)
        </div>
        <h1 class="header-title">Sistem Informasi & Dashboard Analitik Terpadu SIMAK-KUNINGAN</h1>
        <p class="header-desc">
            Integrasi Evaluasi Makroekonomi, Pemetaan Sektoral 17 Lapangan Usaha, Indeks Kemiskinan FGT, serta Pemodelan Ekonometrika Elastisitas Pertumbuhan Inklusif.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_cards(curr_pdrb, delta_pdrb, curr_lpe, delta_lpe, curr_p0, delta_p0, curr_tpt, delta_tpt, basis_label, selected_year, prev_year):
    """Merender 4 kartu metrik utama dengan perbandingan YoY."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        badge_cls = "delta-badge-pos" if delta_pdrb >= 0 else "delta-badge-neg"
        arrow = "▲" if delta_pdrb >= 0 else "▼"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total PDRB ({basis_label})</div>
            <div class="kpi-value">Rp {curr_pdrb:,.1f} <span style="font-size: 1rem; font-weight: 500; color: #94A3B8;">M</span></div>
            <div class="kpi-footer">
                <span class="{badge_cls}">{arrow} {abs(delta_pdrb):.2f}% YoY</span>
                <span style="color: #64748B;">vs {prev_year}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        badge_cls = "delta-badge-pos" if delta_lpe >= 0 else "delta-badge-neg"
        arrow = "▲" if delta_lpe >= 0 else "▼"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Laju Pertumbuhan (LPE)</div>
            <div class="kpi-value" style="color: #60A5FA;">{curr_lpe:.2f}%</div>
            <div class="kpi-footer">
                <span class="{badge_cls}">{arrow} {abs(delta_lpe):.2f}% pt</span>
                <span style="color: #64748B;">Pertumbuhan Riil</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        badge_cls = "delta-badge-pos" if delta_p0 <= 0 else "delta-badge-neg"
        arrow = "▼" if delta_p0 <= 0 else "▲"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Tingkat Kemiskinan (P₀)</div>
            <div class="kpi-value" style="color: #34D399;">{curr_p0:.2f}%</div>
            <div class="kpi-footer">
                <span class="{badge_cls}">{arrow} {abs(delta_p0):.2f}% pt</span>
                <span style="color: #64748B;">Populasi Miskin</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        badge_cls = "delta-badge-pos" if delta_tpt <= 0 else "delta-badge-neg"
        arrow = "▼" if delta_tpt <= 0 else "▲"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Pengangguran Terbuka (TPT)</div>
            <div class="kpi-value" style="color: #FBBF24;">{curr_tpt:.2f}%</div>
            <div class="kpi-footer">
                <span class="{badge_cls}">{arrow} {abs(delta_tpt):.2f}% pt</span>
                <span style="color: #64748B;">Angkatan Kerja</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """Merender footer halaman dashboard."""
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 24px 0 10px 0;">
        <b>SIMAK-KUNINGAN v1.0</b> • Sistem Informasi & Dashboard Analitik Terpadu PDRB dan Kesejahteraan Sosial Kabupaten Kuningan<br>
        Dikembangkan untuk Keperluan Penilaian Magang Akademik & Evaluasi Kebijakan BPS Kab. Kuningan • Data Terverifikasi 2015–2025
    </div>
    """, unsafe_allow_html=True)
