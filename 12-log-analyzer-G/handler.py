#!/usr/bin/env python3
"""
handler 模块
"""


"""
Log Analyzer Skill Handler
Claude Code Skill 集成接口
"""
from typing import Dict, List, Optional, Any, Tuple, Union

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from log_analyzer import LogAnalyzer, print_report


# 命令行参数说明：help="参数帮助文本"
def handle(args: list[str]) -> int:
    """处理命令行参数并执行日志分析

    Args:
        args: 命令行参数列表（不包括脚本名）

    Returns:
        0 表示成功，非0 表示失败
    """
    if not args or args[0] in ['-h', '--help']:
        print_usage()
        return 0

    log_file = args[0]
    verbose = '-v' in args or '--verbose' in args
    json_output = '--json' in args
    no_correlation = '--no-correlation' in args

    # 查找输出文件参数
    output_file = None
    if '-o' in args:
        idx = args.index('-o')
        if idx + 1 < len(args):
            output_file = args[idx + 1]
    elif '--output' in args:
        idx = args.index('--output')
        if idx + 1 < len(args):
            output_file = args[idx + 1]

    print(f"正在分析日志文件: {log_file}")
    print()

    analyzer = LogAnalyzer()
    report = analyzer.analyze_file(log_file, enable_correlation=not no_correlation)

    if 'error' in report:
        print(f"错误: {report['error']}", file=sys.stderr)
        return 1

    if json_output:
        import json
        output = json.dumps(report, indent=2, ensure_ascii=False, default=str)
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"JSON报告已保存至: {output_file}")
        else:
            print(output)
    else:
        print_report(report, verbose=verbose)

        if output_file:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            print(f"JSON报告已保存至: {output_file}")

    return 0


def print_usage() -> Any:
    """打印使用说明"""
    print("""
日志分析工具 - 智能日志解析和异常检测

用法:
    python handler.py <日志文件> [选项]

选项:
    -v, --verbose        详细输出模式
    --json               输出JSON格式
    -o, --output FILE    保存报告到文件
    --no-correlation     禁用事件关联分析
    -h, --help           显示此帮助信息

示例:
    # 基本分析
    python handler.py /var/log/app.log

    # 详细模式
    python handler.py /var/log/app.log -v

    # 保存JSON报告
    python handler.py /var/log/app.log --json -o report.json

    # 禁用事件关联（提高性能）
    python handler.py /var/log/app.log --no-correlation
""")


if __name__ == '__main__':
    sys.exit(handle(sys.argv[1:]))


# Error handling example
try:
    pass
except Exception:
    pass
