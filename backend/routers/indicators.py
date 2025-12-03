from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Indicator
from schemas import IndicatorCreate, IndicatorRead, FetchResponse
from utils.classifier import classify_ioc
from utils import fetch_otx, fetch_abuseipdb
import os
import json
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=IndicatorRead)
def create_indicator(payload: IndicatorCreate, db: Session = Depends(get_db)):
    ioc_type = classify_ioc(payload.value)
    ind = Indicator(
        value=payload.value.strip(),
        ioc_type=ioc_type,
        source=payload.source or "manual",
        description=payload.description,
        threat_level=payload.threat_level or "unknown",
        extra=payload.extra
    )
    db.add(ind)
    db.commit()
    db.refresh(ind)
    return ind

@router.get("/", response_model=List[IndicatorRead])
def list_indicators(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return db.query(Indicator).order_by(Indicator.last_seen.desc()).offset(offset).limit(limit).all()

@router.post("/fetch_otx", response_model=FetchResponse)
def fetch_otx(limit: int = 100, db: Session = Depends(get_db)):
    api_key = os.getenv("OTX_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="OTX_API_KEY not configured in env")
    raw = fetch_otx.fetch_otx_indicators(api_key=api_key, limit=limit)
    inserted = 0
    skipped = 0
    for r in raw:
        val = r.get("value")
        if not val:
            continue
        # de-duplicate basic check
        exists = db.query(Indicator).filter(Indicator.value == val, Indicator.source == r.get("source", "OTX")).first()
        if exists:
            skipped += 1
            continue
        ind = Indicator(
            value=val,
            ioc_type=classify_ioc(val),
            source=r.get("source", "OTX"),
            description=r.get("description"),
            threat_level=r.get("threat_level", "unknown"),
            extra=json.dumps(r.get("meta", {}))
        )
        db.add(ind)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "skipped": skipped}

@router.post("/fetch_abuseipdb", response_model=FetchResponse)
def fetch_abuse(limit: int = 500, days: int = 30, db: Session = Depends(get_db)):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="ABUSEIPDB_API_KEY not configured in env")
    raw = fetch_abuseipdb.fetch_abuseipdb(api_key=api_key, max_age_days=days, limit=limit)
    inserted = 0
    skipped = 0
    for r in raw:
        val = r.get("value")
        if not val:
            continue
        exists = db.query(Indicator).filter(Indicator.value == val, Indicator.source == r.get("source", "AbuseIPDB")).first()
        if exists:
            skipped += 1
            continue
        ind = Indicator(
            value=val,
            ioc_type=classify_ioc(val),
            source=r.get("source", "AbuseIPDB"),
            description=r.get("description"),
            threat_level=r.get("threat_level", "unknown"),
            extra=None
        )
        db.add(ind)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "skipped": skipped}
