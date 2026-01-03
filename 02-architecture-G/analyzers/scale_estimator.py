"""
规模评估器 - 10条评估规则
基于需求分析，评估系统规模（Small/Medium/Large）
"""
import re
from typing import Tuple
from core.models import DesignDraft, ScaleAssessment, ScaleType


class ScaleEstimator:
    """
    系统规模评估器

    评分规则（总分50分）：
    - Small: < 11分
    - Medium: 11-20分
    - Large: > 20分
    """

    def estimate(self, draft: DesignDraft) -> ScaleAssessment:
        """
        评估系统规模

        Args:
            draft: 设计草稿

        Returns:
            规模评估结果
        """
        total_score = 0.0
        details = {}
        reasoning_parts = []

        # R1: 用户规模（最高5分）
        score, detail, reason = self._rule_r1_user_scale(draft.user_scale, draft.target_users)
        total_score += score
        details["R1_用户规模"] = detail
        reasoning_parts.append(reason)

        # R2: 实体复杂度（最高5分）
        score, detail, reason = self._rule_r2_entity_complexity(draft.entities)
        total_score += score
        details["R2_实体复杂度"] = detail
        reasoning_parts.append(reason)

        # R3: 功能点数量（最高5分）
        score, detail, reason = self._rule_r3_feature_count(draft.features)
        total_score += score
        details["R3_功能点数量"] = detail
        reasoning_parts.append(reason)

        # R4: 上下文数量（最高5分）
        score, detail, reason = self._rule_r4_context_count(draft.contexts)
        total_score += score
        details["R4_上下文数量"] = detail
        reasoning_parts.append(reason)

        # R5: 聚合根复杂度（最高5分）
        score, detail, reason = self._rule_r5_aggregate_complexity(draft.aggregates, draft.entities)
        total_score += score
        details["R5_聚合根复杂度"] = detail
        reasoning_parts.append(reason)

        # R6: 工作流复杂度（最高5分）
        score, detail, reason = self._rule_r6_workflow_complexity(draft.workflows)
        total_score += score
        details["R6_工作流复杂度"] = detail
        reasoning_parts.append(reason)

        # R7: 优先级分布（最高5分）
        score, detail, reason = self._rule_r7_priority_distribution(draft.features)
        total_score += score
        details["R7_优先级分布"] = detail
        reasoning_parts.append(reason)

        # R8: 用户故事数量（最高5分）
        score, detail, reason = self._rule_r8_user_story_count(draft.user_stories)
        total_score += score
        details["R8_用户故事数量"] = detail
        reasoning_parts.append(reason)

        # R9: 值对象使用（最高5分）
        score, detail, reason = self._rule_r9_value_object_usage(draft.value_objects)
        total_score += score
        details["R9_值对象使用"] = detail
        reasoning_parts.append(reason)

        # R10: 业务复杂度（最高5分）
        score, detail, reason = self._rule_r10_business_complexity(draft)
        total_score += score
        details["R10_业务复杂度"] = detail
        reasoning_parts.append(reason)

        # 确定规模等级
        if total_score < 11:
            scale = ScaleType.SMALL
            scale_desc = "小型系统"
        elif total_score <= 20:
            scale = ScaleType.MEDIUM
            scale_desc = "中型系统"
        else:
            scale = ScaleType.LARGE
            scale_desc = "大型系统"

        # 估算具体指标
        estimated_users = self._estimate_user_count(draft.user_scale)
        estimated_entities = len(draft.entities)
        estimated_contexts = len(draft.contexts)

        # 复杂度等级
        if total_score < 11:
            complexity_level = "Low"
        elif total_score <= 25:
            complexity_level = "Medium"
        else:
            complexity_level = "High"

        # 生成综合评估理由
        reasoning = f"{scale_desc}（总分：{total_score:.1f}/50）\n\n" + "\n".join(reasoning_parts)

        return ScaleAssessment(
            scale=scale,
            score=total_score,
            details=details,
            reasoning=reasoning,
            estimated_users=estimated_users,
            estimated_entities=estimated_entities,
            estimated_contexts=estimated_contexts,
            complexity_level=complexity_level
        )

    # ===================== 10条评估规则 =====================

    def _rule_r1_user_scale(self, user_scale: str, target_users: str) -> Tuple[float, dict, str]:
        """
        R1: 用户规模（0-5分）
        - < 100: 1分
        - 100-1000: 2分
        - 1000-10000: 3分
        - 10000-100000: 4分
        - > 100000: 5分
        """
        # 提取数字
        numbers = re.findall(r'(\d+)', user_scale + " " + target_users)
        if not numbers:
            score = 1.0
            user_count = 50
            reason = "R1: 用户规模未明确，默认小规模（1分）"
        else:
            user_count = int(numbers[-1])  # 取最大值

            if user_count < 100:
                score = 1.0
            elif user_count < 1000:
                score = 2.0
            elif user_count < 10000:
                score = 3.0
            elif user_count < 100000:
                score = 4.0
            else:
                score = 5.0

            reason = f"R1: 用户规模约{user_count}人 → {score}分"

        detail = {"score": score, "user_count": user_count}
        return score, detail, reason

    def _rule_r2_entity_complexity(self, entities: list) -> Tuple[float, dict, str]:
        """
        R2: 实体复杂度（0-5分）
        - 实体数量 + 平均属性数量
        - < 5实体: 1分
        - 5-10实体: 2分
        - 10-20实体: 3分
        - 20-30实体: 4分
        - > 30实体: 5分
        """
        entity_count = len(entities)

        if entity_count < 5:
            score = 1.0
        elif entity_count < 10:
            score = 2.0
        elif entity_count < 20:
            score = 3.0
        elif entity_count < 30:
            score = 4.0
        else:
            score = 5.0

        # 计算平均属性数
        total_attrs = sum(len(e.get("attributes", [])) for e in entities)
        avg_attrs = total_attrs / entity_count if entity_count > 0 else 0

        reason = f"R2: {entity_count}个实体，平均{avg_attrs:.1f}个属性 → {score}分"
        detail = {"score": score, "entity_count": entity_count, "avg_attributes": avg_attrs}

        return score, detail, reason

    def _rule_r3_feature_count(self, features: list) -> Tuple[float, dict, str]:
        """
        R3: 功能点数量（0-5分）
        - < 5: 1分
        - 5-10: 2分
        - 10-20: 3分
        - 20-30: 4分
        - > 30: 5分
        """
        feature_count = len(features)

        if feature_count < 5:
            score = 1.0
        elif feature_count < 10:
            score = 2.0
        elif feature_count < 20:
            score = 3.0
        elif feature_count < 30:
            score = 4.0
        else:
            score = 5.0

        reason = f"R3: {feature_count}个功能点 → {score}分"
        detail = {"score": score, "feature_count": feature_count}

        return score, detail, reason

    def _rule_r4_context_count(self, contexts: list) -> Tuple[float, dict, str]:
        """
        R4: 上下文数量（0-5分）
        - 1-2: 1分
        - 3-4: 2分
        - 5-6: 3分
        - 7-8: 4分
        - > 8: 5分
        """
        context_count = len(contexts)

        if context_count <= 2:
            score = 1.0
        elif context_count <= 4:
            score = 2.0
        elif context_count <= 6:
            score = 3.0
        elif context_count <= 8:
            score = 4.0
        else:
            score = 5.0

        reason = f"R4: {context_count}个限界上下文 → {score}分"
        detail = {"score": score, "context_count": context_count}

        return score, detail, reason

    def _rule_r5_aggregate_complexity(self, aggregates: list, entities: list) -> Tuple[float, dict, str]:
        """
        R5: 聚合根复杂度（0-5分）
        - 聚合根数量 + 包含的实体数量
        """
        aggregate_count = len(aggregates)
        total_entities_in_agg = sum(len(agg.get("entities", [])) for agg in aggregates)

        complexity_score = aggregate_count + (total_entities_in_agg / 5)

        if complexity_score < 3:
            score = 1.0
        elif complexity_score < 6:
            score = 2.0
        elif complexity_score < 9:
            score = 3.0
        elif complexity_score < 12:
            score = 4.0
        else:
            score = 5.0

        reason = f"R5: {aggregate_count}个聚合根，包含{total_entities_in_agg}个实体 → {score}分"
        detail = {"score": score, "aggregate_count": aggregate_count, "entities_in_aggregates": total_entities_in_agg}

        return score, detail, reason

    def _rule_r6_workflow_complexity(self, workflows: list) -> Tuple[float, dict, str]:
        """
        R6: 工作流复杂度（0-5分）
        - 工作流数量 + 平均步骤数
        """
        workflow_count = len(workflows)
        total_steps = sum(len(wf.get("steps", [])) for wf in workflows)
        avg_steps = total_steps / workflow_count if workflow_count > 0 else 0

        complexity_score = workflow_count + (avg_steps / 3)

        if complexity_score < 5:
            score = 1.0
        elif complexity_score < 10:
            score = 2.0
        elif complexity_score < 15:
            score = 3.0
        elif complexity_score < 20:
            score = 4.0
        else:
            score = 5.0

        reason = f"R6: {workflow_count}个工作流，平均{avg_steps:.1f}步 → {score}分"
        detail = {"score": score, "workflow_count": workflow_count, "avg_steps": avg_steps}

        return score, detail, reason

    def _rule_r7_priority_distribution(self, features: list) -> Tuple[float, dict, str]:
        """
        R7: 优先级分布（0-5分）
        - P0数量多 → 核心功能多 → 复杂度高
        """
        p0_count = sum(1 for f in features if f.get("priority") == "P0")
        p1_count = sum(1 for f in features if f.get("priority") == "P1")

        if p0_count >= 5:
            score = 5.0
        elif p0_count >= 3:
            score = 4.0
        elif p0_count >= 2:
            score = 3.0
        elif p0_count >= 1:
            score = 2.0
        else:
            score = 1.0

        reason = f"R7: {p0_count}个P0功能，{p1_count}个P1功能 → {score}分"
        detail = {"score": score, "p0_count": p0_count, "p1_count": p1_count}

        return score, detail, reason

    def _rule_r8_user_story_count(self, user_stories: list) -> Tuple[float, dict, str]:
        """
        R8: 用户故事数量（0-5分）
        - < 5: 1分
        - 5-10: 2分
        - 10-20: 3分
        - 20-30: 4分
        - > 30: 5分
        """
        story_count = len(user_stories)

        if story_count < 5:
            score = 1.0
        elif story_count < 10:
            score = 2.0
        elif story_count < 20:
            score = 3.0
        elif story_count < 30:
            score = 4.0
        else:
            score = 5.0

        reason = f"R8: {story_count}个用户故事 → {score}分"
        detail = {"score": score, "story_count": story_count}

        return score, detail, reason

    def _rule_r9_value_object_usage(self, value_objects: list) -> Tuple[float, dict, str]:
        """
        R9: 值对象使用（0-5分）
        - 值对象使用说明设计的精细程度
        """
        vo_count = len(value_objects)

        if vo_count < 3:
            score = 1.0
        elif vo_count < 6:
            score = 2.0
        elif vo_count < 10:
            score = 3.0
        elif vo_count < 15:
            score = 4.0
        else:
            score = 5.0

        reason = f"R9: {vo_count}个值对象 → {score}分"
        detail = {"score": score, "value_object_count": vo_count}

        return score, detail, reason

    def _rule_r10_business_complexity(self, draft: DesignDraft) -> Tuple[float, dict, str]:
        """
        R10: 业务复杂度（0-5分）
        - 综合评估：核心价值描述长度、功能描述详细程度等
        """
        # 评估核心价值描述的复杂度
        core_value_length = len(draft.core_value)

        # 评估功能描述的详细程度
        feature_descriptions_length = sum(len(f.get("name", "")) for f in draft.features)

        complexity_indicator = (core_value_length / 10) + (feature_descriptions_length / 50)

        if complexity_indicator < 10:
            score = 1.0
        elif complexity_indicator < 20:
            score = 2.0
        elif complexity_indicator < 30:
            score = 3.0
        elif complexity_indicator < 40:
            score = 4.0
        else:
            score = 5.0

        reason = f"R10: 业务描述复杂度指标{complexity_indicator:.1f} → {score}分"
        detail = {"score": score, "complexity_indicator": complexity_indicator}

        return score, detail, reason

    # ===================== 辅助方法 =====================

    def _estimate_user_count(self, user_scale: str) -> int:
        """估算用户数量"""
        numbers = re.findall(r'(\d+)', user_scale)
        if not numbers:
            return 100  # 默认值

        # 如果有多个数字，取最大值
        return int(numbers[-1])
