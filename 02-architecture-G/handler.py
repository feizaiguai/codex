#!/usr/bin/env python3
"""
Handler 模块

提供 Handler 相关功能的实现。
"""


"""
handler 模块
"""


"""
Architecture Designer - Claude Code Skill Handler
命令行接口，支持架构设计、技术栈推荐、ADR生成等功能
"""
import sys
import json
import argparse
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from pathlib import Path
import logging

# 导入核心模块
from architecture_designer import ArchitectureDesigner
from core.models import ArchitectureDesign, ScaleType
from analyzers.scale_estimator import ScaleEstimator
from analyzers.tech_recommender import TechStackRecommender
from analyzers.pattern_selector import PatternSelector
from generators.adr_generator import ADRGenerator



# 常量定义
LOGGER = logging.getLogger(__name__)

class ArchitectureHandler:
    """
    架构设计器命令处理器

    负责解析DESIGN_DRAFT并生成架构文档

    Attributes:
        parsers: 文档解析器
        analyzers: 分析器集合
        generators: 文档生成器
    """

    def __init__(self) -> None:
        """
        初始化处理器

        创建ArchitectureDesigner实例
        """
        self.designer = ArchitectureDesigner()

    def design(
        self,
        design_draft_path: Optional[str] = None,
        design_draft_content: Optional[str] = None,
        output_file: str = 'ARCHITECTURE.md',
        output_format: str = 'markdown'
    ) -> str:
        """
        架构设计方法 - 公共接口

        Args:
            design_draft_path: 设计草稿文件路径
            design_draft_content: 设计草稿内容（如果不是文件）
            output_file: 输出文件路径
            output_format: 输出格式

        Returns:
            输出文件路径
        """
        # 如果提供了内容而不是文件路径，创建临时文件
        if design_draft_content and not design_draft_path:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                f.write(design_draft_content)
                design_draft_path = f.name

        # 执行完整设计
        if design_draft_path:
            self.design_full(design_draft_path, output_file, output_format)
            return output_file
        else:
            raise ValueError("必须提供design_draft_path或design_draft_content之一")

    def design_full(
        self,
        input_file: str,
        output_file: str = 'ARCHITECTURE.md',
        output_format: str = 'markdown'
    ) -> ArchitectureDesign:
        """
        完整架构设计

        Args:
            input_file: 输入文件(DESIGN_DRAFT.md或.json)
            output_file: 输出文件
            output_format: 输出格式 (markdown/json/both)

        Returns:
            ArchitectureDesign对象
        """
        print(f"开始架构设计...")
        print(f"输入: {input_file}")
        print(f"输出: {output_file}")
        print()

        architecture = self.designer.design(input_file, output_file)

        # 打印摘要
        self._print_design_summary(architecture)

        return architecture

    def design_quick(
        self,
        input_file: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        快速设计(仅核心结果)

        Args:
            input_file: 输入文件
            output_format: 输出格式 (text/json)

        Returns:
            核心设计结果字典
        """
        result = self.designer.design_quick(input_file)

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("快速架构设计结果")
            print("=" * 60)
            print(f"项目名称: {result['project_name']}")
            print(f"系统规模: {result['scale']}")
            print(f"规模评分: {result['score']:.1f}/50")
            print(f"后端技术: {result['backend']}")
            print(f"数据库: {result['database']}")
            print(f"架构模式: {result['pattern']}")

        return result

    def estimate_scale(
        self,
        input_file: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅评估规模

        Args:
            input_file: 输入文件
            output_format: 输出格式

        Returns:
            规模评估结果
        """
        from parsers.design_draft_parser import parse_design_draft
        from parsers.json_loader import load_json

        # 解析输入
        input_path = Path(input_file)
        if input_path.suffix.lower() == '.json':
            draft = load_json(input_file)
        else:
            draft = parse_design_draft(input_file)

        # 评估规模
        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        result = {
            'scale': assessment.scale.value,
            'score': assessment.score,
            'complexity_level': assessment.complexity_level,
            'metrics': {
                'entities': assessment.entity_count,
                'features': assessment.feature_count,
                'contexts': assessment.bounded_context_count,
                'users': assessment.estimated_users
            },
            'recommendations': assessment.recommendations
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_scale_assessment(result)

        return result

    def recommend_tech_stack(
        self,
        input_file: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅推荐技术栈

        Args:
            input_file: 输入文件
            output_format: 输出格式

        Returns:
            技术栈推荐结果
        """
        from parsers.design_draft_parser import parse_design_draft
        from parsers.json_loader import load_json

        # 解析输入
        input_path = Path(input_file)
        if input_path.suffix.lower() == '.json':
            draft = load_json(input_file)
        else:
            draft = parse_design_draft(input_file)

        # 评估规模
        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        # 推荐技术栈
        recommender = TechStackRecommender()
        tech_stack = recommender.recommend(draft, assessment)

        result = {
            'total_score': tech_stack.total_score,
            'recommendations': {
                'backend_language': tech_stack.backend_language.recommendation,
                'frontend_framework': tech_stack.frontend_framework.recommendation,
                'database': tech_stack.database.recommendation,
                'cache': tech_stack.cache.recommendation,
                'message_queue': tech_stack.message_queue.recommendation,
                'api_style': tech_stack.api_style.recommendation,
                'deployment': tech_stack.deployment.recommendation
            },
            'reasons': {
                'backend_language': tech_stack.backend_language.reason,
                'frontend_framework': tech_stack.frontend_framework.reason,
                'database': tech_stack.database.reason,
                'cache': tech_stack.cache.reason,
                'message_queue': tech_stack.message_queue.reason,
                'api_style': tech_stack.api_style.reason,
                'deployment': tech_stack.deployment.reason
            }
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_tech_stack(result)

        return result

    def select_pattern(
        self,
        input_file: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅选择架构模式

        Args:
            input_file: 输入文件
            output_format: 输出格式

        Returns:
            架构模式选择结果
        """
        from parsers.design_draft_parser import parse_design_draft
        from parsers.json_loader import load_json

        # 解析输入
        input_path = Path(input_file)
        if input_path.suffix.lower() == '.json':
            draft = load_json(input_file)
        else:
            draft = parse_design_draft(input_file)

        # 评估规模
        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        # 选择模式
        selector = PatternSelector()
        selection = selector.select(draft, assessment)

        result = {
            'primary_pattern': selection.primary_pattern.value,
            'supporting_patterns': [p.value for p in selection.supporting_patterns],
            'rationale': selection.rationale,
            'implementation_guide': selection.implementation_guide
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_pattern_selection(result)

        return result

    def generate_adr(
        self,
        input_file: str,
        output_file: Optional[str] = None,
        output_format: str = 'markdown'
    ) -> List[Dict]:
        """
        生成ADR文档

        Args:
            input_file: 输入文件
            output_file: 输出文件(可选)
            output_format: 输出格式

        Returns:
            ADR列表
        """
        from parsers.design_draft_parser import parse_design_draft
        from parsers.json_loader import load_json

        # 解析输入
        input_path = Path(input_file)
        if input_path.suffix.lower() == '.json':
            draft = load_json(input_file)
        else:
            draft = parse_design_draft(input_file)

        # 评估和推荐
        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        recommender = TechStackRecommender()
        tech_stack = recommender.recommend(draft, assessment)

        selector = PatternSelector()
        pattern_selection = selector.select(draft, assessment)

        # 生成ADR
        adr_gen = ADRGenerator()
        adrs = adr_gen.generate(draft, assessment, tech_stack, pattern_selection)

        # 保存到文件
        if output_file:
            if output_format == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump([adr.to_dict() for adr in adrs], f, indent=2, ensure_ascii=False)
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    for i, adr in enumerate(adrs, 1):
                        f.write(f"# ADR-{i:03d}: {adr.title}\n\n")
                        f.write(f"**状态**: {adr.status}\n")
                        f.write(f"**日期**: {adr.date}\n\n")
                        f.write(f"## 背景\n\n{adr.context}\n\n")
                        f.write(f"## 决策\n\n{adr.decision}\n\n")
                        f.write(f"## 结果\n\n{adr.consequences}\n\n")
                        if i < len(adrs):
                            f.write("\n---\n\n")

            print(f"✓ ADR已保存到: {output_file}")

        # 打印摘要
        print(f"生成了 {len(adrs)} 个ADR:")
        for i, adr in enumerate(adrs, 1):
            print(f"  {i}. {adr.title}")

        return [adr.to_dict() for adr in adrs]

    def _print_design_summary(self, architecture: ArchitectureDesign) -> Any:
        """
        打印设计摘要

        Args:
            architecture: 架构设计对象

        Returns:
            None
        """
        print("\n" + "=" * 60)
        print("架构设计摘要")
        print("=" * 60)
        print()
        print(f"项目: {architecture.project_name}")
        print(f"版本: {architecture.version}")
        print(f"日期: {architecture.date}")
        print()
        print("系统规模:")
        print(f"  级别: {architecture.scale_assessment.scale.value}")
        print(f"  评分: {architecture.scale_assessment.score:.1f}/50")
        print(f"  复杂度: {architecture.scale_assessment.complexity_level}")
        print()
        print("技术栈:")
        print(f"  后端: {architecture.tech_stack.backend_language.recommendation}")
        if architecture.tech_stack.frontend:
            print(f"  前端: {architecture.tech_stack.frontend.recommendation}")
        print(f"  数据库: {architecture.tech_stack.database.recommendation}")
        print(f"  缓存: {architecture.tech_stack.cache.recommendation}")
        print(f"  API: {architecture.tech_stack.api_style.recommendation}")
        print()
        print("架构模式:")
        print(f"  主模式: {architecture.pattern_selection.primary_pattern.value}")
        if architecture.pattern_selection.supporting_patterns:
            print(f"  支持模式: {', '.join([p.value for p in architecture.pattern_selection.supporting_patterns])}")
        print()
        print(f"ADR数量: {len(architecture.adrs)}")
        print()

    def _print_scale_assessment(self, result: Dict) -> Any:
        """
        打印规模评估

        Args:
            result: 规模评估结果字典

        Returns:
            None
        """
        print("=" * 60)
        print("系统规模评估")
        print("=" * 60)
        print(f"规模级别: {result['scale']}")
        print(f"规模评分: {result['score']:.1f}/50")
        print(f"复杂度: {result['complexity_level']}")
        print()
        print("关键指标:")
        for key, value in result['metrics'].items():
            print(f"  {key}: {value}")
        print()
        if result.get('recommendations'):
            print("建议:")
            for rec in result['recommendations']:
                print(f"  • {rec}")

    def _print_tech_stack(self, result: Dict) -> Any:
        """
        打印技术栈推荐

        Args:
            result: 技术栈推荐结果字典

        Returns:
            None
        """
        print("=" * 60)
        print("技术栈推荐")
        print("=" * 60)
        print(f"总评分: {result['total_score']:.1f}/10")
        print()
        print("推荐技术:")
        for key, value in result['recommendations'].items():
            reason = result['reasons'][key]
            print(f"  {key}: {value}")
            print(f"    理由: {reason}")
        print()

    def _print_pattern_selection(self, result: Dict) -> Any:
        """
        打印架构模式选择

        Args:
            result: 架构模式选择结果字典

        Returns:
            None
        """
        print("=" * 60)
        print("架构模式选择")
        print("=" * 60)
        print(f"主模式: {result['primary_pattern']}")
        if result['supporting_patterns']:
            print(f"支持模式: {', '.join(result['supporting_patterns'])}")
        print()
        print(f"选择理由:\n{result['rationale']}")
        print()
        print(f"实施指南:\n{result['implementation_guide']}")


def main() -> Any:
    """
    命令行入口

    Args:
        无命令行参数(使用argparse处理)

    Returns:
        int: 退出码(0表示成功)
    """
    parser = argparse.ArgumentParser(
        description='Architecture Designer - 架构设计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

  # 完整架构设计
  python handler.py design -i DESIGN_DRAFT.md -o ARCHITECTURE.md
  python handler.py design -i DESIGN_DRAFT.json -o ARCHITECTURE.md

  # 快速设计
  python handler.py quick -i DESIGN_DRAFT.md
  python handler.py quick -i DESIGN_DRAFT.json --json

  # 仅评估规模
  python handler.py scale -i DESIGN_DRAFT.md
  python handler.py scale -i DESIGN_DRAFT.json --json

  # 仅推荐技术栈
  python handler.py tech -i DESIGN_DRAFT.md

  # 仅选择架构模式
  python handler.py pattern -i DESIGN_DRAFT.md

  # 生成ADR
  python handler.py adr -i DESIGN_DRAFT.md -o ADR.md

输入格式:
  - Markdown: DESIGN_DRAFT.md (来自01-spec-explorer)
  - JSON: DESIGN_DRAFT.json (更可靠)
        """
    )

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # design子命令
    design_parser = subparsers.add_parser('design', help='完整架构设计')
    design_parser.add_argument('-i', '--input', required=True, help='输入文件')
    design_parser.add_argument('-o', '--output', default='ARCHITECTURE.md', help='输出文件')

    # quick子命令
    quick_parser = subparsers.add_parser('quick', help='快速设计')
    quick_parser.add_argument('-i', '--input', required=True, help='输入文件')
    quick_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # scale子命令
    scale_parser = subparsers.add_parser('scale', help='评估规模')
    scale_parser.add_argument('-i', '--input', required=True, help='输入文件')
    scale_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # tech子命令
    tech_parser = subparsers.add_parser('tech', help='推荐技术栈')
    tech_parser.add_argument('-i', '--input', required=True, help='输入文件')
    tech_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # pattern子命令
    pattern_parser = subparsers.add_parser('pattern', help='选择架构模式')
    pattern_parser.add_argument('-i', '--input', required=True, help='输入文件')
    pattern_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # adr子命令
    adr_parser = subparsers.add_parser('adr', help='生成ADR')
    adr_parser.add_argument('-i', '--input', required=True, help='输入文件')
    adr_parser.add_argument('-o', '--output', help='输出文件')
    adr_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    # 创建处理器
    handler = ArchitectureHandler()

    try:
        # 执行命令
        if args.command == 'design':
            handler.design_full(args.input, args.output)

        elif args.command == 'quick':
            handler.design_quick(
                args.input,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'scale':
            handler.estimate_scale(
                args.input,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'tech':
            handler.recommend_tech_stack(
                args.input,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'pattern':
            handler.select_pattern(
                args.input,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'adr':
            handler.generate_adr(
                args.input,
                output_file=args.output,
                output_format='json' if args.json else 'markdown'
            )

        else:
            parser.print_help()
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"错误: 文件不存在 - {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"错误: 数据验证失败 - {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
