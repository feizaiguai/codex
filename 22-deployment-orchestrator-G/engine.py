"""22-deployment-orchestrator 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeploymentConfig:
    name: str
    image: str
    replicas: int = 1
    port: int = 80


def generate_deployment(cfg: DeploymentConfig) -> str:
    return "\n".join([
        "apiVersion: apps/v1",
        "kind: Deployment",
        f"metadata:\n  name: {cfg.name}",
        "spec:",
        f"  replicas: {cfg.replicas}",
        "  selector:",
        "    matchLabels:",
        f"      app: {cfg.name}",
        "  template:",
        "    metadata:",
        "      labels:",
        f"        app: {cfg.name}",
        "    spec:",
        "      containers:",
        "      - name: app",
        f"        image: {cfg.image}",
        "        ports:",
        f"        - containerPort: {cfg.port}",
    ])


def generate_service(cfg: DeploymentConfig) -> str:
    return "\n".join([
        "apiVersion: v1",
        "kind: Service",
        f"metadata:\n  name: {cfg.name}",
        "spec:",
        "  selector:",
        f"    app: {cfg.name}",
        "  ports:",
        f"  - port: {cfg.port}",
        f"    targetPort: {cfg.port}",
        "  type: ClusterIP",
    ])


class DeploymentOrchestrator:
    def build(self, cfg: DeploymentConfig) -> str:
        return generate_deployment(cfg) + "\n---\n" + generate_service(cfg)


if __name__ == "__main__":
    print("22-deployment-orchestrator engine ready")