"""
Modul Data Explorer SIMAK-KUNINGAN.
Menyajikan tabel data tabular multi-sheet terpadu dari BPS Kabupaten Kuningan (2015–2025).
"""

import streamlit as st

def render_data_explorer(data: dict):
    """Merender expander eksplorasi data tabular lengkap."""
    with st.expander("📁 Buka Eksplorasi Data Tabular Lengkap (Multi-Sheet BPS 2015–2025)", expanded=False):
        t_sheet1, t_sheet2, t_sheet3, t_sheet4 = st.tabs([
            "📄 Ringkasan Makro",
            "👥 Indikator Sosial",
            "🏢 17 Lapangan Usaha",
            "🛒 Pengeluaran ADHK"
        ])
        with t_sheet1:
            st.dataframe(data['df_makro'], use_container_width=True, hide_index=True)
        with t_sheet2:
            st.dataframe(data['df_sosial'], use_container_width=True, hide_index=True)
        with t_sheet3:
            st.dataframe(data['df_sektor'], use_container_width=True, hide_index=True)
        with t_sheet4:
            st.dataframe(data['df_pengeluaran'], use_container_width=True, hide_index=True)
