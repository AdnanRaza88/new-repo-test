import streamlit as st
import pandas as pd
from utils.api_client import (
    list_grades, create_grade, update_grade, delete_grade, get_student_grades
)


def grade_badge(letter: str) -> str:
    letter_upper = letter.upper()
    css_class = "grade-a" if letter_upper in ("A", "A+") else \
                "grade-b" if letter_upper.startswith("B") else \
                "grade-c" if letter_upper.startswith("C") else \
                "grade-f"
    return f'<span class="grade-badge {css_class}">{letter}</span>'


def render():
    st.markdown('<div class="page-title">📝 Grade Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add, search, update, and remove grade entries</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["All Grades", "Add Grade", "Student Lookup"])

    with tab1:
        _render_all_grades()

    with tab2:
        _render_add_grade()

    with tab3:
        _render_student_lookup()


def _render_all_grades():
    col_filter, col_refresh = st.columns([3, 1])
    with col_filter:
        semester_filter = st.text_input("Filter by semester", placeholder="e.g. Fall 2025")
    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        refresh = st.button("Refresh", key="refresh_grades")

    try:
        grades = list_grades(semester=semester_filter if semester_filter else None)
    except Exception as e:
        st.markdown(f'<div class="alert-error">Failed to load grades: {e}</div>', unsafe_allow_html=True)
        return

    if not grades:
        st.markdown('<div class="neu-card-inset">No grade records found.</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(grades)
    display_cols = ["id", "student_name", "roll_number", "subject", "marks_obtained", "total_marks", "percentage", "grade_letter", "semester", "date"]
    df = df[display_cols]
    df.columns = ["ID", "Student", "Roll No.", "Subject", "Marks", "Total", "Percentage", "Grade", "Semester", "Date"]

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Edit / Delete a record**")

    record_ids = [g["id"] for g in grades]
    selected_id = st.selectbox("Select record ID", record_ids, key="select_edit_id")

    if selected_id:
        selected = next((g for g in grades if g["id"] == selected_id), None)
        if selected:
            with st.expander("Edit this record", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    new_marks = st.number_input("Marks Obtained", value=float(selected["marks_obtained"]), key="edit_marks")
                    new_total = st.number_input("Total Marks", value=float(selected["total_marks"]), key="edit_total")
                    new_semester = st.text_input("Semester", value=selected["semester"], key="edit_sem")
                with col2:
                    new_subject = st.text_input("Subject", value=selected["subject"], key="edit_subj")
                    new_date = st.text_input("Date", value=selected["date"], key="edit_date")

                col_save, col_del = st.columns(2)
                with col_save:
                    if st.button("Save Changes", key="btn_save_edit"):
                        try:
                            update_grade(selected_id, {
                                "marks_obtained": new_marks,
                                "total_marks": new_total,
                                "semester": new_semester,
                                "subject": new_subject,
                                "date": new_date,
                            })
                            st.markdown('<div class="alert-success">Record updated successfully.</div>', unsafe_allow_html=True)
                            st.rerun()
                        except Exception as e:
                            st.markdown(f'<div class="alert-error">Update failed: {e}</div>', unsafe_allow_html=True)

                with col_del:
                    if st.button("Delete Record", key="btn_delete", type="secondary"):
                        st.session_state["confirm_delete"] = selected_id

                    if st.session_state.get("confirm_delete") == selected_id:
                        st.warning("Are you sure? This cannot be undone.")
                        if st.button("Yes, Delete", key="confirm_yes"):
                            try:
                                delete_grade(selected_id)
                                st.session_state.pop("confirm_delete", None)
                                st.rerun()
                            except Exception as e:
                                st.markdown(f'<div class="alert-error">Delete failed: {e}</div>', unsafe_allow_html=True)


def _render_add_grade():
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name", placeholder="Ali Hassan", key="add_name")
        roll = st.text_input("Roll Number", placeholder="0101", key="add_roll")
        subject = st.text_input("Subject", placeholder="Mathematics", key="add_subj")
    with col2:
        marks = st.number_input("Marks Obtained", min_value=0.0, step=0.5, key="add_marks")
        total = st.number_input("Total Marks", min_value=1.0, value=100.0, step=0.5, key="add_total")
        semester = st.text_input("Semester", placeholder="Fall 2025", key="add_sem")
        date = st.text_input("Date", placeholder="2025-12-01", key="add_date")

    if st.button("Add Grade Record", key="btn_add_grade"):
        if not all([name, roll, subject, semester, date]):
            st.markdown('<div class="alert-error">Please fill in all required fields.</div>', unsafe_allow_html=True)
        elif marks > total:
            st.markdown('<div class="alert-error">Marks obtained cannot exceed total marks.</div>', unsafe_allow_html=True)
        else:
            try:
                result = create_grade({
                    "student_name": name,
                    "roll_number": roll,
                    "subject": subject,
                    "marks_obtained": marks,
                    "total_marks": total,
                    "semester": semester,
                    "date": date,
                })
                pct = result.get("percentage", 0)
                gl = result.get("grade_letter", "")
                st.markdown(
                    f'<div class="alert-success">Record added — {name} scored {pct}% ({gl}) in {subject}.</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.markdown(f'<div class="alert-error">Failed to add record: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def _render_student_lookup():
    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    roll = st.text_input("Enter Roll Number", placeholder="0101", key="lookup_roll")

    if st.button("Search Student", key="btn_lookup"):
        if not roll.strip():
            st.markdown('<div class="alert-error">Please enter a roll number.</div>', unsafe_allow_html=True)
        else:
            try:
                grades = get_student_grades(roll.strip())
                if not grades:
                    st.markdown('<div class="alert-error">No records found for this roll number.</div>', unsafe_allow_html=True)
                else:
                    student_name = grades[0]["student_name"]
                    avg_pct = round(sum(g["percentage"] for g in grades) / len(grades), 1)

                    st.markdown(f"**{student_name}** — Roll: {roll} | {len(grades)} subjects | Avg: **{avg_pct}%**")
                    st.markdown('<hr class="neu-divider">', unsafe_allow_html=True)

                    for g in grades:
                        col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 1])
                        pct = g["percentage"]
                        bar_color = "#38C97A" if pct >= 70 else ("#F5A623" if pct >= 50 else "#E05D5D")
                        with col_a:
                            st.write(f"**{g['subject']}**")
                            st.markdown(
                                f'<div class="progress-bar-container"><div class="progress-bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>',
                                unsafe_allow_html=True,
                            )
                        with col_b:
                            st.write(f"{g['marks_obtained']}/{g['total_marks']}")
                        with col_c:
                            st.write(f"{pct}%")
                        with col_d:
                            st.markdown(grade_badge(g["grade_letter"]), unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="alert-error">Error: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
