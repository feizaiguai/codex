"""
设计草稿生成器
"""

from datetime import datetime
from core.models import ClarifiedContext, ImpactModel, FlowModel, DomainModel, GherkinScenario, DesignDraft


def generate(context: ClarifiedContext,
             impact: ImpactModel,
             flow: FlowModel,
             domain: DomainModel,
             scenarios: list[GherkinScenario]) -> str:
    """
    生成设计草稿（Markdown格式）

    Args:
        context: 澄清后的需求
        impact: Impact Mapping模型
        flow: Flow模型
        domain: Domain模型
        scenarios: BDD场景列表

    Returns:
        str: Markdown格式的设计草稿
    """

    print("\n📄 生成设计草稿...")
    print("-" * 60)

    project_name = _extract_project_name(context)

    md = f"""# {project_name} 设计草稿

> 📌 本文档由 SpecExplorer (01号Skill) 自动生成
> 🎯 采用通用三层建模流（Impact → Flow → Domain）
> 🔄 下一步：使用 SpecFlow (35号Skill) 验证和标准化

---

## 元信息

- 项目名称：{project_name}
- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 建模方法：Impact Mapping + Event Storming + DDD

---

## 第1章：需求概览

### 核心问题
{context.core_problem}

### 目标用户
{context.target_users}

### 价值主张
{context.value_proposition}

### 技术挑战
{context.technical_challenges or "待识别"}

### MVP范围
{context.mvp_scope or "待定义"}

---

## 第2章：Impact Mapping（目标与价值）

### 业务目标
{impact.goal}

### 关键角色
"""

    for actor in impact.actors:
        md += f"- **{actor.name}**（{actor.role}）\n"

    md += "\n### 期望影响\n\n"
    md += "| 角色 | 期望变化 | 量化指标 |\n"
    md += "|-----|---------|----------|\n"
    for imp in impact.impacts:
        md += f"| {imp.actor} | {imp.desired_change} | {imp.metrics or '-'} |\n"

    md += "\n### 交付物映射\n\n"
    for i, deliverable in enumerate(impact.deliverables, 1):
        md += f"{i}. {deliverable}\n"

    md += "\n---\n\n## 第3章：Flow Modeling（流程与事件）\n\n"
    md += "### Event Storming\n\n"
    md += "**领域事件**:\n"
    for event in flow.events:
        md += f"- **{event.name}**（触发：{event.trigger}）\n"

    md += "\n### User Story Mapping\n\n"
    md += "**用户旅程阶段**:\n"
    for stage in flow.journey_stages:
        md += f"- {stage.name}\n"

    md += "\n**用户故事列表**:\n\n"
    md += "| ID | 标题 | 描述 | 优先级 | 所属阶段 |\n"
    md += "|---|------|------|--------|----------|\n"
    for story in flow.user_stories:
        md += f"| {story.id} | {story.title} | {story.description} | {story.priority.value} | {story.stage} |\n"

    md += "\n---\n\n## 第4章：Domain Modeling（结构与实体）\n\n"
    md += "### 核心实体\n\n"
    for entity in domain.entities:
        md += f"**{entity.name}**:\n"
        md += f"- 属性：{', '.join(entity.attributes)}\n"
        md += f"- 行为：{', '.join(entity.behaviors)}\n\n"

    md += "### 值对象\n\n"
    for vo in domain.value_objects:
        md += f"- **{vo.name}**：{', '.join(vo.fields)}\n"

    md += "\n### 聚合根\n\n"
    for agg in domain.aggregates:
        md += f"**{agg.root}**:\n"
        md += f"- 包含：{', '.join(agg.entities)}\n"
        md += f"- 不变式：{', '.join(agg.invariants)}\n\n"

    md += "### 限界上下文\n\n"
    for bc in domain.bounded_contexts:
        md += f"**{bc.name}**:\n"
        md += f"- 职责：{bc.responsibilities}\n"
        md += f"- 实体：{', '.join(bc.entities)}\n\n"

    md += "---\n\n## 第5章：BDD/ATDD场景\n\n"
    for scenario in scenarios:
        md += f"### Feature: {scenario.feature}\n\n"
        md += f"```gherkin\n"
        md += f"Feature: {scenario.feature}\n"
        if scenario.as_a:
            md += f"  As a {scenario.as_a}\n"
            md += f"  I want to {scenario.i_want}\n"
            md += f"  So that {scenario.so_that}\n\n"
        md += f"  Scenario: {scenario.scenario}\n"
        for g in scenario.given:
            md += f"    Given {g}\n"
        for w in scenario.when:
            md += f"    When {w}\n"
        for t in scenario.then:
            md += f"    Then {t}\n"
        md += f"```\n\n"

    md += "---\n\n## 附录：下一步行动\n\n"
    md += "1. **验证设计**：与团队评审三层建模是否准确\n"
    md += "2. **使用SpecFlow**：`python specflow.py --input DESIGN_DRAFT.md`\n"
    md += "3. **开始开发**：按用户故事优先级迭代开发\n"

    print(f"✅ 设计草稿生成完成")

    return md


def _extract_project_name(context: ClarifiedContext) -> str:
    """提取项目名称"""
    # 简单规则：从核心问题中提取
    if context.core_problem:
        words = context.core_problem.split()
        return " ".join(words[:3]) if len(words) > 3 else context.core_problem
    return "未命名项目"
