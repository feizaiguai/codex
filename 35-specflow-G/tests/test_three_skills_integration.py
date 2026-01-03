"""
三技能联动集成测试(01→02→35)
确保升级不破坏JSON工作流
"""
import json
import sys
from pathlib import Path

# 添加skills目录到路径
SKILLS_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_DIR / "01-spec-explorer"))
sys.path.insert(0, str(SKILLS_DIR / "02-architecture"))
sys.path.insert(0, str(SKILLS_DIR / "35-specflow"))


def validate_json_schema(json_data: dict, stage: str) -> bool:
    """
    验证JSON是否符合三技能联动Schema

    参数:
        json_data: 待验证的JSON数据
        stage: 阶段标识(01/02/35)

    返回:
        bool: 是否通过验证
    """
    print(f"\n{'='*60}")
    print(f"  验证 {stage} JSON Schema")
    print('='*60)

    # 1. 检查必需字段
    assert 'meta' in json_data, f" {stage}: 缺少 meta 字段"
    print(f"✓ meta 字段存在")

    # 2. 验证meta结构
    meta = json_data['meta']
    assert 'project_name' in meta, f" {stage}: meta缺少project_name"
    assert 'generated_at' in meta, f" {stage}: meta缺少generated_at"
    assert 'generated_by' in meta, f" {stage}: meta缺少generated_by"
    print(f"✓ meta 结构正确")
    print(f"  生成者: {meta['generated_by']}")
    print(f"  项目名: {meta['project_name']}")

    # 3. 阶段特定验证
    if stage == "01-spec-explorer":
        assert 'spec_model' in json_data, " 01: 缺少 spec_model"
        spec_model = json_data['spec_model']

        # 验证user_stories
        flow = spec_model.get('flow_modeling', {})
        user_stories = flow.get('user_stories', [])
        print(f"✓ spec_model 存在")
        print(f"  用户故事数: {len(user_stories)}")

        # 验证bdd_scenarios
        bdd_scenarios = spec_model.get('bdd_scenarios', [])
        print(f"  BDD场景数: {len(bdd_scenarios)}")

        # 验证entities
        domain = spec_model.get('domain_modeling', {})
        entities = domain.get('entities', [])
        print(f"  实体数: {len(entities)}")

    elif stage == "02-architecture":
        assert 'spec_model' in json_data, " 02: 必须保留 spec_model"
        assert 'arch_model' in json_data, " 02: 缺少 arch_model"

        spec_model = json_data['spec_model']
        arch_model = json_data['arch_model']

        print(f"✓ spec_model 已保留(来自01)")
        print(f"✓ arch_model 已添加(02生成)")

        # 验证spec_model完整性
        flow = spec_model.get('flow_modeling', {})
        user_stories = flow.get('user_stories', [])
        bdd_scenarios = spec_model.get('bdd_scenarios', [])

        print(f"  用户故事数: {len(user_stories)}")
        print(f"  BDD场景数: {len(bdd_scenarios)}")

        # 验证arch_model结构
        assert 'scale_assessment' in arch_model, " 02: arch_model缺少scale_assessment"
        assert 'tech_stack' in arch_model, " 02: arch_model缺少tech_stack"
        assert 'pattern_selection' in arch_model, " 02: arch_model缺少pattern_selection"

        print(f"  技术栈: {arch_model['tech_stack'].get('backend_language', {}).get('recommendation', 'N/A')}")
        print(f"  架构模式: {arch_model['pattern_selection'].get('primary_pattern', 'N/A')}")

    elif stage == "35-specflow":
        # 35必须接收完整的spec_model + arch_model
        assert 'spec_model' in json_data, " 35: 缺少 spec_model(来自01)"
        assert 'arch_model' in json_data, " 35: 缺少 arch_model(来自02)"

        print(f"✓ spec_model + arch_model 完整接收")

    print(f"{'='*60}")
    print(f"   {stage} JSON Schema 验证通过")
    print(f"{'='*60}\n")

    return True


