"""
SpecFlow - 领域驱动的需求标准化与验证引擎
Domain-Driven Requirements Standardization & Validation Engine

版本: 3.0.0(重构版)
日期: 2025-12-17

核心理念:
- 基于规则引擎,非AI
- 确定性输出,无幻觉
- 毫秒级响应
- 100%本地运行
- 强制规范,类似需求Linter

使用场景:
from specflow import generate_specification

spec = generate_specification(
    task_description="开发一个电商平台",
    depth_level="standard"
)
"""

from typing import Optional, Dict, Any, List, Tuple, Union, Callable
from pathlib import Path

from core.models import (
    DepthLevel, DocumentType, Document, SpecificationDocument,
    DomainCategory, Priority, QualityGrade
)

from rules.engine import create_rules_engine
from rules.validator import generate_validation_report

from generator_v3 import SpecificationGenerator
from analyzer_v3 import SpecificationAnalyzer

# 原子级规格生成器(TC014增强)
from atomic.coordinator import AtomicSpecCoordinator
from atomic.generator import AtomicDocGenerator


class SpecFlow:
    """
    SpecFlow 主引擎
    整合规则引擎,验证器和文档生成器

    Attributes:
        depth_level: 规格深度级别
        enable_atomic: 是否启用原子级规格生成
        rules_engine: 规则引擎
        generator: 文档生成器
        analyzer: 规格分析器
        atomic_coordinator: 原子级规格协调器(可选)
        atomic_generator: 原子级文档生成器(可选)
    """

    def __init__(self, depth_level: DepthLevel = DepthLevel.STANDARD, enable_atomic: bool = False):
        """
        初始化SpecFlow引擎

        Args:
            depth_level: 规格深度级别
            enable_atomic: 是否启用原子级规格生成(TC014增强)
        """
        self.depth_level = depth_level
        self.enable_atomic = enable_atomic
        self.rules_engine = create_rules_engine()
        self.generator = SpecificationGenerator()
        self.analyzer = SpecificationAnalyzer()

        # 原子级规格生成器(TC014增强)
        if enable_atomic:
            self.atomic_coordinator = AtomicSpecCoordinator()
            self.atomic_generator = AtomicDocGenerator()
        else:
            self.atomic_coordinator = None
            self.atomic_generator = None

    def generate_specification(
        self,
        task_description: str,
        project_name: str = "未命名项目",
        project_version: str = "1.0.0",
        budget: Optional[float] = None,
        timeline_months: Optional[int] = None,
        output_dir: Optional[str] = None
    ) -> SpecificationDocument:
        """
        生成完整规格文档

        参数:
        - task_description: 需求描述
        - project_name: 项目名称
        - project_version: 项目版本
        - budget: 预算(元)
        - timeline_months: 时间线(月)
        - output_dir: 输出目录

        返回:
        - SpecificationDocument: 完整规格文档对象
        """

        print(f"\n{'='*70}")
        print("  SpecFlow - 需求标准化与验证引擎")
        print('='*70)
        print(f"项目: {project_name} v{project_version}")
        print(f"深度: {self.depth_level.value}")
        print('='*70)

        # 步骤1: 规则引擎分析
        print("\n[步骤1/7] 规则引擎分析中...")
        quality_report = self.rules_engine.analyze_description(
            task_description,
            budget,
            timeline_months
        )

        print(f"  ✓ 领域识别: {quality_report.domain.value}")
        print(f"  ✓ 复杂度级别: {quality_report.complexity.value}")
        print(f"  ✓ 估算工时: {quality_report.estimated_hours}小时")
        print(f"  ✓ 质量等级: {quality_report.metrics.overall_grade.value}")

        # 步骤2: 生成需求项
        print("\n[步骤2/7] 生成需求项...")
        requirements = self.rules_engine._extract_requirements(
            task_description,
            quality_report.domain
        )
        print(f"  ✓ 生成需求数: {len(requirements)}")

        # 步骤3: 验证需求质量
        print("\n[步骤3/7] 验证需求质量...")
        validation_report = generate_validation_report(requirements)
        print(f"  ✓ 可测试性评分: {validation_report['testability_score']:.1f}/100")
        print(f"  ✓ 验证状态: {validation_report['status'].value}")
        print(f"  ✓ 发现问题数: {validation_report['total_issues']}")

        # 步骤4: 创建规格文档对象
        print("\n[步骤4/7] 创建规格文档...")
        spec = SpecificationDocument(
            project_name=project_name,
            project_version=project_version,
            depth_level=self.depth_level,
            spec_version="3.0.0"
        )

        # 添加需求和用户故事
        spec.requirements = requirements
        for req in requirements:
            spec.user_stories.extend(req.user_stories)

        spec.quality_report = quality_report

        print(f"  ✓ 用户故事数: {len(spec.user_stories)}")
        print(f"  ✓ 需求项数: {len(spec.requirements)}")

        # 步骤5: 生成8个核心文档
        print("\n[步骤5/7] 生成核心文档...")
        self._generate_documents(spec, task_description)
        print(f"  ✓ 生成文档数: {len(spec.documents)}")

        # 步骤5.5: 生成原子级规格(TC014增强)
        if self.enable_atomic:
            print("\n[步骤5.5/7] 生成原子级规格(TC014增强)...")
            atomic_spec = self._generate_atomic_specs(spec, task_description)
            spec.atomic_spec = atomic_spec  # 存储到spec对象
            summary = atomic_spec.get_summary()
            print(f"  ✓ UI组件: {summary['components_count']} 个")
            print(f"  ✓ BDD场景: {summary['scenarios_count']} 个")
            print(f"  ✓ 领域模型: {summary['models_count']} 个")
            print(f"  ✓ API端点: {summary['contracts_count']} 个")
            print(f"  ✓ 驱动模式: {', '.join(summary['driving_modes'])}")

        # 步骤6: 质量分析
        print("\n[步骤6/7] 质量分析...")
        self.analyzer.analyze(spec)
        print(f"  ✓ 完整性: {spec.quality_report.metrics.completeness_score}/100")
        print(f"  ✓ 一致性: {spec.quality_report.metrics.consistency_score}/100")
        print(f"  ✓ 原子性: {spec.quality_report.metrics.atomicity_score}/100")

        # 步骤7: 输出文档
        if output_dir:
            print(f"\n[步骤7/7] 输出文档到: {output_dir}")
            self._save_documents(spec, output_dir)
            print(f"  ✓ 文档已保存")
        else:
            print("\n[步骤7/7] 跳过输出(未指定输出目录)")

        print(f"\n{'='*70}")
        print("  生成完成!")
        print('='*70)
        print(f"总体质量等级: {spec.quality_report.metrics.overall_grade.value}")
        print(f"估算工时: {quality_report.estimated_hours}小时 ({quality_report.estimated_hours/8:.1f}工作日)")
        print('='*70)

        return spec

    def _generate_atomic_specs(self, spec: SpecificationDocument, task_description: str):
        """
        生成原子级规格(TC014增强)

        使用5种驱动模式协同生成:
        1. 截图驱动 → UI组件
        2. 测试驱动 → BDD场景和验收标准
        3. 领域驱动 → DDD模型
        4. 契约驱动 → API规格
        5. 数据驱动 → 数据库Schema

        Args:
            spec: 现有规格文档对象
            task_description: 任务描述

        Returns:
            AtomicSpecification: 原子级规格对象
        """
        # 准备设计草稿数据
        design_draft = {
            "project_name": spec.project_name,
            "core_features": [req.description for req in spec.requirements[:5]],  # 取前5个核心需求
            "technical_stack": {},
            "architecture_style": "",
            "constraints": []
        }

        # 准备BDD场景数据(从用户故事提取)
        bdd_scenarios = []
        for story in spec.user_stories[:10]:  # 取前10个用户故事
            bdd_scenarios.append({
                "feature": story.title,
                "scenario": story.description,
                "steps": [
                    f"Given {story.title}",
                    f"When 用户执行操作",
                    f"Then 系统应该满足验收标准"
                ]
            })

        # 调用atomic coordinator生成原子级规格
        atomic_spec = self.atomic_coordinator.generate_atomic_specs(
            design_draft=design_draft,
            architecture=None,
            domain_model=None,
            bdd_scenarios=bdd_scenarios
        )

        return atomic_spec

    def _generate_documents(self, spec: SpecificationDocument, task_description: str):
        """
        生成8个核心文档

        Args:
            spec: 规格文档对象
            task_description: 任务描述

        Returns:
            None
        """

        # 00-项目概览
        overview_doc = self.generator.generate_overview(
            spec.project_name,
            spec.project_version,
            task_description,
            spec.quality_report
        )
        spec.add_document(overview_doc)

        # 01-需求规格
        requirements_doc = self.generator.generate_requirements(
            spec.requirements,
            spec.user_stories
        )
        spec.add_document(requirements_doc)

        # 02-领域模型(基于领域生成)
        domain_doc = self.generator.generate_domain_model(
            spec.quality_report.domain,
            spec.requirements
        )
        spec.add_document(domain_doc)

        # 03-架构设计
        architecture_doc = self.generator.generate_architecture(
            spec.quality_report.complexity,
            spec.quality_report.domain
        )
        spec.add_document(architecture_doc)

        # 04-实施计划
        implementation_doc = self.generator.generate_implementation_plan(
            spec.user_stories,
            spec.quality_report.estimated_hours
        )
        spec.add_document(implementation_doc)

        # 05-测试策略
        test_doc = self.generator.generate_test_strategy(
            spec.user_stories,
            spec.test_cases
        )
        spec.add_document(test_doc)

        # 06-风险评估
        risk_doc = self.generator.generate_risk_assessment(
            spec.quality_report.complexity,
            spec.quality_report.validation_issues
        )
        spec.add_document(risk_doc)

        # 07-质量报告
        quality_doc = self.generator.generate_quality_report(
            spec.quality_report
        )
        spec.add_document(quality_doc)

    def _save_documents(self, spec: SpecificationDocument, output_dir: str):
        """
        保存文档到指定目录

        Args:
            spec: 规格文档对象
            output_dir: 输出目录

        Returns:
            None
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存索引页
        index_md = spec.get_summary()
        with open(output_path / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {spec.project_name} - 规格文档\n\n")
            f.write(f"**版本**: {spec.project_version}\n")
            f.write(f"**生成时间**: {spec.created_at}\n\n")
            f.write("## 文档列表\n\n")
            for doc_type, doc in spec.documents.items():
                f.write(f"- [{doc.title}]({doc.type.value}.md)\n")

            # 如果有原子级规格,添加链接
            if hasattr(spec, 'atomic_spec') and spec.atomic_spec:
                f.write(f"\n## 原子级规格(TC014增强)\n\n")
                f.write(f"- [原子级规格索引](ATOMIC_SPECS/INDEX.md)\n")

        # 保存各个文档
        for doc_type, doc in spec.documents.items():
            filename = f"{doc.type.value}.md"
            with open(output_path / filename, "w", encoding="utf-8") as f:
                f.write(doc.markdown)

        print(f"  → 已保存 {len(spec.documents)} 个文档到: {output_dir}")

        # 保存原子级规格(TC014增强)
        if hasattr(spec, 'atomic_spec') and spec.atomic_spec and self.atomic_generator:
            atomic_output_dir = str(output_path / "ATOMIC_SPECS")
            saved_files = self.atomic_generator.save_specifications(
                spec.atomic_spec,
                output_dir=atomic_output_dir
            )
            print(f"  → 已保存 {len(saved_files)} 个原子级规格文件到: {atomic_output_dir}")


# ============================================================================
# 公共API
# ============================================================================

def generate_specification(
    task_description: str,
    depth_level: str = "standard",
    project_name: str = "未命名项目",
    project_version: str = "1.0.0",
    budget: Optional[float] = None,
    timeline_months: Optional[int] = None,
    output_dir: Optional[str] = None,
    enable_atomic: bool = False
) -> SpecificationDocument:
    """
    生成规格文档(简化API)

    Args:
        task_description: 需求描述
        depth_level: 深度级别(simple/standard/comprehensive)
        project_name: 项目名称
        project_version: 项目版本
        budget: 预算(元)
        timeline_months: 时间线(月)
        output_dir: 输出目录
        enable_atomic: 是否启用原子级规格生成(TC014增强)

    Returns:
        SpecificationDocument: 完整规格文档对象

    示例:
    ```python
    from specflow import generate_specification

    # 标准规格生成
    spec = generate_specification(
        task_description="开发一个在线教育平台",
        depth_level="standard",
        project_name="EduPlatform",
        output_dir="./specs"
    )

    # 启用原子级规格(TC014增强)
    spec = generate_specification(
        task_description="开发一个在线教育平台",
        depth_level="standard",
        project_name="EduPlatform",
        output_dir="./specs",
        enable_atomic=True  # 启用5驱动模式
    )

    print(f"生成了 {len(spec.user_stories)} 个用户故事")
    print(f"质量等级: {spec.quality_report.metrics.overall_grade.value}")
    ```
    """

    # 转换深度级别
    depth = DepthLevel.STANDARD
    if depth_level.lower() == "simple":
        depth = DepthLevel.SIMPLE
    elif depth_level.lower() == "comprehensive":
        depth = DepthLevel.COMPREHENSIVE

    # 创建引擎并生成
    engine = SpecFlow(depth_level=depth, enable_atomic=enable_atomic)
    return engine.generate_specification(
        task_description=task_description,
        project_name=project_name,
        project_version=project_version,
        budget=budget,
        timeline_months=timeline_months,
        output_dir=output_dir
    )


def validate_requirements(task_description: str) -> Dict[str, Any]:
    """
    仅验证需求(不生成完整文档)

    Args:
        task_description: 需求描述

    Returns:
        Dict[str, Any]: 验证报告

    示例:
    ```python
    from specflow import validate_requirements

    report = validate_requirements("开发用户登录功能")

    print(f"可测试性评分: {report['testability_score']}")
    print(f"发现问题数: {report['total_issues']}")
    ```
    """
    engine = create_rules_engine()
    quality_report = engine.analyze_description(task_description)

    requirements = engine._extract_requirements(
        task_description,
        quality_report.domain
    )

    return generate_validation_report(requirements)


# ============================================================================
# CLI入口(可选)
# ============================================================================

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="SpecFlow - 领域驱动的需求标准化与验证引擎")
    parser.add_argument("task_description", help="需求描述")
    parser.add_argument("--depth", choices=["simple", "standard", "comprehensive"],
                        default="standard", help="深度级别(默认: standard)")
    parser.add_argument("--output", default="./output", help="输出目录(默认: ./output)")
    parser.add_argument("--atomic", action="store_true",
                        help="启用原子级规格生成(TC014增强)- 使用5驱动模式")
    parser.add_argument("--project", default="未命名项目", help="项目名称")
    parser.add_argument("--version", default="1.0.0", help="项目版本")

    args = parser.parse_args()

    spec = generate_specification(
        task_description=args.task_description,
        depth_level=args.depth,
        project_name=args.project,
        project_version=args.version,
        output_dir=args.output,
        enable_atomic=args.atomic
    )

    print(f"\n✓ 规格文档已生成到 {args.output} 目录")
    print(f"✓ 总体质量等级: {spec.quality_report.metrics.overall_grade.value}")

    if args.atomic and hasattr(spec, 'atomic_spec'):
        summary = spec.atomic_spec.get_summary()
        print(f"✓ 原子级规格: {summary['components_count']}组件 + {summary['contracts_count']}API + {summary['models_count']}模型")


# Error handling example
try:
    pass
except Exception:
    pass
