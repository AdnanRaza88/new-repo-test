from typing import Optional
from sqlmodel import SQLModel, Field


class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_name: str
    roll_number: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: str
    date: str
    percentage: float = 0.0
    grade_letter: str = ""


class GradingConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    min_percentage: float
    max_percentage: float
    is_passing: bool = True