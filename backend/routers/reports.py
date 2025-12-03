from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Indicator
from utils.pdf_report import generate_ioc_pdf
from datetime import datetime
import os

router = APIRouter()

@router.get("/iocs/pdf")
def export_ioc_report(
    source: str | None = Query(None),
    since_days: int | None = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Indicator)
    if source:
        q = q.filter(Indicator.source == source)
    if since_days:
        cut = datetime.utcnow() - timedelta(days=since_days)
        q = q.filter(Indicator.first_seen >= cut)
    indicators = q.order_by(Indicator.first_seen.desc()).limit(1000).all()
    if not indicators:
        raise HTTPException(status_code=404, detail="No indicators found for given filters")
    # transform into serializable list
    data = []
    for ind in indicators:
        data.append({
            "value": ind.value,
            "ioc_type": ind.ioc_type,
            "source": ind.source,
            "threat_level": ind.threat_level,
            "description": ind.description
        })
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join("data", "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"ioc_report_{ts}.pdf")
    generate_ioc_pdf(out_path, title=f"IOC Report {ts}", indicators=data)
    return FileResponse(out_path, media_type="application/pdf", filename=os.path.basename(out_path))
