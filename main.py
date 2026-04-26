from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime, requests, uvicorn, os

# --- DB SETUP ---
DB_PATH = os.path.join(os.getcwd(), "weblens.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    tech = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- APP SETUP ---
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Setup for HTML Templates (Dashboard)
templates = Jinja2Templates(directory="templates")

# --- ROUTES ---

# 1. NEW: The Beautiful Dashboard (For Humans/LinkedIn)
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    scans = db.query(Scan).order_by(Scan.id.desc()).limit(20).all()
    db.close()
    return templates.TemplateResponse("history.html", {"request": request, "scans": scans})

# 2. The Analysis Logic
@app.get("/analyze")
def analyze(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebLens/1.0'}
        res = requests.get(url, timeout=5, headers=headers)
        content = res.text.lower()
        tech_list = []

        if "wp-content" in content: tech_list.append("WordPress")
        if "react" in content: tech_list.append("React.js")
        if "mediawiki" in content: tech_list.append("MediaWiki")
        if "bootstrap" in content: tech_list.append("Bootstrap")
        if "jquery" in content: tech_list.append("jQuery")
        
        server = res.headers.get("Server", "Generic/Cloudflare")
        tech_list.append(server)

        db = SessionLocal()
        db.add(Scan(url=url, tech=", ".join(tech_list)))
        db.commit()
        db.close()

        return {"status": "success", "tech": tech_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. The API Endpoint (For your Extension's History Tab)
@app.get("/history")
def get_history_api():
    db = SessionLocal()
    data = db.query(Scan).order_by(Scan.id.desc()).limit(10).all()
    db.close()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)