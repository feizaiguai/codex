import argparse
import json
import os
import re
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\bigbao\.codex\skills")
CLAUDE_ROOT = Path(r"C:\Users\bigbao\.claude\skills")

FRONT_MATTER_RE = re.compile(r"^---\s*$", re.M)
DEFAULT_TIMEOUT_SEC = 45


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def is_url(text: str) -> bool:
    return text.startswith("http://") or text.startswith("https://")


def clean_ref(ref: str) -> str:
    return ref.rstrip("),.;\"'&")


def extract_path_refs(text: str) -> list[str]:
    refs = set()
    for m in re.findall(r"[A-Za-z]:[/\\\\][^\\s)\"']+", text):
        refs.add(clean_ref(m))
    for m in re.findall(r"(?:references|scripts|assets|templates)[/\\\\][^\\s)\"']+", text):
        refs.add(clean_ref(m))
    for m in re.findall(r"(?:\\./|\\.\\./)[^\\s)\"']+\\.(?:py|ps1|md|json|yaml|yml|txt|csv|docx|pdf|pptx|xlsx)", text):
        refs.add(clean_ref(m))
    for m in re.findall(r"[^\\s)\"']+\\.(?:py|ps1|md|json|yaml|yml|txt|csv|docx|pdf|pptx|xlsx)", text):
        if "/" in m or "\\" in m:
            refs.add(clean_ref(m))
    return sorted(refs)


def resolve_ref(skill_dir: Path, ref: str) -> Path:
    p = Path(ref)
    if p.is_absolute():
        return p
    return (skill_dir / p)


def inventory_skills() -> list[dict]:
    skills = []
    for skill_dir in find_skill_dirs(ROOT):
        text = read_text(skill_dir / "SKILL.md")
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


def detect_entrypoint(runtime_dir: Path) -> tuple[str | None, str | None]:
    run_test = runtime_dir / "run_test.py"
    if run_test.exists():
        return "python run_test.py", "run_test.py"

    test_files = sorted(runtime_dir.glob("test_*.py"))
    if test_files:
        return f"python {test_files[0].name}", test_files[0].name

    handler = runtime_dir / "handler.py"
    if handler.exists():
        return "python handler.py", "handler.py"

    cli = runtime_dir / "cli.py"
    if cli.exists():
        return "python cli.py --help", "cli.py"

    return None, None


def build_matrix() -> dict:
    skills = []
    for skill_dir in find_skill_dirs(ROOT):
        claude_dir = CLAUDE_ROOT / skill_dir.name
        runtime_dir = claude_dir if claude_dir.exists() else skill_dir
        command, entrypoint = detect_entrypoint(runtime_dir)
        skills.append({
            "name": (read_front_matter(read_text(skill_dir / "SKILL.md")).get("name") or skill_dir.name),
            "codex_path": str(skill_dir),
            "claude_path": str(claude_dir),
            "runtime_dir": str(runtime_dir),
            "command": command,
            "entrypoint": entrypoint,
            "manual_required": command is None,
            "timeout_sec": DEFAULT_TIMEOUT_SEC,
            "notes": "",
        })
    return {
        "generated_at": utc_now_iso(),
        "skills": skills,
    }


def validate_front_matter(skill_dir: Path) -> tuple[bool, list[str]]:
    issues = []
    text = read_text(skill_dir / "SKILL.md")
    fm = read_front_matter(text)
    if not fm.get("name"):
        issues.append("missing front matter name")
    if not fm.get("description"):
        issues.append("missing front matter description")
    return (len(issues) == 0), issues


def validate_refs(skill_dir: Path) -> list[str]:
    text = read_text(skill_dir / "SKILL.md")
    refs = extract_path_refs(text)
    missing = []
    for ref in refs:
        if is_url(ref) or "://" in ref:
            continue
        resolved = resolve_ref(skill_dir, ref)
        if resolved.is_absolute():
            resolved_str = str(resolved).lower()
            if not (
                resolved_str.startswith(str(ROOT).lower())
                or resolved_str.startswith(str(CLAUDE_ROOT).lower())
            ):
                continue
        if not resolved.exists():
            missing.append(ref)
    return missing


def command_entry_file(command: str) -> str | None:
    if not command:
        return None
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    if not tokens:
        return None
    exe = tokens[0].lower()
    if exe.endswith("python") or exe in {"python", "py"}:
        if len(tokens) > 1 and not tokens[1].startswith("-"):
            return tokens[1]
    return None


