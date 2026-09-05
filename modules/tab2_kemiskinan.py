"""
Modul Tab 2: Profil Kemiskinan & Sosial Ketenagakerjaan SIMAK-KUNINGAN.
Menyajikan visualisasi indeks FGT, garis kemiskinan, struktur tenaga kerja formal/informal, dan komponen IPM.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_tab2(data: dict, selected_year: int, idx: int):
    """Merender seluruh komponen visual Tab 2."""
    df_ts = data['df_ts']
    row_curr = df_ts.iloc[idx]

    # Section 1: FGT Indices & Garis Kemiskinan
    st.markdown("""
    <div class="content-box">
        <div class="section-title">📉 Dinamika Indeks Kemiskinan FGT (P₀, P₁, P₂) & Garis Kemiskinan</div>
        <div class="section-subtitle">Pelacakan evolusi persentase kemiskinan, kedalaman kesenjangan pengeluaran, dan standar kebutuhan hidup minimum</div>
    """, unsafe_allow_html=True)
    
    col_t2_a, col_t2_b = st.columns([3, 2])
    
    with col_t2_a:
        # FGT Indices Dynamics
        fig_fgt = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_fgt.add_trace(
            go.Scatter(
                x=df_ts['Tahun'],
                y=df_ts['Kemiskinan_P0'],
                name="Persentase Miskin (P₀ %)",
                mode="lines+markers",
                line=dict(color="#EF4444", width=3.5),
                marker=dict(size=8, color="#F87171"),
                hovertemplate="<b>Tahun %{x}</b><br>P₀ (Headcount): %{y:.2f}%<extra></extra>"
            ),
            secondary_y=False
        )
        
        fig_fgt.add_trace(
            go.Scatter(
                x=df_ts['Tahun'],
                y=df_ts['Kedalaman_P1'],
                name="Kedalaman Kemiskinan (P₁)",
                mode="lines+markers",
                line=dict(color="#F59E0B", width=2.5, dash="dash"),
                marker=dict(size=6, color="#FBBF24"),
                hovertemplate="<b>Tahun %{x}</b><br>P₁ (Depth): %{y:.2f}<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig_fgt.add_trace(
            go.Scatter(
                x=df_ts['Tahun'],
                y=df_ts['Keparahan_P2'],
                name="Keparahan Kemiskinan (P₂)",
                mode="lines+markers",
                line=dict(color="#8B5CF6", width=2.5, dash="dot"),
                marker=dict(size=6, color="#A78BFA"),
                hovertemplate="<b>Tahun %{x}</b><br>P₂ (Severity): %{y:.2f}<extra></extra>"
            ),
            secondary_y=True
        )

        fig_fgt.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=1),
            yaxis=dict(title="Persentase Penduduk Miskin (%)", gridcolor="rgba(255,255,255,0.06)"),
            yaxis2=dict(title="Indeks P₁ & P₂", gridcolor="rgba(255,255,255,0.02)")
        )
        st.plotly_chart(fig_fgt, use_container_width=True)

    with col_t2_b:
        # Garis Kemiskinan Area Chart
        fig_gk = go.Figure()
        fig_gk.add_trace(go.Scatter(
            x=df_ts['Tahun'],
            y=df_ts['Garis_Kemiskinan'],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(59, 130, 246, 0.15)",
            line=dict(color="#3B82F6", width=3),
            marker=dict(size=7, color="#60A5FA"),
            hovertemplate="<b>Tahun %{x}</b><br>Garis Kemiskinan: Rp %{y:,.0f}/kap/bln<extra></extra>"
        ))
        fig_gk.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            title=dict(text="Evolusi Garis Kemiskinan (Rp/kapita/bulan)", font=dict(size=14, color="#E2E8F0")),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=2),
            yaxis=dict(title="Rupiah (Rp)", gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_gk, use_container_width=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 2: Ketenagakerjaan Formal vs Informal & IPM Grid
    st.markdown("""
    <div class="content-box">
        <div class="section-title">👔 Struktur Ketenagakerjaan & Komponen Indeks Pembangunan Manusia (IPM)</div>
        <div class="section-subtitle">Ketahanan tenaga kerja sektor informal sebagai katup pengaman ekonomi daerah dan progres kapabilitas dasar</div>
    """, unsafe_allow_html=True)
    
    col_t2_c, col_t2_d = st.columns([3, 2])
    
    with col_t2_c:
        # Stacked Bar Informal vs Formal
        fig_labor = go.Figure()
        fig_labor.add_trace(go.Bar(
            x=df_ts['Tahun'],
            y=df_ts['Proporsi_Informal'],
            name="Sektor Informal (>62%)",
            marker_color="#F59E0B",
            hovertemplate="<b>Tahun %{x}</b><br>Informal: %{y:.2f}%<extra></extra>"
        ))
        fig_labor.add_trace(go.Bar(
            x=df_ts['Tahun'],
            y=df_ts['Proporsi_Formal'],
            name="Sektor Formal",
            marker_color="#3B82F6",
            hovertemplate="<b>Tahun %{x}</b><br>Formal: %{y:.2f}%<extra></extra>"
        ))
        fig_labor.update_layout(
            barmode='stack',
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            title=dict(text="Distribusi Tenaga Kerja: Sektor Formal vs Informal (%)", font=dict(size=14, color="#E2E8F0")),
            height=360,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=1),
            yaxis=dict(title="Proporsi (%)", range=[0, 105], gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_labor, use_container_width=True)

    with col_t2_d:
        # IPM Highlights Grid for Selected Year
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; height: 100%; align-content: center;">
            <div style="background: rgba(30, 41, 59, 0.7); padding: 14px; border-radius: 12px; border-left: 3px solid #10B981;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Umur Harapan Hidup (UHH)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC;">{row_curr['UHH']:.2f} <span style="font-size: 0.8rem; font-weight: 500;">Thn</span></div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.7); padding: 14px; border-radius: 12px; border-left: 3px solid #3B82F6;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Harapan Lama Sekolah (HLS)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC;">{row_curr['HLS']:.2f} <span style="font-size: 0.8rem; font-weight: 500;">Thn</span></div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.7); padding: 14px; border-radius: 12px; border-left: 3px solid #F59E0B;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Rata-rata Lama Sekolah (RLS)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC;">{row_curr['RLS']:.2f} <span style="font-size: 0.8rem; font-weight: 500;">Thn</span></div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.7); padding: 14px; border-radius: 12px; border-left: 3px solid #8B5CF6;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Pengeluaran Riil Per Kapita</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC;">Rp {row_curr['Pengeluaran_Riil']:,.0f} <span style="font-size: 0.75rem; font-weight: 500;">rb/th</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
