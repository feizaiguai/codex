"""
架构文档生成器
生成完整的ARCHITECTURE.md文档，输出给35-specflow

P1-3优化：补充演化路径生成逻辑
"""
from datetime import datetime
from typing import List, Dict
from core.models import (
    DesignDraft, ArchitectureDesign, ScaleAssessment,
    TechStackRecommendation, PatternSelection, ADRDocument
)


class ArchitectureDocGenerator:
    """架构文档生成器"""

    def generate(
            self,
            project_name: str,
            draft: DesignDraft,
            architecture: ArchitectureDesign
    ) -> str:
        """
        生成ARCHITECTURE.md文档

        Args:
            project_name: 项目名称
            draft: 设计草稿
            architecture: 架构设计

        Returns:
            Markdown文档内容
        """
        sections = []

        # 文档头部
        sections.append(self._generate_header(project_name, architecture))

        # 第1章：架构概述
        sections.append(self._generate_chapter1_overview(
            draft, architecture.scale_assessment, architecture.pattern_selection
        ))

        # 第2章：规模评估
        sections.append(self._generate_chapter2_scale_assessment(
            architecture.scale_assessment
        ))

        # 第3章：技术栈选择
        sections.append(self._generate_chapter3_tech_stack(
            architecture.tech_stack
        ))

        # 第4章：架构模式
        sections.append(self._generate_chapter4_architecture_pattern(
            architecture.pattern_selection
        ))

        # 第5章：领域模型
        sections.append(self._generate_chapter5_domain_model(draft))

        # 第6章：架构决策记录（ADR）
        sections.append(self._generate_chapter6_adrs(architecture.adrs))

        # 第7章：实施计划
        sections.append(self._generate_chapter7_implementation(
            architecture.implementation_phases
        ))

        # 第8章：演化路径（P1-3优化）
        sections.append(self._generate_chapter8_evolution(
            architecture.scale_assessment, architecture.pattern_selection
        ))

        # 第9章：与35-specflow集成
        sections.append(self._generate_chapter9_integration(
            architecture.scale_assessment, architecture.tech_stack
        ))

        return "\n\n".join(sections)

    def _generate_header(
            self, project_name: str, architecture: ArchitectureDesign
    ) -> str:
        """生成文档头部"""
        return f"""# {project_name} - 架构设计文档

**版本**: {architecture.version}
**日期**: {architecture.date}
**状态**: 已批准

---

## 文档说明

本文档由 **02-architecture** 自动生成，基于 **01-spec-explorer** 的设计草稿。
本文档将作为 **35-specflow** 的输入，用于生成详细的技术规格。

**文档结构**：
1. 架构概述
2. 规模评估
3. 技术栈选择
4. 架构模式
5. 领域模型
6. 架构决策记录（ADR）
7. 实施计划
8. 演化路径
9. 与35-specflow集成"""

    def _generate_chapter1_overview(
            self, draft: DesignDraft, scale: ScaleAssessment,
            pattern: PatternSelection
    ) -> str:
        """第1章：架构概述"""
        return f"""## 1. 架构概述

### 1.1 项目信息

- **项目名称**: {draft.project_name}
- **核心价值**: {draft.core_value}
- **目标用户**: {draft.target_users}
- **用户规模**: {draft.user_scale}

### 1.2 系统规模

- **规模等级**: {scale.scale.value}
- **评估得分**: {scale.score:.1f}/50
- **复杂度**: {scale.complexity_level}
- **预估用户数**: {scale.estimated_users}
- **核心实体数**: {scale.estimated_entities}
- **限界上下文**: {scale.estimated_contexts}

### 1.3 架构风格

- **主架构模式**: {pattern.primary_pattern.value}
- **支持模式**: {', '.join([p.value for p in pattern.supporting_patterns]) if pattern.supporting_patterns else '无'}
- **可扩展性**: {pattern.scalability}
- **复杂度**: {pattern.complexity}
- **灵活性**: {pattern.flexibility}"""

    def _generate_chapter2_scale_assessment(
            self, scale: ScaleAssessment
    ) -> str:
        """第2章：规模评估"""
        details_md = "\n".join([
            f"- **{key}**: {value['score']:.1f}分"
            for key, value in scale.details.items()
        ])

        return f"""## 2. 规模评估

### 2.1 评估结果

{scale.reasoning}

### 2.2 详细评分

{details_md}

**总分**: {scale.score:.1f}/50
**等级**: {scale.scale.value}

### 2.3 规模指标

| 指标 | 数值 |
|------|------|
| 预估用户数 | {scale.estimated_users} |
| 核心实体数 | {scale.estimated_entities} |
| 限界上下文数 | {scale.estimated_contexts} |
| 复杂度等级 | {scale.complexity_level} |"""

    def _generate_chapter3_tech_stack(
            self, tech_stack: TechStackRecommendation
    ) -> str:
        """第3章：技术栈选择"""
        return f"""## 3. 技术栈选择

### 3.1 技术栈总览

| 类别 | 推荐技术 | 备选方案 | 评分 |
|------|---------|---------|------|
| 后端语言 | {tech_stack.backend_language.recommendation} | {', '.join(tech_stack.backend_language.alternatives)} | {tech_stack.backend_language.score:.1f} |
| 数据库 | {tech_stack.database.recommendation} | {', '.join(tech_stack.database.alternatives)} | {tech_stack.database.score:.1f} |
| 缓存 | {tech_stack.cache.recommendation} | {', '.join(tech_stack.cache.alternatives)} | {tech_stack.cache.score:.1f} |
| 消息队列 | {tech_stack.message_queue.recommendation} | {', '.join(tech_stack.message_queue.alternatives)} | {tech_stack.message_queue.score:.1f} |
| API风格 | {tech_stack.api_style.recommendation} | {', '.join(tech_stack.api_style.alternatives)} | {tech_stack.api_style.score:.1f} |

### 3.2 后端语言

{tech_stack.backend_language.reasoning}

### 3.3 数据库

{tech_stack.database.reasoning}

### 3.4 缓存方案

{tech_stack.cache.reasoning}

### 3.5 消息队列

{tech_stack.message_queue.reasoning}

### 3.6 API设计

{tech_stack.api_style.reasoning}

### 3.7 综合评估

{tech_stack.overall_reasoning}

**综合评分**: {tech_stack.total_score:.1f}/10"""

    def _generate_chapter4_architecture_pattern(
            self, pattern: PatternSelection
    ) -> str:
        """第4章：架构模式"""
        return f"""## 4. 架构模式

### 4.1 模式选择

{pattern.reasoning}

### 4.2 模式特性

| 特性 | 评级 |
|------|------|
| 可扩展性 | {pattern.scalability} |
| 复杂度 | {pattern.complexity} |
| 灵活性 | {pattern.flexibility} |

### 4.3 适用场景

**适合以下场景**：
{chr(10).join(['- ' + s for s in pattern.suitable_for])}

**不适合以下场景**：
{chr(10).join(['- ' + s for s in pattern.not_suitable_for])}

### 4.4 支持模式

{f"本架构同时采用以下支持模式：{', '.join([p.value for p in pattern.supporting_patterns])}" if pattern.supporting_patterns else "无需额外支持模式"}"""

    def _generate_chapter5_domain_model(self, draft: DesignDraft) -> str:
        """第5章：领域模型"""
        # 实体列表
        entities_md = "\n".join([
            f"- **{e['name']}**: {len(e.get('attributes', []))}个属性"
            for e in draft.entities
        ])

        # 聚合根列表
        aggregates_md = "\n".join([
            f"- **{a['name']}**: 包含 {', '.join(a.get('entities', []))}"
            for a in draft.aggregates
        ]) if draft.aggregates else "- 无聚合根定义"

        # 限界上下文列表
        contexts_md = "\n".join([
            f"### {c['name']}\n\n包含实体：{', '.join(c.get('entities', []))}"
            for c in draft.contexts
        ])

        return f"""## 5. 领域模型

### 5.1 核心实体（{len(draft.entities)}个）

{entities_md}

### 5.2 聚合根（{len(draft.aggregates)}个）

{aggregates_md}

### 5.3 值对象（{len(draft.value_objects)}个）

{', '.join(draft.value_objects) if draft.value_objects else '无值对象定义'}

### 5.4 限界上下文（{len(draft.contexts)}个）

{contexts_md}"""

    def _generate_chapter6_adrs(self, adrs: List[ADRDocument]) -> str:
        """第6章：架构决策记录"""
        # ADR索引
        adr_index = "\n".join([
            f"{i + 1}. [{adr.adr_id}]（{adr.title}） - {adr.status}"
            for i, adr in enumerate(adrs)
        ])

        # 所有ADR的完整内容
        adr_contents = "\n\n---\n\n".join([
            adr.to_markdown() for adr in adrs
        ])

        return f"""## 6. 架构决策记录（ADR）

### 6.1 ADR索引

{adr_index}

### 6.2 详细记录

{adr_contents}"""

    def _generate_chapter7_implementation(
            self, phases: List[Dict]
    ) -> str:
        """第7章：实施计划"""
        if not phases:
            # 如果没有提供实施计划，生成默认的
            phases = self._generate_default_implementation_phases()

        phases_md = "\n\n".join([
            f"### {phase['name']}\n\n"
            f"**目标**: {phase['goal']}\n\n"
            f"**任务**:\n{chr(10).join(['- ' + t for t in phase['tasks']])}\n\n"
            f"**产出**: {phase['deliverable']}"
            for phase in phases
        ])

        return f"""## 7. 实施计划

{phases_md}"""

    def _generate_chapter8_evolution(
            self, scale: ScaleAssessment, pattern: PatternSelection
    ) -> str:
        """
        第8章：演化路径（P1-3优化）
        根据系统规模自动生成演化路径
        """
        # 根据规模生成演化路径
        if scale.scale.value == "Small":
            evolution_path = self._generate_small_system_evolution()
        elif scale.scale.value == "Medium":
            evolution_path = self._generate_medium_system_evolution(pattern)
        else:  # Large
            evolution_path = self._generate_large_system_evolution(pattern)

        return f"""## 8. 演化路径

### 8.1 系统演化策略

{evolution_path}

### 8.2 关键里程碑

1. **MVP阶段**（1-3个月）
   - 核心功能实现
   - 基础架构搭建
   - 小规模用户验证

2. **成长阶段**（3-6个月）
   - 功能完善
   - 性能优化
   - 用户规模增长

3. **成熟阶段**（6-12个月）
   - 架构优化
   - 高可用保障
   - 大规模用户支持

4. **优化阶段**（12个月+）
   - 持续改进
   - 技术债务清理
   - 架构演化升级"""

    def _generate_small_system_evolution(self) -> str:
        """小型系统演化路径"""
        return """**小型系统演化策略**：

**阶段1: 单体快速开发（0-3个月）**
- 采用单体架构，快速实现MVP
- 使用轻量级技术栈，降低开发成本
- 专注核心功能，快速验证商业模式

**阶段2: 功能迭代（3-6个月）**
- 根据用户反馈迭代功能
- 优化用户体验
- 保持单体架构，避免过早优化

**阶段3: 性能优化（6-12个月）**
- 引入缓存机制
- 数据库查询优化
- 前端性能优化

**未来演化方向**：
如果系统规模增长超过预期（用户数>1万），考虑：
- 引入微服务架构
- 服务拆分和解耦
- 引入消息队列处理异步任务"""

    def _generate_medium_system_evolution(self, pattern: PatternSelection) -> str:
        """中型系统演化路径"""
        if pattern.primary_pattern.value == "Microservices":
            return """**中型系统演化策略（微服务）**：

**阶段1: 微服务基础架构（0-3个月）**
- 搭建服务注册与发现
- 配置API网关
- 实现核心服务拆分（按限界上下文）

**阶段2: 服务完善（3-6个月）**
- 补充支撑服务
- 引入服务监控和链路追踪
- 实现服务熔断和降级

**阶段3: 高可用保障（6-12个月）**
- 部署多区域容灾
- 实现自动扩缩容
- 完善监控告警体系

**未来演化方向**：
- 引入Service Mesh（如Istio）
- 容器化部署（Kubernetes）
- 事件驱动架构增强"""
        else:
            return """**中型系统演化策略（分层/六边形）**：

**阶段1: 架构分层（0-3个月）**
- 明确分层边界
- 实现核心业务逻辑
- 配置基础设施

**阶段2: 模块化增强（3-6个月）**
- 按领域拆分模块
- 模块间接口标准化
- 引入DDD战术模式

**阶段3: 性能与可用性（6-12个月）**
- 引入缓存和消息队列
- 数据库读写分离
- 部署高可用架构

**未来演化方向**：
如果系统继续扩展，考虑：
- 模块拆分为微服务
- 引入CQRS模式
- 事件驱动架构"""

    def _generate_large_system_evolution(self, pattern: PatternSelection) -> str:
        """大型系统演化路径"""
        return """**大型系统演化策略**：

**阶段1: 微服务架构（0-6个月）**
- 完整的微服务基础设施
- 服务网格（Service Mesh）
- 分布式追踪和监控
- 自动化CI/CD流水线

**阶段2: 高性能架构（6-12个月）**
- 引入CQRS模式（读写分离）
- 事件溯源（Event Sourcing）
- 多级缓存架构（本地+分布式）
- 数据库分库分表

**阶段3: 全球化部署（12-18个月）**
- 多地域部署
- CDN加速
- 跨区域数据同步
- 容灾和备份策略

**阶段4: 持续优化（18个月+）**
- AI/ML集成（智能推荐、预测）
- 成本优化（资源调度）
- 技术栈升级
- 架构重构和债务清理

**未来演化方向**：
- Serverless化改造（部分场景）
- 边缘计算
- 云原生技术栈全面应用"""

    def _generate_chapter9_integration(
            self, scale: ScaleAssessment, tech_stack: TechStackRecommendation
    ) -> str:
        """第9章：与35-specflow集成"""
        return f"""## 9. 与35-specflow集成

### 9.1 输出元数据

本文档将作为35-specflow的输入，提供以下元数据：

**系统规模**:
- 规模等级: {scale.scale.value}
- 复杂度: {scale.complexity_level}
- 预估用户: {scale.estimated_users}
- 核心实体: {scale.estimated_entities}

**技术栈**:
- 后端语言: {tech_stack.backend_language.recommendation}
- 数据库: {tech_stack.database.recommendation}
- 缓存: {tech_stack.cache.recommendation}
- API风格: {tech_stack.api_style.recommendation}

### 9.2 35-specflow需要的输入

35-specflow将基于本文档生成以下规格文档：

1. **SPEC_FLOW.md** - 核心业务流程规格
2. **SPEC_API.md** - API接口规格
3. **SPEC_DATA.md** - 数据模型规格
4. **SPEC_TECH.md** - 技术实现规格
5. **SPEC_SECURITY.md** - 安全规格
6. **SPEC_PERFORMANCE.md** - 性能规格
7. **SPEC_DEPLOYMENT.md** - 部署规格
8. **SPEC_TEST.md** - 测试规格

### 9.3 注意事项

- 35-specflow需要升级以支持双输入（DESIGN_DRAFT.md + ARCHITECTURE.md）
- 本文档提供的技术栈信息将覆盖35-specflow的默认选择
- ADR记录将被纳入SPEC_TECH.md中

---

**文档生成完成**
**下一步**: 将本文档传递给35-specflow进行详细规格生成"""

    def _generate_default_implementation_phases(self) -> List[Dict]:
        """生成默认实施阶段"""
        return [
            {
                "name": "阶段1: 基础架构搭建（Week 1-2）",
                "goal": "搭建项目基础架构和开发环境",
                "tasks": [
                    "初始化项目结构",
                    "配置开发环境",
                    "搭建CI/CD流水线",
                    "配置数据库和缓存"
                ],
                "deliverable": "可运行的项目骨架"
            },
            {
                "name": "阶段2: 核心功能开发（Week 3-6）",
                "goal": "实现核心业务功能",
                "tasks": [
                    "实现领域模型",
                    "开发核心API接口",
                    "实现业务逻辑",
                    "编写单元测试"
                ],
                "deliverable": "核心功能MVP"
            },
            {
                "name": "阶段3: 集成与测试（Week 7-8）",
                "goal": "系统集成和全面测试",
                "tasks": [
                    "集成测试",
                    "性能测试",
                    "安全测试",
                    "用户验收测试"
                ],
                "deliverable": "经过测试的完整系统"
            },
            {
                "name": "阶段4: 部署与上线（Week 9-10）",
                "goal": "系统部署和上线",
                "tasks": [
                    "生产环境部署",
                    "监控和告警配置",
                    "文档完善",
                    "团队培训"
                ],
                "deliverable": "生产环境运行的系统"
            }
        ]


# ===================== 便捷函数 =====================

def generate_architecture_document(
        project_name: str,
        draft: DesignDraft,
        architecture: ArchitectureDesign
) -> str:
    """
    便捷函数：生成架构文档

    Args:
        project_name: 项目名称
        draft: 设计草稿
        architecture: 架构设计

    Returns:
        Markdown文档内容
    """
    generator = ArchitectureDocGenerator()
    return generator.generate(project_name, draft, architecture)
