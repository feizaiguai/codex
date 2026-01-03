#!/usr/bin/env python3
"""
15-web-search-G 命令行接口
智能网络搜索工具 - 集成 6 个搜索 API
"""

import sys
import os
import asyncio
import json
from pathlib import Path
from typing import Optional

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from search import WebSearchEngine
    from models import WebSearchInput
except ImportError:
    print("错误: 无法导入必要的模块。请确保所有依赖已安装。", file=sys.stderr)
    sys.exit(1)


def format_json_output(result: dict) -> str:
    """格式化为 JSON 输出

    Args:
        result: 搜索结果字典

    Returns:
        格式化的 JSON 字符串
    """
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_markdown_output(result: dict) -> str:
    """格式化为 Markdown 输出

    Args:
        result: 搜索结果字典

    Returns:
        格式化的 Markdown 字符串
    """
    lines = []

    # 标题
    query = result.get('query', 'N/A')
    lines.append(f"# 🔍 搜索结果: {query}\n")

    # 元信息
    total = result.get('total_results', 0)
    search_time = result.get('search_time_ms', 0) / 1000
    engines = result.get('engines_used', [])
    lines.append(f"**总结果数**: {total} | **搜索用时**: {search_time:.2f}s | **使用引擎**: {', '.join(engines)}\n")
    lines.append("---\n")

    # 搜索结果
    results = result.get('results', [])
    for i, r in enumerate(results, 1):
        title = r.get('title', 'N/A')
        score = r.get('score', 0)
        url = r.get('url', '#')
        domain = r.get('domain', 'N/A')
        engine = r.get('engine', 'N/A')
        snippet = r.get('snippet', '')

        lines.append(f"## {i}. {title} ({score}/100)\n")
        lines.append(f"**URL**: {url}\n")
        lines.append(f"**来源**: {domain} | **引擎**: {engine}\n")

        if 'published_date' in r and r['published_date']:
            lines.append(f"**日期**: {r['published_date']}\n")

        lines.append(f"\n{snippet}\n")
        lines.append("---\n")

    # 质量指标
    if 'quality_metrics' in result and result['quality_metrics']:
        lines.append("\n## 📊 质量指标\n")
        for metric, value in result['quality_metrics'].items():
            if isinstance(value, (int, float)):
                lines.append(f"- **{metric.replace('_', ' ').title()}**: {value}\n")

    return "".join(lines)


def format_compact_output(result: dict) -> str:
    """格式化为紧凑输出

    Args:
        result: 搜索结果字典

    Returns:
        格式化的紧凑字符串
    """
    lines = []

    query = result.get('query', 'N/A')
    total = result.get('total_results', 0)
    search_time = result.get('search_time_ms', 0) / 1000

    lines.append(f"🔍 {query} ({total} 个结果, {search_time:.2f}s)\n")

    results = result.get('results', [])[:10]  # 只显示前10个
    for i, r in enumerate(results, 1):
        title = r.get('title', 'N/A')
        score = r.get('score', 0)
        url = r.get('url', '#')

        lines.append(f"{i}. [{score}] {title}\n")
        lines.append(f"   {url}\n")

    if len(result.get('results', [])) > 10:
        remaining = len(result.get('results', [])) - 10
        lines.append(f"\n... 还有 {remaining} 个结果\n")

    return "".join(lines)


