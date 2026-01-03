#!/usr/bin/env python3
"""
Chrome 浏览器自动化引擎
基于 Playwright 控制 Google Chrome 浏览器
"""

import os
import json
import time
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


class ChromeAutomation:
    """Chrome 浏览器自动化核心类"""

    def __init__(
        self,
        headless: bool = False,
        chrome_path: Optional[str] = None,
        window_size: tuple = (1920, 1080),
        user_agent: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None,
        timeout: int = 30000
    ):
        """
        初始化 Chrome 浏览器自动化引擎

        Args:
            headless: 是否无头模式（False 显示浏览器窗口）
            chrome_path: Chrome 浏览器路径（None 则自动检测）
            window_size: 窗口大小 (width, height)
            user_agent: 自定义用户代理
            proxy: 代理配置
            timeout: 默认超时时间（毫秒）
        """
        self.headless = headless
        self.chrome_path = chrome_path
        self.window_size = window_size
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        self.proxy = proxy
        self.timeout = timeout

        # Playwright 对象
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # 自动启动浏览器
        self._launch_browser()

    def _launch_browser(self):
        """启动 Chrome 浏览器"""
        self.playwright = sync_playwright().start()

        # 启动参数
        launch_args = {
            "headless": self.headless,
            "channel": "chrome",  # 使用系统安装的 Chrome
            "args": [
                f"--window-size={self.window_size[0]},{self.window_size[1]}",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ]
        }

        # 启动浏览器
        self.browser = self.playwright.chromium.launch(**launch_args)

        # 创建上下文
        context_args = {
            "viewport": {"width": self.window_size[0], "height": self.window_size[1]},
            "user_agent": self.user_agent,
            "accept_downloads": True
        }

        if self.proxy:
            context_args["proxy"] = self.proxy

        self.context = self.browser.new_context(**context_args)

        # 创建页面
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.timeout)

    def navigate(self, url: str, wait_until: str = "load"):
        """
        访问网页

        Args:
            url: 目标网址
            wait_until: 等待条件 (load, domcontentloaded, networkidle)
        """
        print(f"🌐 导航到: {url}")
        self.page.goto(url, wait_until=wait_until)

    def reload(self):
        """刷新当前页面"""
        self.page.reload()

    def wait_for_login(self, seconds: int = 60):
        """
        等待用户手动登录

        Args:
            seconds: 等待秒数
        """
        print("\n" + "=" * 70)
        print("浏览器已打开！请在浏览器中手动登录。")
        print("=" * 70)
        print(f"程序将等待 {seconds} 秒...\n")

        for i in range(seconds, 0, -10):
            print(f"⏱️  剩余 {i} 秒...")
            time.sleep(10)

        print("\n✓ 等待结束，继续执行自动化流程...")

    def wait_for_selector(self, selector: str, timeout: int = None):
        """等待元素出现"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, timeout=timeout)

    def click(self, selector: str):
        """点击元素"""
        self.page.click(selector)

    def type(self, selector: str, text: str, clear: bool = True):
        """输入文本"""
        if clear:
            self.page.fill(selector, text)
        else:
            self.page.type(selector, text)

    def select(self, selector: str, value: str):
        """选择下拉框"""
        self.page.select_option(selector, value)

    def get_text(self, selector: str) -> str:
        """获取单个元素文本"""
        elem = self.page.query_selector(selector)
        if elem:
            return elem.inner_text()
        return ""

    def get_all_text(self, selector: str) -> List[str]:
        """获取多个元素文本"""
        texts = []
        elems = self.page.query_selector_all(selector)
        for elem in elems:
            try:
                texts.append(elem.inner_text())
            except:
                pass
        return texts

    def get_attr(self, selector: str, attr: str) -> str:
        """获取元素属性"""
        elem = self.page.query_selector(selector)
        if elem:
            return elem.get_attribute(attr) or ""
        return ""

    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        elem = self.page.query_selector(selector)
        if elem:
            return elem.is_visible()
        return False

    def extract_products(self, selector: str, fields: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        批量提取商品数据

        Args:
            selector: 商品容器选择器
            fields: 字段映射 {"字段名": "选择器"}

        Returns:
            商品列表
        """
        products = []
        elems = self.page.query_selector_all(selector)

        for elem in elems[:50]:  # 最多 50 个
            product = {}
            for field_name, field_selector in fields.items():
                try:
                    field_elem = elem.query_selector(field_selector)
                    if field_elem:
                        product[field_name] = field_elem.inner_text()
                except:
                    product[field_name] = ""
            products.append(product)

        return products

    def scrape_all_elements(self, selector: str, max_items: int = 20) -> List[Dict[str, Any]]:
        """
        抓取所有匹配的元素

        Args:
            selector: 元素选择器
            max_items: 最大抓取数量

        Returns:
            元素数据列表
        """
        items = []
        elems = self.page.query_selector_all(selector)

        print(f"找到 {len(elems)} 个元素")

        for idx, elem in enumerate(elems[:max_items]):
            try:
                text = elem.inner_text()
                if text and len(text.strip()) > 0:
                    items.append({
                        "index": idx + 1,
                        "text": text.strip(),
                        "html": elem.inner_html()
                    })
            except Exception as e:
                continue

        return items

    def screenshot(self, path: str, full_page: bool = False):
        """
        截图

        Args:
            path: 保存路径
            full_page: 是否全页截图
        """
        self.page.screenshot(path=path, full_page=full_page)
        print(f"📸 截图保存到: {path}")

    def pdf(self, path: str):
        """生成 PDF"""
        self.page.pdf(path=path)
        print(f"📄 PDF 保存到: {path}")

    def evaluate(self, script: str):
        """执行 JavaScript"""
        return self.page.evaluate(script)

    def get_url(self) -> str:
        """获取当前 URL"""
        return self.page.url

    def get_title(self) -> str:
        """获取页面标题"""
        return self.page.title()

    def scroll_to_bottom(self, slow: bool = True, max_scrolls: int = 10):
        """
        滚动页面到底部（用于加载更多内容）

        Args:
            slow: 是否缓慢滚动
            max_scrolls: 最大滚动次数
        """
        print(f"📜 滚动页面加载更多内容...")

        if slow:
            for i in range(max_scrolls):
                self.page.evaluate("window.scrollBy(0, 800)")
                time.sleep(1)  # 增加等待时间
                # 检查是否已经到底部
                scroll_height = self.page.evaluate("document.documentElement.scrollHeight")
                scroll_top = self.page.evaluate("document.documentElement.scrollTop")
                client_height = self.page.evaluate("document.documentElement.clientHeight")
                if scroll_top + client_height >= scroll_height - 100:
                    break
                print(f"   滚动中... ({i+1}/{max_scrolls})")
        else:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

    def click_element(self, selector: str, timeout: int = 5000):
        """
        点击元素并等待导航

        Args:
            selector: 元素选择器
            timeout: 超时时间
        """
        try:
            print(f"🖱️  点击元素: {selector}")
            self.page.click(selector, timeout=timeout)
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  点击失败: {e}")

    def scrape_reviews(self, review_selectors: List[Dict[str, str]], max_reviews: int = 50, scroll: bool = True) -> List[Dict[str, Any]]:
        """
        爬取商品评价

        Args:
            review_selectors: 评价选择器配置列表
                [{"container": "选择器", "user": "用户选择器", "content": "内容选择器", "rating": "评分选择器", "date": "日期选择器"}]
            max_reviews: 最大评价数量
            scroll: 是否滚动加载更多评价

        Returns:
            评价列表
        """
        reviews = []
        print(f"💬 开始爬取评价...")

        # 如果需要滚动，先滚动页面加载更多评价
        if scroll:
            self.scroll_to_bottom(slow=True, max_scrolls=15)
            time.sleep(2)

        # 尝试多种选择器配置
        for config in review_selectors:
            try:
                container_selector = config.get("container", "")
                user_selector = config.get("user", "")
                content_selector = config.get("content", "")
                rating_selector = config.get("rating", "")
                date_selector = config.get("date", "")

                review_elems = self.page.query_selector_all(container_selector)
                print(f"使用选择器 '{container_selector}' 找到 {len(review_elems)} 条评价")

                for idx, elem in enumerate(review_elems[:max_reviews]):
                    try:
                        review = {"index": idx + 1}

                        # 提取用户名
                        if user_selector:
                            user_elem = elem.query_selector(user_selector)
                            if user_elem:
                                review["user"] = user_elem.inner_text().strip()

                        # 提取评价内容
                        if content_selector:
                            content_elem = elem.query_selector(content_selector)
                            if content_elem:
                                review["content"] = content_elem.inner_text().strip()

                        # 提取评分
                        if rating_selector:
                            rating_elem = elem.query_selector(rating_selector)
                            if rating_elem:
                                review["rating"] = rating_elem.inner_text().strip()
                                # 尝试获取属性中的评分
                                if not review["rating"]:
                                    review["rating"] = rating_elem.get_attribute("title") or ""

                        # 提取日期
                        if date_selector:
                            date_elem = elem.query_selector(date_selector)
                            if date_elem:
                                review["date"] = date_elem.inner_text().strip()

                        # 如果至少有内容就添加
                        if "content" in review and review["content"]:
                            reviews.append(review)

                    except Exception as e:
                        continue

                # 如果找到了评价，就不再尝试其他选择器
                if len(reviews) > 0:
                    print(f"✓ 成功提取 {len(reviews)} 条评价")
                    break

            except Exception as e:
                print(f"⚠️  选择器 '{config.get('container', '')}' 失败: {e}")
                continue

        return reviews

    def scrape_all_elements(self, selector: str, max_items: int = 20) -> List[Dict[str, Any]]:
        """
        抓取所有匹配的元素

        Args:
            selector: 元素选择器
            max_items: 最大抓取数量

        Returns:
            元素数据列表
        """
        items = []
        elems = self.page.query_selector_all(selector)

        print(f"找到 {len(elems)} 个元素")

        for idx, elem in enumerate(elems[:max_items]):
            try:
                text = elem.inner_text()
                if text and len(text.strip()) > 0:
                    items.append({
                        "index": idx + 1,
                        "text": text.strip(),
                        "html": elem.inner_html()
                    })
            except Exception as e:
                continue

        return items

    def close(self):
        """关闭浏览器"""
        print("🔚 关闭浏览器...")
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
