from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime, requests, uvicorn

# DB Setup
engine = create_engine("sqlite:///./weblens.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    tech = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/analyze")
def analyze(url: str):
    try:
        # Added headers to mimic a real browser to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebLens/1.0'}
        res = requests.get(url, timeout=5, headers=headers)
        content = res.text.lower()
        tech_list = []

        # --- Enhanced Detection Logic ---
        if "wp-content" in content: tech_list.append("WordPress")
        if "react" in content: tech_list.append("React.js")
        if "mediawiki" in content: tech_list.append("MediaWiki")  # <--- Hits for Wikipedia!
        if "bootstrap" in content: tech_list.append("Bootstrap")
        if "jquery" in content: tech_list.append("jQuery")
        
        # --- Header Analysis ---
        server = res.headers.get("Server", "")
        if server:
            tech_list.append(server)
        else:
            tech_list.append("Cloudflare/Generic") # Fallback

        # Save to DB
        db = SessionLocal()
        db.add(Scan(url=url, tech=", ".join(tech_list)))
        db.commit()
        db.close()

        return {"status": "success", "url": url, "tech": tech_list, "score": 85}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/history")
def get_history():
    db = SessionLocal()
    data = db.query(Scan).order_by(Scan.id.desc()).limit(5).all()
    db.close()
    return data

# ... (Keep your imports and DB setup the same)

if __name__ == "__main__":
    import uvicorn
    import os
    # Render provides a PORT environment variable. We MUST use it.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)