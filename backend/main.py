from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import indicators, reports
from database import Base, engine
import os

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Threat Intel Platform - Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(indicators.router, prefix="/api/indicators", tags=["indicators"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/")
def root():
    return {"service": "threat-intel-backend", "status": "ok"}
