import io
import os
from contextlib import asynccontextmanager
from typing import Optional

import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Grade, GradingConfig
from schemas import (
    GradeCreate,
    GradeUpdate,
    GradeResponse,
    GradingConfigCreate,
    GradingConfigResponse,
    StudyTipsRequest,
    RoutineRequest,
    BulkUploadResult,
)
from grade_utils import compute_percentage, compute_grade_letter
from ai_features import get_study_tips, get_daily_routine


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="GradePulse API",
    description="Student Grade Tracker — Adnan Raza (Roll No. 0267)",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── GRADE CRUD ───────────────────────────────────────────────────────────────

@app.post("/grades", response_model=GradeResponse, tags=["Grades"])
def create_grade(payload: GradeCreate, session: Session = Depends(get_session)):
    percentage = compute_percentage(payload.marks_obtained, payload.total_marks)
    grade_letter = compute_grade_letter(percentage, session)

    grade = Grade(
        **payload.model_dump(),
        percentage=percentage,
        grade_letter=grade_letter,
    )
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


@app.get("/grades", response_model=list[GradeResponse], tags=["Grades"])
def list_grades(
    semester: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Grade)
    if semester:
        query = query.where(Grade.semester == semester)
    return session.exec(query).all()


@app.get("/grades/{grade_id}", response_model=GradeResponse, tags=["Grades"])
def get_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade record not found")
    return grade


@app.put("/grades/{grade_id}", response_model=GradeResponse, tags=["Grades"])
def update_grade(grade_id: int, payload: GradeUpdate, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade record not found")

    update_data = payload.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(grade, key, value)

    grade.percentage = compute_percentage(grade.marks_obtained, grade.total_marks)
    grade.grade_letter = compute_grade_letter(grade.percentage, session)

    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


@app.delete("/grades/{grade_id}", tags=["Grades"])
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade record not found")
    session.delete(grade)
    session.commit()
    return {"message": f"Grade record {grade_id} deleted"}


# ─── STUDENT LOOKUP ───────────────────────────────────────────────────────────

@app.get("/grades/student/{roll_number}", response_model=list[GradeResponse], tags=["Students"])
def get_student_grades(roll_number: str, session: Session = Depends(get_session)):
    grades = session.exec(select(Grade).where(Grade.roll_number == roll_number)).all()
    if not grades:
        raise HTTPException(status_code=404, detail=f"No records found for roll number {roll_number}")
    return grades


# ─── AI ENDPOINTS ─────────────────────────────────────────────────────────────

@app.post("/grades/{grade_id}/study-tips", tags=["AI"])
def study_tips(
    grade_id: int,
    payload: StudyTipsRequest,
    session: Session = Depends(get_session),
):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade record not found")

    tips = get_study_tips(
        student_name=grade.student_name,
        subject=grade.subject,
        marks_obtained=grade.marks_obtained,
        total_marks=grade.total_marks,
        percentage=grade.percentage,
        grade_letter=grade.grade_letter,
        additional_context=payload.additional_context or "",
    )
    return {"grade_id": grade_id, "student_name": grade.student_name, "subject": grade.subject, "tips": tips}


@app.post("/grades/{grade_id}/routine", tags=["AI"])
def daily_routine(
    grade_id: int,
    payload: RoutineRequest,
    session: Session = Depends(get_session),
):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade record not found")

    routine = get_daily_routine(
        student_name=grade.student_name,
        subject=grade.subject,
        percentage=grade.percentage,
        weakest_subject=payload.weakest_subject,
        free_hours_daily=payload.free_hours_daily,
        physical_activity=payload.physical_activity,
        sleep_hours=payload.sleep_hours,
        water_glasses=payload.water_glasses,
    )
    return {"grade_id": grade_id, "student_name": grade.student_name, "routine": routine}


# ─── BULK UPLOAD ──────────────────────────────────────────────────────────────

@app.post("/grades/bulk-upload", response_model=BulkUploadResult, tags=["Grades"])
async def bulk_upload(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    filename = file.filename or ""
    if not (filename.endswith(".csv") or filename.endswith(".xlsx") or filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are accepted")

    contents = await file.read()
    errors = []
    rows_added = 0
    rows_skipped = 0

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

    required_cols = {"student_name", "roll_number", "subject", "marks_obtained", "total_marks", "semester", "date"}
    missing = required_cols - set(df.columns.str.strip().str.lower())
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing)}")

    df.columns = df.columns.str.strip().str.lower()

    for idx, row in df.iterrows():
        row_num = idx + 2

        if pd.isna(row.get("student_name")) or str(row["student_name"]).strip() == "":
            errors.append(f"Row {row_num}: student_name is empty — skipped")
            rows_skipped += 1
            continue

        if pd.isna(row.get("roll_number")) or str(row["roll_number"]).strip() == "":
            errors.append(f"Row {row_num}: roll_number is empty — skipped")
            rows_skipped += 1
            continue

        try:
            marks_obtained = float(row["marks_obtained"])
            total_marks = float(row["total_marks"])
        except (ValueError, TypeError):
            errors.append(f"Row {row_num}: marks_obtained or total_marks is not a valid number — skipped")
            rows_skipped += 1
            continue

        if total_marks <= 0:
            errors.append(f"Row {row_num}: total_marks must be greater than 0 — skipped")
            rows_skipped += 1
            continue

        if marks_obtained > total_marks:
            errors.append(f"Row {row_num}: marks_obtained ({marks_obtained}) exceeds total_marks ({total_marks}) — skipped")
            rows_skipped += 1
            continue

        percentage = compute_percentage(marks_obtained, total_marks)
        grade_letter = compute_grade_letter(percentage, session)

        grade = Grade(
            student_name=str(row["student_name"]).strip(),
            roll_number=str(row["roll_number"]).strip(),
            subject=str(row.get("subject", "")).strip(),
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            semester=str(row.get("semester", "")).strip(),
            date=str(row.get("date", "")).strip(),
            percentage=percentage,
            grade_letter=grade_letter,
        )
        session.add(grade)
        rows_added += 1

    session.commit()
    return BulkUploadResult(rows_added=rows_added, rows_skipped=rows_skipped, errors=errors)


# ─── EXPORT ───────────────────────────────────────────────────────────────────

@app.get("/grades/export/csv", tags=["Export"])
def export_csv(session: Session = Depends(get_session)):
    from fastapi.responses import StreamingResponse

    grades = session.exec(select(Grade)).all()
    data = [g.model_dump() for g in grades]
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=gradepulse_export.csv"},
    )


@app.get("/grades/export/json", tags=["Export"])
def export_json(session: Session = Depends(get_session)):
    grades = session.exec(select(Grade)).all()
    return [g.model_dump() for g in grades]


# ─── GRADING CONFIG ───────────────────────────────────────────────────────────

@app.get("/config", response_model=list[GradingConfigResponse], tags=["Config"])
def list_config(session: Session = Depends(get_session)):
    return session.exec(select(GradingConfig).order_by(GradingConfig.min_percentage.desc())).all()


@app.post("/config", response_model=GradingConfigResponse, tags=["Config"])
def create_config(payload: GradingConfigCreate, session: Session = Depends(get_session)):
    config = GradingConfig(**payload.model_dump())
    session.add(config)
    session.commit()
    session.refresh(config)
    return config


@app.delete("/config/{config_id}", tags=["Config"])
def delete_config(config_id: int, session: Session = Depends(get_session)):
    config = session.get(GradingConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Config entry not found")
    session.delete(config)
    session.commit()
    return {"message": f"Config {config_id} deleted"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "GradePulse API"}