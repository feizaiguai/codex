#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
China Social Media Aggregator - 国内社媒资讯聚合器

自动依次调用5个平台的资讯分析器，生成综合报告

Author: Claude Code Skills Team
Version: 1.0.0
License: MIT
"""

import subprocess
import os
import sys
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class PlatformConfig:
    """平台配置"""
    name: str
    display_name: str
    skill_path: str
    handler_file: str
    emoji: str


class ChinaSocialMediaAggregator:
    """国内社媒资讯聚合器"""

    def __init__(self):
        """初始化聚合器"""
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 6个平台配置
        self.platforms = [
            PlatformConfig(
                name="weibo",
                display_name="微博热搜",
                skill_path="14-weibo-trending-G",
                handler_file="handler.py",
                emoji="🔥"
            ),
            PlatformConfig(
                name="baidu",
                display_name="百度热搜",
                skill_path="21-baidu-trending-G",
                handler_file="handler.py",
                emoji="🔍"
            ),
            PlatformConfig(
                name="douyin",
                display_name="抖音热搜",
                skill_path="28-douyin-trending-G",
                handler_file="handler.py",
                emoji="🎵"
            ),
            PlatformConfig(
                name="wechat",
                display_name="微信热搜",
                skill_path="30-wechat-trending-G",
                handler_file="handler.py",
                emoji="💬"
            ),
            PlatformConfig(
                name="networkhot",
                display_name="全网热搜",
                skill_path="56-networkhot-trending-G",
                handler_file="handler.py",
                emoji="🌐"
            ),
            PlatformConfig(
                name="ai-news",
                display_name="AI资讯",
                skill_path="49-ai-news-G",
                handler_file="handler.py",
                emoji="🤖"
            ),
        ]

        self.results: List[Tuple[str, bool, str]] = []  # (平台名, 成功/失败, 报告内容)

    def execute_platform(self, platform: PlatformConfig, limit: int = 10) -> Tuple[bool, str]:
        """
        执行单个平台的分析

        Args:
            platform: 平台配置
            limit: 返回资讯数量

        Returns:
            (成功/失败, 报告内容或错误信息)
        """
        try:
            skill_dir = os.path.join(self.base_path, platform.skill_path)
            handler_path = os.path.join(skill_dir, platform.handler_file)

            if not os.path.exists(handler_path):
                return False, f"❌ {platform.display_name} skill未找到: {handler_path}"

            print(f"\n{platform.emoji} 正在执行 {platform.display_name}...")

            # 执行handler
            cmd = [
                sys.executable,  # 使用当前Python解释器
                handler_path,
                "--limit", str(limit),
                "--no-analysis"  # 不包含详细分析以加快速度
            ]

            result = subprocess.run(
                cmd,
                cwd=skill_dir,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='ignore'
            )

            if result.returncode == 0:
                # 成功
                output = result.stdout
                print(f"  ✅ {platform.display_name} 分析完成")
                return True, output
            else:
                # 失败
                error_msg = result.stderr or result.stdout or "未知错误"
                print(f"  ❌ {platform.display_name} 分析失败: {error_msg[:100]}")
                return False, f"❌ {platform.display_name} 分析失败:\n{error_msg[:500]}"

        except subprocess.TimeoutExpired:
            error_msg = f"⏱️ {platform.display_name} 执行超时（60秒）"
            print(f"  {error_msg}")
            return False, error_msg

        except Exception as e:
            error_msg = f"❌ {platform.display_name} 执行异常: {str(e)}"
            print(f"  {error_msg}")
            return False, error_msg

    def generate_combined_report(self) -> str:
        """
        生成综合报告

        Returns:
            str: Markdown格式的综合报告
        """
        report_lines = []

        # 标题
        report_lines.append("# 🌐 国内社媒资讯聚合报告")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**平台数量**: {len(self.platforms)} 个")
        report_lines.append("")

        # 执行摘要
        success_count = sum(1 for _, success, _ in self.results if success)
        report_lines.append("## 📊 执行摘要")
        report_lines.append("")
        report_lines.append(f"- **成功**: {success_count}/{len(self.platforms)} 个平台")
        report_lines.append(f"- **失败**: {len(self.platforms) - success_count}/{len(self.platforms)} 个平台")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 各平台报告
        for platform, success, content in self.results:
            platform_config = next((p for p in self.platforms if p.name == platform), None)
            if not platform_config:
                continue

            if success:
                report_lines.append(f"## {platform_config.emoji} {platform_config.display_name}")
                report_lines.append("")
                report_lines.append(content)
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")
            else:
                report_lines.append(f"## {platform_config.emoji} {platform_config.display_name}")
                report_lines.append("")
                report_lines.append(content)
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")

        # 底部说明
        report_lines.append("## 📝 说明")
        report_lines.append("")
        report_lines.append("本报告由以下6个skills生成：")
        for platform in self.platforms:
            report_lines.append(f"- {platform.emoji} **{platform.display_name}** - {platform.skill_path}")
        report_lines.append("")
        report_lines.append("触发关键词: **国内社媒资讯**")
        report_lines.append("")

        return "\n".join(report_lines)

    def run(self, limit: int = 10) -> str:
        """
        执行所有平台的分析并生成综合报告

        Args:
            limit: 每个平台返回的资讯数量

        Returns:
            str: Markdown格式的综合报告
        """
        print("🚀 开始国内社媒资讯聚合分析...")
        print(f"📋 将依次执行 {len(self.platforms)} 个平台的分析")
        print("")

        # 依次执行各平台
        for platform in self.platforms:
            success, content = self.execute_platform(platform, limit)
            self.results.append((platform.name, success, content))

        # 生成综合报告
        print("\n📄 正在生成综合报告...")
        report = self.generate_combined_report()

        print("\n✅ 国内社媒资讯聚合分析完成!")
        return report


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='国内社媒资讯聚合器')
    parser.add_argument('--limit', type=int, default=10, help='每个平台返回资讯数量 (默认: 10)')
    parser.add_argument('--output', type=str, help='输出文件路径')

    args = parser.parse_args()

    # 执行聚合分析
    aggregator = ChinaSocialMediaAggregator()
    report = aggregator.run(limit=args.limit)

    # 输出报告
    print("\n" + "="*80)
    print(report)
    print("="*80)

    # 保存报告
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"china_social_media_{timestamp}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 报告已保存至: {output_file}")


if __name__ == "__main__":
    main()
