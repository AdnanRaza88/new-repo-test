# GradePulse API

**Student Grade Tracker — Project 8**
**Adnan Raza | Roll No. 0267 | Level 2**

Track students and academic performance with AI-powered study tips and daily routine generation.

## Tech Stack

- FastAPI + Pydantic v2 + SQLModel + SQLite
- LangChain + Groq (llama-3.3-70b-versatile)
- Pandas for bulk CSV/Excel upload
- Railway deployment

## Setup

```bash
git clone <your-repo-url>
cd gradepulse-backend
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to .env
uvicorn main:app --reload
```

Open http://localhost:8000/docs

## Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /grades | Create grade record |
| GET | /grades | List all grades |
| GET | /grades/{id} | Get one grade |
| PUT | /grades/{id} | Update grade |
| DELETE | /grades/{id} | Delete grade |
| GET | /grades/student/{roll_number} | All grades for one student |
| POST | /grades/{id}/study-tips | AI study tips |
| POST | /grades/{id}/routine | AI daily routine |
| POST | /grades/bulk-upload | CSV/Excel bulk import |
| GET | /grades/export/csv | Export all as CSV |
| GET | /grades/export/json | Export all as JSON |
| GET | /config | List grading config |
| POST | /config | Create grading threshold |
| DELETE | /config/{id} | Delete grading threshold |

## Sample JSON

**POST /grades**
```json
{
  "student_name": "Ali Hassan",
  "roll_number": "0101",
  "subject": "Mathematics",
  "marks_obtained": 75,
  "total_marks": 100,
  "semester": "Fall 2025",
  "date": "2025-12-01"
}
```

**POST /grades/{id}/study-tips**
```json
{
  "additional_context": "I struggle with calculus topics"
}
```

**POST /grades/{id}/routine**
```json
{
  "free_hours_daily": 4,
  "weakest_subject": "Physics",
  "physical_activity": true,
  "sleep_hours": 7,
  "water_glasses": 6
}
```