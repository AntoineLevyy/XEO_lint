import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from xeolint_core.parsers import NextProjectAnalyzer

class MissingSitemapRule(Rule):
    @property
    def id(self) -> str:
        return "missing_sitemap"
        
    @property
    def description(self) -> str:
        return "Checks if a sitemap exists, which provides a structured map of important pages for discovery."
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        
        # Next.js sitemaps can be static in public/ or dynamic in app/
        public_sitemap = os.path.join(workspace, "public", "sitemap.xml")
        app_sitemap = os.path.join(workspace, "app", "sitemap.ts")
        src_app_sitemap = os.path.join(workspace, "src", "app", "sitemap.ts")
        
        has_sitemap = os.path.exists(public_sitemap) or os.path.exists(app_sitemap) or os.path.exists(src_app_sitemap)
        
        if not has_sitemap:
            return [AuditResult(
                rule_id=self.id,
                level=CheckLevel.ERROR,
                message="No sitemap.xml or app/sitemap.ts found. Sitemaps are essential for crawl efficiency.",
                filepath=workspace,
                fix_suggestion="Create public/sitemap.xml with a <urlset> or run 'xeolint fix'."
            )]
            
        return []
        
    def fix(self, context: Dict[str, Any], audit_results: List[AuditResult]) -> List[FixResult]:
        workspace = context["workspace_path"]
        public_dir = os.path.join(workspace, "public")
        
        if not os.path.exists(public_dir):
            os.makedirs(public_dir, exist_ok=True)
            
        sitemap_path = os.path.join(public_dir, "sitemap.xml")
        
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-01-01</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>'''
        
        try:
            with open(sitemap_path, "w") as f:
                f.write(sitemap_content)
                
            return [FixResult(
                rule_id=self.id,
                status=FixStatus.FIXED,
                message="Created placeholder static sitemap.xml in public/.",
                filepath=sitemap_path
            )]
        except Exception as e:
            return [FixResult(
                rule_id=self.id,
                status=FixStatus.UNABLE_TO_FIX,
                message=f"Failed to create sitemap.xml: {e}",
                filepath=sitemap_path
            )]
