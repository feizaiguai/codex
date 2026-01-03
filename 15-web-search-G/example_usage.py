"""
WebSearchFlow 使用示例
展示各种搜索场景的用法
"""

import asyncio
from main import search, WebSearchFlow
from models import WebSearchInput


async def example_1_quick_search():
    """示例1: 快速搜索 - 最简单的用法"""
    print("\n" + "="*60)
    print("示例1: 快速搜索")
    print("="*60)

    # 使用便捷函数 - 一行代码搞定
    result = await search("Python async programming")

    print(f"找到 {result.total_results} 个结果，耗时 {result.search_time:.0f}ms")

    # 显示前3个结果
    for idx, r in enumerate(result.results[:3], 1):
        print(f"\n{idx}. {r.title}")
        print(f"   {r.url}")
        print(f"   {r.snippet[:100]}...")


async def example_2_fast_mode():
    """示例2: Fast模式 - 快速获取结果（5-7秒）"""
    print("\n" + "="*60)
    print("示例2: Fast模式 - 极速搜索")
    print("="*60)

    result = await search(
        query="React best practices 2024",
        mode="fast",              # 使用Brave + You.com
        max_results=10
    )

    print(f"搜索引擎: {', '.join(result.engines_used)}")
    print(f"结果数量: {result.total_results}")
    print(f"搜索时间: {result.search_time:.0f}ms")
    print(f"平均相关性: {result.quality['relevance_score']:.1f}/100")


async def example_3_deep_mode():
    """示例3: Deep模式 - 深度搜索 + AI答案"""
    print("\n" + "="*60)
    print("示例3: Deep模式 - 深度搜索 + AI答案")
    print("="*60)

    result = await search(
        query="What is quantum computing?",
        mode="deep",              # 使用Exa Deep + Perplexity + You.com
        max_results=20
    )

    # 查找Perplexity AI答案
    ai_answers = [r for r in result.results if r.engine == "perplexity"]
    if ai_answers:
        print("\n🤖 AI答案 (Perplexity):")
        print(ai_answers[0].snippet)
        print()

    # 显示推荐链接
    print("推荐阅读:")
    for link in result.summary['recommended_links'][:3]:
        print(f"  ⭐ {link['title']}")
        print(f"     {link['url']}")
        print(f"     推荐理由: {link['reason']}\n")


async def example_4_code_search():
    """示例4: 代码搜索 - 针对编程问题优化"""
    print("\n" + "="*60)
    print("示例4: 代码搜索")
    print("="*60)

    params = WebSearchInput(
        query="Python decorator example",
        search_type="code",       # 自动使用Exa Deep + Brave
        max_results=10
    )

    flow = WebSearchFlow()
    result = await flow.execute(params)

    print(f"代码搜索引擎: {', '.join(result.engines_used)}")
    print(f"\n前5个代码相关结果:")

    for idx, r in enumerate(result.results[:5], 1):
        print(f"{idx}. {r.title}")
        print(f"   {r.source} - {r.url}")


async def example_5_custom_engines():
    """示例5: 自定义引擎组合"""
    print("\n" + "="*60)
    print("示例5: 自定义引擎组合")
    print("="*60)

    params = WebSearchInput(
        query="TypeScript generics tutorial",
        search_engines=["exa_deep", "perplexity", "brave"],  # 自定义引擎组合
        max_results=15
    )

    flow = WebSearchFlow()
    result = await flow.execute(params)

    print(f"使用引擎: {', '.join(result.engines_used)}")
    print(f"结果数量: {result.total_results}")

    # 按引擎统计结果
    from collections import defaultdict
    engine_counts = defaultdict(int)
    for r in result.results:
        engine_counts[r.engine] += 1

    print("\n各引擎贡献:")
    for engine, count in engine_counts.items():
        print(f"  {engine}: {count}个结果")


async def example_6_with_full_content():
    """示例6: 提取完整网页内容（使用Jina Reader）"""
    print("\n" + "="*60)
    print("示例6: 提取完整网页内容")
    print("="*60)

    result = await search(
        query="OpenAI GPT-4 capabilities",
        mode="fast",
        max_results=3,           # 只取前3个
        fetch_full_content=True  # 启用完整内容提取
    )

    print(f"提取了 {len(result.results)} 个网页的完整内容:\n")

    for idx, r in enumerate(result.results, 1):
        if r.full_content:
            print(f"{idx}. {r.title}")
            print(f"   完整内容: {len(r.full_content)} 字符")

            # 如果提取到代码块
            if r.code_snippets:
                print(f"   代码块: {len(r.code_snippets)} 个")
                for snippet in r.code_snippets[:2]:
                    print(f"   - {snippet['language']}: {len(snippet['code'])} 行")
            print()


