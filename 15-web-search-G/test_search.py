"""
WebSearchFlow 综合测试脚本
测试所有6个API在集成环境下的工作情况
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from main import WebSearchFlow, search
from models import WebSearchInput


class WebSearchTester:
    """WebSearchFlow测试器"""

    def __init__(self):
        self.flow = WebSearchFlow()
        self.test_results = []

    async def test_fast_mode(self) -> Dict[str, Any]:
        """测试Fast模式 (Brave + You.com)"""
        print("\n" + "="*60)
        print("测试1: Fast模式 - 快速搜索")
        print("="*60)

        try:
            result = await search(
                query="Python async programming",
                mode="fast",
                max_results=10
            )

            success = result.success and len(result.results) > 0

            print(f"✅ 查询: {result.query}")
            print(f"✅ 搜索时间: {result.search_time:.2f}ms")
            print(f"✅ 结果数量: {result.total_results}")
            print(f"✅ 使用引擎: {', '.join(result.engines_used)}")
            print(f"✅ 平均相关性: {result.quality.get('relevance_score', 0):.1f}")

            if result.partial_failures:
                print(f"⚠️ 部分失败: {len(result.partial_failures)}个引擎")
                for failure in result.partial_failures:
                    print(f"   - {failure['engine']}: {failure['error']}")

            # 显示前3个结果
            print("\n前3个结果:")
            for idx, r in enumerate(result.results[:3], 1):
                print(f"\n{idx}. {r.title}")
                print(f"   URL: {r.url}")
                print(f"   来源: {r.source} | 引擎: {r.engine}")
                print(f"   相关性: {r.relevance_score:.1f} | 安全: {'HTTPS' if r.is_secure else 'HTTP'}")

            return {
                "test_name": "Fast Mode",
                "success": success,
                "search_time": result.search_time,
                "results_count": result.total_results,
                "engines_used": result.engines_used,
                "quality": result.quality
            }

        except Exception as e:
            print(f"❌ Fast模式测试失败: {str(e)}")
            return {"test_name": "Fast Mode", "success": False, "error": str(e)}

    async def test_auto_mode(self) -> Dict[str, Any]:
        """测试Auto模式 (Exa Auto + Brave)"""
        print("\n" + "="*60)
        print("测试2: Auto模式 - 自动优化搜索")
        print("="*60)

        try:
            result = await search(
                query="TypeScript best practices 2024",
                mode="auto",
                max_results=15
            )

            success = result.success and len(result.results) > 0

            print(f"✅ 查询: {result.query}")
            print(f"✅ 搜索时间: {result.search_time:.2f}ms")
            print(f"✅ 结果数量: {result.total_results}")
            print(f"✅ 使用引擎: {', '.join(result.engines_used)}")
            print(f"✅ 覆盖度分数: {result.quality.get('coverage_score', 0):.1f}")

            # 显示查询优化
            if result.query_optimization:
                opt = result.query_optimization
                print(f"\n查询优化:")
                print(f"  原始: {opt['original']}")
                print(f"  优化: {opt['optimized']}")
                if opt['added_terms']:
                    print(f"  添加词: {', '.join(opt['added_terms'])}")

            # 显示高频域名
            if result.summary.get('top_domains'):
                print(f"\n高频域名:")
                for domain in result.summary['top_domains'][:3]:
                    print(f"  {domain['domain']}: {domain['count']}个结果 ({domain['percentage']}%)")

            return {
                "test_name": "Auto Mode",
                "success": success,
                "search_time": result.search_time,
                "results_count": result.total_results,
                "engines_used": result.engines_used,
                "quality": result.quality
            }

        except Exception as e:
            print(f"❌ Auto模式测试失败: {str(e)}")
            return {"test_name": "Auto Mode", "success": False, "error": str(e)}

    async def test_deep_mode(self) -> Dict[str, Any]:
        """测试Deep模式 (Exa Deep + Perplexity + You.com)"""
        print("\n" + "="*60)
        print("测试3: Deep模式 - 深度搜索 + AI答案")
        print("="*60)

        try:
            result = await search(
                query="What is the future of AI in 2025?",
                mode="deep",
                max_results=10,
                fetch_full_content=False  # 暂不提取完整内容以加快测试
            )

            success = result.success and len(result.results) > 0

            print(f"✅ 查询: {result.query}")
            print(f"✅ 搜索时间: {result.search_time:.2f}ms")
            print(f"✅ 结果数量: {result.total_results}")
            print(f"✅ 使用引擎: {', '.join(result.engines_used)}")

            # 检查是否有Perplexity AI答案
            perplexity_results = [r for r in result.results if r.engine == "perplexity"]
            if perplexity_results:
                print(f"\n🤖 Perplexity AI答案:")
                ai_answer = perplexity_results[0]
                print(f"   {ai_answer.snippet[:200]}...")

            # 显示推荐链接
            if result.summary.get('recommended_links'):
                print(f"\n推荐链接:")
                for link in result.summary['recommended_links'][:3]:
                    print(f"  {link['title'][:50]}...")
                    print(f"  {link['url']}")
                    print(f"  推荐理由: {link['reason']} (分数: {link['score']:.1f})")
                    print()

            return {
                "test_name": "Deep Mode",
                "success": success,
                "search_time": result.search_time,
                "results_count": result.total_results,
                "engines_used": result.engines_used,
                "has_ai_answer": len(perplexity_results) > 0,
                "quality": result.quality
            }

        except Exception as e:
            print(f"❌ Deep模式测试失败: {str(e)}")
            return {"test_name": "Deep Mode", "success": False, "error": str(e)}

    async def test_code_search(self) -> Dict[str, Any]:
        """测试代码搜索模式"""
        print("\n" + "="*60)
        print("测试4: 代码搜索模式")
        print("="*60)

        try:
            params = WebSearchInput(
                query="React useState hook example",
                search_type="code",
                max_results=10,
                fetch_full_content=False
            )

            result = await self.flow.execute(params)

            success = result.success and len(result.results) > 0

            print(f"✅ 查询: {result.query}")
            print(f"✅ 搜索时间: {result.search_time:.2f}ms")
            print(f"✅ 结果数量: {result.total_results}")
            print(f"✅ 使用引擎: {', '.join(result.engines_used)}")

            # 显示代码相关结果
            print(f"\n代码相关结果:")
            for idx, r in enumerate(result.results[:3], 1):
                print(f"\n{idx}. {r.title}")
                print(f"   {r.url}")
                print(f"   {r.snippet[:100]}...")

            return {
                "test_name": "Code Search",
                "success": success,
                "search_time": result.search_time,
                "results_count": result.total_results,
                "engines_used": result.engines_used
            }

        except Exception as e:
            print(f"❌ 代码搜索测试失败: {str(e)}")
            return {"test_name": "Code Search", "success": False, "error": str(e)}

    async def test_deduplication(self) -> Dict[str, Any]:
        """测试去重功能（URL + 语义）"""
        print("\n" + "="*60)
        print("测试5: 去重功能测试")
        print("="*60)

        try:
            # 使用多个引擎搜索相同查询，验证去重
            params = WebSearchInput(
                query="Python tutorial for beginners",
                search_engines=["exa_auto", "brave", "you"],  # 使用3个引擎
                max_results=20,
                deduplication=True
            )

            result = await self.flow.execute(params)

            # 检查URL唯一性
            urls = [r.url for r in result.results]
            unique_urls = set(urls)

            success = len(urls) == len(unique_urls)  # 所有URL应该唯一

            print(f"✅ 总结果数: {len(result.results)}")
            print(f"✅ 唯一URL数: {len(unique_urls)}")
            print(f"✅ 去重状态: {'成功' if success else '失败'}")
            print(f"✅ 使用引擎: {', '.join(result.engines_used)}")

            if not success:
                print(f"⚠️ 发现重复URL!")

            return {
                "test_name": "Deduplication",
                "success": success,
                "total_results": len(result.results),
                "unique_urls": len(unique_urls),
                "dedup_working": success
            }

        except Exception as e:
            print(f"❌ 去重测试失败: {str(e)}")
            return {"test_name": "Deduplication", "success": False, "error": str(e)}

    async def test_content_enhancement(self) -> Dict[str, Any]:
        """测试内容增强功能（Jina Reader）"""
        print("\n" + "="*60)
        print("测试6: 内容增强测试（Jina Reader）")
        print("="*60)

        try:
            params = WebSearchInput(
                query="OpenAI GPT-4",
                mode="fast",
                max_results=3,  # 只取前3个以加快测试
                fetch_full_content=True  # 启用内容提取
            )

            result = await self.flow.execute(params)

            # 检查是否成功提取完整内容
            enhanced_count = sum(1 for r in result.results if r.full_content)

            success = enhanced_count > 0

            print(f"✅ 结果数量: {len(result.results)}")
            print(f"✅ 成功增强: {enhanced_count}个")
            print(f"✅ 增强率: {enhanced_count/len(result.results)*100:.1f}%")

            # 显示增强的结果
            for idx, r in enumerate(result.results, 1):
                if r.full_content:
                    print(f"\n{idx}. {r.title}")
                    print(f"   完整内容长度: {len(r.full_content)}字符")
                    if r.code_snippets:
                        print(f"   代码块数量: {len(r.code_snippets)}")
                        for snippet in r.code_snippets[:2]:
                            print(f"   - {snippet['language']}: {len(snippet['code'])}字符")

            return {
                "test_name": "Content Enhancement",
                "success": success,
                "total_results": len(result.results),
                "enhanced_count": enhanced_count,
                "enhancement_rate": enhanced_count/len(result.results)*100 if result.results else 0
            }

        except Exception as e:
            print(f"❌ 内容增强测试失败: {str(e)}")
            return {"test_name": "Content Enhancement", "success": False, "error": str(e)}

    async def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "🎯"*30)
        print("WebSearchFlow 综合测试开始")
        print("🎯"*30)

        start_time = datetime.now()

        # 运行所有测试
        tests = [
            self.test_fast_mode(),
            self.test_auto_mode(),
            self.test_deep_mode(),
            self.test_code_search(),
            self.test_deduplication(),
            self.test_content_enhancement()
        ]

        results = await asyncio.gather(*tests, return_exceptions=True)

        # 统计结果
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
        total_count = len(results)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 生成测试报告
        print("\n" + "="*60)
        print("📊 测试总结报告")
        print("="*60)
        print(f"\n总测试数: {total_count}")
        print(f"成功: {success_count}")
        print(f"失败: {total_count - success_count}")
        print(f"成功率: {success_count/total_count*100:.1f}%")
        print(f"总耗时: {duration:.2f}秒")

        print("\n" + "-"*60)
        print("详细结果:")
        print("-"*60)

        for idx, result in enumerate(results, 1):
            if isinstance(result, dict):
                status = "✅" if result.get('success') else "❌"
                print(f"{idx}. {status} {result.get('test_name', 'Unknown')}")
                if result.get('error'):
                    print(f"   错误: {result['error']}")
            else:
                print(f"{idx}. ❌ 测试异常: {str(result)}")

        # 保存报告到JSON
        report = {
            "test_date": start_time.isoformat(),
            "duration_seconds": duration,
            "total_tests": total_count,
            "success_count": success_count,
            "success_rate": success_count/total_count*100,
            "results": [r for r in results if isinstance(r, dict)]
        }

        report_path = "test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n📄 详细报告已保存到: {report_path}")

        # 最终评分
        if success_count == total_count:
            print("\n🎉 所有测试通过！WebSearchFlow v3.0 已准备好生产部署！")
        elif success_count >= total_count * 0.8:
            print(f"\n⚠️ {success_count}/{total_count}测试通过，部分功能需要检查")
        else:
            print(f"\n❌ 多个测试失败，需要修复后再部署")

        return report


async def main():
    """主测试函数"""
    tester = WebSearchTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
