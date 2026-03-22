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
