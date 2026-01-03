"""
技术栈推荐器 - 20+维度决策矩阵
基于系统规模和需求特征，推荐最佳技术栈组合

P1-2优化：权重配置化，便于后续调整
"""
from typing import List, Tuple, Dict
from core.models import (
    DesignDraft, ScaleAssessment, TechStackRecommendation,
    TechStackItem, TechCategory
)


# ===================== 权重配置（P1-2优化）=====================

class WeightConfig:
    """权重配置类 - 所有评分权重集中管理"""

    # 后端语言评分权重
    BACKEND_PERFORMANCE_WEIGHT = 1.5
    BACKEND_ECOSYSTEM_WEIGHT = 1.3
    BACKEND_SCALABILITY_WEIGHT = 1.2
    BACKEND_TEAM_FAMILIAR_WEIGHT = 1.0

    # 数据库评分权重
    DATABASE_SCALE_WEIGHT = 2.0
    DATABASE_CONSISTENCY_WEIGHT = 1.5
    DATABASE_PERFORMANCE_WEIGHT = 1.3

    # 缓存评分权重
    CACHE_PERFORMANCE_WEIGHT = 1.8
    CACHE_SCALE_WEIGHT = 1.5
    CACHE_SIMPLICITY_WEIGHT = 1.2

    # 消息队列评分权重
    MQ_RELIABILITY_WEIGHT = 1.8
    MQ_THROUGHPUT_WEIGHT = 1.5
    MQ_COMPLEXITY_WEIGHT = 1.0

    # API风格评分权重
    API_SIMPLICITY_WEIGHT = 1.5
    API_PERFORMANCE_WEIGHT = 1.3
    API_ECOSYSTEM_WEIGHT = 1.2


# ===================== 技术栈评分矩阵 =====================

