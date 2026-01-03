#!/usr/bin/env python3
"""22-deployment-orchestrator CLI"""
import argparse
from pathlib import Path
from engine import DeploymentConfig, DeploymentOrchestrator


def main() -> int:
    parser = argparse.ArgumentParser(
        description="22-deployment-orchestrator: 部署编排器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python handler.py --name codex-app --image nginx:latest --replicas 2 --port 80 --output deploy.yaml
        """,
    )
    parser.add_argument("--name", required=True, help="应用名称")
    parser.add_argument("--image", required=True, help="镜像名称")
    parser.add_argument("--replicas", type=int, default=1, help="副本数")
    parser.add_argument("--port", type=int, default=80, help="端口")
    parser.add_argument("--output", help="输出文件")

    args = parser.parse_args()
    cfg = DeploymentConfig(name=args.name, image=args.image, replicas=args.replicas, port=args.port)
    orchestrator = DeploymentOrchestrator()
    manifest = orchestrator.build(cfg)

    if args.output:
        Path(args.output).write_text(manifest, encoding="utf-8")
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())