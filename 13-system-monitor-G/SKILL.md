---
name: 13-system-monitor-G
description: System monitoring expert for full-stack monitoring and health checks. Supports full-stack monitoring (CPU/Memory/Disk/Network), liveness/readiness probes, error tracking integration (Sentry/Datadog), performance metrics (P50/P95/P99), AI trend prediction (capacity planning). Use for system health monitoring, capacity planning, SLA monitoring.
---

# system-monitor - 系统监控专家

**版本**: 2.0.0
**优先级**: P1
**类别**: 调试与监控

---

## 描述

system-monitor是全栈系统监控专家,整合了monitor、health-monitoring、error-tracker的完整功能。实时监控应用和基础设施健康状况,包括CPU、内存、磁盘、网络、应用性能指标。执行Liveness/Readiness探针和依赖服务健康检查。自动捕获和聚合错误(Sentry风格),分析错误趋势。追踪响应时间、吞吐量、错误率、饱和度等关键指标。预测资源使用趋势,提前告警避免故障。

---

## 核心能力

1. **全栈监控**: CPU、内存、磁盘、网络、JVM、容器、数据库、缓存全覆盖
2. **健康检查**: Kubernetes Liveness/Readiness探针,依赖服务健康检测
3. **错误追踪**: 自动捕获异常,聚合相似错误,追踪错误影响范围(Sentry集成)
4. **性能指标**: 响应时间P50/P95/P99、吞吐量QPS、错误率、资源饱和度
5. **趋势分析**: AI预测资源使用,提前告警,自动扩容建议

---

## Instructions

### 监控架构设计

#### 1. 完整监控栈

```yaml
# 监控架构

┌─────────────────────────────────────────────────────┐
│                 用户/运维                            │
└────────────────┬────────────────────────────────────┘
                 │
      ┌──────────┴──────────┐
      │   Grafana仪表板      │  ← 可视化
      └──────────┬──────────┘
                 │
      ┌──────────┴──────────┐
      │   Prometheus         │  ← 指标存储
      └──────────┬──────────┘
                 │
   ┌─────────────┼─────────────┐
   │             │             │
   ▼             ▼             ▼
[App Metrics] [Node Exporter] [Sentry]
   │             │             │
   ▼             ▼             ▼
[应用服务]    [系统资源]    [错误追踪]
```

### 应用层监控

#### 1. Spring Boot Actuator集成

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true  # Kubernetes探针

  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active}
```

#### 2. 自定义业务指标

```java
import io.micrometer.core.instrument.*;

@Service
public class OrderService {

    private final Counter orderCounter;
    private final Counter orderFailureCounter;
    private final Timer orderProcessingTime;
    private final Gauge activeOrders;

    public OrderService(MeterRegistry registry) {
        // 订单计数器
        this.orderCounter = Counter.builder("orders.created")
            .description("Total orders created")
            .tag("type", "online")
            .register(registry);

        // 失败计数器
        this.orderFailureCounter = Counter.builder("orders.failed")
            .description("Failed orders")
            .register(registry);

        // 处理时间
        this.orderProcessingTime = Timer.builder("orders.processing.time")
            .description("Order processing duration")
            .publishPercentiles(0.5, 0.95, 0.99)  // P50, P95, P99
            .register(registry);

        // 活跃订单数(Gauge)
        this.activeOrders = Gauge.builder("orders.active", this, OrderService::getActiveOrderCount)
            .description("Current active orders")
            .register(registry);
    }

    public Order createOrder(OrderRequest request) {
        return orderProcessingTime.record(() -> {
            try {
                Order order = processOrder(request);
                orderCounter.increment();
                return order;
            } catch (Exception e) {
                orderFailureCounter.increment();
                throw e;
            }
        });
    }

    private long getActiveOrderCount() {
        return orderRepository.countByStatus(OrderStatus.PROCESSING);
    }
}
```

#### 3. 健康检查端点

```java
// 自定义健康检查
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            if (conn.isValid(3)) {
                return Health.up()
                    .withDetail("database", "PostgreSQL")
                    .withDetail("connection_pool", getPoolStatus())
                    .withDetail("response_time_ms", measureResponseTime())
                    .build();
            }
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("error", e.getMessage())
                .build();
        }
        return Health.down().build();
    }

    private Map<String, Object> getPoolStatus() {
        HikariDataSource hikari = (HikariDataSource) dataSource;
        return Map.of(
            "active", hikari.getHikariPoolMXBean().getActiveConnections(),
            "idle", hikari.getHikariPoolMXBean().getIdleConnections(),
            "total", hikari.getHikariPoolMXBean().getTotalConnections(),
            "max", hikari.getMaximumPoolSize(),
            "waiting", hikari.getHikariPoolMXBean().getThreadsAwaitingConnection()
        );
    }
}

