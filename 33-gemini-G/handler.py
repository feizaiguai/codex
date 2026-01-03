#!/usr/bin/env python3
"""
33-gemini 命令行接口（增强版）
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 导入引擎
try:
    from engine import *
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from engine import *


def main() -> None:
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description='33-gemini: 增强版命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 分析命令
    analyze_parser = subparsers.add_parser('analyze', help='分析和检查')
    analyze_parser.add_argument('input', help='输入文件或数据')
    analyze_parser.add_argument('--output', '-o', help='输出文件')
    analyze_parser.add_argument('--format', choices=['json', 'text'], default='text')

    # 生成命令
    generate_parser = subparsers.add_parser('generate', help='生成报告或文档')
    generate_parser.add_argument('--template', help='模板文件')
    generate_parser.add_argument('--output', '-o', default='./output', help='输出目录')

    # 验证命令
    validate_parser = subparsers.add_parser('validate', help='验证和测试')
    validate_parser.add_argument('file', help='要验证的文件')
    validate_parser.add_argument('--strict', action='store_true', help='严格模式')

    # 通用参数
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # 执行命令
        if args.command == 'analyze':
            result = execute_analyze(args)
        elif args.command == 'generate':
            result = execute_generate(args)
        elif args.command == 'validate':
            result = execute_validate(args)
        else:
            print(f"错误：未知命令 '{args.command}'", file=sys.stderr)
            return 1

        # 输出结果
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_result(result)

        return 0

    except FileNotFoundError as e:
        print(f"错误：文件未找到 - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def execute_analyze(args: argparse.Namespace) -> Dict[str, Any]:
    """执行分析命令"""
    p = Path(args.input)
    if p.exists():
        text = p.read_text(encoding="utf-8", errors="replace")
        source = str(p)
    else:
        text = args.input
        source = "<inline>"

    lines = text.splitlines()
    words = text.split()
    return {
        "status": "success",
        "source": source,
        "lines": len(lines),
        "words": len(words),
        "chars": len(text),
    }


def execute_generate(args: argparse.Namespace) -> Dict[str, Any]:
    """执行生成命令"""
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "gemini_report.md"
    content = "生成报告\n\n"
    if args.template:
        template = Path(args.template).read_text(encoding="utf-8", errors="replace")
        content += f"模板行数: {len(template.splitlines())}\n"
    report_path.write_text(content, encoding="utf-8")
    return {"status": "success", "report": str(report_path)}


def execute_validate(args: argparse.Namespace) -> Dict[str, Any]:
    """执行验证命令"""
    p = Path(args.file)
    if not p.exists():
        return {"status": "fail", "message": "文件不存在"}
    size = p.stat().st_size
    if args.strict:
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            return {"status": "fail", "message": "文件为空"}
    return {"status": "success", "size": size}


def print_result(result: Dict[str, Any]) -> None:
    """打印结果"""
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == '__main__':
    sys.exit(main() or 0)
