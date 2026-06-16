from typing import Optional
from pydantic import BaseModel, Field, model_validator


class GradeCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    marks_obtained: float = Field(ge=0)
    total_marks: float = Field(gt=0)
    semester: str
    date: str

    @model_validator(mode="after")
    def marks_must_not_exceed_total(self):
        if self.marks_obtained > self.total_marks:
            raise ValueError("marks_obtained cannot exceed total_marks")
        return self


class GradeUpdate(BaseModel):
    student_name: Optional[str] = None
    roll_number: Optional[str] = None
    subject: Optional[str] = None
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    semester: Optional[str] = None
    date: Optional[str] = None


class GradeResponse(BaseModel):
    id: int
    student_name: str
    roll_number: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: str
    date: str
    percentage: float
    grade_letter: str

    model_config = {"from_attributes": True}


class GradingConfigCreate(BaseModel):
    label: str = Field(min_length=1)
    min_percentage: float = Field(ge=0, le=100)
    max_percentage: float = Field(ge=0, le=100)
    is_passing: bool = True

    @model_validator(mode="after")
    def min_must_be_less_than_max(self):
        if self.min_percentage >= self.max_percentage:
            raise ValueError("min_percentage must be less than max_percentage")
        return self


class GradingConfigResponse(BaseModel):
    id: int
    label: str
    min_percentage: float
    max_percentage: float
    is_passing: bool

    model_config = {"from_attributes": True}


class StudyTipsRequest(BaseModel):
    additional_context: Optional[str] = None


class RoutineRequest(BaseModel):
    free_hours_daily: float = Field(gt=0, le=24)
    weakest_subject: str
    physical_activity: bool = True
    sleep_hours: float = Field(gt=0, le=12)
    water_glasses: int = Field(ge=0, le=20)


class BulkUploadResult(BaseModel):
    rows_added: int
    rows_skipped: int
    errors: list[str]