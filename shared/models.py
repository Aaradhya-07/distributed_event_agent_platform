from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class UserInteractionEvent(BaseModel):
    """Pydantic model for user interaction events."""
    user_id: str
    event_type: str
    timestamp: str = datetime.now().isoformat()  # Default to current time
    event_metadata: Optional[Dict[str, Any]] = None

class ChemicalResearchEvent(BaseModel):
    """Pydantic model for chemical research events."""
    molecule_id: str
    researcher: str
    data: Dict[str, Any]
    timestamp: str = datetime.now().isoformat()  # Default to current time

from sqlalchemy import Column, String, Integer, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy base for ORM models
Base = declarative_base()

class UserInteractionEventDB(Base):
    """SQLAlchemy model for user interaction events table."""
    __tablename__ = "user_interaction_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_type = Column(String)
    timestamp = Column(DateTime)
    event_metadata = Column(JSON)  # Renamed from 'metadata'

class ChemicalResearchEventDB(Base):
    """SQLAlchemy model for chemical research events table."""
    __tablename__ = "chemical_research_events"
    id = Column(Integer, primary_key=True, index=True)
    molecule_id = Column(String, index=True)
    researcher = Column(String)
    data = Column(JSON)
    timestamp = Column(DateTime)
