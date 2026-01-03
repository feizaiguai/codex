"""11-debugger 命令行接口"""
import argparse
import sys
from engine import Debugger

def main():
    parser = argparse.ArgumentParser(description='11-debugger: 高级Debug专家')
    parser.add_argument('--error', required=True, help='错误信息')
    parser.add_argument('--trace', help='堆栈跟踪文件')
    parser.add_argument('--code', help='代码文件')
    parser.add_argument('--output', '-o', default='debug_report.md', help='输出报告')
    args = parser.parse_args()

    debugger = Debugger()

    try:
        stack_trace = ''
        if args.trace:
            with open(args.trace, 'r', encoding='utf-8') as f:
                stack_trace = f.read()

        code = ''
        if args.code:
            with open(args.code, 'r', encoding='utf-8') as f:
                code = f.read()

        report = debugger.debug(
            error_msg=args.error,
            stack_trace=stack_trace,
            code=code
        )

        report_text = debugger.generate_report(report)
        print(report_text)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"\n报告已保存到: {args.output}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
