#!/usr/bin/env python3
"""
SpecExplorer - Claude Code Skill Handler
命令行接口，支持需求探索、业务建模、BDD场景生成等功能
"""
import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from pathlib import Path

# 导入核心模块
from spec_explorer import explore_project, explore_from_document
from core.models import RequirementContext
from modelers import impact, flow, domain
from generators import gherkin, design_doc, json_generator


class SpecExplorerHandler:
    """需求探索器命令处理器"""

    def __init__(self):
        """初始化处理器"""
        pass

    def explore(
        self,
        input_source: str,
        is_document: bool = False,
        interactive: bool = True,
        output_file: str = 'DESIGN_DRAFT.md',
        output_format: str = 'both'
    ) -> str:
        """
        执行需求探索

        Args:
            input_source: 输入源（文档路径或文本描述）
            is_document: 是否为文档模式
            interactive: 是否交互模式
            output_file: 输出文件
            output_format: 输出格式 (markdown/json/both)

        Returns:
            输出文件路径
        """
        if is_document:
            output_path = explore_from_document(
                doc_path=input_source,
                interactive=interactive,
                output_file=output_file
            )
        else:
            output_path = explore_project(
                initial_description=input_source,
                interactive=interactive,
                output_file=output_file
            )

        return output_path

    def analyze_impact(
        self,
        description: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅执行影响力分析

        Args:
            description: 项目描述
            output_format: 输出格式

        Returns:
            影响力分析结果
        """
        # 创建简单的上下文
        context = RequirementContext(
            core_problem=description,
            target_users=['用户'],
            value_proposition='解决核心问题',
            technical_challenges=[],
            mvp_scope=[]
        )

        # 执行影响力分析
        impact_model = impact.analyze_impact(context)

        result = {
            'business_goal': impact_model.business_goal,
            'key_actors': impact_model.key_actors,
            'impacts': impact_model.impacts,
            'deliverables': impact_model.deliverables
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_impact_model(result)

        return result

    def analyze_flow(
        self,
        description: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅执行流程分析

        Args:
            description: 项目描述
            output_format: 输出格式

        Returns:
            流程分析结果
        """
        # 创建上下文和影响模型
        context = RequirementContext(
            core_problem=description,
            target_users=['用户'],
            value_proposition='解决核心问题',
            technical_challenges=[],
            mvp_scope=[]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)

        result = {
            'events': flow_model.events,
            'user_stories': flow_model.user_stories,
            'journey_stages': flow_model.journey_stages
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_flow_model(result)

        return result

    def analyze_domain(
        self,
        description: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        仅执行领域分析

        Args:
            description: 项目描述
            output_format: 输出格式

        Returns:
            领域分析结果
        """
        # 创建完整的分析链
        context = RequirementContext(
            core_problem=description,
            target_users=['用户'],
            value_proposition='解决核心问题',
            technical_challenges=[],
            mvp_scope=[]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        result = {
            'entities': domain_model.entities,
            'value_objects': domain_model.value_objects,
            'aggregates': domain_model.aggregates,
            'bounded_contexts': domain_model.bounded_contexts
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_domain_model(result)

        return result

    def generate_bdd(
        self,
        description: str,
        output_file: Optional[str] = None,
        output_format: str = 'text'
    ) -> List[Dict[str, Any]]:
        """
        生成BDD场景

        Args:
            description: 项目描述
            output_file: 输出文件（可选）
            output_format: 输出格式

        Returns:
            BDD场景列表
        """
        # 执行完整分析
        context = RequirementContext(
            core_problem=description,
            target_users=['用户'],
            value_proposition='解决核心问题',
            technical_challenges=[],
            mvp_scope=[]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        # 生成BDD场景
        scenarios = gherkin.generate_bdd_scenarios(flow_model, domain_model)

        # 保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for scenario in scenarios:
                    f.write(f"Feature: {scenario['feature']}\n\n")
                    f.write(f"Scenario: {scenario['scenario']}\n")
                    for step in scenario['steps']:
                        f.write(f"  {step}\n")
                    f.write("\n")
            print(f"✓ BDD场景已保存到: {output_file}")

        if output_format == 'json':
            print(json.dumps(scenarios, indent=2, ensure_ascii=False))
        else:
            self._print_bdd_scenarios(scenarios)

        return scenarios

    def validate_context(
        self,
        doc_path: str,
        output_format: str = 'text'
    ) -> Dict[str, Any]:
        """
        验证架构文档完整性

        Args:
            doc_path: 文档路径
            output_format: 输出格式

        Returns:
            验证结果
        """
        from parsers.architecture_doc import parse_architecture_document

        # 解析文档
        extracted = parse_architecture_document(doc_path)

        # 检测缺失字段
        missing_fields = []
        if not extracted.get('core_problem'):
            missing_fields.append('核心问题')
        if not extracted.get('target_users'):
            missing_fields.append('目标用户')
        if not extracted.get('value_proposition'):
            missing_fields.append('价值主张')
        if not extracted.get('mvp_scope'):
            missing_fields.append('MVP范围')

        result = {
            'is_valid': len(missing_fields) == 0,
            'extracted_fields': {
                'core_problem': bool(extracted.get('core_problem')),
                'target_users': bool(extracted.get('target_users')),
                'value_proposition': bool(extracted.get('value_proposition')),
                'technical_challenges': bool(extracted.get('technical_challenges')),
                'mvp_scope': bool(extracted.get('mvp_scope'))
            },
            'missing_fields': missing_fields,
            'extracted': extracted
        }

        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            self._print_validation_result(result)

        return result

    def _print_impact_model(self, model: Dict):
        """打印影响力模型"""
        print("=" * 60)
        print("影响力分析 (Impact Mapping)")
        print("=" * 60)
        print(f"业务目标: {model['business_goal']}")
        print()
        print("关键角色:")
        for actor in model['key_actors']:
            print(f"  • {actor}")
        print()
        print("期望影响:")
        for imp in model['impacts']:
            print(f"  • {imp}")
        print()
        print("交付物:")
        for deliverable in model['deliverables']:
            print(f"  • {deliverable}")
        print()

    def _print_flow_model(self, model: Dict):
        """打印流程模型"""
        print("=" * 60)
        print("流程建模 (Flow Modeling)")
        print("=" * 60)
        print("领域事件:")
        for event in model['events']:
            print(f"  • {event}")
        print()
        print("用户故事:")
        for story in model['user_stories']:
            print(f"  • {story}")
        print()
        print("用户旅程阶段:")
        for stage in model['journey_stages']:
            print(f"  • {stage}")
        print()

    def _print_domain_model(self, model: Dict):
        """打印领域模型"""
        print("=" * 60)
        print("领域建模 (Domain Modeling)")
        print("=" * 60)
        print("实体:")
        for entity in model['entities']:
            print(f"  • {entity}")
        print()
        print("值对象:")
        for vo in model['value_objects']:
            print(f"  • {vo}")
        print()
        print("聚合根:")
        for agg in model['aggregates']:
            print(f"  • {agg}")
        print()
        print("限界上下文:")
        for bc in model['bounded_contexts']:
            print(f"  • {bc}")
        print()

    def _print_bdd_scenarios(self, scenarios: List[Dict]):
        """打印BDD场景"""
        print("=" * 60)
        print("BDD场景 (Gherkin)")
        print("=" * 60)
        for scenario in scenarios:
            print(f"\nFeature: {scenario['feature']}")
            print(f"Scenario: {scenario['scenario']}")
            for step in scenario['steps']:
                print(f"  {step}")
        print()

    def _print_validation_result(self, result: Dict):
        """打印验证结果"""
        print("=" * 60)
        print("文档验证结果")
        print("=" * 60)
        print(f"是否完整: {'✓ 是' if result['is_valid'] else '✗ 否'}")
        print()
        print("已提取字段:")
        for field, extracted in result['extracted_fields'].items():
            status = '✓' if extracted else '✗'
            print(f"  {status} {field}")
        print()
        if result['missing_fields']:
            print("缺失字段:")
            for field in result['missing_fields']:
                print(f"  • {field}")
        print()


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='SpecExplorer - 需求探索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

  # 完整探索（文档模式）
  python handler.py explore --doc architecture.md
  python handler.py explore --doc architecture.md --no-interactive

  # 完整探索（文本模式）
  python handler.py explore --text "构建智能合约审计平台"
  python handler.py explore --text "..." --no-interactive --output my_design.md

  # 仅影响力分析
  python handler.py impact "构建电商平台" --json

  # 仅流程分析
  python handler.py flow "用户注册和登录系统"

  # 仅领域分析
  python handler.py domain "订单管理系统"

  # 生成BDD场景
  python handler.py bdd "支付流程" --output scenarios.feature

  # 验证文档
  python handler.py validate architecture.md
        """
    )

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # explore子命令
    explore_parser = subparsers.add_parser('explore', help='完整需求探索')
    explore_group = explore_parser.add_mutually_exclusive_group(required=True)
    explore_group.add_argument('--doc', help='架构文档路径')
    explore_group.add_argument('--text', help='项目描述文本')
    explore_parser.add_argument('--no-interactive', action='store_true', help='禁用交互模式')
    explore_parser.add_argument('--output', default='DESIGN_DRAFT.md', help='输出文件')

    # impact子命令
    impact_parser = subparsers.add_parser('impact', help='影响力分析')
    impact_parser.add_argument('description', help='项目描述')
    impact_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # flow子命令
    flow_parser = subparsers.add_parser('flow', help='流程分析')
    flow_parser.add_argument('description', help='项目描述')
    flow_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # domain子命令
    domain_parser = subparsers.add_parser('domain', help='领域分析')
    domain_parser.add_argument('description', help='项目描述')
    domain_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # bdd子命令
    bdd_parser = subparsers.add_parser('bdd', help='生成BDD场景')
    bdd_parser.add_argument('description', help='项目描述')
    bdd_parser.add_argument('--output', help='输出文件')
    bdd_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    # validate子命令
    validate_parser = subparsers.add_parser('validate', help='验证文档')
    validate_parser.add_argument('doc', help='文档路径')
    validate_parser.add_argument('--json', action='store_true', help='JSON格式输出')

    args = parser.parse_args()

    # 创建处理器
    handler = SpecExplorerHandler()

    try:
        # 执行命令
        if args.command == 'explore':
            if args.doc:
                handler.explore(
                    input_source=args.doc,
                    is_document=True,
                    interactive=not args.no_interactive,
                    output_file=args.output
                )
            else:
                handler.explore(
                    input_source=args.text,
                    is_document=False,
                    interactive=not args.no_interactive,
                    output_file=args.output
                )

        elif args.command == 'impact':
            handler.analyze_impact(
                args.description,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'flow':
            handler.analyze_flow(
                args.description,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'domain':
            handler.analyze_domain(
                args.description,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'bdd':
            handler.generate_bdd(
                args.description,
                output_file=args.output,
                output_format='json' if args.json else 'text'
            )

        elif args.command == 'validate':
            handler.validate_context(
                args.doc,
                output_format='json' if args.json else 'text'
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
