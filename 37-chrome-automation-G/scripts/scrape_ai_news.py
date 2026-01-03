#!/usr/bin/env python3
"""
AI新闻爬取脚本
爬取 AIBase 的今日AI新闻
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime, date as date_class

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from chrome_engine import ChromeAutomation


def scrape_ai_news():
    """爬取AI新闻"""
    print("=" * 70)
    print("AI新闻爬取 - AIBase (含详细内容)")
    print("=" * 70)

    browser = ChromeAutomation(headless=False)

    # 访问新闻页面
    url = "https://www.aibase.com/zh/news"
    print(f"\n🌐 访问: {url}")
    browser.navigate(url, wait_until="domcontentloaded")
    time.sleep(5)

    # 获取今天的日期
    today = date_class.today()
    today_str = today.strftime("%Y-%m-%d")
    print(f"📅 今天日期: {today_str}")

    # 截图
    browser.screenshot("aibase_news_page.png")

    # 使用JavaScript提取新闻数据
    js_code = f"""
    () => {{
        const results = [];

        // 先获取页面上所有链接
        const allLinks = Array.from(document.querySelectorAll('a'));

        // 过滤出新闻相关的链接
        allLinks.forEach((link, index) => {{
            const href = link.getAttribute('href') || '';
            const text = (link.textContent || link.innerText || '').trim();

            // 只处理包含/news/的链接
            if (href.includes('/news/') && !href.includes('#')) {{
                // 获取完整URL
                let fullUrl = href;
                if (href.startsWith('/')) {{
                    fullUrl = 'https://www.aibase.com' + href;
                }}

                // 查找日期
                let parent = link.parentElement;
                let dateText = '';
                for (let i = 0; i < 4; i++) {{
                    if (parent && parent !== document.body) {{
                        const timeElem = parent.querySelector('time, .date, .time, span[class*="date"], span[class*="time"]');
                        if (timeElem) {{
                            dateText = timeElem.textContent || timeElem.getAttribute('datetime') || '';
                            break;
                        }}
                        parent = parent.parentElement;
                    }} else {{
                        break;
                    }}
                }}

                if (text.length > 5 && text.length < 300) {{
                    results.push({{
                        index: results.length + 1,
                        title: text,
                        url: fullUrl,
                        date: dateText
                    }});
                }}
            }}
        }});

        // 去重
        const uniqueResults = [];
        const seenUrls = new Set();
        for (const item of results) {{
            if (!seenUrls.has(item.url)) {{
                seenUrls.add(item.url);
                uniqueResults.push(item);
            }}
        }}

        return uniqueResults.slice(0, 10);  // 只取前10条
    }}
    """

    print("\n🔍 提取新闻列表...")
    try:
        news_items = browser.page.evaluate(js_code)
        print(f"✓ 提取到 {len(news_items)} 条新闻")
    except Exception as e:
        print(f"⚠️ 提取失败: {e}")
        news_items = []

    # 爬取每条新闻的详细内容
    print("\n" + "=" * 70)
    print("开始爬取新闻详细内容...")
    print("=" * 70)

    for i, item in enumerate(news_items, 1):
        print(f"\n[{i}/{len(news_items)}] {item.get('title', '')[:60]}...")
        print(f"   链接: {item.get('url', '')}")

        try:
            # 访问新闻详情页
            browser.page.goto(item['url'], wait_until="domcontentloaded")
            time.sleep(3)

            # 提取正文内容
            content_js = """
            () => {
                // 查找文章正文
                const contentSelectors = [
                    'article',
                    '.article-content',
                    '.content',
                    '.post-content',
                    '[class*="article-body"]',
                    '[class*="post-body"]',
                    'main p',
                    '.entry-content'
                ];

                let content = '';
                let author = '';
                let publishDate = '';

                // 提取作者
                const authorElem = document.querySelector('.author, [class*="author"], .writer, .by');
                if (authorElem) {
                    author = authorElem.textContent || authorElem.innerText || '';
                }

                // 提取发布日期
                const dateElem = document.querySelector('time, .publish-date, [class*="date"], [class*="time"]');
                if (dateElem) {
                    publishDate = dateElem.textContent || dateElem.getAttribute('datetime') || '';
                }

                // 提取正文
                for (const selector of contentSelectors) {
                    const elem = document.querySelector(selector);
                    if (elem) {
                        const paragraphs = elem.querySelectorAll('p');
                        if (paragraphs.length > 0) {
                            const texts = [];
                            paragraphs.forEach(p => {
                                const text = (p.textContent || p.innerText || '').trim();
                                if (text.length > 10) {
                                    texts.push(text);
                                }
                            });
                            if (texts.length > 0) {
                                content = texts.join('\\n\\n');
                                break;
                            }
                        }
                    }
                }

                // 如果没找到，尝试获取页面主要内容
                if (!content) {
                    const mainContent = document.querySelector('main, article, .content, #content');
                    if (mainContent) {
                        content = mainContent.textContent || mainContent.innerText || '';
                        content = content.substring(0, 3000);
                    }
                }

                return {
                    content: content.substring(0, 2000),
                    author: author.substring(0, 50),
                    publishDate: publishDate.substring(0, 50)
                };
            }
            """

            content_data = browser.page.evaluate(content_js)
            item['content'] = content_data.get('content', '')
            item['author'] = content_data.get('author', '')
            item['publishDate'] = content_data.get('publishDate', '')

            content_preview = item['content'][:100] if item['content'] else '无内容'
            print(f"   ✓ 内容长度: {len(item['content'])} 字符")
            print(f"   预览: {content_preview}...")

        except Exception as e:
            print(f"   ✗ 爬取失败: {e}")
            item['content'] = ''
            item['error'] = str(e)

        # 返回列表页
        if i < len(news_items):
            browser.page.go_back()
            time.sleep(2)

    # 保存数据
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # JSON文件
    json_file = f"ai_news_detail_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "scraped_at": datetime.now().isoformat(),
            "today": today_str,
            "total_count": len(news_items),
            "news": news_items
        }, f, ensure_ascii=False, indent=2)

    # 生成详细报告
    report_text = f"""
{'='*70}
                    AI新闻详细报告
{'='*70}

抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
新闻来源: AIBase (https://www.aibase.com/zh/news)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
新闻总数: {len(news_items)} 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for i, item in enumerate(news_items, 1):
        report_text += f"""
─────────────────────────────────────────────────────────────────────────────
【新闻 {i}】{item.get('title', '')}
─────────────────────────────────────────────────────────────────────────────
链接: {item.get('url', '')}
日期: {item.get('date', '')}
"""

        if item.get('author'):
            report_text += f"作者: {item.get('author', '')}\n"

        report_text += f"""
正文内容:
{item.get('content', '(无内容)')}

"""

    # 保存报告
    text_file = f"ai_news_detail_report_{timestamp}.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(report_text)

    # 打印摘要
    print("\n" + "=" * 70)
    print("爬取完成摘要")
    print("=" * 70)
    for i, item in enumerate(news_items, 1):
        has_content = "✓" if item.get('content') else "✗"
        content_len = len(item.get('content', ''))
        title = item.get('title', '')[:60]
        print(f"{has_content} [{i}] {title} ({content_len} 字符)")

    print(f"\n✓ JSON数据: {json_file}")
    print(f"✓ 详细报告: {text_file}")

    print("\n浏览器保持打开 10 秒...")
    time.sleep(10)

    browser.close()

    return json_file, text_file


if __name__ == "__main__":
    try:
        scrape_ai_news()
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