async def execute_search(
    query: str,
    mode: str = 'auto',
    max_results: Optional[int] = None,
    time_range: str = 'all',
    language: Optional[str] = None,
    site: Optional[str] = None,
    full_content: bool = False,
    output_format: str = 'markdown'
) -> None:
    """执行搜索并输出结果

    Args:
        query: 搜索查询
        mode: 搜索模式 (fast/auto/deep)
        max_results: 最大结果数
        time_range: 时间范围
        language: 语言过滤
        site: 站点过滤
        full_content: 是否获取完整内容
        output_format: 输出格式
    """
    # 自动设置 max_results
    if max_results is None:
        max_results = {
            'fast': 10,
            'auto': 15,
            'deep': 25
        }.get(mode, 15)

    # 创建搜索引擎
    engine = WebSearchEngine()

    # 构建搜索参数
    search_params = {
        'query': query,
        'max_results': max_results,
        'time_range': time_range,
    }

    if language:
        search_params['language'] = language
    if site:
        search_params['site_filter'] = [site]

    try:
        # 执行搜索
        result = await engine.search(**search_params)

        # 转换为字典
        result_dict = {
            'query': query,
            'total_results': len(result.get('results', [])),
            'search_time_ms': result.get('search_time_ms', 0),
            'engines_used': result.get('engines_used', []),
            'results': [
                {
                    'title': r.get('title', ''),
                    'url': r.get('url', ''),
                    'snippet': r.get('snippet', ''),
                    'score': round(r.get('relevance_score', 0), 1),
                    'domain': r.get('source', ''),
                    'engine': r.get('engine', ''),
                    'published_date': r.get('publish_date', None)
                }
                for r in result.get('results', [])
            ],
            'quality_metrics': result.get('quality', {}),
        }

        # 格式化输出
        if output_format == 'json':
            print(format_json_output(result_dict))
        elif output_format == 'markdown':
            print(format_markdown_output(result_dict))
        elif output_format == 'compact':
            print(format_compact_output(result_dict))

    except Exception as e:
        error_dict = {
            'error': str(e),
            'type': type(e).__name__,
            'query': query
        }
        print(json.dumps(error_dict, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """主函数 - 命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='15-web-search-G: 智能网络搜索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 快速搜索 (5-7秒)
  python handler.py "Python asyncio" --mode fast

  # 自动模式搜索 (8-12秒)
  python handler.py "Vue 3 最佳实践" --mode auto --time-range month

  # 深度搜索 (15-20秒)
  python handler.py "TypeScript 泛型" --mode deep --max-results 20

  # 站点特定搜索
  python handler.py "Docker 网络" --site stackoverflow.com

  # JSON 输出
  python handler.py "React hooks" --output json

模式说明:
  fast - 5-7秒  - Brave + You.com - 10 个结果
  auto - 8-12秒 - Exa + Brave     - 15 个结果 (默认)
  deep - 15-20秒- Exa + Perplexity + You.com + 完整内容 - 25 个结果
        """
    )

    # 必需参数
    parser.add_argument('query', help='搜索查询')

    # 模式选择
    parser.add_argument(
        '--mode',
        choices=['fast', 'auto', 'deep'],
        default='auto',
        help='搜索模式 (默认: auto)'
    )

    # 结果控制
    parser.add_argument(
        '--max-results',
        type=int,
        help='最大结果数 (不指定则根据模式自动设置)'
    )

    # 过滤器
    parser.add_argument(
        '--time-range',
        choices=['day', 'week', 'month', 'year', 'all'],
        default='all',
        help='时间范围过滤 (默认: all)'
    )

    parser.add_argument(
        '--language',
        help='语言过滤 (如: en, zh, es)'
    )

    parser.add_argument(
        '--site',
        help='站点过滤 (如: github.com, stackoverflow.com)'
    )

    # 内容选项
    parser.add_argument(
        '--full-content',
        action='store_true',
        help='获取完整内容 (建议使用 deep 模式)'
    )

    # 输出格式
    parser.add_argument(
        '--output',
        choices=['json', 'markdown', 'compact'],
        default='markdown',
        help='输出格式 (默认: markdown)'
    )

    args = parser.parse_args()

    # 执行搜索
    asyncio.run(execute_search(
        query=args.query,
        mode=args.mode,
        max_results=args.max_results,
        time_range=args.time_range,
        language=args.language,
        site=args.site,
        full_content=args.full_content,
        output_format=args.output
    ))


if __name__ == '__main__':
    main()
