# Deployment Orchestrator Skill - 部署编排器

**版本**: 2.0.0
**类型**: DevOps
**质量等级**: A+

## 📋 功能概述

多云部署自动化,支持蓝绿/金丝雀/滚动等高级部署策略。

### 核心能力

1. **多云平台** - Kubernetes/AWS/Azure/GCP全平台支持
2. **高级部署策略** - Blue-Green/Canary/Rolling/A/B Testing
3. **健康检查** - Liveness/Readiness/Startup探针自动配置
4. **自动回滚** - 错误率/延迟/健康检查触发自动回滚
5. **流量管理** - Istio/Linkerd服务网格集成,智能流量控制

## 🚀 使用方法

### Slash Command
```bash
/deploy [应用名] --strategy=[部署策略] --env=[环境]
```

### 自然语言调用
```
部署到生产环境使用金丝雀发布
蓝绿部署到K8s集群
零停机更新应用
```

## 📖 使用示例

### 示例:金丝雀发布到生产
**输入**:
```
/deploy payment-service --strategy=canary --env=production --image=v2.5.0
```

**输出**:
- ✅ 部署策略: Canary Release
- ✅ 阶段1: 10%流量 (2/20 pods)
  - 健康检查: ✓ 正常
  - 错误率: 0.12% (< 1% 阈值)
  - 延迟P95: 145ms (< 200ms 阈值)
  - 持续5分钟,指标稳定
- ✅ 阶段2: 25%流量 (5/20 pods)
  - 监控5分钟,指标正常
- ✅ 阶段3: 50%流量 (10/20 pods)
  - 监控5分钟,指标正常
- ✅ 阶段4: 100%流量 (20/20 pods)
  - 新版本完全部署
  - 旧版本pods已清理
- 📊 总耗时: 23分钟
- 🎉 部署成功!

## 🎯 部署策略对比

### 1. Rolling Update (滚动更新)
**特点**: 逐步替换旧版本,默认K8s策略
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%       # 最多超出25%
    maxUnavailable: 25% # 最多不可用25%

# 示例: 20个pods
# 步骤1: 创建5个新pods (20 + 5 = 25, 125%)
# 步骤2: 删除5个旧pods (20 + 5 - 5 = 20)
# 步骤3: 重复直到全部更新
```

**优点**:
- ✅ 零停机
- ✅ 资源使用平稳
- ✅ 故障影响小

**缺点**:
- ❌ 新旧版本共存
- ❌ 回滚较慢

**适用场景**: 日常发布,向后兼容变更

### 2. Blue-Green (蓝绿部署)
**特点**: 维护两套环境,一键切换流量
```yaml
# Blue环境 (旧版本 v2.4.0)
replicas: 20
label: version=v2.4.0
service: app-blue

# Green环境 (新版本 v2.5.0)
replicas: 20
label: version=v2.5.0
service: app-green

# 流量切换
service-main:
  selector: version=v2.5.0  # Blue → Green
```

**优点**:
- ✅ 即时切换 (秒级)
- ✅ 快速回滚
- ✅ 充分测试

**缺点**:
- ❌ 资源消耗双倍
- ❌ 数据库迁移复杂

**适用场景**: 重大版本发布,需快速回滚

### 3. Canary Release (金丝雀发布)
**特点**: 渐进式流量迁移,降低风险
```yaml
# 阶段1: 10%流量到新版本
replicas_new: 2
replicas_old: 18
traffic: 10% new, 90% old

# 阶段2: 25%流量
replicas_new: 5
replicas_old: 15
traffic: 25% new, 75% old

# 阶段3: 50%流量
replicas_new: 10
replicas_old: 10
traffic: 50% new, 50% old

# 阶段4: 100%流量
replicas_new: 20
replicas_old: 0
traffic: 100% new
```

**优点**:
- ✅ 风险最小
- ✅ 实时监控反馈
- ✅ 灵活控制

**缺点**:
- ❌ 发布时间较长
- ❌ 配置复杂

**适用场景**: 高风险变更,用户敏感功能

### 4. A/B Testing (A/B测试)
**特点**: 基于用户特征分流
```yaml
# A版本: 原功能
traffic: 50%
userSegment: control_group

# B版本: 新功能
traffic: 50%
userSegment: test_group

# 路由规则
if user.id % 2 == 0:
  route to B version
