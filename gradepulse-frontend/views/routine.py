import streamlit as st
from utils.api_client import list_grades, get_routine


def render():
    st.markdown('<div class="page-title">🌅 Daily Routine Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">AI builds a complete daily schedule — study, health, sleep, water</div>', unsafe_allow_html=True)

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
    selected_label = st.selectbox("Select a grade record to base the routine on", list(options.keys()), key="routine_select")
    selected_id = options[selected_label]
    selected_grade = next(g for g in grades if g["id"] == selected_id)

    st.markdown('<hr class="neu-divider">', unsafe_allow_html=True)
    st.markdown("**Answer these questions so the AI can personalize your routine:**")

    col1, col2 = st.columns(2)
    with col1:
        free_hours = st.slider("How many free hours do you have daily?", 1.0, 12.0, 4.0, 0.5, key="routine_hours")
        sleep_hours = st.slider("How many hours do you currently sleep?", 4.0, 12.0, 7.0, 0.5, key="routine_sleep")
        water_glasses = st.slider("How many glasses of water do you drink daily?", 0, 20, 6, 1, key="routine_water")
    with col2:
        weakest_subject = st.text_input("Which subject is your weakest?", placeholder="e.g. Physics", key="routine_weak")
        physical_activity = st.radio("Do you do any physical activity?", ["Yes", "No"], key="routine_activity")

    if st.button("Generate My Routine", key="btn_gen_routine"):
        if not weakest_subject.strip():
            st.markdown('<div class="alert-error">Please enter your weakest subject.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Building your personalized daily routine..."):
                try:
                    result = get_routine(selected_id, {
                        "free_hours_daily": free_hours,
                        "weakest_subject": weakest_subject.strip(),
                        "physical_activity": physical_activity == "Yes",
                        "sleep_hours": sleep_hours,
                        "water_glasses": water_glasses,
                    })
                    st.session_state["last_routine"] = result["routine"]
                    st.session_state["last_routine_student"] = selected_grade["student_name"]
                except Exception as e:
                    st.markdown(f'<div class="alert-error">AI request failed: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if "last_routine" in st.session_state:
        st.markdown('<div class="ai-response">', unsafe_allow_html=True)
        st.markdown(f"### Routine for {st.session_state['last_routine_student']}")

        col_h, col_w, col_s = st.columns(3)
        with col_h:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size:1.4rem">{free_hours}h</div>
                <div class="stat-label">Study Time</div>
            </div>""", unsafe_allow_html=True)
        with col_w:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size:1.4rem">{water_glasses}</div>
                <div class="stat-label">Water Glasses</div>
            </div>""", unsafe_allow_html=True)
        with col_s:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="font-size:1.4rem">{sleep_hours}h</div>
                <div class="stat-label">Sleep Target</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="neu-divider">', unsafe_allow_html=True)
        st.markdown(st.session_state["last_routine"])
        st.markdown('</div>', unsafe_allow_html=True)
