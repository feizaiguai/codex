import re
from pathlib import Path

ROOT = Path(r"C:\Users\bigbao\.claude\skills")


def read_with_fallback(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def fix_broken_prints(text: str) -> str:
    # Fix broken newline in print("=" * 50 + "\n")
    text = re.sub(
        r'print\("="\s*\*\s*50\s*\+\s*"\s*\n\s*"\)',
        'print("=" * 50 + "\\\\n")',
        text,
        flags=re.S,
    )
    # Fix broken leading newline prints like print("\n...") that are split
    text = re.sub(
        r'print\("\s*\n\s*([^"]+?)"\)',
        lambda m: f'print("\\n{m.group(1)}")',
        text,
        flags=re.S,
    )
    return text


def _sanitize_ascii(value: str) -> str:
    # Keep printable ASCII only to avoid encoding issues in test output.
    return re.sub(r"[^\x20-\x7E]+", " ", value).strip()


def fix_unclosed_prints(text: str) -> str:
    lines = text.splitlines()
    changed = False
    for idx, line in enumerate(lines):
        if 'print("' not in line:
            continue
        # Only fix obvious missing closing quote cases.
        if re.search(r'print\(".*"\)', line):
            continue
        prefix, _, rest = line.partition('print("')
        content = rest
        content = content.replace('")', "")
        content = content.replace('"', "")
        content = _sanitize_ascii(content)
        if not content:
            content = "message"
        lines[idx] = f'{prefix}print("{content}")'
        changed = True
    if not changed:
        return text
    newline = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + newline


def main() -> None:
    changed = 0
    for path in ROOT.rglob("test_*.py"):
        original = read_with_fallback(path)
        updated = fix_broken_prints(original)
        updated = fix_unclosed_prints(updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
        else:
            # Normalize encoding to UTF-8 for consistency
            try:
                path.write_text(original, encoding="utf-8")
            except Exception:
                pass
    print(f"Updated files: {changed}")


if __name__ == "__main__":
    main()