def is_blocked_error(output: str) -> bool:
    needles = [
        "api key",
        "apikey",
        "token",
        "unauthorized",
        "forbidden",
        "401",
        "403",
        "no module named",
        "modulenotfounderror",
        "importerror",
        "pip install",
    ]
    out_lower = output.lower()
    return any(n in out_lower for n in needles)


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    return json.loads(text)


def dry_run(matrix_path: Path, out_dir: Path) -> dict:
    matrix = load_json(matrix_path)
    results = []

    for entry in matrix.get("skills", []):
        name = entry.get("name") or "unknown"
        codex_path = Path(entry.get("codex_path", ""))
        claude_path = Path(entry.get("claude_path", ""))
        runtime_dir = Path(entry.get("runtime_dir", "")) if entry.get("runtime_dir") else claude_path
        command = entry.get("command")
        manual_required = entry.get("manual_required", False)

        issues = []
        warnings = []
        front_ok, front_issues = validate_front_matter(codex_path)
        issues.extend(front_issues)

        missing_refs = validate_refs(codex_path)
        if missing_refs:
            warnings.append("missing referenced files")

        if not claude_path.exists():
            issues.append("missing claude skill dir")

        if manual_required:
            status = "blocked"
            issues.append("manual_required")
        else:
            if not runtime_dir.exists():
                issues.append("runtime dir missing")
            entry_file = command_entry_file(command) if command else None
            if entry_file:
                entry_path = Path(entry_file)
                if not entry_path.is_absolute():
                    entry_path = runtime_dir / entry_path
                if not entry_path.exists():
                    issues.append(f"entrypoint missing: {entry_file}")
            elif not command:
                issues.append("missing command")

            status = "pass" if len(issues) == 0 else "fail"

        results.append({
            "name": name,
            "status": status,
            "command": command,
            "runtime_dir": str(runtime_dir),
            "front_matter_ok": front_ok,
            "missing_refs": missing_refs,
            "warnings": warnings,
            "issues": issues,
        })

    payload = {
        "generated_at": utc_now_iso(),
        "mode": "dry-run",
        "results": results,
    }
    ensure_dir(out_dir)
    out_path = out_dir / "dry-run.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"Wrote dry-run report: {out_path}")
    return payload


def run_matrix(matrix_path: Path, out_dir: Path) -> dict:
    matrix = load_json(matrix_path)
    ensure_dir(out_dir)
    logs_dir = out_dir / "logs"
    ensure_dir(logs_dir)

    results = []

    for entry in matrix.get("skills", []):
        name = entry.get("name") or "unknown"
        codex_path = Path(entry.get("codex_path", ""))
        claude_path = Path(entry.get("claude_path", ""))
        runtime_dir = Path(entry.get("runtime_dir", "")) if entry.get("runtime_dir") else claude_path
        command = entry.get("command")
        manual_required = entry.get("manual_required", False)
        timeout_sec = int(entry.get("timeout_sec", DEFAULT_TIMEOUT_SEC))

        issues = []
        warnings = []
        front_ok, front_issues = validate_front_matter(codex_path)
        issues.extend(front_issues)
        missing_refs = validate_refs(codex_path)
        if missing_refs:
            warnings.append("missing referenced files")
        if not claude_path.exists():
            issues.append("missing claude skill dir")

        if manual_required or not command:
            results.append({
                "name": name,
                "status": "blocked",
                "command": command,
                "runtime_dir": str(runtime_dir),
                "warnings": warnings,
                "issues": issues + ["manual_required"],
                "exit_code": None,
                "stdout_path": None,
                "stderr_path": None,
                "duration_ms": 0,
            })
            continue

        if not runtime_dir.exists():
            results.append({
                "name": name,
                "status": "fail",
                "command": command,
                "runtime_dir": str(runtime_dir),
                "warnings": warnings,
                "issues": issues + ["runtime dir missing"],
                "exit_code": None,
                "stdout_path": None,
                "stderr_path": None,
                "duration_ms": 0,
            })
            continue

        safe = safe_name(name)
        stdout_path = logs_dir / f"{safe}.stdout.txt"
        stderr_path = logs_dir / f"{safe}.stderr.txt"

        before_files = set(p.name for p in runtime_dir.glob("*"))
        started = time.time()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=runtime_dir,
                timeout=timeout_sec,
            )
            duration_ms = int((time.time() - started) * 1000)
            stdout = proc.stdout or ""
            stderr = proc.stderr or ""
            stdout_path.write_text(stdout, encoding="utf-8", errors="replace")
            stderr_path.write_text(stderr, encoding="utf-8", errors="replace")

            after_files = set(p.name for p in runtime_dir.glob("*"))
            new_files = sorted(list(after_files - before_files))
            output_non_empty = bool(stdout.strip() or stderr.strip() or new_files)

            status = "pass" if proc.returncode == 0 and output_non_empty else "fail"
            combined = f"{stdout}\n{stderr}".strip()
            if status == "fail" and is_blocked_error(combined):
                status = "blocked"
                issues.append("blocked: missing dependency or credentials")

            results.append({
                "name": name,
                "status": status,
                "command": command,
                "runtime_dir": str(runtime_dir),
                "warnings": warnings,
                "issues": issues,
                "exit_code": proc.returncode,
                "stdout_path": str(stdout_path),
                "stderr_path": str(stderr_path),
                "duration_ms": duration_ms,
                "new_files": new_files,
            })
        except subprocess.TimeoutExpired:
            duration_ms = int((time.time() - started) * 1000)
            results.append({
                "name": name,
                "status": "fail",
                "command": command,
                "runtime_dir": str(runtime_dir),
                "warnings": warnings,
                "issues": issues + [f"timeout after {timeout_sec}s"],
                "exit_code": None,
                "stdout_path": None,
                "stderr_path": None,
                "duration_ms": duration_ms,
            })

    payload = {
        "generated_at": utc_now_iso(),
        "mode": "run",
        "results": results,
    }
    out_path = out_dir / "results.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"Wrote run report: {out_path}")
    return payload


