#!/usr/bin/env python3
"""
Chrome 自动化命令行工具
"""
import sys
import json
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from chrome_engine import ChromeAutomation


def cmd_navigate(args):
    """导航命令"""
    browser = ChromeAutomation(headless=False)
    browser.navigate(args.url)

    if args.wait:
        browser.wait_for_login(args.wait)

    if args.screenshot:
        browser.screenshot(args.screenshot)

    if args.keep_open:
        input("\n按回车键关闭浏览器...")

    browser.close()


def cmd_scrape(args):
    """抓取数据命令"""
    browser = ChromeAutomation(headless=args.headless)
    browser.navigate(args.url)

    # 等待登录
    if args.wait:
        browser.wait_for_login(args.wait)

    # 抓取数据
    items = browser.scrape_all_elements(args.selector, args.max_items)

    # 保存结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✓ 数据已保存到: {args.output}")
    else:
        print(json.dumps(items, ensure_ascii=False, indent=2))

    if args.screenshot:
        browser.screenshot(args.screenshot)

    if not args.headless and args.keep_open:
        input("\n按回车键关闭浏览器...")

    browser.close()


def cmd_extract(args):
    """提取单个元素"""
    browser = ChromeAutomation(headless=args.headless)
    browser.navigate(args.url)

    # 等待登录
    if args.wait:
        browser.wait_for_login(args.wait)

    # 提取元素
    text = browser.get_text(args.selector)
    print(f"提取结果:\n{text}")

    if args.screenshot:
        browser.screenshot(args.screenshot)

    browser.close()


def cmd_screenshot(args):
    """截图命令"""
    browser = ChromeAutomation(headless=args.headless)
    browser.navigate(args.url)

    # 等待
    if args.wait:
        browser.wait_for_login(args.wait)

    # 截图
    browser.screenshot(args.output, full_page=args.full_page)

    if not args.headless and args.keep_open:
        input("\n按回车键关闭浏览器...")

    browser.close()


def main():
    parser = argparse.ArgumentParser(description="Chrome 浏览器自动化工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # navigate 命令
    nav_parser = subparsers.add_parser("navigate", help="访问网页")
    nav_parser.add_argument("--url", required=True, help="目标网址")
    nav_parser.add_argument("--wait", type=int, help="等待用户登录（秒）")
    nav_parser.add_argument("--screenshot", help="截图保存路径")
    nav_parser.add_argument("--keep-open", action="store_true", help="保持浏览器打开")

    # scrape 命令
    scrape_parser = subparsers.add_parser("scrape", help="抓取数据")
    scrape_parser.add_argument("--url", required=True, help="目标网址")
    scrape_parser.add_argument("--selector", required=True, help="元素选择器")
    scrape_parser.add_argument("--output", help="输出文件路径 (JSON)")
    scrape_parser.add_argument("--wait", type=int, help="等待用户登录（秒）")
    scrape_parser.add_argument("--max-items", type=int, default=20, help="最大抓取数量")
    scrape_parser.add_argument("--headless", action="store_true", help="无头模式")
    scrape_parser.add_argument("--screenshot", help="同时保存截图")
    scrape_parser.add_argument("--keep-open", action="store_true", help="保持浏览器打开")

    # extract 命令
    extract_parser = subparsers.add_parser("extract", help="提取单个元素")
    extract_parser.add_argument("--url", required=True, help="目标网址")
    extract_parser.add_argument("--selector", required=True, help="元素选择器")
    extract_parser.add_argument("--wait", type=int, help="等待用户登录（秒）")
    extract_parser.add_argument("--headless", action="store_true", help="无头模式")
    extract_parser.add_argument("--screenshot", help="同时保存截图")

    # screenshot 命令
    shot_parser = subparsers.add_parser("screenshot", help="网页截图")
    shot_parser.add_argument("--url", required=True, help="目标网址")
    shot_parser.add_argument("--output", required=True, help="截图保存路径")
    shot_parser.add_argument("--wait", type=int, help="等待用户登录（秒）")
    shot_parser.add_argument("--headless", action="store_true", help="无头模式")
    shot_parser.add_argument("--full-page", action="store_true", help="全页截图")
    shot_parser.add_argument("--keep-open", action="store_true", help="保持浏览器打开")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 执行命令
    if args.command == "navigate":
        cmd_navigate(args)
    elif args.command == "scrape":
        cmd_scrape(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "screenshot":
        cmd_screenshot(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
