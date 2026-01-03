#!/usr/bin/env python3
"""06-documentation CLI"""
import argparse
import sys
from pathlib import Path
from engine import DocumentationEngine


def main() -> int:
    parser = argparse.ArgumentParser(
        description="06-documentation: 文档生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 README
  python handler.py --readme --source README.md --output README.generated.md

  # 生成 ADR
  python handler.py --adr --title "缓存策略" --context "现状" --decision "采用Redis" --consequences "需要运维" --output ADR.md

  # 生成 API 文档
  python handler.py --api --source handler.py --output API.md

  # 一次性生成全部
  python handler.py --all --source handler.py --out-dir ./docs
        """
    )

    parser.add_argument("--readme", action="store_true", help="生成 README")
    parser.add_argument("--adr", action="store_true", help="生成 ADR")
    parser.add_argument("--api", action="store_true", help="生成 API 文档")
    parser.add_argument("--all", action="store_true", help="生成全部文档")

    parser.add_argument("--source", help="源文件路径")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--out-dir", help="输出目录")

    parser.add_argument("--title", default="架构决策", help="ADR 标题")
    parser.add_argument("--context", default="", help="ADR 背景")
    parser.add_argument("--decision", default="", help="ADR 决策")
    parser.add_argument("--consequences", default="", help="ADR 影响")

    args = parser.parse_args()
    engine = DocumentationEngine()

    if args.readme:
        if not args.source:
            print("错误: --readme 需要 --source", file=sys.stderr)
            return 1
        output = Path(args.output or "README.generated.md")
        output.write_text(engine.generate_readme(args.source), encoding="utf-8")
        print(output.read_text(encoding="utf-8"))
        print(f"\n已生成: {output}")
        return 0

    if args.adr:
        output = Path(args.output or "ADR.generated.md")
        output.write_text(
            engine.generate_adr(args.title, args.context, args.decision, args.consequences),
            encoding="utf-8",
        )
        print(output.read_text(encoding="utf-8"))
        print(f"\n已生成: {output}")
        return 0

    if args.api:
        if not args.source:
            print("错误: --api 需要 --source", file=sys.stderr)
            return 1
        output = Path(args.output or "API.generated.md")
        output.write_text(engine.generate_api_docs(args.source), encoding="utf-8")
        print(output.read_text(encoding="utf-8"))
        print(f"\n已生成: {output}")
        return 0

    if args.all:
        if not args.source:
            print("错误: --all 需要 --source", file=sys.stderr)
            return 1
        out_dir = args.out_dir or "./docs"
        files = engine.generate_all_docs(args.source, out_dir)
        print("\n".join(str(p) for p in files))
        print(f"\n已生成 {len(files)} 份文档")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())