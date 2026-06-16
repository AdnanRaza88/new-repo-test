import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

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

from views import dashboard, grades, bulk_upload, ai_tips, routine, config, export_page

NAV_ITEMS = [
    ("📊", "Dashboard",     dashboard),
    ("📝", "Grade Records", grades),
    ("📂", "Bulk Upload",   bulk_upload),
    ("🤖", "AI Study Tips", ai_tips),
    ("🌅", "Daily Routine", routine),
    ("⚙️", "Grade Config",  config),
    ("📤", "Export",        export_page),
]

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🎓 GradePulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">STUDENT GRADE TRACKER</div>', unsafe_allow_html=True)

    is_online = health_check()
    dot = "status-online" if is_online else "status-offline"
    label = "API Connected" if is_online else "API Offline"
    st.markdown(
        f'<div style="text-align:center;margin-bottom:20px;font-size:0.8rem;color:#5A6B82">'
        f'<span class="status-dot {dot}"></span>{label}</div>',
        unsafe_allow_html=True,
    )

    if not is_online:
        st.markdown(
            '<div class="alert-error" style="font-size:0.75rem;margin-bottom:16px">'
            'Backend unreachable. Set API_BASE_URL environment variable correctly.'
            '</div>',
            unsafe_allow_html=True,
        )

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Dashboard"

    for icon, label_text, _ in NAV_ITEMS:
        if st.button(f"{icon}  {label_text}", key=f"nav_{label_text}", use_container_width=True):
            st.session_state["active_page"] = label_text
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-size:0.7rem;color:#8FA3BF">'
        'Adnan Raza · Roll No. 0267<br>Level 2 · Project 8'
        '</div>',
        unsafe_allow_html=True,
    )

active = st.session_state.get("active_page", "Dashboard")
active_module = next((mod for _, lbl, mod in NAV_ITEMS if lbl == active), dashboard)

st.markdown('<div style="padding: 32px 40px;">', unsafe_allow_html=True)
active_module.render()
st.markdown('</div>', unsafe_allow_html=True)
