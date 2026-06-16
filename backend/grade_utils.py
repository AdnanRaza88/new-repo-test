from sqlmodel import Session, select
from models import GradingConfig

DEFAULT_CONFIG = [
    {"label": "A+", "min_percentage": 90, "max_percentage": 100, "is_passing": True},
    {"label": "A",  "min_percentage": 80, "max_percentage": 90,  "is_passing": True},
    {"label": "B",  "min_percentage": 70, "max_percentage": 80,  "is_passing": True},
    {"label": "C",  "min_percentage": 60, "max_percentage": 70,  "is_passing": True},
    {"label": "D",  "min_percentage": 50, "max_percentage": 60,  "is_passing": True},
    {"label": "F",  "min_percentage": 0,  "max_percentage": 50,  "is_passing": False},
]

def compute_percentage(marks_obtained: float, total_marks: float) -> float:
    if total_marks == 0:
        return 0.0
    return round((marks_obtained / total_marks) * 100, 2)

def compute_grade_letter(percentage: float, session: Session) -> str:
    configs = session.exec(select(GradingConfig).order_by(GradingConfig.min_percentage.desc())).all()

    if not configs:
        for cfg in DEFAULT_CONFIG:
            if cfg["min_percentage"] <= percentage <= cfg["max_percentage"]:
                return cfg["label"]
        return "F"

    for cfg in configs:
        if cfg.min_percentage <= percentage <= cfg.max_percentage:
            return cfg.label

    return "F"