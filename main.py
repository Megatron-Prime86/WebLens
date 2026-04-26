from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- TEMPLATE SETUP ---
templates = Jinja2Templates(directory="templates")

# This helper makes sure the date looks nice and doesn't crash the page
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    try:
        scans = db.query(Scan).order_by(Scan.id.desc()).limit(20).all()
        # Pass the current year for the footer too!
        return templates.TemplateResponse("history.html", {
            "request": request, 
            "scans": scans,
            "now": datetime.datetime.utcnow().year
        })
    except Exception as e:
        return HTMLResponse(content=f"Backend Error: {str(e)}", status_code=500)
    finally:
        db.close()

# Keep your /analyze and /history (JSON) routes exactly as they were before
@app.get("/analyze")
def analyze(url: str):
    try:
        headers = {'User-Agent': 'WebLens/1.0'}
        res = requests.get(url, timeout=7, headers=headers)
        tech_list = []
        content = res.text.lower()
        if "wp-content" in content: tech_list.append("WordPress")
        if "react" in content: tech_list.append("React.js")
        if "mediawiki" in content: tech_list.append("MediaWiki")
        
        db = SessionLocal()
        db.add(Scan(url=url, tech=", ".join(tech_list) if tech_list else "Generic Tech"))
        db.commit()
        db.close()
        return {"status": "success", "tech": tech_list}
    except:
        return {"status": "error"}

@app.get("/history")
def get_history_api():
    db = SessionLocal()
    data = db.query(Scan).order_by(Scan.id.desc()).limit(10).all()
    db.close()
    return data