def summarize(results_path: Path, out_path: Path) -> None:
    data = load_json(results_path)
    results = data.get("results", [])
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "pass")
    failed = sum(1 for r in results if r.get("status") == "fail")
    blocked = sum(1 for r in results if r.get("status") == "blocked")

    lines = [
        "# Skills Production Smoke Test Summary",
        "",
        f"Total skills: {total}",
        f"Passed: {passed}",
        f"Failed: {failed}",
        f"Blocked: {blocked}",
        "",
        "## Failures",
    ]

    def first_line(path_str: str | None) -> str:
        if not path_str:
            return ""
        path = Path(path_str)
        if not path.exists():
            return ""
        text = read_text(path)
        keywords = ["traceback", "error", "exception", "failed", "timeout", "syntaxerror"]
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            lower = stripped.lower()
            if any(k in lower for k in keywords):
                return stripped[:200]
        for line in text.splitlines():
            if line.strip():
                return line.strip()[:200]
        return text.strip()[:200]

    failures = [r for r in results if r.get("status") == "fail"]
    if not failures:
        lines.append("- None")
    else:
        for r in failures:
            issues = r.get("issues", []) or []
            reason = "; ".join(issues) if issues else ""
            if not reason:
                reason = first_line(r.get("stderr_path")) or first_line(r.get("stdout_path")) or "unknown error"
            lines.append(f"- {r.get('name')}: {reason}")

    lines.extend(["", "## Blockers"])
    blockers = [r for r in results if r.get("status") == "blocked"]
    if not blockers:
        lines.append("- None")
    else:
        for r in blockers:
            reason = "; ".join(r.get("issues", []) or ["blocked"])
            lines.append(f"- {r.get('name')}: {reason}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote summary: {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", action="store_true")
    ap.add_argument("--generate-matrix", action="store_true")
    ap.add_argument("--matrix")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--results")
    ap.add_argument("--out")
    ap.add_argument("--out-dir")
    args = ap.parse_args()

    if args.inventory:
        data = {
            "generated_at": utc_now_iso(),
            "skills": inventory_skills(),
        }
        out_path = Path(args.out) if args.out else ROOT / "reports" / "skills-inventory.json"
        out_path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")
        print(f"Wrote inventory: {out_path}")
        return

    if args.generate_matrix:
        matrix = build_matrix()
        out_path = Path(args.out) if args.out else ROOT / "tools" / "skill_test_matrix.json"
        out_path.write_text(json.dumps(matrix, ensure_ascii=True, indent=2), encoding="utf-8")
        print(f"Wrote matrix: {out_path}")
        return

    if args.dry_run:
        if not args.matrix or not args.out_dir:
            raise SystemExit("--dry-run requires --matrix and --out-dir")
        dry_run(Path(args.matrix), Path(args.out_dir))
        return

    if args.run:
        if not args.matrix or not args.out_dir:
            raise SystemExit("--run requires --matrix and --out-dir")
        run_matrix(Path(args.matrix), Path(args.out_dir))
        return

    if args.summary:
        if not args.results or not args.out:
            raise SystemExit("--summary requires --results and --out")
        summarize(Path(args.results), Path(args.out))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
