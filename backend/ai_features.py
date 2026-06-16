import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.7,
    )

def get_study_tips(
    student_name: str,
    subject: str,
    marks_obtained: float,
    total_marks: float,
    percentage: float,
    grade_letter: str,
    additional_context: str = "",
) -> str:
    prompt = ChatPromptTemplate.from_template(
        """You are an experienced academic coach helping a student improve their performance.

Student: {student_name}
Subject: {subject}
Marks: {marks_obtained} / {total_marks}
Percentage: {percentage}%
Grade: {grade_letter}
Additional context from student: {additional_context}

Based on this performance, provide exactly 5 personalized, actionable study tips for this specific subject.
Be specific to the subject, not generic. Consider the grade level — struggling students need foundational advice,
high performers need challenge and depth.

Format your response as:

**Study Tips for {student_name} — {subject}**

1. [Tip title]: [Detailed actionable advice — 2-3 sentences]
2. [Tip title]: [Detailed actionable advice — 2-3 sentences]
3. [Tip title]: [Detailed actionable advice — 2-3 sentences]
4. [Tip title]: [Detailed actionable advice — 2-3 sentences]
5. [Tip title]: [Detailed actionable advice — 2-3 sentences]

**Motivational closing**: One sentence of genuine encouragement."""
    )

    chain = prompt | get_llm() | StrOutputParser()

    return chain.invoke({
        "student_name": student_name,
        "subject": subject,
        "marks_obtained": marks_obtained,
        "total_marks": total_marks,
        "percentage": percentage,
        "grade_letter": grade_letter,
        "additional_context": additional_context or "None provided",
    })

def get_daily_routine(
    student_name: str,
    subject: str,
    percentage: float,
    weakest_subject: str,
    free_hours_daily: float,
    physical_activity: bool,
    sleep_hours: float,
    water_glasses: int,
) -> str:
    prompt = ChatPromptTemplate.from_template(
        """You are a holistic student wellness and academic coach.

Student: {student_name}
Current focus subject: {subject} ({percentage}% score)
Weakest subject: {weakest_subject}
Free hours daily: {free_hours_daily} hours
Physical activity: {physical_activity}
Current sleep: {sleep_hours} hours/night
Water intake: {water_glasses} glasses/day

Create a complete personalized daily routine. Be realistic with the time given.

Format exactly as:

**Daily Routine for {student_name}**

🌅 **Morning Block**
- [Time]: [Activity]
- [Time]: [Activity]

📚 **Study Blocks** (focus on {weakest_subject} first)
- [Time]: [Subject — technique to use]
- [Time]: [Break activity]
- [Time]: [Subject — technique to use]

💪 **Health & Activity**
- Exercise recommendation: [specific advice based on activity level]
- Water target: [specific number and when to drink]

🌙 **Evening & Sleep**
- [Time]: [Wind-down activity]
- [Time]: Sleep — [sleep hygiene tip]

⚡ **Quick Health Tips**
- [2-3 specific health tips based on their current habits]

**Coach's Note**: [One personalized message addressing their specific situation]"""
    )

    chain = prompt | get_llm() | StrOutputParser()

    return chain.invoke({
        "student_name": student_name,
        "subject": subject,
        "percentage": percentage,
        "weakest_subject": weakest_subject,
        "free_hours_daily": free_hours_daily,
        "physical_activity": "Yes" if physical_activity else "No",
        "sleep_hours": sleep_hours,
        "water_glasses": water_glasses,
    })