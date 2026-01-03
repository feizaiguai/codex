# Skills Production Smoke Test Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Validate every skill under `C:\Users\bigbao\.codex\skills` for production readiness by running a concrete smoke test per skill, verifying dependencies, and generating a pass/fail report.

**Architecture:** Build a Python-based smoke test runner that (1) inventories skills in `.codex` and `.claude`, (2) validates SKILL.md metadata and referenced files, (3) executes per-skill smoke tests via discovered scripts or explicit test commands, and (4) writes JSON + Markdown reports. The runner uses a rule-based test matrix with manual overrides to ensure each skill is exercised meaningfully.

**Tech Stack:** Python 3.12 (stdlib only), PowerShell for orchestration.

---

### Task 1: Create test scaffolding and inventory script

**Files:**
- Create: `tools/skill_smoke_test.py`
- Create: `reports/.gitkeep` (optional if directory is empty)

**Step 1: Create the directory structure**

Run: `New-Item -ItemType Directory -Force -Path C:\Users\bigbao\.codex\skills\tools, C:\Users\bigbao\.codex\skills\reports`
Expected: directories exist

**Step 2: Write the failing “inventory” run**

Run: `python tools\skill_smoke_test.py --inventory --out reports\skills-inventory.json`
Expected: FAIL because `tools\skill_smoke_test.py` does not exist yet

**Step 3: Implement `tools/skill_smoke_test.py` (inventory + validators)**

```python
import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(r"C:\Users\bigbao\.codex\skills")
CLAUDE_ROOT = Path(r"C:\Users\bigbao\.claude\skills")

FRONT_MATTER_RE = re.compile(r"^---\s*$", re.M)

def read_front_matter(text: str) -> dict:
    parts = FRONT_MATTER_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        return {}
    raw = parts[1].strip().splitlines()
    data = {}
    for line in raw:
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip()
    return data

def find_skill_dirs(root: Path) -> list[Path]:
    return sorted([p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()])

def extract_path_refs(text: str) -> list[str]:
    refs = set()
    # crude path patterns: Windows absolute, relative folders, and common extensions
    for m in re.findall(r"[A-Za-z]:[/\\\\][^\\s)\"']+", text):
        refs.add(m)
    for m in re.findall(r"(?:references|scripts|assets|templates)/[^\\s)\"']+", text):
        refs.add(m)
    for m in re.findall(r"[^\\s)\"']+\\.(?:py|ps1|md|json|yaml|yml|txt|csv|docx|pdf|pptx|xlsx)", text):
        refs.add(m)
    return sorted(refs)

def resolve_ref(skill_dir: Path, ref: str) -> Path:
    # absolute path stays, relative resolves to skill dir then repo root
    p = Path(ref)
    if p.is_absolute():
        return p
    return (skill_dir / p)

def inventory_skills():
    skills = []
    for skill_dir in find_skill_dirs(ROOT):
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        fm = read_front_matter(text)
        refs = extract_path_refs(text)
        skills.append({
            "name": fm.get("name") or skill_dir.name,
            "description": fm.get("description", ""),
            "codex_path": str(skill_dir),
            "claude_path": str(CLAUDE_ROOT / skill_dir.name),
            "skill_md_refs": refs,
        })
    return skills

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", action="store_true")
    ap.add_argument("--out", required=False)
    args = ap.parse_args()

    if args.inventory:
        data = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "skills": inventory_skills(),
        }
        out_path = Path(args.out) if args.out else ROOT / "reports" / "skills-inventory.json"
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote inventory: {out_path}")
        return

if __name__ == "__main__":
    main()
```

**Step 4: Re-run the inventory**

Run: `python tools\skill_smoke_test.py --inventory --out reports\skills-inventory.json`
Expected: PASS, `reports\skills-inventory.json` exists and lists all skills

---

### Task 2: Add smoke-test discovery and execution modes

**Files:**
- Modify: `tools/skill_smoke_test.py`
- Create: `tools/skill_test_matrix.json`

**Step 1: Write a failing dry-run**

Run: `python tools\skill_smoke_test.py --matrix tools\skill_test_matrix.json --dry-run --out-dir reports\skills-prod-smoke-2026-01-01`
Expected: FAIL because matrix file doesn’t exist yet

