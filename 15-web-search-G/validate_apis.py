"""
API Validation Script for 15-WebSearchFlow
验证所有搜索引擎API的可用性

测试以下7个API:
1. Exa.ai - 语义搜索
2. Brave Search - 隐私搜索
3. Perplexity - AI搜索
4. Jina Reader - 网页阅读
5. Jina Embedding - 语义嵌入
6. Gemini - AI模型
7. You.com - 搜索引擎
"""

import os
import asyncio
import httpx
import json
from typing import Dict, List, Any
from datetime import datetime


class APIValidator:
    """API验证器"""

    def __init__(self):
        self.results: List[Dict[str, Any]] = []

    async def test_exa_api(self) -> Dict[str, Any]:
        """测试 Exa.ai API"""
        print("\n🔍 Testing Exa.ai API...")

        api_key = os.getenv("EXA_API_KEY", "")
        url = "https://api.exa.ai/search"

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "query": "Python async programming",
            "numResults": 3,
            "type": "auto"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    result_count = len(data.get("results", []))

                    print(f"✅ Exa.ai: SUCCESS - Got {result_count} results")
                    return {
                        "name": "Exa.ai",
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "result_count": result_count,
                        "features": ["Fast search", "Auto mode", "Deep search", "Neural search"],
                        "sample_response": data.get("results", [])[:1]
                    }
                else:
                    print(f"❌ Exa.ai: FAILED - Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return {
                        "name": "Exa.ai",
                        "status": "❌ FAILED",
                        "endpoint": url,
                        "error": f"HTTP {response.status_code}: {response.text[:200]}"
                    }

        except Exception as e:
            print(f"❌ Exa.ai: ERROR - {str(e)}")
            return {
                "name": "Exa.ai",
                "status": "❌ ERROR",
                "endpoint": url,
                "error": str(e)
            }

    async def test_brave_api(self) -> Dict[str, Any]:
        """测试 Brave Search API"""
        print("\n🔍 Testing Brave Search API...")

        api_key = os.getenv("BRAVE_API_KEY", "")
        url = "https://api.search.brave.com/res/v1/web/search"

        headers = {
            "X-Subscription-Token": api_key,
            "Accept": "application/json"
        }

        params = {
            "q": "Python async programming",
            "count": 3
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    web_results = data.get("web", {}).get("results", [])
                    result_count = len(web_results)

                    print(f"✅ Brave: SUCCESS - Got {result_count} results")
                    return {
                        "name": "Brave Search",
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "result_count": result_count,
                        "features": ["Privacy-focused", "Web search", "News search", "Image search"],
                        "sample_response": web_results[:1]
                    }
                else:
                    print(f"❌ Brave: FAILED - Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return {
                        "name": "Brave Search",
                        "status": "❌ FAILED",
                        "endpoint": url,
                        "error": f"HTTP {response.status_code}: {response.text[:200]}"
                    }

        except Exception as e:
            print(f"❌ Brave: ERROR - {str(e)}")
            return {
                "name": "Brave Search",
                "status": "❌ ERROR",
                "endpoint": url,
                "error": str(e)
            }

    async def test_perplexity_api(self) -> Dict[str, Any]:
        """测试 Perplexity API"""
        print("\n🔍 Testing Perplexity API...")

        api_key = os.getenv("PERPLEXITY_API_KEY", "")
        url = "https://api.perplexity.ai/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "user",
                    "content": "What is Python async programming?"
                }
            ],
            "max_tokens": 100
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                    print(f"✅ Perplexity: SUCCESS - Got response")
                    return {
                        "name": "Perplexity",
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "features": ["AI-powered search", "Direct answers", "Citation support", "Multiple models"],
                        "sample_response": content[:200]
                    }
                else:
                    print(f"❌ Perplexity: FAILED - Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return {
                        "name": "Perplexity",
                        "status": "❌ FAILED",
                        "endpoint": url,
                        "error": f"HTTP {response.status_code}: {response.text[:200]}"
                    }

        except Exception as e:
            print(f"❌ Perplexity: ERROR - {str(e)}")
            return {
                "name": "Perplexity",
                "status": "❌ ERROR",
                "endpoint": url,
                "error": str(e)
            }

    async def test_jina_reader_api(self) -> Dict[str, Any]:
        """测试 Jina Reader API (免费, 无需API key)"""
        print("\n🔍 Testing Jina Reader API...")

        # Jina Reader不需要API key
        test_url = "https://r.jina.ai/https://docs.python.org/3/library/asyncio.html"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(test_url)

                if response.status_code == 200:
                    content = response.text
                    content_length = len(content)

                    print(f"✅ Jina Reader: SUCCESS - Got {content_length} chars")
                    return {
                        "name": "Jina Reader",
                        "status": "✅ WORKING",
                        "endpoint": "https://r.jina.ai/",
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "content_length": content_length,
                        "features": ["Free", "No API key", "Clean markdown output", "URL prefix service"],
                        "sample_response": content[:200]
                    }
                else:
                    print(f"❌ Jina Reader: FAILED - Status {response.status_code}")
                    return {
                        "name": "Jina Reader",
                        "status": "❌ FAILED",
                        "endpoint": "https://r.jina.ai/",
                        "error": f"HTTP {response.status_code}"
                    }

        except Exception as e:
            print(f"❌ Jina Reader: ERROR - {str(e)}")
            return {
                "name": "Jina Reader",
                "status": "❌ ERROR",
                "endpoint": "https://r.jina.ai/",
                "error": str(e)
            }

    async def test_jina_embedding_api(self) -> Dict[str, Any]:
        """测试 Jina Embedding API"""
        print("\n🔍 Testing Jina Embedding API...")

        api_key = os.getenv("JINA_API_KEY", "")
        url = "https://api.jina.ai/v1/embeddings"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "jina-embeddings-v3",
            "task": "text-matching",
            "dimensions": 1024,
            "late_chunking": False,
            "embedding_type": "float",
            "input": ["Python async programming tutorial"]
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    embeddings = data.get("data", [])

                    print(f"✅ Jina Embedding: SUCCESS - Got {len(embeddings)} embeddings")
                    return {
                        "name": "Jina Embedding",
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "embedding_count": len(embeddings),
                        "features": ["Semantic similarity", "MTEB #1", "Multiple dimensions", "Late chunking"],
                        "embedding_dimension": len(embeddings[0].get("embedding", [])) if embeddings else 0
                    }
                else:
                    print(f"❌ Jina Embedding: FAILED - Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return {
                        "name": "Jina Embedding",
                        "status": "❌ FAILED",
                        "endpoint": url,
                        "error": f"HTTP {response.status_code}: {response.text[:200]}"
                    }

        except Exception as e:
            print(f"❌ Jina Embedding: ERROR - {str(e)}")
            return {
                "name": "Jina Embedding",
                "status": "❌ ERROR",
                "endpoint": url,
                "error": str(e)
            }

    async def test_gemini_api(self) -> Dict[str, Any]:
        """测试 Gemini API (双key轮询)"""
        print("\n🔍 Testing Gemini API...")

        api_keys = [k for k in [os.getenv("YOUTUBE_API_KEY", "")] if k]

        base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

        payload = {
            "contents": [{
                "parts": [{
                    "text": "What is Python async programming in one sentence?"
                }]
            }]
        }

        # 测试两个key
        for idx, api_key in enumerate(api_keys, 1):
            url = f"{base_url}?key={api_key}"

            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, json=payload)

                    if response.status_code == 200:
                        data = response.json()
                        content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

                        print(f"✅ Gemini (Key {idx}): SUCCESS - Got response")
                        return {
                            "name": f"Gemini (Key {idx}/2)",
                            "status": "✅ WORKING",
                            "endpoint": base_url,
                            "response_time": response.elapsed.total_seconds() * 1000,
                            "features": ["Multimodal AI", "Dual-key rotation", "Flash model", "Long context"],
                            "sample_response": content[:200],
                            "working_keys": [idx]
                        }
                    else:
                        print(f"⚠️  Gemini (Key {idx}): FAILED - Status {response.status_code}, trying next key...")

            except Exception as e:
                print(f"⚠️  Gemini (Key {idx}): ERROR - {str(e)}, trying next key...")

        # 如果所有key都失败
        print(f"❌ Gemini: ALL KEYS FAILED")
        return {
            "name": "Gemini",
            "status": "❌ FAILED",
            "endpoint": base_url,
            "error": "All API keys failed"
        }

    async def test_you_api(self) -> Dict[str, Any]:
        """测试 You.com API"""
        print("\n🔍 Testing You.com API...")

        api_key = os.getenv("YOU_API_KEY", "")
        url = "https://api.ydc-index.io/search"

        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }

        params = {
            "query": "Python async programming"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    # You.com API response structure may vary
                    hits = data.get("hits", [])
                    result_count = len(hits)

                    print(f"✅ You.com: SUCCESS - Got {result_count} results")
                    return {
                        "name": "You.com",
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "response_time": response.elapsed.total_seconds() * 1000,
                        "result_count": result_count,
                        "features": ["Web Search", "News API", "RAG API", "Deep Search", "Image Search"],
                        "sample_response": hits[:1] if hits else data
                    }
                else:
                    print(f"❌ You.com: FAILED - Status {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return {
                        "name": "You.com",
                        "status": "❌ FAILED",
                        "endpoint": url,
                        "error": f"HTTP {response.status_code}: {response.text[:200]}"
                    }

        except Exception as e:
            print(f"❌ You.com: ERROR - {str(e)}")
            return {
                "name": "You.com",
                "status": "❌ ERROR",
                "endpoint": url,
                "error": str(e)
            }

    async def run_all_tests(self) -> Dict[str, Any]:
        """运行所有API测试"""
        print("\n" + "="*60)
        print("🚀 Starting API Validation for 15-WebSearchFlow")
        print("="*60)

        start_time = datetime.now()

        # 并行测试所有API
        tasks = [
            self.test_exa_api(),
            self.test_brave_api(),
            self.test_perplexity_api(),
            self.test_jina_reader_api(),
            self.test_jina_embedding_api(),
            self.test_gemini_api(),
            self.test_you_api()
        ]

        self.results = await asyncio.gather(*tasks)

        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        # 统计结果
        working_apis = [r for r in self.results if r["status"].startswith("✅")]
        failed_apis = [r for r in self.results if not r["status"].startswith("✅")]

        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)
        print(f"\n✅ Working APIs: {len(working_apis)}/{len(self.results)}")
        print(f"❌ Failed APIs: {len(failed_apis)}/{len(self.results)}")
        print(f"⏱️  Total validation time: {total_time:.2f}s")

        print("\n" + "-"*60)
        print("WORKING APIs:")
        print("-"*60)
        for api in working_apis:
            avg_time = api.get("response_time", 0)
            print(f"  {api['status']} {api['name']}")
            print(f"      Response time: {avg_time:.0f}ms")
            if "result_count" in api:
                print(f"      Results: {api['result_count']}")
            elif "content_length" in api:
                print(f"      Content: {api['content_length']} chars")
            elif "embedding_count" in api:
                print(f"      Embeddings: {api['embedding_count']}")

        if failed_apis:
            print("\n" + "-"*60)
            print("FAILED APIs:")
            print("-"*60)
            for api in failed_apis:
                print(f"  {api['status']} {api['name']}")
                print(f"      Error: {api.get('error', 'Unknown error')}")

        print("\n" + "="*60)

        # 返回汇总报告
        return {
            "timestamp": end_time.isoformat(),
            "total_time": total_time,
            "total_apis": len(self.results),
            "working_count": len(working_apis),
            "failed_count": len(failed_apis),
            "working_apis": [api["name"] for api in working_apis],
            "failed_apis": [api["name"] for api in failed_apis],
            "detailed_results": self.results
        }

    def save_report(self, report: Dict[str, Any], filepath: str = "api_validation_report.json"):
        """保存验证报告到JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Report saved to: {filepath}")


async def main():
    """主函数"""
    validator = APIValidator()
    report = await validator.run_all_tests()

    # 保存报告
    report_path = "D:/trae/claude-skills/skills/15-web-search-G/api_validation_report.json"
    validator.save_report(report, report_path)

    print("\n" + "="*60)
    print("✅ Validation Complete!")
    print("="*60)
    print(f"\n📋 Next Steps:")
    print(f"  1. Review the validation report: {report_path}")
    print(f"  2. Only implement APIs marked as ✅ WORKING")
    print(f"  3. Remove or fix APIs marked as ❌ FAILED")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
