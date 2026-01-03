#!/usr/bin/env python3
"""
AI眼镜商品评价爬取脚本 V3
重点搜索可搭配戒指使用的AI眼镜
直接提取页面所有用户反馈文本
"""
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from chrome_engine import ChromeAutomation


# AI眼镜关键词
KEYWORDS = [
    "智能眼镜",
    "AR眼镜",
    "Xreal 眼镜",
    "Rokid 眼镜",
    "雷鸟 眼镜",
    "Meta Ray Ban"
]


def extract_all_user_feedback(browser):
    """提取页面所有用户反馈/评价内容"""
    print("🔍 提取用户反馈数据...")

    js_code = """
    () => {
        const results = [];

        // 先尝试查找评价相关的容器
        const reviewContainers = [
            'div[class*="review"]',
            'div[class*="Review"]',
            'div[class*="comment"]',
            'div[class*="Comment"]',
            'div[class*="rate"]',
            'div[class*="Rate"]',
            '.review-item',
            '.comment-item',
            '[data-review]',
            '[class*="feedback"]'
        ];

        // 用户反馈关键词
        const feedbackKeywords = [
            '质量', '效果', '使用', '体验', '推荐', '不错', '好', '很好',
            '方便', '实用', '清晰', '舒适', '满意', '喜欢', '棒',
            '差', '问题', '不好', '失望', '退货', '一般',
            '佩戴', '音质', '续航', '连接', '功能', '外观', '价格',
            '发货', '物流', '包装', '客服', '售后', '性价比'
        ];

        // 首先从评价容器中提取
        for (const selector of reviewContainers) {
            const elements = document.querySelectorAll(selector);
            elements.forEach(elem => {
                const text = (elem.textContent || elem.innerText || '').trim();
                if (text.length >= 15 && text.length <= 500) {
                    results.push({
                        text: text,
                        source: 'container',
                        selector: selector,
                        className: elem.className || ''
                    });
                }
            });
        }

        // 如果结果太少，则全局搜索
        if (results.length < 10) {
            const allElements = document.querySelectorAll('p, span, div, li, td');
            allElements.forEach(elem => {
                const text = (elem.textContent || elem.innerText || '').trim();
                if (text.length >= 15 && text.length <= 500) {
                    const hasKeyword = feedbackKeywords.some(kw => text.includes(kw));
                    if (hasKeyword) {
                        const isDuplicate = results.some(r =>
                            text.substring(0, 50) === r.text.substring(0, 50)
                        );
                        if (!isDuplicate) {
                            results.push({
                                text: text,
                                source: 'global',
                                tag: elem.tagName,
                                className: elem.className || ''
                            });
                        }
                    }
                }
            });
        }

        // 去重
        const uniqueResults = [];
        const seen = new Set();
        for (const item of results) {
            const key = item.text.substring(0, 50);
            if (!seen.has(key)) {
                seen.add(key);
                uniqueResults.push(item);
            }
        }

        return uniqueResults.slice(0, 50);
    }
    """

    try:
        feedbacks = browser.page.evaluate(js_code)
        print(f"✓ 提取到 {len(feedbacks)} 条用户反馈")
        return feedbacks
    except Exception as e:
        print(f"⚠️ 提取失败: {e}")
        return []


