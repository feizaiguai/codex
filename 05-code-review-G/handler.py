"""05-code-review 命令行接口
代码审查专家 - 代码质量检查和安全扫描
"""
import argparse
import sys
from pathlib import Path
from typing import Optional
from engine import CodeReviewer


def main() -> None:
    """主函数 - 命令行入口

    执行代码审查流程：
    1. 解析命令行参数
    2. 执行代码审查
    3. 生成并保存报告
    """
    parser = argparse.ArgumentParser(
        description='05-code-review: 代码审查专家',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 审查单个文件
  python handler.py --file module.py

  # 指定输出文件
  python handler.py --file module.py --output custom_report.md

  # 审查并显示详细信息
  python handler.py --file module.py -o report.md
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='要审查的文件路径'
    )
    parser.add_argument(
        '--output', '-o',
        default='review_report.md',
        help='输出报告路径 (默认: review_report.md)'
    )

    args = parser.parse_args()

    try:
        # 验证文件存在
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)

        # 执行审查
        reviewer = CodeReviewer()
        result = reviewer.review_file(args.file)
        report = reviewer.generate_report(result)

        # 保存报告
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # 输出到控制台
        print(report)
        print(f"\n✓ 报告已保存到: {args.output}")

    except FileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"错误: 权限不足 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
