#!/usr/bin/env python3
"""24-cicd-pipeline-builder CLI"""
import argparse
from pathlib import Path
from engine import CICDPipelineBuilder, Platform


def main() -> int:
    parser = argparse.ArgumentParser(
        description="24-cicd-pipeline-builder: CI/CD 生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --platform github --output .github/workflows/ci.yml
  python handler.py --platform gitlab --output .gitlab-ci.yml
        """,
    )
    parser.add_argument("--platform", choices=["github", "gitlab"], default="github")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    builder = CICDPipelineBuilder()
    yaml = builder.build(Platform(args.platform))

    if args.output:
        Path(args.output).write_text(yaml, encoding="utf-8")
    print(yaml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())