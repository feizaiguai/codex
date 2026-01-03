---
name: 12-log-analyzer-G
description: Log analysis expert for intelligent log parsing and anomaly detection. Supports multi-format auto-recognition (CLF/JSON/Syslog/Custom), AI anomaly detection, event correlation (distributed tracing), timeline reconstruction (incident retrospection), visualization reports. Use for production troubleshooting, performance analysis, security incident investigation.
---

# log-analyzer - 日志分析专家

**版本**: 2.0.0
**优先级**: P0
**类别**: 调试与监控

---

## 描述

log-analyzer是专业的日志分析专家,智能解析多源日志、识别异常模式、关联事件、生成可视化报告。支持CLF、JSON、Syslog、Logfmt等多种日志格式自动识别。通过AI驱动的模式识别快速发现错误、性能异常、安全威胁。跨服务、跨时间关联日志事件,重建请求完整生命周期。生成趋势图、热力图、错误分布等可视化报告,快速定位生产环境问题根因。

---

## 核心能力

1. **智能解析**: 自动识别日志格式(CLF/JSON/Syslog/自定义),提取结构化信息
2. **异常检测**: AI识别错误模式、性能异常(慢查询/超时)、安全威胁(爆破/注入)
3. **事件关联**: 跨服务、跨时间关联日志事件,追踪分布式请求链路
4. **时间线重建**: 重建请求完整生命周期,可视化调用关系
5. **可视化报告**: 生成趋势图、错误热力图、QPS曲线、延迟分布

---

## Instructions

### 日志解析引擎

#### 1. 自动格式识别

```python
def auto_detect_log_format(log_lines):
    """
    自动检测日志格式

    支持格式:
    - Apache CLF: 127.0.0.1 - - [01/Jan/2025:12:00:00 +0000] "GET /api HTTP/1.1" 200 1234
    - JSON: {"timestamp": "2025-01-01T12:00:00Z", "level": "ERROR", ...}
    - Syslog: Jan 1 12:00:00 host app[123]: message
    - Logfmt: level=info timestamp=2025-01-01T12:00:00Z message="User logged in"
    - Custom patterns
    """
    sample = log_lines[:100]  # 采样前100行

    formats = [
        ('clf', r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+ \S+ \S+)" (\d+) (\d+)'),
        ('json', r'^\{.*"timestamp".*"level".*\}$'),
        ('syslog', r'^(\w+ \d+ \d+:\d+:\d+) (\S+) (\S+)\[(\d+)\]: (.*)$'),
        ('logfmt', r'^(\w+=\S+\s*)+$'),
    ]

    for format_name, pattern in formats:
        match_count = sum(1 for line in sample if re.match(pattern, line))
        if match_count / len(sample) > 0.8:
            return format_name

    return 'custom'  # 需要自定义解析规则
```

#### 2. 结构化解析

```python
def parse_log_entry(log_line, log_format):
    """
    将日志行解析为结构化数据

    输出:
    {
        'timestamp': datetime,
        'level': 'INFO|WARN|ERROR',
        'message': str,
        'context': dict,  # 上下文信息
        'metadata': dict  # 元数据
    }
    """
    if log_format == 'json':
        return json.loads(log_line)

    elif log_format == 'clf':
        pattern = r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'
        match = re.match(pattern, log_line)
        if match:
            ip, timestamp_str, method, path, protocol, status, size = match.groups()
            return {
                'timestamp': parse_clf_timestamp(timestamp_str),
                'level': determine_level_from_status(int(status)),
                'client_ip': ip,
                'method': method,
                'path': path,
                'status_code': int(status),
                'response_size': int(size)
            }

    elif log_format == 'syslog':
        pattern = r'^(\w+ \d+ \d+:\d+:\d+) (\S+) (\S+)\[(\d+)\]: (.*)$'
        match = re.match(pattern, log_line)
        if match:
            timestamp_str, host, app, pid, message = match.groups()
            return {
                'timestamp': parse_syslog_timestamp(timestamp_str),
                'host': host,
                'application': app,
                'pid': int(pid),
                'message': message,
                'level': extract_level_from_message(message)
            }

    return None
```

### 异常模式识别

#### 1. 错误模式检测

