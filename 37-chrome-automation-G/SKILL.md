---
name: 37-chrome-automation-G
description: Google Chrome 浏览器自动化工具。使用 Playwright 控制 Chrome 浏览器，支持页面导航、元素操作、表单填写、数据抓取、截图、PDF 生成。适用于网页自动化、数据采集、UI 测试、表单自动填写、网页监控。
---

# 37-chrome-automation - Chrome 浏览器自动化工具

**版本**: 1.0.0
**优先级**: P1 (高频使用)
**类别**: 自动化工具
**浏览器**: Google Chrome / Chromium

## 描述

基于 **Google Chrome** 的浏览器自动化工具，使用 Playwright 框架控制 Chrome 浏览器。

**核心功能**:
- 🌐 **页面导航**: 打开网页、前进后退、刷新、等待加载
- 🖱️ **元素操作**: 点击、输入、选择、悬停、拖拽
- 📝 **表单处理**: 自动填写表单、文件上传、下拉选择
- 📊 **数据抓取**: 提取文本、属性、HTML、JSON数据
- 📸 **截图录制**: 全页截图、元素截图、PDF生成
- 🔐 **登录支持**: 打开浏览器让用户手动登录，然后继续自动化
- ⏱️ **智能等待**: 元素可见、网络空闲、自定义条件
- 🎯 **多种选择器**: CSS、XPath、文本内容、ARIA标签

## 使用场景

### 1. 需要登录的数据抓取
```bash
# 打开网站，等待用户登录，然后自动抓取数据
python scripts/with_login.py --url "https://www.taobao.com" --wait 120
```

### 2. 自动化表单填写
```python
from chrome_engine import ChromeAutomation

browser = ChromeAutomation(headless=False)
browser.navigate("https://example.com/form")
browser.type("input[name='email']", "user@example.com")
browser.type("input[name='password']", "password")
browser.click("button[type='submit']")
```

### 3. 批量数据采集
```bash
python scripts/scrape.py --url "https://search.jd.com/Search?keyword=手机" --output products.json
```

### 4. 网页监控和截图
```python
browser = ChromeAutomation()
browser.navigate("https://example.com")
browser.screenshot("screenshot.png")
# 检测页面变化
if browser.is_visible("div.new-item"):
    print("发现新内容！")
```

## 快速开始

### 安装依赖
```bash
cd C:\Users\bigbao\.claude\skills\37-chrome-automation
pip install -r requirements.txt
python -m playwright install chromium
```

### 基础用法

**方式 1: Python API**
```python
from chrome_engine import ChromeAutomation

# 初始化浏览器
browser = ChromeAutomation(headless=False)

# 访问页面
browser.navigate("https://www.example.com")

# 等待用户登录（60秒）
browser.wait_for_login(60)

# 提取数据
products = browser.extract_products(".product-item", {
    "name": "h3.title",
    "price": "span.price"
})

# 关闭浏览器
browser.close()
```

**方式 2: 命令行工具**
```bash
# 打开网站并等待登录
python handler.py navigate --url "https://www.jd.com" --wait 120

# 抓取数据
python handler.py scrape --url "https://search.jd.com/Search?keyword=手机" --selector ".gl-item" --output jd_products.json

# 截图
python handler.py screenshot --url "https://www.example.com" --output screenshot.png
```

## 命令参考

### 导航命令
```bash
# 访问网页
python handler.py navigate --url "https://www.example.com"

# 访问并等待用户登录
python handler.py navigate --url "https://www.taobao.com" --wait 120

# 刷新页面
python handler.py reload
```

### 数据提取命令
```bash
# 抓取单个元素文本
python handler.py extract --url "https://example.com" --selector "h1"

# 抓取多个元素
python handler.py scrape --url "https://example.com" --selector ".item" --output items.json

# 提取表格
python handler.py table --url "https://example.com" --selector "table" --output data.csv
```

### 截图命令
```bash
# 全页截图
python handler.py screenshot --url "https://example.com" --output page.png

# 元素截图
python handler.py screenshot --url "https://example.com" --selector ".main" --output element.png

# 生成 PDF
python handler.py pdf --url "https://example.com" --output page.pdf
```

## Python API 完整参考

### ChromeAutomation 类

```python
class ChromeAutomation:
    def __init__(
        self,
        headless: bool = False,
        chrome_path: str = None,
        window_size: tuple = (1920, 1080),
        user_agent: str = None,
        timeout: int = 30000
    )
```

**方法列表**:

| 方法 | 说明 | 示例 |
|------|------|------|
| `navigate(url)` | 访问网页 | `browser.navigate("https://www.taobao.com")` |
| `wait_for_login(seconds)` | 等待用户登录 | `browser.wait_for_login(120)` |
| `click(selector)` | 点击元素 | `browser.click("button#submit")` |
| `type(selector, text)` | 输入文本 | `browser.type("input#name", "张三")` |
| `get_text(selector)` | 获取文本 | `browser.get_text("h1.title")` |
| `get_all_text(selector)` | 获取多个文本 | `browser.get_all_text(".item")` |
| `extract_products(selector, fields)` | 批量提取 | `browser.extract_products(".item", {"name": "h3", "price": ".price"})` |
| `screenshot(path)` | 截图 | `browser.screenshot("page.png")` |
| `close()` | 关闭浏览器 | `browser.close()` |

## 常见使用场景

### 场景 1: 淘宝/京东商品抓取（需登录）

```bash
# 打开淘宝，等待 120 秒登录，然后自动抓取商品
python scripts/with_login.py \
  --url "https://s.taobao.com/search?q=手机" \
  --wait 120 \
  --selector "[class*='Card']" \
  --output taobao_products.json
```

### 场景 2: 网页定期监控

```python
from chrome_engine import ChromeAutomation
import time

browser = ChromeAutomation()

while True:
    browser.navigate("https://example.com/status")

    # 检查是否有新内容
    if browser.is_visible("div.new-badge"):
        browser.screenshot(f"update_{int(time.time())}.png")
        print("发现更新！")

    time.sleep(300)  # 5分钟后再检查

browser.close()
```

### 场景 3: 自动填写表单

```python
from chrome_engine import ChromeAutomation

browser = ChromeAutomation(headless=False)

# 打开表单页面
browser.navigate("https://example.com/form")

# 填写表单
browser.type("#name", "张三")
browser.type("#email", "zhangsan@example.com")
browser.select("#country", "China")
browser.click("button[type='submit']")

# 等待提交完成
browser.wait_for_selector("div.success")

browser.close()
```

## 配置选项

### 浏览器配置
```python
{
    "headless": False,              # 是否无头模式
    "window_size": (1920, 1080),    # 窗口大小
    "user_agent": "Mozilla/5.0...",  # 自定义 UA
    "timeout": 30000,               # 默认超时
    "chrome_path": None             # Chrome 路径（自动检测）
}
```

### 反检测配置
```python
browser = ChromeAutomation(
    headless=False,  # 有头模式更难检测
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
```

## 注意事项

1. **登录网站**: 淘宝、京东等需要登录的网站，使用 `wait_for_login()` 方法
2. **反爬虫**: 使用真实 User-Agent，避免过于频繁的请求
3. **等待时间**: 页面加载需要时间，使用合适的等待策略
4. **选择器变化**: 网站结构可能变化，需要及时更新选择器

## 依赖安装

```bash
pip install playwright
python -m playwright install chromium
```

## 技术栈

- **Playwright**: 浏览器自动化框架
- **Chrome/Chromium**: Google Chrome 浏览器
- **Python 3.8+**: 编程语言
