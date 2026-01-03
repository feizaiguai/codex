#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hacker News趋势分析器

基于Hacker News官方API，自动抓取热门技术讨论和新闻。

功能特点:
- 获取Hacker News首页热门故事
- 使用15-web-search-G搜索背景信息（可选）
- 支持自定义返回数量
- 完全免费的官方API

作者: Claude Code Skills Team
版本: 1.0.0
许可: MIT
"""

import os
import sys
import json
import argparse
import subprocess
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class HNStoryItem:
    """Hacker News故事数据模型"""
    rank: int
    title: str
    url: str
    score: int
    by: str
    time: str
    comments: int
    story_id: int
    hn_url: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HNConfig:
    """Hacker News API配置"""
    api_base: str = "https://hacker-news.firebaseio.com/v0"
    timeout: int = 10
    top_stories_endpoint: str = "/topstories.json"
    item_endpoint: str = "/item/{id}.json"


class HackerNewsAnalyzer:
    """Hacker News趋势分析器"""

    def __init__(self, config: Optional[HNConfig] = None):
        """
        初始化分析器

        Args:
            config: 可选的配置对象，如果未提供则使用默认配置
        """
        self.config = config or HNConfig()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
        })

    def fetch_top_story_ids(self, limit: int = 10) -> List[int]:
        """
        获取热门故事ID列表

        Args:
            limit: 返回的故事数量

        Returns:
            故事ID列表
        """
        url = f"{self.config.api_base}{self.config.top_stories_endpoint}"

        try:
            response = self.session.get(
                url,
                timeout=self.config.timeout,
                verify=False
            )
            response.raise_for_status()

            all_ids = response.json()
            return all_ids[:limit]

        except Exception as e:
            print(f"❌ 获取故事ID失败: {e}")
            return []

    def fetch_story_details(self, story_id: int) -> Optional[Dict[str, Any]]:
        """
        获取单个故事的详细信息

        Args:
            story_id: 故事ID

        Returns:
            故事详情字典，失败返回None
        """
        url = f"{self.config.api_base}{self.config.item_endpoint.format(id=story_id)}"

        try:
            response = self.session.get(
                url,
                timeout=self.config.timeout,
                verify=False
            )
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"⚠️ 获取故事 {story_id} 详情失败: {e}")
            return None

    def parse_story(self, story_data: Dict[str, Any], rank: int) -> Optional[HNStoryItem]:
        """
        解析故事数据

        Args:
            story_data: API返回的原始故事数据
            rank: 排名

        Returns:
            解析后的HNStoryItem对象
        """
        try:
            # 转换Unix时间戳
            timestamp = story_data.get('time', 0)
            time_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            story_id = story_data.get('id', 0)

            return HNStoryItem(
                rank=rank,
                title=story_data.get('title', ''),
                url=story_data.get('url', ''),
                score=story_data.get('score', 0),
                by=story_data.get('by', 'unknown'),
                time=time_str,
                comments=story_data.get('descendants', 0),
                story_id=story_id,
                hn_url=f"https://news.ycombinator.com/item?id={story_id}",
                details={}
            )

        except Exception as e:
            print(f"⚠️ 解析故事数据失败: {e}")
            return None

    def search_background(self, story: HNStoryItem) -> Dict[str, Any]:
        """
        使用15-web-search-G搜索故事背景信息

        Args:
            story: 故事对象

        Returns:
            背景信息字典
        """
        try:
            skills_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            web_search_dir = os.path.join(skills_dir, "15-web-search-G")
            handler_path = os.path.join(web_search_dir, "handler.py")

            if not os.path.exists(handler_path):
                return {"error": "15-web-search-G skill未安装"}

            # 构建搜索查询
            query = f"{story.title}"

            # 调用15-web-search-G
            cmd = [
                sys.executable,
                handler_path,
                "--query", query,
                "--mode", "fast",
                "--max-results", "3"
            ]

            result = subprocess.run(
                cmd,
                cwd=web_search_dir,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )

            if result.returncode == 0:
                # 解析输出
                output = result.stdout.strip()
                if output:
                    return {
                        "success": True,
                        "background": output[:500]  # 限制长度
                    }

            return {"error": "搜索失败"}

        except subprocess.TimeoutExpired:
            return {"error": "搜索超时"}
        except Exception as e:
            return {"error": f"搜索异常: {str(e)}"}

    def analyze(self, limit: int = 10, no_analysis: bool = False) -> List[HNStoryItem]:
        """
        执行完整分析流程

        Args:
            limit: 返回的故事数量
            no_analysis: 是否跳过背景信息搜索

        Returns:
            故事列表
        """
        print(f"📡 正在获取Hacker News前{limit}个热门故事...")

        # 1. 获取故事ID
        story_ids = self.fetch_top_story_ids(limit)

        if not story_ids:
            print("❌ 未获取到任何故事ID")
            return []

        print(f"✅ 获取到 {len(story_ids)} 个故事ID")

        # 2. 获取故事详情
        stories = []
        for rank, story_id in enumerate(story_ids, 1):
            print(f"📖 [{rank}/{len(story_ids)}] 获取故事详情...")

            story_data = self.fetch_story_details(story_id)
            if not story_data:
                continue

            story = self.parse_story(story_data, rank)
            if not story:
                continue

            # 3. 搜索背景信息（可选）
            if not no_analysis:
                print(f"🔍 [{rank}/{len(story_ids)}] 搜索背景信息: {story.title[:50]}...")
                background = self.search_background(story)
                story.details['background'] = background

            stories.append(story)

        print(f"\n✅ 成功分析 {len(stories)} 个故事")
        return stories

    def format_markdown_report(self, stories: List[HNStoryItem], no_analysis: bool = False) -> str:
        """
        生成Markdown格式报告

        Args:
            stories: 故事列表
            no_analysis: 是否包含详细分析

        Returns:
            Markdown格式的报告
        """
        report_lines = [
            "# 🟠 Hacker News热门故事",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**故事数量**: {len(stories)} 个",
            "",
            "---",
            ""
        ]

        for story in stories:
            report_lines.extend([
                f"## {story.rank}. {story.title}",
                "",
                f"- **分数**: {story.score} 分",
                f"- **作者**: {story.by}",
                f"- **时间**: {story.time}",
                f"- **评论数**: {story.comments}",
                f"- **链接**: {story.url or story.hn_url}",
                f"- **HN讨论**: {story.hn_url}",
                ""
            ])

            # 添加背景信息
            if not no_analysis and story.details.get('background'):
                bg = story.details['background']
                if isinstance(bg, dict) and bg.get('success'):
                    report_lines.extend([
                        "**背景信息**:",
                        f"{bg.get('background', '')}",
                        ""
                    ])

            report_lines.append("---")
            report_lines.append("")

        # 添加说明
        report_lines.extend([
            "## 📝 说明",
            "",
            "- 数据来源: Hacker News官方API",
            "- 备用API: Algolia HN Search、HN RSS",
            "- 触发关键词: \"HackerNews热搜\"、\"HN趋势\"",
            ""
        ])

        return "\n".join(report_lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Hacker News趋势分析器")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="返回的故事数量（默认: 10）"
    )
    parser.add_argument(
        "--no-analysis",
        action="store_true",
        help="跳过背景信息搜索（快速模式）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径（可选）"
    )

    args = parser.parse_args()

    # 创建分析器
    analyzer = HackerNewsAnalyzer()

    # 执行分析
    stories = analyzer.analyze(limit=args.limit, no_analysis=args.no_analysis)

    if not stories:
        print("\n❌ 未获取到任何故事")
        sys.exit(1)

    # 生成报告
    report = analyzer.format_markdown_report(stories, no_analysis=args.no_analysis)

    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 报告已保存到: {args.output}")
    else:
        print("\n" + report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
