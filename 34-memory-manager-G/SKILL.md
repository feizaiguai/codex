---
name: 34-memory-manager-G
description: Claude Code user memory manager for managing Claude Code built-in memory system (~/.claude/CLAUDE.md). Supports add, read, update, delete user preferences and instructions. Stores narrative instructions, coding standards, work habits in Markdown format. Auto-backup, persistent storage. Use for setting language preference, defining coding standards, recording work habits, personal dev guide.
---

# Memory Manager - Claude Code 用户记忆管理器

**版本**: 1.0.0
**类型**: 系统配置与记忆管理
**复杂度**: 中级
**质量**: 生产级
**语言**: 简体中文 🇨🇳

---

## 📋 技能元数据

```yaml
名称: memory-manager
版本: 1.0.0
分类: 系统工具
标签:
  - 用户偏好
  - 配置管理
  - 记忆存储
  - settings.json
质量等级: 生产级
输出语言: 简体中文
```

---

## 🎯 核心目标

**Memory Manager** 是一个系统工具，用于管理 Claude Code 的用户记忆和偏好设置。

它可以：
- 📖 读取 `~/.claude/settings.json` 中的用户偏好
- ✏️ 修改和添加新的偏好设置
- 🗑️ 删除不需要的偏好项
- 💾 持久化存储用户记忆（如语言偏好、工作习惯等）

**重要**：所有输出使用**简体中文**。

---

## 🚀 使用方法（Slash Command）

### 命令格式

```bash
/memory [操作] [参数]
```

### 操作命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `show` | 显示所有用户偏好 | `/memory show` |
| `get <key>` | 获取特定偏好值 | `/memory get language.output` |
| `set <key> <value>` | 设置偏好值 | `/memory set language.output "简体中文"` |
| `delete <key>` | 删除偏好项 | `/memory delete language.output` |
| `path` | 显示配置文件路径 | `/memory path` |

---

## 📖 使用示例

### 示例 1：设置语言偏好

```bash
# 设置输出语言为简体中文
/memory set language.output "简体中文"

# 设置所有交互使用简体中文
/memory set language.preference "所有发给用户的文字都使用简体中文"
```

**输出**：
```
✅ 已设置：language.output = 简体中文
✅ 已设置：language.preference = 所有发给用户的文字都使用简体中文
```

### 示例 2：查看所有偏好

```bash
/memory show
```

**输出**：
```json
{
  "language": {
    "output": "简体中文",
    "preference": "所有发给用户的文字都使用简体中文"
  },
  "theme": "dark",
  "notifications": {
    "enabled": true,
    "sound": false
  }
}
```

### 示例 3：获取特定偏好

```bash
/memory get language.output
```

**输出**：
```
language.output = 简体中文
```

### 示例 4：删除偏好

```bash
/memory delete theme
```

**输出**：
```
✅ 已删除：theme
```

---

## 🔧 高级功能

### 1. 嵌套键支持

支持使用点号（`.`）访问嵌套的配置：

```bash
# 设置嵌套配置
/memory set editor.mode.vim true
/memory set editor.indentation.spaces 2

# 读取嵌套配置
/memory get editor.mode.vim
```

### 2. JSON 值支持

可以设置 JSON 对象或数组：

```bash
# 设置对象
/memory set myConfig '{"theme": "dark", "lang": "zh-CN"}'

# 设置数组
/memory set favoriteColors '["red", "blue", "green"]'
```

### 3. 自动备份

每次修改配置时，会自动备份原文件到 `settings.json.backup`，确保数据安全。

---

## 📊 配置文件结构

`~/.claude/settings.json` 的结构：

```json
{
  "theme": "dark",
  "notifications": {
    "enabled": true
  },
  "mcpServers": {
    // MCP 服务器配置
  },
  "userPreferences": {
    "language": {
      "output": "简体中文",
      "preference": "所有发给用户的文字都使用简体中文"
    },
    "customSettings": {
      // 您的自定义设置
    }
  }
}
```

**注意**：
- `userPreferences` 是专门用于存储用户自定义偏好的字段
- 其他字段（如 `theme`、`mcpServers`）由 Claude Code 系统管理
- Memory Manager 主要操作 `userPreferences` 字段

