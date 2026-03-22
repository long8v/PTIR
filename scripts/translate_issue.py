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
