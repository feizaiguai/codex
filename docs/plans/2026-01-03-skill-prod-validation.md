# Skills Production Validation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在 `C:\Users\bigbao\.codex\skills` 作为独立 git 仓库，对全部 55 个 skills 进行真实数据生产测试（禁止虚拟数据），全部通过后提交并推送到 codex 的 git。

**Architecture:** 以“真实数据测试矩阵 + 逐项执行 + 统一报告”为核心：先初始化独立 git，再统一技能命名元数据与路径引用，构建生产测试矩阵（每个 skill 的真实输入/外部 API 调用），分批执行并修复，最后生成报告并提交/推送。

**Tech Stack:** PowerShell、Python 3.12、git

---

## Progress

- [x] Task 0: 设计文档（已生成 `docs/plans/2026-01-03-skill-prod-validation-design.md`）
- [x] Task 1: 初始化 codex 独立 git 仓库并验证路径隔离
- [x] Task 2: 技能名称后缀一致化（目录 + SKILL.md 前置元信息）
- [~] Task 3: 生产测试标准与矩阵定义（已创建执行器与矩阵骨架，命令待逐项补全）

---

### Task 0: 设计文档

**Files:**
- Create: `C:\Users\bigbao\.codex\skills\docs\plans\2026-01-03-skill-prod-validation-design.md`

**Step 1: 生成设计文档**

Output: `docs/plans/2026-01-03-skill-prod-validation-design.md`

---

### Task 1: 初始化 codex 独立 git 仓库并验证路径隔离

**Files:**
- Create: `C:\Users\bigbao\.codex\skills\.git`
- Create: `C:\Users\bigbao\.codex\skills\.gitignore`

**Step 1: 初始化 git 仓库**

Run: `git init` (workdir: `C:\Users\bigbao\.codex\skills`)
Expected: 输出 “Initialized empty Git repository …”

**Step 2: 创建基础 .gitignore**

```text
# test outputs
reports/
__pycache__/
*.pyc
*.log
.env
```

**Step 3: 确认与 `C:\Users\bigbao\.claude\skills` 独立**

Run: `git rev-parse --show-toplevel` (workdir: `C:\Users\bigbao\.codex\skills`)
Expected: 返回 `C:\Users\bigbao\.codex\skills`

---

### Task 2: 技能名称后缀一致化（目录 + SKILL.md 前置元信息）

**Files:**
- Modify: `C:\Users\bigbao\.codex\skills\**\SKILL.md`
- Create: `C:\Users\bigbao\.codex\skills\tools\fix_skill_names.py`

**Step 1: 编写脚本批量修正 YAML frontmatter 的 name 字段**

```python
# 逻辑：读取每个 SKILL.md 的 name；若不以 -G 结尾则追加 -G
```

**Step 2: 执行脚本并验证**

Run: `python tools\fix_skill_names.py`
Expected: 输出修正数量，且所有 `name:` 以 `-G` 结尾

---

### Task 3: 生产测试标准与矩阵定义

**Files:**
- Create: `C:\Users\bigbao\.codex\skills\tools\skill_prod_matrix.json`
- Create: `C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py`
- Modify: `C:\Users\bigbao\.codex\skills\docs\plans\2026-01-03-skill-prod-validation.md` (记录必要的环境变量)

**Step 1: 定义“功能正常”判定标准**

```text
- 命令退出码 0
- 输出包含真实数据条目（数量 > 0）
- 不包含“fallback/degraded/mock/模拟/示例”标记
- 外部 API 类技能必须使用真实 API 返回
```

**Step 2: 创建生产测试矩阵（每个 skill 一条真实命令）**

```json
{ "name": "15-web-search-G", "command": "python cli.py \"OpenAI GPT-4\" --mode auto --max-results 5 --output json" }
```

**Step 3: 实现 `skill_prod_test.py`**

```python
# 读取矩阵 -> 逐条执行 -> 解析 stdout -> 验证真实数据 -> 生成 results.json/summary.md
```

---

### Task 4: 配置真实外部 API 凭据与测试环境

**Files:**
- Create (local only): `C:\Users\bigbao\.codex\skills\.env`

**Step 1: 填充必须的 API Key（由用户提供）**

```text
YOUTUBE_API_KEY=
NEWSAPI_KEY=
TIANAPI_KEY=
EXA_API_KEY=
BRAVE_API_KEY=
YOU_API_KEY=
PERPLEXITY_API_KEY=
JINA_API_KEY=
```

**Step 2: 通过 PowerShell 导入环境变量并验证**

Run: `Get-Content .env | ForEach-Object { if ($_ -match '^(\w+)=') { $k=$Matches[1]; $v=$_.Split('=',2)[1]; [System.Environment]::SetEnvironmentVariable($k,$v,'Process') } }`
Expected: 变量在当前进程可用

---

### Task 5: 全量真实数据生产测试

**Files:**
- Modify: `C:\Users\bigbao\.codex\skills\reports\skills-prod-real\results.json`
- Modify: `C:\Users\bigbao\.codex\skills\reports\skills-prod-real\summary.md`

**Step 1: 执行生产测试矩阵**

Run: `python tools\skill_prod_test.py --matrix tools\skill_prod_matrix.json --out-dir reports\skills-prod-real`
Expected: 全量 PASS，真实数据条目均大于 0

**Step 2: 若失败则逐项修复**

Run: `python tools\skill_prod_test.py --rerun <skill-name>`
Expected: 单项 PASS

---

### Task 6: 生成最终验证报告

**Files:**
- Modify: `C:\Users\bigbao\.codex\skills\reports\skills-prod-real\summary.md`

**Step 1: 生成汇总报告**

Run: `python tools\skill_prod_test.py --summary --results reports\skills-prod-real\results.json --out reports\skills-prod-real\summary.md`
Expected: Passed=55, Failed=0, Blocked=0

---

### Task 7: 提交并推送到 codex git

**Files:**
- Modify: 全部变更

**Step 1: 查看状态**

Run: `git status -sb`
Expected: 仅显示本次变更

**Step 2: 提交**

Run: `git add .`
Run: `git commit -m "feat: production-validate skills with real data"`
Expected: 1 个提交

**Step 3: 配置远程并推送**

Run: `git remote add origin <codex-git-remote>`
Run: `git push -u origin main`
Expected: 推送成功
