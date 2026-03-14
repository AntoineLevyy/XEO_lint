import os
import re
from typing import List, Dict, Any
from xeolint_core.rule import Rule
from xeolint_core.models import AuditResult, CheckLevel
from xeolint_core.parsers import NextProjectAnalyzer, ContentAnalyzer

# Patterns that indicate runtime data fetching
CLIENT_FETCH_PATTERNS = [
    r'\buseEffect\b',
    r'\bfetch\s*\(',
    r'\baxios\b',
    r'\buseSWR\b',
    r'\buseQuery\b',
    r'\bgetServerSideProps\b',  # not a risk itself, but indicates data dependency
]

SIGNAL_THRESHOLD = 2  # Flag if >= this many signals fire


class ClientOnlyContentRiskRule(Rule):
    @property
    def id(self) -> str:
        return "client_only_content_risk"

    @property
    def description(self) -> str:
        return "Detects pages where important content may not appear in initial HTML due to heavy client-side rendering."

    def audit(self, context: Dict[str, Any]) -> List[AuditResult]:
        workspace = context["workspace_path"]
        analyzer = NextProjectAnalyzer(workspace)
        results = []

        for file_path in analyzer.get_all_page_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                signals = []

                # Signal 1: "use client" directive
                if ContentAnalyzer.has_use_client(content):
                    signals.append('"use client" directive present')

                # Signal 2: Runtime data fetching patterns
                fetch_hits = []
                for pattern in CLIENT_FETCH_PATTERNS:
                    if re.search(pattern, content):
                        fetch_hits.append(pattern.strip(r'\b').rstrip(r'\('))
                if fetch_hits:
                    signals.append(f"Client-side data fetching detected ({', '.join(fetch_hits[:3])})")

                # Signal 3: Very little static text in the JSX
                text_len = ContentAnalyzer.estimate_text_length(content)
                if text_len < 100:
                    signals.append(f"Very little static text content (~{text_len} chars)")

                # Signal 4: No <h1> or <p> tags with real text
                has_h1 = bool(re.search(r'<h1[^>]*>.*?</h1>', content, re.DOTALL))
                has_paragraph = bool(re.search(r'<p[^>]*>[^<]{20,}</p>', content, re.DOTALL))
                if not has_h1 and not has_paragraph:
                    signals.append("No server-rendered <h1> or substantial <p> text found")

                # Only flag if multiple signals present
                if len(signals) >= SIGNAL_THRESHOLD:
                    signal_list = "\n    ".join(f"• {s}" for s in signals)
                    results.append(AuditResult(
                        rule_id=self.id,
                        level=CheckLevel.WARNING,
                        message=(
                            f"This page may rely heavily on client-side rendering "
                            f"({len(signals)} signals detected). "
                            f"Important content might not appear in the initial HTML response."
                        ),
                        filepath=file_path,
                        fix_suggestion=(
                            "Ensure critical content is server-rendered using Next.js SSR or static generation. "
                            "Avoid relying solely on client-side data fetching for core page content."
                        ),
                    ))
            except Exception:
                pass
        return results
