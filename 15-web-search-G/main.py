"""
WebSearchFlow - Main Implementation
主模块：智能网络搜索引擎
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from collections import defaultdict
import re
from urllib.parse import urlparse

from .models import WebSearchInput, WebSearchOutput, SearchResult
from .config import WebSearchConfig
from .api_clients import (
    APIClientFactory,
    ExaClient,
    BraveClient,
    PerplexityClient,
    JinaReaderClient,
    JinaEmbeddingClient,
    YouClient
)


class WebSearchFlow:
    """
    智能网络搜索引擎
    集成6个搜索API，提供智能路由、语义去重、内容增强
    """

    def __init__(self):
        self.config = WebSearchConfig()
        self.cache = {}  # 简单内存缓存

    async def execute(self, input_params: WebSearchInput) -> WebSearchOutput:
        """
        执行搜索

        Args:
            input_params: 搜索输入参数

        Returns:
            WebSearchOutput: 搜索结果
        """
        start_time = time.time()

        # 1. 查询优化
        optimized_query, optimization_record = self._optimize_query(input_params)

        # 2. 智能路由 - 选择搜索引擎
        engines = self._route_engines(input_params)

        # 3. 并行执行搜索
        all_results, partial_failures = await self._parallel_search(
            optimized_query,
            engines,
            input_params
        )

        # 4. 结果去重
        if input_params.deduplication:
            all_results = await self._deduplicate_results(all_results)

        # 5. 相关性排序
        all_results = self._rank_results(all_results, optimized_query)

        # 6. 内容增强（如果需要）
        if input_params.fetch_full_content:
            all_results = await self._enhance_with_full_content(
                all_results[:input_params.max_results]
            )

        # 7. 限制结果数量
        all_results = all_results[:input_params.max_results]

        # 8. 生成聚合分析
        summary = self._generate_summary(all_results)

        # 9. 计算质量指标
        quality = self._calculate_quality_metrics(all_results, optimized_query)

        # 10. 构建输出
        search_time = (time.time() - start_time) * 1000  # ms

        output = WebSearchOutput(
            query=optimized_query,
            total_results=len(all_results),
            search_time=search_time,
            engines_used=engines,
            results=all_results,
            summary=summary,
            quality=quality,
            partial_failures=partial_failures,
            query_optimization=optimization_record
        )

        return output

    def _optimize_query(self, params: WebSearchInput) -> tuple:
        """
        优化搜索查询

        Returns:
            (optimized_query, optimization_record)
        """
        original = params.query
        optimized = original

        added_terms = []
        removed_terms = []

        # 检测查询语言
        is_chinese = bool(re.search(r'[\u4e00-\u9fff]', original))

        # 根据搜索类型添加关键词
        if params.search_type == "code":
            if "代码" not in original and "code" not in original.lower():
                optimized += " code example"
                added_terms.append("code example")

        elif params.search_type == "documentation":
            if "文档" not in original and "documentation" not in original.lower():
                optimized += " documentation"
                added_terms.append("documentation")

        # 移除多余空格
        optimized = " ".join(optimized.split())

        record = {
            "original": original,
            "optimized": optimized,
            "added_terms": added_terms,
            "removed_terms": removed_terms,
            "detected_language": "zh-CN" if is_chinese else "en"
        }

        return optimized, record

    def _route_engines(self, params: WebSearchInput) -> List[str]:
        """
        智能路由 - 根据查询类型和模式选择搜索引擎

        Returns:
            引擎列表 ["exa_auto", "brave", "you"]
        """
        # 如果用户指定了引擎，直接使用
        if params.search_engines:
            return params.search_engines

        # 使用预设模式
        mode_config = self.config.SEARCH_MODES.get(params.mode, {})
        engines = mode_config.get("engines", [])

        # 根据搜索类型调整
        if params.search_type == "code":
            engines = ["exa_deep", "brave"]
        elif params.search_type == "documentation":
            engines = ["brave", "you"]
        elif params.search_type == "stackoverflow":
            engines = ["brave"]  # Brave索引Stack Overflow

        # 如果没有指定，使用默认
        if not engines:
            engines = ["exa_auto", "brave"]

        return engines

    async def _parallel_search(
        self,
        query: str,
        engines: List[str],
        params: WebSearchInput
    ) -> tuple:
        """
        并行执行多个搜索引擎

        Returns:
            (all_results, partial_failures)
        """
        all_results = []
        partial_failures = []

        # 创建搜索任务
        tasks = []
        for engine in engines:
            task = self._search_single_engine(engine, query, params)
            tasks.append(task)

        # 并行执行
        results_list = await asyncio.gather(*tasks, return_exceptions=True)

        # 收集结果
        for engine, result in zip(engines, results_list):
            if isinstance(result, Exception):
                partial_failures.append({
                    "engine": engine,
                    "error": str(result)
                })
            elif isinstance(result, list):
                all_results.extend(result)
            else:
                partial_failures.append({
                    "engine": engine,
                    "error": "Unknown error"
                })

        return all_results, partial_failures

    async def _search_single_engine(
        self,
        engine: str,
        query: str,
        params: WebSearchInput
    ) -> List[SearchResult]:
        """执行单个搜索引擎"""

        try:
            if engine.startswith("exa"):
                # Exa有多种模式
                mode = "auto"
                if engine == "exa_fast":
                    mode = "fast"
                elif engine == "exa_deep":
                    mode = "deep"

                async with ExaClient(self.config.EXA_CONFIG) as client:
                    return await client.search(query, params.max_results, mode)

            elif engine == "brave":
                async with BraveClient(self.config.BRAVE_CONFIG) as client:
                    return await client.search(query, params.max_results, params.language)

            elif engine == "perplexity":
                async with PerplexityClient(self.config.PERPLEXITY_CONFIG) as client:
                    return await client.search(query, max_tokens=500)

            elif engine == "you":
                async with YouClient(self.config.YOU_CONFIG) as client:
                    return await client.search(query, params.max_results)

            else:
                print(f"Unknown engine: {engine}")
                return []

        except Exception as e:
            print(f"Error searching {engine}: {str(e)}")
            raise

    async def _deduplicate_results(
        self,
        results: List[SearchResult]
    ) -> List[SearchResult]:
        """
        去重搜索结果
        1. URL去重
        2. 语义相似度去重
        """
        if not results:
            return []

        # 1. URL去重
        seen_urls = set()
        url_deduped = []

        for result in results:
            normalized_url = self._normalize_url(result.url)
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                url_deduped.append(result)

        # 2. 语义去重（使用Jina Embedding）
        if len(url_deduped) > 1:
            semantic_deduped = await self._semantic_dedup(url_deduped)
            return semantic_deduped

        return url_deduped

    @staticmethod
    def _normalize_url(url: str) -> str:
        """标准化URL用于去重"""
        # 移除协议
        url = re.sub(r'^https?://', '', url)
        # 移除www
        url = re.sub(r'^www\.', '', url)
        # 移除尾随斜杠
        url = url.rstrip('/')
        # 移除查询参数
        url = url.split('?')[0]
        # 转小写
        return url.lower()

    async def _semantic_dedup(
        self,
        results: List[SearchResult],
        threshold: float = 0.85
    ) -> List[SearchResult]:
        """
        使用语义嵌入去重
        """
        if len(results) <= 1:
            return results

        # 提取文本用于embedding
        texts = [f"{r.title} {r.snippet}" for r in results]

        try:
            async with JinaEmbeddingClient(self.config.JINA_EMBEDDING_CONFIG) as client:
                embeddings = await client.embed(texts, dimensions=512)  # 使用较小维度加快速度

            if not embeddings or len(embeddings) != len(results):
                return results

            # 计算相似度矩阵并去重
            unique_results = []
            used_indices = set()

            for i, result in enumerate(results):
                if i in used_indices:
                    continue

                unique_results.append(result)
                used_indices.add(i)

                # 标记相似的结果
                for j in range(i + 1, len(results)):
                    if j not in used_indices:
                        similarity = self._cosine_similarity(
                            embeddings[i],
                            embeddings[j]
                        )
                        if similarity > threshold:
                            used_indices.add(j)

            return unique_results

        except Exception as e:
            print(f"Semantic dedup failed: {str(e)}")
            return results

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

    def _rank_results(
        self,
        results: List[SearchResult],
        query: str
    ) -> List[SearchResult]:
        """
        对结果进行相关性排序
        综合考虑：原始排名、引擎权重、URL权威性
        """
        # 引擎权重
        engine_weights = {
            "exa": 1.0,
            "perplexity": 0.95,
            "brave": 0.9,
            "you": 0.85
        }

        # 计算综合分数
        for result in results:
            engine_weight = engine_weights.get(result.engine, 0.8)

            # 基础分数（原始相关性分数）
            base_score = result.relevance_score

            # 排名惩罚（排名越靠后分数越低）
            rank_penalty = max(0, 100 - result.original_rank * 5)

            # 权威性加成
            authority_bonus = result.authority_score * 0.2

            # HTTPS加成
            https_bonus = 5 if result.is_secure else 0

            # 综合分数
            final_score = (
                base_score * engine_weight +
                rank_penalty +
                authority_bonus +
                https_bonus
            )

            result.relevance_score = min(100, final_score)

        # 按分数降序排序
        results.sort(key=lambda x: x.relevance_score, reverse=True)

        return results

    async def _enhance_with_full_content(
        self,
        results: List[SearchResult]
    ) -> List[SearchResult]:
        """使用Jina Reader提取完整内容"""

        try:
            async with JinaReaderClient(self.config.JINA_READER_CONFIG) as client:
                enhanced = await client.enhance_results(results, max_concurrent=3)
                return enhanced
        except Exception as e:
            print(f"Content enhancement failed: {str(e)}")
            return results

    def _generate_summary(self, results: List[SearchResult]) -> Dict[str, Any]:
        """生成搜索结果摘要分析"""

        if not results:
            return {
                "top_domains": [],
                "common_themes": [],
                "recommended_links": []
            }

        # 1. 统计高频域名
        domain_counts = defaultdict(int)
        for result in results:
            domain_counts[result.source] += 1

        top_domains = [
            {
                "domain": domain,
                "count": count,
                "percentage": round(count / len(results) * 100, 1)
            }
            for domain, count in sorted(
                domain_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]

        # 2. 提取共同主题（简化版）
        common_themes = self._extract_common_themes(results)

        # 3. AI推荐链接（Top 3）
        recommended_links = [
            {
                "url": r.url,
                "title": r.title,
                "reason": self._generate_recommendation_reason(r),
                "score": r.relevance_score
            }
            for r in results[:3]
        ]

        return {
            "top_domains": top_domains,
            "common_themes": common_themes,
            "recommended_links": recommended_links
        }

    @staticmethod
    def _extract_common_themes(results: List[SearchResult]) -> List[str]:
        """提取共同主题（简化版 - 提取高频词）"""
        # 合并所有标题和摘要
        all_text = " ".join([f"{r.title} {r.snippet}" for r in results])

        # 移除常见词
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}

        # 提取词频
        words = re.findall(r'\b\w{4,}\b', all_text.lower())
        word_freq = defaultdict(int)

        for word in words:
            if word not in stop_words:
                word_freq[word] += 1

        # 返回Top 8高频词
        common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
        return [word for word, count in common if count > 1]

    @staticmethod
    def _generate_recommendation_reason(result: SearchResult) -> str:
        """生成推荐理由"""
        reasons = []

        if result.relevance_score >= 90:
            reasons.append("高相关性")

        if result.is_secure:
            reasons.append("HTTPS安全")

        if result.engine == "exa":
            reasons.append("语义搜索引擎验证")
        elif result.engine == "perplexity":
            reasons.append("AI增强答案")

        if result.authority_score >= 80:
            reasons.append("权威来源")

        return "、".join(reasons) if reasons else "综合评分最高"

    def _calculate_quality_metrics(
        self,
        results: List[SearchResult],
        query: str
    ) -> Dict[str, Any]:
        """计算质量指标"""

        if not results:
            return {
                "relevance_score": 0,
                "duplicates_removed": 0,
                "average_source_authority": 0,
                "freshnessScore": 0,
                "coverage_score": 0
            }

        # 平均相关性
        avg_relevance = sum(r.relevance_score for r in results) / len(results)

        # 平均权威性
        avg_authority = sum(r.authority_score for r in results) / len(results)

        # 覆盖度（不同来源数量）
        unique_sources = len(set(r.source for r in results))
        coverage = min(100, unique_sources * 20)

        # 新鲜度（有发布日期的占比）
        dated_results = [r for r in results if r.publish_date]
        freshness = len(dated_results) / len(results) * 100 if results else 0

        return {
            "relevance_score": round(avg_relevance, 1),
            "duplicates_removed": 0,  # 实际去重数会在去重阶段记录
            "average_source_authority": round(avg_authority, 1),
            "freshness_score": round(freshness, 1),
            "coverage_score": round(coverage, 1)
        }


# 便捷函数
async def search(
    query: str,
    mode: str = "auto",
    max_results: int = 10,
    fetch_full_content: bool = False
) -> WebSearchOutput:
    """
    快速搜索函数

    Example:
        >>> result = await search("Python async programming", mode="deep")
        >>> print(f"Found {len(result.results)} results")
    """
    params = WebSearchInput(
        query=query,
        mode=mode,
        max_results=max_results,
        fetch_full_content=fetch_full_content
    )

    flow = WebSearchFlow()
    return await flow.execute(params)
