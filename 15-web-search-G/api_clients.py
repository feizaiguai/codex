"""
API Clients for 6 Search Engines
所有搜索引擎的API客户端实现
"""

import asyncio
import httpx
from typing import List, Dict, Any, Optional
from urllib.parse import quote
import re

from .models import SearchResult
from .config import WebSearchConfig


class BaseAPIClient:
    """API客户端基类"""

    def __init__(self, config):
        self.config = config
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=self.config.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Content-Type": "application/json"}

        if self.config.auth_type == "header":
            if self.config.name == "Exa.ai":
                headers["x-api-key"] = self.config.auth_key
            elif self.config.name == "Brave Search":
                headers["X-Subscription-Token"] = self.config.auth_key
            elif self.config.name == "You.com":
                headers["X-API-Key"] = self.config.auth_key

        elif self.config.auth_type == "bearer":
            headers["Authorization"] = f"Bearer {self.config.auth_key}"

        return headers


class ExaClient(BaseAPIClient):
    """Exa.ai API客户端"""

    async def search(
        self,
        query: str,
        num_results: int = 10,
        mode: str = "auto"
    ) -> List[SearchResult]:
        """执行Exa搜索"""

        headers = self._get_headers()
        payload = {
            "query": query,
            "numResults": num_results,
            "type": mode  # "fast", "auto", "deep"
        }

        try:
            response = await self.client.post(
                self.config.endpoint,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                for idx, item in enumerate(data.get("results", [])[:num_results]):
                    result = SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        snippet=item.get("text", "")[:500],
                        source=self._extract_domain(item.get("url", "")),
                        relevance_score=item.get("score", 0.0) * 100,
                        publish_date=item.get("publishedDate"),
                        engine="exa",
                        original_rank=idx + 1,
                        is_secure=item.get("url", "").startswith("https"),
                        response_time=response.elapsed.total_seconds() * 1000
                    )
                    results.append(result)

                return results
            else:
                print(f"Exa API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Exa search failed: {str(e)}")
            return []

    @staticmethod
    def _extract_domain(url: str) -> str:
        """提取域名"""
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else ""


class BraveClient(BaseAPIClient):
    """Brave Search API客户端"""

    async def search(
        self,
        query: str,
        count: int = 10,
        language: Optional[str] = None
    ) -> List[SearchResult]:
        """执行Brave搜索"""

        headers = self._get_headers()
        headers["Accept"] = "application/json"

        params = {
            "q": query,
            "count": count
        }

        if language:
            params["search_lang"] = language

        try:
            response = await self.client.get(
                self.config.endpoint,
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                web_results = data.get("web", {}).get("results", [])
                for idx, item in enumerate(web_results[:count]):
                    result = SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        snippet=item.get("description", "")[:500],
                        source=item.get("profile", {}).get("long_name", ""),
                        relevance_score=90 - (idx * 3),  # 估算相关性
                        language=item.get("language"),
                        engine="brave",
                        original_rank=idx + 1,
                        is_secure=item.get("url", "").startswith("https"),
                        response_time=response.elapsed.total_seconds() * 1000
                    )
                    results.append(result)

                return results
            else:
                print(f"Brave API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Brave search failed: {str(e)}")
            return []


