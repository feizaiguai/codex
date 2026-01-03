---
name: 02-architecture-G
description: Architecture design expert for technology stack selection and pattern recommendation. Provides tech stack selection matrix (20+ dimensions), ADR document generation, technical debt assessment, evolution path planning, scale assessment. Use for new project tech selection, architecture refactoring, technical debt evaluation. Works with spec-explorer and specflow outputs.
---

# 02-architecture - 架构设计专家

**版本**: V3.0 Final
**状态**: ✅ 生产就绪
**最后更新**: 2025-12-17
**Gemini评级**: S（卓越）4.92/5.00

## 描述

架构设计专家Skill，基于需求分析结果推荐最佳技术栈和架构模式。能够权衡多种技术方案的利弊，生成Architecture Decision Records (ADR)文档，评估技术债务，并规划系统从MVP到成熟阶段的演化路径。

### 核心能力

1. **技术栈选型**: 推荐适合的编程语言、Web框架、数据库、缓存系统
2. **架构模式推荐**: 微服务、分层架构、事件驱动、CQRS等模式选择
3. **ADR文档生成**: 规范化的架构决策记录，包含背景、决策、权衡
4. **技术债务评估**: 识别潜在技术风险和长期维护成本
5. **演化路径规划**: 从MVP到规模化系统的分阶段演进策略

---

## Instructions

当用户需要架构设计建议时，你将作为架构专家执行以下流程：

### 触发条件
- 用户说"设计架构"或"架构设计"
- 用户说"选择技术栈"或"推荐框架"
- 用户提供需求并询问"用什么技术实现"
- 用户说"写ADR"或"架构决策记录"

### 设计流程

#### 1. 需求理解
- 接收需求分析结果（来自requirements skill）
- 识别系统的核心功能需求
- 提取非功能性需求（性能、可扩展性、安全性）
- 了解约束条件（团队技能、预算、时间、合规要求）

#### 2. 规模评估
根据以下指标判断系统规模：

**Small规模**:
- 用户量: < 1万DAU
- 数据量: < 100GB
- 团队: 1-3人
- 特点: 快速上线，成本优先

**Medium规模**:
- 用户量: 1万-10万DAU
- 数据量: 100GB-1TB
- 团队: 3-10人
- 特点: 平衡性能与复杂度

**Large规模**:
- 用户量: > 10万DAU
- 数据量: > 1TB
- 团队: 10人+
- 特点: 高可用、高性能、可扩展

#### 3. 技术栈选型

**后端语言推荐矩阵**:
| 场景 | 首选 | 理由 |
|------|------|------|
| Web API | Python (FastAPI) / TypeScript (Node.js) | 快速开发,生态丰富 |
| 高并发 | Go / Rust | 性能优越,内存安全 |
| 企业应用 | Java (Spring Boot) / C# (.NET) | 成熟稳定,企业支持 |
| AI/ML集成 | Python | 丰富的AI库 |
| 实时系统 | Go / Elixir | 并发模型优秀 |

**数据库选型矩阵**:
| 需求 | 推荐 | 理由 |
|------|------|------|
| 事务+关系数据 | PostgreSQL | 功能完整,性能优 |
| 高性能读写 | MySQL | 简单高效 |
| 文档存储 | MongoDB | 灵活schema |
| 时序数据 | InfluxDB / TimescaleDB | 时序优化 |
| 图数据 | Neo4j | 关系查询性能 |
| 全文搜索 | Elasticsearch | 搜索+分析 |

**架构模式推荐**:
- **单体分层**: Small规模,快速MVP
- **微服务**: Large规模,团队独立部署
- **CQRS**: 读写分离,高性能查询
- **事件驱动**: 异步处理,解耦服务
- **六边形架构**: 可测试性,领域隔离

#### 4. ADR文档生成

使用以下模板生成ADR:

```markdown
# ADR-{number}: {Title}

**状态**: Accepted / Proposed / Deprecated
**日期**: YYYY-MM-DD
**决策者**: {Team/Person}

## 背景 (Context)
{描述需要决策的问题和背景}

## 决策 (Decision)
{明确的决策内容}

## 理由 (Rationale)
- 优势1
- 优势2
- 适合当前场景的原因

## 权衡 (Trade-offs)
- 学习曲线: Low/Medium/High
- 生态成熟度: Low/Medium/High
- 长期维护成本: Low/Medium/High
- 团队熟悉度: Low/Medium/High

## 替代方案 (Alternatives Considered)
- 方案A: {理由为什么不选}
- 方案B: {理由为什么不选}

## 后果 (Consequences)
- 正面: {好的影响}
- 负面: {需要注意的问题}

## 合规性 (Compliance)
{如果有合规要求,说明如何满足}
```

