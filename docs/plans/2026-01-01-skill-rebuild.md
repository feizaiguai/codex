# Skills Full Rebuild Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将全部 55 个 skill 重构到 Codex 官方标准，并确保在生产环境可执行（自动化测试通过、外部依赖可降级）。

**Architecture:** 以“逐技能重建 + 统一执行基线”为核心：规范层（.codex/skills/ SKILL.md）保证触发清晰、元信息完整；运行层（.claude/skills/）提供可靠入口；测试层提供最小可重复用例；统筹层用统一 runner 执行并汇总报告。

**Tech Stack:** Python 3.12、PowerShell、标准库优先。

---

### Task 1: 修复测试脚本语法与编码一致性（批量）

**Files:**
- Create/Modify: `tools/fix_test_files.py`
- Modify: `C:\Users\bigbao\.claude\skills\**\test_*.py`

**Step 1: 修复断裂的 print 字符串**

```python
# 修复 pattern: print("=" * 50 + "\n") 以及 print("\n...") 被拆行导致的语法错误
```

**Step 2: 统一编码为 UTF-8**

Run: `python tools\fix_test_files.py`  
Expected: 语法错误类失败显著下降

---

### Task 2: 修复模板污染导致的 engine.py 语法错误（逐类重写为可用最小实现）

**Files:**
- Modify: `C:\Users\bigbao\.claude\skills\08-performance-optimizer\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\10-quality-gate\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\22-deployment-orchestrator\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\23-infrastructure-coder\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\24-cicd-pipeline-builder\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\26-prompt-engineer\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\29-knowledge-manager\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\33-gemini\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\35-specflow\engine.py`
- Modify: `C:\Users\bigbao\.claude\skills\04-test-automation\engine.py`

**Step 1: 用最小可执行实现替换污染段（保留核心功能点）**

```python
# 示例：保留必要类/函数，输出结构化结果，避免模板残留文本
```

**Step 2: 更新对应 test_*.py 断言（若需）**

Run: `python C:\Users\bigbao\.claude\skills\<skill>\test_*.py`  
Expected: 每个技能 test 脚本可独立运行并退出码 0

---

### Task 3: 修复运行时逻辑错误（重点技能）

**Files:**
- Modify: `C:\Users\bigbao\.claude\skills\01-spec-explorer\modelers\impact.py`
- Modify: `C:\Users\bigbao\.claude\skills\01-spec-explorer\generators\gherkin.py`
- Modify: `C:\Users\bigbao\.claude\skills\01-spec-explorer\core\models.py`
- Modify: `C:\Users\bigbao\.claude\skills\06-documentation\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\09-accessibility-checker\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\12-log-analyzer\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\13-system-monitor\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\16-api-integrator\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\18-youtube-analyzer\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\19-ui-component-generator\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\27-explainability-analyzer\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\31-risk-assessor\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\32-codex\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\34-memory-manager\handler.py`

**Step 1: 修正输入类型不匹配、字段缺失与不一致的模型结构**

```python
# 例如：允许 target_users 既可为 str 也可为 list，并统一转换
```

**Step 2: 修正 handler 输出，保证可序列化并具备稳定字段**

---

### Task 4: 外部 API 可靠性与降级策略

**Files:**
- Modify: `C:\Users\bigbao\.claude\skills\15-web-search\cli.py`
- Modify: `C:\Users\bigbao\.claude\skills\52-reddit-trending\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\53-newsapi\handler.py`
- Modify: `C:\Users\bigbao\.claude\skills\36-deep-research\handler.py`

**Step 1: 加入可配置超时/重试与空结果降级**
**Step 2: 缺 key 时输出可执行提示并返回成功码（附 `status: degraded`）**

---

### Task 5: 为 manual_required 技能补自动入口

**Files:**
- Create: `C:\Users\bigbao\.claude\skills\38-brainstorming\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\39-writing-plans\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\40-executing-plans\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\41-docx\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\42-pdf\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\43-pptx\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\44-xlsx\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\45-senior-architect\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\46-skill-creator\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\47-writing-skills\handler.py`
- Create: `C:\Users\bigbao\.claude\skills\48-skill-list-maintainer\handler.py`

**Step 1: 输出 SKILL.md 摘要 + 验证技能可触发**
**Step 2: 返回结构化 JSON，包含 `status: ok` 与 `next_steps`**

---

### Task 6: 修复 SKILL.md 元信息缺失

**Files:**
- Modify: `C:\Users\bigbao\.codex\skills\46-skill-creator\SKILL.md`
- Modify: `C:\Users\bigbao\.codex\skills\48-skill-list-maintainer\SKILL.md`

**Step 1: 填充 name/description（遵循官方标准）**

---

### Task 7: 回归测试与汇总报告

**Files:**
- Modify: `reports/skills-prod-smoke-2026-01-01/results.json`
- Modify: `reports/skills-prod-smoke-2026-01-01/summary.md`

**Step 1: 全量执行**

Run: `python tools\skill_smoke_test.py --matrix tools\skill_test_matrix.json --run --out-dir reports\skills-prod-smoke-2026-01-01`  
Expected: 全部 PASS

**Step 2: 生成 summary**

Run: `python tools\skill_smoke_test.py --summary --out reports\skills-prod-smoke-2026-01-01\summary.md --results reports\skills-prod-smoke-2026-01-01\results.json`

