<div align="center">
  <h1>🔍 XEOLint</h1>
  <p><strong>Make your vibecoded project discoverable by LLMs and search engines</strong></p>
  <p>
    <a href="#philosophy">Philosophy</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#rules">Rules</a>
  </p>
</div>

---

## What is XEOLint?

Vibecoded projects ship fast — but they often ship with **discovery problems**. Missing meta tags, broken heading hierarchies, no structured data, and client-rendered content that crawlers can't see.

**XEOLint** is a linter built to catch exactly these issues. It statically analyzes your Next.js project and tells you what's missing for **SEO** and **GEO** (Generative Engine Optimization) — so your site is discoverable by both traditional search engines and modern AI crawlers like ChatGPT Search, Perplexity, and AI Overviews.

Supports both the `app/` and `pages/` routers. Audit-first, fix when safe.

### ⚡ The Philosophy
- **Built for vibecoded projects**: Catch the SEO/GEO mistakes that AI-assisted coding often misses.
- **Audit-First**: Finds the missing metadata, broken hierarchies, and crawlability issues.
- **Safe Autofixing**: Modifies your code *only* when the fix is deterministic and low-risk.
- **Deep Next.js Support**: Natively understands `export const metadata`, `"use client"` directives, and `<Head>` tags.

---

## 🚀 Installation

XEOLint is distributed as a Python CLI tool.

```bash
pip install xeolint
```

*(Note: XEOLint requires Python 3.9+)*

---

## 🛠️ Usage

Navigate to the root of your Next.js project and run:

### Audit (default — block format)
```bash
xeolint audit .
```

Output:
```
ERROR  missing_title
  File: src/pages/Terms.tsx
  Message: No <title> found inside <Head> on this page route.
  Fix: Inject a <title> element inside the Next.js <Head> component.

WARNING  missing_canonical
  File: src/pages/Terms.tsx
  Message: No canonical URL defined for this page.
  Fix: Add <link rel='canonical' href='...'> in <Head>.

✅ Passed: missing_robots_txt, missing_sitemap, missing_h1, ...

Summary: 5 errors · 9 warnings · 6 info · 12 passed
```

### Audit (table format)
```bash
xeolint audit . --table
```

### Fix
The `fix` command automatically generates missing files or metadata blocks when it is 100% safe to do so.

```bash
xeolint fix .
```

---

## 📐 The 21 Rules

### 🟢 Safe Auto-Fixes
These rules are automatically fixed when you run `xeolint fix`.

| Rule | What it checks |
|------|---------------|
| `missing_robots_txt` | `robots.txt` or `app/robots.ts` exists |
| `missing_sitemap` | `sitemap.xml` or `app/sitemap.ts` exists |

### 🔴 Errors (audit only)
| Rule | What it checks |
|------|---------------|
| `missing_title` | `<title>` or `metadata.title` is defined |
| `missing_h1` | Page has an `<h1>` tag |

### 🟡 Warnings (audit only)
| Rule | What it checks |
|------|---------------|
| `missing_meta_description` | `description` is defined in metadata |
| `missing_canonical` | Canonical URL is defined |
| `missing_open_graph` | `openGraph` object in metadata |
| `missing_twitter_card` | `twitter` object in metadata |
| `page_noindex_risk` | Accidental `noindex` directives |
| `client_only_critical_content` | Heavy text hidden behind `"use client"` |
| `multiple_h1` | More than one `<h1>` on a page |
| `weak_heading_hierarchy` | Heading levels are skipped (e.g. h1 → h3) |
| `missing_semantic_landmarks` | Missing `<main>`, `<nav>`, `<footer>` |
| `missing_alt_text` | Images missing meaningful `alt` text |
| `missing_json_ld` | No JSON-LD structured data found |
| `client_only_content_risk` | Multi-signal detection of heavy client-side rendering risk |

### 🔵 Info (audit only)
| Rule | What it checks |
|------|---------------|
| `unclear_page_purpose` | H1/hero text is too vague for GEO |
| `weak_entity_clarity` | Brand/product name missing from key areas |
| `missing_faq_or_structured_qa` | No FAQ section or FAQ schema |
| `orphan_risk_internal_linking` | Pages with no internal links pointing to them |
| `generic_anchor_text` | "Click here" / "Learn more" style links |

---

## 🤝 Contributing

### Local Development
1. Clone the repository.
2. Initialize the environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   pip install pytest
   ```
3. Run the test suite:
   ```bash
   pytest
   ```

---
*Built to help your code be understood by machines.*
