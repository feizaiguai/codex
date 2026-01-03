#!/usr/bin/env python3
"""
15-web-search-G - 绠€鍖栫洿鎺ヨ皟鐢ㄨ剼鏈?
鏃犻渶澶嶆潅瀵煎叆,鐩存帴鎵ц
"""

import os
import asyncio
import aiohttp
import time
import argparse
import json
from typing import List, Dict, Any
from dataclasses import dataclass, field
from urllib.parse import quote_plus


# ============ 鏁版嵁妯″瀷 ============

@dataclass
class SearchResult:
    """鎼滅储缁撴灉"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0
    engine: str = ""


# ============ API閰嶇疆 ============

API_CONFIGS = {
    "brave": {
        "endpoint": "https://api.search.brave.com/res/v1/web/search",
        "key": os.getenv("BRAVE_API_KEY", ""),
        "header": "X-Subscription-Token"
    },
    "you": {
        "endpoint": "https://ydc-index.io/v1/search",
        "key": os.getenv("YOU_API_KEY", ""),
        "header": "X-API-Key"
    },
}

async def _brave_available() -> bool:
    config = API_CONFIGS["brave"]
    if not config.get("key"):
        return False
    url = f"{config['endpoint']}?q=ping&count=1"
    headers = {config['header']: config['key']}
    timeout = aiohttp.ClientTimeout(total=3, connect=2)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=timeout) as resp:
                return resp.status == 200
    except Exception:
        return False

# ============ 鎼滅储瀹㈡埛绔?============

async def search_brave(query: str, max_results: int = 10) -> List[SearchResult]:
    """Brave鎼滅储锛堝甫鍚屾闄嶇骇锛?""
    config = API_CONFIGS["brave"]
    if not config.get("key"):
        return []
    url = f"{config['endpoint']}?q={quote_plus(query)}&count={max_results}"
    headers = {config['header']: config['key']}

    # 鍏堝皾璇曞紓姝ヨ姹傦紙蹇€熻秴鏃讹級
    try:
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            ttl_dns_cache=300,
            force_close=False,
            enable_cleanup_closed=True
        )

        # 鍑忓皯瓒呮椂鏃堕棿锛岃澶辫触鏇村揩
        timeout = aiohttp.ClientTimeout(
            total=8,       # 鎬昏秴鏃?8 绉?
            connect=3,     # 杩炴帴瓒呮椂 3 绉?
            sock_read=5    # 璇诲彇瓒呮椂 5 绉?
        )

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers, timeout=timeout) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")

                data = await resp.json()
                results = []

                for item in data.get('web', {}).get('results', [])[:max_results]:
                    results.append(SearchResult(
                        title=item.get('title', ''),
                        url=item.get('url', ''),
                        snippet=item.get('description', ''),
                        source=item.get('url', '').split('/')[2] if '/' in item.get('url', '') else '',
                        relevance_score=85.0,
                        engine="Brave"
                    ))

                return results

    except (asyncio.TimeoutError, Exception) as e:
        # 寮傛澶辫触锛屽皾璇曞悓姝ヨ姹備綔涓洪檷绾ф柟妗?
        try:
            import requests
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code != 200:
                return []

            data = resp.json()
            results = []

            for item in data.get('web', {}).get('results', [])[:max_results]:
                results.append(SearchResult(
                    title=item.get('title', ''),
                    url=item.get('url', ''),
                    snippet=item.get('description', ''),
                    source=item.get('url', '').split('/')[2] if '/' in item.get('url', '') else '',
                    relevance_score=85.0,
                    engine="Brave"
                ))

            return results
        except Exception as sync_e:
            # 涓ょ鏂瑰紡閮藉け璐ヤ簡锛岄潤榛樺け璐?
            return []


async def search_you(query: str, max_results: int = 10) -> List[SearchResult]:
    """You.com鎼滅储"""
    config = API_CONFIGS["you"]
    url = f"{config['endpoint']}?query={quote_plus(query)}&count={max_results}"
    headers = {config['header']: config['key']}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []

                data = await resp.json()
                results = []

                # 鏂扮殑 API 鍝嶅簲缁撴瀯: results.web
                web_results = data.get('results', {}).get('web', [])[:max_results]
                for item in web_results:
                    results.append(SearchResult(
                        title=item.get('title', ''),
                        url=item.get('url', ''),
                        snippet=item.get('description', ''),
                        source=item.get('url', '').split('/')[2] if '/' in item.get('url', '') else '',
                        relevance_score=80.0,
                        engine="You.com"
                    ))

                return results
    except Exception as e:
        print(f"You.com鎼滅储閿欒: {e}")
        return []


# ============ 涓绘悳绱㈠嚱鏁?============

