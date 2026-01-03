"""
架构模式选择器 - Lambda条件选择
基于系统规模和特征，选择最适合的架构模式

亮点：使用Lambda表达式定义选择条件，易于扩展
"""
from typing import List, Callable
from core.models import (
    DesignDraft, ScaleAssessment, PatternSelection,
    ArchitecturePattern
)


class PatternSelector:
    """架构模式选择器"""

    def __init__(self):
        """初始化选择器"""
        self.pattern_rules = self._init_pattern_rules()

    def select(self, draft: DesignDraft, scale: ScaleAssessment) -> PatternSelection:
        """
        选择架构模式

        Args:
            draft: 设计草稿
            scale: 规模评估结果

        Returns:
            架构模式选择结果
        """
        # 准备上下文数据
        context = {
            "scale": scale.scale.value,
            "estimated_users": scale.estimated_users,
            "entity_count": len(draft.entities),
            "context_count": len(draft.contexts),
            "feature_count": len(draft.features),
            "aggregate_count": len(draft.aggregates),
            "workflow_count": len(draft.workflows)
        }

        # 评估每个模式的匹配度
        pattern_scores = {}
        for pattern, rule in self.pattern_rules.items():
            score = rule["scorer"](context)
            pattern_scores[pattern] = score

        # 选择最高分的主模式
        primary_pattern = max(pattern_scores, key=pattern_scores.get)

        # 选择支持模式（分数 >= 7的其他模式）
        supporting_patterns = [
            p for p, s in pattern_scores.items()
            if p != primary_pattern and s >= 7.0
        ]

        # 生成推荐理由
        reasoning = self._generate_reasoning(
            primary_pattern, supporting_patterns, context, pattern_scores
        )

        # 评估模式特性
        scalability, complexity, flexibility = self._evaluate_pattern_characteristics(
            primary_pattern, context
        )

        # 生成适用场景
        suitable_for, not_suitable_for = self._generate_scenarios(
            primary_pattern, context
        )

        return PatternSelection(
            primary_pattern=primary_pattern,
            supporting_patterns=supporting_patterns,
            reasoning=reasoning,
            scalability=scalability,
            complexity=complexity,
            flexibility=flexibility,
            suitable_for=suitable_for,
            not_suitable_for=not_suitable_for
        )

    def _init_pattern_rules(self) -> dict:
        """
        初始化架构模式选择规则（Lambda表达式）

        每个规则返回0-10的分数
        """
        return {
            ArchitecturePattern.MONOLITHIC: {
                "scorer": lambda ctx: (
                    10.0 if ctx["scale"] == "Small" else
                    5.0 if ctx["scale"] == "Medium" else
                    2.0
                ),
                "name": "单体架构",
                "description": "所有功能在一个进程中运行"
            },

            ArchitecturePattern.MICROSERVICES: {
                "scorer": lambda ctx: (
                    2.0 if ctx["scale"] == "Small" else
                    7.0 if ctx["scale"] == "Medium" else
                    10.0 if ctx["context_count"] >= 5 else 8.0
                ),
                "name": "微服务架构",
                "description": "按限界上下文拆分为独立服务"
            },

            ArchitecturePattern.HEXAGONAL: {
                "scorer": lambda ctx: (
                    8.0 if ctx["entity_count"] >= 8 and ctx["context_count"] >= 3 else
                    6.0 if ctx["entity_count"] >= 5 else
                    4.0
                ),
                "name": "六边形架构（端口适配器）",
                "description": "核心业务逻辑与外部依赖解耦"
            },

            ArchitecturePattern.CQRS: {
                "scorer": lambda ctx: (
                    9.0 if ctx["scale"] == "Large" and ctx["feature_count"] >= 20 else
                    7.0 if ctx["feature_count"] >= 15 else
                    4.0 if ctx["feature_count"] >= 10 else
                    2.0
                ),
                "name": "CQRS（命令查询职责分离）",
                "description": "读写分离，优化查询性能"
            },

            ArchitecturePattern.EVENT_DRIVEN: {
                "scorer": lambda ctx: (
                    9.0 if ctx["workflow_count"] >= 8 and ctx["context_count"] >= 5 else
                    7.0 if ctx["workflow_count"] >= 5 else
                    5.0 if ctx["workflow_count"] >= 3 else
                    3.0
                ),
                "name": "事件驱动架构",
                "description": "通过事件解耦服务"
            },

            ArchitecturePattern.SERVERLESS: {
                "scorer": lambda ctx: (
                    8.0 if ctx["scale"] == "Small" and ctx["workflow_count"] <= 5 else
                    6.0 if ctx["scale"] == "Small" else
                    3.0
                ),
                "name": "无服务器架构",
                "description": "基于FaaS的按需计算"
            },

            ArchitecturePattern.LAYERED: {
                "scorer": lambda ctx: (
                    9.0 if ctx["scale"] == "Small" and ctx["entity_count"] <= 10 else
                    7.0 if ctx["scale"] == "Medium" and ctx["entity_count"] <= 15 else
                    5.0
                ),
                "name": "分层架构",
                "description": "经典三层/四层架构"
            },

            ArchitecturePattern.CLEAN: {
                "scorer": lambda ctx: (
                    9.0 if ctx["entity_count"] >= 10 and ctx["aggregate_count"] >= 3 else
                    8.0 if ctx["entity_count"] >= 8 else
                    6.0 if ctx["entity_count"] >= 5 else
                    4.0
                ),
                "name": "整洁架构",
                "description": "依赖倒置，业务逻辑在中心"
            }
        }

    def _generate_reasoning(
            self, primary: ArchitecturePattern,
            supporting: List[ArchitecturePattern],
            context: dict,
            scores: dict
    ) -> str:
        """生成架构模式选择理由"""
        reasons = [
            f"## 架构模式选择\n",
            f"**主模式**：{primary.value}（评分：{scores[primary]:.1f}/10）\n",
            f"**系统规模**：{context['scale']}",
            f"- 预估用户：{context['estimated_users']}",
            f"- 实体数量：{context['entity_count']}",
            f"- 限界上下文：{context['context_count']}",
            f"- 功能点：{context['feature_count']}\n",
            f"**选择理由**："
        ]

        # 根据主模式添加具体理由
        if primary == ArchitecturePattern.MONOLITHIC:
            reasons.append(
                f"1. 系统规模为{context['scale']}，适合单体架构快速开发\n"
                f"2. {context['entity_count']}个实体的复杂度可控\n"
                f"3. 单体架构降低部署和运维复杂度"
            )
        elif primary == ArchitecturePattern.MICROSERVICES:
            reasons.append(
                f"1. 系统规模为{context['scale']}，需要良好的可扩展性\n"
                f"2. {context['context_count']}个限界上下文可拆分为独立服务\n"
                f"3. 微服务架构支持团队独立开发和部署"
            )
        elif primary == ArchitecturePattern.HEXAGONAL:
            reasons.append(
                f"1. {context['entity_count']}个实体需要清晰的领域边界\n"
                f"2. 六边形架构提供良好的测试性和可维护性\n"
                f"3. 业务逻辑与基础设施解耦"
            )
        elif primary == ArchitecturePattern.CQRS:
            reasons.append(
                f"1. {context['feature_count']}个功能点，读写分离可优化性能\n"
                f"2. 查询场景复杂，需要独立的查询模型\n"
                f"3. CQRS支持高并发读取"
            )
        elif primary == ArchitecturePattern.EVENT_DRIVEN:
            reasons.append(
                f"1. {context['workflow_count']}个工作流，事件驱动实现解耦\n"
                f"2. 多上下文协作场景多，事件机制降低耦合\n"
                f"3. 支持异步处理和最终一致性"
            )
        elif primary == ArchitecturePattern.SERVERLESS:
            reasons.append(
                f"1. 系统规模小，无服务器架构降低运维成本\n"
                f"2. 按需计费，适合间歇性负载\n"
                f"3. 快速开发和部署"
            )
        elif primary == ArchitecturePattern.LAYERED:
            reasons.append(
                f"1. 经典分层架构，团队熟悉度高\n"
                f"2. {context['entity_count']}个实体，分层结构清晰\n"
                f"3. 适合传统企业应用"
            )
        elif primary == ArchitecturePattern.CLEAN:
            reasons.append(
                f"1. {context['entity_count']}个实体需要严格的依赖管理\n"
                f"2. 整洁架构保证业务逻辑的纯粹性\n"
                f"3. 高测试性和可维护性"
            )

        # 添加支持模式
        if supporting:
            reasons.append(f"\n**支持模式**：{', '.join([p.value for p in supporting])}")
            reasons.append("这些模式可以与主模式结合使用，提供额外的架构优势")

        return "\n".join(reasons)

    def _evaluate_pattern_characteristics(
            self, pattern: ArchitecturePattern, context: dict
    ) -> tuple:
        """
        评估模式特性

        Returns:
            (scalability, complexity, flexibility)
        """
        characteristics = {
            ArchitecturePattern.MONOLITHIC: ("Low", "Low", "Low"),
            ArchitecturePattern.MICROSERVICES: ("High", "High", "High"),
            ArchitecturePattern.HEXAGONAL: ("Medium", "Medium", "High"),
            ArchitecturePattern.CQRS: ("High", "High", "Medium"),
            ArchitecturePattern.EVENT_DRIVEN: ("High", "High", "High"),
            ArchitecturePattern.SERVERLESS: ("High", "Low", "Medium"),
            ArchitecturePattern.LAYERED: ("Low", "Low", "Low"),
            ArchitecturePattern.CLEAN: ("Medium", "Medium", "High")
        }

        return characteristics.get(pattern, ("Medium", "Medium", "Medium"))

    def _generate_scenarios(
            self, pattern: ArchitecturePattern, context: dict
    ) -> tuple:
        """
        生成适用/不适用场景

        Returns:
            (suitable_for, not_suitable_for)
        """
        scenarios = {
            ArchitecturePattern.MONOLITHIC: (
                ["快速原型", "小型团队", "简单业务", "初创项目"],
                ["大规模系统", "多团队协作", "频繁变更"]
            ),
            ArchitecturePattern.MICROSERVICES: (
                ["大型系统", "多团队", "独立部署", "云原生"],
                ["小型项目", "简单业务", "资源受限"]
            ),
            ArchitecturePattern.HEXAGONAL: (
                ["DDD项目", "复杂业务", "高测试性要求", "多适配器场景"],
                ["简单CRUD", "超小型项目"]
            ),
            ArchitecturePattern.CQRS: (
                ["读写分离", "高并发读", "复杂查询", "事件溯源"],
                ["简单业务", "一致性要求高", "小型系统"]
            ),
            ArchitecturePattern.EVENT_DRIVEN: (
                ["异步处理", "服务解耦", "事件溯源", "流处理"],
                ["同步场景", "强一致性", "简单流程"]
            ),
            ArchitecturePattern.SERVERLESS: (
                ["间歇性负载", "快速扩展", "低运维", "事件响应"],
                ["长时间运行", "状态管理", "复杂依赖"]
            ),
            ArchitecturePattern.LAYERED: (
                ["传统应用", "团队熟悉", "简单结构", "企业级"],
                ["微服务", "高扩展性", "复杂领域"]
            ),
            ArchitecturePattern.CLEAN: (
                ["DDD项目", "高质量代码", "长期维护", "复杂业务"],
                ["简单CRUD", "快速原型", "资源受限"]
            )
        }

        return scenarios.get(pattern, (["通用场景"], ["无特殊限制"]))


# ===================== 便捷函数 =====================

def select_architecture_pattern(
        draft: DesignDraft, scale: ScaleAssessment
) -> PatternSelection:
    """
    便捷函数：选择架构模式

    Args:
        draft: 设计草稿
        scale: 规模评估结果

    Returns:
        架构模式选择结果
    """
    selector = PatternSelector()
    return selector.select(draft, scale)
