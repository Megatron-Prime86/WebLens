# 🔍 WebLens: Full-Stack Tech Stack Detector

WebLens is a comprehensive web utility that allows users to identify the underlying technologies of any website. It consists of a Chrome Extension (Frontend), a FastAPI service (Backend), and a cloud-hosted Dashboard (Analytics).

## 🚀 Live Demo
<<<<<<< HEAD
- **Live Dashboard:** [https://weblens-f2br.onrender.com/](https://weblens-f2br.onrender.com/)
- **Backend API:** [https://weblens-f2br.onrender.com/history](https://weblens-f2br.onrender.com/history)
=======
- **Live Dashboard:** [Insert Your Render Link Here]
- **Backend API:** [Insert Your Render Link Here]/history
>>>>>>> 43479c9 (Saving local changes before syncing with cloud)

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
<<<<<<< HEAD
- **Responsive Dashboard:** A professional dark-mode UI to track scan history.
=======
- **Responsive Dashboard:** A professional dark-mode UI to track scan history across different sessions.
>>>>>>> 43479c9 (Saving local changes before syncing with cloud)

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
<<<<<<< HEAD
=======
🔧 Installation & Setup
1. Backend Setup
Bash
# Clone the repository
git clone [https://github.com/Megatron-Prime86/WebLens.git](https://github.com/Megatron-Prime86/WebLens.git)

# Install dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn main:app --reload
2. Chrome Extension Setup
Open Chrome and navigate to chrome://extensions/.

Enable Developer Mode (top right).

Click Load unpacked.

Select the extension folder from this repository.

Note: Ensure the API_BASE_URL in popup.js matches your live or local backend URL.
>>>>>>> 43479c9 (Saving local changes before syncing with cloud)

💡 Challenges Overcame
Schema Migrations: Managed the transition from local development to cloud deployment, resolving SQLite pathing issues and schema mismatches on the Render platform.

Version Compatibility: Resolved version-specific conflicts with Jinja2Templates and FastAPI context passing during the dashboard build.

<<<<<<< HEAD
CORS Management: Configured Cross-Origin Resource Sharing to allow secure extension-to-API communication.
=======
CORS Management: Configured Cross-Origin Resource Sharing to allow the browser extension to securely communicate with the cloud API.
>>>>>>> 43479c9 (Saving local changes before syncing with cloud)

👤 Author
Subash
Computer Science & Engineering Student
<<<<<<< HEAD
Presidency University, Bangalore
=======
Presidency University, Bangalore
>>>>>>> 43479c9 (Saving local changes before syncing with cloud)
