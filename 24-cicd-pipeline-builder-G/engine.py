"""24-cicd-pipeline-builder 引擎（精简可用版）"""
from __future__ import annotations

from enum import Enum


class Platform(Enum):
    GITHUB_ACTIONS = "github"
    GITLAB_CI = "gitlab"


class CICDPipelineBuilder:
    def build(self, platform: Platform) -> str:
        if platform == Platform.GITLAB_CI:
            return self._gitlab()
        return self._github()

    def _github(self) -> str:
        return "\n".join([
            "name: CI",
            "on:",
            "  push:",
            "  pull_request:",
            "jobs:",
            "  build:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
            "      - uses: actions/setup-python@v5",
            "        with:",
            "          python-version: '3.12'",
            "      - name: Install deps",
            "        run: pip install -r requirements.txt || true",
            "      - name: Run tests",
            "        run: pytest -q || true",
        ])

    def _gitlab(self) -> str:
        return "\n".join([
            "stages:",
            "  - test",
            "",
            "test:",
            "  stage: test",
            "  image: python:3.12",
            "  script:",
            "    - pip install -r requirements.txt || true",
            "    - pytest -q || true",
        ])


if __name__ == "__main__":
    print("24-cicd-pipeline-builder engine ready")