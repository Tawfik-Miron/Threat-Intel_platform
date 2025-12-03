Threat Intelligence Platform

A lightweight Threat Intelligence (TI) platform with a React frontend and FastAPI backend, running entirely on Docker.

Fetches indicators from OSINT feeds (OTX, AbuseIPDB), allows manual entry, and displays them on a dashboard. Generates PDF reports for Indicators of Compromise (IOCs).

Features

Log indicators manually (IP, domain, hash)

Fetch from OTX and AbuseIPDB feeds

Classify indicators by type and threat level

Dashboard with a table view of all indicators

PDF report generation

Fully Dockerized (frontend + backend)

Easy to run from GitHub

Folder Structure
threat-intel_platform/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── docker-compose.yml
├── .env               # Environment variables (API keys)
└── README.md

Setup
1. Clone the repo
git clone https://github.com/Tawfik-Miron/Threat-Intel_platform.git
cd Threat-Intel_platform

2. Create .env file
OTX_API_KEY=your_otx_key
ABUSEIPDB_API_KEY=your_abuseipdb_key
SQLITE_PATH=/app/data/indicators.db
CORS_ORIGINS=http://localhost:3000


Leave keys empty if you just want to test manual entry.

3. Run with Docker

Make sure Docker Desktop is running (Linux containers enabled), then:

docker-compose up --build


Backend → http://localhost:8000/docs

Frontend → http://localhost:3000

4. Test API Endpoints

GET / → Check backend status

POST /api/indicators/ → Add a manual indicator

POST /api/indicators/fetch_otx → Fetch indicators from OTX

POST /api/indicators/fetch_abuseipdb → Fetch indicators from AbuseIPDB

GET /api/reports/iocs/pdf → Generate PDF report

5. Notes

SQLite database is stored at backend/data/indicators.db (persisted outside container)

Do not commit .env or database files to GitHub

Frontend React app will automatically connect to the backend at localhost:8000

6. GitHub Users

Anyone cloning the repo can run:

git clone https://github.com/Tawfik-Miron/Threat-Intel_platform.git
cd Threat-Intel_platform
docker-compose up --build


Full TI platform will be up with dashboard and backend APIs.
