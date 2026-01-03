#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Hot Search Analyzer - 全网热搜分析器

从全平台抓取实时热搜榜单，并为每个话题搜索详细背景信息。

Author: Claude Code Skills Team
Version: 1.0.0
License: MIT
"""

import os
import requests
import json
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import urllib3
import subprocess
import os

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class HotTopic:
    """热搜话题数据模型"""
    rank: int
    title: str
    hotnum: str  # 热度值
    digest: str  # 摘要
    url: str
    mobilurl: str = ""
    tag: str = ""  # 标签
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkHotConfig:
    """配置参数"""
    api_key: str = ""
    api_url: str = "https://apis.tianapi.com/networkhot/index"
    limit: int = 10
    keyword: Optional[str] = None
    include_analysis: bool = True
    timeout: int = 10
    max_retries: int = 3


class NetworkHotAnalyzer:
    """全网热搜分析器核心类"""

    def __init__(self, config: NetworkHotConfig = None):
        """初始化分析器"""
        self.config = config or NetworkHotConfig()
        self.update_time = None
        self.hot_topics: List[HotTopic] = []

    def fetch_hot_topics(self) -> List[Dict]:
        """
        从天行API获取全网热搜

        Returns:
            List[Dict]: 热搜原始数据

        Raises:
            Exception: API调用失败时抛出异常
        """
        api_key = os.environ.get("TIANAPI_KEY") or self.config.api_key
        if not api_key:
            raise ValueError("缺少 TIANAPI_KEY")
        params = {"key": api_key}

        for attempt in range(self.config.max_retries):
            try:
                print(f"📡 正在获取全网热搜... (尝试 {attempt + 1}/{self.config.max_retries})")

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                }

                response = requests.get(
                    self.config.api_url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                    verify=False
                )

                if response.status_code == 200:
                    data = response.json()

                    if data.get('code') == 200:
                        newslist = data.get('result', {}).get('list', [])
                        print(f"✅ 成功获取 {len(newslist)} 个热搜话题")
                        self.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        return newslist
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"❌ API返回错误: {error_msg}")

                else:
                    print(f"❌ HTTP错误: {response.status_code}")

            except requests.exceptions.Timeout:
                print(f"⚠️ 请求超时")
            except requests.exceptions.ConnectionError:
                print(f"⚠️ 网络连接错误")
            except Exception as e:
                print(f"❌ 获取热搜失败: {str(e)}")

            if attempt < self.config.max_retries - 1:
                import time
                wait_time = 2 ** attempt
                print(f"⏳ {wait_time}秒后重试...")
                time.sleep(wait_time)

        raise Exception("获取全网热搜失败，已达最大重试次数")

    def parse_topic(self, topic_data: Dict, rank: int) -> Optional[HotTopic]:
        """
        解析单个热搜话题

        Args:
            topic_data: API返回的原始话题数据
            rank: 排名

        Returns:
            HotTopic对象或None
        """
        try:
            return HotTopic(
                rank=rank,
                title=topic_data.get('title', ''),
                hotnum=topic_data.get('hotnum', ''),
                digest=topic_data.get('digest', ''),
                url=topic_data.get('url', ''),
                mobilurl=topic_data.get('mobilurl', ''),
                tag=topic_data.get('tag', ''),
                details={}
            )
        except Exception as e:
            print(f"⚠️ 解析话题数据失败: {e}")
            return None

    def enrich_with_search(self, topic: HotTopic) -> bool:
        """
        使用15-web-search-G skill搜索话题背景信息

        Args:
            topic: 热搜话题对象

        Returns:
            bool: 是否成功获取背景信息
        """
        if not self.config.include_analysis:
            return False

        try:
            print(f"🔍 正在搜索话题背景: {topic.title[:30]}...")

            # 调用15-web-search-G skill
            search_query = f"{topic.title} 新闻 背景"
            cmd = [
                'python',
                os.path.join(os.path.dirname(__file__), '..', '15-web-search-G', 'handler.py'),
                '--mode', 'auto',
                '--query', search_query,
                '--max-results', '3'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )

            if result.returncode == 0:
                # 解析搜索结果
                output = result.stdout
                topic.details['search_result'] = output
                topic.details['has_background'] = True
                print(f"✅ 成功获取背景信息")
                return True
            else:
                print(f"⚠️ 搜索失败: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"⚠️ 搜索超时")
            return False
        except Exception as e:
            print(f"⚠️ 搜索背景信息时出错: {e}")
            return False

    def analyze(self) -> List[HotTopic]:
        """
        执行完整的分析流程

        Returns:
            List[HotTopic]: 热搜话题列表
        """
        # 1. 获取热搜数据
        topics_data = self.fetch_hot_topics()

        if not topics_data:
            print("❌ 未获取到热搜数据")
            return []

        # 2. 解析热搜话题
        self.hot_topics = []
        for rank, topic_data in enumerate(topics_data[:self.config.limit], 1):
            topic = self.parse_topic(topic_data, rank)
            if topic:
                # 3. 关键词筛选
                if self.config.keyword:
                    if self.config.keyword.lower() not in topic.title.lower():
                        continue

                self.hot_topics.append(topic)

        print(f"✅ 解析完成，共 {len(self.hot_topics)} 个热搜话题")

        # 4. 为每个话题搜索背景信息
        if self.config.include_analysis:
            print(f"\n🔍 开始搜索话题背景信息...")
            for i, topic in enumerate(self.hot_topics, 1):
                print(f"\n[{i}/{len(self.hot_topics)}] 处理中...")
                self.enrich_with_search(topic)

        return self.hot_topics

    def format_markdown_report(self) -> str:
        """
        生成Markdown格式的报告

        Returns:
            str: Markdown格式的报告
        """
        report_lines = [
            "# 全网热搜榜单",
            "",
            f"**更新时间**: {self.update_time}",
            f"**热搜数量**: {len(self.hot_topics)} 个",
            ""
        ]

        if self.config.keyword:
            report_lines.append(f"**筛选关键词**: {self.config.keyword}")
            report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

        # 生成每个热搜的详细信息
        for topic in self.hot_topics:
            # 热搜标题和基本信息
            report_lines.extend([
                f"## 🔥 TOP {topic.rank}: {topic.title}",
                "",
                f"- **热度指数**: {topic.hotnum}",
                f"- **话题链接**: {topic.url}",
            ])

            if topic.tag:
                report_lines.append(f"- **话题标签**: {topic.tag}")

            report_lines.append("")

            # 摘要
            if topic.digest:
                report_lines.extend([
                    "### 📝 话题摘要",
                    "",
                    topic.digest,
                    ""
                ])

            # 背景信息（如果有）
            if topic.details.get('has_background'):
                report_lines.extend([
                    "### 🔍 背景信息与深度分析",
                    "",
                    topic.details.get('search_result', ''),
                    ""
                ])

            report_lines.append("---")
            report_lines.append("")

        # 添加说明
        report_lines.extend([
            "## 📝 说明",
            "",
            "- 数据来源: 天行数据 - 全网热搜API",
            "- 更新频率: 实时更新",
            "- 覆盖平台: 微博、知乎、百度、抖音、B站等",
            "- 背景信息: 通过15-web-search-G skill自动搜索",
            ""
        ])

        return "\n".join(report_lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="全网热搜分析器")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="返回的热搜数量（默认: 10）"
    )
    parser.add_argument(
        "--keyword",
        type=str,
        help="关键词筛选（可选）"
    )
    parser.add_argument(
        "--no-analysis",
        action="store_true",
        help="不包含深度分析（更快）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径（可选）"
    )

    args = parser.parse_args()

    # 创建配置
    config = NetworkHotConfig(
        limit=args.limit,
        keyword=args.keyword,
        include_analysis=not args.no_analysis
    )

    # 创建分析器
    analyzer = NetworkHotAnalyzer(config)

    try:
        # 执行分析
        analyzer.analyze()

        # 生成报告
        report = analyzer.format_markdown_report()

        # 输出报告
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n✅ 报告已保存到: {args.output}")
        else:
            print("\n" + report)

        return 0

    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
