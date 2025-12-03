"""
Simple OTX fetcher.

Notes:
- OTX (AlienVault) offers Pulses and indicators via API.
- You should create an OTX API key and set it as OTX_API_KEY environment variable.
- This function is intentionally generic: adapt endpoints or query for specific pulses depending on your needs.
"""

import os
import requests
from typing import List, Dict

OTX_API_BASE = "https://otx.alienvault.com/api/v1"

def fetch_otx_indicators(api_key: str, limit: int = 100) -> List[Dict]:
    """
    Fetch recent indicators from OTX.

    Returns list of dicts: { "value": "...", "type": "...", "source": "OTX", "description": "..." }
    """
    if not api_key:
        raise ValueError("OTX API key not provided")

    headers = {
        "X-OTX-API-KEY": api_key
    }

    # Example: fetch recent pulses and collect their indicators (this is a simple approach)
    url = f"{OTX_API_BASE}/pulses/subscribed"  # user-subscribed pulses; you can change endpoint
    params = {"limit": 20}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    indicators = []
    pulses = data.get("results", []) if isinstance(data, dict) else []

    for p in pulses:
        pulse_id = p.get("id")
        # fetch indicators for the pulse
        try:
            ind_url = f"{OTX_API_BASE}/pulses/{pulse_id}"
            r2 = requests.get(ind_url, headers=headers, timeout=30)
            r2.raise_for_status()
            pdetail = r2.json()
            for i in pdetail.get("indicators", []):
                indicators.append({
                    "value": i.get("indicator"),
                    "type": i.get("type"),
                    "source": "OTX",
                    "description": pdetail.get("name")
                })
                if len(indicators) >= limit:
                    break
            if len(indicators) >= limit:
                break
        except Exception:
            # ignore pulse-specific errors and continue
            continue

    return indicators