#### 5. 风险评估

识别以下类型的风险:
- **技术风险**: 新技术不成熟、性能瓶颈
- **团队风险**: 学习曲线过陡、缺乏经验
- **运维风险**: 部署复杂、监控困难
- **成本风险**: 许可费用、云资源成本

风险等级:
- **低风险**: 已知解决方案,团队熟悉
- **中风险**: 可控,有备选方案
- **高风险**: 不确定性大,需要验证

#### 6. 演化路径规划

典型演化路线:

```
Phase 1: MVP (0-3个月)
- 单体应用
- 关系型数据库
- 手动部署
- 目标: 快速验证市场

Phase 2: Growth (3-12个月)
- 添加缓存层 (Redis)
- 引入消息队列 (RabbitMQ/Kafka)
- CI/CD自动化
- 目标: 支撑用户增长

Phase 3: Scale (12+个月)
- 微服务拆分
- 数据库分库分表
- Kubernetes编排
- 多区域部署
- 目标: 高可用+可扩展
```

### 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| requirements | object | 是 | - | 需求分析结果（来自requirements skill） |
| constraints | object | 否 | {} | 约束条件 |
| constraints.budget | string | 否 | "medium" | 预算: `low`/`medium`/`high` |
| constraints.team_size | number | 否 | 5 | 团队人数 |
| constraints.team_skills | string[] | 否 | [] | 团队技能栈 (e.g., ["Python", "React"]) |
| constraints.timeline | string | 否 | "6 months" | 上线时间要求 |
| constraints.compliance | string[] | 否 | [] | 合规要求 (e.g., ["GDPR", "HIPAA"]) |
| scale | string | 否 | "medium" | 系统规模: `small`/`medium`/`large` |
| existing_systems | object[] | 否 | [] | 现有系统（用于迁移场景） |

### 输出格式

```typescript
interface ArchitectureDesign {
  tech_stack: {
    language: string;          // e.g., "Python 3.11+"
    framework: string;         // e.g., "FastAPI"
    database: string;          // e.g., "PostgreSQL 15"
    cache?: string;            // e.g., "Redis"
    message_queue?: string;    // e.g., "RabbitMQ"
    search?: string;           // e.g., "Elasticsearch"
    frontend?: string;         // e.g., "React + TypeScript"
  };

  architecture_pattern: string; // e.g., "Layered + CQRS"

  adr: ArchitectureDecisionRecord[];

  risks: {
    level: "low" | "medium" | "high";
    category: "technical" | "team" | "operational" | "cost";
    description: string;
    mitigation: string;
  }[];

  evolution_roadmap: {
    phase: string;
    duration: string;
    goals: string[];
    tech_changes: string[];
  }[];

  deployment_strategy: {
    environment: "cloud" | "on-premise" | "hybrid";
    platform: string;           // e.g., "AWS", "Azure", "GCP"
    ci_cd: string;             // e.g., "GitHub Actions"
    monitoring: string;        // e.g., "Prometheus + Grafana"
  };

  cost_estimate: {
    initial: string;           // e.g., "$5,000"
    monthly: string;           // e.g., "$500/month"
    breakdown: {
      infrastructure: string;
      licenses: string;
      development: string;
    };
  };
}
```

---


---

## TypeScript接口

### 基础输出接口

所有Skill的输出都继承自`BaseOutput`统一接口：

```typescript
interface BaseOutput {
  success: boolean;
  error?: {
    code: string;
    message: string;
    suggestedFix?: string;
  };
  metadata?: {
    requestId: string;
    timestamp: string;
    version: string;
  };
  warnings?: Array<{
    code: string;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>;
}
```

### 输入接口

```typescript
interface ArchitectureDesignInput {
}
```

### 输出接口

```typescript
interface ArchitectureDesignOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例 1: 电商平台架构设计

**用户输入:**
```
设计一个电商平台架构，预计10万日活用户，团队5人有Python背景，
6个月内上线。需要支持商品管理、订单处理、支付集成、库存管理。
```

**Skill输出:**

```markdown
# 电商平台架构设计方案