def extract_product_info(browser):
    """提取商品信息"""
    print("📦 提取商品信息...")

    js_code = """
    () => {
        const results = [];

        // 查找价格
        const pricePatterns = [
            /¥?\\d+\\.?\\d*/,
            /\\d+元/,
            /\\$\\s*\\d+/
        ];

        // 获取页面标题
        results.push({
            type: 'title',
            text: document.title || '无标题'
        });

        // 查找价格元素
        const priceSelectors = ['.price', '[class*="price"]', '[class*="Price"]', '.J_price'];
        for (const selector of priceSelectors) {
            const elems = document.querySelectorAll(selector);
            elems.forEach(elem => {
                const text = (elem.textContent || elem.innerText || '').trim();
                if (text && text.length < 50) {
                    results.push({
                        type: 'price',
                        text: text
                    });
                }
            });
        }

        // 查找商品参数/规格
        const specSelectors = [
            '[class*="param"]',
            '[class*="spec"]',
            '[class*="detail"]',
            '.parameter'
        ];
        for (const selector of specSelectors) {
            const elems = document.querySelectorAll(selector);
            elems.forEach(elem => {
                const text = (elem.textContent || elem.innerText || '').trim();
                if (text.length > 10 && text.length < 300) {
                    results.push({
                        type: 'spec',
                        text: text
                    });
                }
            });
        }

        return results.slice(0, 30);
    }
    """

    try:
        infos = browser.page.evaluate(js_code)
        print(f"✓ 提取到 {len(infos)} 条商品信息")
        return infos
    except Exception as e:
        print(f"⚠️ 提取失败: {e}")
        return []


def scrape_taobao_products(browser, keywords, wait_seconds=120):
    """爬取淘宝商品和用户反馈"""
    print("=" * 70)
    print("淘宝 AI眼镜 爬取")
    print("=" * 70)

    import urllib.parse

    all_data = {
        "products": [],
        "feedbacks": [],
        "specs": []
    }

    for idx, keyword in enumerate(keywords[:3]):
        print(f"\n{'='*70}")
        print(f"[{idx+1}/3] 搜索: {keyword}")
        print(f"{'='*70}")

        encoded = urllib.parse.quote(keyword)
        url = f"https://s.taobao.com/search?q={encoded}"

        try:
            browser.navigate(url, wait_until="domcontentloaded")
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ 导航失败: {e}")
            continue

        # 首次等待登录
        if idx == 0:
            browser.wait_for_login(wait_seconds)

        # 抓取商品列表
        selectors = [
            "[class*='Card']",
            ".item",
            "[class*='ProductItem']",
            "div[class*='Item']",
            "a[class*='title']"
        ]

        products = []
        for selector in selectors:
            try:
                items = browser.scrape_all_elements(selector, max_items=20)
                if items:
                    print(f"✓ 找到 {len(items)} 个元素")
                    products = items
                    break
            except:
                continue

        # 保存商品信息
        for p in products:
            text_lower = p['text'].lower()
            is_ring = '戒指' in text_lower or 'ring' in text_lower or '触控' in text_lower or '手势' in text_lower

            all_data["products"].append({
                "platform": "淘宝",
                "keyword": keyword,
                "title": p['text'][:200],
                "is_ring_related": is_ring
            })

        # 点击第一个商品
        if products:
            try:
                print("\n🔍 进入商品详情页...")

                links = browser.page.query_selector_all("a[href*='item.taobao.com'], a[href*='detail.taobao.com']")
                if links:
                    href = links[0].get_attribute("href")
                    if href:
                        print(f"   正在访问: {href[:80]}...")
                        browser.page.goto(href, wait_until="domcontentloaded")
                        time.sleep(5)  # 增加等待时间

                        print(f"   页面标题: {browser.get_title()}")
                        browser.screenshot(f"taobao_detail_{idx}.png")

                        # 滚动页面
                        print("   开始滚动页面...")
                        browser.scroll_to_bottom(slow=True, max_scrolls=15)
                        time.sleep(3)

                        # 尝试点击评价标签
                        print("   尝试点击评价标签...")
                        review_tab_selectors = [
                            "a:has-text('评价')",
                            "a:has-text('评论')",
                            "[data-tab='reviews']",
                            "li:has-text('评价')",
                            "span:has-text('评价')",
                            "div:has-text('评价')"
                        ]
                        clicked = False
                        for tab in review_tab_selectors:
                            try:
                                elem = browser.page.query_selector(tab)
                                if elem:
                                    print(f"   找到评价标签: {tab}")
                                    browser.page.click(tab, timeout=3000)
                                    time.sleep(3)
                                    clicked = True
                                    break
                            except:
                                continue

                        if not clicked:
                            print("   未找到评价标签，尝试直接提取...")

                        # 再次滚动确保评价加载
                        print("   继续滚动加载评价...")
                        browser.scroll_to_bottom(slow=True, max_scrolls=10)
                        time.sleep(3)

                        # 提取用户反馈
                        print("   提取用户反馈...")
                        feedbacks = extract_all_user_feedback(browser)
                        for f in feedbacks:
                            all_data["feedbacks"].append({
                                "platform": "淘宝",
                                "product": keyword,
                                "content": f.get("text", "")
                            })

                        # 提取商品规格
                        specs = extract_product_info(browser)
                        for s in specs:
                            all_data["specs"].append({
                                "platform": "淘宝",
                                "product": keyword,
                                "type": s.get("type", ""),
                                "content": s.get("text", "")
                            })

                        print(f"✓ 收集到 {len(feedbacks)} 条反馈")

                        # 返回
                        browser.page.go_back()
                        time.sleep(3)

            except Exception as e:
                print(f"⚠️ 详情页处理失败: {e}")
                import traceback
                traceback.print_exc()

    return all_data