```python
def detect_error_patterns(parsed_logs):
    """
    识别错误模式

    模式类型:
    1. 频率突增: 错误数突然增加
    2. 新错误: 之前未出现的错误
    3. 错误聚类: 相似错误集中出现
    4. 级联故障: 错误传播链路
    """
    patterns = []

    # 1. 频率突增检测
    error_timeline = build_error_timeline(parsed_logs)
    baseline_rate = calculate_baseline_error_rate(error_timeline)

    for window in sliding_windows(error_timeline, window_size='5min'):
        current_rate = window.error_count / window.duration
        if current_rate > baseline_rate * 3:  # 3倍阈值
            patterns.append({
                'type': 'error_spike',
                'time_range': window.time_range,
                'error_count': window.error_count,
                'baseline': baseline_rate,
                'current_rate': current_rate,
                'increase_factor': current_rate / baseline_rate
            })

    # 2. 新错误检测
    historical_errors = load_historical_error_signatures()
    current_errors = extract_error_signatures(parsed_logs)

    new_errors = current_errors - historical_errors
    if new_errors:
        patterns.append({
            'type': 'new_error_types',
            'count': len(new_errors),
            'errors': list(new_errors),
            'first_occurrence': {
                err: find_first_occurrence(err, parsed_logs)
                for err in new_errors
            }
        })

    # 3. 错误聚类
    error_clusters = cluster_similar_errors(parsed_logs)
    for cluster in error_clusters:
        if cluster.size > 10:  # 阈值
            patterns.append({
                'type': 'error_cluster',
                'signature': cluster.representative,
                'count': cluster.size,
                'affected_components': cluster.components,
                'sample_logs': cluster.samples[:5]
            })

    return patterns
```

#### 2. 性能异常检测

```python
def detect_performance_anomalies(parsed_logs):
    """
    性能异常检测

    检测项:
    - 响应时间异常 (P95/P99超过阈值)
    - 慢查询 (数据库查询 >1s)
    - 超时事件 (连接超时、读超时)
    - 吞吐量下降
    """
    anomalies = []

    # 提取响应时间数据
    response_times = extract_response_times(parsed_logs)

    if response_times:
        p95 = np.percentile(response_times, 95)
        p99 = np.percentile(response_times, 99)

        # 异常阈值: P95 > 2s 或 P99 > 5s
        if p95 > 2000:
            anomalies.append({
                'type': 'high_p95_latency',
                'p95_ms': p95,
                'threshold_ms': 2000,
                'affected_requests': count_requests_above(response_times, 2000)
            })

        if p99 > 5000:
            anomalies.append({
                'type': 'high_p99_latency',
                'p99_ms': p99,
                'threshold_ms': 5000
            })

    # 慢查询检测
    slow_queries = []
    for log in parsed_logs:
        if 'query_time' in log and log['query_time'] > 1000:
            slow_queries.append({
                'timestamp': log['timestamp'],
                'query': log.get('query', 'N/A'),
                'duration_ms': log['query_time'],
                'database': log.get('database', 'unknown')
            })

    if slow_queries:
        anomalies.append({
            'type': 'slow_queries',
            'count': len(slow_queries),
            'samples': slow_queries[:10],  # Top 10
            'max_duration_ms': max(q['duration_ms'] for q in slow_queries)
        })

    # 超时事件
    timeout_events = [
        log for log in parsed_logs
        if any(kw in log.get('message', '').lower()
               for kw in ['timeout', 'timed out', 'connection refused'])
    ]

    if timeout_events:
        anomalies.append({
            'type': 'timeout_events',
            'count': len(timeout_events),
            'services': group_by_service(timeout_events),
            'samples': timeout_events[:5]
        })

    return anomalies
```

#### 3. 安全威胁检测

```python
def detect_security_threats(parsed_logs):
    """
    安全威胁检测

    威胁类型:
    - 暴力破解 (多次失败登录)
    - SQL注入尝试
    - XSS攻击
    - 路径遍历
    - 异常访问模式
    """
    threats = []

    # 1. 暴力破解检测
    failed_logins = defaultdict(list)
    for log in parsed_logs:
        if is_failed_login(log):
            client_ip = log.get('client_ip')
            failed_logins[client_ip].append(log['timestamp'])

    for ip, timestamps in failed_logins.items():
        if len(timestamps) > 10:  # 10次失败
            time_span = (max(timestamps) - min(timestamps)).seconds
            if time_span < 300:  # 5分钟内
                threats.append({
                    'type': 'brute_force_attack',
                    'severity': 'high',
                    'client_ip': ip,
                    'failed_attempts': len(timestamps),
                    'time_span_seconds': time_span,
                    'first_attempt': min(timestamps),
                    'last_attempt': max(timestamps)
                })

    # 2. SQL注入检测
    sql_injection_patterns = [
        r"(?i)(union.*select|select.*from|'; drop table)",
        r"(?i)(or 1=1|and 1=1|' or '1'='1)",
        r"(?i)(exec\(|execute\(|script>)"
    ]

    for log in parsed_logs:
        request_uri = log.get('path', '') + log.get('query_string', '')
        for pattern in sql_injection_patterns:
            if re.search(pattern, request_uri):
                threats.append({
                    'type': 'sql_injection_attempt',
                    'severity': 'critical',
                    'client_ip': log.get('client_ip'),
                    'timestamp': log['timestamp'],
                    'uri': request_uri,
                    'pattern_matched': pattern
                })

    # 3. 异常访问模式
    access_patterns = analyze_access_patterns(parsed_logs)
    for pattern in access_patterns:
        if pattern.is_suspicious:
            threats.append({
                'type': 'suspicious_access_pattern',
                'severity': 'medium',
                'description': pattern.description,
                'client_ip': pattern.ip,
                'indicators': pattern.indicators
            })

    return threats
```

