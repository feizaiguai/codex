"""
25-ai-code-optimizer 命令行接口
"""

import argparse
import sys
from pathlib import Path
from engine import AICodeOptimizer, optimize_file, batch_optimize


def main():
    parser = argparse.ArgumentParser(
        description='25-ai-code-optimizer: AI代码优化器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 优化单个文件
  python handler.py --file app.py

  # 优化多个文件
  python handler.py --files app.py utils.py models.py

  # 优化整个目录
  python handler.py --dir ./src --pattern "*.py"

  # 生成JSON报告
  python handler.py --file app.py --json --output report.json

  # 只显示高严重度问题
  python handler.py --file app.py --severity high
        """
    )

    parser.add_argument('--file', help='要优化的文件')
    parser.add_argument('--files', nargs='+', help='多个文件')
    parser.add_argument('--dir', help='要优化的目录')
    parser.add_argument('--pattern', default='*.py', help='文件匹配模式（用于--dir）')

    parser.add_argument(
        '--severity',
        choices=['critical', 'high', 'medium', 'low', 'info'],
        help='只显示指定严重度及以上的问题'
    )

    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--score-only', action='store_true', help='只显示评分')

    args = parser.parse_args()

    optimizer = AICodeOptimizer()
    reports = []

    # 收集要处理的文件
    if args.file:
        reports.append(optimize_file(args.file))
    elif args.files:
        reports = batch_optimize(args.files)
    elif args.dir:
        dir_path = Path(args.dir)
        files = list(dir_path.rglob(args.pattern))
        file_paths = [str(f) for f in files if f.is_file()]
        reports = batch_optimize(file_paths)
    else:
        parser.print_help()
        sys.exit(1)

    # 过滤严重度
    if args.severity:
        severity_levels = {
            'critical': ['critical'],
            'high': ['critical', 'high'],
            'medium': ['critical', 'high', 'medium'],
            'low': ['critical', 'high', 'medium', 'low'],
            'info': ['critical', 'high', 'medium', 'low', 'info']
        }
        allowed = severity_levels[args.severity]

        for report in reports:
            report.issues = [
                issue for issue in report.issues
                if issue.severity.value in allowed
            ]

    # 输出结果
    if args.json:
        import json
        output = []
        for report in reports:
            output.append({
                'file_path': report.file_path,
                'overall_score': report.overall_score,
                'complexity': {
                    'time': report.complexity_analysis.time_complexity,
                    'space': report.complexity_analysis.space_complexity,
                    'explanation': report.complexity_analysis.explanation
                },
                'issues': [
                    {
                        'type': issue.issue_type.value,
                        'severity': issue.severity.value,
                        'line': issue.line_number,
                        'description': issue.description,
                        'current_complexity': issue.current_complexity,
                        'suggested_complexity': issue.suggested_complexity,
                        'suggestion': issue.optimization_suggestion
                    }
                    for issue in report.issues
                ]
            })

        json_str = json.dumps(output, indent=2, ensure_ascii=False)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"报告已保存到: {args.output}")
        else:
            print(json_str)

    elif args.score_only:
        for report in reports:
            print(f"{report.file_path}: {report.overall_score}/100")

    else:
        for report in reports:
            print(optimizer.generate_report(report))
            print()

    # 返回状态码
    avg_score = sum(r.overall_score for r in reports) / len(reports) if reports else 0
    if avg_score < 60:
        sys.exit(1)  # 评分过低
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
