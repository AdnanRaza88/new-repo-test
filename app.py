import streamlit as st
from assets.styles import NEUMORPHIC_CSS
from utils.api_client import health_check

st.set_page_config(
    page_title="GradePulse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(NEUMORPHIC_CSS, unsafe_allow_html=True)

from pages import dashboard, grades, bulk_upload, ai_tips, routine, config, export_page

NAV_ITEMS = [
    ("📊", "Dashboard",       dashboard),
    ("📝", "Grade Records",   grades),
    ("📂", "Bulk Upload",     bulk_upload),
    ("🤖", "AI Study Tips",   ai_tips),
    ("🌅", "Daily Routine",   routine),
    ("⚙️", "Grade Config",    config),
    ("📤", "Export",          export_page),
]

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎓 GradePulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">STUDENT GRADE TRACKER</div>', unsafe_allow_html=True)

    is_online = health_check()
    status_color = "status-online" if is_online else "status-offline"
    status_text = "API Connected" if is_online else "API Offline"
    st.markdown(
        f'<div style="text-align:center;margin-bottom:20px;font-size:0.8rem;color:#5A6B82">'
        f'<span class="status-dot {status_color}"></span>{status_text}</div>',
        unsafe_allow_html=True,
    )

    if not is_online:
        st.markdown(
            '<div class="alert-error" style="font-size:0.75rem;margin-bottom:16px">'
            'Cannot reach the backend API. Check your API_BASE_URL environment variable.'
            '</div>',
            unsafe_allow_html=True,
        )

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"

    for icon, label, _ in NAV_ITEMS:
        is_active = st.session_state["active_page"] == label
        active_class = "active" if is_active else ""
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{label}",
            use_container_width=True,
        ):
            st.session_state["active_page"] = label
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-size:0.7rem;color:#8FA3BF">'
        'Adnan Raza · Roll No. 0267<br>Level 2 · Project 8'
        '</div>',
        unsafe_allow_html=True,
    )

active_label = st.session_state.get("active_page", "Dashboard")
active_module = next((mod for _, label, mod in NAV_ITEMS if label == active_label), dashboard)

st.markdown('<div style="padding: 32px 40px;">', unsafe_allow_html=True)
active_module.render()
st.markdown('</div>', unsafe_allow_html=True)