async def web_search(query: str, mode: str = "auto", max_results: int = 10) -> Dict[str, Any]:
    """
    缃戠粶鎼滅储涓诲嚱鏁?

    Args:
        query: 鎼滅储鏌ヨ
        mode: 鎼滅储妯″紡 (fast/auto/deep)
        max_results: 鏈€澶х粨鏋滄暟

    Returns:
        鎼滅储缁撴灉瀛楀吀
    """
    start_time = time.time()

    # 鏍规嵁妯″紡閫夋嫨鎼滅储寮曟搸
    brave_ok = await _brave_available()
    tasks = []
    task_engines = []

    if mode == "fast":
        if brave_ok:
            tasks.append(search_brave(query, max_results))
            task_engines.append("Brave")
        else:
            tasks.append(search_you(query, max_results))
            task_engines.append("You.com")
    else:  # auto / deep
        if brave_ok:
            tasks.append(search_brave(query, max_results))
            task_engines.append("Brave")
        tasks.append(search_you(query, max_results))
        task_engines.append("You.com")

    results_lists = await asyncio.gather(*tasks, return_exceptions=True)

    # 鍚堝苟缁撴灉
    all_results = []
    engines_used = []

    for engine_name, results in zip(task_engines, results_lists):
        if isinstance(results, list):
            all_results.extend(results)
            if results:
                engines_used.append(engine_name)

    # 鍘婚噸锛堝熀浜嶶RL锛?
    seen_urls = set()
    unique_results = []
    for result in all_results:
        if result.url not in seen_urls:
            seen_urls.add(result.url)
            unique_results.append(result)

    # 闄愬埗鏁伴噺
    unique_results = unique_results[:max_results]

    # 璁＄畻鑰楁椂
    search_time = (time.time() - start_time) * 1000  # ms

    return {
        "query": query,
        "total_results": len(unique_results),
        "search_time_ms": round(search_time, 2),
        "engines_used": engines_used,
        "results": unique_results
    }


# ============ 杈撳嚭鏍煎紡鍖?============

def format_markdown(data: Dict[str, Any]) -> str:
    """Markdown鏍煎紡杈撳嚭"""
    output = []
    output.append(f"# 馃攳 鎼滅储缁撴灉: {data['query']}\n")
    output.append(f"**鎬绘暟**: {data['total_results']} | **鑰楁椂**: {data['search_time_ms']/1000:.2f}s | **寮曟搸**: {', '.join(data['engines_used'])}\n")
    output.append("---\n")

    for i, r in enumerate(data['results'], 1):
        output.append(f"## {i}. {r.title} ({r.relevance_score:.0f}/100)")
        output.append(f"**URL**: {r.url}")
        output.append(f"**鏉ユ簮**: {r.source} | **寮曟搸**: {r.engine}\n")
        output.append(f"{r.snippet}\n")
        output.append("---\n")

    return "\n".join(output)


def format_compact(data: Dict[str, Any]) -> str:
    """绱у噾鏍煎紡杈撳嚭"""
    output = []
    output.append(f"馃攳 {data['query']} ({data['total_results']} 缁撴灉, {data['search_time_ms']/1000:.2f}s)")

    for i, r in enumerate(data['results'][:10], 1):
        output.append(f"{i}. [{r.relevance_score:.0f}] {r.title}")
        output.append(f"   {r.url}")

    return "\n".join(output)


def format_json(data: Dict[str, Any]) -> str:
    """JSON鏍煎紡杈撳嚭"""
    output = {
        "query": data["query"],
        "total_results": data["total_results"],
        "search_time_ms": data["search_time_ms"],
        "engines_used": data["engines_used"],
        "results": [
            {
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "score": round(r.relevance_score, 1),
                "source": r.source,
                "engine": r.engine
            }
            for r in data["results"]
        ]
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


# ============ CLI ============

def main():
    parser = argparse.ArgumentParser(
        description='15-web-search-G: 鏅鸿兘缃戠粶鎼滅储宸ュ叿',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
绀轰緥:
  python search.py "Python async programming"
  python search.py "React hooks" --mode fast --max-results 5
  python search.py "machine learning" --output json
        """
    )

    parser.add_argument('query', type=str, help='鎼滅储鏌ヨ')
    parser.add_argument('--mode', type=str, default='auto',
                       choices=['fast', 'auto', 'deep'],
                       help='鎼滅储妯″紡 (榛樿: auto)')
    parser.add_argument('--max-results', type=int, default=10,
                       help='鏈€澶х粨鏋滄暟 (榛樿: 10)')
    parser.add_argument('--output', type=str, default='markdown',
                       choices=['json', 'markdown', 'compact'],
                       help='杈撳嚭鏍煎紡 (榛樿: markdown)')

    args = parser.parse_args()

    # 鎵ц鎼滅储
    try:
        result = asyncio.run(web_search(
            query=args.query,
            mode=args.mode,
            max_results=args.max_results
        ))

        # 鏍煎紡鍖栬緭鍑?
        if args.output == 'json':
            print(format_json(result))
        elif args.output == 'compact':
            print(format_compact(result))
        else:  # markdown
            print(format_markdown(result))

    except KeyboardInterrupt:
        print("\n鎼滅储宸插彇娑?)
        return 1
    except Exception as e:
        print(f"閿欒: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

