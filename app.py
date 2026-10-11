import io, json, os, logging
from xml.sax.saxutils import escape
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pypdf import PdfReader
import docx
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
log = logging.getLogger("copilot")
app = FastAPI(title="AI Career Copilot", version="1.0")


def llm_json(prompt: str, demo: dict) -> dict:
    """Ask Gemini for JSON. Without an API key, return demo data so the UI still works."""
    if not API_KEY:
        return demo
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        r = client.models.generate_content(
            model=MODEL, contents=prompt,
            config={"response_mime_type": "application/json"})
        return json.loads(r.text)
    except Exception as e:
        log.exception("Gemini call failed")
        raise HTTPException(502, f"AI service error: {e}")


def extract_text(name: str, data: bytes) -> str:
    n = (name or "").lower()
    if n.endswith(".pdf"):
        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    if n.endswith(".docx"):
        return "\n".join(p.text for p in docx.Document(io.BytesIO(data)).paragraphs)
    return data.decode("utf-8", "ignore")


@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": not API_KEY, "model": MODEL}


@app.post("/api/analyze")
async def analyze(job_description: str = Form(...), extra_skills: str = Form(""),
                  resume_text: str = Form(""), file: UploadFile | None = File(None)):
    """Agent 1: compare a resume with a job description."""
    text = resume_text
    if file is not None and file.filename:
        try:
            text = extract_text(file.filename, await file.read())
        except Exception:
            raise HTTPException(400, "Could not read that file. Try PDF, DOCX or TXT, or paste the text.")
    if len(text.strip()) < 30:
        raise HTTPException(400, "Resume text is empty. Upload a file or paste your resume.")
    if len(job_description.strip()) < 20:
        raise HTTPException(400, "Please paste a job description.")
    prompt = f"""You are a career coach. Compare the RESUME with the JOB DESCRIPTION.
Extra skills the candidate says they have: {extra_skills or 'none'}
Return ONLY JSON with keys: match_score (integer 0-100), summary (string),
matched_skills (list of strings), missing_skills (list of strings),
resume_improvements (list of strings), action_plan (list of strings),
interview_topics (list of strings).
RESUME:\n{text[:12000]}\n\nJOB DESCRIPTION:\n{job_description[:6000]}"""
    demo = {"match_score": 62, "summary": "DEMO DATA (no API key set). The resume covers core programming skills but lacks some tools named in the job description.",
            "matched_skills": ["Python", "SQL", "Git"], "missing_skills": ["Docker", "REST API design", "Cloud deployment"],
            "resume_improvements": ["Add measurable results to project bullets", "Move skills section to the top"],
            "action_plan": ["Build and deploy one small API project", "Learn Docker basics"],
            "interview_topics": ["REST vs GraphQL", "Database indexing", "Project walkthrough"]}
    r = llm_json(prompt, demo)
    keys = ["matched_skills", "missing_skills", "resume_improvements", "action_plan", "interview_topics"]
    out = {k: [str(x) for x in r.get(k, [])] for k in keys}
    try:
        out["match_score"] = max(0, min(100, int(r.get("match_score", 0))))
    except (TypeError, ValueError):
        out["match_score"] = 0
    out["summary"] = str(r.get("summary", ""))
    return out


@app.post("/api/resume-pdf")
def resume_pdf(result: dict):
    """Download the strategy as a PDF."""
    st = getSampleStyleSheet(); buf = io.BytesIO()
    story = [Paragraph("Career Strategy Report", st["Title"]),
             Paragraph(f"Match score: {int(result.get('match_score', 0))}/100", st["Heading2"]),
             Paragraph(escape(str(result.get("summary", ""))), st["Normal"])]
    for key, title in [("matched_skills", "Matched skills"), ("missing_skills", "Skill gaps"),
                       ("resume_improvements", "Resume improvements"), ("action_plan", "Action plan"),
                       ("interview_topics", "Interview topics")]:
        story += [Spacer(1, 10), Paragraph(title, st["Heading3"])]
        story += [Paragraph("&bull; " + escape(str(i)), st["Normal"]) for i in result.get(key, [])]
    SimpleDocTemplate(buf, pagesize=A4).build(story); buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=career_strategy.pdf"})


class PlanReq(BaseModel):
    missing_skills: list[str]
    days: int = 7
    hours_per_day: int = 2


@app.post("/api/plan")
def plan(req: PlanReq):
    """Agent 2: turn skill gaps into a day-by-day plan."""
    days = max(1, min(req.days, 30)); hrs = max(1, min(req.hours_per_day, 12))
    if not req.missing_skills:
        raise HTTPException(400, "No skills to plan for. Run the analysis first.")
    prompt = f"""Create a {days}-day study plan, {hrs} hours per day, to learn: {', '.join(req.missing_skills)}.
Return ONLY JSON: {{"days":[{{"day":1,"focus":"string","tasks":["string"]}}]}} with exactly {days} entries."""
    skills = req.missing_skills
    demo = {"days": [{"day": d + 1, "focus": skills[d % len(skills)],
                      "tasks": [f"Learn the basics of {skills[d % len(skills)]}", "Do one small hands-on exercise"]}
                     for d in range(days)]}
    r = llm_json(prompt, demo)
    return {"days": [{"day": int(d.get("day", i + 1)), "focus": str(d.get("focus", "")),
                      "tasks": [str(t) for t in d.get("tasks", [])]} for i, d in enumerate(r.get("days", []))]}


class NotifyReq(BaseModel):
    channel: str
    to: str
    message: str


@app.post("/api/notify")
def notify(req: NotifyReq):
    """Stub: swap in a real Email/WhatsApp provider later."""
    if req.channel not in ("email", "whatsapp"):
        raise HTTPException(400, "channel must be email or whatsapp")
    log.info("STUB notify %s -> %s", req.channel, req.to)
    return {"status": "queued (stub, no message actually sent)", "channel": req.channel}


@app.get("/")
def home():
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
