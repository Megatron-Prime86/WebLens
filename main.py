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
templates = Jinja2Templates(directory="templates")

# --- FIXED DASHBOARD ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()
    try:
        scans_from_db = db.query(Scan).order_by(Scan.id.desc()).limit(20).all()
        
        # In modern FastAPI, we pass request as the first argument, 
        # AND context as the second.
        return templates.TemplateResponse(
            request=request, 
            name="history.html", 
            context={"scans": scans_from_db}
        )
    except Exception as e:
        return HTMLResponse(content=f"Dashboard Error: {str(e)}", status_code=500)
    finally:
        db.close()

@app.get("/analyze")
async def analyze(url: str):
    try:
        headers = {'User-Agent': 'WebLens/1.0'}
        res = requests.get(url, timeout=7, headers=headers)
        content = res.text.lower()
        tech_list = []
        if "wp-content" in content: tech_list.append("WordPress")
        if "react" in content: tech_list.append("React.js")
        if "mediawiki" in content: tech_list.append("MediaWiki")
        
        server = res.headers.get("Server", "Cloudflare")
        tech_list.append(server)

        db = SessionLocal()
        db.add(Scan(url=url, tech=", ".join(tech_list)))
        db.commit()
        db.close()
        return {"status": "success", "tech": tech_list}
    except:
        return {"status": "error"}

@app.get("/history")
async def get_history_api():
    db = SessionLocal()
    data = db.query(Scan).order_by(Scan.id.desc()).limit(10).all()
    db.close()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)