"""20-theme-designer 主题生成引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
import json


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def _clamp(x: int) -> int:
    return max(0, min(255, x))


def adjust_lightness(hex_color: str, delta: int) -> str:
    r, g, b = _hex_to_rgb(hex_color)
    r = _clamp(r + delta)
    g = _clamp(g + delta)
    b = _clamp(b + delta)
    return f"#{r:02x}{g:02x}{b:02x}"


@dataclass
class Theme:
    name: str
    colors: Dict[str, str]


class ThemeDesigner:
    def create_theme(self, name: str, primary: str, secondary: str, accent: str) -> Theme:
        colors = {
            "primary": primary,
            "primary_light": adjust_lightness(primary, 40),
            "primary_dark": adjust_lightness(primary, -40),
            "secondary": secondary,
            "accent": accent,
            "background": "#ffffff",
            "text": "#0f172a",
        }
        return Theme(name=name, colors=colors)


class ThemeExporter:
    def to_css_vars(self, theme: Theme) -> str:
        lines = [":root {"]
        for k, v in theme.colors.items():
            lines.append(f"  --{k}: {v};")
        lines.append("}")
        return "\n".join(lines)

    def to_json(self, theme: Theme) -> str:
        return json.dumps({"name": theme.name, "colors": theme.colors}, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("20-theme-designer engine ready")