## 系统规模评估
- DAU: 10万 (Medium规模)
- 团队: 5人 (Python背景)
- 时间: 6个月
- 关键功能: 商品、订单、支付、库存

## 推荐技术栈

### 后端
- **语言**: Python 3.11+
- **Web框架**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **异步任务**: Celery + Redis
- **API文档**: 自动生成OpenAPI 3.0

### 数据库
- **主数据库**: PostgreSQL 15
  - 订单、用户、商品数据
  - 支持事务和复杂查询
- **缓存**: Redis
  - 商品详情缓存
  - 购物车数据
  - 会话管理

### 消息队列
- **RabbitMQ**
  - 订单处理异步化
  - 库存扣减
  - 邮件通知

### 前端
- **React 18** + TypeScript
- **状态管理**: Zustand
- **UI组件**: Ant Design
- **构建工具**: Vite

### 部署
- **容器**: Docker
- **CI/CD**: GitHub Actions
- **云平台**: AWS (或阿里云)
  - ECS (计算)
  - RDS (数据库)
  - ElastiCache (Redis)

## 架构模式

### 分层架构 + CQRS

```
┌─────────────────────────────────────┐
│   API Layer (FastAPI Routes)       │
├─────────────────────────────────────┤
│   Command Side    │   Query Side    │
│  (写操作)         │   (读操作)      │
├─────────────────┬─┴─────────────────┤
│  Business Logic │  Read Models      │
├─────────────────┴───────────────────┤
│   Data Access Layer (SQLAlchemy)    │
├─────────────────────────────────────┤
│   PostgreSQL    │      Redis        │
└─────────────────┴───────────────────┘
```

**为什么CQRS?**
- 读操作(商品浏览)远多于写操作(下单)
- 可以独立优化查询性能
- 使用Redis缓存读模型,减少DB压力

## Architecture Decision Records

### ADR-001: 为什么选择FastAPI而不是Django

**状态**: Accepted
**日期**: 2025-12-12

**背景**:
需要选择Python Web框架,团队熟悉Python但没有特定框架经验。

**决策**:
使用FastAPI作为主Web框架。

**理由**:
- **性能优越**: 异步支持,性能接近Go/Node.js
- **开发效率**: 自动数据验证(Pydantic),自动API文档
- **类型安全**: 完整类型提示,IDE支持好
- **学习曲线**: 相对Django更简单,专注API开发
- **生态**: 与现代Python工具链集成好

**权衡**:
- 学习曲线: **Low** (相比Django)
- 生态成熟度: **High**
- 长期维护成本: **Low**
- 团队熟悉度: **Medium** (需要学习async)

**替代方案**:
- **Django**: 功能更全面(Admin后台,ORM),但对于纯API项目过重,性能稍逊
- **Flask**: 更轻量,但缺少自动文档和数据验证,需要更多手动工作

**后果**:
- **正面**: 快速开发,自动文档,高性能API
- **负面**: 需要单独实现Admin后台(可用FastAPI-Admin)

---

### ADR-002: PostgreSQL vs MongoDB

**状态**: Accepted
**日期**: 2025-12-12

**背景**:
电商系统需要存储用户、商品、订单数据,需要选择主数据库。

**决策**:
使用PostgreSQL作为主数据库。

**理由**:
- **事务支持**: 订单处理需要ACID事务(扣库存+创建订单)
- **关系查询**: 订单-商品-用户关系复杂,关系型数据库更合适
- **JSON支持**: PostgreSQL的JSONB类型可以存储灵活数据
- **成熟度**: 生态完善,工具丰富,团队易于招聘

**权衡**:
- 学习曲线: **Low** (SQL是标准技能)
- 生态成熟度: **Very High**
- 扩展性: **High** (支持分区表)

**替代方案**:
- **MongoDB**: 灵活schema,但缺少事务支持(早期版本),关系查询性能差
- **MySQL**: 也是好选择,但PostgreSQL功能更强(JSONB,全文搜索)

**后果**:
- **正面**: 数据一致性保障,查询性能好
- **负面**: 水平扩展需要Sharding(但10万DAU暂时不需要)

---

### ADR-003: 订单处理异步化

**状态**: Accepted
**日期**: 2025-12-12

**背景**:
订单处理涉及多个步骤(库存扣减、支付、通知),同步处理会导致接口响应慢。

**决策**:
使用Celery + RabbitMQ实现订单异步处理。

