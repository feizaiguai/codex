#!/usr/bin/env python3
"""20-theme-designer CLI"""
import argparse
from pathlib import Path
from engine import ThemeDesigner, ThemeExporter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="20-theme-designer: 主题设计器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --name CodexTheme --primary #2563eb --secondary #10b981 --accent #f97316 --format css --output theme.css
        """,
    )
    parser.add_argument("--name", required=True, help="主题名称")
    parser.add_argument("--primary", required=True, help="主色")
    parser.add_argument("--secondary", required=True, help="辅色")
    parser.add_argument("--accent", required=True, help="强调色")
    parser.add_argument("--format", choices=["css", "json"], default="css")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    designer = ThemeDesigner()
    exporter = ThemeExporter()
    theme = designer.create_theme(args.name, args.primary, args.secondary, args.accent)

    output = exporter.to_css_vars(theme) if args.format == "css" else exporter.to_json(theme)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())