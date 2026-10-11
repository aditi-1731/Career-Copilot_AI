# AI Career Copilot

AI agents that compare a resume with a job description and turn the skill gaps into a daily study plan.
Built by Aditi Tripathi, ABES Engineering College, for SDG 8 (Decent Work and Economic Growth), IBM SkillsBuild Masterclass 5.

## Features
- **Agent 1, Resume Strategist:** upload a resume (PDF, DOCX or TXT) plus a job description, get a match score, skill gaps, resume improvements, interview topics and a downloadable PDF strategy.
- **Agent 2, Daily Planner:** converts skill gaps into a 3, 7 or 14 day plan.
- **Reminders:** Email and WhatsApp behind a stub endpoint (swap in a real provider later).
- **Demo mode:** runs without an API key using sample data.

## Tech stack
FastAPI, Google Gemini (google-genai), pypdf, python-docx, ReportLab, HTML/JavaScript.

## Run locally (Windows PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # then put your GEMINI_API_KEY in .env
uvicorn app:app --reload
```
Open http://127.0.0.1:8000 (API docs at /docs).

## Deploy on Render
Build: `pip install -r requirements.txt`  Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
Add `GEMINI_API_KEY` as an environment variable.

## API
`POST /api/analyze`, `POST /api/resume-pdf`, `POST /api/plan`, `POST /api/notify` (stub), `GET /api/health`
 
## Author
### **Aditi Tripathi**