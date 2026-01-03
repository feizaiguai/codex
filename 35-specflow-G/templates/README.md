# 自定义模板系统

## 概述

SpecFlow支持自定义Markdown模板，用户可以根据需要定制文档格式和内容结构。

## 模板变量

模板中可以使用以下变量（使用`{variable}`语法）：

### 项目信息变量
- `{project_name}` - 项目名称
- `{project_version}` - 项目版本
- `{domain}` - 业务领域
- `{complexity}` - 复杂度级别
- `{estimated_hours}` - 估算工时

### 质量指标变量
- `{completeness_score}` - 完整性评分
- `{consistency_score}` - 一致性评分
- `{atomicity_score}` - 原子性评分
- `{testability_score}` - 可测试性评分
- `{overall_grade}` - 总体等级

### 内容变量
- `{requirements_count}` - 需求数量
- `{user_stories_count}` - 用户故事数量
- `{test_cases_count}` - 测试用例数量

## 模板示例

### overview.md - 项目概览模板

```markdown
# {project_name} - 项目概览

## 基本信息

- **版本**: {project_version}
- **领域**: {domain}
- **复杂度**: {complexity}
- **估算工时**: {estimated_hours}小时

## 项目愿景

[在此处添加项目愿景描述]

## 质量概览

- 完整性: {completeness_score}/100
- 一致性: {consistency_score}/100
- 原子性: {atomicity_score}/100
- 可测试性: {testability_score}/100

**总体等级**: {overall_grade}
```

### requirements.md - 需求规格模板

```markdown
# 需求规格说明

## 需求概览

本项目共包含 {requirements_count} 个需求，{user_stories_count} 个用户故事。

## 功能性需求

[功能性需求列表将在此处生成]

## 非功能性需求

[非功能性需求列表将在此处生成]

## 用户故事

[用户故事列表将在此处生成]
```

## 使用方法

### 1. 创建自定义模板

在`templates/`目录下创建Markdown文件，使用上述变量语法。

### 2. 应用模板

使用命令行参数指定模板目录：

```bash
python specflow.py --task "项目描述" --template-dir ./templates
```

### 3. 模板命名规范

模板文件名应与文档类型对应：

- `overview.md` - 项目概览
- `requirements.md` - 需求规格
- `domain_model.md` - 领域模型
- `architecture.md` - 架构设计
- `implementation.md` - 实施计划
- `test_strategy.md` - 测试策略
- `risk_assessment.md` - 风险评估
- `quality_report.md` - 质量报告

## 高级功能

### 条件渲染

使用`{#if variable}...{/if}`语法：

```markdown
{#if estimated_hours > 100}
## 大型项目警告
本项目估算工时超过100小时，建议分阶段实施。
{/if}
```

### 循环渲染

使用`{#for item in items}...{/for}`语法：

```markdown
{#for requirement in requirements}
### {requirement.id}: {requirement.title}
{requirement.description}
{/for}
```

## 最佳实践

1. **保持简洁**: 模板应该简洁明了，避免过度复杂
2. **一致性**: 所有模板应使用一致的格式和风格
3. **灵活性**: 使用变量而不是硬编码，提高复用性
4. **文档化**: 为自定义模板添加注释说明

## 示例模板集

参见`examples/`目录下的完整模板示例：

- `examples/minimal/` - 极简模板
- `examples/detailed/` - 详细模板
- `examples/agile/` - 敏捷开发模板
- `examples/enterprise/` - 企业级模板
