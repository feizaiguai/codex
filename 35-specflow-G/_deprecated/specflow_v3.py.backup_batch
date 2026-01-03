"""
SpecFlow V3.0 - 主入口
AI 驱动的原子级多文档规格生成系统

版本: 3.0.0
新增功能:
- AI 驱动需求生成 (10x 生产率)
- Shift-Left 测试集成 (需求阶段前置验证)
- 多模态输入支持 (文本 + 图像)
- 用户故事地图 (可视化用户旅程)
- 智能需求冲突检测

使用示例:
    from specflow_v3 import generate_specification_v3

    spec = generate_specification_v3(
        task_description="构建 B2B 电商平台,多租户,AI 推荐...",
        image_paths=["mockup.png", "flow.png"],  # 可选
        metadata={
            "budget": 1200000,
            "timeline_months": 18,
            "team_size": 8
        }
    )
"""

from typing import Dict, Any, Optional, List
import os
from datetime import datetime

# V2.0 核心模块
from analyzer import TaskAnalyzer, TaskAnalysisResult
from atomic_component import (
    AtomicComponent, UserStory, Feature,
    ComponentCategory, Priority
)
from models_v2 import SpecificationV2, DepthLevel, DocumentType
from config_v2 import SpecFlowConfigV2
from validators import QualityValidator
from generators_extended import SpecificationGenerator

# V3.0 新模块
from models_v3 import (
    SpecificationV3, V3Config, InputMode,
    create_v3_specification, merge_v2_documents_to_v3
)
from ai_requirements_agent import (
    AIRequirementsAgent, create_ai_agent,
    AIAnalysisResult, DecomposedRequirement
)
from shift_left_testing import (
    ShiftLeftTester, create_shift_left_tester,
    ValidationReport
)
from multimodal_processor import (
    MultimodalProcessor, create_multimodal_processor,
    MultimodalAnalysisResult
)
from user_story_mapping import (
    UserStoryMapper,
    UserStory as V3UserStory,
    StoryMap, PrioritizedBacklog
)


# ============ V3.0 主生成函数 ============