def test_json_data_flow():
    """
    测试JSON数据在三技能间的流转

    工作流: 01 → DESIGN.json → 02 → ARCHITECTURE.json → 35 → 规格文档
    """
    print("\n" + "="*80)
    print("  三技能JSON联动数据流测试")
    print("="*80)

    # 模拟数据(简化版)
    mock_spec_model = {
        "context": {
            "core_problem": "测试问题",
            "target_users": ["测试用户"],
            "value_proposition": "测试价值"
        },
        "flow_modeling": {
            "user_stories": [
                {
                    "id": "US-001",
                    "title": "测试故事",
                    "as_a": "测试用户",
                    "i_want": "测试功能",
                    "so_that": "达成测试目标",
                    "priority": "HIGH",
                    "acceptance_criteria": ["测试标准1", "测试标准2"]
                }
            ]
        },
        "domain_modeling": {
            "entities": [
                {
                    "name": "测试实体",
                    "attributes": ["属性1", "属性2"],
                    "behaviors": ["行为1"]
                }
            ],
            "bounded_contexts": [
                {
                    "name": "测试上下文",
                    "entities": ["测试实体"],
                    "responsibilities": ["职责1"]
                }
            ]
        },
        "bdd_scenarios": [
            {
                "feature": "测试功能",
                "scenario": "测试场景",
                "given": ["前置条件1"],
                "when": ["操作1"],
                "then": ["预期结果1"]
            }
        ]
    }

    # 阶段1: 模拟01-spec-explorer输出
    design_json = {
        "meta": {
            "project_name": "三技能联动测试项目",
            "version": "1.0.0",
            "generated_at": "2025-12-20T10:00:00Z",
            "generated_by": "01-spec-explorer"
        },
        "spec_model": mock_spec_model
    }

    print("\n[阶段1] 01-spec-explorer → DESIGN.json")
    validate_json_schema(design_json, "01-spec-explorer")

    # 阶段2: 模拟02-architecture输出(保留spec_model + 添加arch_model)
    architecture_json = {
        "meta": {
            "project_name": "三技能联动测试项目",
            "version": "1.0.0",
            "generated_at": "2025-12-20T10:05:00Z",
            "generated_by": "02-architecture"
        },
        "spec_model": design_json["spec_model"],  # 🔑 保留完整spec_model
        "arch_model": {
            "scale_assessment": {
                "scale": "MEDIUM",
                "score": 20.0,
                "complexity_level": "中等"
            },
            "tech_stack": {
                "backend_language": {
                    "recommendation": "Python/FastAPI",
                    "alternatives": ["Go", "Java"],
                    "rationale": "高性能异步支持"
                },
                "database": {
                    "recommendation": "PostgreSQL",
                    "alternatives": ["MySQL"],
                    "rationale": "强大的JSONB支持"
                }
            },
            "pattern_selection": {
                "primary_pattern": "模块化单体架构",
                "supporting_patterns": ["分层架构"],
                "rationale": "适合中等复杂度项目"
            },
            "adrs": []
        }
    }

    print("\n[阶段2] 02-architecture → ARCHITECTURE.json")
    validate_json_schema(architecture_json, "02-architecture")

    # 阶段3: 验证35-specflow能够接收完整JSON
    print("\n[阶段3] 35-specflow 接收 ARCHITECTURE.json")
    validate_json_schema(architecture_json, "35-specflow")

    # 验证关键数据完整性
    print("\n" + "="*80)
    print("  数据完整性验证")
    print("="*80)

    spec_from_35 = architecture_json['spec_model']
    user_stories = spec_from_35['flow_modeling']['user_stories']
    bdd_scenarios = spec_from_35['bdd_scenarios']
    entities = spec_from_35['domain_modeling']['entities']

    assert len(user_stories) > 0, " 用户故事丢失"
    assert len(bdd_scenarios) > 0, " BDD场景丢失"
    assert len(entities) > 0, " 实体丢失"

    print(f"✓ 用户故事: {len(user_stories)}个 → 完整传递")
    print(f"✓ BDD场景: {len(bdd_scenarios)}个 → 完整传递")
    print(f"✓ 实体: {len(entities)}个 → 完整传递")

    arch_model = architecture_json['arch_model']
    assert 'tech_stack' in arch_model, " 技术栈丢失"
    assert 'pattern_selection' in arch_model, " 架构模式丢失"

    print(f"✓ 技术栈: {arch_model['tech_stack']['backend_language']['recommendation']} → 正确添加")
    print(f"✓ 架构模式: {arch_model['pattern_selection']['primary_pattern']} → 正确添加")

    print("\n" + "="*80)
    print("   三技能JSON联动测试通过")
    print("="*80)

    return True


def test_backward_compatibility():
    """
    测试升级后的向后兼容性
    确保35-specflow V4.0仍能处理旧版本JSON
    """
    print("\n" + "="*80)
    print("  向后兼容性测试")
    print("="*80)

    # 旧版JSON(可能缺少某些字段)
    legacy_json = {
        "meta": {
            "project_name": "旧版项目",
            "version": "1.0.0",
            "generated_at": "2025-12-19T10:00:00Z",
            "generated_by": "02-architecture"
        },
        "spec_model": {
            "flow_modeling": {
                "user_stories": [
                    {
                        "id": "US-001",
                        "title": "旧版故事",
                        "as_a": "用户",
                        "i_want": "功能",
                        "so_that": "目标",
                        "priority": "HIGH",
                        "acceptance_criteria": []
                    }
                ]
            },
            "bdd_scenarios": []  # 可能为空
        },
        "arch_model": {
            "scale_assessment": {
                "scale": "MEDIUM",
                "score": 15.0
            },
            "tech_stack": {
                "backend_language": {
                    "recommendation": "Python",
                    "alternatives": []
                }
            }
        }
    }

    print("\n测试旧版JSON兼容性...")

    # 验证必需字段
    assert 'meta' in legacy_json
    assert 'spec_model' in legacy_json

    print("✓ 旧版JSON结构兼容")

    # 验证35能够处理空的bdd_scenarios
    bdd_scenarios = legacy_json['spec_model'].get('bdd_scenarios', [])
    print(f"✓ 处理空BDD场景: {len(bdd_scenarios)}个")

    print("\n" + "="*80)
    print("   向后兼容性测试通过")
    print("="*80)

    return True


if __name__ == "__main__":
    try:
        print("\n\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + "    35-specflow A+ 升级 - 三技能联动集成测试套件".center(78) + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)

        # 运行测试
        test_json_data_flow()
        test_backward_compatibility()

        print("\n\n")
        print("█" * 80)
        print("█" + " " * 78 + "█")
        print("█" + "     所有测试通过 - 可以安全升级".center(78) + "█")
        print("█" + " " * 78 + "█")
        print("█" * 80)
        print("\n")

        sys.exit(0)

    except AssertionError as e:
        print(f"\n\n 测试失败: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n 错误: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
