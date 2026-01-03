import sys
from pathlib import Path


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def update_frontmatter_name(text: str) -> tuple[str, bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text, False
    try:
        end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return text, False

    changed = False
    for i in range(1, end_idx):
        line = lines[i]
        stripped = line.lstrip()
        if not stripped.startswith("name:"):
            continue
        prefix = line[: len(line) - len(stripped)]
        value = stripped[len("name:") :].strip()
        if not value:
            continue
        quote = ""
        if (value.startswith("\"") and value.endswith("\"")) or (
            value.startswith("'") and value.endswith("'")
        ):
            quote = value[0]
            val = value[1:-1]
        else:
            val = value
        if not val.endswith("-G"):
            val = f"{val}-G"
            new_value = f"{quote}{val}{quote}" if quote else val
            lines[i] = f"{prefix}name: {new_value}"
            changed = True
        break

    if not changed:
        return text, False

    newline = detect_newline(text)
    trailing_newline = text.endswith("\n")
    out = newline.join(lines)
    if trailing_newline:
        out += newline
    return out, True


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    files = list(root.rglob("SKILL.md"))
    updated = 0
    for path in files:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            # Skip files with unexpected encoding
            continue
        new_text, changed = update_frontmatter_name(text)
        if changed:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
    print(f"Updated name field in {updated} SKILL.md files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())