def generate_specification_v3(
    task_description: str,
    image_paths: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    depth_level: Optional[str] = None,
    output_dir: Optional[str] = None,
    v3_config: Optional[V3Config] = None
) -> SpecificationV3:
    """
    生成完整的 V3.0 规格文档集(AI 驱动 + 多模态)

    Args:
        task_description: 任务描述(文本)
        image_paths: 图像文件路径列表(可选,支持 UI 原型,流程图等)
        metadata: 元数据(预算,时间线,团队规模等)
        depth_level: 深度级别("simple", "standard", "comprehensive")
        output_dir: 输出目录
        v3_config: V3.0 配置(可选)

    Returns:
        SpecificationV3: 完整的 V3.0 规格文档集

    Example:
        >>> spec = generate_specification_v3(
        ...     task_description="构建 B2B 电商平台...",
        ...     image_paths=["ui_mockup.png", "architecture.png"],
        ...     metadata={"budget": 1200000, "timeline_months": 18}
        ... )
        >>> print(f"质量等级: {spec.quality_metrics.overall_grade.value}")
    """

    if metadata is None:
        metadata = {}

    if v3_config is None:
        v3_config = V3Config()

    print("🚀 SpecFlow V3.0 - AI 驱动的原子级规格生成")
    print("=" * 80)
    print(f"新功能: AI 需求生成 | Shift-Left 测试 | 多模态输入 | 用户故事地图")
    print("=" * 80)

    # ============ V3.0 新增:阶段 0 - 多模态输入处理 ============

    multimodal_analysis = None
    if v3_config.enable_multimodal and image_paths:
        print("\n🖼️  阶段 0/7: 多模态输入分析...")
        processor = create_multimodal_processor()
        multimodal_analysis = processor.analyze_multimodal_input(
            text=task_description,
            image_paths=image_paths
        )

        print(f"   - 输入模式: {multimodal_analysis.input_mode.value}")
        print(f"   - 检测到 {len(multimodal_analysis.ui_components)} 个 UI 组件")
        print(f"   - 推断出 {len(multimodal_analysis.inferred_requirements)} 个需求")

        # 将多模态推断的需求合并到任务描述
        if multimodal_analysis.inferred_requirements:
            task_description += "\n\n多模态分析补充需求:\n"
            task_description += "\n".join(f"- {req}" for req in multimodal_analysis.inferred_requirements)

    # ============ 阶段 1: 任务分析(继承 V2.0) ============

    print("\n📊 阶段 1/7: 分析任务...")
    analysis_result = TaskAnalyzer.analyze(task_description, metadata)

    print(f"   - 项目名称: {analysis_result.project_name}")
    print(f"   - 估算工时: {analysis_result.estimated_hours:.1f} 小时")
    print(f"   - 复杂度: {analysis_result.complexity_level}")
    print(f"   - 推荐深度: {analysis_result.recommended_depth.value}")

    # 确定深度级别
    if depth_level:
        selected_depth = DepthLevel(depth_level)
    else:
        selected_depth = analysis_result.recommended_depth

    # ============ V3.0 新增:阶段 2 - AI 需求生成 ============

    ai_analysis = None
    decomposed_requirements = []

    if v3_config.enable_ai_requirements:
        print("\n🤖 阶段 2/7: AI 驱动需求生成...")
        ai_agent = create_ai_agent()

        # AI 分析
        ai_analysis = ai_agent.analyze_description(
            description=task_description,
            budget=metadata.get("budget_wan"),
            timeline_months=metadata.get("timeline_months")
        )

        print(f"   - 领域: {ai_analysis.domain.value}")
        print(f"   - 复杂度: {ai_analysis.complexity.value}")
        print(f"   - 提取到 {len(ai_analysis.requirement_seeds)} 个需求种子")
        print(f"   - 识别到 {len(ai_analysis.context_signals)} 个上下文信号")

        # AI 需求分解
        decomposed_requirements = ai_agent.decompose_requirements(
            ai_analysis.requirement_seeds
        )

        print(f"   - 分解为 {len(decomposed_requirements)} 个结构化需求")

        # AI 验证
        validation_result = ai_agent.validate_and_iterate(decomposed_requirements)
        print(f"   - 需求质量评分: {validation_result['quality_score']:.1f}/100")

    # ============ V3.0 新增:阶段 3 - Shift-Left 测试验证 ============

    validation_report = None

    if v3_config.enable_shift_left:
        print("\n🧪 阶段 3/7: Shift-Left 测试验证...")
        tester = create_shift_left_tester()

        # 转换为验证格式
        requirements_for_validation = [
            {
                "id": req.id,
                "title": req.title,
                "description": req.description,
                "acceptance_criteria": req.acceptance_criteria
            }
            for req in decomposed_requirements
        ]

        validation_report = tester.validate_requirements_early(requirements_for_validation)

        print(f"   - 验证状态: {validation_report.status.value}")
        print(f"   - 可测试性评分: {validation_report.testability_score:.1f}/100")
        print(f"   - 发现问题: {len(validation_report.issues)} 个")
        print(f"   - 生成 BDD 场景: {len(validation_report.bdd_scenarios)} 个")
        print(f"   - 生成测试用例: {len(validation_report.test_cases)} 个")
        print(f"   - 混沌工程场景: {len(validation_report.chaos_scenarios)} 个")

    # ============ V3.0 新增:阶段 4 - 用户故事地图 ============

    story_map = None
    prioritized_backlog = None

    if v3_config.enable_story_mapping:
        print("\n🗺️  阶段 4/7: 用户故事地图生成...")
        mapper = UserStoryMapper()

        # 从需求生成用户故事
        requirements_for_mapping = [
            {
                "title": req.title,
                "description": req.description,
                "priority": "高" if "High" in req.user_story or "Critical" in req.user_story else "中"
            }
            for req in decomposed_requirements
        ]

        user_stories = mapper.generate_stories_from_requirements(requirements_for_mapping)

        print(f"   - 生成用户故事: {len(user_stories)} 个")

        # 生成故事地图
        story_map = mapper.generate_story_map(user_stories)

        print(f"   - 活动数: {len(story_map.activities)}")
        print(f"   - 用户类型: {len(story_map.user_types)} 种")

        # 优先级排序和发布规划
        prioritized_backlog = mapper.prioritize_stories(
            story_map,
            release_count=v3_config.default_release_count
        )

        print(f"   - 发布计划: {len(prioritized_backlog.releases)} 个版本")
        print(f"   - 总工时: {prioritized_backlog.total_effort}h ({prioritized_backlog.total_effort / 8:.1f} 天)")

    # ============ 阶段 5: 生成 V2.0 基础文档 ============

    print("\n📄 阶段 5/7: 生成基础规格文档集...")

    # 使用 V2.0 生成器生成文档
    config = SpecFlowConfigV2.MULTI_DOC_CONFIGS.get(
        selected_depth.value,
        SpecFlowConfigV2.MULTI_DOC_CONFIGS["standard"]
    )
    config["constraints"] = analysis_result.constraints

    # 从 AI 分解的需求创建原子组件和用户故事(V2.0 格式)
    components = _convert_to_v2_components(decomposed_requirements)
    v2_user_stories = _convert_to_v2_user_stories(decomposed_requirements, components)
    features = _create_features_from_stories(v2_user_stories, components)

    generator = SpecificationGenerator(config)
    v2_spec = generator.generate(
        project_name=analysis_result.project_name,
        task_description=task_description,
        analysis_result=analysis_result,
        components=components,
        user_stories=v2_user_stories,
        features=features
    )

    print(f"   - 生成了 {len(v2_spec.documents)} 个文档")
    print(f"   - 总 Token: {v2_spec.get_total_tokens():,}")

    # ============ 阶段 6: 创建 V3.0 规格文档 ============

    print("\n🎯 阶段 6/7: 整合为 V3.0 规格文档...")

    # 创建 V3.0 规格
    v3_spec = create_v3_specification(
        project_name=analysis_result.project_name,
        depth_level=selected_depth
    )

    # 合并 V2.0 文档
    v3_spec = merge_v2_documents_to_v3(v2_spec.documents, v3_spec)

    # 添加 V3.0 特有数据
    v3_spec.ai_analysis = ai_analysis
    v3_spec.multimodal_analysis = multimodal_analysis
    v3_spec.validation_report = validation_report
    v3_spec.story_map = story_map
    v3_spec.prioritized_backlog = prioritized_backlog
    v3_spec.quality_metrics = v2_spec.quality_metrics

    print(f"   - V3.0 规格文档创建完成")
    print(f"   - 包含 V2.0 文档: {len(v3_spec.documents)} 个")
    print(f"   - AI 分析: {'' if v3_spec.ai_analysis else ''}")
    print(f"   - 多模态分析: {'' if v3_spec.multimodal_analysis else ''}")
    print(f"   - Shift-Left 验证: {'' if v3_spec.validation_report else ''}")
    print(f"   - 用户故事地图: {'' if v3_spec.story_map else ''}")

    # ============ 阶段 7: 质量报告 ============

    print("\n 阶段 7/7: 质量验证...")
    if v3_spec.quality_metrics:
        qm = v3_spec.quality_metrics
        print(f"   - 完整性: {qm.completeness_score:.1f}/100")
        print(f"   - 一致性: {qm.consistency_score:.1f}/100")
        print(f"   - 原子性: {qm.atomicity_score:.1f}/100")
        print(f"   - 可行性: {qm.feasibility_score:.1f}/100")
        print(f"   - 总体等级: {qm.overall_grade.value}")

    # V3.0 特有指标
    if validation_report:
        print(f"   - 可测试性: {validation_report.testability_score:.1f}/100")

    if ai_analysis:
        print(f"   - AI 分析质量: {ai_analysis.quality_score:.1f}/100")

    # ============ 保存到文件 ============

    if output_dir:
        print(f"\n💾 保存到: {output_dir}")
        save_specification_v3(v3_spec, output_dir)

    print("\n" + "=" * 80)
    print("🎉 V3.0 规格文档生成完成!")
    print("=" * 80)

    return v3_spec


