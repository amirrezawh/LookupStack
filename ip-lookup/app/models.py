from sqlalchemy import Column, Integer, String
from app.database import Base

class IPLookup(Base):
    __tablename__ = "ip_lookup"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, nullable=False)
    region = Column(String, nullable=False)
