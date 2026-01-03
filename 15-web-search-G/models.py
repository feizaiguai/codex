"""
Data Models for WebSearchFlow
数据模型定义
"""

from typing import List, Optional, Dict, Any, Literal
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchResult:
    """单条搜索结果"""

    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0

    # 可选字段
    publish_date: Optional[str] = None
    full_content: Optional[str] = None
    code_snippets: List[Dict[str, Any]] = field(default_factory=list)
    images: List[Dict[str, str]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)

    # 元数据
    engine: str = ""
    original_rank: int = 0
    language: Optional[str] = None
    authority_score: float = 0.0
    is_secure: bool = True
    response_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "relevance_score": self.relevance_score,
            "publish_date": self.publish_date,
            "full_content": self.full_content,
            "code_snippets": self.code_snippets,
            "images": self.images,
            "tables": self.tables,
            "metadata": {
                "engine": self.engine,
                "original_rank": self.original_rank,
                "language": self.language,
                "authority_score": self.authority_score,
                "is_secure": self.is_secure,
                "response_time": self.response_time
            }
        }


@dataclass
class WebSearchInput:
    """搜索输入参数"""

    # 核心参数
    query: str
    search_engines: Optional[List[str]] = None
    max_results: int = 10

    # 过滤器
    language: Optional[str] = None
    region: Optional[str] = None
    time_range: Literal["day", "week", "month", "year", "all"] = "all"
    site_filter: Optional[List[str]] = None
    exclude_sites: Optional[List[str]] = None

    # 结果控制
    include_snippets: bool = True
    fetch_full_content: bool = False

    # 高级选项
    search_type: Literal["general", "code", "documentation", "stackoverflow"] = "general"
    semantic_search: bool = False
    deduplication: bool = True
    mode: Literal["fast", "auto", "deep"] = "auto"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "query": self.query,
            "search_engines": self.search_engines,
            "max_results": self.max_results,
            "language": self.language,
            "region": self.region,
            "time_range": self.time_range,
            "site_filter": self.site_filter,
            "exclude_sites": self.exclude_sites,
            "include_snippets": self.include_snippets,
            "fetch_full_content": self.fetch_full_content,
            "search_type": self.search_type,
            "semantic_search": self.semantic_search,
            "deduplication": self.deduplication,
            "mode": self.mode
        }


@dataclass
class WebSearchOutput:
    """搜索输出结果"""

    # 元数据
    query: str
    total_results: int
    search_time: float
    engines_used: List[str]

    # 搜索结果
    results: List[SearchResult]

    # 聚合分析
    summary: Dict[str, Any] = field(default_factory=dict)

    # 质量指标
    quality: Dict[str, Any] = field(default_factory=dict)

    # 错误与警告
    warnings: List[Dict[str, str]] = field(default_factory=list)
    partial_failures: List[Dict[str, str]] = field(default_factory=list)

    # 查询优化记录
    query_optimization: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "query": self.query,
            "total_results": self.total_results,
            "search_time": self.search_time,
            "engines_used": self.engines_used,
            "results": [r.to_dict() for r in self.results],
            "summary": self.summary,
            "quality": self.quality,
            "warnings": self.warnings,
            "partial_failures": self.partial_failures,
            "query_optimization": self.query_optimization
        }

    @property
    def success(self) -> bool:
        """是否成功"""
        return len(self.results) > 0 and len(self.partial_failures) < len(self.engines_used)


@dataclass
class CodeSnippet:
    """代码片段"""

    language: str
    code: str
    context: Optional[str] = None
    position: int = 0
    highlighted_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "language": self.language,
            "code": self.code,
            "context": self.context,
            "position": self.position,
            "highlighted_code": self.highlighted_code
        }
