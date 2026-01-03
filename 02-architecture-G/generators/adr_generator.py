"""
ADR（架构决策记录）生成器
自动生成8个关键架构决策记录

亮点：自动化ADR生成，提升架构文档专业性和可追溯性
"""
from datetime import datetime
from typing import List
from core.models import (
    DesignDraft, ScaleAssessment, TechStackRecommendation,
    PatternSelection, ADRDocument
)


class ADRGenerator:
    """ADR生成器"""

    def generate(
            self,
            draft: DesignDraft,
            scale: ScaleAssessment,
            tech_stack: TechStackRecommendation,
            pattern: PatternSelection
    ) -> List[ADRDocument]:
        """
        生成8个核心ADR

        Args:
            draft: 设计草稿
            scale: 规模评估
            tech_stack: 技术栈推荐
            pattern: 架构模式选择

        Returns:
            ADR文档列表
        """
        current_date = datetime.now().strftime("%Y-%m-%d")

        adrs = [
            self._generate_adr001_architecture_pattern(pattern, scale, current_date),
            self._generate_adr002_backend_language(tech_stack, scale, current_date),
            self._generate_adr003_database_choice(tech_stack, draft, current_date),
            self._generate_adr004_cache_strategy(tech_stack, scale, current_date),
            self._generate_adr005_api_style(tech_stack, pattern, current_date),
            self._generate_adr006_message_queue(tech_stack, scale, current_date),
            self._generate_adr007_ddd_implementation(draft, pattern, current_date),
            self._generate_adr008_deployment_strategy(scale, pattern, current_date)
        ]

        return adrs

    def _generate_adr001_architecture_pattern(
            self, pattern: PatternSelection, scale: ScaleAssessment, date: str
    ) -> ADRDocument:
        """ADR-001: 架构模式选择"""
        return ADRDocument(
            adr_id="ADR-001",
            title="架构模式选择",
            date=date,
            status="Accepted",
            context=(
                f"系统规模为{scale.scale.value}，预计{scale.estimated_users}用户，"
                f"{scale.estimated_entities}个核心实体，{scale.estimated_contexts}个限界上下文。"
                f"需要选择合适的架构模式来支持系统的可扩展性、可维护性和性能需求。"
            ),
            decision=(
                f"采用**{pattern.primary_pattern.value}**作为主架构模式。\n\n"
                f"**模式特性**：\n"
                f"- 可扩展性：{pattern.scalability}\n"
                f"- 复杂度：{pattern.complexity}\n"
                f"- 灵活性：{pattern.flexibility}\n\n"
                f"**支持模式**：{', '.join([p.value for p in pattern.supporting_patterns]) if pattern.supporting_patterns else '无'}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 适合{scale.scale.value}规模的系统\n"
                f"- 可扩展性达到{pattern.scalability}级别\n"
                f"- 支持以下场景：{', '.join(pattern.suitable_for)}\n\n"
                f"**负面影响**：\n"
                f"- 复杂度为{pattern.complexity}级别\n"
                f"- 不适合以下场景：{', '.join(pattern.not_suitable_for)}"
            ),
            alternatives=[
                p.value for p in pattern.supporting_patterns
            ] if pattern.supporting_patterns else None
        )

    def _generate_adr002_backend_language(
            self, tech_stack: TechStackRecommendation, scale: ScaleAssessment, date: str
    ) -> ADRDocument:
        """ADR-002: 后端语言选择"""
        backend = tech_stack.backend_language

        return ADRDocument(
            adr_id="ADR-002",
            title="后端语言选择",
            date=date,
            status="Accepted",
            context=(
                f"系统规模为{scale.scale.value}，需要选择性能优秀、生态丰富、团队熟悉的后端语言。"
                f"需要考虑开发效率、运行性能、可维护性等多方面因素。"
            ),
            decision=(
                f"选择**{backend.recommendation}**作为后端开发语言。\n\n"
                f"**评分**：{backend.score:.1f}/10\n\n"
                f"**理由**：\n{backend.reasoning}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 适合{scale.scale.value}规模的系统开发\n"
                f"- 拥有丰富的生态系统和成熟的框架\n"
                f"- 团队熟悉度高，降低学习成本\n\n"
                f"**负面影响**：\n"
                f"- 需要遵循该语言的最佳实践\n"
                f"- 可能需要针对性能进行优化"
            ),
            alternatives=backend.alternatives
        )

    def _generate_adr003_database_choice(
            self, tech_stack: TechStackRecommendation, draft: DesignDraft, date: str
    ) -> ADRDocument:
        """ADR-003: 数据库选择"""
        database = tech_stack.database

        return ADRDocument(
            adr_id="ADR-003",
            title="数据库技术选择",
            date=date,
            status="Accepted",
            context=(
                f"系统包含{len(draft.entities)}个实体，{len(draft.aggregates)}个聚合根。"
                f"需要选择合适的数据库来存储和管理数据，同时满足性能、一致性和可扩展性需求。"
            ),
            decision=(
                f"选择**{database.recommendation}**作为主数据库。\n\n"
                f"**评分**：{database.score:.1f}/10\n\n"
                f"**理由**：\n{database.reasoning}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 满足数据存储和查询需求\n"
                f"- 支持事务和数据一致性\n"
                f"- 可扩展性良好\n\n"
                f"**负面影响**：\n"
                f"- 需要设计合理的表结构或文档结构\n"
                f"- 需要考虑查询优化和索引设计"
            ),
            alternatives=database.alternatives
        )

    def _generate_adr004_cache_strategy(
            self, tech_stack: TechStackRecommendation, scale: ScaleAssessment, date: str
    ) -> ADRDocument:
        """ADR-004: 缓存策略"""
        cache = tech_stack.cache

        return ADRDocument(
            adr_id="ADR-004",
            title="缓存策略选择",
            date=date,
            status="Accepted",
            context=(
                f"系统规模为{scale.scale.value}，需要优化读取性能和降低数据库压力。"
                f"需要选择合适的缓存方案来提升系统响应速度。"
            ),
            decision=(
                f"采用**{cache.recommendation}**作为缓存方案。\n\n"
                f"**评分**：{cache.score:.1f}/10\n\n"
                f"**理由**：\n{cache.reasoning}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 显著提升读取性能\n"
                f"- 降低数据库负载\n"
                f"- 支持高并发访问\n\n"
                f"**负面影响**：\n"
                f"- 需要处理缓存一致性问题\n"
                f"- 需要设计缓存更新策略"
            ),
            alternatives=cache.alternatives
        )

    def _generate_adr005_api_style(
            self, tech_stack: TechStackRecommendation, pattern: PatternSelection, date: str
    ) -> ADRDocument:
        """ADR-005: API设计风格"""
        api_style = tech_stack.api_style

        return ADRDocument(
            adr_id="ADR-005",
            title="API设计风格选择",
            date=date,
            status="Accepted",
            context=(
                f"采用{pattern.primary_pattern.value}架构模式，需要设计清晰的API接口。"
                f"需要选择合适的API风格来满足前后端通信、服务间通信的需求。"
            ),
            decision=(
                f"采用**{api_style.recommendation}**作为API设计风格。\n\n"
                f"**评分**：{api_style.score:.1f}/10\n\n"
                f"**理由**：\n{api_style.reasoning}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 前后端接口清晰明确\n"
                f"- 生态系统成熟，工具链完善\n"
                f"- 易于文档化和测试\n\n"
                f"**负面影响**：\n"
                f"- 需要遵循API设计规范\n"
                f"- 需要考虑版本管理和兼容性"
            ),
            alternatives=api_style.alternatives
        )

    def _generate_adr006_message_queue(
            self, tech_stack: TechStackRecommendation, scale: ScaleAssessment, date: str
    ) -> ADRDocument:
        """ADR-006: 消息队列选择"""
        mq = tech_stack.message_queue

        return ADRDocument(
            adr_id="ADR-006",
            title="消息队列技术选择",
            date=date,
            status="Accepted",
            context=(
                f"系统规模为{scale.scale.value}，需要处理异步任务和服务间通信。"
                f"需要选择合适的消息队列来解耦服务、提升系统弹性。"
            ),
            decision=(
                f"采用**{mq.recommendation}**作为消息队列方案。\n\n"
                f"**评分**：{mq.score:.1f}/10\n\n"
                f"**理由**：\n{mq.reasoning}"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 服务解耦，提升系统弹性\n"
                f"- 支持异步处理，提升响应速度\n"
                f"- 消息可靠传递\n\n"
                f"**负面影响**：\n"
                f"- 增加系统复杂度\n"
                f"- 需要处理消息幂等性和顺序性"
            ),
            alternatives=mq.alternatives
        )

    def _generate_adr007_ddd_implementation(
            self, draft: DesignDraft, pattern: PatternSelection, date: str
    ) -> ADRDocument:
        """ADR-007: DDD实施策略"""
        return ADRDocument(
            adr_id="ADR-007",
            title="领域驱动设计（DDD）实施",
            date=date,
            status="Accepted",
            context=(
                f"系统包含{len(draft.entities)}个实体、{len(draft.aggregates)}个聚合根、"
                f"{len(draft.contexts)}个限界上下文。采用{pattern.primary_pattern.value}架构模式。"
                f"需要明确DDD的实施策略和边界。"
            ),
            decision=(
                f"采用**战术DDD**进行领域建模，明确以下要素：\n\n"
                f"**实体（Entity）**：{len(draft.entities)}个\n"
                f"- {', '.join([e['name'] for e in draft.entities[:5]])}"
                f"{'等' if len(draft.entities) > 5 else ''}\n\n"
                f"**聚合根（Aggregate Root）**：{len(draft.aggregates)}个\n"
                f"- {', '.join([a['name'] for a in draft.aggregates])}\n\n"
                f"**限界上下文（Bounded Context）**：{len(draft.contexts)}个\n"
                f"- {', '.join([c['name'] for c in draft.contexts])}\n\n"
                f"**值对象（Value Object）**：{len(draft.value_objects)}个"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 领域边界清晰，职责明确\n"
                f"- 聚合根保证业务一致性\n"
                f"- 上下文映射明确服务边界\n"
                f"- 值对象保证领域模型纯粹性\n\n"
                f"**负面影响**：\n"
                f"- 需要团队理解DDD概念\n"
                f"- 初期建模成本较高"
            )
        )

    def _generate_adr008_deployment_strategy(
            self, scale: ScaleAssessment, pattern: PatternSelection, date: str
    ) -> ADRDocument:
        """ADR-008: 部署策略"""
        # 根据规模和模式推荐部署策略
        if scale.scale.value == "Large" or pattern.primary_pattern.value == "Microservices":
            deployment = "Kubernetes容器化部署"
            reasoning = "大型系统或微服务架构，需要容器编排和自动化运维"
        elif scale.scale.value == "Medium":
            deployment = "Docker Compose或轻量级K8s（K3s）"
            reasoning = "中型系统，使用容器化但不需要复杂的编排"
        else:
            deployment = "传统虚拟机部署或Serverless"
            reasoning = "小型系统，选择简单的部署方式降低运维成本"

        return ADRDocument(
            adr_id="ADR-008",
            title="部署策略选择",
            date=date,
            status="Accepted",
            context=(
                f"系统规模为{scale.scale.value}，采用{pattern.primary_pattern.value}架构模式。"
                f"需要选择合适的部署策略来保证系统的可用性、可扩展性和运维效率。"
            ),
            decision=(
                f"采用**{deployment}**作为部署策略。\n\n"
                f"**理由**：{reasoning}\n\n"
                f"**部署要素**：\n"
                f"- CI/CD流水线自动化\n"
                f"- 蓝绿部署或金丝雀发布\n"
                f"- 健康检查和自动恢复\n"
                f"- 日志收集和监控告警"
            ),
            consequences=(
                f"**正面影响**：\n"
                f"- 自动化部署，降低人为错误\n"
                f"- 支持快速回滚\n"
                f"- 弹性伸缩，应对流量波动\n\n"
                f"**负面影响**：\n"
                f"- 需要建设DevOps能力\n"
                f"- 初期基础设施投入较大"
            )
        )


# ===================== 便捷函数 =====================

def generate_adrs(
        draft: DesignDraft,
        scale: ScaleAssessment,
        tech_stack: TechStackRecommendation,
        pattern: PatternSelection
) -> List[ADRDocument]:
    """
    便捷函数：生成ADR列表

    Args:
        draft: 设计草稿
        scale: 规模评估
        tech_stack: 技术栈推荐
        pattern: 架构模式选择

    Returns:
        ADR文档列表
    """
    generator = ADRGenerator()
    return generator.generate(draft, scale, tech_stack, pattern)