@Component
public class RedisHealthIndicator implements HealthIndicator {

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @Override
    public Health health() {
        try {
            long start = System.currentTimeMillis();
            String pong = redisTemplate.getConnectionFactory()
                .getConnection()
                .ping();
            long latency = System.currentTimeMillis() - start;

            if ("PONG".equals(pong)) {
                return Health.up()
                    .withDetail("cache", "Redis")
                    .withDetail("latency_ms", latency)
                    .withDetail("status", latency < 100 ? "healthy" : "slow")
                    .build();
            }
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("error", e.getMessage())
                .build();
        }
        return Health.down().build();
    }
}
```

### Kubernetes集成

```yaml
# Deployment with probes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: ecommerce:v1.2.3
        ports:
        - containerPort: 8080

        # 存活探针 - 应用是否活着
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # 就绪探针 - 应用是否准备接收流量
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # 资源限制
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

        env:
        - name: JAVA_OPTS
          value: "-Xms512m -Xmx1g -XX:+PrintGCDetails"
```

### Prometheus配置

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # 应用监控
  - job_name: 'spring-boot-app'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['localhost:8080']

  # 系统监控
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']

  # 数据库监控
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']

  # Redis监控
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']

# 告警规则
rule_files:
  - 'alerts.yml'

# 告警管理器
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
```

### 告警规则

```yaml
# alerts.yml
groups:
  - name: application_alerts
    rules:
      # 高错误率
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          /
          rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate: {{ $value | humanizePercentage }}"
          description: "Error rate above 5% for 5 minutes"

      # 慢响应
      - alert: SlowResponseTime
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency: {{ $value }}s"

      # 内存使用高
      - alert: HighMemoryUsage
        expr: |
          jvm_memory_used_bytes{area="heap"}
          /
          jvm_memory_max_bytes{area="heap"} > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Memory usage: {{ $value | humanizePercentage }}"

      # 数据库连接池耗尽
      - alert: DatabasePoolExhausted
        expr: |
          hikaricp_connections_active / hikaricp_connections_max > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Connection pool 90% full"

  - name: business_alerts
    rules:
      # 订单失败率高
      - alert: HighOrderFailureRate
        expr: |
          rate(orders_failed_total[5m]) / rate(orders_created_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Order failure rate: {{ $value | humanizePercentage }}"
```

### Grafana仪表板

```json
{
  "dashboard": {
    "title": "应用监控大盘",
    "panels": [
      {
        "title": "请求速率 (QPS)",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "P95响应时间",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "错误率",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "JVM内存使用",
        "targets": [
          {
            "expr": "jvm_memory_used_bytes{area=\"heap\"} / jvm_memory_max_bytes{area=\"heap\"}"
          }
        ]
      }
    ]
  }
}
```

### 错误追踪 (Sentry集成)

```python
# Python应用集成Sentry
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,  # 10%请求采样
    environment="production",
    release="v1.2.3",
    before_send=filter_sensitive_data  # 过滤敏感信息
)

def filter_sensitive_data(event, hint):
    """过滤敏感数据"""
    if 'request' in event:
        # 移除敏感header
        event['request']['headers'].pop('Authorization', None)
        event['request']['headers'].pop('Cookie', None)

        # 脱敏query参数
        if 'query_string' in event['request']:
            event['request']['query_string'] = '[REDACTED]'

    return event

# 手动捕获错误
try:
    process_payment(order_id)
except PaymentError as e:
    sentry_sdk.capture_exception(e)
    sentry_sdk.set_context("order", {
        "order_id": order_id,
        "amount": amount,
        "payment_method": payment_method
    })
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| monitor_type | string | 是 | - | health/metrics/errors/all |
| targets | array | 否 | [] | 监控目标(服务、主机) |
| interval | number | 否 | 60 | 采集间隔(秒) |
| alert_rules | object | 否 | {} | 告警规则配置 |
| dashboards | array | 否 | [] | 需要生成的仪表板 |

---

## 输出格式

```typescript
interface SystemMonitorOutput {
  health_status: 'healthy' | 'degraded' | 'unhealthy';

