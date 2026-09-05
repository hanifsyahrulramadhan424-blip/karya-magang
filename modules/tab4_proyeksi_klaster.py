"""
Modul Tab 4: Klasterisasi Sektoral & Proyeksi Deret Waktu (Clustering & Forecasting) SIMAK-KUNINGAN.
Menyajikan Machine Learning K-Means Clustering 17 Lapangan Usaha dan Proyeksi Deret Waktu Ekonomi-Sosial 2026–2030 beserta Interpretasi Analitis Dinamis yang Menyesuaikan Jumlah Klaster (k).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.api import Holt
from scipy import stats

def calculate_sector_growth(df_sektor: pd.DataFrame, raw_years: list) -> pd.DataFrame:
    """Menghitung rata-rata laju pertumbuhan tahunan (CAGR/Mean Growth) untuk setiap sektor."""
    df_clean = df_sektor[~df_sektor['Sektor'].str.contains('TOTAL', na=False, case=False)].copy()
    
    # Ambil nilai awal (2015) dan akhir (2025**)
    val_2015 = df_clean['2015'].astype(float)
    val_2025 = df_clean[raw_years[-1]].astype(float)
    
    # CAGR 10 Tahun (2015-2025)
    n_years = len(raw_years) - 1
    cagr = ((val_2025 / val_2015) ** (1 / n_years) - 1) * 100
    
    df_clean['Laju_Pertumbuhan_Tahunan'] = cagr
    return df_clean

def render_tab4(data: dict, selected_year: int, idx: int):
    """Merender seluruh komponen analisis klasterisasi dan peramalan Tab 4."""
    df_ts = data['df_ts']
    raw_years = data['raw_years']
    raw_col_name = raw_years[idx]
    
    # =========================================================================
    # BAGIAN 1: K-MEANS CLUSTERING & TIPOLOGI SEKTORAL
    # =========================================================================
    st.markdown("""<div class="content-box">
<div class="section-title">🧬 1. Machine Learning Clustering & Tipologi 17 Lapangan Usaha</div>
<div class="section-subtitle">Pengelompokan analitik berbasis perpaduan pangsa kontribusi ekonomi daerah dan laju pertumbuhan rata-rata tahunan (2015–2025)</div>""", unsafe_allow_html=True)
    
    # Siapkan Data Sektor untuk Klasterisasi
    df_sektor_calc = calculate_sector_growth(data['df_sektor'], raw_years)
    df_sektor_calc['Nilai_Tahun'] = df_sektor_calc[raw_col_name].astype(float)
    total_pdrb = df_sektor_calc['Nilai_Tahun'].sum()
    df_sektor_calc['Pangsa_PDRB'] = (df_sektor_calc['Nilai_Tahun'] / total_pdrb) * 100
    
    col_c1, col_c2 = st.columns([1, 2.5])
    
    with col_c1:
        st.markdown("##### ⚙️ Konfigurasi K-Means")
        k_clusters = st.slider(
            "Pilih Jumlah Klaster (k):",
            min_value=2,
            max_value=4,
            value=3,
            help="Menentukan jumlah kelompok profil ekonomi sektor berdasarkan algoritma K-Means."
        )
        
        # Ekstraksi Fitur
        X_features = df_sektor_calc[['Pangsa_PDRB', 'Laju_Pertumbuhan_Tahunan']].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_features)
        
        # Fit K-Means
        kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
        df_sektor_calc['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # Beri label klaster berbasis profil rata-rata
        cluster_means = df_sektor_calc.groupby('Cluster')[['Pangsa_PDRB', 'Laju_Pertumbuhan_Tahunan']].mean()
        # Urutkan berdasarkan skor pembobotan pangsa + pertumbuhan
        cluster_rank = (cluster_means['Pangsa_PDRB'] * 0.6 + cluster_means['Laju_Pertumbuhan_Tahunan'] * 0.4).sort_values(ascending=False).index
        
        cluster_label_map = {}
        cluster_color_map = {}
        palette = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']
        
        if k_clusters == 2:
            titles = [
                "Klaster 1: Sektor Inti & Penggerak Utama Ekonomi (Pangsa & Pertumbuhan Unggul)",
                "Klaster 2: Sektor Penunjang & Skala Terbatas (Pangsa/Pertumbuhan Rendah-Sedang)"
            ]
        elif k_clusters == 3:
            titles = [
                "Klaster 1: Sektor Prima & Tulang Punggung (Pangsa PDRB Dominan)",
                "Klaster 2: Sektor Akselerator / High-Growth (Potensial - Rising Stars)",
                "Klaster 3: Sektor Penunjang & Skala Terbatas (Pertumbuhan Moderat)"
            ]
        else: # k_clusters == 4
            titles = [
                "Klaster 1: Sektor Prima & Tulang Punggung Tradisional (Pangsa Sangat Besar)",
                "Klaster 2: Sektor Akselerator / High-Growth (Pertumbuhan Pesat)",
                "Klaster 3: Sektor Penunjang / Berkembang Moderat (Skala Menengah)",
                "Klaster 4: Sektor Terbatas / Pertumbuhan Melandai (Butuh Revitalisasi)"
            ]
        
        for i, c_idx in enumerate(cluster_rank):
            cluster_label_map[c_idx] = titles[i]
            cluster_color_map[c_idx] = palette[i]
            
        df_sektor_calc['Klaster_Label'] = df_sektor_calc['Cluster'].map(cluster_label_map)
        df_sektor_calc['Klaster_Warna'] = df_sektor_calc['Cluster'].map(cluster_color_map)

        st.markdown(f"""<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; font-size: 0.83rem; color: #94A3B8;">
