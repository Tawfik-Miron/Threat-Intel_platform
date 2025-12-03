from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=False, index=True, nullable=False)  # ip, domain or hash
    ioc_type = Column(String, index=True)  # ip / domain / md5 / sha1 / sha256 / unknown
    source = Column(String, index=True)  # OTX, AbuseIPDB, manual, ...
    threat_level = Column(String, index=True, default="unknown")  # low/medium/high/unknown
    first_seen = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now(), onupdate=func.now())
    description = Column(Text, nullable=True)
    extra = Column(Text, nullable=True)  # JSON string for any metadata
