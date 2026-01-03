#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Trending Analyzer - 微信热搜分析器

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
class TrendingTopic:
    """微信热搜话题数据模型"""
    rank: int
    title: str
    url: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WeChatTrendingConfig:
    """配置参数"""
    api_key: str = ""
    api_url: str = "https://apis.tianapi.com/wxhottopic/index"
    limit: int = 10
    keyword: Optional[str] = None
    include_analysis: bool = True
    timeout: int = 10
    max_retries: int = 3


class WeChatTrendingAnalyzer:
    """微信热搜分析器核心类"""

    def __init__(self, config: WeChatTrendingConfig = None):
        """初始化分析器"""
        self.config = config or WeChatTrendingConfig()
        self.update_time = None
        self.topics: List[TrendingTopic] = []

    def fetch_trending(self) -> List[Dict]:
        """
        从天行API获取微信热搜榜单

        Returns:
            List[Dict]: 热搜榜单原始数据

        Raises:
            Exception: API调用失败时抛出异常
        """
        api_key = os.environ.get("TIANAPI_KEY") or self.config.api_key
        if not api_key:
            raise ValueError("缺少 TIANAPI_KEY")
        params = {"key": api_key}

        for attempt in range(self.config.max_retries):
            try:
                print(f"📡 正在获取微信热搜... (尝试 {attempt + 1}/{self.config.max_retries})")

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
                    trending_list = result.get('list', [])
                    self.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    print(f"✅ 成功获取 {len(trending_list)} 条热搜")
                    return trending_list

                else:
                    error_msg = data.get('msg', 'Unknown error')
                    raise Exception(f"API错误: {error_msg}")

            except requests.Timeout:
                print(f"⚠️ 请求超时 (尝试 {attempt + 1})")
                if attempt == self.config.max_retries - 1:
                    raise Exception("获取热搜失败: 请求超时")

            except requests.RequestException as e:
                print(f"⚠️ 网络错误: {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"获取热搜失败: {str(e)}")

            except Exception as e:
                raise Exception(f"获取热搜失败: {str(e)}")

        raise Exception("获取热搜失败: 超过最大重试次数")

    def parse_topics(self, raw_data: List[Dict]) -> List[TrendingTopic]:
        """
        解析原始热搜数据

        Args:
            raw_data: API返回的原始数据

        Returns:
            List[TrendingTopic]: 解析后的热搜话题列表
        """
        topics = []

        for item in raw_data:
            # 微信热搜API返回的数据格式：word和index
            title = item.get('word', '')
            index = item.get('index', 0)

            if not title:
                continue

            # 生成微信搜索URL（编码中文）
            encoded_title = quote(title)
            url = f"https://weixin.sogou.com/weixin?type=2&query={encoded_title}"

            topic = TrendingTopic(
                rank=index + 1,  # index从0开始，rank从1开始
                title=title,
                url=url
            )
            topics.append(topic)

        print(f"📋 解析完成: {len(topics)} 条热搜")
        return topics

    def filter_topics(self, topics: List[TrendingTopic]) -> List[TrendingTopic]:
        """
        根据配置筛选话题

        Args:
            topics: 所有话题列表

        Returns:
            List[TrendingTopic]: 筛选后的话题列表
        """
        filtered = topics

        # 关键词筛选
        if self.config.keyword:
            keyword = self.config.keyword.lower()
            filtered = [
                t for t in filtered
                if keyword in t.title.lower()
            ]
            print(f"🔍 关键词筛选 '{self.config.keyword}': {len(filtered)} 条结果")

        # 数量限制
        filtered = filtered[:self.config.limit]
        print(f"✅ 筛选完成: {len(filtered)} 条话题")

        return filtered

    def search_topic_details(self, topic: TrendingTopic) -> Dict[str, Any]:
        """
        使用15-web-search-G搜索话题详细信息

        Args:
            topic: 热搜话题

        Returns:
            Dict: 话题详细信息
        """
        try:
            # 15-web-search-G skill的路径
            web_search_path = "C:/Users/bigbao/.codex/skills/15-web-search-G"
            cli_path = os.path.join(web_search_path, "cli.py")

            if not os.path.exists(cli_path):
                return {
                    "summary": f"关于 \"{topic.title}\" 的搜索暂时失败",
                    "background": "15-web-search-G skill未安装",
                    "key_points": [],
                    "sources": []
                }

            # 构建搜索查询
            search_query = f"{topic.title} 最新消息 背景 新闻"

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
                summary = lines[0] if lines else f"{topic.title}"

                return {
                    "summary": summary[:200] if len(summary) > 200 else summary,
                    "background": "详见搜索结果",
                    "key_points": lines[1:4] if len(lines) > 1 else [],
                    "sources": ["15-web-search-G"]
                }
            else:
                return {
                    "summary": f"关于 \"{topic.title}\" 的搜索暂时失败",
                    "background": "搜索服务暂不可用",
                    "key_points": [],
                    "sources": []
                }

        except subprocess.TimeoutExpired:
            return {
                "summary": f"关于 \"{topic.title}\" 的搜索超时",
                "background": "搜索服务超时",
                "key_points": [],
                "sources": []
            }
        except Exception as e:
            return {
                "summary": f"关于 \"{topic.title}\" 的搜索暂时失败",
                "background": "搜索服务暂不可用",
                "key_points": [],
                "sources": []
            }

    def enrich_topics(self, topics: List[TrendingTopic]) -> None:
        """
        为每个话题搜索详细信息

        Args:
            topics: 话题列表（会直接修改）
        """
        if not self.config.include_analysis:
            return

        print(f"\n🔍 正在搜索话题详细信息...")

        for i, topic in enumerate(topics, 1):
            print(f"[{i}/{len(topics)}]   🔎 正在搜索: {topic.title}")

            try:
                details = self.search_topic_details(topic)
                topic.details = details
                print(f"  ✅ 搜索完成")
            except Exception as e:
                print(f"  ⚠️ 搜索失败: {str(e)[:100]}")
                topic.details = {
                    "summary": f"关于 \"{topic.title}\" 的搜索暂时失败",
                    "background": "搜索服务暂不可用",
                    "key_points": [],
                    "sources": []
                }

    def generate_report(self, topics: List[TrendingTopic]) -> str:
        """
        生成Markdown格式的热搜报告

        Args:
            topics: 话题列表

        Returns:
            str: Markdown格式报告
        """
        report_lines = []

        # 标题
        report_lines.append("# 💬 微信热搜榜")
        report_lines.append("")
        report_lines.append(f"**更新时间**: {self.update_time}")
        report_lines.append(f"**热搜数量**: {len(topics)} 条")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 热搜话题
        report_lines.append(f"## 🔥 Top {len(topics)} 热搜话题")
        report_lines.append("")

        for topic in topics:
            # 话题标题
            report_lines.append(f"### {topic.rank}. {topic.title}")
            report_lines.append("")

            # 如果有详细信息
            if topic.details and self.config.include_analysis:
                summary = topic.details.get('summary', '')
                background = topic.details.get('background', '')

                if summary:
                    report_lines.append(f"**话题概述**: {summary}")
                    report_lines.append("")

                if background and background != "详见搜索结果":
                    report_lines.append(f"**背景信息**: {background}")
                    report_lines.append("")

                key_points = topic.details.get('key_points', [])
                if key_points:
                    report_lines.append("**关键要点**:")
                    for point in key_points[:3]:
                        report_lines.append(f"- {point}")
                    report_lines.append("")

            # 微信搜索链接
            report_lines.append(f"**🔗 微信搜索**: [{topic.title}]({topic.url})")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 数据说明
        report_lines.append("## 📊 数据说明")
        report_lines.append("")
        report_lines.append("- **数据源**: 天行API (微信热搜)")
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
            filename = f"wechat_trending_{timestamp}.md"

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
            print("🚀 开始微信热搜分析...\n")

            # 1. 获取热搜数据
            raw_data = self.fetch_trending()

            # 2. 解析数据
            self.topics = self.parse_topics(raw_data)

            # 3. 筛选话题
            filtered_topics = self.filter_topics(self.topics)

            # 4. 搜索详细信息
            self.enrich_topics(filtered_topics)

            # 5. 生成报告
            report = self.generate_report(filtered_topics)

            print("\n✅ 分析完成!\n")
            return report

        except Exception as e:
            error_report = f"# ❌ 错误\n\n❌ 分析失败: {str(e)}\n"
            print(f"\n❌ 分析失败: {str(e)}\n")
            return error_report


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='微信热搜分析器')
    parser.add_argument('--limit', type=int, default=10, help='返回热搜数量 (默认: 10)')
    parser.add_argument('--keyword', type=str, help='关键词筛选')
    parser.add_argument('--no-analysis', action='store_true', help='不包含详细分析')
    parser.add_argument('--output', type=str, help='输出文件路径')

    args = parser.parse_args()

    # 创建配置
    config = WeChatTrendingConfig(
        limit=args.limit,
        keyword=args.keyword,
        include_analysis=not args.no_analysis
    )

    # 执行分析
    analyzer = WeChatTrendingAnalyzer(config)
    report = analyzer.analyze()

    # 输出报告
    print(report)

    # 保存报告
    output_file = analyzer.save_report(report, args.output)
    print(f"📄 报告已保存至: {output_file}")


if __name__ == "__main__":
    main()
