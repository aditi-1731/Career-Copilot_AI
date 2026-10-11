# AI Career Copilot

AI career agents that compare your resume with a job description, show your skill gaps and match score, and build a daily study plan. Built with FastAPI and Google Gemini for SDG 8.
---

## Overview

Many skilled students and job seekers, especially in Tier-2/3 cities, struggle to turn their skills into jobs. They do not know how their resume matches a real job opening, or which skills to learn first. AI Career Copilot gives them personalised, instant guidance: an honest match score, the exact skill gaps, resume fixes, and a daily plan to close the gap.
--- 
## Features
--- 
### Agent 1, Resume Strategist
---

Upload a resume (PDF, DOCX or TXT) or paste the text
Compare it with any job description
Get a match score (0 to 100), matched skills, skill gaps, resume improvements, an action plan and likely interview topics
Download the full strategy as a PDF
---

### Agent 2, Daily Planner
---
Converts the skill gaps into a 3, 7 or 14 day plan with 1, 2 or 4 hours per day
Reminders (stub): Email and WhatsApp endpoint ready to connect to a real provider
---

## How it works
---
The user uploads a resume and pastes a job description.
The backend extracts the resume text (pypdf for PDF, python-docx for DOCX).
Google Gemini compares the two and returns structured JSON.
The UI shows the results, and the user can download a PDF report.
The skill gaps are sent to the planner, which returns a day-by-day timeline.
---

## Tech stack
---
1. Backend
---
- Python
-  FastAPI
-   Uvicorn
- AI	Google Gemini (google-genai SDK)
- File handling
- pypdf
-  python-docx
- PDF report	ReportLab
---

2. Frontend
---
- HTML
- CSS
- JavaScript
---
3. Hosting	Render
---

## Project structure
```
career-copilot/
|-- app.py              # FastAPI app: agents, PDF report, notify stub
|-- static/
|   `-- index.html      # Complete frontend (HTML, CSS, JS)
|-- requirements.txt    # Python dependencies
|-- .env.example        # Template for environment variables
|-- test_smoke.py       # Quick API smoke test (demo mode)
`-- README.md
```
---

## Getting started

Prerequisites: Python 3.10 or newer and a free Gemini API key from Google AI Studio.
```
git clone https://github.com/<your-username>/AI-Career-Copilot.git
cd AI-Career-Copilot
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell (use: source .venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
copy .env.example .env            # then add your GEMINI_API_KEY inside .env
uvicorn app:app --reload
```
```
Open http://127.0.0.1:8000 (interactive API docs at /docs).
```
---
## Environment variables
```
GEMINI_API_KEY	Your Gemini API key. If empty, the app runs in demo mode	empty
```
---
```
GEMINI_MODEL	: 	gemini-3.8-flash
```
---
```
Deployment (Render)
```
---
Build command: 
```
pip install -r requirements.txt
```
---
Start command:
```
uvicorn app:app --host 0.0.0.0 --port $PORT
```
---
## Method	Endpoint	Purpose
```
GET	/api/health	Status and whether demo mode is on
POST	/api/analyze	Agent 1: resume vs job description (multipart form)
POST	/api/resume-pdf	Generate the PDF strategy report
POST	/api/plan	Agent 2: daily study plan from skill gaps
POST	/api/notify	Reminder stub (does not send real messages)
```
---
## Limitations
- No user accounts or database: results are not saved between sessions.
- Email and WhatsApp reminders are a stub and do not send anything yet.
- Scanned or image-only PDFs cannot be read, because there is no OCR.
- AI output can be inaccurate. For example, the model does not know today's date and may wrongly flag recent dates on a resume.
-  Treat results as guidance, not fact.
- Quality depends on how complete the job description is.
- Each analysis is one Gemini call, so it needs internet and is subject to API quotas.
- On a free hosting tier, the app sleeps when idle and the first load can take up to a minute.
---

## Future scope
- User accounts and saved history to track improvement over time
- Real Email and WhatsApp reminders through a provider
- OCR support for scanned resumes
- Resume rewriting suggestions and an ATS-friendly resume builder
- Job recommendations based on skills and location
- Regional language support for students outside English-medium education
- Progress tracking and streaks for the daily plan
- Mock interview practice using the suggested interview topics
---

## Acknowledgements

Built as part of the IBM SkillsBuild x AICTE x BharatCares (CSRBOX) Machine Learning and Applied AI Internship Program 2026.
---

## Author

### **Aditi Tripathi**
