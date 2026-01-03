"""
JSON生成器

将内部数据模型导出为符合project_schema.json的JSON格式
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import asdict

from core.models import (
    ClarifiedContext,
    ImpactModel,
    FlowModel,
    DomainModel,
    GherkinScenario,
    Priority
)


def generate_json(
    project_name: str,
    context: ClarifiedContext,
    impact: ImpactModel,
    flow: FlowModel,
    domain: DomainModel,
    scenarios: List[GherkinScenario]
) -> Dict[str, Any]:
    """
    生成符合project_schema.json的JSON数据
    
    Args:
        project_name: 项目名称
        context: 澄清后的上下文
        impact: Impact Mapping模型
        flow: Flow Modeling模型
        domain: Domain Modeling模型
        scenarios: BDD场景列表
    
    Returns:
        Dict[str, Any]: 符合schema的JSON字典
    """
    
    # 元数据
    meta = {
        "project_name": project_name,
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "generated_by": "01-spec-explorer"
    }
    
    # spec_model - context
    spec_context = {
        "core_problem": context.core_problem,
        "target_users": context.target_users.split("、") if context.target_users else [],
        "value_proposition": context.value_proposition,
        "technical_challenges": context.technical_challenges.split("\n") if context.technical_challenges else [],
        "mvp_scope": context.mvp_scope
    }
    
    # spec_model - impact_mapping
    impact_mapping = {
        "business_goal": impact.goal,
        "actors": [
            {
                "name": actor.name,
                "role": actor.role,
                "impacts": [imp.desired_change for imp in impact.impacts if imp.actor == actor.name]
            }
            for actor in impact.actors
        ],
        "deliverables": impact.deliverables
    }
    
    # spec_model - flow_modeling
    flow_modeling = {
        "user_stories": [
            {
                "id": story.id,
                "title": story.title,
                "as_a": _extract_as_a(story),
                "i_want": _extract_i_want(story),
                "so_that": _extract_so_that(story),
                "priority": _convert_priority(story.priority),
                "acceptance_criteria": []  # 会从scenarios中填充
            }
            for story in flow.user_stories
        ],
        "event_flow": [
            {
                "event": event.name,
                "trigger": event.trigger,
                "actions": [],
                "outcome": event.description
            }
            for event in flow.events
        ]
    }
    
    # spec_model - domain_modeling
    domain_modeling = {
        "entities": [
            {
                "name": entity.name,
                "attributes": entity.attributes,
                "behaviors": entity.behaviors
            }
            for entity in domain.entities
        ],
        "bounded_contexts": [
            {
                "name": bc.name,
                "entities": bc.entities,
                "responsibilities": [bc.responsibilities] if bc.responsibilities else []
            }
            for bc in domain.bounded_contexts
        ]
    }
    
    # spec_model - bdd_scenarios
    bdd_scenarios = [
        {
            "feature": scenario.feature,
            "scenario": scenario.scenario,
            "given": scenario.given,
            "when": scenario.when,
            "then": scenario.then
        }
        for scenario in scenarios
    ]
    
    # 组装完整JSON
    return {
        "meta": meta,
        "spec_model": {
            "context": spec_context,
            "impact_mapping": impact_mapping,
            "flow_modeling": flow_modeling,
            "domain_modeling": domain_modeling,
            "bdd_scenarios": bdd_scenarios
        }
    }


def _extract_as_a(story) -> str:
    """从用户故事描述中提取'As a'部分"""
    desc = story.description
    if "作为" in desc:
        parts = desc.split("，")
        if parts:
            return parts[0].replace("作为", "").strip()
    return ""


def _extract_i_want(story) -> str:
    """从用户故事描述中提取'I want'部分"""
    desc = story.description
    if "我想" in desc or "希望" in desc:
        parts = desc.split("，")
        for part in parts:
            if "我想" in part or "希望" in part:
                return part.replace("我想", "").replace("希望", "").strip()
    return story.title


def _extract_so_that(story) -> str:
    """从用户故事描述中提取'So that'部分"""
    desc = story.description
    if "以便" in desc or "从而" in desc:
        parts = desc.split("，")
        for part in parts:
            if "以便" in part or "从而" in part:
                return part.replace("以便", "").replace("从而", "").strip()
    return ""


def _convert_priority(priority: Priority) -> str:
    """将Priority枚举转换为schema定义的优先级"""
    mapping = {
        Priority.P0: "HIGH",
        Priority.P1: "HIGH",
        Priority.P2: "MEDIUM",
        Priority.P3: "LOW"
    }
    return mapping.get(priority, "MEDIUM")


def save_json(data: Dict[str, Any], output_path: str) -> None:
    """
    保存JSON到文件
    
    Args:
        data: JSON数据字典
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON数据已保存: {output_path}")


def main():
    """测试代码（仅用于开发）"""
    pass


if __name__ == "__main__":
    main()
