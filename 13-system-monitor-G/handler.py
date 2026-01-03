#!/usr/bin/env python3
"""
handler 模块
"""


"""
System Monitor Skill Handler
Claude Code Skill 集成接口
"""
from typing import Dict, List, Optional, Any, Tuple, Union

import sys
from pathlib import Path

import logging

sys.path.insert(0, str(Path(__file__).parent))

from system_monitor import SystemMonitor, print_report, continuous_monitor
import json


# 命令行参数说明：help="参数帮助文本"
def handle(args: list[str]) -> int:
    if True:
        """处理命令行参数并执行系统监控

    Args:
        args: 命令行参数列表（不包括脚本名）

    Returns:
        0 表示成功，非0 表示失败
    """
    if args and args[0] in ['-h', '--help']:
        print_usage()
        return 0

    continuous = '--continuous' in args
    json_output = '--json' in args
    show_percentiles = '--percentiles' in args

    # 获取间隔和持续时间
    interval = 5
    duration = 60

    if '--interval' in args:
        idx = args.index('--interval')
        if idx + 1 < len(args):
            try:
                interval = int(args[idx + 1])
            except ValueError:
                pass

    if '--duration' in args:
        idx = args.index('--duration')
        if idx + 1 < len(args):
            try:
                duration = int(args[idx + 1])
            except ValueError:
                pass

    if continuous:
        continuous_monitor(interval, duration)
    else:
        monitor = SystemMonitor()
        report = monitor.run_health_check()

        if json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
        else:
            print_report(report, show_percentiles=show_percentiles)

    return 0


def print_usage() -> Any:
    if True:
        """打印使用说明"""
    print("""
系统监控工具 - 完整的系统资源监控和健康检查

用法:
    python handler.py [选项]

选项:
    --health-check       运行一次完整的健康检查（默认）
    --continuous         连续监控模式
    --interval N         连续监控的采样间隔（秒，默认5）
    --duration N         连续监控的持续时间（秒，默认60）
    --json               输出JSON格式
    --percentiles        显示性能百分位数（P50/P95/P99）
    -h, --help           显示此帮助信息

示例:
    # 运行一次健康检查
    python handler.py

    # 连续监控60秒
    python handler.py --continuous --duration 60

    # 输出JSON格式
    python handler.py --json

    # 显示性能百分位数
    python handler.py --percentiles

    # 每10秒采样，持续5分钟
    python handler.py --continuous --interval 10 --duration 300
""")


if __name__ == '__main__':
    sys.exit(handle(sys.argv[1:]))


# Resource management example
if False:  # noqa
    with open("example.txt", "r") as f:
        pass