  system_metrics: {
    cpu_usage: number;              // CPU使用率 %
    memory_usage: number;           // 内存使用率 %
    disk_usage: number;             // 磁盘使用率 %
    network_rx_bytes: number;       // 网络接收字节
    network_tx_bytes: number;       // 网络发送字节
  };

  application_metrics: {
    response_time_p50: number;      // P50响应时间(ms)
    response_time_p95: number;      // P95响应时间(ms)
    response_time_p99: number;      // P99响应时间(ms)
    error_rate: number;             // 错误率 %
    throughput: number;             // 吞吐量(QPS)
  };

  dependency_health: {
    database: HealthStatus;
    redis: HealthStatus;
    external_apis: HealthStatus[];
  };

  recent_errors: ErrorSummary[];
  active_alerts: Alert[];

  trend_prediction: {
    memory_exhaustion_eta: string;  // 内存耗尽预计时间
    disk_full_eta: string;
    recommended_actions: string[];
  };
}

interface HealthStatus {
  status: 'up' | 'down' | 'degraded';
  latency_ms: number;
  last_check: string;
  details: any;
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
interface SystemMonitorInput {
}
```

### 输出接口

```typescript
interface SystemMonitorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例: 配置生产环境完整监控

**输入**:
```json
{
  "monitor_type": "all",
  "targets": ["ecommerce-app", "payment-service", "user-service"],
  "interval": 30,
  "alert_rules": {
    "high_error_rate": { "threshold": 0.05, "duration": "5m" },
    "slow_response": { "p95_threshold_ms": 1000, "duration": "10m" },
    "high_memory": { "threshold": 0.85, "duration": "5m" }
  },
  "dashboards": ["overview", "application", "business"]
}
```

**输出**:
```yaml
监控配置成功!

系统健康状态: Healthy ✅

当前指标:
  系统资源:
    - CPU: 45% (正常)
    - 内存: 68% (正常)
    - 磁盘: 52% (正常)

  应用性能:
    - P50响应时间: 125ms
    - P95响应时间: 487ms ✅
    - P99响应时间: 892ms ✅
    - 吞吐量: 1,250 QPS
    - 错误率: 0.12% ✅

  依赖健康:
    - 数据库: UP (延迟: 3ms)
    - Redis: UP (延迟: 1ms)
    - 支付网关: UP (延迟: 245ms)

活跃告警: 0个

趋势预测:
  - 内存使用稳定,预计72小时内不会耗尽
  - 磁盘空间充足,预计30天内不会满
  - 无需扩容

仪表板已创建:
  - http://grafana:3000/d/overview
  - http://grafana:3000/d/application
  - http://grafana:3000/d/business
```

---

## Best Practices

### 1. 四个黄金指标

```yaml
# SRE四个黄金指标
golden_signals:
  latency:          # 延迟
    - P50, P95, P99响应时间
    - 数据库查询时间
    - 外部API调用时间

  traffic:          # 流量
    - 每秒请求数(QPS)
    - 每秒事务数(TPS)
    - 并发用户数

  errors:           # 错误
    - HTTP 4xx/5xx错误率
    - 异常抛出率
    - 超时率

  saturation:       # 饱和度
    - CPU使用率
    - 内存使用率
    - 连接池使用率
    - 队列长度
```

### 2. 分层监控

```python
# L1: 基础设施层
infrastructure_metrics = [
    'cpu_usage', 'memory_usage', 'disk_io',
    'network_bandwidth', 'system_load'
]

# L2: 平台层
platform_metrics = [
    'kubernetes_pod_status', 'docker_container_status',
    'database_connections', 'message_queue_depth'
]

# L3: 应用层
application_metrics = [
    'http_request_rate', 'response_time',
    'error_rate', 'active_sessions'
]

# L4: 业务层
business_metrics = [
    'orders_per_minute', 'payment_success_rate',
    'user_signups', 'revenue_per_hour'
]
```

### 3. 监控即代码

```yaml
# monitoring-as-code
# 所有监控配置版本控制
monitoring:
  version: "2.0"
  environments:
    production:
      prometheus:
        retention: 30d
        scrape_interval: 15s
      grafana:
        dashboards:
          - overview.json
          - application.json
      alertmanager:
        routes:
          - critical_alerts.yml
          - warning_alerts.yml
```

---

## Related Skills

- `log-analyzer`: 日志分析
- `alert-manager`: 告警管理
- `debugger`: 问题诊断
- `performance-optimizer`: 性能优化

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | 整合monitor+health+error-tracker,完整监控方案 |
| 1.0.0 | 2025-06-01 | 初始版本 |