### 事件关联与时间线重建

#### 1. 分布式追踪关联

```python
def correlate_distributed_trace(parsed_logs):
    """
    关联分布式请求链路

    基于:
    - trace_id / request_id
    - correlation_id
    - span_id (OpenTelemetry)
    """
    traces = defaultdict(list)

    for log in parsed_logs:
        trace_id = (
            log.get('trace_id') or
            log.get('request_id') or
            log.get('correlation_id')
        )

        if trace_id:
            traces[trace_id].append(log)

    # 重建调用链
    call_chains = []
    for trace_id, logs in traces.items():
        # 按时间排序
        logs.sort(key=lambda x: x['timestamp'])

        call_chain = {
            'trace_id': trace_id,
            'start_time': logs[0]['timestamp'],
            'end_time': logs[-1]['timestamp'],
            'duration_ms': (logs[-1]['timestamp'] - logs[0]['timestamp']).total_seconds() * 1000,
            'services': list(set(log.get('service') for log in logs)),
            'spans': [
                {
                    'timestamp': log['timestamp'],
                    'service': log.get('service'),
                    'operation': log.get('operation'),
                    'duration_ms': log.get('duration_ms'),
                    'status': log.get('status')
                }
                for log in logs
            ],
            'has_error': any(log.get('level') == 'ERROR' for log in logs)
        }

        call_chains.append(call_chain)

    return call_chains
```

#### 2. 时间线可视化

```python
def build_timeline_visualization(events):
    """
    构建时间线可视化

    输出ASCII时间线:
    14:00 ━━━━┳━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━
              ┃       ┃         ┃
              ↓       ↓         ↓
         [Request] [DB Query] [Error]
    """
    timeline = []

    # 按时间排序
    sorted_events = sorted(events, key=lambda e: e['timestamp'])

    for event in sorted_events:
        timeline.append({
            'time': event['timestamp'].strftime('%H:%M:%S'),
            'type': event['type'],
            'description': event['description'],
            'severity': event.get('severity', 'info')
        })

    # 生成ASCII可视化
    ascii_timeline = generate_ascii_timeline(timeline)

    return ascii_timeline
```

### 智能根因分析

```python
def perform_root_cause_analysis(error_spike, all_logs):
    """
    根因分析

    策略:
    1. 时间线分析: 在错误激增前发生了什么
    2. 依赖分析: 哪些依赖服务出现异常
    3. 代码变更: 是否有最近的部署
    4. 资源分析: CPU/内存/网络是否异常
    """
    analysis = {
        'error_spike': error_spike,
        'root_cause_candidates': []
    }

    # 1. 时间线分析 (错误前30分钟)
    pre_error_window = get_logs_before(
        all_logs,
        error_spike['start_time'],
        minutes=30
    )

    # 查找异常事件
    anomalies_before_error = []

    # 检查部署事件
    deployments = find_deployment_logs(pre_error_window)
    if deployments:
        analysis['root_cause_candidates'].append({
            'type': 'recent_deployment',
            'confidence': 0.85,
            'evidence': deployments,
            'description': f"Deployment {deployments[0]['version']} occurred {calculate_time_diff(deployments[0]['timestamp'], error_spike['start_time'])} before error spike"
        })

    # 检查依赖服务异常
    dependency_errors = find_dependency_errors(pre_error_window)
    if dependency_errors:
        analysis['root_cause_candidates'].append({
            'type': 'dependency_failure',
            'confidence': 0.90,
            'evidence': dependency_errors,
            'description': f"{len(dependency_errors)} dependency errors detected before spike"
        })

    # 检查资源异常
    resource_alerts = find_resource_alerts(pre_error_window)
    if resource_alerts:
        analysis['root_cause_candidates'].append({
            'type': 'resource_exhaustion',
            'confidence': 0.75,
            'evidence': resource_alerts,
            'description': f"Resource alerts: {', '.join(a['type'] for a in resource_alerts)}"
        })

    # 2. 模式匹配 (已知问题库)
    known_issues = match_known_issue_patterns(error_spike)
    if known_issues:
        analysis['root_cause_candidates'].extend(known_issues)

    # 排序候选根因 (按可信度)
    analysis['root_cause_candidates'].sort(
        key=lambda x: x['confidence'],
        reverse=True
    )

    return analysis
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| log_source | string/array | 是 | - | 日志文件路径或日志内容 |
| log_format | string | 否 | auto | clf/json/syslog/custom/auto |
| analysis_type | string | 否 | analyze | parse/analyze/detect_anomaly/correlate/timeline |
| time_range | object | 否 | null | 时间范围过滤 {start, end} |
| filters | object | 否 | {} | 过滤条件 {level, service} |

---

## 输出格式

```typescript
interface LogAnalyzerOutput {
  summary: {
    total_entries: number;
    errors: number;
    warnings: number;
    time_span: string;
  };

