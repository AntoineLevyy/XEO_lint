from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus

class Rule(ABC):
    """
    Abstract base class for all XEOLint checks.
    """
    
    @property
    @abstractmethod
    def id(self) -> str:
        """The string identifier for this rule (e.g. missing_robots_txt)."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """A short description of what the rule checks."""
        pass
        
    @abstractmethod
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        """
        Runs the audit logic on the given context (e.g. workspace files).
        Returns a list of AuditResults. If the list is empty, the rule passed or wasn't applicable.
        """
        pass
        
    def fix(self, context: Dict[str, Any], audit_results: List[AuditResult]) -> List[FixResult]:
        """
        Attempts to auto-fix the issues identified in audit_results.
        By default, it returns NOT_APPLICABLE for all results, meaning this rule doesn't support auto-fix.
        Override this method to provide auto-fix functionality.
        """
        results = []
        for res in audit_results:
            results.append(FixResult(
                rule_id=self.id,
                status=FixStatus.NOT_APPLICABLE,
                message="Autofix not implemented for this rule.",
                filepath=res.filepath
            ))
        return results
