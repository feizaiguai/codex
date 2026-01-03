#!/usr/bin/env python3
"""SpecFlow V3.0 简化功能测试
功能: 快速验证所有 V3.0 核心模块是否可以正常导入和基本运行
日期: 2025-12-17
"""
import sys
from pathlib import Path

# 添加 skill 目录到路径
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

def print_test(test_name: str):
    """打印测试名称"""
    print(f"\n{'='*70}")
    print(f"  {test_name}")
    print('='*70)

def test_01_models_v3():
    """测试 1: V3.0 数据模型导入"""
    print_test("测试 1: V3.0 数据模型导入")
    try:
        from models_v3 import (
            InputMode, ImageType, DomainCategory, ComplexityLevel,
            ValidationStatus, ChaosType, UserTypeEnum, TestType,
            RequirementSeed, AIAnalysisResult, DecomposedRequirement,
            TestabilityIssue, ValidationReport,
            MultimodalAnalysisResult,
            UserType, StoryMap, PrioritizedBacklog,
            SpecificationV3, V3Config
        )
        print(" 所有 V3.0 数据模型导入成功")
        print(f"   - 核心枚举: InputMode, DomainCategory, ComplexityLevel, ValidationStatus")
        print(f"   - AI 模型: RequirementSeed, AIAnalysisResult, DecomposedRequirement")
        print(f"   - 测试模型: TestabilityIssue, ValidationReport")
        print(f"   - 多模态: MultimodalAnalysisResult")
        print(f"   - 故事地图: UserType, StoryMap, PrioritizedBacklog")
        print(f"   - 核心配置: SpecificationV3, V3Config")
        return True
    except Exception as e:
        print(f" 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_02_ai_agent():
    """测试 2: AI 需求代理创建"""
    print_test("测试 2: AI 需求生成代理")
    try:
        from ai_requirements_agent import create_ai_agent
        agent = create_ai_agent()
        print(" AI 需求代理创建成功")
        print(f"   - 类型: {type(agent).__name__}")
        print(f"   - 可用方法: analyze_description, decompose_requirements, validate_and_iterate")
        return True
    except Exception as e:
        print(f" 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_03_shift_left():
    """测试 3: Shift-Left 测试器创建"""
    print_test("测试 3: Shift-Left 测试模块")
    try:
        from shift_left_testing import create_shift_left_tester
        tester = create_shift_left_tester()
        print(" Shift-Left 测试器创建成功")
        print(f"   - 类型: {type(tester).__name__}")
        print(f"   - 可用方法: validate_requirements_early")
        return True
    except Exception as e:
        print(f" 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_04_multimodal():
    """测试 4: 多模态处理器创建"""
    print_test("测试 4: 多模态输入处理模块")
    try:
        from multimodal_processor import create_multimodal_processor
        processor = create_multimodal_processor()
        print(" 多模态处理器创建成功")
        print(f"   - 类型: {type(processor).__name__}")
        print(f"   - 可用方法: analyze_multimodal_input")
        return True
    except Exception as e:
        print(f" 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_05_story_mapper():
    """测试 5: 用户故事映射器创建"""
    print_test("测试 5: 用户故事地图模块")
    try:
        from user_story_mapping import UserStoryMapper
        mapper = UserStoryMapper()
        print(" 用户故事映射器创建成功")
        print(f"   - 类型: {type(mapper).__name__}")
        print(f"   - 可用方法: generate_stories_from_requirements, generate_story_map, prioritize_stories")
        return True
    except Exception as e:
        print(f" 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_06_specflow_v3():
    """测试 6: SpecFlow V3.0 主程序导入"""
    print_test("测试 6: SpecFlow V3.0 主程序")
    try:
        from specflow_v3 import generate_specification_v3, create_v3_specification
        from models_v3 import V3Config
        print(" SpecFlow V3.0 主程序导入成功")
        print(f"   - 主函数: generate_specification_v3")
        print(f"   - 辅助函数: create_v3_specification")
        print(f"   - 配置类: V3Config")

        # 测试配置创建
        config = V3Config(
            enable_ai_requirements=True,
            enable_shift_left=True,
            enable_multimodal=False,
            enable_story_mapping=True
        )
        print(f"   - V3Config 实例化成功")
        print(f"     • AI需求: {config.enable_ai_requirements}")
        print(f"     • Shift-Left: {config.enable_shift_left}")
        print(f"     • 多模态: {config.enable_multimodal}")
        print(f"     • 故事地图: {config.enable_story_mapping}")

        return True
    except Exception as e:
        print(f" 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_07_ai_analysis():
    """测试 7: AI 需求分析基本功能"""
    print_test("测试 7: AI 需求分析基本功能")
    try:
        from ai_requirements_agent import create_ai_agent

        agent = create_ai_agent()
        description = "开发一个简单的待办事项管理系统,用户可以添加,编辑,删除任务"

        print(f"📝 测试输入: {description}")
        result = agent.analyze_description(description, budget=None, timeline_months=None)

        print(f" AI 分析完成")
        print(f"   - 检测领域: {result.domain.value}")
        print(f"   - 复杂度: {result.complexity.value}")
        print(f"   - 预估工时: {result.estimated_hours}h")
        print(f"   - 需求种子数: {len(result.requirement_seeds)}")
        print(f"   - 质量评分: {result.quality_score:.1f}/100")

        return True
    except Exception as e:
        print(f" 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_08_shift_left_validation():
    """测试 8: Shift-Left 早期验证"""
    print_test("测试 8: Shift-Left 早期验证")
    try:
        from shift_left_testing import create_shift_left_tester

        tester = create_shift_left_tester()
        requirements = [
            {
                "id": "REQ-001",
                "title": "用户登录",
                "description": "用户可以登录系统",
                "acceptance_criteria": ["输入邮箱和密码", "验证成功后跳转到首页"],
                "priority": "HIGH"
            }
        ]

        print(f"📝 测试输入: {len(requirements)} 个需求")
        report = tester.validate_requirements_early(requirements)

        print(f" 验证完成")
        print(f"   - 验证状态: {report.status.value}")
        print(f"   - 可测试性评分: {report.testability_score:.1f}/100")
        print(f"   - 发现问题数: {len(report.issues)}")
        print(f"   - BDD 场景数: {len(report.bdd_scenarios)}")
        print(f"   - 测试用例数: {len(report.test_cases)}")

        return True
    except Exception as e:
        print(f" 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_09_multimodal_text():
    """测试 9: 多模态文本处理"""
    print_test("测试 9: 多模态文本处理")
    try:
        from multimodal_processor import create_multimodal_processor
        from models_v3 import InputMode

        processor = create_multimodal_processor()
        text = "开发一个用户登录界面,包含邮箱输入框,密码输入框和登录按钮"

        print(f"📝 测试输入: {text}")
        result = processor.analyze_multimodal_input(text=text, image_paths=None)

        print(f" 分析完成")
        print(f"   - 输入模式: {result.input_mode.value}")
        print(f"   - 推断需求数: {len(result.inferred_requirements)}")
        print(f"   - UI 组件数: {len(result.ui_components)}")
        print(f"   - 建议数: {len(result.recommendations)}")

        assert result.input_mode == InputMode.TEXT_ONLY

        return True
    except Exception as e:
        print(f" 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_10_story_mapping():
    """测试 10: 用户故事映射"""
    print_test("测试 10: 用户故事映射")
    try:
        from user_story_mapping import UserStoryMapper

        mapper = UserStoryMapper()
        requirements = [
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
                "description": "注册用户可以登录",
                "acceptance_criteria": ["邮箱密码验证"],
                "priority": "HIGH",
                "estimated_hours": 12
            }
        ]

        print(f"📝 测试输入: {len(requirements)} 个需求")
        stories = mapper.generate_stories_from_requirements(requirements)

        print(f" 故事生成完成")
        print(f"   - 生成故事数: {len(stories)}")
        for story in stories[:2]:
            print(f"   - [{story.user_type.value}] {story.title}")

        # 生成故事地图
        story_map = mapper.generate_story_map(stories)
        print(f" 故事地图生成完成")
        print(f"   - 活动数: {len(story_map.activities)}")
        print(f"   - 用户类型数: {len(story_map.user_types)}")

        return True
    except Exception as e:
        print(f" 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有简化测试"""
    print("\n" + "="*70)
    print("  SpecFlow V3.0 简化功能测试套件")
    print("="*70)
    print(f"测试日期: 2025-12-17")
    print(f"测试目标: 验证所有 V3.0 模块可以正常导入和基本运行")

    tests = [
        ("V3.0 数据模型导入", test_01_models_v3),
        ("AI 需求代理创建", test_02_ai_agent),
        ("Shift-Left 测试器创建", test_03_shift_left),
        ("多模态处理器创建", test_04_multimodal),
        ("用户故事映射器创建", test_05_story_mapper),
        ("SpecFlow V3.0 主程序", test_06_specflow_v3),
        ("AI 需求分析基本功能", test_07_ai_analysis),
        ("Shift-Left 早期验证", test_08_shift_left_validation),
        ("多模态文本处理", test_09_multimodal_text),
        ("用户故事映射", test_10_story_mapping),
    ]

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
    print("\n" + "="*70)
    print("  测试报告总结")
    print("="*70)

    passed = sum(1 for _, r in results if r)
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0

    print(f"\n总体统计:")
    print(f"   - 总测试数: {total}")
    print(f"   - 通过数: {passed}")
    print(f"   - 失败数: {total - passed}")
    print(f"   - 通过率: {pass_rate:.1f}%")

    print(f"\n详细结果:")
    for i, (name, result) in enumerate(results, 1):
        status = " 通过" if result else " 失败"
        print(f"   {i}. {name}: {status}")

    print(f"\n" + "="*70)
    if passed == total:
        print("🎉 所有测试通过!SpecFlow V3.0 核心功能正常.")
        return 0
    elif passed >= total * 0.7:
        print(f"  大部分测试通过({pass_rate:.0f}%),少量问题需要修复.")
        return 0
    else:
        print(f" 测试失败过多({total - passed}/{total}),需要进一步检查.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