<div style="font-weight: 700; color: #E2E8F0; margin-bottom: 4px;">📌 Parameter Klaster Terpilih:</div>
• <b>Jumlah Klaster (k):</b> <span class="stat-badge">{k_clusters} Kelompok</span><br>
• <b>Fitur X:</b> Laju Pertumbuhan Tahunan (CAGR %)<br>
• <b>Fitur Y:</b> Pangsa Kontribusi PDRB (%)<br>
• <b>Standarisasi:</b> Z-Score (StandardScaler)
</div>""", unsafe_allow_html=True)

    with col_c2:
        # Scatter Plot Klasterisasi Sektoral
        fig_clust = go.Figure()
        
        # Garis Rata-rata Kuadran
        mean_x = df_sektor_calc['Laju_Pertumbuhan_Tahunan'].mean()
        mean_y = df_sektor_calc['Pangsa_PDRB'].mean()
        
        fig_clust.add_vline(x=mean_x, line_width=1, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_clust.add_hline(y=mean_y, line_width=1, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        
        for c_idx in cluster_rank:
            sub = df_sektor_calc[df_sektor_calc['Cluster'] == c_idx]
            fig_clust.add_trace(go.Scatter(
                x=sub['Laju_Pertumbuhan_Tahunan'],
                y=sub['Pangsa_PDRB'],
                mode='markers+text',
                text=sub['Kode'],
                textposition='top center',
                name=cluster_label_map[c_idx][:28] + "...",
                marker=dict(
                    size=14,
                    color=cluster_color_map[c_idx],
                    line=dict(width=1.5, color="#FFFFFF")
                ),
                customdata=np.column_stack([sub['Sektor'], sub['Nilai_Tahun']]),
                hovertemplate="<b>[%{text}] %{customdata[0]}</b><br>Nilai: Rp %{customdata[1]:,.1f} Miliar<br>Pangsa PDRB: %{y:.2f}%<br>Pertumbuhan Tahunan: %{x:.2f}%<extra></extra>"
            ))
            
        fig_clust.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            title=dict(text=f"Peta Klaster 17 Sektor Lapangan Usaha (k = {k_clusters}, Evaluasi {selected_year})", font=dict(size=14, color="#E2E8F0")),
            height=370,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
            xaxis=dict(title="Laju Pertumbuhan Rata-rata Tahunan (%)", gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(title="Pangsa Kontribusi terhadap PDRB (%)", gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_clust, use_container_width=True)
        
    # Tabel Rekapitulasi Klaster
    with st.expander(f"📋 Lihat Anggota & Karakteristik Detail Setiap Klaster (k = {k_clusters})", expanded=False):
        rekap_cols = ['Kode', 'Sektor', 'Nilai_Tahun', 'Pangsa_PDRB', 'Laju_Pertumbuhan_Tahunan', 'Klaster_Label']
        df_rekap = df_sektor_calc[rekap_cols].sort_values(by=['Klaster_Label', 'Pangsa_PDRB'], ascending=[True, False]).copy()
        df_rekap.columns = ['Kode', 'Lapangan Usaha', 'Nilai PDRB (Miliar Rp)', 'Pangsa (%)', 'Pertumbuhan Tahunan (%)', 'Hasil Klasterisasi']
        st.dataframe(df_rekap.style.format({
            'Nilai PDRB (Miliar Rp)': '{:,.2f}',
            'Pangsa (%)': '{:.2f}%',
            'Pertumbuhan Tahunan (%)': '{:.2f}%'
        }), use_container_width=True, hide_index=True)

    # =========================================================================
    # INTERPRETASI ANALITIS DINAMIS SESUAI JUMLAH KLASTER (k)
    # =========================================================================
    cluster_cards_html = ""
    
    # Arahan kebijakan spesifik per tipe klaster
    policy_templates = {
        0: "<b>Fokus Kebijakan Pemda:</b> Mempertahankan stabilitas ketahanan pangan, mempercepat hilirisasi produk pertanian ke industri pengolahan, dan menjaga kelancaran distribusi perdagangan rakyat.",
        1: "<b>Fokus Kebijakan Pemda:</b> Mendorong investasi modal, peningkatan infrastruktur digital (telekomunikasi), dan promosi terintegrasi ekosistem pariwisata Gunung Ciremai untuk mengoptimalkan potensi <i>'Rising Stars'</i>.",
        2: "<b>Fokus Kebijakan Pemda:</b> Penguatan akses permodalan KUR untuk UMKM, modernisasi logistik daerah, serta peningkatan mutu fasilitas layanan pendidikan dan kesehatan masyarakat.",
        3: "<b>Fokus Kebijakan Pemda:</b> Fasilitasi pelatihan vokasi kerja, efisiensi konsumsi energi/sumber daya, perbaikan regulasi lingkungan, dan diversifikasi produk usaha skala mikro."
    }
    
    for i, c_idx in enumerate(cluster_rank):
        sub_c = df_sektor_calc[df_sektor_calc['Cluster'] == c_idx].sort_values(by='Pangsa_PDRB', ascending=False)
        n_sec = len(sub_c)
        c_tot_share = sub_c['Pangsa_PDRB'].sum()
        c_avg_growth = sub_c['Laju_Pertumbuhan_Tahunan'].mean()
        c_color = palette[i]
        c_title = titles[i]
        
        member_items = [f"<b>[{row['Kode']}] {row['Sektor']}</b> (Pangsa: {row['Pangsa_PDRB']:.2f}%, Pertumbuhan: {row['Laju_Pertumbuhan_Tahunan']:+.2f}%)" for _, row in sub_c.iterrows()]
        members_formatted = " • ".join(member_items)
        
        policy_note = policy_templates.get(i if k_clusters >= 3 else (0 if i == 0 else 1), "")
        
        card_html = f'<div style="background: rgba(15, 23, 42, 0.6); border-left: 4px solid {c_color}; border: 1px solid rgba(255,255,255,0.06); border-left-width: 4px; border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">' \
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">' \
            f'<div style="font-weight: 700; color: {c_color}; font-size: 0.92rem;">{c_title}</div>' \
            f'<div style="font-size: 0.8rem; color: #94A3B8;">Jumlah: <span class="stat-badge">{n_sec} Sektor</span> | Total Pangsa: <span class="stat-badge">{c_tot_share:.2f}% PDRB</span> | Rerata Pertumbuhan: <span class="stat-badge">{c_avg_growth:+.2f}%/thn</span></div>' \
            f'</div>' \
            f'<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 6px;"><b>Anggota Sektor:</b> {members_formatted}</div>' \
            f'<div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5; border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 6px;">{policy_note}</div>' \
            f'</div>'
        cluster_cards_html += card_html

    cluster_interpret_html = f"""<div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%); border-left: 4px solid #10B981; border: 1px solid rgba(16, 185, 129, 0.25); border-left-width: 4px; padding: 18px 22px; border-radius: 0 14px 14px 0; margin-top: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.2);">
