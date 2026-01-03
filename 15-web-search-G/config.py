"""
WebSearchFlow configuration (API keys via environment variables).
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class APIConfig:
    """Single API config."""
    name: str
    endpoint: str
    auth_type: str  # "header", "bearer", "query", "none"
    auth_key: str
    enabled: bool = True
    timeout: int = 30


class WebSearchConfig:
    """WebSearchFlow config."""

    @staticmethod
    def _env(key: str) -> str:
        return os.getenv(key, "")

    EXA_CONFIG = APIConfig(
        name="Exa.ai",
        endpoint="https://api.exa.ai/search",
        auth_type="header",
        auth_key=_env.__func__("EXA_API_KEY"),
        enabled=bool(_env.__func__("EXA_API_KEY")),
        timeout=30,
    )

    BRAVE_CONFIG = APIConfig(
        name="Brave Search",
        endpoint="https://api.search.brave.com/res/v1/web/search",
        auth_type="header",
        auth_key=_env.__func__("BRAVE_API_KEY"),
        enabled=bool(_env.__func__("BRAVE_API_KEY")),
        timeout=30,
    )

    PERPLEXITY_CONFIG = APIConfig(
        name="Perplexity",
        endpoint="https://api.perplexity.ai/chat/completions",
        auth_type="bearer",
        auth_key=_env.__func__("PERPLEXITY_API_KEY"),
        enabled=bool(_env.__func__("PERPLEXITY_API_KEY")),
        timeout=30,
    )

    JINA_READER_CONFIG = APIConfig(
        name="Jina Reader",
        endpoint="https://r.jina.ai/",
        auth_type="bearer",
        auth_key=_env.__func__("JINA_API_KEY"),
        enabled=bool(_env.__func__("JINA_API_KEY")),
        timeout=30,
    )

    JINA_EMBEDDING_CONFIG = APIConfig(
        name="Jina Embedding",
        endpoint="https://api.jina.ai/v1/embeddings",
        auth_type="bearer",
        auth_key=_env.__func__("JINA_API_KEY"),
        enabled=bool(_env.__func__("JINA_API_KEY")),
        timeout=30,
    )

    YOU_CONFIG = APIConfig(
        name="You.com",
        endpoint="https://ydc-index.io/v1/search",
        auth_type="header",
        auth_key=_env.__func__("YOU_API_KEY"),
        enabled=bool(_env.__func__("YOU_API_KEY")),
        timeout=30,
    )

    SEARCH_MODES = {
        "fast": {
            "engines": ["brave", "you"],
            "max_results": 10,
            "fetch_full_content": False,
            "enable_dedup": True,
            "timeout": 10,
        },
        "auto": {
            "engines": ["exa_auto", "brave"],
            "max_results": 15,
            "fetch_full_content": False,
            "enable_dedup": True,
            "timeout": 15,
        },
        "deep": {
            "engines": ["exa_deep", "perplexity", "you"],
            "max_results": 25,
            "fetch_full_content": True,
            "enable_dedup": True,
            "timeout": 30,
        },
        "code": {
            "engines": ["exa_deep", "brave"],
            "max_results": 20,
            "fetch_full_content": True,
            "enable_dedup": True,
            "timeout": 20,
            "site_filter": ["stackoverflow.com", "github.com", "dev.to"],
        },
    }

    DEDUP_CONFIG = {
        "similarity_threshold": 0.85,
        "url_normalization": True,
        "content_dedup": True,
        "use_embedding": True,
    }

    QUALITY_CONFIG = {
        "min_relevance_score": 50,
        "min_authority_score": 30,
        "filter_low_quality": True,
        "prefer_https": True,
    }

    CACHE_CONFIG = {
        "enabled": True,
        "ttl": 3600,
        "max_size": 500,
    }

    DEFAULT_LANGUAGE = "auto"
    DEFAULT_REGION = None
    MAX_CONCURRENT_REQUESTS = 6
    RETRY_ATTEMPTS = 2
    RETRY_DELAY = 1.0

    @classmethod
    def get_api_configs(cls) -> Dict[str, APIConfig]:
        return {
            "exa": cls.EXA_CONFIG,
            "brave": cls.BRAVE_CONFIG,
            "perplexity": cls.PERPLEXITY_CONFIG,
            "jina_reader": cls.JINA_READER_CONFIG,
            "jina_embedding": cls.JINA_EMBEDDING_CONFIG,
            "you": cls.YOU_CONFIG,
        }

    @classmethod
    def get_enabled_apis(cls) -> Dict[str, APIConfig]:
        return {
            name: config
            for name, config in cls.get_api_configs().items()
            if config.enabled
        }
