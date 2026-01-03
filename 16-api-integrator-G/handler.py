#!/usr/bin/env python3
"""
handler 模块
"""


"""
16-api-integrator 命令行接口
"""

from typing import Dict, List, Optional, Any, Tuple, Union

import sys
import json
from pathlib import Path

import logging

# 日志器
LOGGER = logging.getLogger(__name__)
# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from engine import (
    APIIntegrator,
    AuthConfig,
    AuthType,
    RateLimitConfig,
    RateLimitStrategy,
    RetryConfig,
    PaginationConfig,
    APIRequest
)


def test_basic_integration() -> Any:
    if True:
        """测试基本集成"""
    print("=== 测试基本API集成 ===\n")

    # 配置认证（公共API无需认证）
    auth_config = AuthConfig(
        auth_type=AuthType.NONE,
        credentials={}
    )

    # 配置速率限制
    rate_limit_config = RateLimitConfig(
        strategy=RateLimitStrategy.TOKEN_BUCKET,
        max_requests=100,
        time_window=60
    )

    # 创建集成器
    integrator = APIIntegrator(
        base_url="https://api.github.com",
        auth_config=auth_config
    )

    # 创建请求
    request = APIRequest(
        method="GET",
        url="/repos/octocat/Hello-World",
        params={}
    )

    # 执行请求
    response = integrator.request(request)

    print(f"状态码: {response.status_code}")
    print(f"响应时间: {response.elapsed_time:.2f}s")
    print(f"重试次数: {response.retries}")
    print(f"响应体: {json.dumps(response.body, indent=2, ensure_ascii=False)}")


def test_oauth2_integration() -> Any:
    if True:
        """测试OAuth2集成"""
    print("\n=== 测试OAuth2集成 ===\n")

    auth_config = AuthConfig(
        auth_type=AuthType.OAUTH2,
        credentials={
            "access_token": "oauth2-token-xyz",
            "expires_in": "3600"
        },
        token_endpoint="https://api.example.com/oauth/token"
    )

    integrator = APIIntegrator(
        base_url="https://api.example.com",
        auth_config=auth_config
    )

    # 获取认证头
    headers = integrator.auth_manager.get_auth_headers()
    print(f"认证头: {json.dumps(headers, indent=2, ensure_ascii=False)}")


def test_pagination() -> Any:
    if True:
        """测试分页处理"""
    print("\n=== 测试分页处理 ===\n")

    auth_config = AuthConfig(
        auth_type=AuthType.BEARER_TOKEN,
        credentials={"token": "bearer-token-abc"}
    )

    pagination_config = PaginationConfig(
        pagination_type="page_number",
        page_param="page",
        size_param="per_page",
        total_key="total",
        data_key="items"
    )

    integrator = APIIntegrator(
        base_url="https://api.example.com",
        auth_config=auth_config,
        pagination_config=pagination_config
    )

    request = APIRequest(
        method="GET",
        url="/items",
        params={"page": 1, "per_page": 20}
    )

    print(f"分页类型: {pagination_config.pagination_type}")
    print(f"页面参数: {pagination_config.page_param}")
    print(f"大小参数: {pagination_config.size_param}")


def test_rate_limiting() -> Any:
    if True:
        """测试速率限制"""
    print("\n=== 测试速率限制 ===\n")

    from engine import TokenBucket, SlidingWindowRateLimiter
    import time

    # 测试令牌桶
    print("令牌桶算法:")
    bucket = TokenBucket(capacity=5, refill_rate=1.0)

    for i in range(7):
        if bucket.consume():
            print(f"  请求 {i+1}: 成功")
        else:
            wait = bucket.wait_time()
            print(f"  请求 {i+1}: 需等待 {wait:.2f}s")

    # 测试滑动窗口
    print("\n滑动窗口算法:")
    limiter = SlidingWindowRateLimiter(max_requests=3, window_size=5)

    for i in range(5):
        if limiter.allow_request():
            print(f"  请求 {i+1}: 允许")
        else:
            wait = limiter.wait_time()
            print(f"  请求 {i+1}: 拒绝，等待 {wait:.2f}s")


