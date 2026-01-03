"""19-ui-component-generator 组件生成引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path


@dataclass
class ComponentSpec:
    name: str
    framework: str
    props: List[str]


class ComponentGenerator:
    def generate(self, spec: ComponentSpec, with_tests: bool = True) -> Dict[str, str]:
        if spec.framework == "vue":
            code = self._generate_vue(spec)
            files = {f"{spec.name}.vue": code}
        else:
            code = self._generate_react(spec)
            files = {f"{spec.name}.jsx": code}

        if with_tests:
            test_code = self._generate_test(spec)
            files[f"{spec.name}.test.js"] = test_code

        return files

    def _generate_react(self, spec: ComponentSpec) -> str:
        props = ", ".join(spec.props) if spec.props else ""
        return "\n".join([
            f"import React from 'react';",
            "",
            f"export default function {spec.name}({{{props}}}) {{",
            "  return (",
            f"    <div className=\"{spec.name}\">",
            f"      <h3>{spec.name}</h3>",
            "    </div>",
            "  );",
            "}",
        ])

    def _generate_vue(self, spec: ComponentSpec) -> str:
        props = ", ".join(spec.props) if spec.props else ""
        return "\n".join([
            "<template>",
            f"  <div class=\"{spec.name}\">",
            f"    <h3>{spec.name}</h3>",
            "  </div>",
            "</template>",
            "",
            "<script>",
            f"export default {{ name: '{spec.name}', props: [{props}] }};",
            "</script>",
        ])

    def _generate_test(self, spec: ComponentSpec) -> str:
        return "\n".join([
            "import { render } from '@testing-library/react';",
            f"import {spec.name} from './{spec.name}';",
            "",
            f"test('renders {spec.name}', () => {{",
            f"  render(<{spec.name} />);",
            "});",
        ])


def save_files(output_dir: str, files: Dict[str, str]) -> List[Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, content in files.items():
        p = out / name
        p.write_text(content, encoding="utf-8")
        paths.append(p)
    return paths


if __name__ == "__main__":
    print("19-ui-component-generator engine ready")
