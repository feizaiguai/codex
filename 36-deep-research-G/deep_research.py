#!/usr/bin/env python3
"""Minimal deep research engine using 15-web-search-G."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import List

# Add 15-web-search-G to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "15-web-search-G"))

from search import web_search

FAST_MODE = os.getenv("DEEP_RESEARCH_FAST", "").lower() in ("1", "true", "yes")


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


def split_report_by_tokens(report: str, max_tokens: int = 20000) -> List[str]:
    if estimate_tokens(report) <= max_tokens:
        return [report]
    parts: List[str] = []
    current: List[str] = []
    current_tokens = 0
    for block in report.split("\n\n"):
        block_tokens = len(block.split())
        if current and current_tokens + block_tokens > max_tokens:
            parts.append("\n\n".join(current))
            current = [block]
            current_tokens = block_tokens
        else:
            current.append(block)
            current_tokens += block_tokens
    if current:
        parts.append("\n\n".join(current))
    return parts


class DeepResearchOrchestrator:
    async def execute(self, query: str) -> str:
        queries = [query, f"{query} best practices"]
        if FAST_MODE:
            queries = queries[:1]
        max_results = 5 if FAST_MODE else 8

        sections: List[str] = []
        sections.append(f"# Deep Research: {query}")
        sections.append("")
        sections.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sections.append("")

        for q in queries:
            data = await web_search(q, mode="auto", max_results=max_results)
            sections.append(f"## Query: {data.get('query')}")
            sections.append("")
            results = data.get("results", [])
            for idx, r in enumerate(results, 1):
                sections.append(f"{idx}. {r.title}")
                sections.append(f"- URL: {r.url}")
                sections.append(f"- Source: {r.source}")
                sections.append(f"- Snippet: {r.snippet}")
                sections.append("")

        return "\n".join(sections)
