"""
Retry Failed APIs with Corrected Configurations
尝试修复失败的3个API
"""

import os
import asyncio
import httpx
import json


async def test_perplexity_with_correct_model():
    """测试 Perplexity API - 使用正确的模型名"""
    print("\n🔍 Retrying Perplexity API with corrected model names...")

    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 尝试不同的模型名称
    models_to_try = [
        "llama-3.1-sonar-small-128k-online",  # 原始尝试
        "sonar-small-online",                  # 简化名称
        "sonar",                               # 最简名称
        "llama-3.1-sonar-large-128k-online",  # 大模型
        "sonar-medium-online"                  # 中等模型
    ]

    for model in models_to_try:
        print(f"\n  Trying model: {model}...")

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "What is Python async?"
                }
            ],
            "max_tokens": 50
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    print(f"  ✅ SUCCESS with model '{model}'!")
                    print(f"  Response: {content[:100]}...")
                    return {
                        "status": "✅ WORKING",
                        "model": model,
                        "response": content
                    }
                elif response.status_code == 401:
                    print(f"  ❌ 401 Unauthorized - API key invalid")
                    return {
                        "status": "❌ FAILED",
                        "error": "Invalid API key"
                    }
                else:
                    error_text = response.text[:200]
                    print(f"  ⚠️  Failed with {response.status_code}: {error_text}")

        except Exception as e:
            print(f"  ⚠️  Error: {str(e)}")

    print("\n  ❌ All Perplexity models failed")
    return {
        "status": "❌ FAILED",
        "error": "All model names failed"
    }


async def test_gemini_with_correct_endpoint():
    """测试 Gemini API - 尝试不同的endpoint和模型"""
    print("\n🔍 Retrying Gemini API with corrected endpoints...")

    api_keys = [
        os.getenv("YOUTUBE_API_KEY", ""),
        os.getenv("YOUTUBE_API_KEY", "")
    ]

    # 尝试不同的endpoint配置
    endpoints_to_try = [
        ("gemini-1.5-flash", "v1beta"),
        ("gemini-1.5-flash-latest", "v1beta"),
        ("gemini-pro", "v1"),
        ("gemini-1.0-pro", "v1"),
        ("gemini-flash-1.5", "v1")
    ]

    for model, version in endpoints_to_try:
        print(f"\n  Trying {version}/models/{model}...")

        for idx, api_key in enumerate(api_keys, 1):
            url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": "What is Python async?"
                    }]
                }]
            }

            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, json=payload)

                    if response.status_code == 200:
                        data = response.json()
                        content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        print(f"  ✅ SUCCESS with {model} (Key {idx})!")
                        print(f"  Response: {content[:100]}...")
                        return {
                            "status": "✅ WORKING",
                            "model": model,
                            "version": version,
                            "working_key": idx,
                            "response": content
                        }
                    elif response.status_code == 401 or response.status_code == 403:
                        print(f"  ⚠️  Key {idx}: Auth error (trying next key)")
                    elif response.status_code == 404:
                        print(f"  ⚠️  Model not found (trying next model)")
                        break  # 跳到下一个模型
                    else:
                        error_text = response.text[:200]
                        print(f"  ⚠️  Key {idx}: {response.status_code} - {error_text}")

            except Exception as e:
                print(f"  ⚠️  Key {idx} Error: {str(e)}")

    print("\n  ❌ All Gemini endpoints and models failed")
    return {
        "status": "❌ FAILED",
        "error": "All endpoint/model combinations failed"
    }


async def test_you_with_different_endpoints():
    """测试 You.com API - 尝试不同的endpoint"""
    print("\n🔍 Retrying You.com API with different endpoints...")

    api_key = os.getenv("YOU_API_KEY", "")

    # 尝试不同的endpoint
    endpoints_to_try = [
        ("https://api.ydc-index.io/search", "GET"),
        ("https://api.ydc-index.io/search", "POST"),
        ("https://api.you.com/search", "GET"),
        ("https://api.you.com/v1/search", "GET")
    ]

    for url, method in endpoints_to_try:
        print(f"\n  Trying {method} {url}...")

        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "GET":
                    params = {"query": "Python async"}
                    response = await client.get(url, headers=headers, params=params)
                else:
                    payload = {"query": "Python async"}
                    response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    print(f"  ✅ SUCCESS with {method} {url}!")
                    print(f"  Response keys: {list(data.keys())}")
                    return {
                        "status": "✅ WORKING",
                        "endpoint": url,
                        "method": method,
                        "response": str(data)[:200]
                    }
                elif response.status_code == 403:
                    print(f"  ❌ 403 Forbidden - API key might be invalid or expired")
                elif response.status_code == 404:
                    print(f"  ⚠️  404 Not Found - endpoint doesn't exist")
                else:
                    error_text = response.text[:200]
                    print(f"  ⚠️  {response.status_code}: {error_text}")

        except Exception as e:
            print(f"  ⚠️  Error: {str(e)}")

    print("\n  ❌ All You.com endpoints failed - API key likely invalid")
    return {
        "status": "❌ FAILED",
        "error": "All endpoints failed - API key likely invalid or expired"
    }


async def main():
    """主函数"""
    print("="*60)
    print("🔄 Retrying Failed APIs with Corrected Configurations")
    print("="*60)

    results = {}

    # 测试 Perplexity
    results["Perplexity"] = await test_perplexity_with_correct_model()

    # 测试 Gemini
    results["Gemini"] = await test_gemini_with_correct_endpoint()

    # 测试 You.com
    results["You.com"] = await test_you_with_different_endpoints()

    print("\n" + "="*60)
    print("📊 RETRY RESULTS")
    print("="*60)

    for api_name, result in results.items():
        print(f"\n{result['status']} {api_name}")
        if result['status'].startswith("✅"):
            if 'model' in result:
                print(f"   Working model: {result['model']}")
            if 'endpoint' in result:
                print(f"   Working endpoint: {result['endpoint']}")
            if 'working_key' in result:
                print(f"   Working key: #{result['working_key']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")

    # 保存结果
    with open("D:/trae/claude-skills/skills/15-web-search-G/retry_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n💾 Retry results saved to: retry_results.json")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
