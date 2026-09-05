"""
Modul Tab 1: Struktur Makroekonomi & Sektoral SIMAK-KUNINGAN.
Menyajikan visualisasi deret waktu PDRB, LPE, dekomposisi 17 lapangan usaha (dengan info interpretasi lengkap), komponen pengeluaran, dan ICVAR.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import textwrap

# Kamus Narasi & Interpretasi Ekonomi 17 Sektor Lapangan Usaha
SECTOR_INTERPRETATIONS = {
    'A': {
        'nama_pendek': 'Pertanian, Kehutanan & Perikanan',
        'match': 'pertanian',
        'interpretasi': 'Angkanya menempati posisi terbesar karena bertumpu pada hamparan sawah produktif dan hortikultura lereng Ciremai, sentra peternakan sapi perah Cigugur, serta perannya menyerap sepertiga angkatan kerja daerah untuk kebutuhan pangan pokok.'
    },
    'B': {
        'nama_pendek': 'Pertambangan & Penggalian',
        'match': 'pertambangan',
        'interpretasi': 'Angkanya tertahan kecil karena operasinya hanya mengandalkan galian pasir dan batu kali lokal yang dibatasi ketat oleh regulasi zona konservasi Gunung Ciremai.'
    },
    'C': {
        'nama_pendek': 'Industri Pengolahan',
        'match': 'industri',
        'interpretasi': 'Nilainya hanya berkisar ratusan miliar karena struktur manufaktur didominasi UMKM olahan pangan rumahan seperti tape ketan dan olahan susu, tanpa adanya pabrik padat modal berskala multinasional.'
    },
    'D': {
        'nama_pendek': 'Pengadaan Listrik & Gas',
        'match': 'listrik',
        'interpretasi': 'Menghasilkan nilai paling rendah karena daerah tidak memiliki pembangkit listrik mandiri, sehingga perputarannya murni berasal dari margin tarif distribusi PLN dan agen elpiji.'
    },
    'E': {
        'nama_pendek': 'Pengadaan Air, Sampah & Daur Ulang',
        'match': 'pengadaan air',
        'interpretasi': 'Nilainya terbentuk dari monetisasi komersial sumber mata air alami Ciremai oleh PDAM daerah serta penarikan retribusi pengangkutan limbah permukiman.'
    },
    'F': {
        'nama_pendek': 'Konstruksi',
        'match': 'konstruksi',
        'interpretasi': 'Angkanya menembus Rp 3 triliun berkat pembiayaan proyek jalan lingkar, sarana irigasi bendungan, serta tingginya pembangunan rumah tapak dari serapan dana remitansi perantau.'
    },
    'G': {
        'nama_pendek': 'Perdagangan Besar & Eceran; Reparasi',
        'match': 'perdagangan',
        'interpretasi': 'Angkanya berada di posisi tiga besar karena menjadi terminal transaksi belanja kebutuhan harian masyarakat di ratusan pasar tradisional dan jejaring ritel modern.'
    },
    'H': {
        'nama_pendek': 'Transportasi & Pergudangan',
        'match': 'transportasi',
        'interpretasi': 'Nilainya melonjak tinggi ke posisi kedua akibat perputaran tiket armada bus antarkota bagi mobilitas perantau Jabodetabek serta peran strategis akses jalan regional dalam distribusi barang.'
    },
    'I': {
        'nama_pendek': 'Penyediaan Akomodasi & Makan Minum',
        'match': 'akomodasi',
        'interpretasi': 'Angkanya didorong oleh aliran uang wisatawan luar daerah yang berlibur dan membelanjakan dananya di hotel resor serta kafe panorama lereng pegunungan.'
    },
    'J': {
        'nama_pendek': 'Informasi & Komunikasi',
        'match': 'informasi',
        'interpretasi': 'Nilainya tumbuh berkat perluasan jaringan internet serat optik, penambahan menara pemancar, serta maraknya transaksi daring masyarakat.'
    },
    'K': {
        'nama_pendek': 'Jasa Keuangan & Asuransi',
        'match': 'keuangan',
        'interpretasi': 'Angkanya mencapai Rp 2,2 triliun karena digerakkan oleh perputaran bunga dan likuiditas pembiayaan perbankan, BPR daerah, serta kredit usaha rakyat bagi petani dan pedagang.'
    },
    'L': {
        'nama_pendek': 'Real Estat',
        'match': 'real estat',
        'interpretasi': 'Berada di angka Rp 1 triliun karena tingginya permintaan kavling perumahan baru seiring urbanisasi lokal dan investasi tanah oleh warga perantauan.'
    },
    'M,N': {
        'nama_pendek': 'Jasa Perusahaan',
        'match': 'jasa perusahaan',
        'interpretasi': 'Skalanya masih terbatas karena permintaannya baru mencakup penyediaan tenaga alih daya keamanan, kebersihan gedung, dan jasa penyewaan perlengkapan acara.'
    },
    'O': {
        'nama_pendek': 'Administrasi Pemerintahan',
        'match': 'administrasi pemerintahan',
        'interpretasi': 'Porsinya melandai di kisaran Rp 1,1 triliun akibat pengetatan belanja operasional birokrasi dan keterbatasan alokasi APBD daerah pascapandemi.'
    },
    'P': {
        'nama_pendek': 'Jasa Pendidikan',
        'match': 'pendidikan',
        'interpretasi': 'Masuk jajaran empat besar karena ditopang oleh perputaran dana ratusan sekolah formal, kampus swasta, dan puluhan pondok pesantren berasrama besar yang menampung ribuan santri luar kota.'
    },
    'Q': {
        'nama_pendek': 'Jasa Kesehatan & Kegiatan Sosial',
        'match': 'kesehatan',
        'interpretasi': 'Angkanya terbentuk dari akumulasi pendapatan operasional rumah sakit umum daerah, puskesmas kecamatan, dan klaim biaya medis melalui BPJS Kesehatan.'
    },
    'R,S,T,U': {
        'nama_pendek': 'Jasa Lainnya',
        'match': 'jasa lainnya',
        'interpretasi': 'Nilainya menyentuh Rp 1,5 triliun karena menjadi penampung utama aktivitas jasa perorangan seperti bengkel reparasi, pangkas rambut, dan jasa kesenian rakyat.'
    }
}

def get_sector_info(sector_name: str) -> tuple:
    """Mengembalikan kode sektor dan teks interpretasi yang sesuai."""
    s_lower = sector_name.lower()
    for code, info in SECTOR_INTERPRETATIONS.items():
        if info['match'] in s_lower:
            return code, info['interpretasi'], info['nama_pendek']
    return '-', 'Kontributor nilai tambah bruto daerah Kabupaten Kuningan.', sector_name

def render_tab1(data: dict, selected_year: int, idx: int):
    """Merender seluruh komponen visual Tab 1."""
    df_ts = data['df_ts']
    raw_years = data['raw_years']
    raw_col_name = raw_years[idx]

    # Section 1: Evolusi PDRB & LPE
    st.markdown("""
    <div class="content-box">
        <div class="section-title">📊 Evolusi PDRB & Laju Pertumbuhan Ekonomi Kuningan (2015–2025)</div>
        <div class="section-subtitle">Perbandingan nominal ADHB vs riil ADHK 2010 serta akselerasi dinamika output daerah</div>
    """, unsafe_allow_html=True)
    
    col_t1_a, col_t1_b = st.columns([3, 2])
    
    with col_t1_a:
        # Dual Scale Line Chart: ADHB vs ADHK
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_dual.add_trace(
            go.Scatter(
                x=df_ts['Tahun'],
                y=df_ts['PDRB_ADHB'],
                name="PDRB ADHB (Nominal)",
                mode="lines+markers",
                line=dict(color="#3B82F6", width=3, shape="spline"),
                marker=dict(size=7, color="#60A5FA", symbol="circle"),
                hovertemplate="<b>Tahun %{x}</b><br>PDRB ADHB: Rp %{y:,.2f} Miliar<extra></extra>"
            ),
            secondary_y=False
        )
        
        fig_dual.add_trace(
            go.Scatter(
                x=df_ts['Tahun'],
                y=df_ts['PDRB_ADHK'],
                name="PDRB ADHK 2010 (Riil)",
                mode="lines+markers",
                line=dict(color="#10B981", width=3, dash="dot", shape="spline"),
                marker=dict(size=7, color="#34D399", symbol="diamond"),
                hovertemplate="<b>Tahun %{x}</b><br>PDRB ADHK: Rp %{y:,.2f} Miliar<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Anotasi Covid 2020 shock
        fig_dual.add_annotation(
            x=2020, y=df_ts.loc[df_ts['Tahun']==2020, 'PDRB_ADHK'].values[0],
            text="Guncangan Pandemi 2020<br>(LPE melambat ke 0.11%)",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#EF4444",
            ax=0, ay=-45,
            bgcolor="rgba(239, 68, 68, 0.2)",
            bordercolor="#EF4444",
            font=dict(size=10, color="#FCA5A5")
        )
        
        # Anotasi Akselerasi 2025
        fig_dual.add_annotation(
            x=2025, y=df_ts.loc[df_ts['Tahun']==2025, 'PDRB_ADHB'].values[0],
            text="Akselerasi 2025<br>Rp 41.95 Triliun",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#3B82F6",
            ax=-50, ay=-20,
            bgcolor="rgba(59, 130, 246, 0.2)",
            bordercolor="#3B82F6",
            font=dict(size=10, color="#93C5FD")
        )

        fig_dual.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=1),
            yaxis=dict(title="Nilai PDRB (Miliar Rp)", gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    with col_t1_b:
        # LPE Bar Chart
        colors_lpe = ['#EF4444' if y == 2020 else ('#3B82F6' if y < 2024 else '#10B981') for y in df_ts['Tahun']]
        
        fig_lpe = go.Figure(go.Bar(
            x=df_ts['Tahun'],
            y=df_ts['LPE'],
            marker=dict(
                color=colors_lpe,
                line=dict(color="rgba(255,255,255,0.15)", width=1)
            ),
            text=[f"{val:.2f}%" for val in df_ts['LPE']],
            textposition="outside",
            hovertemplate="<b>Tahun %{x}</b><br>LPE: %{y:.2f}%<extra></extra>"
        ))
        
        fig_lpe.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            title=dict(text="Laju Pertumbuhan Ekonomi Tahunan (%)", font=dict(size=14, color="#E2E8F0")),
            height=380,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickmode='linear', dtick=2),
            yaxis=dict(title="LPE (%)", gridcolor="rgba(255,255,255,0.06)", range=[0, 8.5])
        )
        st.plotly_chart(fig_lpe, use_container_width=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 2: Dekomposisi 17 Sektor Lapangan Usaha & Pengeluaran
    st.markdown(f"""
    <div class="content-box">
        <div class="section-title">🏛️ Dekomposisi 17 Sektor Lapangan Usaha & Pengeluaran Agregat (Tahun {selected_year})</div>
        <div class="section-subtitle">Visualisasi kontribusi sektoral pembentuk nilai tambah bruto serta narasi interpretasi ekonomis</div>
    """, unsafe_allow_html=True)
    
    col_t1_c, col_t1_d = st.columns([3, 2])
    
    # Menyiapkan Data Sektor
    df_sektor_clean = data['df_sektor'][~data['df_sektor']['Sektor'].str.contains('TOTAL', na=False, case=False)].copy()
    df_sektor_clean['Nilai'] = df_sektor_clean[raw_col_name].astype(float)
    df_sektor_clean['Persentase'] = (df_sektor_clean['Nilai'] / df_sektor_clean['Nilai'].sum()) * 100
    
    # Format Nilai Ringkas
    def format_ringkas(val):
        if val >= 1000:
            return f"Rp {val/1000:.2f} Triliun ({val:,.1f} M)"
        return f"Rp {val:,.1f} Miliar"
        
    df_sektor_clean['Nilai_Format'] = df_sektor_clean['Nilai'].apply(format_ringkas)
    df_sektor_clean['Pangsa_Str'] = df_sektor_clean['Persentase'].apply(lambda x: f"{x:.2f}%")
    
    # Mengisi Info & Interpretasi ke Kolom DataFrame
    codes = []
    interpretations = []
    wrapped_tooltips = []
    short_names = []
    
    for _, r in df_sektor_clean.iterrows():
        c, interp, sname = get_sector_info(r['Sektor'])
        codes.append(c)
        interpretations.append(interp)
        short_names.append(sname)
        # Format baris teks interpretasi untuk tooltip (diberi tag <br> setiap ~44 karakter)
        wrapped_text = "<br>".join(textwrap.wrap(interp, width=44))
        wrapped_tooltips.append(wrapped_text)
        
    df_sektor_clean['Kode'] = codes
    df_sektor_clean['Nama_Pendek'] = short_names
    df_sektor_clean['Interpretasi'] = interpretations
    df_sektor_clean['Tooltip_Interp'] = wrapped_tooltips
    df_sektor_clean['Label_Lengkap'] = "[" + df_sektor_clean['Kode'] + "] " + df_sektor_clean['Nama_Pendek']
    
    with col_t1_c:
        # Treemap Sektoral Murni dengan go.Treemap untuk jaminan rendering customdata & hovertemplate
        custom_arr = np.column_stack([
            df_sektor_clean['Pangsa_Str'].values,
            df_sektor_clean['Nilai_Format'].values,
            df_sektor_clean['Tooltip_Interp'].values
        ])
        
        fig_tree = go.Figure(go.Treemap(
            labels=df_sektor_clean['Label_Lengkap'],
            parents=[""] * len(df_sektor_clean),
            values=df_sektor_clean['Nilai'],
            textinfo="label+percent root",
            marker=dict(
                colors=df_sektor_clean['Nilai'],
                colorscale='Blues',
                showscale=False
            ),
            customdata=custom_arr,
            hovertemplate="<b>%{label}</b><br><b>Nilai PDRB:</b> %{customdata[1]}<br><b>Pangsa Kontribusi:</b> %{customdata[0]}<br><br><b>💡 Realitas & Interpretasi BPS:</b><br>%{customdata[2]}<extra></extra>"
        ))
        
        fig_tree.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=420,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    with col_t1_d:
        # Top 5 Sektor Unggulan
        top_5 = df_sektor_clean.sort_values(by='Nilai', ascending=False).head(5)
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=top_5['Label_Lengkap'],
            values=top_5['Nilai'],
            hole=.55,
            marker=dict(colors=['#2563EB', '#3B82F6', '#60A5FA', '#10B981', '#F59E0B']),
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>Rp %{value:,.1f} Miliar (%{percent})<extra></extra>"
        )])
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            title=dict(text=f"Top 5 Sektor Unggulan ({selected_year})", font=dict(size=13, color="#E2E8F0")),
            height=420,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=10))
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    st.markdown("---")
    
    # Sub-section 2.1: Panel Kartu Detail & Interpretasi Naratif Interaktif Sektor
    st.markdown("##### 📖 Eksplorasi Narasi & Interpretasi Ekonomi 17 Sektor Lapangan Usaha")
    
    sector_choices = df_sektor_clean['Label_Lengkap'].tolist()
    selected_sector_label = st.selectbox(
        "Pilih Sektor untuk Melihat Profil & Interpretasi Kebijakan:",
        options=sector_choices,
        index=0,
        help="Pilih salah satu dari 17 lapangan usaha untuk menampilkan angka realisasi, pangsa kontribusi, dan latar belakang struktural ekonominya."
    )
    
    sel_row = df_sektor_clean[df_sektor_clean['Label_Lengkap'] == selected_sector_label].iloc[0]
    # Rank sektor
    rank = df_sektor_clean.sort_values(by='Nilai', ascending=False)['Label_Lengkap'].tolist().index(selected_sector_label) + 1
    
    st.markdown(f"""
    <div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 16px; padding: 20px; margin: 10px 0 20px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px;">
            <div>
                <span style="background: #2563EB; color: #FFFFFF; font-weight: 700; padding: 3px 10px; border-radius: 6px; font-size: 0.8rem; margin-right: 8px;">KATEGORI {sel_row['Kode']}</span>
                <span style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">{sel_row['Sektor']}</span>
            </div>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                Peringkat Sektoral di Kuningan: <span style="color: #F59E0B; font-weight: 700;">#{rank} dari 17 Sektor</span>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 14px;">
            <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 10px; border-left: 3px solid #3B82F6;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Nilai PDRB ({selected_year})</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #60A5FA;">{sel_row['Nilai_Format']}</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 10px; border-left: 3px solid #10B981;">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Pangsa Kontribusi PDRB</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #34D399;">{sel_row['Persentase']:.2f}%</div>
            </div>
        </div>
        <div style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3B82F6; padding: 14px 18px; border-radius: 0 10px 10px 0;">
            <div style="font-weight: 700; color: #93C5FD; font-size: 0.88rem; margin-bottom: 4px;">💡 Makna & Interpretasi Realitas Ekonomi Daerah:</div>
            <div style="font-size: 0.92rem; color: #E2E8F0; line-height: 1.6;">
                <b>{sel_row['Kode']}. {sel_row['Nama_Pendek']} (~{sel_row['Nilai_Format']} / {sel_row['Persentase']:.1f}%):</b> {sel_row['Interpretasi']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sub-section 2.2: Komponen Pengeluaran & ICVAR
    col_t1_e, col_t1_f = st.columns([1.5, 1])
    with col_t1_e:
        st.markdown("##### 🛒 Komponen Pengeluaran ADHK (Miliar Rp)")
        df_peng_clean = data['df_pengeluaran'][~data['df_pengeluaran']['Komponen'].str.contains('TOTAL', na=False, case=False)].copy()
        df_peng_clean['Nilai_Thn'] = df_peng_clean[raw_col_name].astype(float)
        
        fig_peng = px.bar(
            df_peng_clean,
            x='Nilai_Thn',
            y='Komponen',
            orientation='h',
            color='Nilai_Thn',
            color_continuous_scale='Teal',
            labels={'Nilai_Thn': 'Miliar Rp', 'Komponen': ''}
        )
        fig_peng.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_peng, use_container_width=True)
        
    with col_t1_f:
        st.markdown("##### ⚙️ Efisiensi Modal & ICVAR")
        icvar_curr = data['df_icvar'].loc[data['df_icvar']['Parameter'].str.contains('ICVAR', na=False), raw_col_name].values
        icvar_val = float(icvar_curr[0]) if len(icvar_curr) > 0 else 4.0
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 18px; margin-top: 10px;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Koefisien ICVAR (Tahun {selected_year})</div>
            <div style="font-size: 2rem; font-weight: 800; color: #34D399; margin: 4px 0;">{icvar_val:.2f}</div>
            <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                Rasio efisiensi investasi fisik (PMTB) terhadap pertumbuhan nilai tambah riil (ΔY). Rata-rata normal berkisar di rentang <b>3.6 – 4.7</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