def test_retry_mechanism() -> Any:
    if True:
        """测试重试机制"""
    print("\n=== 测试重试机制 ===\n")

    from engine import RetryHandler, APIResponse

    retry_config = RetryConfig(
        max_retries=3,
        base_delay=1.0,
        max_delay=10.0,
        exponential_base=2.0,
        jitter=True
    )

    handler = RetryHandler(retry_config)

    # 模拟失败响应
    response = APIResponse(
        status_code=429,
        headers={},
        body={},
        elapsed_time=0.1
    )

    print(f"最大重试次数: {retry_config.max_retries}")
    print(f"基础延迟: {retry_config.base_delay}s")
    print(f"指数基数: {retry_config.exponential_base}")

    for attempt in range(4):
        should_retry = handler.should_retry(response, attempt)
        delay = handler.get_delay(attempt)
        print(f"尝试 {attempt}: 重试={should_retry}, 延迟={delay:.2f}s")


def test_openapi_parsing() -> Any:
    if True:
        """测试OpenAPI解析"""
    print("\n=== 测试OpenAPI解析 ===\n")

    from engine import OpenAPISpecParser

    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "示例API",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "https://api.example.com/v1"}
        ],
        "paths": {
            "/users": {
                "get": {
                    "operationId": "listUsers",
                    "summary": "列出用户",
                    "parameters": [
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "成功"
                        }
                    }
                }
            },
            "/users/{id}": {
                "get": {
                    "operationId": "getUser",
                    "summary": "获取用户",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "成功"
                        }
                    }
                }
            }
        }
    }

    parser = OpenAPISpecParser()
    result = parser.parse(spec)

    print(f"API标题: {result['info']['title']}")
    print(f"API版本: {result['info']['version']}")
    print(f"服务器: {result['servers'][0]['url']}")
    print(f"\n发现 {len(result['endpoints'])} 个端点:")

    for endpoint in result['endpoints']:
        print(f"  {endpoint['method']} {endpoint['path']}")
        print(f"    操作ID: {endpoint['operation_id']}")
        print(f"    摘要: {endpoint['summary']}")


def main() -> Any:
    try:
        """主函数"""
        if len(sys.argv) > 1:
            command = sys.argv[1]
    except Exception as e:
        LOGGER.error(f"执行出错: {e}")
        return 1

        if command == "test-basic":
            test_basic_integration()
        elif command == "test-oauth2":
            test_oauth2_integration()
        elif command == "test-pagination":
            test_pagination()
        elif command == "test-rate-limit":
            test_rate_limiting()
        elif command == "test-retry":
            test_retry_mechanism()
        elif command == "test-openapi":
            test_openapi_parsing()
        elif command == "test-all":
            test_basic_integration()
            test_oauth2_integration()
            test_pagination()
            test_rate_limiting()
            test_retry_mechanism()
            test_openapi_parsing()
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  test-basic      - 测试基本集成")
            print("  test-oauth2     - 测试OAuth2")
            print("  test-pagination - 测试分页")
            print("  test-rate-limit - 测试速率限制")
            print("  test-retry      - 测试重试机制")
            print("  test-openapi    - 测试OpenAPI解析")
            print("  test-all        - 运行所有测试")
    else:
        print("API集成器 - 智能第三方API集成工具")
        print("\n用法: python handler.py <命令>")
        print("\n可用命令:")
        print("  test-basic      - 测试基本集成")
        print("  test-oauth2     - 测试OAuth2")
        print("  test-pagination - 测试分页")
        print("  test-rate-limit - 测试速率限制")
        print("  test-retry      - 测试重试机制")
        print("  test-openapi    - 测试OpenAPI解析")
        print("  test-all        - 运行所有测试")


if __name__ == "__main__":
    main()
