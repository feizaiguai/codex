# Web Search Brave Fix & Full Retest Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复 15-web-search-G 的 Brave 连接失败问题，并用真实数据重新测试所有剩余 skills，汇总问题并修复。

**Architecture:** 在 15-web-search-G 中加入引擎可用性检测与替换逻辑，避免 Brave 超时导致失败；然后使用 `tools/skill_prod_test.py` 批量测试与复测。

**Tech Stack:** PowerShell, Python, httpx, 15-web-search-G, skill_prod_test.py

---

### Task 1: 修复 15-web-search-G 的 Brave 连接问题

**Files:**
- Modify: `15-web-search-G/main.py`
- Modify: `15-web-search-G/search.py`

**Step 1: 在 main.py 增加引擎可用性检测**

- 新增 `_is_engine_available` 与 `_filter_engines_by_availability`
- Brave 连接失败时自动移除，并用可用引擎补位（优先 You/Exa）
- 禁止输出包含 fallback/degraded 等词

**Step 2: 在 search.py 同步处理 Brave 不可用时的引擎选择**

- 若 Brave 不可用，fast/auto 改为仅使用 You
- 连接检测使用短超时，避免卡住

**Step 3: 本地验证**

Run:
`cd C:\Users\bigbao\.codex\skills\15-web-search-G`
`python cli.py "AI news yesterday" --mode auto --max-results 5 --time-range day --language zh --output markdown`

确认不再出现 Brave 连接失败提示，且有结果返回。

**Step 4: Commit**

Run:
`git -C C:\Users\bigbao\.codex\skills add -A`
`git -C C:\Users\bigbao\.codex\skills commit -m "fix: avoid brave timeouts in web search"`

---

### Task 2: 真实数据测试全部剩余 skills

**Files:**
- Output: `reports/skills-prod-real/*`

**Step 1: 分批执行测试**

Run (按批次避免超时):
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 0 --count 10 --append`
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 10 --count 10 --append`
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 20 --count 10 --append`
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 30 --count 10 --append`
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 40 --count 10 --append`
`python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --start 50 --count 4 --append`

**Step 2: 查看汇总**

Check:
`C:\Users\bigbao\.codex\skills\reports\skills-prod-real\summary.md`

---

### Task 3: 记录并修复失败项（如有）

**Step 1: 记录失败项名称与原因**

**Step 2: 修复失败项**

**Step 3: 重新跑测试**

重复 Task 2 直到全部通过。

**Step 4: Commit & Push**

Run:
`git -C C:\Users\bigbao\.codex\skills add -A`
`git -C C:\Users\bigbao\.codex\skills commit -m "fix: repair failing skills after retest"`
`git -C C:\Users\bigbao\.codex\skills push`
