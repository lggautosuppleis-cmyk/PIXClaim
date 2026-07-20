from pydantic import BaseModel
from typing import Optional, Dict, Any

class VehicleRecord(BaseModel):
    vin: str
    make: Optional[str] = None
    model: Optional[str] = None
    model_year: Optional[int] = None
    trim: Optional[str] = None
    body_class: Optional[str] = None
    raw: Dict[str, Any]

class RecallRecord(BaseModel):
    recall_id: str
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    component: Optional[str] = None
    summary: Optional[str] = None
    remedy: Optional[str] = None
    raw: Dict[str, Any]
