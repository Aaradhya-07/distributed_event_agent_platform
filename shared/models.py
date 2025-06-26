from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserInteractionEvent(BaseModel):
    user_id: str
    event_type: str
    timestamp: str  # ISO format
    event_metadata: Optional[Dict[str, Any]] = None

class ChemicalResearchEvent(BaseModel):
    molecule_id: str
    researcher: str
    data: Dict[str, Any]
    timestamp: str  # ISO format

from sqlalchemy import Column, String, Integer, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserInteractionEventDB(Base):
    __tablename__ = "user_interaction_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_type = Column(String)
    timestamp = Column(DateTime)
    event_metadata = Column(JSON)

class ChemicalResearchEventDB(Base):
    __tablename__ = "chemical_research_events"
    id = Column(Integer, primary_key=True, index=True)
    molecule_id = Column(String, index=True)
    researcher = Column(String)
    data = Column(JSON)
    timestamp = Column(DateTime)
