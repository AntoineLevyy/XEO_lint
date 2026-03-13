import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from xeolint_core.parsers import NextProjectAnalyzer

class MissingRobotsTxtRule(Rule):
    @property
    def id(self) -> str:
        return "missing_robots_txt"
        
    @property
    def description(self) -> str:
        return "Checks if robots.txt exists, which is critical for crawler behavior and search engine indexing."
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        
        # Next.js robots.txt can be in public/robots.txt or app/robots.ts
        public_robots = os.path.join(workspace, "public", "robots.txt")
        app_robots = os.path.join(workspace, "app", "robots.ts")
        src_app_robots = os.path.join(workspace, "src", "app", "robots.ts")
        
        has_robots = os.path.exists(public_robots) or os.path.exists(app_robots) or os.path.exists(src_app_robots)
        
        if not has_robots:
            return [AuditResult(
                rule_id=self.id,
                level=CheckLevel.ERROR,
                message="No robots.txt or app/robots.ts found. This is a basic crawlability requirement.",
                filepath=os.path.join(workspace, "public"),
                fix_suggestion="Create public/robots.txt with 'User-Agent: *\\nAllow: /' or run 'xeolint fix'."
            )]
            
        return []
        
    def fix(self, context: Dict[str, Any], audit_results: List[AuditResult]) -> List[FixResult]:
        workspace = context["workspace_path"]
        public_dir = os.path.join(workspace, "public")
        
        if not os.path.exists(public_dir):
            os.makedirs(public_dir, exist_ok=True)
            
        robots_path = os.path.join(public_dir, "robots.txt")
        
        try:
            with open(robots_path, "w") as f:
                f.write("User-Agent: *\nAllow: /\n")
            return [FixResult(
                rule_id=self.id,
                status=FixStatus.FIXED,
                message="Created default robots.txt allowing all crawlers.",
                filepath=robots_path
            )]
        except Exception as e:
            return [FixResult(
                rule_id=self.id,
                status=FixStatus.UNABLE_TO_FIX,
                message=f"Failed to create robots.txt: {e}",
                filepath=robots_path
            )]
