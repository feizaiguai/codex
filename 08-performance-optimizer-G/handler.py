#!/usr/bin/env python3
"""08-performance-optimizer CLI"""
import argparse
import json
import sys
from pathlib import Path
from engine import PerformanceOptimizer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="08-performance-optimizer: 性能优化专家",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --file handler.py
  python handler.py --file handler.py --json --output report.json
        """,
    )
    parser.add_argument("--file", required=True, help="待分析的代码文件")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    optimizer = PerformanceOptimizer()
    analysis = optimizer.analyze_file(args.file)

    if args.json:
        output = json.dumps(analysis, ensure_ascii=False, indent=2)
    else:
        output = optimizer.generate_report(analysis)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())