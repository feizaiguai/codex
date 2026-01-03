from pathlib import Path

ROOT = Path(r"C:\Users\bigbao\.claude\skills")


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


handlers = {
    "04-test-automation": '''import argparse
import json
from engine import UnitTestGenerator, TestFramework, Function, MockGenerator, CoverageAnalyzer


def main() -> int:
    parser = argparse.ArgumentParser(description="test-automation handler")
    parser.add_argument("--mode", choices=["unit", "mock", "coverage"], default="unit")
    args = parser.parse_args()

    if args.mode == "unit":
        gen = UnitTestGenerator(TestFramework.PYTEST)
        fn = Function(name="add", params=[{"name": "a", "type": "int"}, {"name": "b", "type": "int"}], return_type="int")
        cases = gen.generate_tests(fn)
        code = gen.generate_test_code(fn, cases[:1])
        payload = {"cases": [c.__dict__ for c in cases], "sample": code}
    elif args.mode == "mock":
        mg = MockGenerator()
        payload = {"fixture": mg.generate_pytest_fixture("db_session", "db = SessionLocal()"), "mock": mg.generate_mock("Service", ["get"])}
    else:
        ca = CoverageAnalyzer()
        data = ca.analyze_coverage("dummy.coverage")
        payload = {"report": ca.generate_coverage_report(data)}

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "06-documentation": '''import argparse
import json
from engine import DocumentationEngine, APIEndpoint


def main() -> int:
    parser = argparse.ArgumentParser(description="documentation handler")
    parser.add_argument("--readme", action="store_true")
    parser.add_argument("--api", action="store_true")
    args = parser.parse_args()

    engine = DocumentationEngine()
    result = {}
    if args.readme or not args.api:
        result["readme"] = engine.generate_readme({"name": "Sample", "description": "Demo project", "features": ["Docs"]})
    if args.api:
        ep = APIEndpoint(path="/api/ping", method="GET", summary="Ping", parameters=[], responses={"200": {"description": "OK"}})
        result["api_docs"] = engine.generate_api_docs([ep])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "08-performance-optimizer": '''import argparse
import json
from engine import PerformanceOptimizer


def main() -> int:
    parser = argparse.ArgumentParser(description="performance optimizer")
    parser.add_argument("--file", help="python file to analyze")
    args = parser.parse_args()

    optimizer = PerformanceOptimizer()
    if args.file:
        issues = optimizer.analyze_file(args.file)
    else:
        sample = "def f(xs):\\n    for x in xs:\\n        for y in xs:\\n            pass\\n"
        issues = optimizer.analyze_code(sample)
    payload = {"issues": [i.__dict__ for i in issues]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "09-accessibility-checker": '''import argparse
import json
from engine import AccessibilityChecker, WCAGLevel


def main() -> int:
    parser = argparse.ArgumentParser(description="accessibility checker")
    parser.add_argument("--level", choices=["A", "AA", "AAA"], default="AA")
    args = parser.parse_args()

    checker = AccessibilityChecker(WCAGLevel(args.level))
    html = "<img src='x'><h1>Title</h1><h3>Subtitle</h3>"
    issues = checker.check_html(html)
    contrast = checker.check_color_contrast("#000000", "#FFFFFF")
    payload = {"issues": [i.__dict__ for i in issues], "contrast": contrast}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "10-quality-gate": '''import argparse
import json
from engine import QualityGate


def main() -> int:
    parser = argparse.ArgumentParser(description="quality gate")
    parser.add_argument("--code", help="code snippet", default="def f(x):\\n    if x:\\n        return x\\n")
    args = parser.parse_args()

    gate = QualityGate()
    report = gate.evaluate_source(args.code)
    payload = report.__dict__
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "20-theme-designer": '''import json
from engine import ThemeDesigner


def main() -> int:
    designer = ThemeDesigner()
    theme = designer.generate_light_theme()
    payload = theme.__dict__
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "22-deployment-orchestrator": '''import argparse
import json
from engine import DeploymentOrchestrator


def main() -> int:
    parser = argparse.ArgumentParser(description="deployment orchestrator")
    parser.add_argument("--strategy", default="rolling")
    args = parser.parse_args()

    orch = DeploymentOrchestrator()
    payload = orch.as_dict(args.strategy)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "23-infrastructure-coder": '''import json
from engine import InfrastructureCoder


def main() -> int:
    coder = InfrastructureCoder()
    vpc = coder.generate_basic_vpc()
    module = coder.generate_terraform_module()
    payload = {"artifacts": [vpc.__dict__, module.__dict__]}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "24-cicd-pipeline-builder": '''import json
from engine import CICDPipelineBuilder


def main() -> int:
    builder = CICDPipelineBuilder()
    spec = builder.generate_github_actions()
    payload = spec.__dict__
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "26-prompt-engineer": '''import argparse
import json
from engine import PromptEngineer


def main() -> int:
    parser = argparse.ArgumentParser(description="prompt engineer")
    parser.add_argument("--prompt", default="Summarize the report")
    args = parser.parse_args()

    pe = PromptEngineer()
    score = pe.score_prompt(args.prompt)
    improved = pe.improve_prompt(args.prompt)
    payload = {"score": score.__dict__, "improved": improved}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "29-knowledge-manager": '''import json
from engine import KnowledgeManager


def main() -> int:
    km = KnowledgeManager()
    sections = km.build_runbook("service outage")
    payload = {"markdown": km.to_markdown(sections)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "33-gemini": '''import argparse
import json
from engine import GeminiEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="gemini handler")
    parser.add_argument("--prompt", default="hello")
    args = parser.parse_args()

    engine = GeminiEngine()
    payload = engine.as_dict(args.prompt)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    "35-specflow": '''import argparse
import json
from engine import SpecflowEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="specflow handler")
    parser.add_argument("--text", default="User can login")
    args = parser.parse_args()

    engine = SpecflowEngine()
    issues = engine.lint(args.text)
    summary = engine.summarize(args.text)
    payload = {"issues": [i.__dict__ for i in issues], "summary": summary}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
}


def main() -> None:
    for skill, content in handlers.items():
        path = ROOT / skill / "handler.py"
        write(path, content)
    print(f"Wrote handlers: {len(handlers)}")


if __name__ == "__main__":
    main()
