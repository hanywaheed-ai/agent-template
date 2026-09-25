from typing import List, Optional
from pydantic import BaseModel, Field


class AuditFinding(BaseModel):
    category: str = Field(
        ..., 
        description="Category of the audit check (e.g., Security, Accuracy, Compliance)"
    )
    severity: str = Field(
        ..., 
        description="Severity rating: LOW, MEDIUM, HIGH, CRITICAL"
    )
    description: str = Field(
        ..., 
        description="Detailed description of the issue or verification check"
    )


class AuditReport(BaseModel):
    passed: bool = Field(
        ..., 
        description="True if the output meets all verification standards, False otherwise"
    )
    quality_score: int = Field(
        ..., 
        description="Quality score from 0 to 100 based on accuracy and policy guidelines"
    )
    findings: List[AuditFinding] = Field(
        default_factory=list, 
        description="List of specific issues identified during auditing"
    )
    revised_output: Optional[str] = Field(
        None, 
        description="The corrected, ready-to-use output if passed is False"
    )


# Clean export definition
__all__ = ["AuditFinding", "AuditReport"]
