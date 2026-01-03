#!/usr/bin/env python3
"""27-explainability-analyzer CLI"""
import argparse
import json
from pathlib import Path
from engine import ExplainabilityAnalyzer


def main() -> int:
    parser = argparse.ArgumentParser(
        description="27-explainability-analyzer: 可解释性分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --data data.csv --target label --output report.md
  python handler.py --data data.csv --target label --sensitive gender --json
        """,
    )
    parser.add_argument("--data", required=True, help="CSV 数据文件")
    parser.add_argument("--target", required=True, help="目标列")
    parser.add_argument("--sensitive", help="敏感列")
    parser.add_argument("--top-k", type=int, default=5, help="Top 特征数量")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    analyzer = ExplainabilityAnalyzer()
    analysis = analyzer.analyze_csv(args.data, args.target, args.sensitive, args.top_k)

    output = json.dumps(analysis, ensure_ascii=False, indent=2) if args.json else analyzer.generate_report(analysis)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())