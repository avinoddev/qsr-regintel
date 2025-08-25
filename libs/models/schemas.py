
from pydantic import BaseModel, Field, AnyUrl
from typing import List, Optional, Literal, Dict
from datetime import datetime

SeverityLevel = Literal["Critical", "High", "Medium", "Low"]

class Citation(BaseModel):
    url: AnyUrl | str
    section: Optional[str] = None
    quote: Optional[str] = None
    retrieved_at: Optional[datetime] = None
    page: Optional[str] = None
    confidence: Optional[float] = None

class Escalation(BaseModel):
    sla_hours: int
    owner: List[str]

class Severity(BaseModel):
    level: SeverityLevel
    rationale: Optional[str] = None
    signals: List[str] = []
    escalation: Escalation

class Obligation(BaseModel):
    key: str
    value: str | int | float | bool | None
    unit: Optional[str] = None
    trigger: Optional[str] = None
    citation: Citation
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)

class Jurisdiction(BaseModel):
    level: Literal["federal","state","city","county"]
    name: str
    parent: Optional[str] = None

class RuleRecord(BaseModel):
    id: str
    jurisdiction: Jurisdiction
    rule_family: str
    obligations: List[Obligation] = []
    penalties_premiums: List[Dict] = []
    severity: Severity
    provenance: Dict[str, str] = {}
    effective: Optional[Dict[str, str]] = None