def scrape_jd_products(browser, keywords, wait_seconds=90):
    """爬取京东商品和用户反馈"""
    print("\n" + "=" * 70)
    print("京东 AI眼镜 爬取")
    print("=" * 70)

    import urllib.parse

    all_data = {
        "products": [],
        "feedbacks": [],
        "specs": []
    }

    for idx, keyword in enumerate(keywords[:3]):
        print(f"\n{'='*70}")
        print(f"[{idx+1}/3] 搜索: {keyword}")
        print(f"{'='*70}")

        encoded = urllib.parse.quote(keyword)
        url = f"https://search.jd.com/Search?keyword={encoded}&enc=utf-8"

        try:
            browser.navigate(url, wait_until="domcontentloaded")
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ 导航失败: {e}")
            continue

        # 首次等待登录
        if idx == 0:
            browser.wait_for_login(wait_seconds)

        # 抓取商品列表
        selectors = [
            ".gl-item",
            ".gl-warp .gl-item",
            "[class*='product']",
            "[data-sku]",
            "li[class*='item']"
        ]

        products = []
        for selector in selectors:
            try:
                items = browser.scrape_all_elements(selector, max_items=20)
                if items:
                    print(f"✓ 找到 {len(items)} 个元素")
                    products = items
                    break
            except:
                continue

        # 保存商品信息
        for p in products:
            text_lower = p['text'].lower()
            is_ring = '戒指' in text_lower or 'ring' in text_lower or '触控' in text_lower or '手势' in text_lower

            all_data["products"].append({
                "platform": "京东",
                "keyword": keyword,
                "title": p['text'][:200],
                "is_ring_related": is_ring
            })

        # 点击第一个商品
        if products:
            try:
                print("\n🔍 进入商品详情页...")

                links = browser.page.query_selector_all(".gl-item a, .p-name a")
                if links:
                    href = links[0].get_attribute("href")
                    if href:
                        if href.startswith('/'):
                            href = "https://item.jd.com" + href

                        print(f"   正在访问: {href[:80]}...")
                        browser.page.goto(href, wait_until="domcontentloaded")
                        time.sleep(5)

                        print(f"   页面标题: {browser.get_title()}")
                        browser.screenshot(f"jd_detail_{idx}.png")

                        # 滚动页面
                        print("   开始滚动页面...")
                        browser.scroll_to_bottom(slow=True, max_scrolls=15)
                        time.sleep(3)

                        # 尝试点击评价标签
                        print("   尝试点击评价标签...")
                        review_tab_selectors = [
                            "a:has-text('评价')",
                            "a:has-text('商品评价')",
                            ".tab-item:has-text('评价')",
                            "#detail-tab-2",
                            "li:has-text('评价')",
                            "div:has-text('评价')"
                        ]
                        clicked = False
                        for tab in review_tab_selectors:
                            try:
                                elem = browser.page.query_selector(tab)
                                if elem:
                                    print(f"   找到评价标签: {tab}")
                                    browser.page.click(tab, timeout=3000)
                                    time.sleep(3)
                                    clicked = True
                                    break
                            except:
                                continue

                        if not clicked:
                            print("   未找到评价标签，尝试直接提取...")

                        # 再次滚动确保评价加载
                        print("   继续滚动加载评价...")
                        browser.scroll_to_bottom(slow=True, max_scrolls=10)
                        time.sleep(3)

                        # 提取用户反馈
                        print("   提取用户反馈...")
                        feedbacks = extract_all_user_feedback(browser)
                        for f in feedbacks:
                            all_data["feedbacks"].append({
                                "platform": "京东",
                                "product": keyword,
                                "content": f.get("text", "")
                            })

                        # 提取商品规格
                        specs = extract_product_info(browser)
                        for s in specs:
                            all_data["specs"].append({
                                "platform": "京东",
                                "product": keyword,
                                "type": s.get("type", ""),
                                "content": s.get("text", "")
                            })

                        print(f"✓ 收集到 {len(feedbacks)} 条反馈")

                        # 返回
                        browser.page.go_back()
                        time.sleep(3)

            except Exception as e:
                print(f"⚠️ 详情页处理失败: {e}")
                import traceback
                traceback.print_exc()

    return all_data


