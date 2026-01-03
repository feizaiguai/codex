#!/usr/bin/env python3
"""Minimal Reddit trending analyzer."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests


def fetch_posts(subreddit: str, limit: int) -> List[Dict[str, Any]]:
    bases = [
        "https://api.reddit.com",
        "https://www.reddit.com",
        "https://old.reddit.com",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    last_error = None
    for base in bases:
        url = f"{base}/r/{subreddit}/hot.json"
        try:
            resp = requests.get(url, params={"limit": limit}, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            return [p.get("data", {}) for p in data.get("data", {}).get("children", [])]
        except Exception as exc:
            last_error = exc
            continue
    if last_error:
        return fetch_posts_via_search(subreddit, limit)
    return []


def fetch_posts_via_search(subreddit: str, limit: int) -> List[Dict[str, Any]]:
    skills_dir = Path(__file__).parent.parent / "15-web-search-G"
    query = f"reddit r/{subreddit} hot"
    cmd = [
        sys.executable,
        "cli.py",
        query,
        "--mode",
        "auto",
        "--max-results",
        str(limit),
        "--output",
        "json",
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(skills_dir),
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return []
        raw = result.stdout.strip()
        start = raw.find("{")
        if start == -1:
            return []
        raw = raw[start:]
        data = json.loads(raw)
        results = data.get("results", [])
        posts: List[Dict[str, Any]] = []
        for r in results:
            url = r.get("url", "")
            title = r.get("title", "")
            if not url:
                continue
            posts.append({
                "title": title,
                "author": "unknown",
                "score": 0,
                "num_comments": 0,
                "url": url,
                "permalink": "",
            })
        return posts
    except Exception:
        return []


def format_report(posts: List[Dict[str, Any]], subreddit: str) -> str:
    lines: List[str] = []
    lines.append(f"# Reddit Hot - r/{subreddit}")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Count: {len(posts)}")
    lines.append("")
    for idx, p in enumerate(posts, 1):
        title = p.get("title", "")
        author = p.get("author", "unknown")
        score = p.get("score", 0)
        comments = p.get("num_comments", 0)
        permalink = p.get("permalink", "")
        url = p.get("url", "")
        lines.append(f"## {idx}. {title}")
        lines.append(f"- Author: u/{author}")
        lines.append(f"- Score: {score}")
        lines.append(f"- Comments: {comments}")
        lines.append(f"- URL: {url}")
        if permalink:
            lines.append(f"- Thread: https://www.reddit.com{permalink}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reddit trending analyzer")
    parser.add_argument("--subreddit", type=str, default="popular")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--no-analysis", action="store_true")
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    try:
        posts = fetch_posts(args.subreddit, args.limit)
        if not posts:
            print("No posts found", file=sys.stderr)
            return 1
        report = format_report(posts, args.subreddit)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
        print(report)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
