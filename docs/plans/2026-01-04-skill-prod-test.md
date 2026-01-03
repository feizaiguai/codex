# Skill Production Test Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Delete skill 32, run real-data production tests for all remaining skills, record any issues, fix them, and re-verify.

**Architecture:** Use the existing test harness (`tools/skill_prod_test.py`) and matrix (`tools/skill_prod_matrix.json`). Run tests with real API keys from local `.env`, collect reports, then fix failures and retest.

**Tech Stack:** PowerShell, Python, local skill scripts, Git

---

### Task 1: Remove 32-codex-G and update test inputs

**Files:**
- Delete: `32-codex-G/`
- Modify: `tools/skill_prod_matrix.json`

**Step 1: Delete the directory**

Run: `Remove-Item -Recurse -Force C:\Users\bigbao\.codex\skills\32-codex-G`

**Step 2: Remove matrix entry**

Edit `tools/skill_prod_matrix.json` to remove the 32-codex-G entry (if present).

**Step 3: Verify directory list**

Run: `Get-ChildItem C:\Users\bigbao\.codex\skills | Select-Object Name`

**Step 4: Commit**

Run:
`git -C C:\Users\bigbao\.codex\skills add -A`
`git -C C:\Users\bigbao\.codex\skills commit -m "chore: remove 32-codex-G"`

### Task 2: Run real-data production tests for all skills

**Files:**
- Read: `.env`
- Read: `tools/skill_prod_matrix.json`
- Output: `reports/skills-prod-real/*`

**Step 1: Execute test runner**

Run: `python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --append`

**Step 2: Verify summary**

Check `reports/skills-prod-real/summary.md` for pass/fail and any failures.

**Step 3: Capture failures list**

Extract failed skill names and error summaries into notes for remediation.

### Task 3: Fix failures and re-test

**Files:**
- Modify: Skill files as needed
- Output: `reports/skills-prod-real/*`

**Step 1: For each failed skill, implement minimal fix**

Apply targeted fixes based on error logs. Avoid behavior changes not required to pass production test.

**Step 2: Re-run tests**

Run: `python C:\Users\bigbao\.codex\skills\tools\skill_prod_test.py --append`

**Step 3: Repeat until all pass**

Continue until `summary.md` shows all skills passing.

**Step 4: Commit**

Run:
`git -C C:\Users\bigbao\.codex\skills add -A`
`git -C C:\Users\bigbao\.codex\skills commit -m "fix: repair failing skills"`

### Task 4: Push to remote

**Step 1: Push**

Run: `git -C C:\Users\bigbao\.codex\skills push`
