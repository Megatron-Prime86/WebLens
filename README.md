# 🔍 WebLens: Full-Stack Tech Stack Detector

WebLens is a comprehensive web utility that allows users to identify the underlying technologies of any website. It consists of a Chrome Extension (Frontend), a FastAPI service (Backend), and a cloud-hosted Dashboard (Analytics).

## 🚀 Live Demo
- **Live Dashboard:** [https://weblens-f2br.onrender.com/](https://weblens-f2br.onrender.com/)
- **Backend API:** [https://weblens-f2br.onrender.com/history](https://weblens-f2br.onrender.com/history)

## 🛠️ Tech Stack
- **Frontend:** JavaScript (Chrome Manifest V3), HTML5, CSS3 (Glassmorphism design)
- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Database:** SQLAlchemy, SQLite (Cloud Persistent)
- **Templating:** Jinja2
- **Deployment:** Render with GitHub CI/CD integration

## ✨ Key Features
- **Real-time Detection:** Instantly identifies WordPress, React, MediaWiki, Bootstrap, and jQuery.
- **Header Analysis:** Extracts server-side information (Nginx, Cloudflare, etc.).
- **Cloud Persistence:** Automatically logs every scan to a remote database.
- **Responsive Dashboard:** A professional dark-mode UI to track scan history.

## 📂 Project Structure
```text
WebLens/
├── extension/           # Chrome Extension files
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── templates/           # Backend UI Templates
│   └── history.html
├── main.py              # FastAPI Backend Logic
├── requirements.txt     # Python Dependencies
└── weblens.db           # Local Database (Git-ignored)

💡 Challenges Overcame
Schema Migrations: Managed the transition from local development to cloud deployment, resolving SQLite pathing issues and schema mismatches on the Render platform.

Version Compatibility: Resolved version-specific conflicts with Jinja2Templates and FastAPI context passing during the dashboard build.

CORS Management: Configured Cross-Origin Resource Sharing to allow secure extension-to-API communication.

👤 Author
Subash
Computer Science & Engineering Student
Presidency University, Bangalore
