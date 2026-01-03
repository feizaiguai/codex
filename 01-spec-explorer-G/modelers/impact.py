"""
Layer 1: Impact Mapping（目标与价值）

使用启发式规则分析影响（无需AI）
"""

from core.models import ClarifiedContext, ImpactModel, Actor, Impact
import re


def analyze_impact(context: ClarifiedContext) -> ImpactModel:
    """
    构建Impact Mapping

    Args:
        context: 澄清后的需求上下文

    Returns:
        ImpactModel: 影响地图模型
    """

    print("\n📊 Layer 1: Impact Mapping（目标与价值）")
    print("-" * 60)

    # 使用规则提取各个维度
    goal = _extract_goal(context)
    actors = _identify_actors(context)
    impacts = _analyze_impacts(context, actors)
    deliverables = _map_deliverables(context, impacts)

    model = ImpactModel(
        goal=goal,
        actors=actors,
        impacts=impacts,
        deliverables=deliverables
    )

    print(f"✅ 业务目标: {goal}")
    print(f"✅ 识别角色: {len(actors)}个")
    print(f"✅ 期望影响: {len(impacts)}条")
    print(f"✅ 交付物: {len(deliverables)}个")

    return model


def _extract_goal(context: ClarifiedContext) -> str:
    """使用规则提取业务目标"""
    # 优先使用value_proposition，其次使用core_problem
    if context.value_proposition and context.value_proposition != context.core_problem:
        return f"{context.value_proposition}（核心问题：{context.core_problem}）"
    return context.value_proposition or context.core_problem or "待定义业务目标"


def _identify_actors(context: ClarifiedContext) -> list[Actor]:
    """使用规则识别关键角色"""
    actors = []
    seen = set()

    if context.target_users:
        # 规则1：按顿号或逗号分割
        separators = ["、", "，", ",", "和", "以及"]
        users_text = context.target_users

        for sep in separators:
            users_text = users_text.replace(sep, "、")

        users = [u.strip() for u in users_text.split("、") if u.strip()]

        # 提取角色
        for user in users[:5]:  # 最多5个角色
            if user and user not in seen:
                # 判断角色类型
                if any(keyword in user for keyword in ["开发", "工程师", "程序员"]):
                    role_type = "开发者"
                elif any(keyword in user for keyword in ["管理", "经理", "负责人", "领导"]):
                    role_type = "管理者"
                elif any(keyword in user for keyword in ["客户", "买家", "购买"]):
                    role_type = "付费客户"
                else:
                    role_type = "主要用户"

                actors.append(Actor(
                    name=user,
                    role=role_type,
                    description=f"{user}是{role_type}"
                ))
                seen.add(user)

    # 规则2：如果没有识别到角色，添加默认角色
    if not actors:
        actors.append(Actor(name="通用用户", role="主要用户", description="系统的主要使用者"))

    return actors[:5]  # 最多5个


def _analyze_impacts(context: ClarifiedContext, actors: list[Actor]) -> list[Impact]:
    """基于规则分析期望影响"""
    impacts = []

    # 规则1：为每个角色生成影响
    for actor in actors:
        # 从价值主张中提取量化指标
        metrics = _extract_metrics(context.value_proposition)

        impacts.append(Impact(
            actor=actor.name,
            desired_change=f"提升{actor.name}的工作效率和满意度",
            metrics=metrics if metrics else ""
        ))

    # 规则2：如果有技术挑战，添加技术相关影响
    if context.technical_challenges:
        impacts.append(Impact(
            actor="系统",
            desired_change="提升系统性能和稳定性",
            metrics=""
        ))

    return impacts[:8]  # 最多8个影响


def _extract_metrics(text: str) -> str:
    """使用正则表达式提取量化指标"""
    if not text:
        return ""

    # 查找百分比
    percent_pattern = r'(\d+%|\d+\s*%|提升\s*\d+|降低\s*\d+|增加\s*\d+)'
    matches = re.findall(percent_pattern, text)

    if matches:
        return "、".join(matches[:3])  # 最多3个指标

    return ""


def _map_deliverables(context: ClarifiedContext, impacts: list[Impact]) -> list[str]:
    """基于规则映射交付物"""
    deliverables = []

    # 规则1：从MVP范围中提取
    if context.mvp_scope:
        # 优先按换行符分割（保留每行内部的顿号、逗号等）
        if "\n" in context.mvp_scope:
            items = [item.strip() for item in context.mvp_scope.split("\n") if item.strip()]
        else:
            # 按多种分隔符分割（包括顿号）
            separators = ["、", "，", ",", "；", ";"]
            scope_text = context.mvp_scope
            for sep in separators:
                scope_text = scope_text.replace(sep, "|SPLIT|")
            items = [item.strip() for item in scope_text.split("|SPLIT|") if item.strip()]

        deliverables.extend(items[:10])  # 最多10个

    # 规则2：如果交付物少于3个，从核心问题中推导
    if len(deliverables) < 3:
        # 添加通用交付物
        generic_deliverables = [
            "用户管理模块",
            "核心业务模块",
            "数据处理模块",
            "报告生成模块",
            "通知服务模块"
        ]
        deliverables.extend(generic_deliverables[:5 - len(deliverables)])

    return deliverables[:10]  # 最多10个交付物
