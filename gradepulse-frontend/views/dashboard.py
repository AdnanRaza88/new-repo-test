import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.api_client import list_grades, list_config


def render():
    st.markdown('<div class="page-title">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Overview of all student performance</div>', unsafe_allow_html=True)

    try:
        grades = list_grades()
    except Exception as e:
        st.markdown(f'<div class="alert-error">Could not load grades: {e}</div>', unsafe_allow_html=True)
        return

    if not grades:
        st.markdown('<div class="neu-card-inset">No grade records yet. Add grades or upload a CSV to get started.</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(grades)

    total_records = len(df)
    unique_students = df["student_name"].nunique()
    avg_pct = round(df["percentage"].mean(), 1)

    try:
        config = list_config()
        passing_labels = {c["label"] for c in config if c["is_passing"]}
        if not passing_labels:
            passing_labels = {"A+", "A", "B", "C", "D"}
    except Exception:
        passing_labels = {"A+", "A", "B", "C", "D"}

    pass_count = df[df["grade_letter"].isin(passing_labels)].shape[0]
    fail_count = total_records - pass_count

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_records}</div>
            <div class="stat-label">Total Records</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{unique_students}</div>
            <div class="stat-label">Students</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_pct}%</div>
            <div class="stat-label">Avg Percentage</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: {'#38C97A' if fail_count == 0 else '#E05D5D'}">{fail_count}</div>
            <div class="stat-label">Failing Records</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="neu-card">', unsafe_allow_html=True)

        grade_counts = df["grade_letter"].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Count"]

        color_map = {
            "A+": "#38C97A", "A": "#4EC98A",
            "B": "#4A7FE5", "B+": "#6B9AF5",
            "C": "#F5A623", "C+": "#F7B944",
            "D": "#E07B5D", "F": "#E05D5D",
        }
        colors = [color_map.get(g, "#8FA3BF") for g in grade_counts["Grade"]]

        fig = go.Figure(go.Bar(
            x=grade_counts["Grade"],
            y=grade_counts["Count"],
            marker_color=colors,
            text=grade_counts["Count"],
            textposition="outside",
        ))
        fig.update_layout(
            title="Grade Distribution",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#2D3748"),
            showlegend=False,
            height=320,
            margin=dict(t=40, b=20, l=0, r=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#D1DCF0"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="neu-card">', unsafe_allow_html=True)

        subject_avg = df.groupby("subject")["percentage"].mean().round(1).reset_index()
        subject_avg.columns = ["Subject", "Avg %"]
        subject_avg = subject_avg.sort_values("Avg %", ascending=True)

        fig2 = go.Figure(go.Bar(
            x=subject_avg["Avg %"],
            y=subject_avg["Subject"],
            orientation="h",
            marker_color="#4A7FE5",
            text=subject_avg["Avg %"].astype(str) + "%",
            textposition="outside",
        ))
        fig2.update_layout(
            title="Avg % by Subject",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#2D3748"),
            height=320,
            margin=dict(t=40, b=20, l=0, r=0),
            xaxis=dict(showgrid=True, gridcolor="#D1DCF0", range=[0, 110]),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="neu-card">', unsafe_allow_html=True)
    st.markdown("**Top 5 Students by Average Percentage**")

    top5 = (
        df.groupby(["student_name", "roll_number"])["percentage"]
        .mean()
        .round(1)
        .reset_index()
        .sort_values("percentage", ascending=False)
        .head(5)
    )
    top5.columns = ["Student", "Roll No.", "Avg %"]

    for i, row in top5.iterrows():
        col_a, col_b, col_c = st.columns([3, 1, 2])
        with col_a:
            st.write(f"**{row['Student']}**")
        with col_b:
            st.write(row["Roll No."])
        with col_c:
            pct = row["Avg %"]
            color = "#38C97A" if pct >= 70 else ("#F5A623" if pct >= 50 else "#E05D5D")
            st.markdown(f'<span style="color:{color};font-weight:700">{pct}%</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
