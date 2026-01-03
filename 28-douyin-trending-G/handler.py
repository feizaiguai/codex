#!/usr/bin/env python3
"""
Douyin Trending Analyzer - 抖音热搜分析器

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

# 禁用SSL警告（解决Windows SSL验证问题）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class TrendingTopic:
    """抖音热搜话题数据模型"""
    rank: int
    title: str
    hot_index: int
    label: str = ""
    url: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DouyinTrendingConfig:
    """配置参数"""
    api_key: str = ""
    api_url: str = "https://apis.tianapi.com/douyinhot/index"
    limit: int = 10
    keyword: Optional[str] = None
    include_analysis: bool = True
    timeout: int = 10
    max_retries: int = 3


class DouyinTrendingAnalyzer:
    """抖音热搜分析器核心类"""

    def __init__(self, config: DouyinTrendingConfig = None):
        """初始化分析器"""
        self.config = config or DouyinTrendingConfig()
        self.update_time = None
        self.topics: List[TrendingTopic] = []

    def fetch_trending(self) -> List[Dict]:
        """
        从天行API获取抖音热搜榜单

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
                print(f"📡 正在获取抖音热搜... (尝试 {attempt + 1}/{self.config.max_retries})")

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
        解析热搜数据

        Args:
            raw_data: API返回的原始数据

        Returns:
            List[TrendingTopic]: 解析后的热搜话题列表
        """
        topics = []

        for idx, item in enumerate(raw_data, 1):
            try:
                # 获取热搜标题
                title = item.get('word', '').strip()
                if not title:
                    continue

                # 获取热度指数
                hot_index = item.get('hotindex', 0)
                if isinstance(hot_index, str):
                    hot_index = int(hot_index) if hot_index.isdigit() else 0

                # 获取标签
                label_code = item.get('label', 0)
                label = self._get_label_name(label_code)

                # 构建抖音搜索URL（抖音搜索页面）
                # 注意：抖音的搜索URL格式为 https://www.douyin.com/search/{关键词}
                import urllib.parse
                encoded_title = urllib.parse.quote(title)
                url = f"https://www.douyin.com/search/{encoded_title}"

                topic = TrendingTopic(
                    rank=idx,
                    title=title,
                    hot_index=hot_index,
                    label=label,
                    url=url
                )
                topics.append(topic)

            except Exception as e:
                print(f"⚠️ 解析话题失败: {item.get('word', 'Unknown')} - {str(e)}")
                continue

        return topics

    def _get_label_name(self, label_code: int) -> str:
        """转换标签代码为中文名称"""
        label_map = {
            0: '',
            1: '新',
            2: '热',
            3: '爆',
            4: '沸',
            5: '推荐',
            8: '视频',
            9: '挑战',
            16: '话题',
            17: '音乐'
        }
        return label_map.get(label_code, '')

    def filter_topics(self, topics: List[TrendingTopic]) -> List[TrendingTopic]:
        """
        根据配置筛选话题

        Args:
            topics: 话题列表

        Returns:
            List[TrendingTopic]: 筛选后的话题列表
        """
        filtered = topics

        # 关键词筛选
        if self.config.keyword:
            keyword_lower = self.config.keyword.lower()
            filtered = [
                t for t in filtered
                if keyword_lower in t.title.lower()
            ]
            print(f"🔍 关键词筛选 '{self.config.keyword}': {len(filtered)} 条匹配")

        # 限制数量
        filtered = filtered[:self.config.limit]

        return filtered

    def enrich_topic_details(self, topic: TrendingTopic) -> None:
        """
        使用15-web-search-G skill为话题添加详细信息

        调用15-web-search-G的Python CLI进行网络搜索

        Args:
            topic: 话题对象
        """
        if not self.config.include_analysis:
            return

        print(f"  🔎 正在搜索: {topic.title}")

        # 构建搜索查询
        search_query = f"{topic.title} 抖音 最新消息 背景 新闻"

        try:
            import subprocess
            import os

            # 构建15-web-search-G命令
            web_search_dir = "C:/Users/bigbao/.codex/skills/15-web-search-G"

            # 检查15-web-search-G是否存在
            if not os.path.exists(web_search_dir):
                print(f"  ⚠️ 15-web-search-G skill未找到，跳过详细搜索")
                topic.details = {
                    'summary': f'"{topic.title}" - 详细搜索功能需要15-web-search-G skill',
                    'background': '请安装15-web-search-G skill以获取详细背景信息',
                    'key_points': ['基本热搜信息已显示'],
                    'sources': []
                }
                return

            # 构建命令
            cmd = [
                "python",
                f"{web_search_dir}/cli.py",
                search_query,
                "--mode", "auto",
                "--max-results", "10",
                "--time-range", "week",
                "--language", "zh",
                "--output", "markdown"
            ]

            # 执行搜索（超时15秒）
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                cwd=web_search_dir
            )

            if result.returncode == 0:
                # 解析搜索结果
                search_output = result.stdout

                # 简单解析输出，提取关键信息
                summary = self._extract_summary(search_output, topic.title)
                key_points = self._extract_key_points(search_output)
                sources = self._extract_sources(search_output)

                topic.details = {
                    'summary': summary,
                    'background': '通过15-web-search-G多引擎搜索获取',
                    'key_points': key_points,
                    'sources': sources,
                    'search_query': search_query
                }

                print(f"  ✅ 搜索完成: {len(key_points)} 个要点")

            else:
                error_msg = result.stderr or "未知错误"
                print(f"  ⚠️ 搜索失败: {error_msg[:100]}")
                topic.details = {
                    'summary': f'关于 "{topic.title}" 的搜索暂时失败',
                    'background': '搜索服务暂不可用',
                    'key_points': [],
                    'sources': []
                }

        except subprocess.TimeoutExpired:
            print(f"  ⚠️ 搜索超时（15秒）")
            topic.details = {
                'summary': '搜索超时',
                'background': '搜索时间过长已终止',
                'key_points': [],
                'sources': []
            }

        except Exception as e:
            print(f"  ⚠️ 搜索异常: {str(e)}")
            topic.details = {
                'summary': '详细信息暂不可用',
                'background': f'搜索错误: {str(e)}',
                'key_points': [],
                'sources': []
            }

    def _extract_summary(self, search_output: str, topic_title: str) -> str:
        """从搜索结果中提取摘要"""
        lines = search_output.split('\n')

        # 寻找AI答案或摘要部分
        for i, line in enumerate(lines):
            if 'AI答案' in line or 'Perplexity' in line or '摘要' in line:
                # 返回接下来的几行作为摘要
                summary_lines = []
                for j in range(i+1, min(i+6, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        summary_lines.append(lines[j].strip())
                if summary_lines:
                    return ' '.join(summary_lines)[:200]

        return f'关于"{topic_title}"的最新动态'

    def _extract_key_points(self, search_output: str) -> list:
        """从搜索结果中提取关键要点"""
        lines = search_output.split('\n')
        key_points = []

        # 提取列表项
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                point = line.lstrip('-•').strip()
                if point and len(point) > 10:
                    key_points.append(point)
                    if len(key_points) >= 5:
                        break

        if not key_points:
            key_points = ['相关新闻和信息请查看来源链接']

        return key_points

    def _extract_sources(self, search_output: str) -> list:
        """从搜索结果中提取信息来源"""
        import re
        sources = []

        # 提取所有URL
        urls = re.findall(r'https?://[^\s\)]+', search_output)

        # 去重并限制数量
        seen = set()
        for url in urls:
            if url not in seen and len(sources) < 5:
                sources.append(url)
                seen.add(url)

        return sources

    def generate_report(self, topics: List[TrendingTopic]) -> str:
        """
        生成Markdown格式报告

        Args:
            topics: 话题列表

        Returns:
            str: Markdown格式的报告
        """
        report_lines = []

        # 标题
        report_lines.append(f"# 🎵 抖音实时热搜榜")
        report_lines.append(f"")
        report_lines.append(f"**更新时间**: {self.update_time}")
        report_lines.append(f"**热搜数量**: {len(topics)} 条")
        report_lines.append(f"")
        report_lines.append(f"---")
        report_lines.append(f"")

        # Top N热搜
        report_lines.append(f"## 🔥 Top {len(topics)} 热搜话题")
        report_lines.append(f"")

        for topic in topics:
            # 话题标题
            label_emoji = {
                '热': '🔥',
                '新': '🆕',
                '爆': '💥',
                '沸': '🌡️',
                '推荐': '⭐',
                '视频': '📹',
                '挑战': '🎯',
                '话题': '💬',
                '音乐': '🎵'
            }.get(topic.label, '')

            report_lines.append(f"### {topic.rank}. {topic.title} {label_emoji}")
            report_lines.append(f"")
            report_lines.append(f"**热度指数**: {topic.hot_index:,}")

            if topic.label:
                report_lines.append(f"**标签**: {topic.label}")

            report_lines.append(f"")

            # 详细信息
            if topic.details and self.config.include_analysis:
                details = topic.details

                if details.get('summary'):
                    report_lines.append(f"**话题概述**: {details['summary']}")
                    report_lines.append(f"")

                if details.get('background'):
                    report_lines.append(f"**背景信息**: {details['background']}")
                    report_lines.append(f"")

                if details.get('key_points'):
                    report_lines.append(f"**关键要点**:")
                    for point in details['key_points']:
                        report_lines.append(f"- {point}")
                    report_lines.append(f"")

            # 抖音链接
            report_lines.append(f"**🔗 抖音搜索**: [{topic.title}]({topic.url})")
            report_lines.append(f"")
            report_lines.append(f"---")
            report_lines.append(f"")

        # 总结
        report_lines.append(f"## 📊 数据说明")
        report_lines.append(f"")
        report_lines.append(f"- **数据源**: 天行API (抖音热搜榜)")
        report_lines.append(f"- **更新频率**: 实时")
        report_lines.append(f"- **数据时效**: {self.update_time}")
        report_lines.append(f"")

        return "\n".join(report_lines)

    def analyze(self) -> str:
        """
        执行完整分析流程

        Returns:
            str: Markdown格式的分析报告
        """
        try:
            print("🚀 开始抖音热搜分析...")
            print("")

            # 1. 获取热搜数据
            raw_data = self.fetch_trending()

            # 2. 解析数据
            all_topics = self.parse_topics(raw_data)
            print(f"📋 解析完成: {len(all_topics)} 条热搜")

            # 3. 筛选话题
            filtered_topics = self.filter_topics(all_topics)
            print(f"✅ 筛选完成: {len(filtered_topics)} 条话题")
            print("")

            # 4. 丰富话题详情 (使用WebSearch)
            if self.config.include_analysis:
                print("🔍 正在搜索话题详细信息...")
                for i, topic in enumerate(filtered_topics, 1):
                    print(f"[{i}/{len(filtered_topics)}]", end=" ")
                    self.enrich_topic_details(topic)
                print("")

            # 5. 生成报告
            self.topics = filtered_topics
            report = self.generate_report(filtered_topics)

            print("✅ 分析完成!")
            print("")

            return report

        except Exception as e:
            error_msg = f"❌ 分析失败: {str(e)}"
            print(error_msg)
            return f"# ❌ 错误\n\n{error_msg}"


def main():
    """
    主函数 - 命令行入口

    Usage:
        python handler.py                    # 默认前10名
        python handler.py --limit 5          # 前5名
        python handler.py --keyword "音乐"   # 搜索关键词
    """
    import argparse

    parser = argparse.ArgumentParser(description='抖音热搜分析器')
    parser.add_argument('--limit', type=int, default=10, help='返回热搜数量 (默认: 10)')
    parser.add_argument('--keyword', type=str, help='关键词筛选')
    parser.add_argument('--no-analysis', action='store_true', help='不包含详细分析')

    args = parser.parse_args()

    # 创建配置
    config = DouyinTrendingConfig(
        limit=args.limit,
        keyword=args.keyword,
        include_analysis=not args.no_analysis
    )

    # 执行分析
    analyzer = DouyinTrendingAnalyzer(config)
    report = analyzer.analyze()

    # 输出报告
    print(report)

    # 保存到文件
    output_file = f"douyin_trending_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 报告已保存至: {output_file}")


if __name__ == '__main__':
    main()
