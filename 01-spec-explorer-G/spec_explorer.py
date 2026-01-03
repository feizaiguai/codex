#!/usr/bin/env python3
"""
SpecExplorer - 需求探索器

支持两种输入模式：
1. 文本描述模式：从用户描述开始交互
2. 架构文档模式：从架构文档提取信息（推荐）

通用三层建模流：Impact → Flow → Domain
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from interaction import clarify_requirements, clarify_from_document
from modelers import impact, flow, domain
from generators import gherkin, design_doc, json_generator
from parsers.requirement_doc import parse_requirement


def explore_from_document(doc_path: str, interactive: bool = True, output_file: str = "DESIGN_DRAFT.md") -> str:
    """
    从架构文档开始探索（推荐模式）

    Args:
        doc_path: 架构文档路径
        interactive: 是否交互式补充缺失信息（默认True）
        output_file: 输出文件名（默认DESIGN_DRAFT.md）

    Returns:
        str: 输出文件路径
    """

    print("\n" + "=" * 80)
    print("🚀 SpecExplorer - 需求探索器（架构文档模式）")
    print("=" * 80)
    print("\n📋 采用通用三层建模流（适用所有项目类型）")
    print("   Layer 1: Impact Mapping（目标与价值）")
    print("   Layer 2: Flow Modeling（流程与事件）")
    print("   Layer 3: Domain Modeling（结构与实体）")
    print("\n" + "=" * 80 + "\n")

    # 第1步：解析架构文档并澄清
    print("🔍 第1步：架构文档解析与需求澄清...")
    context = clarify_from_document(doc_path, interactive=interactive)

    # 第2步：三层建模（线性执行，无分支）
    print("\n" + "=" * 80)
    print("🎯 第2步：三层建模")
    print("=" * 80)

    # Layer 1: Impact Mapping
    impact_model = impact.analyze_impact(context)

    # Layer 2: Flow Modeling
    flow_model = flow.analyze_flow(context, impact_model)

    # Layer 3: Domain Modeling
    domain_model = domain.analyze_domain(context, flow_model)

    # 第3步：生成BDD场景
    print("\n" + "=" * 80)
    print("🧪 第3步：生成BDD/ATDD场景")
    print("=" * 80)
    bdd_scenarios = gherkin.generate_bdd_scenarios(flow_model, domain_model)
    acceptance_criteria = gherkin.generate_acceptance_criteria(flow_model)

    # 第4步：生成设计草稿
    print("\n" + "=" * 80)
    print("📄 第4步：生成设计草稿")
    print("=" * 80)
    design_draft_content = design_doc.generate(
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )

    # 保存Markdown文件
    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(design_draft_content)

    # 保存JSON文件（新增）
    json_output_path = output_path.with_suffix('.json')
    project_name = context.core_problem[:50] if context.core_problem else "未命名项目"
    json_data = json_generator.generate_json(
        project_name=project_name,
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )
    json_generator.save_json(json_data, str(json_output_path))

    # 完成
    print("\n" + "=" * 80)
    print("✅ 设计草稿生成完成")
    print("=" * 80)
    print(f"\n📁 Markdown输出: {output_path}")
    print(f"📁 JSON输出: {json_output_path}")
    print("\n📌 下一步：")
    print("   1. 评审设计草稿")
    print("   2. 使用 02-architecture 生成架构文档")
    print("   3. 使用 SpecFlow (35号Skill) 验证和标准化\n")

    return str(output_path)


def explore_from_requirement(content: str, format_hint: str = "auto", interactive: bool = True, output_file: str = "DESIGN_DRAFT.md") -> str:
    """
    从任意格式需求开始探索（新增：多格式支持）

    Args:
        content: 需求内容（可以是文本或文件路径）
        format_hint: 格式提示（auto/chat_transcript/requirement_list/user_stories/free_text）
        interactive: 是否交互式补充缺失信息（默认True）
        output_file: 输出文件名（默认DESIGN_DRAFT.md）

    Returns:
        str: 输出文件路径
    """

    print("\n" + "=" * 80)
    print("🚀 SpecExplorer - 需求探索器（多格式需求模式）")
    print("=" * 80)
    print("\n📋 采用通用三层建模流（适用所有项目类型）")
    print("   Layer 1: Impact Mapping（目标与价值）")
    print("   Layer 2: Flow Modeling（流程与事件）")
    print("   Layer 3: Domain Modeling（结构与实体）")
    print("\n" + "=" * 80 + "\n")

    # 第1步：解析多格式需求
    print(f"🔍 第1步：多格式需求解析（格式提示：{format_hint}）...")
    req_dict = parse_requirement(content, format_hint)

    print(f"✓ 检测到格式: {req_dict['source_format']}")
    print(f"✓ 项目目标: {req_dict['project_goal'][:80] if req_dict['project_goal'] else '(未提取)'}")
    print(f"✓ 核心功能: {len(req_dict['core_features'])} 个")
    print(f"✓ 目标用户: {len(req_dict['target_users'])} 个")

    # 将解析结果转换为Context对象（使用现有的clarify逻辑）
    from core.context import RequirementContext

    context = RequirementContext(
        core_problem=req_dict['project_goal'] or "需求探索项目",
        target_users=req_dict['target_users'],
        user_roles=req_dict['user_roles'],
        value_proposition=req_dict['value_proposition'],
        success_criteria=req_dict['success_metrics'],
        constraints=req_dict['constraints'],
        project_type="通用项目",
        industry="未指定",
        scale="未指定"
    )

    # 补充上下文字段
    context.core_features = req_dict['core_features']
    context.mvp_scope = req_dict['mvp_scope']
    context.technical_stack = req_dict['technical_stack']
    context.technical_challenges = req_dict['technical_challenges']
    context.performance_requirements = req_dict['performance_requirements']
    context.security_requirements = req_dict['security_requirements']
    context.business_goals = req_dict['business_goals']

    # 如果启用交互模式，补充缺失信息
    if interactive:
        print("\n💬 交互式补充缺失信息...")
        # 简单检查缺失字段
        missing_fields = []
        if not context.core_problem or context.core_problem == "需求探索项目":
            missing_fields.append("项目目标")
        if not context.target_users:
            missing_fields.append("目标用户")
        if not context.core_features:
            missing_fields.append("核心功能")

        if missing_fields:
            print(f"⚠️ 检测到缺失字段: {', '.join(missing_fields)}")
            print("提示: 如需补充，请使用 --interactive 模式")

    # 第2步：三层建模（线性执行，无分支）
    print("\n" + "=" * 80)
    print("🎯 第2步：三层建模")
    print("=" * 80)

    # Layer 1: Impact Mapping
    impact_model = impact.analyze_impact(context)

    # Layer 2: Flow Modeling
    flow_model = flow.analyze_flow(context, impact_model)

    # Layer 3: Domain Modeling
    domain_model = domain.analyze_domain(context, flow_model)

    # 第3步：生成BDD场景
    print("\n" + "=" * 80)
    print("🧪 第3步：生成BDD/ATDD场景")
    print("=" * 80)
    bdd_scenarios = gherkin.generate_bdd_scenarios(flow_model, domain_model)
    acceptance_criteria = gherkin.generate_acceptance_criteria(flow_model)

    # 第4步：生成设计草稿
    print("\n" + "=" * 80)
    print("📄 第4步：生成设计草稿")
    print("=" * 80)
    design_draft_content = design_doc.generate(
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )

    # 保存Markdown文件
    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(design_draft_content)

    # 保存JSON文件（新增）
    json_output_path = output_path.with_suffix('.json')
    project_name = context.core_problem[:50] if context.core_problem else "未命名项目"
    json_data = json_generator.generate_json(
        project_name=project_name,
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )
    json_generator.save_json(json_data, str(json_output_path))

    # 完成
    print("\n" + "=" * 80)
    print("✅ 设计草稿生成完成")
    print("=" * 80)
    print(f"\n📁 Markdown输出: {output_path}")
    print(f"📁 JSON输出: {json_output_path}")
    print(f"\n📊 需求来源格式: {req_dict['source_format']}")
    print("\n📌 下一步：")
    print("   1. 评审设计草稿")
    print("   2. 使用 02-architecture 生成架构文档")
    print("   3. 使用 SpecFlow (35号Skill) 验证和标准化\n")

    return str(output_path)


def explore_project(initial_description: str, interactive: bool = True, output_file: str = "DESIGN_DRAFT.md") -> str:
    """
    从文本描述开始探索（原有模式）

    Args:
        initial_description: 用户的初始项目描述
        interactive: 是否使用交互模式（默认True）
        output_file: 输出文件名（默认DESIGN_DRAFT.md）

    Returns:
        str: 输出文件路径
    """

    print("\n" + "=" * 80)
    print("🚀 SpecExplorer - 需求探索器")
    print("=" * 80)
    print("\n📋 采用通用三层建模流（适用所有项目类型）")
    print("   Layer 1: Impact Mapping（目标与价值）")
    print("   Layer 2: Flow Modeling（流程与事件）")
    print("   Layer 3: Domain Modeling（结构与实体）")
    print("\n" + "=" * 80 + "\n")

    # 第1步：交互式澄清（3-5轮提问）
    print("🔍 第1步：需求澄清...")
    context = clarify_requirements(initial_description, interactive=interactive)

    # 第2步：三层建模（线性执行，无分支）
    print("\n" + "=" * 80)
    print("🎯 第2步：三层建模")
    print("=" * 80)

    # Layer 1: Impact Mapping
    impact_model = impact.analyze_impact(context)

    # Layer 2: Flow Modeling
    flow_model = flow.analyze_flow(context, impact_model)

    # Layer 3: Domain Modeling
    domain_model = domain.analyze_domain(context, flow_model)

    # 第3步：生成BDD场景
    print("\n" + "=" * 80)
    print("🧪 第3步：生成BDD/ATDD场景")
    print("=" * 80)
    bdd_scenarios = gherkin.generate_bdd_scenarios(flow_model, domain_model)
    acceptance_criteria = gherkin.generate_acceptance_criteria(flow_model)

    # 第4步：生成设计草稿
    print("\n" + "=" * 80)
    print("📄 第4步：生成设计草稿")
    print("=" * 80)
    design_draft_content = design_doc.generate(
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )

    # 保存Markdown文件
    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(design_draft_content)

    # 保存JSON文件（新增）
    json_output_path = output_path.with_suffix('.json')
    project_name = context.core_problem[:50] if context.core_problem else "未命名项目"
    json_data = json_generator.generate_json(
        project_name=project_name,
        context=context,
        impact=impact_model,
        flow=flow_model,
        domain=domain_model,
        scenarios=bdd_scenarios
    )
    json_generator.save_json(json_data, str(json_output_path))

    # 完成
    print("\n" + "=" * 80)
    print("✅ 设计草稿生成完成")
    print("=" * 80)
    print(f"\n📁 Markdown输出: {output_path}")
    print(f"📁 JSON输出: {json_output_path}")
    print("\n📌 下一步：")
    print("   1. 评审设计草稿")
    print("   2. 使用 02-architecture 生成架构文档")
    print("   3. 使用 SpecFlow (35号Skill) 验证和标准化\n")

    return str(output_path)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="SpecExplorer - 需求探索器（通用三层建模流）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：

  📄 架构文档模式（推荐）：
  python spec_explorer.py --doc architecture.md
  python spec_explorer.py --doc architecture.md --no-interactive

  💬 文本描述模式：
  python spec_explorer.py "我想做一个AI驱动的智能合约审计平台"
  python spec_explorer.py "..." --no-interactive
  python spec_explorer.py "..." --output my_design.md

架构文档格式要求：
  支持Markdown格式，建议包含以下章节：
  - 项目目标/背景
  - 目标用户/角色
  - 核心价值主张
  - 核心功能/MVP范围
  - 技术栈/架构
  - 技术挑战/约束
        """
    )

    # 互斥参数组：文档模式 vs 需求模式 vs 文本模式
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--doc",
        metavar="FILE",
        help="架构文档文件路径（Markdown格式）"
    )
    input_group.add_argument(
        "--req",
        metavar="FILE_OR_TEXT",
        help="需求文档或文本（支持多种格式：聊天记录/需求列表/用户故事/自由文本）"
    )
    input_group.add_argument(
        "description",
        nargs="?",
        help="项目的初始描述（文本模式）"
    )

    parser.add_argument(
        "--format",
        choices=["auto", "chat_transcript", "requirement_list", "user_stories", "free_text", "markdown_doc"],
        default="auto",
        help="需求格式提示（仅在使用--req时有效，默认：auto自动识别）"
    )

    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="禁用交互模式"
    )

    parser.add_argument(
        "--output", "-o",
        default="DESIGN_DRAFT.md",
        help="输出文件名（默认：DESIGN_DRAFT.md）"
    )

    args = parser.parse_args()

    try:
        if args.doc:
            # 架构文档模式
            output_path = explore_from_document(
                doc_path=args.doc,
                interactive=not args.no_interactive,
                output_file=args.output
            )
        elif args.req:
            # 多格式需求模式
            output_path = explore_from_requirement(
                content=args.req,
                format_hint=args.format,
                interactive=not args.no_interactive,
                output_file=args.output
            )
        else:
            # 文本描述模式
            output_path = explore_project(
                initial_description=args.description,
                interactive=not args.no_interactive,
                output_file=args.output
            )

        print(f"✅ 成功生成设计草稿: {output_path}\n")
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断\n")
        return 130
    except FileNotFoundError as e:
        print(f"\n❌ 文件不存在: {e}\n", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"\n❌ 错误: {e}\n", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
