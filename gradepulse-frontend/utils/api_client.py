import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def _url(path: str) -> str:
    return f"{API_BASE_URL}{path}"


def create_grade(data: dict):
    r = requests.post(_url("/grades"), json=data, timeout=15)
    r.raise_for_status()
    return r.json()


def list_grades(semester: str = None):
    params = {}
    if semester:
        params["semester"] = semester
    r = requests.get(_url("/grades"), params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def get_grade(grade_id: int):
    r = requests.get(_url(f"/grades/{grade_id}"), timeout=15)
    r.raise_for_status()
    return r.json()


def update_grade(grade_id: int, data: dict):
    r = requests.put(_url(f"/grades/{grade_id}"), json=data, timeout=15)
    r.raise_for_status()
    return r.json()


def delete_grade(grade_id: int):
    r = requests.delete(_url(f"/grades/{grade_id}"), timeout=15)
    r.raise_for_status()
    return r.json()


def get_student_grades(roll_number: str):
    r = requests.get(_url(f"/grades/student/{roll_number}"), timeout=15)
    r.raise_for_status()
    return r.json()


def get_study_tips(grade_id: int, additional_context: str = ""):
    r = requests.post(
        _url(f"/grades/{grade_id}/study-tips"),
        json={"additional_context": additional_context},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def get_routine(grade_id: int, payload: dict):
    r = requests.post(_url(f"/grades/{grade_id}/routine"), json=payload, timeout=60)
    r.raise_for_status()
    return r.json()


def bulk_upload(file_bytes: bytes, filename: str):
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = "text/csv" if ext == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    r = requests.post(
        _url("/grades/bulk-upload"),
        files={"file": (filename, file_bytes, mime)},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def export_csv():
    r = requests.get(_url("/grades/export/csv"), timeout=30)
    r.raise_for_status()
    return r.content


def export_json():
    r = requests.get(_url("/grades/export/json"), timeout=30)
    r.raise_for_status()
    return r.json()


def list_config():
    r = requests.get(_url("/config"), timeout=10)
    r.raise_for_status()
    return r.json()


def create_config(data: dict):
    r = requests.post(_url("/config"), json=data, timeout=10)
    r.raise_for_status()
    return r.json()


def delete_config(config_id: int):
    r = requests.delete(_url(f"/config/{config_id}"), timeout=10)
    r.raise_for_status()
    return r.json()


def health_check():
    try:
        r = requests.get(_url("/health"), timeout=5)
        return r.status_code == 200
    except Exception:
        return False
