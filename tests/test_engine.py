import pytest
from xeolint_core.engine import Engine
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from typing import List, Dict, Any

class MockRule(Rule):
    @property
    def id(self) -> str:
        return "mock_rule"
        
    @property
    def description(self) -> str:
        return "A mock rule for testing"
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        return [AuditResult(rule_id=self.id, level=CheckLevel.WARNING, message="Mock warning")]

def test_engine_initialization():
    engine = Engine(workspace_path=".")
    assert engine.workspace_path.endswith("XEOLint")
    
def test_engine_audit():
    engine = Engine(workspace_path=".")
    engine.register_rule(MockRule())
    results = engine.audit_all()
    
    assert len(results) == 1
    assert results[0].rule_id == "mock_rule"
    assert results[0].level == CheckLevel.WARNING

def test_engine_fix():
    engine = Engine(workspace_path=".")
    engine.register_rule(MockRule())
    # The default rule implementation returns NOT_APPLICABLE
    results = engine.fix_all()
    
    assert len(results) == 1
    assert results[0].rule_id == "mock_rule"
    assert results[0].status == FixStatus.NOT_APPLICABLE