<div style="font-weight: 800; color: #34D399; font-size: 0.98rem; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
<div style="display: flex; align-items: center; gap: 6px;">
<span>💡</span> Panduan Membaca & Interpretasi Sektoral (Hasil Analisis K-Means: k = {k_clusters} Klaster):
</div>
<div style="font-size: 0.8rem; color: #94A3B8;">
Rerata Benchmark Daerah: Pangsa PDRB = <span class="stat-badge">{mean_y:.2f}%</span> | CAGR = <span class="stat-badge">{mean_x:.2f}%</span>
</div>
</div>
<div style="font-size: 0.86rem; color: #E2E8F0; line-height: 1.7; margin-bottom: 12px;">
Berikut adalah rincian karakteristik struktural, performa pertumbuhan, dan arahan intervensi kebijakan untuk masing-masing dari <b>{k_clusters} klaster</b> yang terbentuk berdasarkan algoritma K-Means:
</div>
{cluster_cards_html}
<div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.6; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 8px;">
<b>Catatan Tipologi Klassen:</b> Sektor yang berada di atas garis horizontal (<span class="stat-badge">&gt; {mean_y:.2f}%</span>) memiliki pangsa skala ekonomi dominan, sedangkan sektor di sebelah kanan garis vertikal (<span class="stat-badge">&gt; {mean_x:.2f}%</span>) memiliki akselerasi pertumbuhan di atas rata-rata PDRB Kabupaten Kuningan.
</div>
</div>"""
    st.markdown(cluster_interpret_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # BAGIAN 2: FORECASTING & PROYEKSI DERET WAKTU (2026–2030)
    # =========================================================================
    st.markdown("""<div class="content-box">
