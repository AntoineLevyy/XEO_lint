import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

class MissingSemanticLandmarksRule(Rule):
    @property
    def id(self) -> str:
        return "missing_semantic_landmarks"

    @property
    def description(self) -> str:
        return "Checks if semantic HTML landmarks (<main>, <nav>, <footer>) are used instead of generic <div>."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        # Check layouts for landmarks (they're most likely to have structural tags)
        files_to_check = analyzer.get_all_layout_files() + analyzer.get_all_page_files()
        
        found_main = False
        found_nav = False
        found_footer = False
        
        for file_path in files_to_check:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if ContentAnalyzer.has_semantic_landmark(content, "main"):
                    found_main = True
                if ContentAnalyzer.has_semantic_landmark(content, "nav"):
                    found_nav = True
                if ContentAnalyzer.has_semantic_landmark(content, "footer"):
                    found_footer = True
            except Exception:
                pass

        missing = []
        if not found_main:
            missing.append("<main>")
        if not found_nav:
            missing.append("<nav>")
        if not found_footer:
            missing.append("<footer>")
            
        if missing:
            results.append(AuditResult(
                rule_id=self.id,
                level=CheckLevel.WARNING,
                message=f"Missing semantic landmarks: {', '.join(missing)}. Using generic <div> wrappers hurts structure.",
                fix_suggestion=f"Replace top-level <div> wrappers with semantic tags: {', '.join(missing)}."
            ))
        return results
