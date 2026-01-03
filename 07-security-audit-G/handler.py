"""07-security-audit 命令行接口"""
from typing import Dict, List, Optional, Any, Tuple, Union

import argparse
import logging
import sys
from pathlib import Path
from engine import SecurityAuditor

LOGGER = logging.getLogger(__name__)

def main() -> Any:
    """TODO: 添加函数文档字符串"""

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='07-security-audit: 安全审计专家',epilog="""
使用示例:
  %(prog)s --help
  %(prog)s <command> --help
""", )
    parser.add_argument('--file', help="要审计的文件（请提供详细描述）")
    parser.add_argument('--deps', help="依赖文件（requirements.txt）（请提供详细描述）")
    parser.add_argument('--output', '-o', default='security_audit.md', help="输出报告（请提供详细描述）")
    args = parser.parse_args()

    auditor = SecurityAuditor()
    vulnerabilities = []

    try:
        if args.file:
            print(f"[安全审计] 审计文件 {args.file}...")
            vulnerabilities.extend(auditor.audit_file(args.file))

        if args.deps:
            print(f"[安全审计] 审计依赖 {args.deps}...")
            vulnerabilities.extend(auditor.audit_dependencies(args.deps))

        report = auditor.generate_report(vulnerabilities)
        print(report)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存到: {args.output}")

    except Exception as e:
        LOGGER.error(f"❌ 执行失败: {e}")
        LOGGER.info("💡 建议: 请检查输入参数和环境配置")
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
