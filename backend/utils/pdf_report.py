"""
Minimal PDF report generator using reportlab.

Generates a readable PDF summary for a list of indicators.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_ioc_pdf(path: str, title: str, indicators: list):
    """
    indicators: list of dicts with keys: value, ioc_type, source, threat_level, description
    path: full output file path (e.g. data/reports/report_2025-...pdf)
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, title)
    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(margin, y, f"Generated: {datetime.utcnow().isoformat()} UTC")
    y -= 30

    # header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "IOC")
    c.drawString(margin + 200, y, "Type")
    c.drawString(margin + 280, y, "Source")
    c.drawString(margin + 360, y, "Threat")
    y -= 12
    c.line(margin, y, width - margin, y)
    y -= 12
    c.setFont("Helvetica", 9)

    for i, ind in enumerate(indicators):
        if y < 80:
            c.showPage()
            y = height - margin
        val = ind.get("value", "")
        ioc_type = ind.get("ioc_type", ind.get("type", ""))
        src = ind.get("source", "")
        threat = ind.get("threat_level", "")
        desc = ind.get("description", "") or ""
        c.drawString(margin, y, str(val)[:40])
        c.drawString(margin + 200, y, ioc_type)
        c.drawString(margin + 280, y, src)
        c.drawString(margin + 360, y, threat)
        y -= 12
        if desc:
            # wrap description in next line if long
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(margin + 10, y, desc[:100])
            c.setFont("Helvetica", 9)
            y -= 12
    c.save()
    return path
