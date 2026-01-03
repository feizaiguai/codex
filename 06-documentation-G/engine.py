"""
06-documentation 文档生成引擎（精简可用版）
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
import ast
import datetime


@dataclass
class APIEndpoint:
    method: str
    path: str
    description: str


class DocumentationEngine:
    """生成 README/ADR/API 文档的最小可用引擎"""

    def summarize_text(self, text: str) -> Dict[str, object]:
        lines = [l.rstrip() for l in text.splitlines()]
        headings = [l.strip() for l in lines if l.strip().startswith("#")]
        non_empty = [l for l in lines if l.strip()]
        return {
            "line_count": len(lines),
            "non_empty": len(non_empty),
            "headings": headings[:10],
        }

    def extract_python_api(self, source_path: Path) -> Dict[str, List[str]]:
        data = {"functions": [], "classes": []}
        try:
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
        except Exception:
            return data

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                data["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                data["classes"].append(node.name)
        return data

    def generate_readme(self, source_path: str, project_name: str | None = None) -> str:
        src = Path(source_path)
        text = src.read_text(encoding="utf-8", errors="replace")
        summary = self.summarize_text(text)
        title = project_name or src.stem
        lines = [
            f"# {title}",
            "",
            "## 概览",
            f"- 源文件: {src.name}",
            f"- 行数: {summary['line_count']}",
            f"- 非空行: {summary['non_empty']}",
            "",
            "## 章节",
        ]
        for h in summary["headings"]:
            lines.append(f"- {h}")
        lines.extend([
            "",
            "## 片段",
            "以下为源文件前 30 行内容摘录：",
            "```",
        ])
        excerpt = text.splitlines()[:30]
        lines.extend(excerpt)
        lines.append("```")
        return "\n".join(lines)

    def generate_adr(self, title: str, context: str, decision: str, consequences: str) -> str:
        date_str = datetime.date.today().isoformat()
        lines = [
            f"# ADR: {title}",
            "",
            f"- 日期: {date_str}",
            "- 状态: 已接受",
            "",
            "## 背景",
            context or "未提供背景信息。",
            "",
            "## 决策",
            decision or "未提供决策内容。",
            "",
            "## 影响",
            consequences or "未提供影响分析。",
        ]
        return "\n".join(lines)

    def generate_api_docs(self, source_path: str) -> str:
        src = Path(source_path)
        api = self.extract_python_api(src)
        lines = [
            f"# API 文档 - {src.name}",
            "",
            "## 类",
        ]
        if api["classes"]:
            lines.extend([f"- {c}" for c in sorted(api["classes"])])
        else:
            lines.append("- 未检测到类")
        lines.extend(["", "## 函数"]) 
        if api["functions"]:
            lines.extend([f"- {f}" for f in sorted(api["functions"])])
        else:
            lines.append("- 未检测到函数")
        return "\n".join(lines)

    def generate_all_docs(self, source_path: str, out_dir: str) -> List[Path]:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        readme = out / "README.generated.md"
        api = out / "API.generated.md"
        adr = out / "ADR.generated.md"

        readme.write_text(self.generate_readme(source_path), encoding="utf-8")
        api.write_text(self.generate_api_docs(source_path), encoding="utf-8")
        adr.write_text(self.generate_adr("默认决策", "自动生成", "采用标准模板", "便于追踪"), encoding="utf-8")
        return [readme, api, adr]


def generate_readme(source_path: str, project_name: str | None = None) -> str:
    return DocumentationEngine().generate_readme(source_path, project_name)


def generate_adr(title: str, context: str, decision: str, consequences: str) -> str:
    return DocumentationEngine().generate_adr(title, context, decision, consequences)


def generate_api_docs(source_path: str) -> str:
    return DocumentationEngine().generate_api_docs(source_path)


def generate_all_docs(source_path: str, out_dir: str) -> List[Path]:
    return DocumentationEngine().generate_all_docs(source_path, out_dir)


if __name__ == "__main__":
    print("06-documentation engine ready")