"""16-api-integrator 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List
import json
import time
import requests


class AuthType(str, Enum):
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer"
    BASIC = "basic"
    OAUTH2 = "oauth2"


class RateLimitStrategy(str, Enum):
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"


@dataclass
class RateLimitConfig:
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    max_requests: int = 60
    time_window: int = 60


@dataclass
class RetryConfig:
    max_retries: int = 2
    backoff_seconds: float = 0.5


@dataclass
class PaginationConfig:
    pagination_type: str = "page_number"
    page_param: str = "page"
    size_param: str = "per_page"
    total_key: str = "total"
    data_key: str = "items"


@dataclass
class AuthConfig:
    auth_type: AuthType = AuthType.NONE
    credentials: Dict[str, str] = field(default_factory=dict)
    header_name: str = "Authorization"
    api_key_param: str = "api_key"


@dataclass
class APIRequest:
    method: str
    url: str
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    json_body: Optional[Any] = None
    timeout: int = 15


@dataclass
class APIResponse:
    status_code: int
    body: Any
    elapsed_time: float
    retries: int = 0


class AuthenticationManager:
    def __init__(self, config: AuthConfig) -> None:
        self.config = config

    def get_auth_headers(self) -> Dict[str, str]:
        if self.config.auth_type == AuthType.BEARER_TOKEN:
            token = self.config.credentials.get("token", "")
            if token:
                return {self.config.header_name: f"Bearer {token}"}
        if self.config.auth_type == AuthType.OAUTH2:
            token = self.config.credentials.get("access_token", "")
            if token:
                return {self.config.header_name: f"Bearer {token}"}
        if self.config.auth_type == AuthType.BASIC:
            user = self.config.credentials.get("username", "")
            pwd = self.config.credentials.get("password", "")
            if user and pwd:
                import base64
                b64 = base64.b64encode(f"{user}:{pwd}".encode()).decode()
                return {self.config.header_name: f"Basic {b64}"}
        return {}

    def get_auth_params(self) -> Dict[str, str]:
        if self.config.auth_type == AuthType.API_KEY:
            key = self.config.credentials.get("api_key", "")
            if key:
                return {self.config.api_key_param: key}
        return {}


class OpenAPISpecParser:
    def parse(self, spec_path: str) -> List[Dict[str, str]]:
        spec = json.loads(open(spec_path, "r", encoding="utf-8").read())
        endpoints = []
        for path, methods in spec.get("paths", {}).items():
            for method in methods.keys():
                endpoints.append({"method": method.upper(), "path": path})
        return endpoints


class APIIntegrator:
    def __init__(self, base_url: str, auth_config: Optional[AuthConfig] = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_manager = AuthenticationManager(auth_config or AuthConfig())

    def request(self, req: APIRequest) -> APIResponse:
        headers = dict(req.headers)
        headers.update(self.auth_manager.get_auth_headers())
        params = dict(req.params)
        params.update(self.auth_manager.get_auth_params())

        start = time.time()
        resp = requests.request(
            method=req.method,
            url=f"{self.base_url}{req.url}",
            params=params,
            headers=headers,
            json=req.json_body,
            timeout=req.timeout,
        )
        elapsed = time.time() - start

        body: Any
        try:
            body = resp.json()
        except Exception:
            body = resp.text

        return APIResponse(status_code=resp.status_code, body=body, elapsed_time=elapsed, retries=0)


if __name__ == "__main__":
    print("16-api-integrator engine ready")
