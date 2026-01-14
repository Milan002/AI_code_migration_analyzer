"""
Data models for migration reports - Simplified.
"""
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class Severity(str, Enum):
    """Issue severity levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalysisResult(BaseModel):
    """Result from LLM code analysis."""
    is_valid_python3: bool
    files_analyzed: List[str]
    issues: List[dict]  # Each has: issue, severity, line_hint, fix
    summary: str


class MigrationReport(BaseModel):
    """Stored migration report."""
    id: Optional[str] = Field(None, alias="_id")
    is_valid_python3: bool
    files_analyzed: List[str]
    issues: List[dict]
    summary: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


class AnalysisResponse(BaseModel):
    """API response after analysis."""
    report_id: str
    message: str
