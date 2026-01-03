"""
原子级文档生成器

将原子级规格转换为Markdown文档
"""

from typing import Dict, List
from pathlib import Path
import json

from .schema import AtomicSpecification, AtomicComponent


class AtomicDocGenerator:
    """原子级文档生成器"""

    def generate_component_doc(self, component: AtomicComponent) -> str:
        """
        生成单个组件的Markdown文档

        Args:
            component: 原子组件对象

        Returns:
            str: Markdown格式的组件文档
        """
        doc = f"""# {component.name} - {component.category}组件

**生成方式**: {component.component_type}组件
**驱动模式**: 截图驱动 + 测试驱动

---

## 1. 组件用途

{component.purpose}

---

## 2. 属性定义

| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
"""

        # 添加属性表格
        for prop in component.props:
            required = "" if prop.required else ""
            default = prop.default if prop.default else "-"
            doc += f"| {prop.name} | {prop.type} | {required} | {default} | {prop.description} |\n"

        # TypeScript接口
        doc += f"""

**TypeScript接口**:
```typescript
interface {component.name}Props {{
"""
        for prop in component.props:
            optional = "" if prop.required else "?"
            doc += f"  {prop.name}{optional}: {prop.type};\n"

        doc += """}}
```

---

## 3. UI规格

### 布局
{layout}

### 样式
{styles}

### 状态
{states}

---

## 4. 数据契约

**数据源**: {data_source}

**契约**:
{contracts}

---

## 5. 交互规格

| 事件 | 触发条件 | 结果 |
|------|---------|------|
""".format(
            layout=component.ui.layout,
            styles="\n".join(f"- {s}" for s in component.ui.styles),
            states="\n".join(f"- `{s}`" for s in component.ui.states),
            data_source=component.data.get("source", "props"),
            contracts="\n".join(f"- {c}" for c in component.data.get("contracts", []))
        )

        # 添加交互表格
        for interaction in component.interactions:
            doc += f"| {interaction.event} | 用户触发 | {interaction.result} |\n"

        doc += f"""

---

## 6. 依赖组件

{self._format_list(component.dependencies, "无依赖组件")}

---

## 7. 约束条件

{self._format_list(component.constraints, "无特殊约束")}

---

## 8. 边界情况处理

| 场景 | 处理方式 |
|------| --------|
"""

        # 添加边界情况表格
        for edge_case in component.edge_cases:
            parts = edge_case.split(":") if ":" in edge_case else edge_case.split("显示")
            scenario = parts[0] if parts else edge_case
            handling = parts[1] if len(parts) > 1 else "见描述"
            doc += f"| {scenario} | {handling} |\n"

        doc += f"""

---

## 9. 验收标准

{self._format_list(component.acceptance, "无明确验收标准", checkbox=True)}

---

## 10. 遥测与日志

```json
{json.dumps(component.telemetry, indent=2, ensure_ascii=False) if component.telemetry else "{}"}
```

---

## 11. 使用示例

{self._format_list(component.examples, "暂无示例")}

---

**状态**:  已生成
**最后更新**: {component.name}组件规格
"""

        return doc

    def generate_index_doc(self, spec: AtomicSpecification) -> str:
        """
        生成索引文档

        Args:
            spec: 原子级规格对象

        Returns:
            str: Markdown格式的索引文档
        """
        summary = spec.get_summary()

        doc = f"""# {spec.project_name} - 原子级规格索引

**生成时间**: {spec.generated_at}
**驱动模式**: {', '.join(spec.driving_modes_used)}

---

## 📊 规格统计

| 类型 | 数量 |
|------|------|
| UI组件 | {summary['components_count']} |
| 原子任务 | {summary['tasks_count']} |
| API契约 | {summary['contracts_count']} |
| 数据模型 | {summary['models_count']} |
| BDD场景 | {summary['scenarios_count']} |
| 业务流程 | {summary['workflows_count']} |

---

## 🎨 UI组件列表

"""

        # 添加组件列表
        for i, comp in enumerate(spec.components, 1):
            doc += f"{i}. **[{comp.name}](components/{comp.name}.md)** - {comp.purpose}\n"

        doc += f"""

---

## 🔌 API契约列表

"""

        # 添加API列表
        for i, contract in enumerate(spec.contracts, 1):
            method = contract.get("method", "GET")
            endpoint = contract.get("endpoint", "/")
            summary_text = contract.get("summary", "")
            doc += f"{i}. **{method} {endpoint}** - {summary_text}\n"

        doc += f"""

---

## 📦 数据模型列表

"""

        # 添加模型列表
        for i, model in enumerate(spec.models, 1):
            model_name = model.get("name", "Model")
            model_type = model.get("type", "entity")
            doc += f"{i}. **{model_name}** ({model_type})\n"

        doc += f"""

---

## 🧪 BDD场景列表

"""

        # 添加场景列表
        for i, scenario in enumerate(spec.scenarios, 1):
            feature = scenario.get("feature", "Feature")
            scenario_name = scenario.get("scenario", "Scenario")
            doc += f"{i}. **{feature}**: {scenario_name}\n"

        doc += """

---

## 📁 文档结构

```
ATOMIC_SPECS/
├── INDEX.md                     # 本文件
├── components/                  # UI原子组件
│   ├── UserCard.md
│   ├── LogoutButton.md
│   └── ...
├── contracts/                   # API契约
│   ├── api-spec.json
│   └── openapi.yaml
├── models/                      # 数据模型
│   ├── user.json
│   ├── domain-models.json
│   └── database-schema.json
├── scenarios/                   # BDD场景
│   └── scenarios.md
└── workflows/                   # 业务流程
    └── database-migrations.sql
```

---

**文档版本**: 1.0.0
**生成工具**: 35-specflow (原子级规格生成器)
"""

        return doc

    def save_specifications(
        self,
        spec: AtomicSpecification,
        output_dir: str = "ATOMIC_SPECS"
    ) -> Dict[str, str]:
        """
        保存所有规格文档到文件系统

        Args:
            spec: 原子级规格对象
            output_dir: 输出目录

        Returns:
            Dict[str, str]: 保存的文件路径映射
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        (output_path / "components").mkdir(exist_ok=True)
        (output_path / "contracts").mkdir(exist_ok=True)
        (output_path / "models").mkdir(exist_ok=True)
        (output_path / "scenarios").mkdir(exist_ok=True)
        (output_path / "workflows").mkdir(exist_ok=True)

        saved_files = {}

        # 1. 保存索引文档
        index_doc = self.generate_index_doc(spec)
        index_path = output_path / "INDEX.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_doc)
        saved_files["index"] = str(index_path)

        # 2. 保存组件文档
        for component in spec.components:
            comp_doc = self.generate_component_doc(component)
            comp_path = output_path / "components" / f"{component.name}.md"
            with open(comp_path, "w", encoding="utf-8") as f:
                f.write(comp_doc)
            saved_files[f"component_{component.name}"] = str(comp_path)

        # 3. 保存API契约(JSON格式)
        if spec.contracts:
            contracts_path = output_path / "contracts" / "api-spec.json"
            with open(contracts_path, "w", encoding="utf-8") as f:
                json.dump(spec.contracts, f, indent=2, ensure_ascii=False)
            saved_files["contracts"] = str(contracts_path)

        # 4. 保存数据模型(JSON格式)
        if spec.models:
            models_path = output_path / "models" / "domain-models.json"
            with open(models_path, "w", encoding="utf-8") as f:
                json.dump(spec.models, f, indent=2, ensure_ascii=False)
            saved_files["models"] = str(models_path)

        # 5. 保存BDD场景(Markdown格式)
        if spec.scenarios:
            scenarios_doc = self._generate_scenarios_doc(spec.scenarios)
            scenarios_path = output_path / "scenarios" / "scenarios.md"
            with open(scenarios_path, "w", encoding="utf-8") as f:
                f.write(scenarios_doc)
            saved_files["scenarios"] = str(scenarios_path)

        # 6. 保存工作流(如数据库迁移)
        if spec.workflows:
            for i, workflow in enumerate(spec.workflows):
                if workflow.get("type") == "database_schema":
                    # 保存数据库Schema
                    schema_path = output_path / "models" / "database-schema.json"
                    with open(schema_path, "w", encoding="utf-8") as f:
                        json.dump(workflow.get("data", {}), f, indent=2, ensure_ascii=False)
                    saved_files["database_schema"] = str(schema_path)

                    # 保存迁移脚本
                    migrations = workflow.get("data", {}).get("migrations", {})
                    if migrations:
                        up_migrations = migrations.get("up", [])
                        migration_sql = "\n\n".join(up_migrations)
                        migration_path = output_path / "workflows" / "database-migrations.sql"
                        with open(migration_path, "w", encoding="utf-8") as f:
                            f.write(migration_sql)
                        saved_files["migrations"] = str(migration_path)

        # 7. 保存完整规格(JSON格式)
        full_spec_path = output_path / "full-specification.json"
        with open(full_spec_path, "w", encoding="utf-8") as f:
            json.dump(spec.to_dict(), f, indent=2, ensure_ascii=False)
        saved_files["full_spec"] = str(full_spec_path)

        return saved_files

    def _format_list(self, items: List[str], empty_message: str = "无", checkbox: bool = False) -> str:
        """格式化列表"""
        if not items:
            return empty_message

        if checkbox:
            return "\n".join(f"- [ ] {item}" for item in items)
        else:
            return "\n".join(f"- {item}" for item in items)

    def _generate_scenarios_doc(self, scenarios: List[Dict]) -> str:
        """生成BDD场景文档"""
        doc = "# BDD场景集合\n\n"

        for i, scenario in enumerate(scenarios, 1):
            feature = scenario.get("feature", "Feature")
            scenario_name = scenario.get("scenario", "Scenario")
            steps = scenario.get("steps", [])

            doc += f"## {i}. {feature}\n\n"
            doc += f"### 场景: {scenario_name}\n\n"
            doc += "```gherkin\n"
            for step in steps:
                doc += f"{step}\n"
            doc += "```\n\n"
            doc += "---\n\n"

        return doc
