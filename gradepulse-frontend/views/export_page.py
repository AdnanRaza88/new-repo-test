import json
import streamlit as st
from utils.api_client import export_csv, export_json


def render():
    st.markdown('<div class="page-title">📤 Export Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Download all grade records in your preferred format</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="neu-card">', unsafe_allow_html=True)
        st.markdown("### CSV Export")
        st.markdown("Download all records as a `.csv` file. Compatible with Excel, Google Sheets, and most data tools.")
        if st.button("Download CSV", key="btn_export_csv"):
            try:
                csv_bytes = export_csv()
                st.download_button(
                    label="Click to Save CSV",
                    data=csv_bytes,
                    file_name="gradepulse_export.csv",
                    mime="text/csv",
                    key="dl_csv",
                )
            except Exception as e:
                st.markdown(f'<div class="alert-error">Export failed: {e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="neu-card">', unsafe_allow_html=True)
        st.markdown("### JSON Export")
        st.markdown("Download all records as a `.json` file. Useful for developers or data pipelines.")
        if st.button("Download JSON", key="btn_export_json"):
            try:
                data = export_json()
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    label="Click to Save JSON",
                    data=json_str,
                    file_name="gradepulse_export.json",
                    mime="application/json",
                    key="dl_json",
                )
            except Exception as e:
                st.markdown(f'<div class="alert-error">Export failed: {e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