def analyze_and_generate_report(taobao_data, jd_data):
    """分析数据并生成报告"""
    print("\n" + "=" * 70)
    print("数据分析和报告生成")
    print("=" * 70)

    # 合并数据
    all_products = taobao_data.get("products", []) + jd_data.get("products", [])
    all_feedbacks = taobao_data.get("feedbacks", []) + jd_data.get("feedbacks", [])
    all_specs = taobao_data.get("specs", []) + jd_data.get("specs", [])

    # 分析
    analysis = {
        "total_products": len(all_products),
        "total_feedbacks": len(all_feedbacks),
        "total_specs": len(all_specs),
        "ring_related": sum(1 for p in all_products if p.get("is_ring_related")),
        "by_platform": {
            "淘宝": len(taobao_data.get("products", [])),
            "京东": len(jd_data.get("products", []))
        },
        "keywords_stats": {
            "戒指": 0, "ring": 0, "触控": 0, "手势": 0,
            "AR": 0, "Xreal": 0, "Rokid": 0, "雷鸟": 0,
            "Meta": 0, "智能": 0
        },
        "feedback_categories": {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "quality": 0,
            "comfort": 0,
            "battery": 0,
            "connection": 0,
            "price": 0
        }
    }

    # 统计关键词
    for p in all_products:
        title = p.get("title", "").lower()
        for kw in analysis["keywords_stats"]:
            if kw.lower() in title:
                analysis["keywords_stats"][kw] += 1

    # 分析反馈
    for f in all_feedbacks:
        content = f.get("content", "").lower()

        # 情感分析
        if any(w in content for w in ["好", "不错", "推荐", "满意", "喜欢", "棒", "清晰", "方便"]):
            analysis["feedback_categories"]["positive"] += 1
        elif any(w in content for w in ["差", "不好", "失望", "退货", "问题"]):
            analysis["feedback_categories"]["negative"] += 1
        else:
            analysis["feedback_categories"]["neutral"] += 1

        # 分类分析
        if any(w in content for w in ["质量", "做工", "材质"]):
            analysis["feedback_categories"]["quality"] += 1
        if any(w in content for w in ["舒适", "佩戴", "重量", "轻"]):
            analysis["feedback_categories"]["comfort"] += 1
        if any(w in content for w in ["续航", "电池", "电量", "充电"]):
            analysis["feedback_categories"]["battery"] += 1
        if any(w in content for w in ["连接", "蓝牙", "配对"]):
            analysis["feedback_categories"]["connection"] += 1
        if any(w in content for w in ["价格", "便宜", "贵", "性价比"]):
            analysis["feedback_categories"]["price"] += 1

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_text = f"""
{'='*70}
                    AI眼镜市场调研报告
{'='*70}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
一、数据概览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  搜索商品总数: {analysis['total_products']}
  收集反馈总数: {analysis['total_feedbacks']}
  商品规格信息: {analysis['total_specs']}
  戒指相关商品: {analysis['ring_related']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
二、平台分布
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  淘宝: {analysis['by_platform']['淘宝']} 个商品
  京东: {analysis['by_platform']['京东']} 个商品

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
三、品牌关键词统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for kw, count in sorted(analysis['keywords_stats'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            report_text += f"  {kw}: {count} 次\n"

    report_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
四、用户反馈分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  积极反馈: {analysis['feedback_categories']['positive']} 条
  消极反馈: {analysis['feedback_categories']['negative']} 条
  中性反馈: {analysis['feedback_categories']['neutral']} 条

  按类别统计:
  - 质量相关: {analysis['feedback_categories']['quality']} 条
  - 舒适度相关: {analysis['feedback_categories']['comfort']} 条
  - 续航相关: {analysis['feedback_categories']['battery']} 条
  - 连接相关: {analysis['feedback_categories']['connection']} 条
  - 价格相关: {analysis['feedback_categories']['price']} 条
"""

    total_fb = sum([analysis['feedback_categories']['positive'],
                   analysis['feedback_categories']['negative'],
                   analysis['feedback_categories']['neutral']])
    if total_fb > 0:
        positive_rate = analysis['feedback_categories']['positive'] / total_fb * 100
        report_text += f"\n  好评率: {positive_rate:.1f}%\n"

    report_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