<div class="section-title">🔮 2. Proyeksi Makroekonomi & Indikator Sosial (2026–2030)</div>
<div class="section-subtitle">Simulasi proyeksi deret waktu menggunakan metode Holt's Linear Exponential Smoothing dan OLS Trend Projection</div>""", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns([1, 2.5])
    
    forecast_vars = {
        'PDRB_ADHK': {'name': 'PDRB Riil ADHK 2010 (Miliar Rp)', 'unit': 'Miliar Rp', 'format': '{:,.2f}'},
        'PDRB_ADHB': {'name': 'PDRB Nominal ADHB (Miliar Rp)', 'unit': 'Miliar Rp', 'format': '{:,.2f}'},
        'Kemiskinan_P0': {'name': 'Persentase Kemiskinan (P₀ %)', 'unit': '%', 'format': '{:.2f}%'},
        'Garis_Kemiskinan': {'name': 'Garis Kemiskinan (Rp/kapita/bulan)', 'unit': 'Rp', 'format': 'Rp {:,.0f}'},
        'TPT': {'name': 'Tingkat Pengangguran Terbuka (TPT %)', 'unit': '%', 'format': '{:.2f}%'},
        'Pengeluaran_Riil': {'name': 'Pengeluaran Riil per Kapita Disesuaikan', 'unit': 'Ribu Rp', 'format': '{:,.0f}'}
    }
    
    with col_f1:
        st.markdown("##### ⚙️ Pengaturan Model Peramalan")
        sel_var = st.selectbox(
            "Pilih Indikator:",
            options=list(forecast_vars.keys()),
            format_func=lambda x: forecast_vars[x]['name'],
            index=2 # Kemiskinan_P0
        )
        
        model_choice = st.radio(
            "Pilihan Algoritma:",
            options=["Holt's Linear Smoothing (Level + Trend)", "OLS Polynomial Trend Regression"],
            index=0
        )
        
        horizon = st.slider(
            "Jangkauan Proyeksi (Tahun ke Depan):",
            min_value=1,
            max_value=5,
            value=5,
            help="Proyeksi ke depan mulai dari 2026 hingga maksimal 2030."
        )
        
        # Eksekusi Model Peramalan
        y_hist = df_ts[sel_var].values
        x_hist = df_ts['Tahun'].values
        future_years = [2025 + i for i in range(1, horizon + 1)]
        
        if "Holt" in model_choice:
            # Holt's Exponential Smoothing
            holt_model = Holt(y_hist, initialization_method="estimated").fit(smoothing_level=0.6, smoothing_trend=0.3)
            y_pred_in_sample = holt_model.fittedvalues
            y_forecast = holt_model.forecast(horizon)
            # Standard error of residuals
            residuals = y_hist - y_pred_in_sample
            std_err_f = np.std(residuals)
        else:
            # OLS Polynomial/Linear Trend
            slope_f, intercept_f, r_f, p_f, se_f = stats.linregress(x_hist, y_hist)
            y_pred_in_sample = intercept_f + slope_f * x_hist
            y_forecast = intercept_f + slope_f * np.array(future_years)
            residuals = y_hist - y_pred_in_sample
            std_err_f = np.std(residuals)
            
        # Evaluasi Akurasi (In-sample)
        mape = np.mean(np.abs(residuals / y_hist)) * 100
        rmse = np.sqrt(np.mean(residuals ** 2))
        
        mape_label = "Sangat Akurat (MAPE < 5%)" if mape < 5 else ("Akurasi Baik (MAPE < 10%)" if mape < 10 else "Akurasi Cukup")
        
        st.markdown(f"""<div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; font-size: 0.83rem; color: #CBD5E1; margin-top: 10px;">
<div style="font-weight: 700; color: #60A5FA; margin-bottom: 4px;">📊 Evaluasi Akurasi Model:</div>
• <b>MAPE:</b> <span class="stat-badge">{mape:.2f}%</span> ({mape_label})<br>
• <b>RMSE:</b> <span class="stat-badge">{rmse:.3f}</span><br>
• <b>Titik Akhir 2025:</b> {y_hist[-1]:,.2f}<br>
• <b>Estimasi 2030:</b> <span style="color: #34D399; font-weight:700;">{y_forecast[-1]:,.2f}</span>
</div>""", unsafe_allow_html=True)

    with col_f2:
        # Plot Deret Waktu + Proyeksi
        fig_fcast = go.Figure()
        
        # 1. Data Historis
        fig_fcast.add_trace(go.Scatter(
            x=x_hist,
            y=y_hist,
            mode='lines+markers',
            name='Data Aktual BPS (2015–2025)',
            line=dict(color='#3B82F6', width=3),
            marker=dict(size=7, color='#60A5FA')
        ))
        
        # 2. Proyeksi Masa Depan
        x_all_proj = [x_hist[-1]] + future_years
        y_all_proj = [y_hist[-1]] + list(y_forecast)
        
        fig_fcast.add_trace(go.Scatter(
            x=x_all_proj,
            y=y_all_proj,
            mode='lines+markers',
            name=f'Lintasan Proyeksi ({model_choice[:14]})',
            line=dict(color='#10B981', width=3, dash='dash'),
            marker=dict(size=8, color='#34D399', symbol='star')
        ))
        
        # 3. Confidence Interval 95% Ribbon
        ci_upper = [y_hist[-1]] + [val + 1.96 * std_err_f * np.sqrt(i) for i, val in enumerate(y_forecast, 1)]
        ci_lower = [y_hist[-1]] + [max(0, val - 1.96 * std_err_f * np.sqrt(i)) for i, val in enumerate(y_forecast, 1)]
        
        fig_fcast.add_trace(go.Scatter(
            x=x_all_proj + x_all_proj[::-1],
            y=ci_upper + ci_lower[::-1],
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.12)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='Rentang Toleransi 95% CI'
        ))
        
        fig_fcast.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            title=dict(text=f"Lintasan Proyeksi: {forecast_vars[sel_var]['name']}", font=dict(size=14, color="#E2E8F0")),
            height=370,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
            xaxis=dict(title="Tahun", gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=2),
            yaxis=dict(title=forecast_vars[sel_var]['unit'], gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_fcast, use_container_width=True)
        
    # Ringkasan Angka Prediksi Tahunan
    st.markdown("##### 📑 Tabel Angka Proyeksi Tahunan (2026–2030)")
    df_pred_table = pd.DataFrame({
        'Tahun Proyeksi': future_years,
        'Nilai Proyeksi': y_forecast,
        'Batas Bawah (95% CI)': ci_lower[1:],
        'Batas Atas (95% CI)': ci_upper[1:],
        'Keterangan Kebijakan': [
            'Target Capaian RPJMD 2026',
            'Proyeksi Jangka Menengah 2027',
            'Evaluasi Rencana Daerah 2028',
            'Proyeksi Akselerasi 2029',
            'Target Indonesia Emas / SDGs 2030'
        ][:horizon]
    })
    
    st.dataframe(df_pred_table.style.format({
        'Nilai Proyeksi': '{:,.2f}',
        'Batas Bawah (95% CI)': '{:,.2f}',
        'Batas Atas (95% CI)': '{:,.2f}'
    }), use_container_width=True, hide_index=True)
    
    # =========================================================================
    # INTERPRETASI ANALITIS DINAMIS PROYEKSI DERET WAKTU
    # =========================================================================
    val_2025 = y_hist[-1]
    val_last_proj = y_forecast[-1]
    delta_val = val_last_proj - val_2025
    delta_pct = ((val_last_proj / val_2025) - 1) * 100 if val_2025 != 0 else 0
    
    # Generate Dynamic Narrative based on Selected Variable
    if sel_var == 'Kemiskinan_P0':
        narrative_text = f"""<div>• <b>Lintasan Penurunan Kemiskinan (P₀):</b> Berdasarkan tren historis 2015–2025, persentase penduduk miskin Kabupaten Kuningan diproyeksikan menurun dari <span class="stat-badge">{val_2025:.2f}%</span> (2025) menjadi <span class="stat-badge">{val_last_proj:.2f}%</span> pada tahun {future_years[-1]} (penurunan kumulatif sebesar <span class="stat-badge">{delta_val:.2f}% poin</span>).</div>
<div>• <b>Peluang Menuju Satu Digit (Single-Digit Poverty Target):</b> Dengan batas toleransi 95% CI antara <b>{ci_lower[-1]:.2f}%</b> hingga <b>{ci_upper[-1]:.2f}%</b>, terdapat probabilitas kuat bagi Kuningan untuk mendekati target kemiskinan di bawah 10% (Target SDGs & RPJMD).</div>
<div>• <b>Rekomendasi Intervensi:</b> Penurunan di bawah 11% membutuhkan penanganan <i>hardcore poverty</i> (kemiskinan kronis) melalui program perlindungan sosial adaptif, bantuan pangan tepat sasaran, dan penciptaan lapangan kerja formal di pedesaan guna mencegah kelompok rentan jatuh kembali ke bawah garis kemiskinan.</div>"""
    elif sel_var == 'PDRB_ADHK':
        narrative_text = f"""<div>• <b>Ekspansi Kapasitas Output Riil:</b> PDRB Riil ADHK 2010 diproyeksikan tumbuh dari <span class="stat-badge">Rp {val_2025:,.1f} Miliar</span> (2025) menuju <span class="stat-badge">Rp {val_last_proj:,.1f} Miliar</span> pada tahun {future_years[-1]} (ekspansi riil sebesar <span class="stat-badge">+{delta_pct:.2f}%</span>).</div>
<div>• <b>Stabilitas Produksi Riil:</b> Karena telah memperhitungkan deflator harga (ADHK 2010), kenaikan ini mencerminkan peningkatan kapasitas riil barang dan jasa yang diproduksi di wilayah Kabupaten Kuningan tanpa distorsi inflasi.</div>
<div>• <b>Fokus Akselerasi:</b> Menjaga stabilitas pasokan sektor pertanian dan memacu produktivitas sektor manufaktur serta jasa pariwisata agar laju pertumbuhan tahunan tetap konsisten di atas 5%.</div>"""
    elif sel_var == 'PDRB_ADHB':
        narrative_text = f"""<div>• <b>Skala Nominal Perekonomian Daerah:</b> PDRB Nominal ADHB diproyeksikan meningkat dari <span class="stat-badge">Rp {val_2025:,.1f} Miliar</span> (2025) menuju <span class="stat-badge">Rp {val_last_proj:,.1f} Miliar</span> pada tahun {future_years[-1]}.</div>
<div>• <b>Dinamika Volume dan Inflasi:</b> Pertumbuhan ADHB merefleksikan perpaduan antara peningkatan volume output riil dan dinamika kenaikan tingkat harga pasar (inflasi) di Kabupaten Kuningan.</div>
<div>• <b>Kapasitas Fiskal:</b> Peningkatan skala nominal PDRB memberikan potensi perluasan basis penerimaan pajak dan retribusi daerah bagi optimalisasi PAD.</div>"""
    elif sel_var == 'Garis_Kemiskinan':
        narrative_text = f"""<div>• <b>Eskalasi Standar Kebutuhan Minimum:</b> Garis Kemiskinan diproyeksikan meningkat dari <span class="stat-badge">Rp {val_2025:,.0f}</span> (2025) menuju <span class="stat-badge">Rp {val_last_proj:,.0f}</span> per kapita/bulan pada tahun {future_years[-1]}.</div>
<div>• <b>Tekanan Inflasi Komoditas Pangan:</b> Mengingat komoditas makanan menyumbang lebih dari 70% penentuan garis kemiskinan, tren kenaikan ini sangat dipengaruhi oleh dinamika harga bahan pokok (beras, telur, cabai, minyak goreng).</div>
<div>• <b>Urgensi Pengendalian Inflasi Daerah (TPID):</b> Kebijakan operasi pasar murah dan subsidi ongkos angkut pangan menjadi kunci utama agar kenaikan garis kemiskinan tidak melampaui pertumbuhan pendapatan masyarakat berpenghasilan rendah.</div>"""
    elif sel_var == 'TPT':
        narrative_text = f"""<div>• <b>Proyeksi Tingkat Pengangguran Terbuka:</b> TPT Kabupaten Kuningan diproyeksikan bergerak dari <span class="stat-badge">{val_2025:.2f}%</span> (2025) menuju <span class="stat-badge">{val_last_proj:.2f}%</span> pada tahun {future_years[-1]}.</div>
<div>• <b>Daya Serap Angkatan Kerja:</b> Tren penurunan TPT menunjukkan pemulihan pasar tenaga kerja pasca-pandemi dan ekspansi aktivitas usaha lokal.</div>
<div>• <b>Peningkatan Kualitas Kerja:</b> Tantangan utama bukan hanya menekan angka pengangguran, melainkan memfasilitasi transisi tenaga kerja dari sektor informal menuju sektor formal yang lebih produktif dan terlindungi jaminan sosial.</div>"""
    else: # Pengeluaran_Riil
        narrative_text = f"""<div>• <b>Peningkatan Standar Hidup Layak:</b> Pengeluaran riil per kapita disesuaikan diproyeksikan naik dari <span class="stat-badge">Rp {val_2025:,.0f} Ribu</span> (2025) menjadi <span class="stat-badge">{val_last_proj:,.0f} Ribu</span> pada tahun {future_years[-1]}.</div>
<div>• <b>Refleksi Komponen IPM:</b> Pengeluaran riil per kapita merupakan pilar penentu dimensi standar hidup layak dalam Indeks Pembangunan Manusia (IPM). Kenaikan ini mengindikasikan perbaikan daya beli riil rumah tangga Kuningan.</div>
<div>• <b>Pemerataan Daya Beli:</b> Program pemberdayaan ekonomi mikro dan stabilitas daya beli masyarakat lapisan bawah harus dijaga agar perbaikan standar hidup dinikmati secara merata.</div>"""

    forecast_interpret_html = f"""<div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%); border-left: 4px solid #3B82F6; border: 1px solid rgba(59, 130, 246, 0.25); border-left-width: 4px; padding: 18px 22px; border-radius: 0 14px 14px 0; margin-top: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.2);">
<div style="font-weight: 800; color: #60A5FA; font-size: 0.98rem; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
<span>💡</span> Panduan Membaca & Interpretasi Proyeksi ({forecast_vars[sel_var]['name']}):
</div>
<div style="font-size: 0.88rem; color: #E2E8F0; line-height: 1.8;">
{narrative_text}
<div style="margin-top: 6px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.08); font-size: 0.84rem; color: #94A3B8;">
<b>Catatan Metodologi:</b> Model <i>{model_choice}</i> menghasilkan nilai akurasi <i>Mean Absolute Percentage Error</i> (MAPE) sebesar <span class="stat-badge">{mape:.2f}%</span> ({mape_label}). Area pita hijau merepresentasikan <b>Rentang Toleransi 95% Confidence Interval (CI)</b> untuk mengantisipasi ketidakpastian guncangan eksternal (<i>exogenous shocks</i>).
</div>
</div>
</div>"""
    st.markdown(forecast_interpret_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
