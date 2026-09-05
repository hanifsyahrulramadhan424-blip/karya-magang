"""
Modul Data Loader & Preprocessing SIMAK-KUNINGAN.
Mengelola pemuatan berkas Excel multi-sheet BPS dengan caching @st.cache_data.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_all_datasets(file_path: str = "PDRB_dan_Indikator_Sosial_Ekonomi_Kuningan_2015_2025_Final.xlsx") -> dict:
    """
    Memuat seluruh lembar kerja data makroekonomi dan sosial BPS Kuningan (2015-2025).
    Header BPS disesuaikan pada header=3 untuk membaca tabel secara presisi.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Berkas data '{file_path}' tidak ditemukan.")
        
    # Membaca seluruh sheet terkait
    df_makro_raw = pd.read_excel(file_path, sheet_name='Ringkasan Makro', header=3)
    df_sosial_raw = pd.read_excel(file_path, sheet_name='Indikator Sosial Ekonomi', header=3)
    df_sektor_raw = pd.read_excel(file_path, sheet_name='PDRB Lapangan Usaha (ADHB)', header=3)
    df_pengeluaran_raw = pd.read_excel(file_path, sheet_name='Pengeluaran ADHK (Miliar)', header=3)
    df_icvar_raw = pd.read_excel(file_path, sheet_name='Analisis ICVAR', header=3)
    df_coicop_raw = pd.read_excel(file_path, sheet_name='Rincian PK-RT (7 COICOP)', header=3)

    raw_years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024*', '2025**']
    int_years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    # 1. Ringkasan Makro
    df_makro = df_makro_raw.dropna(subset=['Indikator Ekonomi']).copy()
    df_makro['Indikator'] = df_makro['Indikator Ekonomi'].astype(str).str.strip()
    
    # 2. Indikator Sosial
    df_sosial = df_sosial_raw.dropna(subset=['Indikator Sosial Ekonomi']).copy()
    df_sosial['Indikator'] = df_sosial['Indikator Sosial Ekonomi'].astype(str).str.strip()
    df_sosial = df_sosial[~df_sosial['Indikator'].str.contains('TABEL PENDUKUNG|Catatan', na=False, case=False)].copy()
    if 'No' in df_sosial.columns:
        df_sosial['No'] = df_sosial['No'].astype(str)
        
    # Clean numeric types for raw_years
    for y in raw_years:
        if y in df_makro.columns:
            df_makro[y] = pd.to_numeric(df_makro[y], errors='coerce')
        if y in df_sosial.columns:
            df_sosial[y] = pd.to_numeric(df_sosial[y], errors='coerce')
        if y in df_sektor_raw.columns:
            df_sektor_raw[y] = pd.to_numeric(df_sektor_raw[y], errors='coerce')
        if y in df_pengeluaran_raw.columns:
            df_pengeluaran_raw[y] = pd.to_numeric(df_pengeluaran_raw[y], errors='coerce')
    
    # 3. Lapangan Usaha (17 Sektor)
    df_sektor = df_sektor_raw.dropna(subset=['Kategori Lapangan Usaha']).copy()
    df_sektor['Sektor'] = df_sektor['Kategori Lapangan Usaha'].astype(str).str.strip()
    
    # 4. Pengeluaran ADHK
    df_pengeluaran = df_pengeluaran_raw.dropna(subset=['Komponen Pengeluaran']).copy()
    df_pengeluaran['Komponen'] = df_pengeluaran['Komponen Pengeluaran'].astype(str).str.strip()
    if 'No' in df_pengeluaran.columns:
        df_pengeluaran['No'] = df_pengeluaran['No'].astype(str)
    
    # 5. ICVAR
    df_icvar = df_icvar_raw.dropna(subset=['Uraian Parameter']).copy()
    df_icvar['Parameter'] = df_icvar['Uraian Parameter'].astype(str).str.strip()
    
    # 6. COICOP
    df_coicop = df_coicop_raw.dropna(subset=['Kelompok Konsumsi COICOP']).copy()
    df_coicop['Kelompok'] = df_coicop['Kelompok Konsumsi COICOP'].astype(str).str.strip()

    # Membangun Dataframe Deret Waktu Terpadu
    ts_dict = {'Tahun': int_years, 'Year_Label': raw_years}
    
    def extract_row(df, col_name, val_name):
        match = df[df[col_name].str.lower().str.contains(val_name.lower(), na=False)]
        if not match.empty:
            return match.iloc[0][raw_years].values.astype(float)
        return np.zeros(len(raw_years))

    ts_dict['PDRB_ADHB'] = extract_row(df_makro, 'Indikator', 'Harga Berlaku')
    ts_dict['PDRB_ADHK'] = extract_row(df_makro, 'Indikator', 'Harga Konstan')
    ts_dict['LPE'] = extract_row(df_makro, 'Indikator', 'Laju Pertumbuhan Ekonomi')
    ts_dict['PDRB_Kapita_ADHB'] = extract_row(df_makro, 'Indikator', 'PDRB Per Kapita ADHB')
    ts_dict['PDRB_Kapita_ADHK'] = extract_row(df_makro, 'Indikator', 'PDRB Per Kapita ADHK 2010')
    ts_dict['Penduduk'] = extract_row(df_makro, 'Indikator', 'Jumlah Penduduk')
    ts_dict['Deflator'] = extract_row(df_makro, 'Indikator', 'Indeks Harga Implisit')

    ts_dict['Kemiskinan_P0'] = extract_row(df_sosial, 'Indikator', 'Persentase Penduduk Miskin')
    ts_dict['Kedalaman_P1'] = extract_row(df_sosial, 'Indikator', 'Kedalaman Kemiskinan')
    ts_dict['Keparahan_P2'] = extract_row(df_sosial, 'Indikator', 'Keparahan Kemiskinan')
    ts_dict['Garis_Kemiskinan'] = extract_row(df_sosial, 'Indikator', 'Garis Kemiskinan')
    ts_dict['TPT'] = extract_row(df_sosial, 'Indikator', 'Tingkat Pengangguran Terbuka')
    ts_dict['Proporsi_Informal'] = extract_row(df_sosial, 'Indikator', 'Sektor Informal')
    ts_dict['Proporsi_Formal'] = extract_row(df_sosial, 'Indikator', 'Sektor Formal')
    ts_dict['TPAK'] = extract_row(df_sosial, 'Indikator', 'TPAK')
    ts_dict['RLS'] = extract_row(df_sosial, 'Indikator', 'Rata-rata Lama Sekolah')
    ts_dict['HLS'] = extract_row(df_sosial, 'Indikator', 'Harapan Lama Sekolah')
    ts_dict['UHH'] = extract_row(df_sosial, 'Indikator', 'Umur Harapan Hidup')
    ts_dict['Pengeluaran_Riil'] = extract_row(df_sosial, 'Indikator', 'Pengeluaran Riil per Kapita')
    
    # Sektoral Sektor Utama
    ts_dict['Pertanian'] = extract_row(df_sektor, 'Sektor', 'Pertanian')
    ts_dict['Perdagangan'] = extract_row(df_sektor, 'Sektor', 'Perdagangan')
    ts_dict['Transportasi'] = extract_row(df_sektor, 'Sektor', 'Transportasi')
    ts_dict['Konstruksi'] = extract_row(df_sektor, 'Sektor', 'Konstruksi')
    ts_dict['Industri'] = extract_row(df_sektor, 'Sektor', 'Industri Pengolahan')
    ts_dict['Pendidikan'] = extract_row(df_sektor, 'Sektor', 'Jasa Pendidikan')

    df_ts = pd.DataFrame(ts_dict)
    
    return {
        'df_ts': df_ts,
        'df_makro': df_makro,
        'df_sosial': df_sosial,
        'df_sektor': df_sektor,
        'df_pengeluaran': df_pengeluaran,
        'df_icvar': df_icvar,
        'df_coicop': df_coicop,
        'raw_years': raw_years,
        'int_years': int_years
    }
