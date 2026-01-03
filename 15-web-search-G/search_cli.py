#!/usr/bin/env python3
"""
Simple CLI wrapper for 15-web-search-G
简化的CLI包装器 - 避免导入问题
"""

import sys
import subprocess
import json
from pathlib import Path

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='15-web-search-G: Intelligent web search',
        epilog="Note: This is a simplified wrapper. For full functionality, ensure dependencies are installed."
    )

    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--mode', type=str, default='auto',
                       choices=['fast', 'auto', 'deep'],
                       help='Search mode (default: auto)')
    parser.add_argument('--max-results', type=int,
                       help='Maximum results')
    parser.add_argument('--time-range', type=str, default='all',
                       choices=['day', 'week', 'month', 'year', 'all'])
    parser.add_argument('--language', type=str)
    parser.add_argument('--site', type=str)
    parser.add_argument('--full-content', action='store_true')
    parser.add_argument('--output', type=str, default='markdown',
                       choices=['json', 'markdown', 'compact'])

    args = parser.parse_args()

    #Auto-set max_results
    if args.max_results is None:
        args.max_results = {
            'fast': 10,
            'auto': 15,
            'deep': 25
        }[args.mode]

    # Use Python package execution to avoid import issues
    script_dir = Path(__file__).parent
    parent_dir = script_dir.parent

    # Build command to run via package import
    python_code = f'''
import sys
sys.path.insert(0, r"{parent_dir}")

# Mock the package structure
import importlib.util
import os

os.chdir(r"{script_dir}")

# Load as package
spec = importlib.util.spec_from_file_location("websearch", r"{script_dir}/__init__.py")
pkg = importlib.util.module_from_spec(spec)
sys.modules["websearch"] = pkg

# Load submodules with package context
for mod_name in ["models", "config", "api_clients", "main"]:
    mod_path = r"{script_dir}" + os.sep + mod_name + ".py"
    mod_spec = importlib.util.spec_from_file_location(f"websearch.{{mod_name}}", mod_path)
    mod = importlib.util.module_from_spec(mod_spec)
    mod.__package__ = "websearch"
    sys.modules[f"websearch.{{mod_name}}"] = mod
    setattr(pkg, mod_name, mod)
    mod_spec.loader.exec_module(mod)

# Execute package
spec.loader.exec_module(pkg)

# Now run the search
import asyncio
from websearch.models import WebSearchInput
from websearch.main import WebSearchFlow

input_params = WebSearchInput(
    query={json.dumps(args.query)},
    mode={json.dumps(args.mode)},
    max_results={args.max_results},
    time_range={json.dumps(args.time_range)},
    language={json.dumps(args.language) if args.language else None},
    site_filter=[{json.dumps(args.site)}] if args.site else None,
    fetch_full_content={args.full_content},
)

flow = WebSearchFlow()
result = asyncio.run(flow.execute(input_params))

# Format output
if {json.dumps(args.output)} == "markdown":
    print(f"# 🔍 Search Results: {{result.query}}\\n")
    print(f"**Total**: {{result.total_results}} | **Time**: {{result.search_time/1000:.2f}}s | **Engines**: {{', '.join(result.engines_used)}}\\n")
    print("---\\n")

    for i, r in enumerate(result.results, 1):
        print(f"## {{i}}. {{r.title}} ({{r.relevance_score:.1f}}/100)")
        print(f"**URL**: {{r.url}}")
        print(f"**Domain**: {{r.source}} | **Engine**: {{r.engine}}")
        if r.publish_date:
            print(f" | **Date**: {{r.publish_date}}")
        print(f"\\n{{r.snippet}}\\n")
        print("---\\n")

    if result.quality:
        print("\\n## 📊 Quality Metrics")
        for k, v in result.quality.items():
            if isinstance(v, (int, float)):
                print(f"- **{{k.replace('_', ' ').title()}}**: {{v}}")
elif {json.dumps(args.output)} == "json":
    import json
    output = {{
        "query": result.query,
        "total_results": result.total_results,
        "search_time_ms": round(result.search_time, 2),
        "results": [
            {{
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "score": round(r.relevance_score, 1),
                "domain": r.source
            }}
            for r in result.results
        ]
    }}
    print(json.dumps(output, indent=2, ensure_ascii=False))
elif {json.dumps(args.output)} == "compact":
    print(f"🔍 {{result.query}} ({{result.total_results}} results, {{result.search_time/1000:.2f}}s)")
    for i, r in enumerate(result.results[:10], 1):
        print(f"{{i}}. [{{r.relevance_score:.1f}}] {{r.title}}")
        print(f"   {{r.url}}")
'''

    try:
        result = subprocess.run(
            [sys.executable, "-c", python_code],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr and result.returncode != 0:
            print("Error:", result.stderr, file=sys.stderr)
            sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        print("Error: Search timed out after 60 seconds", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
