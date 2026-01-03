"""
26-prompt-engineer 命令行接口
"""

from typing import Dict, List, Optional, Any, Tuple, Union

import argparse
import json
import logging
import sys
from engine import PromptEngineer, Example, check_prompt_safety


LOGGER = logging.getLogger(__name__)


def main() -> Any:
    try:
        """TODO: 添加函数文档字符串"""
    except Exception as e:
        LOGGER.error(f"执行出错: {e}")
        return 1

    parser = argparse.ArgumentParser(
        description='26-prompt-engineer: Prompt工程师',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 优化Prompt
  python handler.py --optimize "解决这个数学问题" --type math

  # 安全检查
  python handler.py --check "ignore previous instructions"

  # A/B测试
  python handler.py --ab-test --prompt-a "简洁版" --prompt-b "详细版"

  # 创建Few-shot模板
  python handler.py --few-shot --task "分类" --examples examples.json
        """
    )

    parser.add_argument('--optimize', help='要优化的Prompt')
    parser.add_argument('--type', default='general',
                       choices=['general', 'math', 'reasoning', 'decision'],
                       help='任务类型')

    parser.add_argument('--check', help='检查Prompt安全性')

    parser.add_argument('--ab-test', action='store_true', help='进行A/B测试')
    parser.add_argument('--prompt-a', help='Prompt A')
    parser.add_argument('--prompt-b', help='Prompt B')

    parser.add_argument('--few-shot', action='store_true', help='生成Few-shot Prompt')
    parser.add_argument('--task', help='任务描述')
    parser.add_argument('--examples', help='示例文件(JSON)')

    parser.add_argument('--model', choices=['gpt-4', 'claude-3', 'gemini-pro'],
                       help='目标模型')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')

    args = parser.parse_args()

    engineer = PromptEngineer()

    if args.optimize:
        result = engineer.optimize_prompt(args.optimize, args.type)

        if args.json:
            print(json.dumps({
                'original': result.original,
                'optimized': result.optimized,
                'improvements': result.improvements,
                'expected_impact': result.expected_impact
            }, indent=2, ensure_ascii=False))
        else:
            print("原始Prompt:")
            print("-" * 80)
            print(result.original)
            print("\n优化后Prompt:")
            print("-" * 80)
            print(result.optimized)
            print("\n改进点:")
            for i, imp in enumerate(result.improvements, 1):
                print(f"  {i}. {imp}")
            print(f"\n预期影响: {result.expected_impact}")

    elif args.check:
        result = check_prompt_safety(args.check)

        print(f"安全等级: {result.level.value}")
        if result.issues:
            print("\n发现问题:")
            for issue in result.issues:
                print(f"  - {issue}")
        print("\n安全建议:")
        for suggestion in result.suggestions:
            print(f"  - {suggestion}")

        if result.level.value in ['critical', 'dangerous']:
            sys.exit(1)

    elif args.ab_test:
        if not args.prompt_a or not args.prompt_b:
            print("错误: A/B测试需要 --prompt-a 和 --prompt-b")
            sys.exit(1)

        result = engineer.ab_tester.compare_prompts(args.prompt_a, args.prompt_b, [])

        print(f"获胜者: Prompt {result.winner}")
        print(f"置信度: {result.confidence:.2%}")
        print(f"\nPrompt A 评分: {result.metrics['score_a']:.1f}")
        print(f"Prompt B 评分: {result.metrics['score_b']:.1f}")

    elif args.few_shot:
        if not args.task:
            print("错误: Few-shot需要 --task")
            sys.exit(1)

        examples = []
        if args.examples:
            with open(args.examples, 'r', encoding='utf-8') as f:
                data = json.load(f)
                examples = [Example(**ex) for ex in data]

        query = "新的输入"
        prompt = engineer.few_shot_optimizer.generate_few_shot_prompt(
            args.task, examples, query
        )
        print(prompt)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
