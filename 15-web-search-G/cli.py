#!/usr/bin/env python3
"""
15-web-search-G CLI Entry Point
命令行入口 - 修复相对导入问题
"""

import sys
import os
import asyncio
import json
from pathlib import Path
from typing import List
import importlib.util

# Setup package path to enable relative imports
SCRIPT_DIR = Path(__file__).parent.absolute()
PARENT_DIR = SCRIPT_DIR.parent
PACKAGE_NAME = SCRIPT_DIR.name.replace('-', '_')  # "15_web_search"

# Add parent directory to sys.path so we can import the package
sys.path.insert(0, str(PARENT_DIR))

# Create a proper package name mapping in sys.modules
# This allows relative imports within the package to work
def setup_package():
    """Setup the package structure to allow relative imports"""
    # Register the package itself
    if PACKAGE_NAME not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            PACKAGE_NAME,
            SCRIPT_DIR / "__init__.py",
            submodule_search_locations=[str(SCRIPT_DIR)]
        )
        package = importlib.util.module_from_spec(spec)
        sys.modules[PACKAGE_NAME] = package
        package.__path__ = [str(SCRIPT_DIR)]
        package.__package__ = PACKAGE_NAME
        spec.loader.exec_module(package)

    return sys.modules[PACKAGE_NAME]

# Load the package
package = setup_package()

# Now we can import from the package
WebSearchFlow = package.WebSearchFlow
from models import WebSearchInput, SearchResult


