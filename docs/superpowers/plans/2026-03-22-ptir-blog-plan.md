# PTIR Paper Review Blog — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Auto-translate Korean paper reviews from GitHub Issues to English and publish as a Hugo blog on GitHub Pages.

**Architecture:** Hugo static site in `blog/` dir with PaperMod theme. Two GitHub Actions: (1) issue → translate → commit markdown, (2) push → Hugo build → deploy. Python script handles GitHub API fetch + Claude API translation.

**Tech Stack:** Hugo, PaperMod theme, GitHub Actions, Python 3 + anthropic SDK, GitHub Pages

---

## File Structure

```
PTIR/
├── .github/workflows/
│   ├── translate-issue.yml      # Trigger: issues opened/edited → translate → commit
│   └── deploy-hugo.yml          # Trigger: push to main (blog/) → build Hugo → deploy Pages
├── blog/
│   ├── hugo.toml                # Hugo config (PaperMod theme, site metadata)
│   ├── content/posts/           # Auto-generated translated posts
│   ├── themes/PaperMod/         # Git submodule
│   └── layouts/                 # Custom overrides if needed
├── scripts/
│   ├── translate_issue.py       # Single issue: fetch → translate → write markdown
│   ├── migrate_all.py           # One-time: bulk translate all 233 issues
│   └── requirements.txt         # anthropic, PyGithub
└── docs/superpowers/            # Specs and plans
```

---

### Task 1: Hugo Site Scaffold

**Files:**
- Create: `blog/hugo.toml`
- Create: `.gitmodules` (PaperMod theme as submodule)
- Create: `blog/content/posts/.gitkeep`
- Create: `blog/content/_index.md`

- [ ] **Step 1: Install Hugo locally**

```bash
brew install hugo
```

- [ ] **Step 2: Initialize Hugo site**

```bash
cd /Users/long8v/PTIR
hugo new site blog --force
```

- [ ] **Step 3: Add PaperMod theme as git submodule**

```bash
cd /Users/long8v/PTIR
git submodule add https://github.com/adityatelange/hugo-PaperMod.git blog/themes/PaperMod
```

- [ ] **Step 4: Configure hugo.toml**

```toml
baseURL = "https://long8v.github.io/PTIR/"
languageCode = "en-us"
title = "Paper Today I Read"
theme = "PaperMod"

[params]
  author = "long8v"
  description = "Paper reviews translated from Korean to English"
  ShowReadingTime = true
  ShowShareButtons = false
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  defaultTheme = "auto"
  ShowToc = true

[params.homeInfoParams]
  Title = "Paper Today I Read"
  Content = "Paper reviews and notes — auto-translated from [GitHub Issues](https://github.com/long8v/PTIR/issues)"

[outputs]
  home = ["HTML", "RSS", "JSON"]

[taxonomies]
  tag = "tags"

[markup.goldmark.renderer]
  unsafe = true
```

- [ ] **Step 5: Create a sample post to verify**

Create `blog/content/posts/000-test.md`:
```markdown
---
title: "Test Post"
date: 2022-01-01
tags: ["test"]
---
Hello world.
```

- [ ] **Step 6: Build and verify locally**

```bash
cd /Users/long8v/PTIR/blog
hugo server -D
```
Open http://localhost:1313/PTIR/ — verify PaperMod theme renders correctly.

- [ ] **Step 7: Remove test post and commit**

```bash
rm blog/content/posts/000-test.md
git add blog/ .gitmodules
git commit -m "feat: scaffold Hugo site with PaperMod theme"
```

---

### Task 2: Translation Script (`scripts/translate_issue.py`)

**Files:**
- Create: `scripts/translate_issue.py`
- Create: `scripts/requirements.txt`

- [ ] **Step 1: Create requirements.txt**

```
anthropic>=0.40.0
PyGithub>=2.0.0
```

- [ ] **Step 2: Write translate_issue.py**

The script should:
1. Accept `--issue-number` and `--repo` args
2. Fetch issue via GitHub API (title, body, labels, created_at)
3. Extract paper URL from body (first markdown link)
4. Send body to Claude API with translation prompt
5. Generate Hugo front matter (title, date, tags from labels, paper URL, issue number)
6. Write to `blog/content/posts/{number:03d}-{slugified-title}.md`
7. Print the output path

