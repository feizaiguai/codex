import re
import html as htmllib
import urllib.request
from pathlib import Path

CREATE_URL = "https://developers.openai.com/codex/skills/create-skill/"
SKILLS_URL = "https://developers.openai.com/codex/skills/"
OUT_PATH = Path(r"C:\Users\bigbao\.codex\skills\reports\codex_skills_official_excerpt.txt")


def fetch(url: str) -> str:
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return htmllib.unescape(text)


def extract_example_skill(html_text: str) -> str:
    match = re.search(
        r"See an example skill.*?<pre[^>]*data-language=\"md\"[^>]*><code>(.*?)</code></pre>",
        html_text,
        re.S,
    )
    if not match:
        return ""
    return strip_tags(match.group(1)).strip()


def extract_best_practices(html_text: str) -> list[str]:
    match = re.search(r"id=\"follow-best-practices\".*?</h2>\s*<ul>(.*?)</ul>", html_text, re.S)
    if not match:
        return []
    items = []
    for li in re.findall(r"<li>(.*?)</li>", match.group(1), re.S):
        item = strip_tags(li).strip()
        if item:
            items.append(item)
    return items


def extract_where_to_save_from_create(html_text: str) -> list[str]:
    match = re.search(
        r"Codex loads skills from these locations.*?<ul>(.*?)</ul>",
        html_text,
        re.S,
    )
    if not match:
        return []
    items = []
    for li in re.findall(r"<li>(.*?)</li>", match.group(1), re.S):
        item = strip_tags(li).strip()
        if item:
            items.append(item)
    return items


def main() -> None:
    create_html = fetch(CREATE_URL)
    example = extract_example_skill(create_html)
    best_practices = extract_best_practices(create_html)
    where_to_save = extract_where_to_save_from_create(create_html)

    lines = []
    lines.append("Example skill:")
    lines.append(example)
    lines.append("")
    lines.append("Best practices:")
    lines.extend([f"- {x}" for x in best_practices])
    lines.append("")
    lines.append("Where to save skills:")
    lines.extend([f"- {x}" for x in where_to_save])

    OUT_PATH.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(str(OUT_PATH))


if __name__ == "__main__":
    main()
