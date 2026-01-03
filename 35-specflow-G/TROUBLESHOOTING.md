# SpecFlow 故障排除指南

**版本**: 1.0.0  
**语言**: 简体中文 🇨🇳

---

## 🔧 已修复的问题

### 问题 1：在其他项目中使用 `/spec` 报错

**症状**：
- 在 skills 目录所在项目中 `/spec` 正常工作
- 在其他项目（如 WWChat）中使用 `/spec` 时报错
- 提示"找不到 30-SpecFlow 或类似的 skill"

**根本原因**：
1. ✅ **路径问题**：原来使用 `~/.claude/skills/` 相对路径，在不同项目中可能解析失败
2. ✅ **缺少明确指令**：slash command 没有明确告诉 Claude 读取哪些文件
3. ✅ **序号冲突**：SpecFlow 从 30 号改为 36 号后，命令未同步更新

**解决方案**：
1. ✅ 使用**绝对路径**：`C:/Users/bigbao/.claude/skills/36-specflow/`
2. ✅ 添加**明确的读取指令**：第 1 步强制读取 SKILL.md 和 README.md
3. ✅ 更新所有引用：从 30-specflow 改为 36-specflow

---

## ✅ 修复验证

### 测试步骤

1. **在任意项目目录中运行**：
   ```bash
   cd /path/to/any/project
   # 然后使用 /spec 命令
   /spec 构建一个测试项目
   ```

2. **Claude 应该执行**：
   ```
   第 1 步：读取 C:/Users/bigbao/.claude/skills/36-specflow/SKILL.md
   第 2 步：读取 C:/Users/bigbao/.claude/skills/36-specflow/README.md
   第 3 步：分析任务描述
   第 4 步：生成 6D 规格文档
   ```

3. **预期结果**：
   - ✅ 无论在哪个目录，都能正确读取 skill 文件
   - ✅ 生成完整的简体中文规格文档
   - ✅ 包含所有 6 个阶段（发现、定义、设计、分解、声明、文档）

---

## 📋 当前配置

### Skill 文件位置

**绝对路径**（Windows）：
```
C:/Users/bigbao/.claude/skills/36-specflow/SKILL.md
C:/Users/bigbao/.claude/skills/36-specflow/README.md
C:/Users/bigbao/.claude/skills/36-specflow/IMPLEMENTATION_SUMMARY.md
C:/Users/bigbao/.claude/skills/36-specflow/examples/ecommerce-platform-spec.md
```

### Slash Command 位置

```
C:/Users/bigbao/.claude/commands/spec.md
```

### 工作流程

```
用户输入 /spec [任务描述]
    ↓
Claude 读取 spec.md 命令定义
    ↓
执行第 1 步：读取 SKILL.md（使用绝对路径）
    ↓
执行第 2 步：读取 README.md（使用绝对路径）
    ↓
执行第 3-5 步：生成规格文档
    ↓
输出简体中文 Markdown 文档
```

---

## 🎯 快速测试

### 测试命令

```bash
/spec 构建一个简单的待办事项应用，支持添加、删除、标记完成功能。预算 10 万，3 个月完成
```

### 预期输出结构

```markdown
# SpecFlow 规格文档：待办事项应用

## 执行摘要
[简体中文摘要]

## 阶段 1：发现 (DISCOVER)
### 1.1 利益相关者
### 1.2 业务目标
### 1.3 约束条件

## 阶段 2：定义 (DEFINE)
### 2.1 功能需求
### 2.2 非功能需求
### 2.3 BDD 场景

## 阶段 3：设计 (DESIGN)
### 3.1 DDD 领域模型
### 3.2 技术栈
### 3.3 架构决策

## 阶段 4：分解 (DECOMPOSE)
### 4.1 WBS 工作分解
### 4.2 PERT 估算
### 4.3 里程碑

## 阶段 5：声明 (DECLARE)
### 5.1 测试策略
### 5.2 性能基准

## 阶段 6：文档 (DOCUMENT)
### 6.1 质量评分
### 6.2 风险评估
### 6.3 实施建议
```

---

## 🔍 常见问题

### Q1: 为什么必须使用绝对路径？

**A**: 因为 Claude Code 在不同项目目录中运行时，相对路径（如 `~/.claude/`）可能解析不一致。绝对路径确保无论在哪个目录都能找到 skill 文件。

### Q2: 如果在 macOS/Linux 上怎么办？

**A**: 修改 `/spec` 命令中的路径：
- Windows: `C:/Users/bigbao/.claude/skills/36-specflow/`
- macOS: `/Users/bigbao/.claude/skills/36-specflow/`
- Linux: `/home/bigbao/.claude/skills/36-specflow/`

### Q3: 为什么是 36-specflow 而不是 30-specflow？

**A**: 因为 30 号已被 `30-knowledge-manager` 占用，为了避免冲突，将 SpecFlow 改为 36 号。

### Q4: 如果还是报错怎么办？

**A**: 检查以下几点：
1. 文件是否存在：`ls C:/Users/bigbao/.claude/skills/36-specflow/SKILL.md`
2. 权限是否正确：确保有读取权限
3. 路径是否正确：根据操作系统调整路径
4. Read tool 是否可用：确保 Claude 可以使用 Read tool

---

## 📚 相关文档

- **SKILL.md**: 完整的 SpecFlow 使用指南
- **README.md**: 快速入门指南
- **IMPLEMENTATION_SUMMARY.md**: 实施总结和技术细节
- **examples/ecommerce-platform-spec.md**: 完整示例规格文档

---

**创建日期**: 2025-12-14  
**最后更新**: 2025-12-14  
**状态**: ✅ 问题已解决
