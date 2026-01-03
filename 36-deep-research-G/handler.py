#!/usr/bin/env python3
"""
36-deep-research 命令行接口

深度研究引擎：三 AI 协作搜索系统
- Claude: 技术深度分析、架构设计、安全最佳实践
- Gemini: 生态系统分析、趋势预测、社区洞察
- Codex: 代码实践、示例项目、工具链推荐

使用示例：
    python handler.py "React Server Components"
    python handler.py "Kubernetes security best practices"
    python handler.py --query "Python async programming" --max-tokens 15000
"""

import sys
import asyncio
import argparse
from pathlib import Path
from typing import Optional

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from deep_research import DeepResearchOrchestrator, estimate_tokens, split_report_by_tokens


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数命名空间
    """
    parser = argparse.ArgumentParser(
        description="深度研究引擎 - 三 AI 协作搜索系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s "React Server Components"
  %(prog)s --query "Kubernetes security" --max-tokens 15000
  %(prog)s -q "Python async" -o research_output.md

三 AI 分工：
  Claude:  技术深度、架构设计、安全实践
  Gemini:  生态系统、趋势分析、社区洞察
  Codex:   代码实践、示例项目、工具推荐
        """
    )

    parser.add_argument(
        'query',
        nargs='?',
        help='研究主题（如果使用 -q/--query 则此参数可选）'
    )

    parser.add_argument(
        '-q', '--query',
        dest='query_flag',
        help='研究主题（与位置参数二选一）'
    )

    parser.add_argument(
        '-o', '--output',
        help='输出文件名（默认自动生成）'
    )

    parser.add_argument(
        '--max-tokens',
        type=int,
        default=20000,
        help='每个文件的最大 token 数（默认 20000）'
    )

    parser.add_argument(
        '--no-split',
        action='store_true',
        help='禁用自动分割（即使超过 token 限制也保存为单文件）'
    )

    parser.add_argument(
        '--preview-lines',
        type=int,
        default=50,
        help='预览的行数（默认 50）'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    return parser.parse_args()


def get_query_from_args(args: argparse.Namespace) -> str:
    """
    从参数中获取查询字符串

    Args:
        args: 命令行参数

    Returns:
        查询字符串

    Raises:
        ValueError: 如果没有提供查询字符串
    """
    query = args.query or args.query_flag

    if not query:
        raise ValueError(
            "错误：必须提供研究主题\n\n"
            "使用方式：\n"
            "  python handler.py \"研究主题\"\n"
            "  python handler.py --query \"研究主题\"\n\n"
            "示例：\n"
            "  python handler.py \"React Server Components\"\n"
            "  python handler.py --query \"Kubernetes security best practices\""
        )

    return query


def generate_output_filename(query: str, output: Optional[str], part: Optional[int] = None) -> str:
    """
    生成输出文件名

    Args:
        query: 查询字符串
        output: 用户指定的输出文件名
        part: 分段编号（如果分割）

    Returns:
        输出文件名
    """
    if output:
        # 用户指定了文件名
        if part is not None:
            # 添加分段后缀
            base, ext = output.rsplit('.', 1) if '.' in output else (output, 'md')
            return f"{base}_part{part}.{ext}"
        return output
    else:
        # 自动生成文件名
        safe_query = query.replace(' ', '_')[:50]
        if part is not None:
            return f"research_{safe_query}_part{part}.md"
        return f"research_{safe_query}.md"


async def main() -> int:
    """
    主函数

    Returns:
        退出码（0 表示成功）
    """
    try:
        # 解析参数
        args = parse_arguments()

        # 获取查询字符串
        query = get_query_from_args(args)

        # 执行研究
        print(f"🔍 开始深度研究: {query}")
        print("=" * 80)

        orchestrator = DeepResearchOrchestrator()
        report = await orchestrator.execute(query)

        # 估算 token 数量
        estimated_tokens = estimate_tokens(report)

        if args.verbose:
            print(f"\n📊 报告统计:")
            print(f"  - 总字符数: {len(report):,}")
            print(f"  - 估算 tokens: {estimated_tokens:,}")
            print(f"  - Token 限制: {args.max_tokens:,}")

        # 检查是否需要分割
        if not args.no_split and estimated_tokens > args.max_tokens:
            print(f"\n⚠️  报告超过 {args.max_tokens:,} tokens 限制，自动分割为多个文件...")

            report_parts = split_report_by_tokens(report, max_tokens=args.max_tokens)

            # 保存多个文件
            saved_files = []

            for i, part in enumerate(report_parts, 1):
                output_file = generate_output_filename(query, args.output, part=i)

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(part)

                part_tokens = estimate_tokens(part)
                print(f"   ✅ Part {i}/{len(report_parts)}: {output_file} ({part_tokens:,} tokens)")
                saved_files.append(output_file)

            print(f"\n📄 报告已分割保存为 {len(report_parts)} 个文件:")
            for f in saved_files:
                print(f"   - {f}")
        else:
            # 单文件保存
            output_file = generate_output_filename(query, args.output)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"\n📄 报告已保存到: {output_file}")
            print(f"   - 总字符数: {len(report):,}")
            print(f"   - 估算 tokens: {estimated_tokens:,}")

        # 显示预览
        print("\n" + "=" * 80)
        print(f"报告预览（前 {args.preview_lines} 行）:")
        print("=" * 80)
        preview_lines = report.split('\n')[:args.preview_lines]
        print('\n'.join(preview_lines))

        if len(report.split('\n')) > args.preview_lines:
            print(f"\n... (完整报告共 {len(report.split('\n'))} 行，请查看文件)")

        print("\n✅ 研究完成！")
        return 0

    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