def format_json_output(result, full_content: bool = False) -> str:
    """格式化为 JSON 输出"""
    output = {
        "query": result.query,
        "total_results": result.total_results,
        "search_time_ms": round(result.search_time, 2),
        "engines_used": result.engines_used,
        "results": [
            {
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "score": round(r.relevance_score, 1),
                "published_date": r.publish_date,
                "domain": r.source,
                "engine": r.engine,
                "full_content": r.full_content if full_content else None
            }
            for r in result.results
        ],
        "quality_metrics": result.quality,
        "summary": result.summary,
        "partial_failures": result.partial_failures
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_markdown_output(result, full_content: bool = False) -> str:
    """格式化为 Markdown 输出"""
    lines = []

    # 标题
    lines.append(f"# 🔍 Search Results: {result.query}\n")

    # 元信息
    search_time_sec = result.search_time / 1000
    lines.append(f"**Total Results**: {result.total_results} | "
                 f"**Search Time**: {search_time_sec:.2f}s | "
                 f"**Engines**: {', '.join(result.engines_used)}\n")
    lines.append("---\n")

    # 搜索结果
    for i, r in enumerate(result.results, 1):
        score = round(r.relevance_score, 1)
        lines.append(f"## {i}. {r.title} ({score}/100)\n")
        lines.append(f"**URL**: {r.url}\n")
        lines.append(f"**Domain**: {r.source} | **Engine**: {r.engine}")
        if r.publish_date:
            lines.append(f" | **Date**: {r.publish_date}")
        lines.append("\n")

        # Snippet
        lines.append(f"{r.snippet}\n")

        # Full content (if requested)
        if full_content and r.full_content:
            lines.append(f"\n### 📄 Full Content\n")
            # Limit to first 1000 chars for readability
            content_preview = r.full_content[:1000]
            if len(r.full_content) > 1000:
                content_preview += f"\n\n... (truncated, full content: {len(r.full_content)} chars)"
            lines.append(f"{content_preview}\n")

        lines.append("---\n")

    # Quality metrics
    if result.quality:
        lines.append("\n## 📊 Quality Metrics\n")
        for metric, value in result.quality.items():
            if isinstance(value, (int, float)):
                lines.append(f"- **{metric.replace('_', ' ').title()}**: {value}\n")
            else:
                lines.append(f"- **{metric.replace('_', ' ').title()}**: {value}\n")

    # Summary
    if result.summary:
        lines.append("\n## 📈 Summary\n")

        # Top domains
        if "top_domains" in result.summary:
            lines.append("**Top Domains**:\n")
            top_domains = result.summary["top_domains"]
            if isinstance(top_domains, dict):
                for domain, count in top_domains.items():
                    lines.append(f"- {domain}: {count} results\n")
            elif isinstance(top_domains, list):
                for item in top_domains:
                    if isinstance(item, dict):
                        lines.append(f"- {item.get('domain', 'N/A')}: {item.get('count', 0)} results\n")
                    else:
                        lines.append(f"- {item}\n")

        # Common themes
        if "common_themes" in result.summary:
            lines.append("\n**Common Themes**: " + ", ".join(result.summary["common_themes"]) + "\n")

        # Recommendations
        if "recommended_links" in result.summary:
            lines.append("\n**⭐ Top Recommendations**:\n")
            for idx, rec in enumerate(result.summary["recommended_links"], 1):
                lines.append(f"{idx}. [{rec.get('title', 'N/A')}]({rec.get('url', '#')})\n")
                if "reason" in rec:
                    lines.append(f"   *Reason*: {rec['reason']}\n")

    # Partial failures (if any)
    if result.partial_failures:
        lines.append(f"\n## ⚠️ Partial Failures ({len(result.partial_failures)})\n")
        for failure in result.partial_failures:
            lines.append(f"- **{failure.get('engine', 'Unknown')}**: {failure.get('error', 'N/A')}\n")

    return "".join(lines)


def format_compact_output(result) -> str:
    """格式化为紧凑输出"""
    lines = []

    search_time_sec = result.search_time / 1000
    lines.append(f"🔍 {result.query} ({result.total_results} results, {search_time_sec:.2f}s)\n")
    lines.append(f"Engines: {', '.join(result.engines_used)}\n")
    lines.append("---\n")

    # Show top 10 results
    for i, r in enumerate(result.results[:10], 1):
        score = round(r.relevance_score, 1)
        lines.append(f"{i}. [{score}] {r.title}\n")
        lines.append(f"   {r.url}\n")
        if r.publish_date:
            lines.append(f"   📅 {r.publish_date} | 🔗 {r.source}\n")
        else:
            lines.append(f"   🔗 {r.source}\n")

    if len(result.results) > 10:
        lines.append(f"\n... and {len(result.results) - 10} more results\n")

    # Quality summary
    if result.quality:
        avg_score = sum(v for v in result.quality.values() if isinstance(v, (int, float))) / len([v for v in result.quality.values() if isinstance(v, (int, float))])
        lines.append(f"\nAverage Quality Score: {avg_score:.1f}/100\n")

    return "".join(lines)


async def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='15-web-search-G: World-class AI-powered intelligent web search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast search (5-7s)
  python cli.py "Python asyncio" --mode fast

  # Auto search with time filter (8-12s)
  python cli.py "Vue 3 best practices" --mode auto --time-range month

  # Deep search with full content (15-20s)
  python cli.py "TypeScript generics" --mode deep --full-content --max-results 20

  # Site-specific search
  python cli.py "Docker networking" --site stackoverflow.com

  # Markdown output
  python cli.py "React hooks" --output markdown

Modes:
  fast  - 5-7s  - Brave + You.com - 10 results
  auto  - 8-12s - Exa + Brave     - 15 results (default)
  deep  - 15-20s- Exa + Perplexity + You.com + Full Content - 25 results
        """
    )

    # Required arguments
    parser.add_argument('query', type=str, help='Search query')

    # Mode selection
    parser.add_argument('--mode', type=str, default='auto',
                       choices=['fast', 'auto', 'deep'],
                       help='Search mode (default: auto)')

    # Result control
    parser.add_argument('--max-results', type=int,
                       help='Maximum number of results (auto-set based on mode if not specified)')

    # Filters
    parser.add_argument('--time-range', type=str, default='all',
                       choices=['day', 'week', 'month', 'year', 'all'],
                       help='Time range filter (default: all)')
    parser.add_argument('--language', type=str,
                       help='Language filter (e.g., en, zh, es)')
    parser.add_argument('--site', type=str,
                       help='Site filter (e.g., github.com, stackoverflow.com)')
    parser.add_argument('--exclude-site', type=str, action='append',
                       help='Exclude site (can be used multiple times)')

    # Content options
    parser.add_argument('--full-content', action='store_true',
                       help='Fetch full content for results (deep mode recommended)')
    parser.add_argument('--no-dedup', action='store_true',
                       help='Disable semantic deduplication')

    # Output format
    parser.add_argument('--output', type=str, default='markdown',
                       choices=['json', 'markdown', 'compact'],
                       help='Output format (default: markdown)')

    # Advanced options
    parser.add_argument('--search-type', type=str, default='general',
                       choices=['general', 'code', 'documentation', 'stackoverflow'],
                       help='Search type (default: general)')

    args = parser.parse_args()

    # Auto-set max_results based on mode if not specified
    if args.max_results is None:
        if args.mode == 'fast':
            args.max_results = 10
        elif args.mode == 'auto':
            args.max_results = 15
        elif args.mode == 'deep':
            args.max_results = 25

    # Build site_filter list
    site_filter = [args.site] if args.site else None
    exclude_sites = args.exclude_site if args.exclude_site else None

    # Create input
    input_params = WebSearchInput(
        query=args.query,
        mode=args.mode,
        max_results=args.max_results,
        time_range=args.time_range,
        language=args.language,
        site_filter=site_filter,
        exclude_sites=exclude_sites,
        fetch_full_content=args.full_content,
        deduplication=not args.no_dedup,
        search_type=args.search_type
    )

    # Execute search
    try:
        flow = WebSearchFlow()
        result = await flow.execute(input_params)

        # Format output
        if args.output == 'json':
            print(format_json_output(result, args.full_content))
        elif args.output == 'markdown':
            print(format_markdown_output(result, args.full_content))
        elif args.output == 'compact':
            print(format_compact_output(result))

        # Exit with success code
        sys.exit(0 if result.success else 1)

    except Exception as e:
        # Error output
        error_output = {
            "error": str(e),
            "type": type(e).__name__,
            "query": args.query,
            "mode": args.mode
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Run async main
    asyncio.run(main())
