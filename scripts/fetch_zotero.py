#!/usr/bin/env python3
"""Fetch Zotero library and save as Hugo data file."""

import json
import os
import urllib.request

USER_ID = "13937487"
EXCLUDE_COLLECTION = "STHVZEJQ"
TYPES = "journalArticle || preprint || conferencePaper || book || bookSection || report"
API = f"https://api.zotero.org/users/{USER_ID}"
PER_PAGE = 100


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PTIR-Zotero/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        total = int(resp.headers.get("Total-Results", "0"))
        return json.loads(resp.read()), total


def main():
    # Fetch excluded collection items
    exclude_keys = set()
    url = f"{API}/collections/{EXCLUDE_COLLECTION}/items?format=json&v=3&limit={PER_PAGE}"
    try:
        items, _ = fetch_json(url)
        exclude_keys = {it["key"] for it in items}
        print(f"Excluding {len(exclude_keys)} items from 'my draft/review'")
    except Exception as e:
        print(f"Warning: couldn't fetch excluded collection: {e}")

    # Fetch all library items
    all_items = []
    start = 0
    total = None

    while True:
        url = (
            f"{API}/items?format=json&v=3"
            f"&itemType={urllib.parse.quote(TYPES)}"
            f"&sort=dateModified&direction=desc"
            f"&limit={PER_PAGE}&start={start}"
        )
        items, total = fetch_json(url)
        all_items.extend(items)
        print(f"  Fetched {len(all_items)}/{total}")

        if len(all_items) >= total or len(items) == 0:
            break
        start += PER_PAGE

    # Filter excluded
    filtered = [it for it in all_items if it["key"] not in exclude_keys]
    print(f"Total: {len(filtered)} papers (excluded {len(all_items) - len(filtered)})")

    # Simplify for Hugo
    papers = []
    for it in filtered:
        d = it.get("data", {})
        authors = [c for c in d.get("creators", []) if c.get("creatorType") == "author"]
        author_str = ", ".join(
            a.get("lastName") or a.get("name", "") for a in authors[:3]
        )
        if len(authors) > 3:
            author_str += " et al."

        link = d.get("url") or (f"https://doi.org/{d['DOI']}" if d.get("DOI") else "")
        tags = [t["tag"] for t in d.get("tags", [])]

        papers.append({
            "title": d.get("title", ""),
            "authors": author_str,
            "date": d.get("date", ""),
            "type": d.get("itemType", ""),
            "url": link,
            "tags": tags,
        })

    output_dir = os.environ.get("OUTPUT_DIR", "blog/data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "zotero.json")

    with open(output_path, "w") as f:
        json.dump({"count": len(papers), "papers": papers}, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    import urllib.parse
    main()
