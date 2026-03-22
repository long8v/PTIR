# PTIR Paper Review Blog — Design Spec

## Goal
Auto-translate Korean paper review issues from `long8v/PTIR` to English and publish as a Hugo static site on GitHub Pages.

## Architecture
- Hugo static site with PaperMod theme in `blog/` directory
- GitHub Action triggers on `issues: [opened, edited]` → runs Python script → Claude API translates → commits markdown to `blog/content/posts/`
- Second GitHub Action builds Hugo and deploys to GitHub Pages on push to main
- One-time migration script to bulk-translate all 233 existing issues

## Tech Stack
- Hugo + PaperMod theme
- GitHub Actions
- Python 3.x + anthropic SDK
- Claude API (translation)
- GitHub Pages (hosting)

## Post Format
Each issue becomes a markdown file with Hugo front matter:
- title: from issue title (translated)
- date: issue created_at
- tags: from issue labels
- paper: extracted from issue body
- issue: link back to original GitHub issue

## Site Features
- Tag-based filtering (labels → tags)
- Search
- Dark mode
- Minimal design
- Link back to original issue

## Costs
- GitHub Pages: free
- Claude API: ~$0.05/issue, ~$12 for initial migration
