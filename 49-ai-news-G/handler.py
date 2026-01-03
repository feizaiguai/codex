#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI News Analyzer - AI资讯分析器

Author: Claude Code Skills Team
Version: 1.0.0
License: MIT
"""

import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import urllib3
import subprocess
import os
from urllib.parse import quote

# 禁用SSL警告（解决Windows SSL验证问题）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class AINewsItem:
    """AI资讯数据模型"""
    rank: int
    title: str
    description: str
    source: str
    url: str
    publish_time: str
    pic_url: str = ""
    news_id: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AINewsConfig:
    """配置参数"""
    api_key: str = ""
    api_url: str = "https://apis.tianapi.com/ai/index"
    limit: int = 10
    keyword: Optional[str] = None
    include_analysis: bool = True
    timeout: int = 10
    max_retries: int = 3


class AINewsAnalyzer:
    """AI资讯分析器核心类"""

    def __init__(self, config: AINewsConfig = None):
        """初始化分析器"""
        self.config = config or AINewsConfig()
        self.update_time = None
        self.news_items: List[AINewsItem] = []

    def fetch_news(self) -> List[Dict]:
        """
        从天行API获取AI资讯

        Returns:
            List[Dict]: AI资讯原始数据

        Raises:
            Exception: API调用失败时抛出异常
        """
        api_key = os.environ.get("TIANAPI_KEY") or self.config.api_key
        if not api_key:
            raise ValueError("缺少 TIANAPI_KEY")
        params = {"key": api_key}

        for attempt in range(self.config.max_retries):
            try:
                print(f"📡 正在获取AI资讯... (尝试 {attempt + 1}/{self.config.max_retries})")

                # 添加请求头和禁用SSL验证
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                }

                response = requests.get(
                    self.config.api_url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                    verify=False  # 禁用SSL验证解决Windows SSL问题
                )
                response.raise_for_status()
                data = response.json()

                # 检查API响应状态
                if data.get('code') == 200:
                    result = data.get('result', {})
                    news_list = result.get('newslist', [])
                    self.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    print(f"✅ 成功获取 {len(news_list)} 条AI资讯")
                    return news_list

                else:
                    error_msg = data.get('msg', 'Unknown error')
                    raise Exception(f"API错误: {error_msg}")

            except requests.Timeout:
                print(f"⚠️ 请求超时 (尝试 {attempt + 1})")
                if attempt == self.config.max_retries - 1:
                    raise Exception("获取AI资讯失败: 请求超时")

            except requests.RequestException as e:
                print(f"⚠️ 网络错误: {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"获取AI资讯失败: {str(e)}")

            except Exception as e:
                raise Exception(f"获取AI资讯失败: {str(e)}")

        raise Exception("获取AI资讯失败: 超过最大重试次数")

    def parse_news(self, raw_data: List[Dict]) -> List[AINewsItem]:
        """
        解析原始AI资讯数据

        Args:
            raw_data: API返回的原始数据

        Returns:
            List[AINewsItem]: 解析后的AI资讯列表
        """
        news_items = []

        for index, item in enumerate(raw_data, start=1):
            # AI资讯API返回的数据格式
            title = item.get('title', '')
            description = item.get('description', '')
            source = item.get('source', '')
            url = item.get('url', '')
            ctime = item.get('ctime', '')
            pic_url = item.get('picUrl', '')
            news_id = item.get('id', '')

            if not title:
                continue

            news_item = AINewsItem(
                rank=index,
                title=title,
                description=description,
                source=source,
                url=url,
                publish_time=ctime,
                pic_url=pic_url,
                news_id=news_id
            )
            news_items.append(news_item)

        print(f"📋 解析完成: {len(news_items)} 条AI资讯")
        return news_items

    def filter_news(self, news_items: List[AINewsItem]) -> List[AINewsItem]:
        """
        根据配置筛选资讯

        Args:
            news_items: 所有资讯列表

        Returns:
            List[AINewsItem]: 筛选后的资讯列表
        """
        filtered = news_items

        # 关键词筛选
        if self.config.keyword:
            keyword = self.config.keyword.lower()
            filtered = [
                item for item in filtered
                if keyword in item.title.lower() or keyword in item.description.lower()
            ]
            print(f"🔍 关键词筛选 '{self.config.keyword}': {len(filtered)} 条结果")

        # 数量限制
        filtered = filtered[:self.config.limit]
        print(f"✅ 筛选完成: {len(filtered)} 条资讯")

        return filtered

    def search_news_details(self, news_item: AINewsItem) -> Dict[str, Any]:
        """
        使用15-web-search-G搜索资讯详细信息

        Args:
            news_item: AI资讯条目

        Returns:
            Dict: 资讯详细信息
        """
        try:
            # 15-web-search-G skill的路径
            web_search_path = "C:/Users/bigbao/.codex/skills/15-web-search-G"
            cli_path = os.path.join(web_search_path, "cli.py")

            if not os.path.exists(cli_path):
                return {
                    "summary": f"关于 \"{news_item.title}\" 的搜索暂时失败",
                    "background": "15-web-search-G skill未安装",
                    "key_points": [],
                    "sources": []
                }

            # 构建搜索查询（使用标题 + 关键词）
            search_query = f"{news_item.title} 详细 分析"

            # 调用15-web-search-G
            cmd = [
                "python", cli_path,
                search_query,
                "--mode", "auto",
                "--max-results", "10",
                "--time-range", "week",
                "--language", "zh",
                "--output", "markdown"
            ]

            result = subprocess.run(
                cmd,
                cwd=web_search_path,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='ignore'
            )

            if result.returncode == 0 and result.stdout:
                # 解析搜索结果（简单提取关键信息）
                output = result.stdout

                # 提取摘要（取第一段非空内容）
                lines = [line.strip() for line in output.split('\n') if line.strip()]
                summary = lines[0] if lines else news_item.description

                return {
                    "summary": summary[:200] if len(summary) > 200 else summary,
                    "background": "详见搜索结果",
                    "key_points": lines[1:4] if len(lines) > 1 else [],
                    "sources": ["15-web-search-G"]
                }
            else:
                return {
                    "summary": news_item.description,
                    "background": "搜索服务暂不可用",
                    "key_points": [],
                    "sources": []
                }

        except subprocess.TimeoutExpired:
            return {
                "summary": news_item.description,
                "background": "搜索服务超时",
                "key_points": [],
                "sources": []
            }
        except Exception as e:
            return {
                "summary": news_item.description,
                "background": "搜索服务暂不可用",
                "key_points": [],
                "sources": []
            }

    def enrich_news(self, news_items: List[AINewsItem]) -> None:
        """
        为每条资讯搜索详细信息

        Args:
            news_items: 资讯列表（会直接修改）
        """
        if not self.config.include_analysis:
            return

        print(f"\n🔍 正在搜索资讯详细信息...")

        for i, news_item in enumerate(news_items, 1):
            print(f"[{i}/{len(news_items)}] 🔎 正在搜索: {news_item.title}")

            try:
                details = self.search_news_details(news_item)
                news_item.details = details
                print(f"  ✅ 搜索完成")
            except Exception as e:
                print(f"  ⚠️ 搜索失败: {str(e)[:100]}")
                news_item.details = {
                    "summary": news_item.description,
                    "background": "搜索服务暂不可用",
                    "key_points": [],
                    "sources": []
                }

    def generate_report(self, news_items: List[AINewsItem]) -> str:
        """
        生成Markdown格式的AI资讯报告

        Args:
            news_items: 资讯列表

        Returns:
            str: Markdown格式报告
        """
        report_lines = []

        # 标题
        report_lines.append("# 🤖 AI资讯速递")
        report_lines.append("")
        report_lines.append(f"**更新时间**: {self.update_time}")
        report_lines.append(f"**资讯数量**: {len(news_items)} 条")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # AI资讯条目
        report_lines.append(f"## 📰 Top {len(news_items)} AI资讯")
        report_lines.append("")

        for news_item in news_items:
            # 资讯标题
            report_lines.append(f"### {news_item.rank}. {news_item.title}")
            report_lines.append("")

            # 基本信息
            report_lines.append(f"**📅 发布时间**: {news_item.publish_time}")
            report_lines.append(f"**📌 来源**: {news_item.source}")
            report_lines.append("")

            # 资讯描述
            if news_item.description:
                report_lines.append(f"**📝 内容概述**: {news_item.description}")
                report_lines.append("")

            # 如果有详细信息
            if news_item.details and self.config.include_analysis:
                summary = news_item.details.get('summary', '')
                background = news_item.details.get('background', '')

                if summary and summary != news_item.description:
                    report_lines.append(f"**💡 深度解读**: {summary}")
                    report_lines.append("")

                key_points = news_item.details.get('key_points', [])
                if key_points:
                    report_lines.append("**🔑 关键要点**:")
                    for point in key_points[:3]:
                        report_lines.append(f"- {point}")
                    report_lines.append("")

            # 原文链接
            report_lines.append(f"**🔗 原文链接**: [{news_item.title}]({news_item.url})")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 数据说明
        report_lines.append("## 📊 数据说明")
        report_lines.append("")
        report_lines.append("- **数据源**: 天行API (AI资讯)")
        report_lines.append("- **更新频率**: 实时更新")
        report_lines.append(f"- **数据时效**: {self.update_time}")
        report_lines.append("")

        return "\n".join(report_lines)

    def save_report(self, report: str, filename: str = None) -> str:
        """
        保存报告到文件

        Args:
            report: 报告内容
            filename: 文件名（可选）

        Returns:
            str: 保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_news_{timestamp}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        return filename

    def analyze(self) -> str:
        """
        执行完整的分析流程

        Returns:
            str: Markdown格式的分析报告
        """
        try:
            print("🚀 开始AI资讯分析...\n")

            # 1. 获取AI资讯数据
            raw_data = self.fetch_news()

            # 2. 解析数据
            self.news_items = self.parse_news(raw_data)

            # 3. 筛选资讯
            filtered_news = self.filter_news(self.news_items)

            # 4. 搜索详细信息
            self.enrich_news(filtered_news)

            # 5. 生成报告
            report = self.generate_report(filtered_news)

            print("\n✅ 分析完成!\n")
            return report

        except Exception as e:
            error_report = f"# ❌ 错误\n\n❌ 分析失败: {str(e)}\n"
            print(f"\n❌ 分析失败: {str(e)}\n")
            return error_report


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='AI资讯分析器')
    parser.add_argument('--limit', type=int, default=10, help='返回资讯数量 (默认: 10)')
    parser.add_argument('--keyword', type=str, help='关键词筛选')
    parser.add_argument('--no-analysis', action='store_true', help='不包含详细分析')
    parser.add_argument('--output', type=str, help='输出文件路径')

    args = parser.parse_args()

    # 创建配置
    config = AINewsConfig(
        limit=args.limit,
        keyword=args.keyword,
        include_analysis=not args.no_analysis
    )

    # 执行分析
    analyzer = AINewsAnalyzer(config)
    report = analyzer.analyze()

    # 输出报告
    print(report)

    # 保存报告
    output_file = analyzer.save_report(report, args.output)
    print(f"📄 报告已保存至: {output_file}")


if __name__ == "__main__":
    main()
