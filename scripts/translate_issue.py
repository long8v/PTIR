#!/usr/bin/env python3
"""Translate a GitHub issue to English and generate a Hugo post."""

import argparse
import os
import re
import unicodedata

import deepl
from github import Auth, Github


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


def translate_body(translator: deepl.Translator, body: str) -> str:
    """Translate issue body to English using DeepL API."""
    # Split by lines to preserve markdown structure
    # Skip lines that are only images, URLs, or already English
    lines = body.split("\n")
    translated_lines = []

    for line in lines:
        stripped = line.strip()
        # Skip empty lines, image-only lines, URL-only lines
        if (
            not stripped
            or stripped.startswith("<img ")
            or stripped.startswith("![")
            or re.match(r"^https?://\S+$", stripped)
            or re.match(r"^\[.*\]\(https?://\S+\)$", stripped)
        ):
            translated_lines.append(line)
            continue

        # Check if line has any Korean characters
        if re.search(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]", stripped):
            try:
                result = translator.translate_text(
                    stripped, source_lang="KO", target_lang="EN-US"
                )
                translated_lines.append(result.text)
            except Exception:
                translated_lines.append(line)
        else:
            translated_lines.append(line)

    return "\n".join(translated_lines)


def extract_summary(translator: deepl.Translator, body: str) -> str:
    """Extract a one-sentence summary from TL;DR section (why + contribution/result)."""
    why = ""
    contribution = ""
    result_text = ""

    for line in body.split("\n"):
        if "**I read this because" in line:
            why = re.sub(r".*\*\*I read this because.*?:\*\*\s*", "", line).strip()
        elif "**contribution" in line:
            contribution = re.sub(r".*\*\*contribution\s*:\*\*\s*", "", line).strip()
        elif "**result" in line and not result_text:
            result_text = re.sub(r".*\*\*result\s*:\*\*\s*", "", line).strip()

    # Use contribution if available, otherwise result
    highlight = contribution or result_text
    parts = [p for p in [why, highlight] if p and p.lower() not in ("", "see results")]

    if not parts:
        return ""

    raw = " — ".join(parts)

    # Translate if Korean
    if re.search(r"[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]", raw):
        try:
            result = translator.translate_text(raw, source_lang="KO", target_lang="EN-US")
            return result.text
        except Exception:
            return raw
    return raw


def clean_title(title: str) -> str:
    """Remove [number] prefix from issue title."""
    return re.sub(r"^\[\d+\]\s*", "", title)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--repo", default="long8v/PTIR")
    parser.add_argument("--output-dir", default="blog/content/posts")
    args = parser.parse_args()

    gh = Github(auth=Auth.Token(os.environ["GH_TOKEN"]))
    repo = gh.get_repo(args.repo)
    issue = repo.get_issue(args.issue_number)

    title = issue.title
    labels = [l.name for l in issue.labels]
    paper_url = extract_paper_url(issue.body or "")
    created = issue.created_at.strftime("%Y-%m-%d")

    translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
    translated_body = translate_body(translator, issue.body or "")
    summary = extract_summary(translator, issue.body or "")

    slug = slugify(clean_title(title))
    filename = f"{args.issue_number:03d}-{slug}.md"
    filepath = os.path.join(args.output_dir, filename)

    safe_title = title.replace('"', '\\"')
    safe_summary = summary.replace('"', '\\"')

    front_matter = f'''---
title: "{safe_title}"
date: {created}
tags: {labels}
paper: "{paper_url}"
issue: {args.issue_number}
issueUrl: "https://github.com/{args.repo}/issues/{args.issue_number}"
summary: "{safe_summary}"
---
'''

    os.makedirs(args.output_dir, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(front_matter)
        f.write(translated_body)

    # Also generate Korean version (original body, no translation)
    ko_filename = f"{args.issue_number:03d}-{slug}.ko.md"
    ko_filepath = os.path.join(args.output_dir, ko_filename)

    ko_front_matter = f'''---
title: "{safe_title}"
date: {created}
tags: {labels}
paper: "{paper_url}"
issue: {args.issue_number}
issueUrl: "https://github.com/{args.repo}/issues/{args.issue_number}"
---
'''
    with open(ko_filepath, "w") as f:
        f.write(ko_front_matter)
        f.write(issue.body or "")

    print(filepath)


if __name__ == "__main__":
    main()
