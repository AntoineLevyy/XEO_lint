<div align="center">
  <h1>🔍 XEOLint</h1>
  <p><strong>A fast, deterministic GEO and SEO linter & autofixer for Next.js</strong></p>
  <p>
    <a href="#philosophy">Philosophy</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#rules">Rules</a>
  </p>
</div>

---

## What is XEOLint?

**XEOLint** is an ESLint-like tool built specifically for **Generative Engine Optimization (GEO)** and **SEO**. 

As search evolves toward LLM-driven engines (like ChatGPT Search, Perplexity, and AI Overviews), structural clarity and machine-readability are more important than ever. XEOLint statically analyzes your Next.js project (supporting both the `app/` and `pages/` routers) to ensure your content is perfectly structured for both traditional crawlers and modern AI agents.

### ⚡ The V1 Philosophy
- **"ESLint for Discoverability"**: Useful, deterministic, and narrowly focused.
- **Audit-First**: Finds the missing metadata, broken hierarchies, and crawlability issues.
- **Safe Autofixing**: Modifies your code *only* when the fix is deterministic and extremely low-risk (e.g., generating missing `robots.txt` or `sitemap.xml`).
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

### Audit
The `audit` command statically analyzes your workspace and outputs a clean table of any GEO/SEO violations.

```bash
xeolint audit .
```

### Fix
The `fix` command automatically generates missing files or metadata blocks when it is 100% safe to do so.

```bash
xeolint fix .
```

---

## 📐 The Rules (V1)

XEOLint is built to verify 20 critical checks.

### 🟢 Safe Auto-Fixes
These rules can be automatically fixed when you run `xeolint fix`.

*   `missing_robots_txt`: Ensures `robots.txt` or `app/robots.ts` exists so crawlers can index you.
*   `missing_sitemap`: Ensures `sitemap.xml` or `app/sitemap.ts` exists for crawl efficiency.

### 🟡 Conditional Auto-Fixes & 🟠 Suggestions
These rules will trigger warnings during an `audit`, but are intentionally skipped by `fix` because they require human context or complex AST rewriting. The CLI outputs targeted "Suggested Fixes" allowing developers to easily paste the solution.

*   `missing_title`: Checks if `<title>` or `metadata.title` is defined.
*   `missing_meta_description`: Checks if `description` is defined in metadata.
*   `missing_open_graph`: Checks if `openGraph` object is defined in metadata.
*   `missing_twitter_card`: Checks if `twitter` object is defined in metadata.
*   `client_only_critical_content`: Warns if heavy text blocks are hidden behind `"use client"`.
*   `missing_h1` / `multiple_h1`: Analyzes your heading hierarchy.
*   `missing_semantic_landmarks`: Warns if main wrappers are generic `<div>`s instead of `<main>`/`<section>`.
*   `unclear_page_purpose`: Checks if your H1 and Hero copy provide a clear statement of purpose for LLMs.
*   *...and many more.*

---

## 🤝 Contributing

XEOLint is heavily under development! We are actively building out the core rules engine and Next.js AST parsers. 

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