**理由**:
- **响应速度**: 用户下单接口立即返回,后台异步处理
- **可靠性**: 消息持久化,任务失败可重试
- **解耦**: 订单服务和库存服务通过消息队列解耦

**流程**:
```python
# 用户下单 (FastAPI endpoint)
@app.post("/orders")
async def create_order(order: OrderCreate):
    # 1. 快速验证
    validate_order(order)

    # 2. 创建pending订单
    order_id = await db.create_order_pending(order)

    # 3. 发送异步任务
    process_order.delay(order_id)

    # 4. 立即返回
    return {"order_id": order_id, "status": "pending"}

# Celery任务
@celery.task(bind=True, max_retries=3)
def process_order(self, order_id):
    try:
        # 扣库存
        inventory.deduct(order_id)
        # 调用支付
        payment.charge(order_id)
        # 更新订单状态
        db.update_order_status(order_id, "paid")
        # 发送通知
        notification.send_order_confirmation(order_id)
    except Exception as e:
        # 重试机制
        self.retry(exc=e, countdown=60)
```

**权衡**:
- 复杂度: **Medium** (需要管理队列和worker)
- 性能提升: **High** (API响应时间从2s降到200ms)

**替代方案**:
- **Kafka**: 更强大,但对于10万DAU规模过重,RabbitMQ够用
- **同步处理**: 简单,但用户体验差(等待时间长)

---

## 风险评估

### 低风险 ✅
- **技术栈成熟**: Python/FastAPI/PostgreSQL都是成熟技术
- **团队技能**: 团队有Python背景,学习成本低

### 中风险 ⚠️
- **异步编程**: 团队可能不熟悉async/await
  - **缓解**: 提供培训,代码review
- **峰值流量**: 促销活动可能导致流量激增
  - **缓解**: 提前进行压力测试,准备水平扩展方案(增加EC2实例)

### 高风险 ❌
- **无高风险项** (当前架构适合10万DAU规模)

## 演化路径

### Phase 1: MVP (Month 1-3)
**目标**: 核心功能上线,验证市场

**架构**:
- 单体FastAPI应用
- PostgreSQL单库
- Redis缓存
- 手动部署到单台服务器

**功能**:
- 用户注册/登录
- 商品浏览/搜索
- 购物车
- 订单创建(简化流程)

---

### Phase 2: Growth (Month 4-6)
**目标**: 支撑10万DAU,优化性能

**架构升级**:
- ✅ 引入RabbitMQ (订单异步处理)
- ✅ Redis集群 (高可用缓存)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ 容器化部署 (Docker)
- ✅ 负载均衡 (Nginx)

**功能**:
- 支付集成(支付宝/微信支付)
- 库存管理优化
- 邮件/短信通知
- 订单跟踪

---

### Phase 3: Scale (Month 6-12+)
**目标**: 支持百万级DAU,高可用

**架构升级**:
- ✅ 微服务拆分:
  - 用户服务
  - 商品服务
  - 订单服务
  - 支付服务
  - 库存服务
- ✅ 数据库分库分表
- ✅ Kubernetes编排
- ✅ 多区域部署(异地容灾)
- ✅ Elasticsearch (商品搜索)
- ✅ Kafka (替代RabbitMQ)

**运维**:
- Prometheus + Grafana监控
- ELK日志聚合
- 自动扩缩容

## 部署策略

### 环境
- **Cloud Provider**: AWS (或阿里云)
- **Region**: 主region + 备用region (容灾)

### 基础设施 (Phase 2)
```yaml
# AWS Resources
- ECS (Elastic Container Service): 4 x t3.medium
- RDS PostgreSQL: db.t3.large (Multi-AZ)
- ElastiCache Redis: cache.t3.medium (Cluster mode)
- ALB (Application Load Balancer)
- S3 (静态资源 + 备份)
- CloudWatch (监控和日志)
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/
      - name: Lint
        run: ruff check .

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t ecommerce:${{ github.sha }} .
      - name: Push to ECR
        run: |
          aws ecr get-login-password | docker login ...
          docker push ...

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster production \
            --service ecommerce-api \
            --force-new-deployment
```

### 监控
- **Prometheus**: 指标收集(请求量、响应时间、错误率)
- **Grafana**: 可视化Dashboard
- **AlertManager**: 告警(响应时间>1s, 错误率>1%)
- **Sentry**: 异常追踪

