"""
Simple AbuseIPDB blacklist fetcher.

Docs: https://docs.abuseipdb.com/
You need an API key, set as ABUSEIPDB_API_KEY environment variable.
"""

import os
import requests
from typing import List, Dict

ABUSE_URL = "https://api.abuseipdb.com/api/v2/blacklist"

def fetch_abuseipdb(api_key: str, max_age_days: int = 30, limit: int = 500) -> List[Dict]:
    if not api_key:
        raise ValueError("AbuseIPDB API key not provided")

    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "confidenceMinimum": 50,
        "maxAgeInDays": max_age_days,
        "limit": limit
    }

    r = requests.get(ABUSE_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    data = j.get("data", [])
    indicators = []
    for item in data:
        ip = item.get("ipAddress")
        if not ip:
            continue
        indicators.append({
            "value": ip,
            "type": "ip",
            "source": "AbuseIPDB",
            "description": f"Abuse reports: {item.get('abuseConfidenceScore', '')}"
        })
    return indicators
