from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserInteractionEvent(BaseModel):
    user_id: str
    event_type: str
    timestamp: str  # ISO format
    metadata: Optional[Dict[str, Any]] = None

class ChemicalResearchEvent(BaseModel):
    molecule_id: str
    researcher: str
    data: Dict[str, Any]
    timestamp: str  # ISO format