```python
#!/usr/bin/env python3
"""Translate a GitHub issue to English and generate a Hugo post."""

import argparse
import os
import re
import unicodedata
from datetime import datetime

import anthropic
from github import Github


def slugify(text: str, max_length: int = 60) -> str:
    """Convert text to URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:max_length].rstrip("-")


def extract_paper_url(body: str) -> str:
    """Extract first URL from [paper](url) pattern."""
    match = re.search(r"\[paper\]\((https?://[^\s)]+)\)", body)
    return match.group(1) if match else ""


def translate_body(client: anthropic.Anthropic, body: str) -> str:
    """Translate issue body to English using Claude API."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "Translate the following paper review from Korean to English. "
                    "Keep all markdown formatting, image tags, and URLs exactly as-is. "
                    "Only translate the Korean text to natural English. "
                    "If text is already in English, keep it unchanged. "
                    "Do not add any commentary — return only the translated content.\n\n"
                    f"{body}"
                ),
            }
        ],
    )
    return response.content[0].text


def clean_title(title: str) -> str:
    """Remove [number] prefix from issue title."""
    return re.sub(r"^\[\d+\]\s*", "", title)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--repo", default="long8v/PTIR")
    parser.add_argument("--output-dir", default="blog/content/posts")
    args = parser.parse_args()

    gh = Github(os.environ["GH_TOKEN"])
    repo = gh.get_repo(args.repo)
    issue = repo.get_issue(args.issue_number)

    title = clean_title(issue.title)
    labels = [l.name for l in issue.labels]
    paper_url = extract_paper_url(issue.body or "")
    created = issue.created_at.strftime("%Y-%m-%d")

    client = anthropic.Anthropic()
    translated_body = translate_body(client, issue.body or "")

    slug = slugify(title)
    filename = f"{args.issue_number:03d}-{slug}.md"
    filepath = os.path.join(args.output_dir, filename)

    # Escape quotes in title for YAML
    safe_title = title.replace('"', '\\"')

    front_matter = f'''---
title: "{safe_title}"
date: {created}
tags: {labels}
paper: "{paper_url}"
issue: {args.issue_number}
issueUrl: "https://github.com/{args.repo}/issues/{args.issue_number}"
---
'''

    os.makedirs(args.output_dir, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(front_matter)
        f.write(translated_body)

    print(filepath)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Test with a single issue**

```bash
cd /Users/long8v/PTIR
export GH_TOKEN=<token>
export ANTHROPIC_API_KEY=<key>
pip install -r scripts/requirements.txt
python scripts/translate_issue.py --issue-number 242
cat blog/content/posts/242-*.md | head -30
```
Verify: front matter is correct, body is translated, images preserved.

- [ ] **Step 4: Commit**

```bash
git add scripts/
git commit -m "feat: add issue translation script"
```

---

### Task 3: Bulk Migration Script (`scripts/migrate_all.py`)

**Files:**
- Create: `scripts/migrate_all.py`

- [ ] **Step 1: Write migrate_all.py**

```python
#!/usr/bin/env python3
"""Bulk translate all open issues to Hugo posts."""

import os
import subprocess
import sys
import time

from github import Github


def main():
    gh = Github(os.environ["GH_TOKEN"])
    repo = gh.get_repo("long8v/PTIR")

    issues = list(repo.get_issues(state="open", sort="created", direction="asc"))
    print(f"Found {len(issues)} issues")

    for issue in issues:
        output_path = f"blog/content/posts/{issue.number:03d}-*.md"
        # Skip if already translated
        existing = subprocess.run(
            f"ls {output_path} 2>/dev/null",
            shell=True, capture_output=True, text=True
        )
        if existing.stdout.strip():
            print(f"  Skip #{issue.number} (already exists)")
            continue

        print(f"  Translating #{issue.number}: {issue.title}")
        result = subprocess.run(
            [
                sys.executable, "scripts/translate_issue.py",
                "--issue-number", str(issue.number),
            ],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
            continue

        print(f"  -> {result.stdout.strip()}")
        time.sleep(1)  # Rate limit buffer


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with first 3 issues**

Run for issues 1-3 and verify output.

- [ ] **Step 3: Run full migration**

```bash
python scripts/migrate_all.py
```
Expected: 233 markdown files in `blog/content/posts/`.

- [ ] **Step 4: Build site and verify**

```bash
cd blog && hugo
```
Check `blog/public/` for generated HTML.

- [ ] **Step 5: Commit all posts**

```bash
git add blog/content/posts/
git commit -m "feat: migrate all 233 issues to blog posts"
```

---

### Task 4: GitHub Action — Translate on Issue Create/Edit

**Files:**
- Create: `.github/workflows/translate-issue.yml`

- [ ] **Step 1: Write the workflow**

```yaml
name: Translate Issue to Blog Post

on:
  issues:
    types: [opened, edited]

permissions:
  contents: write

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r scripts/requirements.txt

      - name: Translate issue
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/translate_issue.py --issue-number ${{ github.event.issue.number }}

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add blog/content/posts/
          git diff --staged --quiet || git commit -m "post: translate issue #${{ github.event.issue.number }}"
          git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/translate-issue.yml
git commit -m "feat: add GitHub Action for auto-translating issues"
```

---

### Task 5: GitHub Action — Deploy Hugo to GitHub Pages

**Files:**
- Create: `.github/workflows/deploy-hugo.yml`

- [ ] **Step 1: Write the workflow**

```yaml
name: Deploy Hugo to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - "blog/**"

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "latest"
          extended: true

      - name: Build
        working-directory: blog
        run: hugo --minify --baseURL "https://long8v.github.io/PTIR/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: blog/public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/deploy-hugo.yml
git commit -m "feat: add GitHub Action for Hugo Pages deployment"
```

---

### Task 6: Configure GitHub Repo Settings

- [ ] **Step 1: Add repository secrets**

Go to `github.com/long8v/PTIR/settings/secrets/actions` and add:
- `ANTHROPIC_API_KEY` — Claude API key
- `GH_TOKEN` — GitHub PAT with repo read access

(Or use `gh secret set`)

- [ ] **Step 2: Enable GitHub Pages**

```bash
gh api repos/long8v/PTIR/pages -X POST -f build_type=workflow 2>/dev/null || \
gh api repos/long8v/PTIR/pages -X PUT -f build_type=workflow
```

- [ ] **Step 3: Push to main and verify deployment**

```bash
git push origin main
```

Check Actions tab for successful build + deploy.
Verify site at `https://long8v.github.io/PTIR/`.

---

## Summary

| Task | What | Depends on |
|------|------|-----------|
| 1 | Hugo scaffold + PaperMod theme | — |
| 2 | Translation script | — |
| 3 | Bulk migration (233 issues) | 1, 2 |
| 4 | GitHub Action: translate on issue | 2 |
| 5 | GitHub Action: deploy Hugo | 1 |
| 6 | Repo settings + deploy | 1-5 |