## 成本估算

### 初始开发成本
- 开发人员: 5人 x 6个月 x $8,000 = **$240,000**
- 设计师: 1人 x 3个月 x $6,000 = **$18,000**
- 项目管理: 1人 x 6个月 x $7,000 = **$42,000**
- **总计**: **$300,000**

### 月度运营成本 (Phase 2, 10万DAU)
```
AWS基础设施:
- ECS (4 x t3.medium): $120/月
- RDS PostgreSQL (db.t3.large): $150/月
- ElastiCache Redis: $80/月
- ALB: $25/月
- S3 + CloudFront: $50/月
- 数据传输: $100/月
---
小计: $525/月

第三方服务:
- SendGrid (邮件): $50/月
- Twilio (短信): $100/月
- 支付网关费用: 交易量 x 2.5%
---
小计: $150/月 + 交易费

总计: ~$675/月 + 交易费
```

### 扩展成本 (Phase 3, 100万DAU)
```
- ECS: 20实例 x $30 = $600/月
- RDS: db.r5.xlarge = $500/月
- ElastiCache: 3节点 = $300/月
- Elasticsearch: 3节点 = $400/月
- Kubernetes (EKS): $150/月
---
总计: ~$2,500/月 + 数据传输
```
```

---

### 示例 2: SaaS平台架构 (AI驱动的客服系统)

**用户输入:**
```
设计一个AI客服SaaS平台,支持多租户,每个租户可配置自己的AI模型。
预计1000家企业客户,平均每家100个座席,团队10人,需要符合GDPR。
```

**Skill输出:**

```markdown
# AI客服SaaS平台架构设计

## 系统规模评估
- 租户数: 1000家企业
- 并发座席: 10万
- 规模: Large
- 合规: GDPR (数据隐私)

## 推荐技术栈

### 后端
- **语言**: Go (高并发性能)
- **微服务框架**: Go-Micro / gRPC
- **API Gateway**: Kong
- **认证**: OAuth 2.0 + JWT

### 数据库
- **主库**: PostgreSQL (租户配置,用户数据)
  - 使用Row-Level Security (RLS) 实现租户隔离
- **时序库**: TimescaleDB (对话历史,分析数据)
- **向量库**: Pinecone / Weaviate (AI语义搜索)

### AI/ML
- **LLM集成**: OpenAI API / 自部署LLaMA
- **模型管理**: MLflow
- **推理服务**: TensorFlow Serving

### 消息 & 实时
- **WebSocket**: Socket.IO
- **消息队列**: Kafka (高吞吐)
- **流处理**: Apache Flink

### 部署
- **Kubernetes** (多租户隔离)
- **Istio** (Service Mesh,流量管理)
- **Helm** (应用打包)

## 架构模式

### 微服务 + 多租户架构

```
                  ┌──────────────┐
                  │  API Gateway │ (Kong)
                  └───────┬──────┘
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
   ┌───▼────┐      ┌──────▼─────┐    ┌──────▼────┐
   │  认证   │      │  对话服务   │    │  AI服务   │
   │ Service │      │  Service   │    │  Service  │
   └────────┘      └─────┬──────┘    └─────┬─────┘
                         │                  │
                    ┌────▼──────────────────▼────┐
                    │      Kafka (Event Bus)     │
                    └────┬──────────────────┬────┘
                         │                  │
              ┌──────────▼─────┐    ┌──────▼────────┐
              │  分析服务       │    │  通知服务     │
              │  Service       │    │  Service      │
              └────────────────┘    └───────────────┘
```

### 多租户隔离策略

**Database Per Tenant** (推荐):
- 每个租户独立数据库Schema
- PostgreSQL的Schema隔离
- 优点: 数据完全隔离,符合GDPR
- 缺点: 管理复杂度中等

```sql
-- 租户A的数据
CREATE SCHEMA tenant_a;
CREATE TABLE tenant_a.conversations (...);

-- 租户B的数据
CREATE SCHEMA tenant_b;
CREATE TABLE tenant_b.conversations (...);

-- Row-Level Security
CREATE POLICY tenant_isolation ON conversations
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

## ADR-004: 为什么选择Go而不是Python

**状态**: Accepted
**日期**: 2025-12-12

**背景**:
AI客服系统需要处理10万并发WebSocket连接,对性能要求高。

**决策**:
主服务使用Go,AI推理服务使用Python。

**理由**:
- **并发模型**: Go的goroutine轻量,支持百万级并发
- **性能**: 编译型语言,内存占用低
- **部署**: 单一二进制文件,容器化简单
- **AI集成**: Python生态更适合AI,但可以通过gRPC调用

**架构**:
```
Go Services (对话路由,WebSocket,业务逻辑)
    ↕ gRPC
