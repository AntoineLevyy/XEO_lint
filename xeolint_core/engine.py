from typing import List, Dict, Any
import os
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus

class Engine:
    """
    Core execution engine for XEOLint.
    Responsible for organizing the context, running rules, and aggregating results.
    """
    def __init__(self, workspace_path: str):
        self.workspace_path = os.path.abspath(workspace_path)
        self.rules: List[Rule] = []

    def register_rule(self, rule: Rule):
        """Adds a new rule to the engine."""
        self.rules.append(rule)

    def _build_context(self) -> Dict[str, Any]:
        """
        Builds the context object passed to all rules.
        Contains basic information about the target directory.
        """
        return {
            "workspace_path": self.workspace_path,
        }

    def audit_all(self) -> List[AuditResult]:
        """
        Runs the audit method on all registered rules.
        Results are sorted by severity: ERROR > WARNING > INFO > PASS.
        """
        LEVEL_ORDER = {
            CheckLevel.ERROR: 0,
            CheckLevel.WARNING: 1,
            CheckLevel.INFO: 2,
            CheckLevel.PASS: 3,
        }

        context = self._build_context()
        all_results: List[AuditResult] = []
        for rule in self.rules:
            rule_results = rule.audit(context)
            
            # If a rule returns nothing, it means it completely passed globally.
            # We explicitly add a PASS result so the CLI can display it.
            if not rule_results:
                all_results.append(AuditResult(
                    rule_id=rule.id,
                    level=CheckLevel.PASS,
                    message="Check passed successfully."
                ))
            else:
                all_results.extend(rule_results)
        
        all_results.sort(key=lambda r: LEVEL_ORDER.get(r.level, 99))
        return all_results

    def fix_all(self) -> List[FixResult]:
        """
        Runs audit first, and then sequentially runs fix for each rule
        that generated an Error/Warning AuditResult.
        """
        all_fix_results = []
        context = self._build_context()
        
        for rule in self.rules:
            audit_results = rule.audit(context)
            
            # Filter out PASS results before sending to fix engine
            actionable_results = [r for r in audit_results if r.level != CheckLevel.PASS]
            
            if not actionable_results:
                continue
                
            fix_results = rule.fix(context, actionable_results)
            all_fix_results.extend(fix_results)
            
        return all_fix_results