class PerplexityClient(BaseAPIClient):
    """Perplexity API客户端"""

    async def search(
        self,
        query: str,
        max_tokens: int = 500
    ) -> List[SearchResult]:
        """执行Perplexity AI搜索"""

        headers = self._get_headers()
        payload = {
            "model": "sonar",  # 使用简短模型名
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": max_tokens
        }

        try:
            response = await self.client.post(
                self.config.endpoint,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                # Perplexity返回直接答案，包装成SearchResult
                result = SearchResult(
                    title=f"AI Answer: {query[:50]}...",
                    url="https://www.perplexity.ai",
                    snippet=content[:500],
                    source="perplexity.ai",
                    full_content=content,
                    relevance_score=95.0,  # AI答案通常高相关性
                    engine="perplexity",
                    original_rank=1,
                    is_secure=True,
                    response_time=response.elapsed.total_seconds() * 1000
                )

                return [result]
            else:
                print(f"Perplexity API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Perplexity search failed: {str(e)}")
            return []


class JinaReaderClient(BaseAPIClient):
    """Jina Reader API客户端"""

    async def fetch_content(self, url: str) -> Optional[str]:
        """提取网页内容为Markdown"""

        # Jina Reader使用URL前缀方式
        reader_url = f"{self.config.endpoint}{url}"

        try:
            # 使用认证headers（如果配置了）
            headers = self._get_headers()
            response = await self.client.get(reader_url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                error_msg = f"Jina Reader error for {url}: HTTP {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text[:200]}"
                print(error_msg)
                return None

        except httpx.TimeoutException as e:
            print(f"Jina Reader timeout for {url}: {str(e)}")
            return None
        except httpx.HTTPError as e:
            print(f"Jina Reader HTTP error for {url}: {type(e).__name__} - {str(e)}")
            return None
        except Exception as e:
            print(f"Jina Reader failed for {url}: {type(e).__name__} - {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()[:500]}")
            return None

    async def enhance_results(
        self,
        results: List[SearchResult],
        max_concurrent: int = 3
    ) -> List[SearchResult]:
        """批量增强搜索结果的完整内容"""

        async def fetch_one(result: SearchResult) -> SearchResult:
            content = await self.fetch_content(result.url)
            if content:
                result.full_content = content
                # 提取代码片段
                result.code_snippets = self._extract_code_blocks(content)
            return result

        # 限制并发数
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_limit(result):
            async with semaphore:
                return await fetch_one(result)

        # 并行处理
        tasks = [fetch_with_limit(r) for r in results]
        enhanced = await asyncio.gather(*tasks)

        return enhanced

    @staticmethod
    def _extract_code_blocks(content: str) -> List[Dict[str, Any]]:
        """从Markdown中提取代码块"""
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            language = match.group(1) or "text"
            code = match.group(2)
            code_blocks.append({
                "language": language,
                "code": code,
                "position": idx + 1
            })

        return code_blocks


class JinaEmbeddingClient(BaseAPIClient):
    """Jina Embedding API客户端"""

    async def embed(
        self,
        texts: List[str],
        dimensions: int = 1024
    ) -> List[List[float]]:
        """生成文本嵌入向量"""

        headers = self._get_headers()
        payload = {
            "model": "jina-embeddings-v3",
            "task": "text-matching",
            "dimensions": dimensions,
            "late_chunking": False,
            "embedding_type": "float",
            "input": texts
        }

        try:
            response = await self.client.post(
                self.config.endpoint,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                embeddings = [item["embedding"] for item in data.get("data", [])]
                return embeddings
            else:
                print(f"Jina Embedding error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Jina Embedding failed: {str(e)}")
            return []

    async def compute_similarity(
        self,
        text1: str,
        text2: str
    ) -> float:
        """计算两个文本的相似度"""

        embeddings = await self.embed([text1, text2])

        if len(embeddings) == 2:
            return self._cosine_similarity(embeddings[0], embeddings[1])
        return 0.0

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        import math

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


class YouClient(BaseAPIClient):
    """You.com API客户端"""

    async def search(
        self,
        query: str,
        count: int = 10
    ) -> List[SearchResult]:
        """执行You.com搜索"""

        headers = self._get_headers()
        params = {
            "query": query,
            "count": count
        }

        try:
            response = await self.client.get(
                self.config.endpoint,
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                # You.com API响应结构
                hits = data.get("hits", [])
                for idx, item in enumerate(hits[:count]):
                    result = SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        snippet=item.get("snippet", "")[:500],
                        source=item.get("domain", ""),
                        relevance_score=item.get("score", 0.0) * 100,
                        engine="you",
                        original_rank=idx + 1,
                        is_secure=item.get("url", "").startswith("https"),
                        response_time=response.elapsed.total_seconds() * 1000
                    )
                    results.append(result)

                return results
            else:
                print(f"You.com API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"You.com search failed: {str(e)}")
            return []


class APIClientFactory:
    """API客户端工厂"""

    @staticmethod
    def create_client(engine_name: str):
        """创建API客户端"""

        configs = WebSearchConfig.get_enabled_apis()

        if engine_name.startswith("exa"):
            return ExaClient(configs["exa"])
        elif engine_name == "brave":
            return BraveClient(configs["brave"])
        elif engine_name == "perplexity":
            return PerplexityClient(configs["perplexity"])
        elif engine_name == "jina_reader":
            return JinaReaderClient(configs["jina_reader"])
        elif engine_name == "jina_embedding":
            return JinaEmbeddingClient(configs["jina_embedding"])
        elif engine_name == "you":
            return YouClient(configs["you"])
        else:
            raise ValueError(f"Unknown engine: {engine_name}")
