#!/usr/bin/env python3
"""
简单测试 - 验证 Chrome 自动化是否正常工作
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from chrome_engine import ChromeAutomation


def test_basic():
    """基础功能测试"""
    print("=" * 70)
    print("Chrome 自动化基础测试")
    print("=" * 70)

    print("\n[1] 启动浏览器...")
    browser = ChromeAutomation(headless=False)

    print("[2] 访问百度...")
    browser.navigate("https://www.baidu.com")

    print("[3] 获取页面信息...")
    print(f"页面标题: {browser.get_title()}")
    print(f"当前 URL: {browser.get_url()}")

    print("[4] 截图保存...")
    browser.screenshot("test_baidu.png")

    print("\n[5] 测试完成！浏览器将在 5 秒后自动关闭...")
    import time
    time.sleep(5)

    browser.close()
    print("\n✓ 测试完成！")


if __name__ == "__main__":
    try:
        test_basic()
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
