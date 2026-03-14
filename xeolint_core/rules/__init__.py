from xeolint_core.rules.missing_robots_txt import MissingRobotsTxtRule
from xeolint_core.rules.missing_sitemap import MissingSitemapRule
from xeolint_core.rules.missing_title import MissingTitleRule
from xeolint_core.rules.missing_meta_description import MissingMetaDescriptionRule
from xeolint_core.rules.missing_open_graph import MissingOpenGraphRule
from xeolint_core.rules.missing_twitter_card import MissingTwitterCardRule
from xeolint_core.rules.missing_canonical import MissingCanonicalRule
from xeolint_core.rules.page_noindex_risk import PageNoindexRiskRule
from xeolint_core.rules.client_only_critical_content import ClientOnlyCriticalContentRule
from xeolint_core.rules.missing_h1 import MissingH1Rule
from xeolint_core.rules.multiple_h1 import MultipleH1Rule
from xeolint_core.rules.weak_heading_hierarchy import WeakHeadingHierarchyRule
from xeolint_core.rules.missing_semantic_landmarks import MissingSemanticLandmarksRule
from xeolint_core.rules.missing_alt_text import MissingAltTextRule
from xeolint_core.rules.missing_json_ld import MissingJsonLdRule
from xeolint_core.rules.unclear_page_purpose import UnclearPagePurposeRule
from xeolint_core.rules.weak_entity_clarity import WeakEntityClarityRule
from xeolint_core.rules.missing_faq import MissingFaqRule
from xeolint_core.rules.orphan_risk import OrphanRiskInternalLinkingRule
from xeolint_core.rules.generic_anchor_text import GenericAnchorTextRule
from xeolint_core.rules.client_only_content_risk import ClientOnlyContentRiskRule

ALL_RULES = [
    MissingRobotsTxtRule,
    MissingSitemapRule,
    MissingTitleRule,
    MissingMetaDescriptionRule,
    MissingOpenGraphRule,
    MissingTwitterCardRule,
    MissingCanonicalRule,
    PageNoindexRiskRule,
    ClientOnlyCriticalContentRule,
    MissingH1Rule,
    MultipleH1Rule,
    WeakHeadingHierarchyRule,
    MissingSemanticLandmarksRule,
    MissingAltTextRule,
    MissingJsonLdRule,
    UnclearPagePurposeRule,
    WeakEntityClarityRule,
    MissingFaqRule,
    OrphanRiskInternalLinkingRule,
    GenericAnchorTextRule,
    ClientOnlyContentRiskRule,
]

__all__ = [
    "MissingRobotsTxtRule",
    "MissingSitemapRule",
    "MissingTitleRule",
    "MissingMetaDescriptionRule",
    "MissingOpenGraphRule",
    "MissingTwitterCardRule",
    "MissingCanonicalRule",
    "PageNoindexRiskRule",
    "ClientOnlyCriticalContentRule",
    "MissingH1Rule",
    "MultipleH1Rule",
    "WeakHeadingHierarchyRule",
    "MissingSemanticLandmarksRule",
    "MissingAltTextRule",
    "MissingJsonLdRule",
    "UnclearPagePurposeRule",
    "WeakEntityClarityRule",
    "MissingFaqRule",
    "OrphanRiskInternalLinkingRule",
    "GenericAnchorTextRule",
    "ClientOnlyContentRiskRule",
    "ALL_RULES",
]
