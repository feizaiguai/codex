#!/usr/bin/env python3
"""SpecFlow V3.0 完整功能测试
功能: 验证所有 V3.0 新模块和集成功能
日期: 2025-12-17
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Any

# 添加 skill 目录到路径
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

def print_section(title: str):
    """打印测试章节标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_test(test_name: str):
    """打印测试名称"""
    print(f"\n【测试】 {test_name}")
    print("-" * 70)

def test_models_v3_import():
    """测试 1: 导入 models_v3 所有类型"""
    print_test("1. 导入 models_v3 模块")
    try:
        from models_v3 import (
            # V3.0 新枚举
            InputMode, ImageType, DomainCategory,
            ComplexityLevel, ContextSignalType, TestabilityLevel,
            ValidationStatus, ChaosType, UserTypeEnum,TestType,

            # V3.0 AI 需求模型
            RequirementSeed, AIAnalysisResult, DecomposedRequirement,

            # V3.0 Shift-Left 测试模型
            TestabilityIssue, BDDScenario, TestCase, ChaosScenario,
            ValidationReport,

            # V3.0 多模态模型
            ImageInput, MultimodalFeatures, MultimodalAnalysisResult,

            # V3.0 用户故事模型
            UserType, Activity, StoryMap, PrioritizedBacklog, Release,

            # V3.0 完整规格
            SpecificationV3, V3Config
        )
        print(" 所有 V3.0 数据模型导入成功")
        print(f"   - 枚举类型: 9 个")
        print(f"   - AI 需求模型: 3 个")
        print(f"   - Shift-Left 测试模型: 5 个")
        print(f"   - 多模态模型: 3 个")
        print(f"   - 用户故事模型: 5 个")
        print(f"   - 核心配置: 2 个")
        return True
    except Exception as e:
        print(f" 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_requirements_agent():
    """测试 2: AI 需求生成代理"""
    print_test("2. AI 需求生成代理功能")
    try:
        from ai_requirements_agent import AIRequirementsAgent, create_ai_agent
        from models_v3 import RequirementSeed, DomainCategory, ComplexityLevel

        # 创建代理实例
        agent = create_ai_agent()
        print(" AI 代理实例创建成功")

        # 测试任务描述分析
        test_description = """
        开发一个电商平台,需要支持用户注册登录,商品浏览,购物车,
        订单管理,支付集成,库存管理,用户评论功能.
        预算 50 万,时间 6 个月.
        """

        print(f"\n📝 测试输入: {test_description.strip()[:50]}...")

        ai_analysis = agent.analyze_description(
            description=test_description,
            budget=500000,
            timeline_months=6
        )

        print(f" AI 分析完成")
        print(f"   - 检测领域: {ai_analysis.domain.value}")
        print(f"   - 复杂度: {ai_analysis.complexity.value}")
        print(f"   - 预估工时: {ai_analysis.estimated_hours} 小时")
        print(f"   - 上下文信号数: {len(ai_analysis.context_signals)}")
        print(f"   - 需求种子数: {len(ai_analysis.requirement_seeds)}")
        print(f"   - 质量评分: {ai_analysis.quality_score:.1f}/100")

        # 验证基本属性
        assert ai_analysis.domain in DomainCategory
        assert ai_analysis.complexity in ComplexityLevel
        assert ai_analysis.estimated_hours > 0
        assert len(ai_analysis.requirement_seeds) > 0
        assert 0 <= ai_analysis.quality_score <= 100

        # 测试需求分解
        print(f"\n🔄 开始需求分解...")
        decomposed = agent.decompose_requirements(ai_analysis.requirement_seeds[:3])

        print(f" 需求分解完成")
        print(f"   - 分解后需求数: {len(decomposed)}")
        for i, req in enumerate(decomposed[:2], 1):
            print(f"   - 需求 {i}: {req.title}")
            print(f"     用户故事: {req.user_story[:60]}...")
            print(f"     验收标准数: {len(req.acceptance_criteria)}")

        # 测试验证迭代
        print(f"\n✔️ 开始验证迭代...")
        validation = agent.validate_and_iterate(decomposed)

        print(f" 验证完成")
        print(f"   - 验证通过: {validation.is_valid}")
        print(f"   - 质量评分: {validation.quality_score:.1f}/100")
        print(f"   - 发现问题数: {len(validation.issues)}")

        return True

    except Exception as e:
        print(f" AI 需求代理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shift_left_testing():
    """测试 3: Shift-Left 测试模块"""
    print_test("3. Shift-Left 测试功能")
    try:
        from shift_left_testing import ShiftLeftTester, create_shift_left_tester
        from models_v3 import ValidationStatus

        # 创建测试器实例
        tester = create_shift_left_tester()
        print(" Shift-Left 测试器创建成功")

        # 准备测试需求
        test_requirements = [
            {
                "id": "REQ-001",
                "title": "用户登录功能",
                "description": "用户应该能够使用邮箱和密码登录系统",
                "acceptance_criteria": [
                    "输入正确的邮箱和密码后能够登录",
                    "输入错误的密码显示错误信息",
                    "连续失败3次后账号锁定10分钟"
                ],
                "priority": "HIGH",
                "complexity": "MEDIUM"
            },
            {
                "id": "REQ-002",
                "title": "商品搜索",
                "description": "用户可以搜索商品",
                "acceptance_criteria": [
                    "支持关键词搜索",
                    "显示搜索结果"
                ],
                "priority": "MEDIUM",
                "complexity": "LOW"
            }
        ]

        print(f"\n📝 测试输入: {len(test_requirements)} 个需求")

        # 执行早期验证
        validation_report = tester.validate_requirements_early(test_requirements)

        print(f" 验证完成")
        print(f"   - 验证状态: {validation_report.status.value}")
        print(f"   - 可测试性评分: {validation_report.testability_score:.1f}/100")
        print(f"   - 发现问题数: {len(validation_report.issues)}")
        print(f"   - BDD 场景数: {len(validation_report.bdd_scenarios)}")
        print(f"   - 测试用例数: {len(validation_report.test_cases)}")
        print(f"   - 混沌场景数: {len(validation_report.chaos_scenarios)}")
        print(f"   - 改进建议数: {len(validation_report.recommendations)}")

        # 显示 BDD 场景示例
        if validation_report.bdd_scenarios:
            print(f"\n📋 BDD 场景示例:")
            scenario = validation_report.bdd_scenarios[0]
            print(f"   标题: {scenario.title}")
            print(f"   Given: {scenario.given[:60]}...")
            print(f"   When: {scenario.when[:60]}...")
            print(f"   Then: {scenario.then[:60]}...")

        # 显示测试用例示例
        if validation_report.test_cases:
            print(f"\n🧪 测试用例示例:")
            test_case = validation_report.test_cases[0]
            print(f"   名称: {test_case.name}")
            print(f"   类型: {test_case.test_type}")
            print(f"   步骤数: {len(test_case.steps)}")

        # 验证基本属性
        assert validation_report.status in ValidationStatus
        assert 0 <= validation_report.testability_score <= 100
        assert len(validation_report.bdd_scenarios) > 0

        return True

    except Exception as e:
        print(f" Shift-Left 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multimodal_processor():
    """测试 4: 多模态处理模块"""
    print_test("4. 多模态输入处理功能")
    try:
        from multimodal_processor import MultimodalProcessor, create_multimodal_processor
        from models_v3 import InputMode, ImageType

        # 创建处理器实例
        processor = create_multimodal_processor()
        print(" 多模态处理器创建成功")

        # 测试纯文本模式
        print(f"\n📝 测试模式 1: 纯文本输入")
        text_only = "开发一个用户登录界面,包含邮箱输入框,密码输入框和登录按钮"

        result = processor.analyze_multimodal_input(text=text_only, image_paths=None)

        print(f" 纯文本分析完成")
        print(f"   - 输入模式: {result.input_mode.value}")
        print(f"   - 提取特征数: {len(result.features.text_features) if result.features.text_features else 0}")
        print(f"   - 推断需求数: {len(result.inferred_requirements)}")

        assert result.input_mode == InputMode.TEXT_ONLY
        assert len(result.inferred_requirements) > 0

        # 测试多模态输入(模拟)
        print(f"\n🖼️ 测试模式 2: 多模态输入(文本+图像)")
        multimodal_text = "这是用户登录页面的设计"
        mock_image_paths = [
            "login_ui_mockup.png",
            "user_flow_diagram.png"
        ]

        result = processor.analyze_multimodal_input(
            text=multimodal_text,
            image_paths=mock_image_paths
        )

        print(f" 多模态分析完成")
        print(f"   - 输入模式: {result.input_mode.value}")
        print(f"   - 图像输入数: {len(result.features.image_features)}")
        print(f"   - 文本特征: {len(result.features.text_features) if result.features.text_features else 0}")
        print(f"   - UI 组件数: {len(result.ui_components)}")
        print(f"   - 用户流程数: {len(result.user_flows)}")
        print(f"   - 推断需求数: {len(result.inferred_requirements)}")

        # 显示推断的需求示例
        if result.inferred_requirements:
            print(f"\n💡 推断需求示例:")
            for i, req in enumerate(result.inferred_requirements[:2], 1):
                print(f"   {i}. {req}")

        # 验证基本属性
        assert result.input_mode == InputMode.MULTIMODAL
        assert len(result.features.image_features) == 2

        return True

    except Exception as e:
        print(f" 多模态处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_story_mapping():
    """测试 5: 用户故事地图模块"""
    print_test("5. 用户故事地图功能")
    try:
        from user_story_mapping import UserStoryMapper
        from models_v3 import UserType, Priority

        # 创建映射器实例
        mapper = UserStoryMapper()
        print(" 用户故事映射器创建成功")

        # 准备测试需求
        test_requirements = [
            {
                "id": "REQ-001",
                "title": "用户注册",
                "description": "新用户可以注册账号",
                "acceptance_criteria": ["邮箱验证", "密码强度检查"],
                "priority": "HIGH",
                "estimated_hours": 16
            },
            {
                "id": "REQ-002",
                "title": "用户登录",
                "description": "注册用户可以登录系统",
                "acceptance_criteria": ["邮箱密码验证", "记住登录状态"],
                "priority": "HIGH",
                "estimated_hours": 12
            },
            {
                "id": "REQ-003",
                "title": "商品浏览",
                "description": "用户可以浏览商品列表",
                "acceptance_criteria": ["分页显示", "筛选排序"],
                "priority": "MEDIUM",
                "estimated_hours": 24
            },
            {
                "id": "REQ-004",
                "title": "管理员后台",
                "description": "管理员可以管理商品和订单",
                "acceptance_criteria": ["商品CRUD", "订单查看"],
                "priority": "MEDIUM",
                "estimated_hours": 40
            }
        ]

        print(f"\n📝 测试输入: {len(test_requirements)} 个需求")

        # 生成用户故事
        user_stories = mapper.generate_stories_from_requirements(test_requirements)

        print(f" 用户故事生成完成")
        print(f"   - 生成故事数: {len(user_stories)}")

        # 按用户类型统计
        user_type_count = {}
        for story in user_stories:
            user_type_count[story.user_type] = user_type_count.get(story.user_type, 0) + 1

        print(f"   - 用户类型分布:")
        for user_type, count in user_type_count.items():
            print(f"     • {user_type.value}: {count} 个故事")

        # 显示故事示例
        print(f"\n📖 故事示例:")
        for i, story in enumerate(user_stories[:2], 1):
            print(f"   {i}. [{story.user_type.value}] {story.title}")
            print(f"      描述: {story.description[:60]}...")
            print(f"      业务价值: {story.business_value}/100")
            print(f"      工作量: {story.effort_estimate}h")

        # 生成故事地图
        story_map = mapper.generate_story_map(user_stories)

        print(f"\n 故事地图生成完成")
        print(f"   - 用户类型数: {len(story_map.user_types)}")
        print(f"   - 活动数: {len(story_map.activities)}")
        print(f"   - 总故事数: {len(story_map.stories)}")

        # 优先级排序
        prioritized_backlog = mapper.prioritize_stories(story_map, release_count=2)

        print(f"\n 优先级排序完成")
        print(f"   - 发布计划数: {len(prioritized_backlog.releases)}")
        print(f"   - 总估算工时: {prioritized_backlog.total_estimated_hours}h")

        for i, release in enumerate(prioritized_backlog.releases, 1):
            print(f"   - Release {i}: {len(release.stories)} 个故事, {release.estimated_hours}h")

        # 验证依赖关系检测
        dependencies_found = any(len(story.dependencies) > 0 for story in user_stories)
        if dependencies_found:
            print(f"   -  依赖关系检测成功")

        # 验证基本属性
        assert len(user_stories) == len(test_requirements)
        assert len(story_map.activities) > 0
        assert len(prioritized_backlog.releases) == 2

        return True

    except Exception as e:
        print(f" 用户故事地图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specflow_v3_integration():
    """测试 6: SpecFlow V3.0 集成测试"""
    print_test("6. SpecFlow V3.0 端到端集成")
    try:
        from specflow_v3 import generate_specification_v3
        from models_v3 import V3Config, DepthLevel

        print(" SpecFlow V3.0 主程序导入成功")

        # 配置 V3 功能
        v3_config = V3Config(
            enable_ai_requirements=True,
            enable_shift_left=True,
            enable_multimodal=False,  # 不使用图像以简化测试
            enable_story_mapping=True,
            v2_compatibility_mode=True
        )

        print(f"\n⚙️ V3.0 配置:")
        print(f"   - AI 需求生成: {v3_config.enable_ai_requirements}")
        print(f"   - Shift-Left 测试: {v3_config.enable_shift_left}")
        print(f"   - 多模态输入: {v3_config.enable_multimodal}")
        print(f"   - 用户故事地图: {v3_config.enable_story_mapping}")
        print(f"   - V2.0 兼容模式: {v3_config.v2_compatibility_mode}")

        # 测试任务描述
        task_description = """
        开发一个在线教育平台,包括以下功能:
        1. 学生可以注册,登录,浏览课程,购买课程,在线学习
        2. 老师可以创建课程,上传视频,管理学生,查看数据
        3. 管理员可以管理用户,课程,订单,财务数据
        4. 支持在线支付,视频播放,进度追踪,证书颁发
        预算:80万,时间:8个月
        """

        metadata = {
            "budget": 800000,
            "timeline_months": 8,
            "team_size": 6
        }

        print(f"\n📝 测试任务:")
        print(f"   描述: {task_description.strip().split('1.')[0].strip()}")
        print(f"   预算: {metadata['budget']:,} 元")
        print(f"   时间: {metadata['timeline_months']} 个月")

        print(f"\n🚀 开始 V3.0 规格生成...")
        print(f"   这将执行完整的 7 阶段工作流:")
        print(f"   Phase 0: 多模态输入分析 (跳过)")
        print(f"   Phase 1: 任务分析")
        print(f"   Phase 2: AI 需求生成")
        print(f"   Phase 3: Shift-Left 测试验证")
        print(f"   Phase 4: 用户故事地图")
        print(f"   Phase 5: 生成 V2.0 基础文档")
        print(f"   Phase 6: 创建 V3.0 规格")
        print(f"   Phase 7: 质量验证")

        # 执行完整生成
        spec_v3 = generate_specification_v3(
            task_description=task_description,
            image_paths=None,
            metadata=metadata,
            depth_level=None,  # 自动选择
            output_dir=None,  # 不保存文件
            v3_config=v3_config
        )

        print(f"\n V3.0 规格生成完成!")
        print(f"\n📊 生成结果统计:")
        print(f"   - 项目名称: {spec_v3.project_name}")
        print(f"   - 版本: {spec_v3.version}")
        print(f"   - 深度级别: {spec_v3.depth_level.value if spec_v3.depth_level else 'N/A'}")
        print(f"   - 文档数量: {len(spec_v3.documents)}")

        # AI 分析结果
        if spec_v3.ai_analysis:
            print(f"\n🤖 AI 分析结果:")
            print(f"   - 领域: {spec_v3.ai_analysis.domain.value}")
            print(f"   - 复杂度: {spec_v3.ai_analysis.complexity.value}")
            print(f"   - 预估工时: {spec_v3.ai_analysis.estimated_hours}h")
            print(f"   - 需求种子: {len(spec_v3.ai_analysis.requirement_seeds)}")
            print(f"   - 质量评分: {spec_v3.ai_analysis.quality_score:.1f}/100")

        # Shift-Left 验证结果
        if spec_v3.validation_report:
            print(f"\n🧪 Shift-Left 验证:")
            print(f"   - 状态: {spec_v3.validation_report.status.value}")
            print(f"   - 可测试性: {spec_v3.validation_report.testability_score:.1f}/100")
            print(f"   - BDD 场景: {len(spec_v3.validation_report.bdd_scenarios)}")
            print(f"   - 测试用例: {len(spec_v3.validation_report.test_cases)}")
            print(f"   - 混沌场景: {len(spec_v3.validation_report.chaos_scenarios)}")

        # 用户故事地图
        if spec_v3.story_map:
            print(f"\n📖 用户故事地图:")
            print(f"   - 用户类型: {len(spec_v3.story_map.user_types)}")
            print(f"   - 活动数: {len(spec_v3.story_map.activities)}")
            print(f"   - 故事数: {len(spec_v3.story_map.stories)}")

        # 优先级排序
        if spec_v3.prioritized_backlog:
            print(f"\n📋 优先级排序:")
            print(f"   - 发布计划: {len(spec_v3.prioritized_backlog.releases)}")
            print(f"   - 总工时: {spec_v3.prioritized_backlog.total_estimated_hours}h")

        # 质量指标
        if spec_v3.quality_metrics:
            print(f"\n⭐ 质量指标:")
            print(f"   - 完整性: {spec_v3.quality_metrics.completeness_score:.1f}/100")
            print(f"   - 一致性: {spec_v3.quality_metrics.consistency_score:.1f}/100")
            print(f"   - 原子性: {spec_v3.quality_metrics.atomicity_score:.1f}/100")
            print(f"   - 总体评级: {spec_v3.quality_metrics.overall_grade.value}")

        # 文档列表
        print(f"\n📄 生成文档列表:")
        for doc in spec_v3.documents:
            print(f"   - {doc.id}: {doc.title} ({len(doc.content)} 字符)")

        # 验证基本属性
        assert spec_v3.version == "3.0.0"
        assert len(spec_v3.documents) > 0
        assert spec_v3.ai_analysis is not None
        assert spec_v3.validation_report is not None
        assert spec_v3.story_map is not None
        assert spec_v3.prioritized_backlog is not None

        print(f"\n 所有验证通过!V3.0 集成测试成功!")

        return True

    except Exception as e:
        print(f" V3.0 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有 V3.0 测试"""
    print_section("SpecFlow V3.0 完整功能测试套件")
    print(f"测试日期: 2025-12-17")
    print(f"测试目标: 验证所有 V3.0 新模块和端到端集成")

    # 定义所有测试
    tests = [
        ("V3.0 数据模型导入", test_models_v3_import),
        ("AI 需求生成代理", test_ai_requirements_agent),
        ("Shift-Left 测试", test_shift_left_testing),
        ("多模态输入处理", test_multimodal_processor),
        ("用户故事地图", test_user_story_mapping),
        ("V3.0 端到端集成", test_specflow_v3_integration),
    ]

    # 运行测试
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n 测试 '{test_name}' 执行异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # 生成测试报告
    print_section("测试报告总结")

    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0

    print(f"\n总体统计:")
    print(f"   - 总测试数: {total_count}")
    print(f"   - 通过数: {passed_count}")
    print(f"   - 失败数: {total_count - passed_count}")
    print(f"   - 通过率: {pass_rate:.1f}%")

    print(f"\n详细结果:")
    for i, (test_name, result) in enumerate(results, 1):
        status = " 通过" if result else " 失败"
        print(f"   {i}. {test_name}: {status}")

    # 最终结论
    print(f"\n" + "="*70)
    if passed_count == total_count:
        print("🎉 恭喜!所有 V3.0 测试全部通过!")
        print("SpecFlow V3.0 已准备好投入使用.")
        return 0
    else:
        print(f" 有 {total_count - passed_count} 个测试失败,需要进一步检查.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
