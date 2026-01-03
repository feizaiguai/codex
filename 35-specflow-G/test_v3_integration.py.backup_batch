"""
35-specflow V3.0 集成测试

测试真正的 V3.0 规则引擎功能:
- SpecFlow 主程序(specflow.py)
- SpecificationGenerator(generator_v3.py)
- SpecificationAnalyzer(analyzer_v3.py)
- 规则引擎集成
"""

import sys
from pathlib import Path

def test_v3_imports():
    """测试 V3.0 核心模块导入"""
    print("\n" + "="*70)
    print("  测试 1: V3.0 核心模块导入")
    print("="*70)

    try:
        from specflow import SpecFlow
        from generator_v3 import SpecificationGenerator
        from analyzer_v3 import SpecificationAnalyzer
        from core.models import DepthLevel

        print(" 所有核心模块导入成功")
        print(f"   - SpecFlow: {SpecFlow}")
        print(f"   - SpecificationGenerator: {SpecificationGenerator}")
        print(f"   - SpecificationAnalyzer: {SpecificationAnalyzer}")
        return True
    except Exception as e:
        print(f" 导入失败: {e}")
        return False


def test_specflow_initialization():
    """测试 SpecFlow 初始化"""
    print("\n" + "="*70)
    print("  测试 2: SpecFlow 初始化")
    print("="*70)

    try:
        from specflow import SpecFlow
        from core.models import DepthLevel

        # 创建实例
        specflow = SpecFlow(depth_level=DepthLevel.STANDARD)

        print(" SpecFlow 初始化成功")
        print(f"   - 深度级别: {specflow.depth_level}")
        print(f"   - 规则引擎: {type(specflow.rules_engine).__name__}")
        print(f"   - 生成器: {type(specflow.generator).__name__}")
        print(f"   - 分析器: {type(specflow.analyzer).__name__}")
        return True
    except Exception as e:
        print(f" 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_specification_generation():
    """测试简单规格生成"""
    print("\n" + "="*70)
    print("  测试 3: 简单规格生成(图书馆系统)")
    print("="*70)

    try:
        from specflow import SpecFlow
        from core.models import DepthLevel

        # 创建实例
        specflow = SpecFlow(depth_level=DepthLevel.STANDARD)

        # 生成规格
        task_description = """
        开发一个在线图书馆管理系统,支持以下功能:
        1. 用户注册和登录
        2. 图书搜索和浏览
        3. 图书借阅和归还
        4. 图书预约
        5. 借阅历史查询
        """

        print(f"📝 任务描述: {task_description.strip()[:50]}...")

        spec = specflow.generate_specification(
            task_description=task_description,
            project_name="在线图书馆管理系统",
            project_version="1.0.0"
        )

        print(" 规格生成成功")
        print(f"   - 项目名称: {spec.project_name}")
        print(f"   - 项目版本: {spec.project_version}")
        print(f"   - 规格版本: {spec.spec_version}")
        print(f"   - 文档数量: {len(spec.documents)}")
        print(f"   - 需求数量: {len(spec.requirements)}")
        print(f"   - 用户故事数量: {len(spec.user_stories)}")

        # 检查质量报告
        if spec.quality_report:
            print(f"   - 质量等级: {spec.quality_report.metrics.overall_grade.value}")
            print(f"   - 完整性: {spec.quality_report.metrics.completeness_score}/100")
            print(f"   - 一致性: {spec.quality_report.metrics.consistency_score}/100")
            print(f"   - 原子性: {spec.quality_report.metrics.atomicity_score}/100")
            print(f"   - 可测试性: {spec.quality_report.metrics.testability_score}/100")

        return True
    except Exception as e:
        print(f" 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_generation():
    """测试文档生成"""
    print("\n" + "="*70)
    print("  测试 4: 8个核心文档生成")
    print("="*70)

    try:
        from specflow import SpecFlow
        from core.models import DepthLevel, DocumentType

        specflow = SpecFlow(depth_level=DepthLevel.STANDARD)

        task_description = "开发一个电商平台,支持商品浏览,购物车,订单管理"

        spec = specflow.generate_specification(
            task_description=task_description,
            project_name="电商平台",
            project_version="1.0.0"
        )

        # 检查8个核心文档
        required_docs = [
            DocumentType.OVERVIEW,
            DocumentType.REQUIREMENTS,
            DocumentType.DOMAIN_MODEL,
            DocumentType.ARCHITECTURE,
            DocumentType.IMPLEMENTATION,
            DocumentType.TEST_STRATEGY,
            DocumentType.RISK_ASSESSMENT,
            DocumentType.QUALITY_REPORT
        ]

        print(" 文档生成完成")
        for doc_type in required_docs:
            if doc_type in spec.documents:
                doc = spec.documents[doc_type]
                content_len = len(doc.content) if doc.content else 0
                status = "" if content_len > 0 else ""
                print(f"   {status} {doc_type.value}: {doc.title} ({content_len} chars)")
            else:
                print(f"    {doc_type.value}: 缺失")

        return all(dt in spec.documents for dt in required_docs)
    except Exception as e:
        print(f" 文档生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quality_analysis():
    """测试质量分析"""
    print("\n" + "="*70)
    print("  测试 5: 质量分析和评分")
    print("="*70)

    try:
        from specflow import SpecFlow
        from core.models import DepthLevel

        specflow = SpecFlow(depth_level=DepthLevel.COMPREHENSIVE)

        task_description = """
        开发一个智能客服系统:
        1. 用户可以通过文字,语音提问
        2. 系统自动理解问题并回答
        3. 支持多轮对话
        4. 支持知识库管理
        5. 支持对话历史查询
        6. 支持客服人员接入
        """

        spec = specflow.generate_specification(
            task_description=task_description,
            project_name="智能客服系统",
            project_version="1.0.0"
        )

        print(" 质量分析完成")

        if spec.quality_report:
            qr = spec.quality_report
            print(f"   - 领域: {qr.domain.value}")
            print(f"   - 复杂度: {qr.complexity.value}")
            print(f"   - 估算工时: {qr.estimated_hours} 小时")
            print(f"   - 质量等级: {qr.metrics.overall_grade.value}")
            print(f"   - 完整性: {qr.metrics.completeness_score}/100")
            print(f"   - 一致性: {qr.metrics.consistency_score}/100")
            print(f"   - 验证问题数: {len(qr.validation_issues)}")
            print(f"   - 改进建议数: {len(qr.recommendations)}")

            # 显示部分建议
            if qr.recommendations:
                print("\n   改进建议:")
                for i, rec in enumerate(qr.recommendations[:3], 1):
                    print(f"   {i}. {rec[:60]}...")

        return True
    except Exception as e:
        print(f" 质量分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_markdown_export():
    """测试文档内容生成"""
    print("\n" + "="*70)
    print("  测试 6: 文档内容生成")
    print("="*70)

    try:
        from specflow import SpecFlow
        from core.models import DepthLevel, DocumentType

        specflow = SpecFlow(depth_level=DepthLevel.STANDARD)

        spec = specflow.generate_specification(
            task_description="开发一个任务管理系统,支持任务创建,分配,跟踪",
            project_name="任务管理系统",
            project_version="1.0.0"
        )

        print(" 文档内容生成成功")
        print(f"   - 文档数量: {len(spec.documents)}")

        # 检查文档内容长度(markdown格式)
        total_content_length = 0
        for doc_type, doc in spec.documents.items():
            markdown_len = len(doc.markdown) if doc.markdown else 0
            total_content_length += markdown_len
            print(f"   - {doc_type.value}: {markdown_len} 字符")

        print(f"   - 总内容长度: {total_content_length} 字符")

        return total_content_length > 1000
    except Exception as e:
        print(f" 文档生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance():
    """测试性能(响应时间)"""
    print("\n" + "="*70)
    print("  测试 7: 性能测试(响应时间)")
    print("="*70)

    try:
        import time
        from specflow import SpecFlow
        from core.models import DepthLevel

        specflow = SpecFlow(depth_level=DepthLevel.SIMPLE)

        task_description = "开发一个博客系统,支持文章发布,评论,标签"

        start_time = time.time()

        spec = specflow.generate_specification(
            task_description=task_description,
            project_name="博客系统",
            project_version="1.0.0"
        )

        end_time = time.time()
        elapsed = end_time - start_time

        print(" 性能测试完成")
        print(f"   - 执行时间: {elapsed:.3f} 秒")
        print(f"   - 文档数量: {len(spec.documents)}")
        print(f"   - 平均每文档: {elapsed/max(len(spec.documents), 1):.3f} 秒")

        # V3.0 目标:毫秒级响应(<1秒)
        if elapsed < 1.0:
            print(f"   ⭐ 性能优秀(目标 <1秒)")
        elif elapsed < 3.0:
            print(f"    性能良好(目标 <3秒)")
        else:
            print(f"    性能需优化(当前 {elapsed:.3f}秒)")

        return True
    except Exception as e:
        print(f" 性能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("  35-specflow V3.0 规则引擎集成测试套件")
    print("="*70)
    print("测试日期: 2025-12-18")
    print("测试目标: 验证 V3.0 规则引擎核心功能")
    print()

    tests = [
        ("V3.0 核心模块导入", test_v3_imports),
        ("SpecFlow 初始化", test_specflow_initialization),
        ("简单规格生成", test_simple_specification_generation),
        ("8个核心文档生成", test_document_generation),
        ("质量分析和评分", test_quality_analysis),
        ("Markdown 文档导出", test_markdown_export),
        ("性能测试", test_performance),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f" 测试异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # 总结
    print("\n" + "="*70)
    print("  测试报告总结")
    print("="*70)

    passed = sum(1 for _, result in results if result)
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

    print("\n" + "="*70)

    if pass_rate >= 85:
        print(" V3.0 核心功能测试通过")
        return 0
    elif pass_rate >= 70:
        print(" V3.0 部分功能需要优化")
        return 1
    else:
        print(" V3.0 功能测试失败,需要修复")
        return 2


if __name__ == "__main__":
    sys.exit(run_all_tests())
