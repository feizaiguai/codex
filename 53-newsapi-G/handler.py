#!/usr/bin/env python3
"""Minimal NewsAPI analyzer with search fallback."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests


def fetch_newsapi(api_key: str, mode: str, category: str, query: str, limit: int) -> List[Dict[str, Any]]:
    base_url = "https://newsapi.org/v2"
    headers = {"X-Api-Key": api_key, "User-Agent": "Mozilla/5.0"}
    if mode == "everything":
        url = f"{base_url}/everything"
        params = {"q": query or "technology", "pageSize": min(limit, 100), "language": "en"}
    else:
        url = f"{base_url}/top-headlines"
        params = {"category": category or "technology", "country": "us", "pageSize": min(limit, 100)}
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "ok":
        raise RuntimeError(data.get("message", "NewsAPI error"))
    return data.get("articles", [])


def fetch_via_search(limit: int) -> List[Dict[str, Any]]:
    skills_dir = Path(__file__).parent.parent / "15-web-search-G"
    query = "latest technology news"
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
    data = json.loads(raw[start:])
    out: List[Dict[str, Any]] = []
    for r in data.get("results", []):
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "source": {"name": r.get("domain", "")},
            "description": r.get("snippet", ""),
            "publishedAt": r.get("published_date", ""),
        })
    return out


def format_report(articles: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# News Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Count: {len(articles)}")
    lines.append("")
    for idx, a in enumerate(articles, 1):
        lines.append(f"## {idx}. {a.get('title', '')}")
        source = a.get("source", {})
        source_name = source.get("name", "") if isinstance(source, dict) else str(source)
        if source_name:
            lines.append(f"- Source: {source_name}")
        if a.get("publishedAt"):
            lines.append(f"- Published: {a.get('publishedAt')}")
        if a.get("url"):
            lines.append(f"- URL: {a.get('url')}")
        if a.get("description"):
            lines.append(f"- Summary: {a.get('description')}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="NewsAPI analyzer")
    parser.add_argument("--api-key", type=str, help="NewsAPI key")
    parser.add_argument("--mode", choices=["headlines", "everything"], default="headlines")
    parser.add_argument("--category", type=str, default="technology")
    parser.add_argument("--query", type=str, default="")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("NEWSAPI_KEY", "")
    articles: List[Dict[str, Any]] = []
    if api_key:
        try:
            articles = fetch_newsapi(api_key, args.mode, args.category, args.query, args.limit)
        except Exception:
            articles = []

    if not articles:
        articles = fetch_via_search(args.limit)

    if not articles:
        print("No articles found", file=sys.stderr)
        return 1

    report = format_report(articles)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
