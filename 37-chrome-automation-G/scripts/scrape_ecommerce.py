#!/usr/bin/env python3
"""
淘宝/京东商品抓取示例
支持用户登录后自动抓取数据
"""
import sys
import json
import argparse
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from chrome_engine import ChromeAutomation


def scrape_taobao(keyword="手机", wait_seconds=120):
    """抓取淘宝商品"""
    print("=" * 70)
    print(f"抓取淘宝商品 - 搜索关键词: {keyword}")
    print("=" * 70)

    browser = ChromeAutomation(headless=False)

    # 访问淘宝搜索页面
    url = f"https://s.taobao.com/search?q={keyword}"
    browser.navigate(url)

    # 等待用户登录
    browser.wait_for_login(wait_seconds)

    # 尝试多种选择器
    selectors = [
        "[class*='Card']",
        ".item",
        "[class*='product']",
        "div[class*='Item']"
    ]

    items = []
    for selector in selectors:
        try:
            items = browser.scrape_all_elements(selector, max_items=30)
            if len(items) > 0:
                print(f"\n✓ 使用选择器 '{selector}' 找到 {len(items)} 个商品")
                break
        except Exception as e:
            continue

    # 显示结果
    print("\n" + "=" * 70)
    print(f"成功抓取 {len(items)} 个商品:")
    print("=" * 70)

    for item in items[:10]:
        print(f"\n【商品 {item['index']}】")
        text_lines = item['text'].split('\n')
        for line in text_lines[:8]:
            if line.strip():
                print(f"  {line.strip()}")

    # 保存数据
    output_file = "taobao_products.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 数据已保存到: {output_file}")

    # 截图
    browser.screenshot("taobao_result.png")

    print("\n浏览器保持打开 30 秒...")
    import time
    time.sleep(30)

    browser.close()
    return len(items) > 0


def scrape_jd(keyword="手机", wait_seconds=120):
    """抓取京东商品"""
    print("=" * 70)
    print(f"抓取京东商品 - 搜索关键词: {keyword}")
    print("=" * 70)

    browser = ChromeAutomation(headless=False)

    # 访问京东搜索页面
    url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8"
    browser.navigate(url)

    # 等待用户登录
    browser.wait_for_login(wait_seconds)

    # 尝试多种选择器
    selectors = [
        ".gl-item",
        ".gl-warp .gl-item",
        "[class*='product']",
        "[data-sku]"
    ]

    items = []
    for selector in selectors:
        try:
            items = browser.scrape_all_elements(selector, max_items=30)
            if len(items) > 0:
                print(f"\n✓ 使用选择器 '{selector}' 找到 {len(items)} 个商品")
                break
        except Exception as e:
            continue

    # 显示结果
    print("\n" + "=" * 70)
    print(f"成功抓取 {len(items)} 个商品:")
    print("=" * 70)

    for item in items[:10]:
        print(f"\n【商品 {item['index']}】")
        text_lines = item['text'].split('\n')
        for line in text_lines[:8]:
            if line.strip():
                print(f"  {line.strip()}")

    # 保存数据
    output_file = "jd_products.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 数据已保存到: {output_file}")

    # 截图
    browser.screenshot("jd_result.png")

    print("\n浏览器保持打开 30 秒...")
    import time
    time.sleep(30)

    browser.close()
    return len(items) > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", choices=["taobao", "jd"], default="taobao", help="目标网站")
    parser.add_argument("--keyword", default="手机", help="搜索关键词")
    parser.add_argument("--wait", type=int, default=120, help="等待登录时间（秒）")

    args = parser.parse_args()

    try:
        if args.site == "taobao":
            scrape_taobao(args.keyword, args.wait)
        else:
            scrape_jd(args.keyword, args.wait)
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
