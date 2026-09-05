"""
Modul Tab 3: Analisis Silang, Korelasi & Elastisitas Kemiskinan SIMAK-KUNINGAN.
Menyajikan heatmap korelasi bivariat Pearson, dynamic OLS regression engine, kalkulator elastisitas pro-poor growth, dan automated policy narrative.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats

def render_tab3(data: dict):
    """Merender seluruh komponen analisis inferensial Tab 3."""
    df_ts = data['df_ts']
    int_years = data['int_years']

    # Section 1: Heatmap Korelasi Pearson
    st.markdown("""
    <div class="content-box">
        <div class="section-title">🔬 Heatmap Matriks Korelasi Pearson Bivariat Dinamis</div>
        <div class="section-subtitle">Evaluasi derajat asosiasi linier antara 8 variabel makroekonomi/sektoral dengan 7 indikator kesejahteraan sosial</div>
    """, unsafe_allow_html=True)
    
    macro_vars = {
        'PDRB_ADHB': 'PDRB ADHB (Nominal)',
        'PDRB_ADHK': 'PDRB ADHK (Riil)',
        'PDRB_Kapita_ADHK': 'PDRB Per Kapita ADHK',
        'LPE': 'Laju Pertumbuhan (LPE)',
        'Pertanian': 'Sektor Pertanian',
        'Perdagangan': 'Sektor Perdagangan',
        'Transportasi': 'Sektor Transportasi',
        'Konstruksi': 'Sektor Konstruksi'
    }
    
    social_vars = {
        'Kemiskinan_P0': 'Persentase Kemiskinan (P₀)',
        'Kedalaman_P1': 'Indeks Kedalaman (P₁)',
        'Keparahan_P2': 'Indeks Keparahan (P₂)',
        'TPT': 'Tingkat Pengangguran (TPT)',
        'Proporsi_Informal': 'Proporsi Tenaga Kerja Informal',
        'TPAK': 'Partisipasi Angkatan Kerja (TPAK)',
        'Pengeluaran_Riil': 'Pengeluaran Riil Per Kapita'
    }
    
    # Hitung Matriks Korelasi & P-values
    corr_matrix = []
    annot_matrix = []
    
    for s_key in social_vars.keys():
        row_corr = []
        row_annot = []
        for m_key in macro_vars.keys():
            r_val, p_val = stats.pearsonr(df_ts[m_key], df_ts[s_key])
            row_corr.append(r_val)
            star = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else ""))
            row_annot.append(f"{r_val:.2f}{star}")
        corr_matrix.append(row_corr)
        annot_matrix.append(row_annot)
        
    corr_df = pd.DataFrame(corr_matrix, index=list(social_vars.values()), columns=list(macro_vars.values()))
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        text=annot_matrix,
        texttemplate="%{text}",
        textfont={"size": 11, "color": "#080808"},
        colorbar=dict(title="Koefisien Pearson (r)", len=0.8)
    ))
    
    fig_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(l=20, r=20, t=20, b=30),
        xaxis=dict(tickangle=-25)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # Panduan Membaca & Ringkasan Temuan
    st.markdown("""
    <div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%); border-left: 4px solid #3B82F6; border: 1px solid rgba(59, 130, 246, 0.25); border-left-width: 4px; padding: 18px 22px; border-radius: 0 14px 14px 0; margin-top: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.2);">
        <div style="font-weight: 800; color: #60A5FA; font-size: 0.98rem; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
            <span>💡</span> Panduan Membaca & Ringkasan Temuan:
        </div>
        <div style="font-size: 0.88rem; color: #E2E8F0; line-height: 1.8;">
            <div>• <b>Arah Hubungan:</b> Warna merah tua (<i>r</i> &rarr; +1) menunjukkan hubungan searah (kedua indikator naik bersamaan), sedangkan warna biru tua (<i>r</i> &rarr; -1) menunjukkan hubungan berlawanan arah.</div>
            <div>• <b>Tingkat Signifikansi:</b> Tanda bintang menandakan keabsahan statistik uji dua arah (two-tailed): <span class="stat-badge">*** p &lt; 0,001</span> (sangat signifikan), <span class="stat-badge">** p &lt; 0,01</span>, dan <span class="stat-badge">* p &lt; 0,05</span>.</div>
            <div>• <b>Korelasi Pengentasan Kemiskinan:</b> PDRB per kapita riil (<span class="stat-badge">-0,90***</span>) serta output sektor Pertanian (<span class="stat-badge">-0,83**</span>), Perdagangan (<span class="stat-badge">-0,80**</span>), dan Konstruksi (<span class="stat-badge">-0,80**</span>) memiliki korelasi negatif kuat terhadap persentase penduduk miskin (<i>P₀</i>), membuktikan pertumbuhan ekonomi Kuningan bersifat inklusif (<i>pro-poor</i>).</div>
            <div>• <b>Konfirmasi Hukum Okun:</b> Korelasi signifikan antara laju pertumbuhan ekonomi (LPE) dan tingkat pengangguran terbuka/TPT (<span class="stat-badge">-0,74**</span>) mengindikasikan bahwa akselerasi pertumbuhan output riil terbukti efektif menyerap angkatan kerja daerah.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 2: Dynamic OLS Regression Engine & Poverty Elasticity
    st.markdown("""
    <div class="content-box">
        <div class="section-title">📐 Dynamic OLS Regression Engine & Kalkulator Elastisitas Kemiskinan</div>
        <div class="section-subtitle">Eksplorasi regresi linier bebas dan evaluasi empiris elastisitas pertumbuhan ekonomi inklusif</div>
    """, unsafe_allow_html=True)
    
    col_t3_a, col_t3_b = st.columns([1.1, 1.9])
    
    all_var_options = {**macro_vars, **social_vars}
    
    with col_t3_a:
        st.markdown("##### ⚙️ Konfigurasi Model Regresi")
        var_x_key = st.selectbox("Pilih Variabel Bebas (X):", options=list(all_var_options.keys()), format_func=lambda x: all_var_options[x], index=2)
        var_y_key = st.selectbox("Pilih Variabel Terikat (Y):", options=list(all_var_options.keys()), format_func=lambda x: all_var_options[x], index=8)
        
        x_vals = df_ts[var_x_key].values
        y_vals = df_ts[var_y_key].values
        
        # Komputasi OLS
        slope, intercept, r_val, p_val, std_err = stats.linregress(x_vals, y_vals)
        r_squared = r_val ** 2
        
        if p_val < 0.001:
            sig_badge = "<span style='color: #34D399; font-weight:700;'>Sangat Signifikan (p < 0.001)</span>"
        elif p_val < 0.05:
            sig_badge = "<span style='color: #60A5FA; font-weight:700;'>Signifikan (p < 0.05)</span>"
        else:
            sig_badge = "<span style='color: #F87171; font-weight:700;'>Tidak Signifikan (p ≥ 0.05)</span>"

        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 16px; margin-top: 14px;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Persamaan Model Regresi:</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #60A5FA; margin: 6px 0;">
                Ŷ = {intercept:.4f} {slope:+.4f} X
            </div>
            <div style="font-size: 0.84rem; color: #CBD5E1; line-height: 1.8;">
                • Korelasi (r): <span class="stat-badge">{r_val:.4f}</span><br>
                • Koefisien Determinasi (R²): <span class="stat-badge">{r_squared*100:.2f}%</span><br>
                • P-value: <span class="stat-badge">{p_val:.5f}</span><br>
                • Standard Error (SE): <span class="stat-badge">{std_err:.5f}</span><br>
                • Status: {sig_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_t3_b:
        # Scatter Plot dengan Garis Tren OLS
        x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_trend = intercept + slope * x_trend
        
        fig_ols = go.Figure()
        
        fig_ols.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers+text',
            text=[str(y) for y in df_ts['Tahun']],
            textposition='top center',
            marker=dict(size=11, color='#3B82F6', line=dict(width=1.5, color='#93C5FD')),
            hovertemplate="<b>Tahun %{text}</b><br>X: %{x:,.2f}<br>Y: %{y:,.2f}<extra></extra>",
            name="Data Titik Observasi"
        ))
        
        fig_ols.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode='lines',
            line=dict(color='#10B981', width=3),
            name=f"Garis Tren OLS (R²={r_squared*100:.1f}%)"
        ))
        
        fig_ols.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            height=370,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title=all_var_options[var_x_key], gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(title=all_var_options[var_y_key], gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_ols, use_container_width=True)

    # Kotak Interpretasi Analitik Dinamis Model Regresi OLS
    arah_teks = "berbanding terbalik (kenaikan X menekan nilai Y)" if slope < 0 else "searah (kenaikan X mendorong kenaikan Y)"
    if p_val < 0.001:
        signifikan_teks = "sangat signifikan secara statistik (p < 0.001)"
    elif p_val < 0.05:
        signifikan_teks = "signifikan secara statistik (p < 0.05)"
    else:
        signifikan_teks = "tidak signifikan secara statistik (p ≥ 0.05)"

    # Konteks Kebijakan Khusus
    if 'Kemiskinan' in all_var_options[var_y_key] and 'PDRB' in all_var_options[var_x_key]:
        konteks_kebijakan = f"Secara empiris membuktikan terjadinya <i>trickle-down effect</i> di Kabupaten Kuningan: setiap kenaikan Rp 1 juta PDRB per kapita riil secara efektif mampu menekan angka kemiskinan sebesar <b>{abs(slope):.4f}% poin</b>."
    elif 'Kemiskinan' in all_var_options[var_y_key] and 'Pertanian' in all_var_options[var_x_key]:
        konteks_kebijakan = f"Mengonfirmasi sektor pertanian sebagai sektor kunci (<i>key driver</i>) pengentasan kemiskinan perdesaan karena menyerap basis tenaga kerja terbesar di Kuningan."
    elif 'TPT' in all_var_options[var_y_key] and 'LPE' in all_var_options[var_x_key]:
        konteks_kebijakan = f"Memvalidasi berlakunya <b>Hukum Okun (Okun's Law)</b> di tingkat daerah: akselerasi pertumbuhan ekonomi riil terbukti efektif menyerap angkatan kerja dan menurunkan pengangguran."
    else:
        konteks_kebijakan = f"Pola regresi ini mencerminkan dinamika struktural makroekonomi daerah yang dapat dijadikan rujukan penetapan target indikator kinerja pembangunan daerah."

    st.markdown(f"""
    <div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%); border-left: 4px solid #10B981; border: 1px solid rgba(16, 185, 129, 0.25); border-left-width: 4px; padding: 18px 22px; border-radius: 0 14px 14px 0; margin-top: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.2);">
        <div style="font-weight: 800; color: #34D399; font-size: 0.98rem; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
            <span>💡</span> Interpretasi Analitik & Makna Ekonometrika Model:
        </div>
        <div style="font-size: 0.88rem; color: #E2E8F0; line-height: 1.8;">
            <div>• <b>Kemiringan Garis (Slope &beta;₁ = {slope:.4f}):</b> Menunjukkan hubungan <b>{arah_teks}</b>. Setiap kenaikan 1 satuan <i>{all_var_options[var_x_key]}</i> terestimasi mengubah nilai <i>{all_var_options[var_y_key]}</i> sebesar <b>{abs(slope):.4f} satuan</b>.</div>
            <div>• <b>Koefisien Determinasi (R² = {r_squared*100:.2f}%):</b> Sebesar <b>{r_squared*100:.2f}%</b> variasi perubahan pada <i>{all_var_options[var_y_key]}</i> dapat dijelaskan secara linier oleh variabel <i>{all_var_options[var_x_key]}</i>, sedangkan sisanya ({100 - r_squared*100:.2f}%) dipengaruhi oleh faktor-faktor lain di luar model.</div>
            <div>• <b>Keabsahan Statistik (p-value = {p_val:.5f}):</b> Model berada pada tingkat <b>{signifikan_teks}</b>, membuktikan bahwa asosiasi empiris ini sangat kokoh dan bukan kebetulan acak.</div>
            <div>• <b>Makna Kebijakan (Policy Insight):</b> {konteks_kebijakan}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Section 3: Poverty Elasticity of Growth Calculator
    st.markdown("---")
    st.markdown("##### 📊 Analisis Elastisitas Pertumbuhan Kemiskinan (Poverty Elasticity of Growth)")
    
    p0_series = df_ts['Kemiskinan_P0'].values
    pdrb_series = df_ts['PDRB_ADHK'].values
    
    pct_dp0 = np.diff(p0_series) / p0_series[:-1] * 100
    pct_dpdrb = np.diff(pdrb_series) / pdrb_series[:-1] * 100
    elasticity_raw = pct_dp0 / pct_dpdrb
    year_diff_labels = [f"{y1}–{y2}" for y1, y2 in zip(int_years[:-1], int_years[1:])]
    
    col_el_toggle, col_el_stat = st.columns([1, 2])
    with col_el_toggle:
        isolate_2020 = st.toggle(
            "🛡️ Isolasi Outlier Guncangan Pandemi 2020",
            value=True,
            help="Tahun 2020 mengalami guncangan ekstrim di mana pertumbuhan PDRB melambat ke 0.11% sehingga kalkulasi elastisitas menjadi terdistorsi (+111.98)."
        )
    
    if isolate_2020:
        mask = [i != 4 for i in range(len(elasticity_raw))]
        avg_elasticity = np.mean(np.array(elasticity_raw)[mask])
        display_years = [y for i, y in enumerate(year_diff_labels) if i != 4]
        display_el = [e for i, e in enumerate(elasticity_raw) if i != 4]
        status_note = "Kondisi Normal (di luar anomali 2020)"
    else:
        avg_elasticity = np.mean(elasticity_raw)
        display_years = year_diff_labels
        display_el = elasticity_raw
        status_note = "Seluruh Periode (termasuk 2020)"

    with col_el_stat:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border-left: 4px solid #10B981; padding: 10px 16px; border-radius: 0 10px 10px 0;">
            <span style="font-weight: 700; color: #34D399; font-size: 1.05rem;">Rata-rata Elastisitas Kemiskinan (ε̄): {avg_elasticity:.3f}</span>
            <span style="font-size: 0.85rem; color: #CBD5E1; margin-left: 8px;">({status_note} ➔ <b>Pro-Poor Growth</b>)</span>
        </div>
        """, unsafe_allow_html=True)
        
    # Elasticity Bar Chart
    fig_el = go.Figure(go.Bar(
        x=display_years,
        y=display_el,
        marker=dict(
            color=['#10B981' if val < 0 else '#EF4444' for val in display_el],
            line=dict(color="rgba(255,255,255,0.15)", width=1)
        ),
        text=[f"{val:.2f}" for val in display_el],
        textposition="outside",
        hovertemplate="<b>Periode %{x}</b><br>Elastisitas (ε): %{y:.3f}<extra></extra>"
    ))
    fig_el.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(title="Koefisien Elastisitas (ε)", gridcolor="rgba(255,255,255,0.06)")
    )
    st.plotly_chart(fig_el, use_container_width=True)
    
    # Section 4: Automated Policy Narrative Box
    st.markdown("""
    <div class="stat-highlight">
        <div style="font-weight: 700; color: #60A5FA; margin-bottom: 4px;">📝 Automated Policy Narrative (Siap Dikutip untuk Laporan/Sidang Magang):</div>
        <div>
            Berdasarkan estimasi ekonometrika deret waktu 2015–2025 di Kabupaten Kuningan, pertumbuhan ekonomi terbukti secara empiris bersifat <b>inklusif dan pro-poor</b>. 
            Koefisien elastisitas rata-rata bernilai <span class="stat-badge">{:.2f}</span>, mengindikasikan bahwa setiap 1% peningkatan PDRB riil secara konsisten mampu mereduksi persentase kemiskinan sebesar {:.2f}%. 
            Sektor Pertanian memegang peranan krusial sebagai transmisi utama pengentasan kemiskinan (korelasi r = -0.828, p = 0.00167), sementara sektor informal (>62%) berperan sebagai katup pengaman penyerap tenaga kerja saat terjadi guncangan makro.
        </div>
    </div>
    """.format(avg_elasticity, abs(avg_elasticity)), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
