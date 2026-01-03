import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List

BANNED_MARKERS = [
    "fallback",
    "degraded",
    "mock",
    "模拟",
    "示例数据",
    "fake",
    "dummy",
    "placeholder",
]


def load_matrix(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("matrix", [])
    if not isinstance(data, list):
        raise ValueError("Matrix JSON must be a list or have a top-level 'matrix' list")
    return data


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_env_file(env_path: Path) -> Dict[str, str]:
    if not env_path.exists():
        return {}
    env = {}
    for line in env_path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env[key.strip()] = val.strip()
    return env


def contains_banned_markers(text: str) -> List[str]:
    hits = []
    lowered = text.lower()
    for marker in BANNED_MARKERS:
        if marker in lowered:
            hits.append(marker)
    return hits


def run_entry(entry: Dict[str, Any], base_dir: Path, out_dir: Path) -> Dict[str, Any]:
    name = entry.get("name", "<unnamed>")
    command = entry.get("command")
    cwd = entry.get("cwd")
    requires_env = entry.get("requires_env", []) or []
    must_contain = entry.get("must_contain", []) or []
    min_output_lines = int(entry.get("min_output_lines", 5))
    min_output_chars = int(entry.get("min_output_chars", 200))

    env_from_file = load_env_file(base_dir / ".env")
    merged_env = os.environ.copy()
    merged_env.update(env_from_file)
    missing_env = [k for k in requires_env if not merged_env.get(k)]
    result: Dict[str, Any] = {
        "name": name,
        "command": command,
        "cwd": cwd,
        "requires_env": requires_env,
        "status": "unknown",
        "exit_code": None,
        "duration_sec": None,
        "missing_env": missing_env,
        "banned_markers": [],
        "missing_markers": [],
        "output_lines": 0,
        "output_chars": 0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    if missing_env:
        result["status"] = "blocked"
        result["reason"] = "missing_env"
        return result

    if not command or not isinstance(command, str) or not command.strip():
        result["status"] = "blocked"
        result["reason"] = "missing_command"
        return result

    entry_dir = out_dir / name
    ensure_dir(entry_dir)
    log_path = entry_dir / "stdout.log"

    start = time.time()
    env = merged_env

    proc = subprocess.run(
        command,
        shell=True,
        cwd=str(Path(cwd)) if cwd else str(base_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    duration = time.time() - start
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    combined = stdout + ("\n" if stdout and stderr else "") + stderr

    result["exit_code"] = proc.returncode
    result["duration_sec"] = round(duration, 3)
    result["output_lines"] = combined.count("\n") + (1 if combined else 0)
    result["output_chars"] = len(combined)

    log_path.write_text(combined, encoding="utf-8")

    banned_hits = contains_banned_markers(combined)
    result["banned_markers"] = banned_hits

    missing_required = [m for m in must_contain if m not in combined]
    result["missing_markers"] = missing_required

    if proc.returncode != 0:
        result["status"] = "fail"
        result["reason"] = "nonzero_exit"
        return result

    if result["output_lines"] < min_output_lines or result["output_chars"] < min_output_chars:
        result["status"] = "fail"
        result["reason"] = "insufficient_output"
        return result

    if banned_hits:
        result["status"] = "fail"
        result["reason"] = "banned_markers"
        return result

    if missing_required:
        result["status"] = "fail"
        result["reason"] = "missing_required_markers"
        return result

    result["status"] = "pass"
    return result


def write_summary(results: List[Dict[str, Any]], out_path: Path) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "pass")
    failed = sum(1 for r in results if r.get("status") == "fail")
    blocked = sum(1 for r in results if r.get("status") == "blocked")

    lines = [
        "# Skills Production Validation Summary",
        "",
        f"Total: {total}",
        f"Passed: {passed}",
        f"Failed: {failed}",
        f"Blocked: {blocked}",
        "",
        "## Failures",
    ]
    for r in results:
        if r.get("status") == "fail":
            reason = r.get("reason", "unknown")
            lines.append(f"- {r.get('name')}: {reason}")
    lines.append("")
    lines.append("## Blocked")
    for r in results:
        if r.get("status") == "blocked":
            reason = r.get("reason", "unknown")
            missing_env = r.get("missing_env") or []
            extra = f" (missing env: {', '.join(missing_env)})" if missing_env else ""
            lines.append(f"- {r.get('name')}: {reason}{extra}")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run production tests for Codex skills")
    parser.add_argument("--matrix", required=False, default="tools/skill_prod_matrix.json")
    parser.add_argument("--out-dir", required=False, default="reports/skills-prod-real")
    parser.add_argument("--rerun", required=False)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=0)
    parser.add_argument("--append", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--results", default="")
    args = parser.parse_args()

    if args.summary:
        results_path = Path(args.results) if args.results else Path(args.out_dir) / "results.json"
        results = json.loads(results_path.read_text(encoding="utf-8"))
        write_summary(results, Path(args.out_dir) / "summary.md")
        return 0

    base_dir = Path(__file__).resolve().parents[1]
    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)

    matrix_path = Path(args.matrix)
    matrix = load_matrix(matrix_path)
    full_matrix = matrix
    if args.rerun:
        matrix = [m for m in matrix if m.get("name") == args.rerun]
        if not matrix:
            raise SystemExit(f"No matrix entry named {args.rerun}")
    elif args.start or args.count:
        start = max(args.start, 0)
        end = start + args.count if args.count else None
        matrix = matrix[start:end]

    results: List[Dict[str, Any]] = []
    for entry in matrix:
        results.append(run_entry(entry, base_dir, out_dir))

    results_path = out_dir / "results.json"
    if args.append and results_path.exists():
        existing = json.loads(results_path.read_text(encoding="utf-8"))
        merged: Dict[str, Dict[str, Any]] = {r.get("name", ""): r for r in existing if r.get("name")}
        for r in results:
            name = r.get("name")
            if name:
                merged[name] = r
        ordered_names = [m.get("name") for m in full_matrix if m.get("name")]
        results = [merged[name] for name in ordered_names if name in merged]

    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    write_summary(results, out_dir / "summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
