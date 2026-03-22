#!/usr/bin/env python3
"""Fetch recent arxiv papers matching keywords and save as Hugo data file."""

import json
import os
import re
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

KEYWORDS = [
    "video language model",
    "multimodal large language model",
    "vision language model",
    "reinforcement learning from human feedback",
    "reinforcement learning LLM",
    "vision language action",
    "VLA robot",
    "video understanding",
    "MLLM",
    "visual reasoning",
]

ARXIV_API = "http://export.arxiv.org/api/query"
MAX_RESULTS_PER_QUERY = 30
DAYS_BACK = 14

NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch_papers(query: str, max_results: int = MAX_RESULTS_PER_QUERY) -> list[dict]:
    """Fetch papers from arxiv API for a given query."""
    params = urllib.parse.urlencode({
        "search_query": f'all:"{query}"',
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PTIR-ArxivFeed/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"  Error fetching '{query}': {e}")
        return []

    root = ET.fromstring(xml_data)
    papers = []

    for entry in root.findall("atom:entry", NS):
        published = entry.find("atom:published", NS).text[:10]
        # Filter by date
        pub_date = datetime.strptime(published, "%Y-%m-%d")
        if pub_date < datetime.now() - timedelta(days=DAYS_BACK):
            continue

        arxiv_id = entry.find("atom:id", NS).text.split("/abs/")[-1]
        title = re.sub(r"\s+", " ", entry.find("atom:title", NS).text.strip())
        summary = re.sub(r"\s+", " ", entry.find("atom:summary", NS).text.strip())
        authors = [a.find("atom:name", NS).text for a in entry.findall("atom:author", NS)]

        categories = [c.get("term") for c in entry.findall("atom:category", NS)]

        pdf_link = ""
        for link in entry.findall("atom:link", NS):
            if link.get("title") == "pdf":
                pdf_link = link.get("href")

        papers.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors[:5],
            "author_count": len(authors),
            "summary": summary[:300] + ("..." if len(summary) > 300 else ""),
            "published": published,
            "categories": categories[:3],
            "pdf": pdf_link,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "query": query,
        })

    return papers


def main():
    all_papers = {}
    for kw in KEYWORDS:
        print(f"Fetching: {kw}")
        papers = fetch_papers(kw)
        print(f"  Found {len(papers)} recent papers")
        for p in papers:
            all_papers[p["id"]] = p
        time.sleep(3)  # Be nice to arxiv API

    # Sort by date descending
    sorted_papers = sorted(all_papers.values(), key=lambda p: p["published"], reverse=True)
    print(f"\nTotal unique papers: {len(sorted_papers)}")

    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        "days_back": DAYS_BACK,
        "keywords": KEYWORDS,
        "count": len(sorted_papers),
        "papers": sorted_papers,
    }

    output_dir = os.environ.get("OUTPUT_DIR", "blog/data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "arxiv.json")

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
