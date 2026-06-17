import streamlit as st
from utils.api_client import list_grades, get_study_tips


def render():
    st.markdown('<div class="page-title">🤖 AI Study Tips</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Personalized subject-specific advice powered by Groq LLM</div>', unsafe_allow_html=True)

    try:
        grades = list_grades()
    except Exception as e:
        st.markdown(f'<div class="alert-error">Could not load grades: {e}</div>', unsafe_allow_html=True)
        return

    if not grades:
        st.markdown('<div class="neu-card-inset">No grade records found. Add some grades first.</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)

    options = {f"{g['student_name']} — {g['subject']} ({g['percentage']}%)": g["id"] for g in grades}
    selected_label = st.selectbox("Select a grade record", list(options.keys()), key="tips_select")
    selected_id = options[selected_label]
    selected_grade = next(g for g in grades if g["id"] == selected_id)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Student", selected_grade["student_name"])
    with col2:
        st.metric("Subject", selected_grade["subject"])
    with col3:
        st.metric("Score", f"{selected_grade['percentage']}% ({selected_grade['grade_letter']})")

    context = st.text_area(
        "Additional context (optional)",
        placeholder="e.g. I struggle with calculus, I have exams in 2 weeks, I study better at night...",
        key="tips_context",
        height=90,
    )

    if st.button("Generate Study Tips", key="btn_gen_tips"):
        with st.spinner("Generating personalized tips..."):
            try:
                result = get_study_tips(selected_id, additional_context=context)
                st.session_state["last_tips"] = result["tips"]
                st.session_state["last_tips_subject"] = selected_grade["subject"]
                st.session_state["last_tips_student"] = selected_grade["student_name"]
            except Exception as e:
                st.markdown(f'<div class="alert-error">AI request failed: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if "last_tips" in st.session_state:
        st.markdown('<div class="ai-response">', unsafe_allow_html=True)
        st.markdown(f"### Study Tips for {st.session_state['last_tips_student']} — {st.session_state['last_tips_subject']}")
        st.markdown('<hr class="neu-divider">', unsafe_allow_html=True)
        st.markdown(st.session_state["last_tips"])
        st.markdown('</div>', unsafe_allow_html=True)
