"""
架构设计生成器
负责生成 03-架构设计.md
"""
from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, ComplexityLevel, DomainCategory


class ArchitectureGenerator(BaseGenerator):
    """架构设计生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成架构设计文档

        context 必需字段:
            - complexity: ComplexityLevel
            - domain: DomainCategory
        """
        # 1. 提取数据
        complexity: ComplexityLevel = context['complexity']
        domain: DomainCategory = context['domain']

        # 2. 推荐架构模式和技术栈
        architecture_pattern = self._recommend_architecture_pattern(complexity)
        tech_stack = self._recommend_tech_stack(complexity)

        # 3. 准备模板数据
        template_data = {
            'complexity': complexity.value,
            'domain': domain.value,
            'architecture_pattern': architecture_pattern,
            'tech_stack': tech_stack,
        }

        # 4. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('architecture.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 5. 创建Document对象
        return Document(
            type=DocumentType.ARCHITECTURE,
            title="架构设计",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=20000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 架构概览
        parts.append(f"## 架构概览\n\n")
        parts.append(f"**复杂度级别**: {data['complexity']}\n")
        parts.append(f"**推荐架构模式**: {data['architecture_pattern']}\n\n")
        parts.append(f"根据系统复杂度,推荐使用{data['architecture_pattern']}架构模式.\n\n")

        # 技术栈建议
        parts.append(f"## 技术栈建议\n\n")
        parts.append(f"{data['tech_stack']}\n\n")

        # 系统设计
        parts.append(self._get_system_design(data['architecture_pattern']))

        return "".join(parts)

    def _recommend_architecture_pattern(self, complexity: ComplexityLevel) -> str:
        """基于复杂度推荐架构模式"""
        patterns = {
            "简单": "单体分层架构(Monolithic Layered)",
            "中等": "模块化单体架构(Modular Monolith)",
            "复杂": "微服务架构(Microservices)",
            "非常复杂": "分布式微服务架构(Distributed Microservices)"
        }
        return patterns.get(complexity.value, "模块化单体架构")

    def _recommend_tech_stack(self, complexity: ComplexityLevel) -> str:
        """推荐技术栈(简化版,详细配置在阶段3外部化)"""
        stacks = {
            "简单": """**后端**: Python/Django 或 Node.js/Express
**前端**: React 18+ 或 Vue 3+
**数据库**: PostgreSQL 15+
**缓存**: Redis 7+
**部署**: Docker + Docker Compose""",

            "中等": """**后端**: Python/FastAPI, Java/Spring Boot, 或 Go/Gin
**前端**: React + TypeScript + Next.js
**数据库**: PostgreSQL 15+ (主) + MongoDB (文档) + Redis (缓存)
**消息队列**: RabbitMQ 或 Redis Pub/Sub
**搜索**: Elasticsearch 8+
**部署**: Docker + Kubernetes""",

            "复杂": """**后端**: Java/Spring Cloud, Go, Python/FastAPI (微服务架构)
**前端**: React + TypeScript + 微前端
**API网关**: Kong 或 APISIX
**服务发现**: Consul 或 Nacos
**数据库**: PostgreSQL (主) + MongoDB + Redis Cluster + Elasticsearch
**消息队列**: Apache Kafka + RabbitMQ
**部署**: Kubernetes + Istio + Helm
**监控**: Prometheus + Grafana + Jaeger""",

            "非常复杂": """**后端**: 多语言微服务 (Java/Go/Python)
**前端**: 微前端架构
**API网关**: Kong + GraphQL Federation
**服务发现**: Consul + Nacos
**数据库**: 多数据库架构 (CQRS + Event Sourcing)
**消息队列**: Kafka + Pulsar
**部署**: 多集群 K8s + 服务网格
**监控**: 完整可观测性平台 (Prometheus + Grafana + Jaeger + ELK)"""
        }
        return stacks.get(complexity.value, stacks["中等"])

    def _get_system_design(self, pattern: str) -> str:
        """获取系统设计章节"""
        return f"""## 系统设计

### 分层架构

1. **表示层**: 处理用户交互和API请求
2. **业务层**: 核心业务逻辑
3. **数据层**: 数据持久化和访问

### 关键设计决策

- 采用{pattern}架构以支持系统扩展
- 使用RESTful API进行服务间通信
- 实施缓存策略提升性能
"""