Python Services (AI模型推理,NLP处理)
```

**权衡**:
- Go学习曲线: **Medium** (团队需要学习)
- Python生态: **保留** (AI部分仍用Python)

**替代方案**:
- **全Python**: 性能不足,难以支撑10万并发
- **全Go**: AI生态弱,开发效率低

---

## GDPR合规设计

### 数据隐私
1. **数据加密**:
   - 传输: TLS 1.3
   - 存储: PostgreSQL透明加密
   - 备份: 加密备份到S3

2. **数据访问控制**:
   - RBAC (Role-Based Access Control)
   - 审计日志 (所有数据访问记录)

3. **数据删除权**:
   - 提供 /api/gdpr/delete-user API
   - 级联删除用户所有数据
   - 保留审计日志(符合6年留存要求)

4. **数据可移植性**:
   - 提供 /api/gdpr/export-data API
   - JSON格式导出用户数据

### ADR-005: GDPR数据留存策略

**决策**: 对话数据默认保留2年,可配置

```python
# 自动清理策略
@celery.task
def cleanup_old_conversations():
    """删除超过2年的对话数据"""
    cutoff = datetime.now() - timedelta(days=730)
    db.conversations.delete_many({
        "created_at": {"$lt": cutoff},
        "retention_override": False  # 允许租户延长保留期
    })
```

## 演化路径

### Phase 1: MVP (Month 1-4)
- 单租户版本(验证AI模型效果)
- 基础对话功能
- 简单Dashboard

### Phase 2: Multi-Tenant (Month 5-8)
- 多租户架构
- 租户自助配置
- WebSocket实时对话
- 基础分析报表

### Phase 3: Enterprise (Month 9-12)
- AI模型自定义(Fine-tuning)
- 高级分析(情感分析,关键词提取)
- SSO集成
- 99.9% SLA保障

## 成本估算 (Large规模)

### 月度运营成本 (1000租户,10万座席)
```
Kubernetes集群 (AWS EKS):
- Worker nodes: 20 x m5.2xlarge = $3,000/月
- RDS PostgreSQL: db.r5.2xlarge = $1,200/月
- TimescaleDB (时序): db.r5.xlarge = $600/月
- Pinecone (向量数据库): $500/月
- Kafka集群: 5 x m5.large = $500/月
- Load Balancer: $100/月
---
基础设施小计: $5,900/月

AI推理成本:
- OpenAI API: $2,000/月 (取决于调用量)
- 或自部署LLaMA: GPU实例 4 x g4dn.xlarge = $2,000/月
---
AI成本小计: $2,000-$4,000/月

总计: ~$8,000-$10,000/月
```

每租户成本: $8-$10/月
定价建议: $50-$200/月/租户 (根据座席数)
```

---

## 最佳实践

1. **从约束条件出发**
   - 团队技能是硬约束,选择团队熟悉的技术
   - 预算限制影响云服务选型
   - 合规要求(GDPR/HIPAA)影响架构设计

2. **避免过度工程**
   - Small规模不要用微服务
   - MVP阶段不要纠结完美架构
   - 优先快速验证,再逐步演化

3. **用ADR记录决策**
   - 每个重要技术选择都写ADR
   - 明确记录"为什么不选XX"
   - 方便后续回顾和优化

4. **规划演化路径**
   - 不要一开始就设计最终架构
   - 分阶段演化,每个阶段有明确目标
   - 为未来扩展预留接口

5. **成本意识**
   - 评估云服务成本
   - 考虑开源替代方案(Kubernetes vs ECS)
   - 预估业务增长带来的成本增长

---

## 相关Skills

- **requirements** (需求分析): 提供需求输入
- **code-generator** (代码生成): 基于架构生成项目骨架
- **deployment-orchestrator** (部署编排): 实施部署策略
- **risk-assessor** (风险评估): 深入评估技术风险

---

## 版本历史

- **2.0.0** (2025-12-12): 重构设计,增加ADR模板和多租户架构案例
- **1.0.0** (2025-01-01): 初始版本