  anomalies: Anomaly[];
  error_patterns: ErrorPattern[];
  security_threats: SecurityThreat[];

  timeline: TimelineEvent[];
  distributed_traces: DistributedTrace[];

  root_cause_analysis: RootCauseAnalysis;
  recommendations: Recommendation[];

  visualizations: {
    error_trend_chart: string;      // Base64 PNG
    heatmap: string;
    qps_curve: string;
  };
}

interface Anomaly {
  type: 'error_spike' | 'performance_degradation' | 'resource_exhaustion';
  severity: 'critical' | 'high' | 'medium' | 'low';
  time_range: string;
  description: string;
  metrics: any;
}

interface ErrorPattern {
  signature: string;
  count: number;
  first_occurrence: string;
  last_occurrence: string;
  affected_services: string[];
  sample_logs: string[];
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
interface LogAnalyzerInput {
}
```

### 输出接口

```typescript
interface LogAnalyzerOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例: 分析生产环境500错误激增

**输入**:
```json
{
  "log_source": "/var/log/application.log",
  "analysis_type": "analyze",
  "time_range": {
    "start": "2025-01-15T13:00:00Z",
    "end": "2025-01-15T15:00:00Z"
  }
}
```

**输出**:
```markdown
# 日志分析报告

## 📊 概览

**时间范围**: 2025-01-15 13:00 ~ 15:00 (2小时)
**总日志条目**: 15,432
**错误级别分布**:
- ERROR: 423 (2.7%) ⚠️ 异常高 (平均: 0.3%)
- WARN: 1,234 (8.0%)
- INFO: 13,775 (89.3%)

**HTTP状态码**:
- 500: 387 ⚠️ **激增300%**
- 504: 36
- 200: 14,928

## 🔍 根因分析

### 主要问题: 内存泄漏导致OOM

**证据1**: OutOfMemoryError频繁出现
- 出现次数: 312次
- 首次出现: 14:10:23
- 趋势: 指数增长

**证据2**: JVM堆内存使用
```
13:00 - 72% (正常)
13:30 - 79% (轻微上升)
14:00 - 87% (警告)
14:10 - 94% (严重)
14:20 - 98% (临界) → OOM频发
```

**证据3**: 级联故障链
```
14:10 - 内存87% → GC频繁
14:12 - 系统变慢 → 请求超时
14:15 - Redis超时 → 缓存失效
14:17 - 数据库压力 → 连接池耗尽
14:20 - 支付网关超时 → 订单失败
14:23 - OOM频发 → 服务不可用
```

## 🎯 修复建议

### 紧急措施 (立即)
1. 滚动重启实例
2. 增加堆内存: 2GB → 4GB
3. 启用GC日志

### 短期修复 (24小时)
1. Heap dump分析
2. 优化连接池配置
3. 添加断路器

### 长期改进 (1-2周)
1. 完善监控告警
2. 自动扩容配置
3. 代码审计
```

---

## Best Practices

### 1. 日志聚合架构

```yaml
# ELK Stack配置
logstash:
  inputs:
    - beats: 5044
    - syslog: 5000
  filters:
    - grok: parse_logs
    - mutate: add_fields
  outputs:
    - elasticsearch: localhost:9200

kibana:
  dashboards:
    - error_trends
    - performance_metrics
    - security_threats
```

### 2. 实时告警规则

```python
# 配置告警规则
alert_rules = [
    {
        'name': 'error_spike',
        'condition': 'error_rate > baseline * 3',
        'window': '5min',
        'action': 'send_pagerduty'
    },
    {
        'name': 'slow_queries',
        'condition': 'p95_query_time > 1000ms',
        'window': '10min',
        'action': 'send_slack'
    }
]
```

### 3. 日志采样策略

```python
# 高流量系统日志采样
sampling_config = {
    'info_logs': 0.1,      # 10%采样
    'warn_logs': 0.5,      # 50%采样
    'error_logs': 1.0,     # 100%保留
    'debug_logs': 0.01     # 1%采样 (仅开发环境)
}
```

---

## Related Skills

- `debugger`: 深度问题诊断
- `system-monitor`: 实时系统监控
- `performance-optimizer`: 性能优化

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | AI异常检测、分布式追踪、根因分析 |
| 1.0.0 | 2025-06-01 | 初始版本 |
