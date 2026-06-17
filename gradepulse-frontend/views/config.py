import streamlit as st
from utils.api_client import list_config, create_config, delete_config


DEFAULT_THRESHOLDS = [
    {"label": "A+", "min_percentage": 90, "max_percentage": 100, "is_passing": True},
    {"label": "A",  "min_percentage": 80, "max_percentage": 90,  "is_passing": True},
    {"label": "B",  "min_percentage": 70, "max_percentage": 80,  "is_passing": True},
    {"label": "C",  "min_percentage": 60, "max_percentage": 70,  "is_passing": True},
    {"label": "D",  "min_percentage": 50, "max_percentage": 60,  "is_passing": True},
    {"label": "F",  "min_percentage": 0,  "max_percentage": 50,  "is_passing": False},
]


def render():
    st.markdown('<div class="page-title">⚙️ Grading Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Define your own grade thresholds and pass/fail boundaries</div>', unsafe_allow_html=True)

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("ℹ️ If no configuration is set, the system uses default thresholds (A+=90–100, A=80–90, B=70–80, C=60–70, D=50–60, F=0–50).")
    st.markdown('</div>', unsafe_allow_html=True)

    try:
        configs = list_config()
    except Exception as e:
        st.markdown(f'<div class="alert-error">Failed to load config: {e}</div>', unsafe_allow_html=True)
        return

    if configs:
        st.markdown('<div class="neu-card">', unsafe_allow_html=True)
        st.markdown("**Current Grading Thresholds**")

        for cfg in configs:
            col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
            with col1:
                css = "grade-a" if cfg["label"] in ("A", "A+") else \
                      "grade-b" if cfg["label"].startswith("B") else \
                      "grade-c" if cfg["label"].startswith("C") else "grade-f"
                st.markdown(f'<span class="grade-badge {css}">{cfg["label"]}</span>', unsafe_allow_html=True)
            with col2:
                st.write(f"Min: {cfg['min_percentage']}%")
            with col3:
                st.write(f"Max: {cfg['max_percentage']}%")
            with col4:
                status = "✅ Passing" if cfg["is_passing"] else "❌ Failing"
                st.write(status)
            with col5:
                if st.button("✕", key=f"del_cfg_{cfg['id']}"):
                    try:
                        delete_config(cfg["id"])
                        st.rerun()
                    except Exception as e:
                        st.markdown(f'<div class="alert-error">Delete failed: {e}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="neu-card-inset">No custom config set — using system defaults.</div>', unsafe_allow_html=True)

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("**Add a Grade Threshold**")

    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        label = st.text_input("Label", placeholder="A+", key="cfg_label")
    with col2:
        min_pct = st.number_input("Min %", min_value=0.0, max_value=100.0, value=0.0, key="cfg_min")
    with col3:
        max_pct = st.number_input("Max %", min_value=0.0, max_value=100.0, value=50.0, key="cfg_max")
    with col4:
        is_passing = st.selectbox("Is Passing?", ["Yes", "No"], key="cfg_pass")

    if st.button("Add Threshold", key="btn_add_cfg"):
        if not label.strip():
            st.markdown('<div class="alert-error">Label is required.</div>', unsafe_allow_html=True)
        elif min_pct >= max_pct:
            st.markdown('<div class="alert-error">Min percentage must be less than max percentage.</div>', unsafe_allow_html=True)
        else:
            try:
                create_config({
                    "label": label.strip().upper(),
                    "min_percentage": min_pct,
                    "max_percentage": max_pct,
                    "is_passing": is_passing == "Yes",
                })
                st.markdown('<div class="alert-success">Threshold added.</div>', unsafe_allow_html=True)
                st.rerun()
            except Exception as e:
                st.markdown(f'<div class="alert-error">Failed: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("**Load Default Thresholds (replaces nothing — just adds)**")
    if st.button("Load Defaults", key="btn_load_defaults"):
        added = 0
        for threshold in DEFAULT_THRESHOLDS:
            try:
                create_config(threshold)
                added += 1
            except Exception:
                pass
        st.markdown(f'<div class="alert-success">{added} default thresholds added.</div>', unsafe_allow_html=True)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