class TechStackRecommender:
    """技术栈推荐器"""

    def __init__(self):
        """初始化推荐器"""
        self.weights = WeightConfig()

    def recommend(self, draft: DesignDraft, scale: ScaleAssessment) -> TechStackRecommendation:
        """
        推荐完整技术栈

        Args:
            draft: 设计草稿
            scale: 规模评估结果

        Returns:
            技术栈推荐
        """
        # 推荐后端语言
        backend = self._recommend_backend_language(scale)

        # 推荐数据库
        database = self._recommend_database(scale, draft)

        # 推荐缓存
        cache = self._recommend_cache(scale)

        # 推荐消息队列
        mq = self._recommend_message_queue(scale)

        # 推荐API风格
        api_style = self._recommend_api_style(scale)

        # 计算总分
        total_score = (
                backend.score +
                database.score +
                cache.score +
                mq.score +
                api_style.score
        ) / 5

        # 生成综合理由
        overall_reasoning = self._generate_overall_reasoning(
            scale, backend, database, cache, mq, api_style
        )

        return TechStackRecommendation(
            backend_language=backend,
            database=database,
            cache=cache,
            message_queue=mq,
            api_style=api_style,
            overall_reasoning=overall_reasoning,
            total_score=total_score
        )

    # ===================== 后端语言推荐 =====================

    def _recommend_backend_language(self, scale: ScaleAssessment) -> TechStackItem:
        """
        推荐后端语言

        评估维度：
        1. 性能需求（权重1.5）
        2. 生态系统（权重1.3）
        3. 可扩展性（权重1.2）
        4. 团队熟悉度（权重1.0）
        """
        candidates = {
            "Python": {
                "performance": 6.0,
                "ecosystem": 10.0,
                "scalability": 7.0,
                "team_familiar": 9.0,
                "scenarios": ["快速开发", "数据处理", "AI/ML集成", "中小型系统"]
            },
            "Java": {
                "performance": 9.0,
                "ecosystem": 10.0,
                "scalability": 10.0,
                "team_familiar": 8.0,
                "scenarios": ["企业级应用", "大型分布式系统", "高并发场景"]
            },
            "Go": {
                "performance": 10.0,
                "ecosystem": 8.0,
                "scalability": 10.0,
                "team_familiar": 6.0,
                "scenarios": ["微服务", "高性能API", "云原生应用"]
            },
            "TypeScript/Node.js": {
                "performance": 7.0,
                "ecosystem": 9.0,
                "scalability": 8.0,
                "team_familiar": 8.0,
                "scenarios": ["全栈开发", "实时应用", "快速原型"]
            }
        }

        # 计算加权得分
        scores = {}
        for lang, metrics in candidates.items():
            score = (
                    metrics["performance"] * self.weights.BACKEND_PERFORMANCE_WEIGHT +
                    metrics["ecosystem"] * self.weights.BACKEND_ECOSYSTEM_WEIGHT +
                    metrics["scalability"] * self.weights.BACKEND_SCALABILITY_WEIGHT +
                    metrics["team_familiar"] * self.weights.BACKEND_TEAM_FAMILIAR_WEIGHT
            )

            # 根据规模调整
            if scale.scale.value == "Large" and lang == "Java":
                score *= 1.2  # 大型系统偏好Java
            elif scale.scale.value == "Small" and lang == "Python":
                score *= 1.2  # 小型系统偏好Python
            elif scale.scale.value == "Medium" and lang == "Go":
                score *= 1.1  # 中型系统偏好Go

            scores[lang] = score

        # 选择最高分
        recommendation = max(scores, key=scores.get)
        alternatives = sorted(
            [k for k in scores.keys() if k != recommendation],
            key=lambda x: scores[x],
            reverse=True
        )[:2]

        # 生成推荐理由
        reasoning = self._generate_backend_reasoning(
            recommendation, scale, candidates[recommendation]
        )

        return TechStackItem(
            category=TechCategory.BACKEND_LANGUAGE,
            recommendation=recommendation,
            alternatives=alternatives,
            score=scores[recommendation],
            reasoning=reasoning
        )

    def _generate_backend_reasoning(self, lang: str, scale: ScaleAssessment,
                                     metrics: dict) -> str:
        """生成后端语言推荐理由"""
        reasons = [
            f"**推荐{lang}作为后端语言**",
            f"- 系统规模：{scale.scale.value}（{scale.estimated_users}用户）",
            f"- 性能评分：{metrics['performance']}/10",
            f"- 生态系统：{metrics['ecosystem']}/10",
            f"- 适用场景：{', '.join(metrics['scenarios'])}"
        ]
        return "\n".join(reasons)

    # ===================== 数据库推荐 =====================

    def _recommend_database(self, scale: ScaleAssessment, draft: DesignDraft) -> TechStackItem:
        """
        推荐数据库

        评估维度：
        1. 规模需求（权重2.0）
        2. 一致性需求（权重1.5）
        3. 性能需求（权重1.3）
        """
        # 判断是否需要关系型特性
        needs_relations = len(draft.aggregates) >= 3 or len(draft.entities) >= 5

        candidates = {
            "PostgreSQL": {
                "scale": 9.0,
                "consistency": 10.0,
                "performance": 8.5,
                "type": "关系型",
                "scenarios": ["复杂查询", "强一致性", "事务处理", "JSONB支持"]
            },
            "MySQL": {
                "scale": 8.5,
                "consistency": 9.0,
                "performance": 8.0,
                "type": "关系型",
                "scenarios": ["传统应用", "读多写少", "成熟稳定"]
            },
            "MongoDB": {
                "scale": 9.5,
                "consistency": 7.0,
                "performance": 9.0,
                "type": "文档型",
                "scenarios": ["灵活Schema", "水平扩展", "高写入量"]
            },
            "Redis + PostgreSQL": {
                "scale": 10.0,
                "consistency": 9.5,
                "performance": 10.0,
                "type": "混合",
                "scenarios": ["高性能", "缓存+持久化", "大型系统"]
            }
        }

        # 计算加权得分
        scores = {}
        for db, metrics in candidates.items():
            score = (
                    metrics["scale"] * self.weights.DATABASE_SCALE_WEIGHT +
                    metrics["consistency"] * self.weights.DATABASE_CONSISTENCY_WEIGHT +
                    metrics["performance"] * self.weights.DATABASE_PERFORMANCE_WEIGHT
            )

            # 根据规模调整
            if scale.scale.value == "Large":
                if "Redis" in db:
                    score *= 1.3
            elif scale.scale.value == "Small":
                if db in ["PostgreSQL", "MySQL"]:
                    score *= 1.2

            # 根据关系需求调整
            if needs_relations and metrics["type"] == "关系型":
                score *= 1.2

            scores[db] = score

        # 选择最高分
        recommendation = max(scores, key=scores.get)
        alternatives = sorted(
            [k for k in scores.keys() if k != recommendation],
            key=lambda x: scores[x],
            reverse=True
        )[:2]

        # 生成推荐理由
        reasoning = self._generate_database_reasoning(
            recommendation, scale, candidates[recommendation], needs_relations
        )

        return TechStackItem(
            category=TechCategory.DATABASE,
            recommendation=recommendation,
            alternatives=alternatives,
            score=scores[recommendation],
            reasoning=reasoning
        )

    def _generate_database_reasoning(self, db: str, scale: ScaleAssessment,
                                      metrics: dict, needs_relations: bool) -> str:
        """生成数据库推荐理由"""
        reasons = [
            f"**推荐{db}作为数据库**",
            f"- 系统规模：{scale.scale.value}（{scale.estimated_entities}个实体）",
            f"- 数据库类型：{metrics['type']}",
            f"- 关系型需求：{'强' if needs_relations else '弱'}",
            f"- 适用场景：{', '.join(metrics['scenarios'])}"
        ]
        return "\n".join(reasons)

    # ===================== 缓存推荐 =====================

    def _recommend_cache(self, scale: ScaleAssessment) -> TechStackItem:
        """
        推荐缓存方案

        评估维度：
        1. 性能需求（权重1.8）
        2. 规模需求（权重1.5）
        3. 简单性（权重1.2）
        """
        candidates = {
            "Redis": {
                "performance": 10.0,
                "scale": 10.0,
                "simplicity": 8.0,
                "scenarios": ["分布式缓存", "会话存储", "排行榜", "消息队列"]
            },
            "Memcached": {
                "performance": 9.5,
                "scale": 9.0,
                "simplicity": 9.5,
                "scenarios": ["简单KV缓存", "高速读取"]
            },
            "In-Memory (Dict/LRU)": {
                "performance": 8.0,
                "scale": 5.0,
                "simplicity": 10.0,
                "scenarios": ["单机应用", "小规模系统", "快速原型"]
            },
            "无需缓存": {
                "performance": 5.0,
                "scale": 3.0,
                "simplicity": 10.0,
                "scenarios": ["超小型系统", "无性能要求"]
            }
        }

        # 计算加权得分
        scores = {}
        for cache, metrics in candidates.items():
            score = (
                    metrics["performance"] * self.weights.CACHE_PERFORMANCE_WEIGHT +
                    metrics["scale"] * self.weights.CACHE_SCALE_WEIGHT +
                    metrics["simplicity"] * self.weights.CACHE_SIMPLICITY_WEIGHT
            )

            # 根据规模调整
            if scale.scale.value == "Large" and cache == "Redis":
                score *= 1.3
            elif scale.scale.value == "Small" and cache == "In-Memory (Dict/LRU)":
                score *= 1.2

            scores[cache] = score

        # 选择最高分
        recommendation = max(scores, key=scores.get)
        alternatives = sorted(
            [k for k in scores.keys() if k != recommendation],
            key=lambda x: scores[x],
            reverse=True
        )[:2]

        # 生成推荐理由
        reasoning = self._generate_cache_reasoning(
            recommendation, scale, candidates[recommendation]
        )

        return TechStackItem(
            category=TechCategory.CACHE,
            recommendation=recommendation,
            alternatives=alternatives,
            score=scores[recommendation],
            reasoning=reasoning
        )

    def _generate_cache_reasoning(self, cache: str, scale: ScaleAssessment,
                                   metrics: dict) -> str:
        """生成缓存推荐理由"""
        reasons = [
            f"**推荐{cache}作为缓存方案**",
            f"- 系统规模：{scale.scale.value}",
            f"- 性能评分：{metrics['performance']}/10",
            f"- 适用场景：{', '.join(metrics['scenarios'])}"
        ]
        return "\n".join(reasons)

    # ===================== 消息队列推荐 =====================

    def _recommend_message_queue(self, scale: ScaleAssessment) -> TechStackItem:
        """
        推荐消息队列

        评估维度：
        1. 可靠性（权重1.8）
        2. 吞吐量（权重1.5）
        3. 复杂度（权重1.0）
        """
        candidates = {
            "RabbitMQ": {
                "reliability": 10.0,
                "throughput": 7.0,
                "complexity": 7.0,
                "scenarios": ["可靠消息传递", "复杂路由", "企业级"]
            },
            "Kafka": {
                "reliability": 9.5,
                "throughput": 10.0,
                "complexity": 6.0,
                "scenarios": ["高吞吐量", "事件流", "大数据"]
            },
            "Redis Pub/Sub": {
                "reliability": 6.0,
                "throughput": 9.0,
                "complexity": 9.0,
                "scenarios": ["轻量级消息", "实时通知", "简单场景"]
            },
            "无需消息队列": {
                "reliability": 5.0,
                "throughput": 5.0,
                "complexity": 10.0,
                "scenarios": ["同步处理", "小型系统"]
            }
        }

        # 计算加权得分
        scores = {}
        for mq, metrics in candidates.items():
            score = (
                    metrics["reliability"] * self.weights.MQ_RELIABILITY_WEIGHT +
                    metrics["throughput"] * self.weights.MQ_THROUGHPUT_WEIGHT +
                    metrics["complexity"] * self.weights.MQ_COMPLEXITY_WEIGHT
            )

            # 根据规模调整
            if scale.scale.value == "Large" and mq == "Kafka":
                score *= 1.3
            elif scale.scale.value == "Small" and mq == "无需消息队列":
                score *= 1.2
            elif scale.scale.value == "Medium" and mq == "RabbitMQ":
                score *= 1.1

            scores[mq] = score

        # 选择最高分
        recommendation = max(scores, key=scores.get)
        alternatives = sorted(
            [k for k in scores.keys() if k != recommendation],
            key=lambda x: scores[x],
            reverse=True
        )[:2]

        # 生成推荐理由
        reasoning = self._generate_mq_reasoning(
            recommendation, scale, candidates[recommendation]
        )

        return TechStackItem(
            category=TechCategory.MESSAGE_QUEUE,
            recommendation=recommendation,
            alternatives=alternatives,
            score=scores[recommendation],
            reasoning=reasoning
        )

    def _generate_mq_reasoning(self, mq: str, scale: ScaleAssessment,
                                metrics: dict) -> str:
        """生成消息队列推荐理由"""
        reasons = [
            f"**推荐{mq}作为消息队列**",
            f"- 系统规模：{scale.scale.value}",
            f"- 可靠性：{metrics['reliability']}/10",
            f"- 适用场景：{', '.join(metrics['scenarios'])}"
        ]
        return "\n".join(reasons)

    # ===================== API风格推荐 =====================

    def _recommend_api_style(self, scale: ScaleAssessment) -> TechStackItem:
        """
        推荐API风格

        评估维度：
        1. 简单性（权重1.5）
        2. 性能（权重1.3）
        3. 生态系统（权重1.2）
        """
        candidates = {
            "RESTful": {
                "simplicity": 9.0,
                "performance": 8.0,
                "ecosystem": 10.0,
                "scenarios": ["CRUD操作", "资源导向", "通用API"]
            },
            "GraphQL": {
                "simplicity": 6.0,
                "performance": 7.0,
                "ecosystem": 8.0,
                "scenarios": ["灵活查询", "前端驱动", "减少请求"]
            },
            "gRPC": {
                "simplicity": 5.0,
                "performance": 10.0,
                "ecosystem": 7.0,
                "scenarios": ["微服务", "高性能", "类型安全"]
            },
            "RESTful + GraphQL": {
                "simplicity": 6.5,
                "performance": 8.5,
                "ecosystem": 9.0,
                "scenarios": ["混合场景", "大型系统", "多客户端"]
            }
        }

        # 计算加权得分
        scores = {}
        for api, metrics in candidates.items():
            score = (
                    metrics["simplicity"] * self.weights.API_SIMPLICITY_WEIGHT +
                    metrics["performance"] * self.weights.API_PERFORMANCE_WEIGHT +
                    metrics["ecosystem"] * self.weights.API_ECOSYSTEM_WEIGHT
            )

            # 根据规模调整
            if scale.scale.value == "Large" and "GraphQL" in api:
                score *= 1.2
            elif scale.scale.value == "Small" and api == "RESTful":
                score *= 1.2
            elif scale.scale.value == "Medium" and api == "gRPC":
                score *= 1.1

            scores[api] = score

        # 选择最高分
        recommendation = max(scores, key=scores.get)
        alternatives = sorted(
            [k for k in scores.keys() if k != recommendation],
            key=lambda x: scores[x],
            reverse=True
        )[:2]

        # 生成推荐理由
        reasoning = self._generate_api_reasoning(
            recommendation, scale, candidates[recommendation]
        )

        return TechStackItem(
            category=TechCategory.API_STYLE,
            recommendation=recommendation,
            alternatives=alternatives,
            score=scores[recommendation],
            reasoning=reasoning
        )

    def _generate_api_reasoning(self, api: str, scale: ScaleAssessment,
                                 metrics: dict) -> str:
        """生成API风格推荐理由"""
        reasons = [
            f"**推荐{api}作为API风格**",
            f"- 系统规模：{scale.scale.value}",
            f"- 简单性：{metrics['simplicity']}/10",
            f"- 性能：{metrics['performance']}/10",
            f"- 适用场景：{', '.join(metrics['scenarios'])}"
        ]
        return "\n".join(reasons)

    # ===================== 综合理由生成 =====================

    def _generate_overall_reasoning(
            self, scale: ScaleAssessment,
            backend: TechStackItem,
            database: TechStackItem,
            cache: TechStackItem,
            mq: TechStackItem,
            api_style: TechStackItem
    ) -> str:
        """生成综合技术栈推荐理由"""
        reasoning = [
            f"## 技术栈推荐总结\n",
            f"**系统规模**：{scale.scale.value}（{scale.estimated_users}用户，{scale.estimated_entities}个实体）\n",
            f"**技术栈组合**：",
            f"- 后端语言：**{backend.recommendation}**",
            f"- 数据库：**{database.recommendation}**",
            f"- 缓存：**{cache.recommendation}**",
            f"- 消息队列：**{mq.recommendation}**",
            f"- API风格：**{api_style.recommendation}**\n",
            f"**核心优势**：",
            f"1. 该技术栈组合适合{scale.scale.value}规模的系统",
            f"2. 后端语言{backend.recommendation}提供了良好的性能和生态支持",
            f"3. {database.recommendation}满足数据存储和一致性需求",
            f"4. {cache.recommendation}提供了必要的性能优化",
            f"5. {api_style.recommendation}符合API设计最佳实践"
        ]

        return "\n".join(reasoning)
