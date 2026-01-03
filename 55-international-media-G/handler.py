#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国外社媒资讯聚合器

协调器skill，自动依次调用3个国外平台的资讯分析器：
- 51-hackernews（Hacker News趋势）
- 52-reddit-trending（Reddit热门）
- 53-newsapi（全球科技新闻）

生成综合的国外社媒资讯报告。

作者: Claude Code Skills Team
版本: 1.0.0
许可: MIT
"""

import os
import sys
import argparse
import subprocess
from dataclasses import dataclass
from typing import List, Tuple
from datetime import datetime


@dataclass
class PlatformConfig:
    """平台配置"""
    name: str
    display_name: str
    skill_path: str
    emoji: str


class InternationalMediaAggregator:
    """国外社媒资讯聚合器"""

    def __init__(self):
        """初始化聚合器"""
        self.platforms = [
            PlatformConfig(
                name="hackernews",
                display_name="Hacker News",
                skill_path="51-hackernews-G",
                emoji="🟠"
            ),
            PlatformConfig(
                name="reddit",
                display_name="Reddit",
                skill_path="52-reddit-trending-G",
                emoji="🔴"
            ),
            PlatformConfig(
                name="newsapi",
                display_name="NewsAPI",
                skill_path="53-newsapi-G",
                emoji="📰"
            ),
        ]

        # 获取skills根目录
        self.skills_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def execute_platform(
        self,
        platform: PlatformConfig,
        limit: int = 10,
        newsapi_key: str = ""
    ) -> Tuple[bool, str]:
        """
        执行单个平台的分析

        Args:
            platform: 平台配置
            limit: 返回数量
            newsapi_key: NewsAPI密钥（仅newsapi需要）

        Returns:
            (是否成功, 报告内容或错误信息)
        """
        try:
            skill_dir = os.path.join(self.skills_dir, platform.skill_path)
            handler_path = os.path.join(skill_dir, "handler.py")

            if not os.path.exists(handler_path):
                error_msg = f"❌ {platform.display_name} skill未安装 ({platform.skill_path})"
                return False, error_msg

            print(f"\n{'='*60}")
            print(f"{platform.emoji} 正在执行: {platform.display_name}")
            print(f"{'='*60}\n")

            # 构建命令
            cmd = [
                sys.executable,
                handler_path,
                "--limit", str(limit),
                "--no-analysis"  # 快速模式
            ]

            # NewsAPI需要特殊处理
            if platform.name == "newsapi":
                if newsapi_key:
                    cmd.extend(["--api-key", newsapi_key])
                else:
                    # 检查环境变量
                    if not os.environ.get('NEWSAPI_KEY'):
                        error_msg = f"⚠️ NewsAPI需要API密钥，请设置NEWSAPI_KEY环境变量或使用--newsapi-key参数"
                        return False, error_msg

            # Reddit默认使用popular
            if platform.name == "reddit":
                cmd.extend(["--subreddit", "popular"])

            # 执行命令
            result = subprocess.run(
                cmd,
                cwd=skill_dir,
                capture_output=True,
                text=True,
                timeout=60,  # 60秒超时
                encoding='utf-8',
                errors='replace'
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"✅ {platform.display_name} 执行成功")
                return True, output
            else:
                error_msg = f"❌ {platform.display_name} 执行失败:\n{result.stderr}"
                print(error_msg)
                return False, error_msg

        except subprocess.TimeoutExpired:
            error_msg = f"⏱️ {platform.display_name} 执行超时（60秒）"
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"❌ {platform.display_name} 执行异常: {str(e)}"
            print(error_msg)
            return False, error_msg

    def aggregate(
        self,
        limit: int = 10,
        newsapi_key: str = ""
    ) -> str:
        """
        聚合所有平台的资讯

        Args:
            limit: 每个平台返回的资讯数量
            newsapi_key: NewsAPI密钥

        Returns:
            综合报告（Markdown格式）
        """
        print("="*60)
        print("🌐 国外社媒资讯聚合器")
        print("="*60)
        print(f"平台数量: {len(self.platforms)}")
        print(f"每个平台限制: {limit} 条")
        print("="*60)

        # 收集结果
        results = []

        # 依次执行每个平台
        for platform in self.platforms:
            success, content = self.execute_platform(platform, limit, newsapi_key)
            results.append((platform, success, content))

        # 生成综合报告
        report = self.generate_report(results, limit)

        return report

    def generate_report(
        self,
        results: List[Tuple[PlatformConfig, bool, str]],
        limit: int
    ) -> str:
        """
        生成综合报告

        Args:
            results: 平台执行结果列表
            limit: 每个平台数量

        Returns:
            Markdown格式的综合报告
        """
        # 统计成功/失败
        success_count = sum(1 for _, success, _ in results if success)
        failure_count = len(results) - success_count

        # 报告头部
        report_lines = [
            "# 🌐 国外社媒资讯聚合报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**平台数量**: {len(results)} 个",
            "",
            "## 📊 执行摘要",
            f"- **成功**: {success_count}/{len(results)} 个平台",
            f"- **失败**: {failure_count}/{len(results)} 个平台",
            "",
            "---",
            ""
        ]

        # 添加各平台报告
        for platform, success, content in results:
            report_lines.append(f"## {platform.emoji} {platform.display_name}")
            report_lines.append("")

            if success:
                # 提取报告主体（去掉第一个标题）
                lines = content.split('\n')
                # 跳过第一行标题
                if lines and lines[0].startswith('#'):
                    content_body = '\n'.join(lines[1:])
                else:
                    content_body = content

                report_lines.append(content_body)
            else:
                report_lines.append(f"**状态**: ❌ 执行失败")
                report_lines.append("")
                report_lines.append(f"**错误信息**:")
                report_lines.append(f"```")
                report_lines.append(content)
                report_lines.append(f"```")

            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # 添加说明
        report_lines.extend([
            "## 📝 说明",
            "",
            "**包含的平台**:",
            "- 🟠 **51-hackernews-G** - Hacker News趋势分析",
            "- 🔴 **52-reddit-trending-G** - Reddit热门讨论",
            "- 📰 **53-newsapi-G** - 全球科技新闻",
            "",
            "**触发关键词**: \"国外社媒资讯\"",
            "",
            "**执行模式**: 快速模式（--no-analysis），串行执行",
            ""
        ])

        return "\n".join(report_lines)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="国外社媒资讯聚合器")
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="每个平台返回的资讯数量（默认: 10）"
    )
    parser.add_argument(
        "--newsapi-key",
        type=str,
        default="",
        help="NewsAPI密钥（或设置NEWSAPI_KEY环境变量）"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出文件路径（可选）"
    )

    args = parser.parse_args()

    # 创建聚合器
    aggregator = InternationalMediaAggregator()

    # 执行聚合
    report = aggregator.aggregate(
        limit=args.limit,
        newsapi_key=args.newsapi_key
    )

    # 输出报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ 综合报告已保存到: {args.output}")
    else:
        print("\n" + "="*60)
        print("综合报告")
        print("="*60 + "\n")
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
