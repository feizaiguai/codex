#!/usr/bin/env python3
"""SpecFlow Skill 修复验证测试
功能: 验证 models.py 的 dataclass 字段顺序修复是否成功
日期: 2025-12-14
"""
import sys
import os
from pathlib import Path

# 添加 skill 目录到路径
skill_path = r"C:\Users\bigbao\.claude\skills\36-specflow"
sys.path.insert(0, skill_path)

def test_import_models():
    """测试 1: 导入所有 models"""
    print("测试 1: 导入 models...")
    try:
        from models import (
            UltraThinkInput,
            UltraThinkOutput,
            Phase,
            DepthLevel,
            OutputFormat,
            QualityGrade,
            Conflict,
            Recommendation,
            QualityMetrics
        )
        print(" 所有 models 导入成功")
        return True
    except Exception as e:
        print(f" 导入失败: {e}")
        return False

def test_create_conflict():
    """测试 2: 创建 Conflict 实例(修复的目标类)"""
    print("\n测试 2: 创建 Conflict 实例...")
    try:
        from models import Conflict

        # 测试只提供必需字段
        conflict1 = Conflict(
            id="C001",
            type="Requirement",
            description="需求冲突",
            severity="High"
        )
        print(f" Conflict 实例创建成功(仅必需字段): {conflict1.id}")

        # 测试提供所有字段
        conflict2 = Conflict(
            id="C002",
            type="Design",
            description="设计冲突",
            severity="Critical",
            affected_items=["Component A", "Component B"],
            recommendation="重新设计架构"
        )
        print(f" Conflict 实例创建成功(所有字段): {conflict2.id}")
        return True
    except Exception as e:
        print(f" 创建 Conflict 失败: {e}")
        return False

def test_create_recommendation():
    """测试 3: 创建 Recommendation 实例"""
    print("\n测试 3: 创建 Recommendation 实例...")
    try:
        from models import Recommendation

        rec = Recommendation(
            category="Architecture",
            priority="High",
            recommendation="采用微服务架构",
            rationale="提高可扩展性",
            impact="重大架构变更"
        )
        print(f" Recommendation 实例创建成功: {rec.category}")
        return True
    except Exception as e:
        print(f" 创建 Recommendation 失败: {e}")
        return False

def test_import_config():
    """测试 4: 导入 config"""
    print("\n测试 4: 导入 config...")
    try:
        from config import UltraThinkConfig

        # 验证关键配置项存在
        assert hasattr(UltraThinkConfig, 'DEPTH_CONFIGS')
        assert hasattr(UltraThinkConfig, 'QUALITY_THRESHOLDS')
        assert hasattr(UltraThinkConfig, 'VALIDATION_RULES')

        print(" config 导入成功")
        print(f"   - 深度配置: {len(UltraThinkConfig.DEPTH_CONFIGS)} 种模式")
        return True
    except Exception as e:
        print(f" 导入 config 失败: {e}")
        return False

def test_field_order():
    """测试 5: 验证 Conflict 字段顺序"""
    print("\n测试 5: 验证 Conflict dataclass 字段顺序...")
    try:
        from models import Conflict
        from dataclasses import fields

        conflict_fields = fields(Conflict)
        field_info = []

        for f in conflict_fields:
            has_default = f.default != f.default_factory if f.default_factory else f.default != None
            field_info.append({
                'name': f.name,
                'has_default': has_default
            })

        # 验证字段顺序:无默认值的在前,有默认值的在后
        found_default = False
        for info in field_info:
            if info['has_default']:
                found_default = True
            elif found_default:
                print(f" 字段顺序错误: {info['name']} 无默认值但在有默认值字段之后")
                return False

        print(" Conflict 字段顺序正确")
        print("   字段详情:")
        for info in field_info:
            status = "有默认值" if info['has_default'] else "无默认值"
            print(f"   - {info['name']}: {status}")
        return True
    except Exception as e:
        print(f" 字段顺序验证失败: {e}")
        return False

def test_quality_metrics():
    """测试 6: 创建 QualityMetrics 实例"""
    print("\n测试 6: 创建 QualityMetrics 实例...")
    try:
        from models import QualityMetrics, QualityGrade

        metrics = QualityMetrics(
            completeness_score=85.0,
            consistency_score=90.0,
            feasibility_score=88.0,
            overall_grade=QualityGrade.A
        )
        print(f" QualityMetrics 实例创建成功: Grade {metrics.overall_grade.value}")
        return True
    except Exception as e:
        print(f" 创建 QualityMetrics 失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("="*60)
    print("SpecFlow Skill 修复验证测试")
    print("="*60)

    tests = [
        test_import_models,
        test_create_conflict,
        test_create_recommendation,
        test_import_config,
        test_field_order,
        test_quality_metrics
    ]

    results = []
    for test_func in tests:
        results.append(test_func())

    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n 所有测试通过!修复成功!")
        return 0
    else:
        print(f"\n {total - passed} 个测试失败,需要进一步检查")
        return 1

if __name__ == "__main__":
    sys.exit(main())
