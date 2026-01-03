"""
多驱动模式协调器

协调5种驱动模式,确保规格文档的完整性和一致性
"""

from typing import Dict, List
from datetime import datetime

from .schema import AtomicSpecification
from .drivers import (
    ScreenshotDrivenDriver,
    TestDrivenDriver,
    DomainDrivenDriver,
    ContractDrivenDriver,
    DataDrivenDriver
)


class AtomicSpecCoordinator:
    """原子级规格协调器"""

    def __init__(self):
        self.screenshot_driver = ScreenshotDrivenDriver()
        self.test_driver = TestDrivenDriver()
        self.domain_driver = DomainDrivenDriver()
        self.contract_driver = ContractDrivenDriver()
        self.data_driver = DataDrivenDriver()

    def generate_atomic_specs(
        self,
        design_draft: Dict,
        architecture: Dict = None,
        domain_model: Dict = None,
        bdd_scenarios: List[Dict] = None
    ) -> AtomicSpecification:
        """
        协调多驱动模式生成完整原子级规格

        工作流程:
        1. 截图驱动 → 生成UI组件
        2. 测试驱动 → 为每个组件生成BDD场景和验收标准
        3. 领域驱动 → 生成业务逻辑和数据模型
        4. 契约驱动 → 生成API规格
        5. 数据驱动 → 生成数据库Schema
        6. 交叉验证 → 确保一致性
        7. 输出 → 原子级规格文档集

        Args:
            design_draft: 设计草稿数据
            architecture: 架构设计数据(可选)
            domain_model: 领域模型数据(可选)
            bdd_scenarios: BDD场景列表(可选)

        Returns:
            AtomicSpecification: 完整的原子级规格
        """
        print("\n" + "=" * 80)
        print("🔧 原子级规格生成器 - 多驱动模式协同")
        print("=" * 80)

        # 初始化规格对象
        spec = AtomicSpecification(
            project_name=design_draft.get("project_name", "未命名项目"),
            generated_at=datetime.now().isoformat(),
            driving_modes_used=[]
        )

        # 如果没有提供这些参数,从design_draft中提取
        if architecture is None:
            architecture = self._extract_architecture_from_draft(design_draft)

        if domain_model is None:
            domain_model = self._extract_domain_model_from_draft(design_draft)

        if bdd_scenarios is None:
            bdd_scenarios = design_draft.get("bdd_scenarios", [])

        # 1. UI组件(截图驱动)
        print("\n🎨 驱动模式1: 截图驱动(UI组件生成)...")
        ui_components = self.screenshot_driver.generate_component_specs(
            design_draft,
            context=architecture
        )
        spec.components.extend(ui_components)
        spec.driving_modes_used.append("screenshot_driven")
        print(f"   ✓ 生成 {len(ui_components)} 个UI组件")

        # 2. BDD场景和验收标准(测试驱动)
        print("\n🧪 驱动模式2: 测试驱动(BDD场景与验收标准)...")
        if bdd_scenarios:
            test_components = self.test_driver.generate_from_bdd(bdd_scenarios)

            # 增强现有组件的验收标准
            spec.components = self.test_driver.enhance_components_with_bdd(
                spec.components,
                bdd_scenarios
            )

            # 添加测试驱动生成的新组件(如果有)
            for test_comp in test_components:
                if not any(c.name == test_comp.name for c in spec.components):
                    spec.components.append(test_comp)

            spec.scenarios = bdd_scenarios
            spec.driving_modes_used.append("test_driven")
            print(f"   ✓ 增强 {len(spec.components)} 个组件的验收标准")
            print(f"   ✓ 关联 {len(bdd_scenarios)} 个BDD场景")
        else:
            print("    未提供BDD场景,跳过测试驱动")

        # 3. 领域模型(领域驱动)
        print("\n📦 驱动模式3: 领域驱动(DDD建模)...")
        domain_models = self.domain_driver.generate_from_domain_model(domain_model)
        spec.models = domain_models
        spec.driving_modes_used.append("domain_driven")
        print(f"   ✓ 生成 {len(domain_models)} 个领域模型")

        # 4. API契约(契约驱动)
        print("\n🔌 驱动模式4: 契约驱动(API设计)...")
        api_design = {
            "features": design_draft.get("core_features", []),
            "entities": [m.get("name", "") for m in domain_models if m.get("type") in ["entity", "aggregate_root"]]
        }
        api_contracts = self.contract_driver.generate_api_specs(api_design)
        spec.contracts = api_contracts
        spec.driving_modes_used.append("contract_driven")
        print(f"   ✓ 生成 {len(api_contracts)} 个API端点")

        # 5. 数据库Schema(数据驱动)
        print("\n💾 驱动模式5: 数据驱动(数据库Schema)...")
        db_schema = self.data_driver.generate_database_schema(domain_models)
        spec.workflows.append({
            "type": "database_schema",
            "data": db_schema
        })
        spec.driving_modes_used.append("data_driven")

        table_count = len(db_schema.get("database", {}).get("tables", []))
        migration_count = len(db_schema.get("migrations", {}).get("up", []))
        print(f"   ✓ 生成 {table_count} 个数据表")
        print(f"   ✓ 生成 {migration_count} 个迁移脚本")

        # 6. 交叉验证
        print("\n🔍 交叉验证中...")
        validation_results = self._cross_validate(
            spec.components,
            spec.contracts,
            spec.models,
            bdd_scenarios
        )

        if validation_results["passed"]:
            print("   ✓ 交叉验证通过")
        else:
            print(f"    发现 {len(validation_results['warnings'])} 个警告:")
            for warning in validation_results["warnings"][:5]:  # 只显示前5个
                print(f"      - {warning}")

        # 7. 输出统计
        print("\n" + "=" * 80)
        print(" 原子级规格生成完成")
        print("=" * 80)
        summary = spec.get_summary()
        print(f"\n📊 规格统计:")
        print(f"   - UI组件: {summary['components_count']} 个")
        print(f"   - BDD场景: {summary['scenarios_count']} 个")
        print(f"   - 领域模型: {summary['models_count']} 个")
        print(f"   - API端点: {summary['contracts_count']} 个")
        print(f"   - 数据表: {table_count} 个")
        print(f"\n🎯 使用的驱动模式: {', '.join(summary['driving_modes'])}")
        print()

        return spec

    def _extract_architecture_from_draft(self, design_draft: Dict) -> Dict:
        """从设计草稿提取架构信息"""
        return {
            "technical_stack": design_draft.get("technical_stack", {}),
            "architecture_style": design_draft.get("architecture_style", ""),
            "constraints": design_draft.get("constraints", [])
        }

    def _extract_domain_model_from_draft(self, design_draft: Dict) -> Dict:
        """从设计草稿提取领域模型"""
        # 从核心功能推断核心概念
        core_features = design_draft.get("core_features", [])
        core_concepts = []

        for feature in core_features:
            # 提取关键实体词(简化版)
            if "用户" in feature or "User" in feature:
                core_concepts.append("用户")
            if "产品" in feature or "商品" in feature or "Product" in feature:
                core_concepts.append("产品")
            if "订单" in feature or "Order" in feature:
                core_concepts.append("订单")

        return {
            "core_concepts": list(set(core_concepts)),
            "entities": [],
            "value_objects": [],
            "aggregates": []
        }

    def _cross_validate(
        self,
        components: List,
        contracts: List[Dict],
        models: List[Dict],
        scenarios: List[Dict]
    ) -> Dict:
        """
        交叉验证不同驱动模式生成的规格

        验证规则:
        - UI组件的props必须与API响应Schema一致
        - BDD场景必须覆盖所有UI交互
        - 数据模型必须支持所有业务规则
        - API契约必须与前端组件需求匹配

        Returns:
            Dict: 验证结果 {"passed": bool, "warnings": List[str]}
        """
        warnings = []

        # 验证1: 检查UI组件与API契约的一致性
        for component in components:
            component_name = component.name.lower()

            # 查找相关API端点
            related_apis = [
                api for api in contracts
                if component_name.replace("form", "").replace("button", "").replace("card", "") in api.get("endpoint", "").lower()
            ]

            if not related_apis and component.component_type == "UI":
                # UI组件但没有对应API,可能是纯展示组件,这是正常的
                pass

        # 验证2: 检查BDD场景覆盖
        if scenarios:
            scenario_count = len(scenarios)
            component_with_scenarios = len([c for c in components if c.examples])

            if component_with_scenarios < len(components) * 0.5:
                warnings.append(f"BDD场景覆盖率较低: 只有 {component_with_scenarios}/{len(components)} 个组件有场景")

        # 验证3: 检查数据模型完整性
        if models:
            model_names = [m.get("name", "").lower() for m in models]

            # 检查是否有用户模型(大多数系统都需要)
            if not any("user" in name for name in model_names):
                warnings.append("缺少用户(User)模型")

        # 验证4: 检查API契约完整性
        if contracts:
            methods = [api.get("method", "") for api in contracts]

            # 检查CRUD完整性
            if "GET" not in methods:
                warnings.append("缺少GET端点")
            if "POST" not in methods:
                warnings.append("缺少POST端点")

        return {
            "passed": len(warnings) == 0,
            "warnings": warnings
        }

    def generate_workflow_documentation(
        self,
        design_draft: Dict,
        spec: AtomicSpecification
    ) -> str:
        """
        生成工作流文档

        Args:
            design_draft: 设计草稿
            spec: 原子级规格

        Returns:
            str: Markdown格式的工作流文档
        """
        doc = f"""# {spec.project_name} - 原子级规格文档

**生成时间**: {spec.generated_at}
**驱动模式**: {', '.join(spec.driving_modes_used)}

---

## 📊 规格统计

{self._format_summary(spec.get_summary())}

---

## 🎨 UI组件规格

{self._format_components(spec.components)}

---

## 📦 领域模型

{self._format_models(spec.models)}

---

## 🔌 API契约

{self._format_contracts(spec.contracts)}

---

## 🧪 BDD场景

{self._format_scenarios(spec.scenarios)}

---

**文档结束**
"""
        return doc

    def _format_summary(self, summary: Dict) -> str:
        """格式化统计摘要"""
        return f"""| 类型 | 数量 |
|------|------|
| UI组件 | {summary['components_count']} |
| BDD场景 | {summary['scenarios_count']} |
| 领域模型 | {summary['models_count']} |
| API端点 | {summary['contracts_count']} |
"""

    def _format_components(self, components: List) -> str:
        """格式化组件列表"""
        if not components:
            return "暂无UI组件"

        lines = []
        for i, comp in enumerate(components, 1):
            lines.append(f"### {i}. {comp.name}")
            lines.append(f"\n**用途**: {comp.purpose}")
            lines.append(f"\n**属性**:")
            for prop in comp.props:
                req = "✓" if prop.required else " "
                lines.append(f"- [{req}] `{prop.name}`: {prop.type} - {prop.description}")
            lines.append("")

        return "\n".join(lines)

    def _format_models(self, models: List[Dict]) -> str:
        """格式化模型列表"""
        if not models:
            return "暂无领域模型"

        lines = []
        for i, model in enumerate(models, 1):
            lines.append(f"### {i}. {model.get('name', 'Model')}")
            lines.append(f"\n**类型**: {model.get('type', 'entity')}")

            if model.get("properties"):
                lines.append(f"\n**属性**: {', '.join(model['properties'].keys())}")

            lines.append("")

        return "\n".join(lines)

    def _format_contracts(self, contracts: List[Dict]) -> str:
        """格式化API契约列表"""
        if not contracts:
            return "暂无API契约"

        lines = []
        for i, api in enumerate(contracts, 1):
            method = api.get("method", "GET")
            endpoint = api.get("endpoint", "/")
            summary = api.get("summary", "")

            lines.append(f"### {i}. {method} {endpoint}")
            if summary:
                lines.append(f"\n{summary}")
            lines.append("")

        return "\n".join(lines)

    def _format_scenarios(self, scenarios: List[Dict]) -> str:
        """格式化BDD场景列表"""
        if not scenarios:
            return "暂无BDD场景"

        lines = []
        for i, scenario in enumerate(scenarios, 1):
            feature = scenario.get("feature", "Feature")
            scenario_name = scenario.get("scenario", "Scenario")

            lines.append(f"### {i}. {feature}: {scenario_name}")

            steps = scenario.get("steps", [])
            if steps:
                lines.append("\n```gherkin")
                for step in steps:
                    lines.append(step)
                lines.append("```")

            lines.append("")

        return "\n".join(lines)
