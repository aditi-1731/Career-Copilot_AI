from fastapi.testclient import TestClient
import app as m
c=TestClient(m.app)
print(c.get("/api/health").json(), c.get("/").status_code)
r=c.post("/api/analyze",data={"job_description":"Looking for a Python developer with Docker and REST API experience","resume_text":"Aditi, CSE student. Built projects in Python, SQL and Git. "*3}); print(r.status_code, r.json()["match_score"])
print(c.post("/api/analyze",data={"job_description":"x"}).status_code)
d=r.json(); p=c.post("/api/resume-pdf",json=d); print(p.status_code,p.headers["content-type"],len(p.content))
pl=c.post("/api/plan",json={"missing_skills":d["missing_skills"],"days":3}); print(pl.status_code,len(pl.json()["days"]))
print(c.post("/api/notify",json={"channel":"email","to":"a@b.com","message":"hi"}).json())
print(c.post("/api/analyze",data={"job_description":"Python developer needed with Docker skills","resume_text":""},files={"file":("r.txt",b"Python SQL Git developer with several projects and internships completed")}).status_code)
