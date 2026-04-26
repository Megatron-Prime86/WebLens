from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime, requests, uvicorn, os

# --- CLOUD OPTIMIZED DB SETUP ---
# We use an absolute path for the DB file to avoid "Internal Server Error" on Render
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

# This line ensures the database and table are "born" when the server starts
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Standard CORS setup
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "WebLens API is Live!"}

@app.get("/analyze")
def analyze(url: str):
    try:
        # Added headers to mimic a real browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebLens/1.0'}
        res = requests.get(url, timeout=5, headers=headers)
        content = res.text.lower()
        tech_list = []

        # --- Enhanced Detection Logic ---
        if "wp-content" in content: tech_list.append("WordPress")
        if "react" in content: tech_list.append("React.js")
        if "mediawiki" in content: tech_list.append("MediaWiki")
        if "bootstrap" in content: tech_list.append("Bootstrap")
        if "jquery" in content: tech_list.append("jQuery")
        
        # --- Header Analysis ---
        server = res.headers.get("Server", "")
        if server:
            tech_list.append(server)
        else:
            tech_list.append("Cloudflare/Generic")

        # Save to DB
        db = SessionLocal()
        new_scan = Scan(url=url, tech=", ".join(tech_list))
        db.add(new_scan)
        db.commit()
        db.close()

        return {"status": "success", "url": url, "tech": tech_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        data = db.query(Scan).order_by(Scan.id.desc()).limit(10).all()
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    # Render assigns a port via environment variables
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)