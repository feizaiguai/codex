"""29-knowledge-manager 命令行接口
技术知识管理 - 智能文档生成与管理
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple, Union, Callable
from engine import KnowledgeManager, DocType


import logging

def main() -> None:
    if True:
        """主函数 - 命令行入口

    执行知识管理流程：
    1. 解析命令行参数
    2. 执行相应操作（添加/搜索/生成文档）
    3. 输出结果
    """
    parser = argparse.ArgumentParser(
        description='29-knowledge-manager: 技术知识管理',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加 API 文档
  python handler.py --add "用户API" --type api --content "用户相关API文档" --output docs/

  # 搜索文档
  python handler.py --search "API" --json

  # 生成知识库摘要
  python handler.py --summary --output summary.md

  # 列出所有文档
  python handler.py --list --type api

  # 生成 API 文档
  python handler.py --generate-api --source api_spec.json --output api_docs/

  # 生成架构文档
  python handler.py --generate-arch --title "系统架构" --output arch/
        """
    )

    # 文档操作
    parser.add_argument('--add', help='添加文档标题')
    parser.add_argument('--content', help='文档内容')
    parser.add_argument('--search', help='搜索关键词')
    parser.add_argument('--list', action='store_true', help='列出所有文档')
    parser.add_argument('--summary', action='store_true', help='生成知识库摘要')

    # 文档类型
    parser.add_argument(
        '--type',
        choices=['api', 'architecture', 'runbook', 'tutorial', 'faq'],
        default='tutorial',
        help='文档类型 (默认: tutorial)'
    )

    # 文档生成
    parser.add_argument('--generate-api', help='生成 API 文档（指定源文件）')
    parser.add_argument('--generate-arch', help='生成架构文档（指定标题）')
    parser.add_argument('--generate-runbook', help='生成 Runbook（指定标题）')

    parser.add_argument('--source', help='源文件路径')
    parser.add_argument('--title', help='文档标题')

    # 输出选项
    parser.add_argument('--output', '-o', help='输出目录或文件')
    parser.add_argument('--json', action='store_true', help='JSON 输出格式')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    args = parser.parse_args()

    try:
        manager = KnowledgeManager()

        # 添加文档
        if args.add:
            if not args.content:
                print("错误: 添加文档需要 --content 参数", file=sys.stderr)
                sys.exit(1)

            doc_type = DocType(args.type)
            manager.add_document(args.add, args.content, doc_type)

            print(f"✓ 已添加 {args.type} 文档: {args.add}")

        # 搜索文档
        elif args.search:
            results = manager.search_documents(args.search)

            if args.json:
                print(json.dumps({
                    'query': args.search,
                    'total': len(results),
                    'results': results
                }, indent=2, ensure_ascii=False))
            else:
                print(f"找到 {len(results)} 篇文档:\n")
                for i, doc in enumerate(results, 1):
                    print(f"{i}. [{doc['type']}] {doc['title']}")
                    if args.verbose:
                        print(f"   {doc.get('summary', '')[:100]}...")
                    print()

        # 列出文档
        elif args.list:
            docs = manager.list_documents(doc_type=args.type if args.type != 'tutorial' else None)

            if args.json:
                print(json.dumps(docs, indent=2, ensure_ascii=False))
            else:
                print(f"{'所有' if not args.type else args.type.upper()} 文档列表:\n")
                for i, doc in enumerate(docs, 1):
                    print(f"{i}. [{doc['type']}] {doc['title']}")
                    if args.verbose:
                        print(f"   创建时间: {doc.get('created', 'N/A')}")
                    print()

        # 生成摘要
        elif args.summary:
            summary = manager.generate_summary()

            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(summary, encoding='utf-8')
                print(f"✓ 摘要已保存到: {args.output}")
            else:
                print(summary)

        # 生成 API 文档
        elif args.generate_api:
            if not args.output:
                print("错误: 生成文档需要 --output 参数", file=sys.stderr)
                sys.exit(1)

            # 假设有 generate_api_docs 方法
            docs = manager.generate_api_docs(args.generate_api)

            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            for filename, content in docs.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding='utf-8')
                print(f"✓ 已生成: {filepath}")

        # 生成架构文档
        elif args.generate_arch:
            if not args.output:
                print("错误: 生成文档需要 --output 参数", file=sys.stderr)
                sys.exit(1)

            docs = manager.generate_architecture_docs(args.generate_arch)

            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            for filename, content in docs.items():
                filepath = output_dir / filename
                filepath.write_text(content, encoding='utf-8')
                print(f"✓ 已生成: {filepath}")

        # 生成 Runbook
        elif args.generate_runbook:
            if not args.output:
                print("错误: 生成文档需要 --output 参数", file=sys.stderr)
                sys.exit(1)

            runbook = manager.generate_runbook(args.generate_runbook)

            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(runbook, encoding='utf-8')

            print(f"✓ Runbook 已生成: {args.output}")

        else:
            parser.print_help()

    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"错误: 权限不足 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