async def example_7_filtering():
    """示例7: 高级过滤和控制"""
    print("\n" + "="*60)
    print("示例7: 高级过滤")
    print("="*60)

    params = WebSearchInput(
        query="machine learning tutorial",
        language="en",                    # 仅英文结果
        time_range="month",               # 最近一个月
        site_filter=["github.com", "medium.com"],  # 只搜索这些网站
        max_results=10,
        deduplication=True                # 启用去重
    )

    flow = WebSearchFlow()
    result = await flow.execute(params)

    print(f"语言过滤: {params.language}")
    print(f"时间范围: {params.time_range}")
    print(f"网站过滤: {', '.join(params.site_filter)}")
    print(f"\n结果数量: {result.total_results}")

    # 显示高频域名
    print("\n高频域名:")
    for domain in result.summary['top_domains'][:5]:
        print(f"  {domain['domain']}: {domain['count']}个 ({domain['percentage']}%)")


async def example_8_quality_metrics():
    """示例8: 查看搜索质量指标"""
    print("\n" + "="*60)
    print("示例8: 搜索质量指标")
    print("="*60)

    result = await search(
        query="climate change solutions 2024",
        mode="deep",
        max_results=20
    )

    print("质量指标:")
    print(f"  相关性分数: {result.quality['relevance_score']:.1f}/100")
    print(f"  平均权威性: {result.quality['average_source_authority']:.1f}/100")
    print(f"  新鲜度分数: {result.quality['freshness_score']:.1f}/100")
    print(f"  覆盖度分数: {result.quality['coverage_score']:.1f}/100")

    # 显示查询优化
    if result.query_optimization:
        opt = result.query_optimization
        print(f"\n查询优化:")
        print(f"  原始查询: {opt['original']}")
        print(f"  优化查询: {opt['optimized']}")
        print(f"  检测语言: {opt['detected_language']}")


async def example_9_error_handling():
    """示例9: 错误处理 - 部分引擎失败"""
    print("\n" + "="*60)
    print("示例9: 容错处理")
    print("="*60)

    result = await search(
        query="artificial intelligence",
        mode="deep"
    )

    if result.partial_failures:
        print(f"⚠️ {len(result.partial_failures)} 个引擎部分失败:")
        for failure in result.partial_failures:
            print(f"  {failure['engine']}: {failure['error']}")
    else:
        print("✅ 所有引擎正常工作")

    # 即使部分失败，仍然返回可用结果
    print(f"\n仍然获得 {result.total_results} 个有效结果")


async def example_10_export_results():
    """示例10: 导出搜索结果"""
    print("\n" + "="*60)
    print("示例10: 导出搜索结果")
    print("="*60)

    result = await search(
        query="Docker best practices",
        mode="auto",
        max_results=10
    )

    # 转换为字典
    result_dict = result.to_dict()

    # 保存为JSON
    import json
    with open("search_results.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)

    print("✅ 搜索结果已导出到 search_results.json")
    print(f"   包含 {len(result_dict['results'])} 个结果")
    print(f"   文件大小: {len(json.dumps(result_dict))} 字节")


async def main():
    """运行所有示例"""
    print("\n" + "🎯"*30)
    print("WebSearchFlow 使用示例集合")
    print("🎯"*30)

    examples = [
        ("快速搜索", example_1_quick_search),
        ("Fast模式", example_2_fast_mode),
        ("Deep模式", example_3_deep_mode),
        ("代码搜索", example_4_code_search),
        ("自定义引擎", example_5_custom_engines),
        ("完整内容提取", example_6_with_full_content),
        ("高级过滤", example_7_filtering),
        ("质量指标", example_8_quality_metrics),
        ("错误处理", example_9_error_handling),
        ("导出结果", example_10_export_results),
    ]

    for name, example_func in examples:
        try:
            await example_func()
            await asyncio.sleep(1)  # 避免API限流
        except Exception as e:
            print(f"\n❌ 示例 '{name}' 失败: {str(e)}")

    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