else:
  route to A version
```

**优点**:
- ✅ 功能验证
- ✅ 用户反馈
- ✅ 数据驱动决策

**缺点**:
- ❌ 需业务指标
- ❌ 长期运行成本

**适用场景**: 新功能验证,UI/UX测试

## ☸️ Kubernetes部署

### 完整部署配置
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: production
  labels:
    app: payment-service
    version: v2.5.0
spec:
  replicas: 20
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 5
      maxUnavailable: 5
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
        version: v2.5.0
    spec:
      containers:
      - name: payment-service
        image: company/payment-service:v2.5.0
        ports:
        - containerPort: 8080

        # 健康检查
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3

        # 资源限制
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi

        # 环境变量
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: production
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: host
```

### 自动回滚配置
```yaml
# 回滚触发条件
rollback:
  triggers:
    - type: error_rate
      threshold: 5%        # 错误率 > 5%
      window: 5m          # 5分钟窗口

    - type: latency
      metric: p95
      threshold: 500ms    # P95延迟 > 500ms
      window: 5m

    - type: health_check
      consecutiveFailures: 3  # 连续3次失败

    - type: crash_loop
      restarts: 5         # 5次重启

# 回滚动作
rollbackAction:
  strategy: immediate    # 立即回滚
  version: previous      # 回滚到上一个版本
  notification:
    slack: '#deployments'
    email: ops-team@company.com
```

## ☁️ 多云平台支持

### AWS Lambda (无服务器)
```typescript
// Lambda蓝绿部署
{
  function: 'payment-processor',
  version: 'v2.5.0',
  strategy: 'blue-green',
  alias: {
    production: {
      version1: '$LATEST',     // Green (新版本)
      version1Weight: 0,       // 初始0%流量
      version2: '23',          // Blue (旧版本)
      version2Weight: 100      // 100%流量
    }
  },
  rollout: {
    step1: { v1: 10, v2: 90 },   // 10%流量到新版
    step2: { v1: 50, v2: 50 },   // 50%
    step3: { v1: 100, v2: 0 }    // 100%
  }
}
```

### GCP Cloud Run
```yaml
# Cloud Run流量控制
service: payment-service
revisions:
  - name: payment-service-v2-5-0
    image: gcr.io/company/payment-service:v2.5.0
    traffic: 10%   # 金丝雀流量

  - name: payment-service-v2-4-0
    image: gcr.io/company/payment-service:v2.4.0
    traffic: 90%   # 稳定版本流量

# 自动扩缩容
autoscaling:
  minInstances: 2
  maxInstances: 100
  targetCPU: 70%
  targetConcurrency: 80
```

## 📊 监控和告警

### 部署指标监控
```yaml
# Prometheus指标
deployment_status{app="payment-service", version="v2.5.0"} 1
deployment_replicas_ready{app="payment-service"} 20
deployment_replicas_desired{app="payment-service"} 20

http_request_duration_seconds{quantile="0.95"} 0.145
http_requests_total{status="2xx"} 12456
http_requests_total{status="5xx"} 15

# Grafana Dashboard
- 实时副本数变化
- 错误率趋势图
- 延迟分布图(P50/P90/P95/P99)
- 流量分布(旧版本 vs 新版本)
```

### 告警规则
```yaml
# AlertManager规则
groups:
- name: deployment
  rules:
  - alert: DeploymentReplicasMismatch
    expr: deployment_replicas_ready != deployment_replicas_desired
    for: 5m
    annotations:
      summary: "Deployment replicas mismatch for 5 minutes"

  - alert: HighErrorRate
    expr: rate(http_requests_total{status="5xx"}[5m]) > 0.05
    for: 5m
    annotations:
      summary: "Error rate > 5% for 5 minutes - triggering rollback"
```

## 🛠️ 最佳实践

1. **金丝雀优先**: 生产环境使用金丝雀发布
2. **健康检查必备**: 所有服务配置健康检查
3. **资源限制**: 设置合理的CPU/内存limits
4. **监控告警**: 部署后持续监控关键指标
5. **回滚预案**: 提前测试回滚流程

## 🔗 与其他 Skills 配合

- `infrastructure-coder`: 生成基础设施代码
- `cicd-pipeline-builder`: CI/CD流水线集成
- `system-monitor`: 部署后监控

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