**Step 2: Extend `tools/skill_smoke_test.py`**

Add:
- `--generate-matrix` to create a default matrix from heuristics (prefer `run_test.py`, then `test_*.py`, then `handler.py`, then `cli.py`)
- `--dry-run` to only validate paths/commands without executing
- `--run` to execute and capture stdout/stderr per skill
- Check that `.claude\skills\<skill>` exists and report drift if missing
- Validate all path refs in SKILL.md (record missing refs)

**Heuristic defaults:**
- If `run_test.py` exists, command = `python run_test.py`
- Else if `test_*.py` exists, command = `python <first test file>`
- Else if `handler.py` exists, command = `python handler.py`
- Else if `cli.py` exists, command = `python cli.py --help`
- Else mark as “no entrypoint”

**Step 3: Generate the initial matrix**

Run: `python tools\skill_smoke_test.py --generate-matrix --out tools\skill_test_matrix.json`
Expected: PASS, file contains an entry for every skill

**Step 4: Manually review and patch the matrix for required-arg skills**

Edit `tools\skill_test_matrix.json` to override commands where default execution would be invalid.
Examples of overrides:
- `14-weibo-trending`: `python handler.py --limit 3` (keep analysis on)
- `21-baidu-trending`: `python handler.py --limit 3`
- `28-douyin-trending`: `python handler.py --limit 3`
- `30-wechat-trending`: `python handler.py --limit 3`
- `49-ai-news`: `python handler.py --limit 3`
- `56-networkhot-trending`: `python handler.py --limit 3`
- `15-web-search`: `python cli.py "AI news today" --mode fast --max-results 5 --output markdown`
- `37-chrome-automation`: `python handler.py --help` if it requires UI setup
- `50-china-social-media`: `python handler.py --limit 3` (if supported)
- `55-international-media`: `python handler.py --limit 3` (if supported)

---

### Task 3: Dry-run validation across all skills

**Files:**
- Modify: `tools/skill_test_matrix.json` (if dry-run reveals issues)
- Create: `reports/skills-prod-smoke-2026-01-01/dry-run.json`

**Step 1: Run dry-run**

Run: `python tools\skill_smoke_test.py --matrix tools\skill_test_matrix.json --dry-run --out-dir reports\skills-prod-smoke-2026-01-01`
Expected: PASS with per-skill status; failures are missing paths/entrypoints

**Step 2: Fix matrix or note blockers**

Update `tools\skill_test_matrix.json` for any invalid commands or missing args. If a skill has no runnable entrypoint, mark it as `manual_required: true`.

---

### Task 4: Execute production smoke tests (real data)

**Files:**
- Create: `reports/skills-prod-smoke-2026-01-01/results.json`
- Create: `reports/skills-prod-smoke-2026-01-01/summary.md`

**Step 1: Run tests**

Run: `python tools\skill_smoke_test.py --matrix tools\skill_test_matrix.json --run --out-dir reports\skills-prod-smoke-2026-01-01`
Expected: PASS for each skill with exit code 0 and non-empty output file(s)

**Step 2: Generate summary**

Add a `--summary` mode in `tools/skill_smoke_test.py` to aggregate results into Markdown:

```markdown
# Skills Production Smoke Test Summary (2026-01-01)

Total skills: 56
Passed: X
Failed: Y
Blocked (missing deps/keys): Z

## Failures
- <skill>: <reason>

## Blockers
- <skill>: <missing key/dependency>
```

Run: `python tools\skill_smoke_test.py --summary --out reports\skills-prod-smoke-2026-01-01\summary.md --results reports\skills-prod-smoke-2026-01-01\results.json`
Expected: summary lists counts and reasons

---

### Task 5: Define pass/fail criteria (production readiness)

**Criteria:**
- **PASS**: SKILL.md has valid front matter (`name`, `description`), `.claude` skill dir exists, all referenced local files exist, and the smoke-test command exits 0 with non-empty output (or expected artifact).
- **FAIL**: Any of the above fails, or command exits non-zero, or output is empty/invalid.
- **BLOCKED**: Missing API keys/credentials or missing dependencies; record as blocker and skip execution.

**Verification Step:**
Cross-check any external API usage with real calls (non-empty results) for all trending/news/search skills.

