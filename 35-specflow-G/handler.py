#!/usr/bin/env python3
"""35-specflow CLI"""
import argparse
from pathlib import Path
import sys

from specflow import generate_specification


def main() -> int:
    parser = argparse.ArgumentParser(
        description="35-specflow: 需求标准化与验证",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --task "开发订单管理系统" --output ./specs
  python handler.py --doc requirements.md --depth standard --output ./specs
        """,
    )
    parser.add_argument("--task", help="需求描述文本")
    parser.add_argument("--doc", help="需求文档路径")
    parser.add_argument("--depth", choices=["simple", "standard", "comprehensive"], default="standard")
    parser.add_argument("--output", default="./output", help="输出目录")
    parser.add_argument("--project", default="未命名项目")
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--atomic", action="store_true")

    args = parser.parse_args()
    if not args.task and not args.doc:
        print("错误: 必须提供 --task 或 --doc", file=sys.stderr)
        return 1

    if args.doc:
        task_description = Path(args.doc).read_text(encoding="utf-8", errors="replace")
    else:
        task_description = args.task

    spec = generate_specification(
        task_description=task_description,
        depth_level=args.depth,
        project_name=args.project,
        project_version=args.version,
        output_dir=args.output,
        enable_atomic=args.atomic,
    )

    print(f"\n✓ 规格文档已生成到 {args.output} 目录")
    print(f"✓ 总体质量等级: {spec.quality_report.metrics.overall_grade.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())