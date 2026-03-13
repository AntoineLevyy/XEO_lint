from enum import Enum
from dataclasses import dataclass
from typing import Optional

class CheckLevel(str, Enum):
    ERROR = "ERROR"       # Fails the linter (e.g. absolutely needed GEO check missing)
    WARNING = "WARNING"   # Linter shows warning (e.g. best practice)
    INFO = "INFO"         # Info level recommendation
    PASS = "PASS"         # The check passed successfully

class FixStatus(str, Enum):
    FIXED = "FIXED"
    UNABLE_TO_FIX = "UNABLE_TO_FIX"
    NOT_APPLICABLE = "NOT_APPLICABLE"

@dataclass
class AuditResult:
    rule_id: str
    level: CheckLevel
    message: str
    filepath: Optional[str] = None
    line_number: Optional[int] = None
    fix_suggestion: Optional[str] = None

@dataclass
class FixResult:
    rule_id: str
    status: FixStatus
    message: str
    filepath: Optional[str] = None
