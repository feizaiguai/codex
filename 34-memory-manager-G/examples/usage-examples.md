# Memory Manager 使用示例

本文档包含 Memory Manager 的实际使用示例和最佳实践。

---

## 📋 基础示例

### 1. 设置语言偏好（最常用）

```bash
# 设置输出语言
/memory set language.output "简体中文"

# 设置语言偏好说明
/memory set language.preference "所有发给用户的文字都使用简体中文"

# 设置代码注释语言
/memory set language.codeComments "简体中文"
```

**效果**：
```
✅ 已设置：language.output = 简体中文
✅ 已设置：language.preference = 所有发给用户的文字都使用简体中文
✅ 已设置：language.codeComments = 简体中文
```

### 2. 查看当前设置

```bash
/memory show
```

**输出**：
```json
{
  "language": {
    "output": "简体中文",
    "preference": "所有发给用户的文字都使用简体中文",
    "codeComments": "简体中文"
  }
}
```

---

## 🔧 编码偏好设置

### 设置 Python 开发偏好

```bash
# 代码风格
/memory set coding.python.style "google"

# 包管理器
/memory set coding.python.packageManager "poetry"

# 类型提示
/memory set coding.python.alwaysTypeHints true

# 测试框架
/memory set coding.python.testFramework "pytest"

# Python 版本
/memory set coding.python.version "3.11"
```

### 设置 JavaScript/TypeScript 偏好

```bash
# 包管理器
/memory set coding.javascript.packageManager "pnpm"

# 代码风格
/memory set coding.javascript.style "airbnb"

# 框架偏好
/memory set coding.javascript.framework "react"

# TypeScript 严格模式
/memory set coding.typescript.strict true
```

### 设置通用编码偏好

```bash
# 缩进
/memory set coding.indentation 2

# 行宽
/memory set coding.lineWidth 100

# 是否使用分号
/memory set coding.useSemicolons true

# 引号风格
/memory set coding.quotes "double"
```

---

## 📁 项目管理偏好

### Git 工作流偏好

```bash
# 默认分支命名规则
/memory set project.git.branchNaming "feature/{issue-id}-{description}"

# 提交消息格式
/memory set project.git.commitFormat "conventional"

# 是否总是签名提交
/memory set project.git.signCommits true
```

### 项目模板偏好

```bash
# Python 项目模板
/memory set project.templates.python "poetry-modern"

# Node.js 项目模板
/memory set project.templates.nodejs "typescript-express"

# React 项目模板
/memory set project.templates.react "vite-typescript"
```

---

## 🎨 UI/UX 偏好

### Claude Code 界面偏好

```bash
# 主题
/memory set ui.theme "dark"

# 字体大小
/memory set ui.fontSize 14

# 是否显示行号
/memory set ui.showLineNumbers true

# 是否启用通知
/memory set ui.notifications.enabled true

# 通知声音
/memory set ui.notifications.sound false
```

---

## 📊 复杂对象示例

### 设置 JSON 对象

```bash
# 设置完整的编辑器配置
/memory set editor '{"theme": "monokai", "fontSize": 14, "tabSize": 2, "wordWrap": true}'

# 设置代码格式化配置
/memory set formatter '{"printWidth": 100, "semi": true, "singleQuote": false, "trailingComma": "all"}'
```

### 设置数组

```bash
# 设置喜欢的编程语言
/memory set preferences.languages '["Python", "TypeScript", "Rust", "Go"]'

# 设置忽略的文件模式
/memory set project.ignorePatterns '["node_modules", "__pycache__", "*.pyc", ".git"]'
```

---

## 🔍 查询和管理

### 查询特定配置

```bash
# 查询语言设置
/memory get language.output

# 查询 Python 版本
/memory get coding.python.version

# 查询主题
/memory get ui.theme
```

### 删除配置

```bash
# 删除单个配置
/memory delete old_setting

# 删除整个配置组
/memory delete coding.python
```

---

## 🚀 高级用例

### 用例 1：团队协作配置

```bash
# 团队代码风格
/memory set team.codingStyle "company-standard"

# 团队审查要求
/memory set team.reviewRequired true

# 团队最小测试覆盖率
/memory set team.minTestCoverage 80

# 团队文档要求
/memory set team.requireDocs true
```

### 用例 2：多环境配置

```bash
# 开发环境
/memory set environments.dev.apiUrl "http://localhost:3000"
/memory set environments.dev.debug true

# 生产环境
/memory set environments.prod.apiUrl "https://api.example.com"
/memory set environments.prod.debug false
```

### 用例 3：AI 辅助偏好

```bash
# AI 代码生成偏好
/memory set ai.codeGeneration.verboseComments true
/memory set ai.codeGeneration.includeTests true
/memory set ai.codeGeneration.includeDocstrings true

# AI 解释风格
/memory set ai.explanationStyle "beginner-friendly"

# AI 语言偏好
/memory set ai.language "简体中文"
```

---

## 🎯 实际场景

### 场景 1：新项目初始化

当开始一个新的 Python 项目时：

```bash
# 设置项目偏好
/memory set project.current.name "my-awesome-project"
/memory set project.current.language "python"
/memory set project.current.version "3.11"
/memory set project.current.packageManager "poetry"

# 设置代码规范
/memory set project.current.linter "ruff"
/memory set project.current.formatter "black"
/memory set project.current.typeChecker "mypy"
```

### 场景 2：远程工作配置

```bash
# 工作时间偏好
/memory set work.timezone "Asia/Shanghai"
/memory set work.hours '{"start": "09:00", "end": "18:00"}'

# 会议偏好
/memory set work.meetingPreferences '{"preferredDays": ["Monday", "Wednesday"], "preferredTime": "14:00"}'

# 通知设置
/memory set work.notifications.urgentOnly true
```

### 场景 3：学习和文档偏好

```bash
# 学习风格
/memory set learning.style "hands-on"

# 文档偏好
/memory set documentation.format "markdown"
/memory set documentation.includeExamples true
/memory set documentation.detailLevel "comprehensive"

# 语言
/memory set documentation.language "简体中文"
```

---

## 💡 最佳实践总结

### 1. 使用层级结构

✅ **推荐**：
```bash
/memory set language.output "简体中文"
/memory set language.docs "简体中文"
/memory set language.comments "简体中文"
```

### 2. 使用有意义的键名

✅ **推荐**：
```bash
/memory set coding.python.style "google"
```

❌ **不推荐**：
```bash
/memory set pyStyle "google"
```

### 3. 定期审查和清理

```bash
# 查看所有设置
/memory show

# 删除不再使用的设置
/memory delete deprecated_setting
```

### 4. 备份重要配置

```bash
# 查看配置文件位置
/memory path

# 手动备份
# 配置文件：~/.claude/settings.json
# 备份位置：~/.claude/settings.json.backup
```

---

## 📚 参考

### 常用键名约定

| 类别 | 键名示例 |
|------|---------|
| 语言 | `language.output`, `language.preference` |
| 编码 | `coding.style`, `coding.indentation` |
| 项目 | `project.template`, `project.git.branchNaming` |
| UI | `ui.theme`, `ui.fontSize` |
| AI | `ai.language`, `ai.codeGeneration.includeTests` |

---

**创建日期**: 2025-12-14  
**版本**: 1.0.0  
**语言**: 简体中文 🇨🇳