def save_specification_v3(spec: SpecificationV3, output_dir: str):
    """
    保存 V3.0 规格文档到文件系统

    Args:
        spec: V3.0 规格对象
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)

    # 保存 V2.0 文档(使用 V2.0 生成器)
    generator = SpecificationGenerator({})
    v2_spec = SpecificationV2(
        project_name=spec.project_name,
        version="2.0.0",
        documents=spec.documents,
        quality_metrics=spec.quality_metrics
    )
    generator.save_specification(v2_spec, output_dir)

    # 保存 V3.0 特有数据
    v3_data_dir = os.path.join(output_dir, "v3_data")
    os.makedirs(v3_data_dir, exist_ok=True)

    # 保存摘要
    summary = spec.to_summary()
    summary_path = os.path.join(output_dir, "v3_summary.json")
    import json
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"   - V3.0 规格文档已保存到: {output_dir}")
    print(f"   - V3.0 摘要已保存到: {summary_path}")


# ============ 辅助函数:格式转换 ============

def _convert_to_v2_components(decomposed_reqs: List[DecomposedRequirement]) -> List[AtomicComponent]:
    """将 V3.0 分解需求转换为 V2.0 原子组件"""
    components = []

    for i, req in enumerate(decomposed_reqs[:10], 1):  # 限制数量
        component = AtomicComponent(
            id=req.id.replace("REQ", "COMP"),
            name=f"{req.title}Component",
            category=ComponentCategory.BUSINESS_LOGIC,
            purpose=req.description[:100],
            context={"requirement_id": req.id},
            props=[],
            interactions=[],
            edge_cases=[],
            acceptance_criteria=req.acceptance_criteria,
            bdd_scenarios=[],
            estimated_hours=req.estimated_hours
        )
        components.append(component)

    return components


def _convert_to_v2_user_stories(decomposed_reqs: List[DecomposedRequirement],
                                 components: List[AtomicComponent]) -> List[UserStory]:
    """将 V3.0 分解需求转换为 V2.0 用户故事"""
    user_stories = []

    for i, req in enumerate(decomposed_reqs, 1):
        # 解析用户故事
        parts = req.user_story.split(",")
        as_a = "用户"
        i_want = req.title
        so_that = "满足业务需求"

        if len(parts) >= 3:
            if "作为" in parts[0]:
                as_a = parts[0].replace("作为", "").strip()
            if "我希望" in parts[1] or "我想要" in parts[1]:
                i_want = parts[1].replace("我希望", "").replace("我想要", "").strip()
            if "以便" in parts[2]:
                so_that = parts[2].replace("以便", "").strip()

        story = UserStory(
            id=req.id.replace("REQ", "US"),
            title=req.title,
            as_a=as_a,
            i_want=i_want,
            so_that=so_that,
            acceptance_criteria=req.acceptance_criteria,
            components=[c.id for c in components if c.context.get("requirement_id") == req.id],
            priority=Priority.HIGH,
            estimated_hours=req.estimated_hours
        )
        user_stories.append(story)

    return user_stories


def _create_features_from_stories(user_stories: List[UserStory],
                                   components: List[AtomicComponent]) -> List[Feature]:
    """从用户故事创建特性"""
    features = []

    # 按相似性分组用户故事
    feature_groups = {}

    for story in user_stories:
        # 简单分组:按标题的第一个词
        words = story.title.split()
        key = words[0] if words else "其他"

        if key not in feature_groups:
            feature_groups[key] = []

        feature_groups[key].append(story)

    # 为每组创建特性
    for i, (key, stories) in enumerate(feature_groups.items(), 1):
        feature = Feature(
            id=f"FEAT-{i:03d}",
            name=f"{key}功能集",
            description=f"包含所有{key}相关的用户故事",
            user_stories=[s.id for s in stories],
            components=[c for story in stories for c in story.components],
            priority=Priority.HIGH,
            business_value=f"实现{key}核心功能"
        )
        features.append(feature)

    return features


# ============ 测试代码 ============

if __name__ == "__main__":
    print("=" * 80)
    print("SpecFlow V3.0 测试")
    print("=" * 80)

    test_description = """
    构建一个 B2B 电商平台,需要支持以下功能:

    1. 多租户架构:支持 500 个供应商和 10,000 个买家
    2. AI 推荐系统:基于用户行为推荐商品
    3. 实时库存同步:与供应商系统实时同步库存
    4. 支付集成:支持支付宝,微信支付
    5. 订单管理:订单创建,跟踪,退款

    预算:120 万元
    时间线:18 个月
    团队:8 人(2 前端 + 3 后端 + 1 测试 + 1 产品 + 1 架构师)

    技术要求:
    - 高并发:支持 10 万日活
    - 高可用:99.9% 可用性
    - 安全:符合 GDPR 和国内数据安全法规
    """

    metadata = {
        "budget_wan": 120,
        "timeline_months": 18,
        "team_size": 8
    }

    # 生成 V3.0 规格
    spec = generate_specification_v3(
        task_description=test_description,
        metadata=metadata,
        output_dir="./test_output_v3"
    )

    print("\n" + "=" * 80)
    print("V3.0 规格文档摘要:")
    print("=" * 80)

    summary = spec.to_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
