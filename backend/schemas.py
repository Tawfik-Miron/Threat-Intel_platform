from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IndicatorCreate(BaseModel):
    value: str = Field(..., example="1.2.3.4 or evil.com or d41d8cd98f00b204e9800998ecf8427e")
    source: Optional[str] = "manual"
    description: Optional[str] = None
    threat_level: Optional[str] = "unknown"
    extra: Optional[str] = None

class IndicatorRead(BaseModel):
    id: int
    value: str
    ioc_type: Optional[str]
    source: Optional[str]
    threat_level: Optional[str]
    first_seen: datetime
    last_seen: datetime
    description: Optional[str]
    extra: Optional[str]

    class Config:
        orm_mode = True

class FetchResponse(BaseModel):
    inserted: int
    skipped: int
