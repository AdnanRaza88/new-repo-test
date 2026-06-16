# GradePulse — Frontend

**Streamlit UI for Student Grade Tracker**
**Adnan Raza | Roll No. 0267 | Level 2 | Project 8**

## Setup

```bash
git clone <your-frontend-repo-url>
cd gradepulse-frontend
pip install -r requirements.txt
cp .env.example .env
# Set API_BASE_URL in .env to your deployed backend URL
streamlit run app.py
```

## Environment Variables

| Variable | Value |
|----------|-------|
| `API_BASE_URL` | URL of deployed FastAPI backend |

## Pages

- Dashboard — stats, charts, top students
- Grade Records — add, edit, delete, search by roll number
- Bulk Upload — CSV/Excel import with Pandas validation
- AI Study Tips — LangChain + Groq personalized tips per subject
- Daily Routine — AI full day planner with health, water, sleep
- Grade Config — custom grade thresholds and pass/fail settings
- Export — download all data as CSV or JSON
