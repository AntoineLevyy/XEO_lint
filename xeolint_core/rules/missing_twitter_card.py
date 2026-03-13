import os
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, FixResult, CheckLevel, FixStatus
from xeolint_core.parsers import NextProjectAnalyzer, MetadataExtractor

class MissingTwitterCardRule(Rule):
    @property
    def id(self) -> str:
        return "missing_twitter_card"
        
    @property
    def description(self) -> str:
        return "Checks if Twitter Card metadata is provided to improve link previews on X/Twitter."
        
    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        page_files = analyzer.get_all_page_files()
        
        results = []
        
        for file_path in page_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                is_app_router = "app" in file_path.split(os.sep)
                
                if is_app_router:
                    if MetadataExtractor.has_app_router_metadata(content) and not MetadataExtractor.has_app_router_twitter(content):
                        results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.INFO,
                            message="Metadata exported, but no Twitter definition found.",
                            filepath=file_path,
                            fix_suggestion="Add a 'twitter' object with card, title, and description to exported metadata."
                        ))
                else:
                    if "<Head>" in content and "name=\"twitter:" not in content and "name='twitter:" not in content:
                         results.append(AuditResult(
                            rule_id=self.id,
                            level=CheckLevel.INFO,
                            message="No Twitter Card <meta name=\"twitter:...\"> found inside <Head>.",
                            filepath=file_path,
                            fix_suggestion="Add <meta name='twitter:card' content='summary_large_image'> inside <Head>."
                        ))
            except Exception:
                pass
                
        return results
