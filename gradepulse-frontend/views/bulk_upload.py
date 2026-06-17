import streamlit as st
import pandas as pd
from utils.api_client import bulk_upload


def render():
    st.markdown('<div class="page-title">📂 Bulk Upload</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Import multiple student grades from CSV or Excel</div>', unsafe_allow_html=True)

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("**Required columns in your file:**")
    cols_info = {
        "student_name": "Text",
        "roll_number": "Text",
        "subject": "Text",
        "marks_obtained": "Number",
        "total_marks": "Number",
        "semester": "Text",
        "date": "Text (YYYY-MM-DD)",
    }
    col_a, col_b = st.columns(2)
    items = list(cols_info.items())
    for i, (col, dtype) in enumerate(items):
        target = col_a if i % 2 == 0 else col_b
        with target:
            st.markdown(f"• **`{col}`** — {dtype}")

    st.markdown("**Notes:**")
    st.markdown("- Rows with missing or invalid data are skipped — valid rows are still imported")
    st.markdown("- `percentage` and `grade_letter` are computed automatically — do not include them")
    st.markdown("- `marks_obtained` cannot exceed `total_marks`")
    st.markdown('</div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                preview_df = pd.read_csv(uploaded)
            else:
                preview_df = pd.read_excel(uploaded)

            st.markdown('<div class="neu-card">', unsafe_allow_html=True)
            st.markdown(f"**Preview** — {len(preview_df)} rows detected")
            st.dataframe(preview_df.head(10), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

            uploaded.seek(0)
            file_bytes = uploaded.read()

            if st.button("Import All Valid Rows", key="btn_bulk_import"):
                with st.spinner("Processing file..."):
                    try:
                        result = bulk_upload(file_bytes, uploaded.name)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-number" style="color:#38C97A">{result['rows_added']}</div>
                                <div class="stat-label">Rows Added</div>
                            </div>""", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-number" style="color:#E05D5D">{result['rows_skipped']}</div>
                                <div class="stat-label">Rows Skipped</div>
                            </div>""", unsafe_allow_html=True)
                        with col3:
                            total = result["rows_added"] + result["rows_skipped"]
                            success_rate = round((result["rows_added"] / total * 100) if total > 0 else 0, 1)
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-number">{success_rate}%</div>
                                <div class="stat-label">Success Rate</div>
                            </div>""", unsafe_allow_html=True)

                        if result["errors"]:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("**Skipped rows detail:**")
                            st.markdown('<div class="neu-card-inset">', unsafe_allow_html=True)
                            for err in result["errors"]:
                                st.markdown(f'<div class="alert-error" style="margin-bottom:6px">{err}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="alert-success">All rows imported successfully — no errors found.</div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.markdown(f'<div class="alert-error">Import failed: {e}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f'<div class="alert-error">Could not read file: {e}</div>', unsafe_allow_html=True)