---

## 💡 常见用例

### 用例 1：设置语言偏好

```bash
# 设置默认输出语言
/memory set language.output "简体中文"

# 设置代码注释语言
/memory set language.codeComments "简体中文"

# 设置文档语言
/memory set language.documentation "简体中文"
```

### 用例 2：工作习惯配置

```bash
# 设置默认代码风格
/memory set coding.style "google"

# 设置默认测试框架
/memory set coding.testFramework "pytest"

# 设置是否总是包含类型注解
/memory set coding.alwaysTypeHints true
```

### 用例 3：项目偏好

```bash
# 设置默认项目模板
/memory set project.defaultTemplate "python-poetry"

# 设置默认 Git 分支命名
/memory set project.branchNaming "feature/{issue-id}-{description}"
```

---

## 🎓 最佳实践

### 1. 使用有意义的键名

✅ **好**：
```bash
/memory set language.output "简体中文"
/memory set coding.indentation 2
```

❌ **差**：
```bash
/memory set lang "简体中文"
/memory set indent 2
```

### 2. 使用嵌套结构组织配置

✅ **好**：
```bash
/memory set language.output "简体中文"
/memory set language.docs "简体中文"
/memory set language.comments "简体中文"
```

❌ **差**：
```bash
/memory set outputLanguage "简体中文"
/memory set docsLanguage "简体中文"
/memory set commentsLanguage "简体中文"
```

### 3. 定期备份重要配置

```bash
# 查看配置文件位置
/memory path

# 手动复制到安全位置
# 配置文件：~/.claude/settings.json
# 备份文件：~/.claude/settings.json.backup
```

---

## 🔒 安全注意事项

1. **不要存储敏感信息**：
   - ❌ 不要存储 API keys、密码
   - ✅ 使用环境变量或 secrets 管理工具

2. **权限控制**：
   - `settings.json` 文件权限应设为 `600`（仅所有者可读写）

3. **备份策略**：
   - 定期备份 `settings.json`
   - 使用版本控制（Git）管理配置文件

---

## 🛠️ 程序化使用

### Python 脚本示例

```python
from memory_tool import MemoryManager

# 初始化管理器
manager = MemoryManager()

# 读取偏好
lang = manager.get('language.output')
print(f"当前语言：{lang}")

# 设置偏好
manager.set('language.output', '简体中文')

# 显示所有偏好
prefs = manager.show_all()
print(prefs)

# 删除偏好
manager.delete('old_setting')
```

### 命令行使用

```bash
# 使用 Python 脚本
python ~/.claude/skills/35-memory-manager/memory_tool.py show
python ~/.claude/skills/35-memory-manager/memory_tool.py get language.output
python ~/.claude/skills/35-memory-manager/memory_tool.py set language.output "简体中文"
```

---

## 📈 与其他系统的集成

### 与 MCP 的关系

Memory Manager 管理的是 Claude Code 的**本地配置文件**（`settings.json`），而 MCP Memory Server 是一个**独立的记忆服务**。

| 特性 | Memory Manager | MCP Memory Server |
|------|----------------|-------------------|
| **存储位置** | `~/.claude/settings.json` | SQLite 或独立数据库 |
| **适用场景** | 用户偏好、配置 | 知识图谱、上下文记忆 |
| **复杂度** | 简单 | 复杂 |
| **搜索能力** | 键值查找 | 全文搜索、语义搜索 |

**推荐**：
- 使用 Memory Manager 存储**用户偏好**（语言、风格、习惯）
- 使用 MCP Memory Server 存储**知识和上下文**（事实、关系、历史）

---

## 🌟 总结

**Memory Manager** = 简单高效的用户偏好管理工具

✅ 直接读写 `~/.claude/settings.json`  
✅ 支持嵌套键和 JSON 值  
✅ 自动备份，数据安全  
✅ 简体中文输出  
✅ 易于集成和程序化使用

**质量**：生产级  
**状态**：✅ 生产就绪  
**语言**：简体中文 🇨🇳

---

**由 Claude (Sonnet 4.5) 制作**  
**版本**: 1.0.0