五、商品示例
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for i, p in enumerate(all_products[:10], 1):
        ring_mark = "🔴 戒指相关" if p.get('is_ring_related') else "  "
        title = p.get('title', '')[:80]
        report_text += f"{ring_mark} [{i}] {title}...\n"
        report_text += f"      来源: {p.get('platform', '')} | 搜索: {p.get('keyword', '')}\n\n"

    report_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
六、用户反馈精选
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # 去重反馈
    seen = set()
    unique_feedbacks = []
    for f in all_feedbacks:
        key = f.get('content', '')[:50]
        if key not in seen:
            seen.add(key)
            unique_feedbacks.append(f)

    for i, f in enumerate(unique_feedbacks[:15], 1):
        content = f.get('content', '')[:120]
        platform = f.get('platform', '')
        report_text += f"[{i}] [{platform}] {content}...\n\n"

    # 保存文件
    text_file = f"ai_glasses_report_{timestamp}.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(report_text)

    json_file = f"ai_glasses_data_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "analysis": analysis,
            "products": all_products,
            "feedbacks": all_feedbacks[:50],
            "specs": all_specs[:30]
        }, f, ensure_ascii=False, indent=2)

    # 打印报告
    print(report_text)
    print(f"\n✓ 文本报告: {text_file}")
    print(f"✓ 数据文件: {json_file}")

    return text_file, json_file


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("       AI眼镜市场调研 - 用户反馈爬取 (V3)")
    print("=" * 70)

    browser = ChromeAutomation(headless=False)

    taobao_data = {"products": [], "feedbacks": [], "specs": []}
    jd_data = {"products": [], "feedbacks": [], "specs": []}

    # 爬取淘宝
    try:
        print("\n开始爬取淘宝...")
        taobao_data = scrape_taobao_products(browser, KEYWORDS, wait_seconds=120)
    except Exception as e:
        print(f"淘宝爬取异常: {e}")

    # 爬取京东
    try:
        print("\n开始爬取京东...")
        jd_data = scrape_jd_products(browser, KEYWORDS, wait_seconds=90)
    except Exception as e:
        print(f"京东爬取异常: {e}")

    # 分析和报告
    text_file, json_file = analyze_and_generate_report(taobao_data, jd_data)

    browser.screenshot("ai_glasses_final.png")

    print(f"\n{'='*70}")
    print("爬取完成！")
    print(f"{'='*70}")

    print("\n浏览器保持打开 10 秒...")
    time.sleep(10)
    browser.close()


if __name__ == "__main__":
    main()
