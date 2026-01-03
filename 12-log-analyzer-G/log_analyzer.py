#!/usr/bin/env python3
"""
log_analyzer 模块
"""


"""
Log Analyzer - 智能日志分析工具
支持多种日志格式的解析、异常检测、事件关联和可视化报告
"""
import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional, Tuple
import sys
import hashlib


class LogParser:
    """日志解析器 - 自动识别和解析多种日志格式"""

    # Apache CLF格式: 127.0.0.1 - - [01/Jan/2025:12:00:00 +0000] "GET /api" 200
    CLF_PATTERN = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+)(?: (\d+))?'

    # Syslog格式: Jan 1 12:00:00 host app[123]: message
    SYSLOG_PATTERN = r'(\w+ \d+ \d+:\d+:\d+) (\S+) (\S+)\[(\d+)\]: (.+)'

    # Logfmt格式: level=info timestamp=2025-01-01T12:00:00Z msg="test"
    LOGFMT_PATTERN = r'(\w+)=("?[^"\s]+"?)'

    # Nginx格式
    NGINX_PATTERN = r'(\S+) - (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+) "([^"]*)" "([^"]*)"'

    # Custom application log pattern
    CUSTOM_PATTERN = r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\s+\[?(\w+)\]?\s+(.*)'

    def __init__(self) -> None:
        self.format_detected = None
        self.parse_errors = 0
        self.supported_formats = {
            'json': 'JSON格式',
            'clf': 'Apache CLF格式',
            'syslog': 'Syslog格式',
            'logfmt': 'Logfmt格式',
            'nginx': 'Nginx格式',
            'custom': '自定义应用日志格式',
            'unknown': '未知格式'
        }

    def detect_format(self, line: str) -> str:
        """自动检测日志格式"""
        line = line.strip()
        if not line:
            return 'unknown'

        # JSON格式
        if line.startswith('{'):
            try:
                json.loads(line)
                return 'json'
            except:
                pass

        # Nginx格式
        if re.match(self.NGINX_PATTERN, line):
            return 'nginx'

        # Apache CLF格式
        if re.match(self.CLF_PATTERN, line):
            return 'clf'

        # Syslog格式
        if re.match(self.SYSLOG_PATTERN, line):
            return 'syslog'

        # Logfmt格式
        if '=' in line and len(re.findall(self.LOGFMT_PATTERN, line)) >= 2:
            return 'logfmt'

        # Custom application log
        if re.match(self.CUSTOM_PATTERN, line):
            return 'custom'

        return 'unknown'

    def parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """解析单行日志"""
        line = line.strip()
        if not line:
            return None

        # 自动检测格式（首次）
        if not self.format_detected:
            self.format_detected = self.detect_format(line)

        try:
            if self.format_detected == 'json':
                return self._parse_json(line)
            elif self.format_detected == 'clf':
                return self._parse_clf(line)
            elif self.format_detected == 'syslog':
                return self._parse_syslog(line)
            elif self.format_detected == 'logfmt':
                return self._parse_logfmt(line)
            elif self.format_detected == 'nginx':
                return self._parse_nginx(line)
            elif self.format_detected == 'custom':
                return self._parse_custom(line)
            else:
                return self._parse_plain(line)
        except Exception as e:
            self.parse_errors += 1
            return None

    def _parse_json(self, line: str) -> Dict[str, Any]:
        """解析JSON格式日志"""
        data = json.loads(line)
        return {
            'timestamp': self._extract_timestamp(data),
            'level': data.get('level', data.get('severity', 'INFO')).upper(),
            'message': data.get('message', data.get('msg', '')),
            'trace_id': data.get('trace_id', data.get('traceId', '')),
            'span_id': data.get('span_id', data.get('spanId', '')),
            'raw': data
        }

    def _parse_clf(self, line: str) -> Dict[str, Any]:
        """解析Apache CLF格式日志"""
        match = re.match(self.CLF_PATTERN, line)
        if match:
            groups = match.groups()
            ip, timestamp, method, path, protocol, status = groups[:6]
            size = groups[6] if len(groups) > 6 and groups[6] else '0'

            return {
                'timestamp': self._parse_clf_timestamp(timestamp),
                'level': 'ERROR' if int(status) >= 500 else 'WARN' if int(status) >= 400 else 'INFO',
                'message': f"{method} {path} {status}",
                'trace_id': '',
                'span_id': '',
                'raw': {
                    'ip': ip,
                    'method': method,
                    'path': path,
                    'status': int(status),
                    'size': int(size)
                }
            }
        return None

    def _parse_nginx(self, line: str) -> Dict[str, Any]:
        """解析Nginx格式日志"""
        match = re.match(self.NGINX_PATTERN, line)
        if match:
            ip, user, timestamp, method, path, protocol, status, size, referer, user_agent = match.groups()
            return {
                'timestamp': self._parse_clf_timestamp(timestamp),
                'level': 'ERROR' if int(status) >= 500 else 'WARN' if int(status) >= 400 else 'INFO',
                'message': f"{method} {path} {status}",
                'trace_id': '',
                'span_id': '',
                'raw': {
                    'ip': ip,
                    'method': method,
                    'path': path,
                    'status': int(status),
                    'size': int(size),
                    'referer': referer,
                    'user_agent': user_agent
                }
            }
        return None

    def _parse_syslog(self, line: str) -> Dict[str, Any]:
        """解析Syslog格式日志"""
        match = re.match(self.SYSLOG_PATTERN, line)
        if match:
            timestamp, host, app, pid, message = match.groups()
            return {
                'timestamp': self._parse_syslog_timestamp(timestamp),
                'level': self._detect_level(message),
                'message': message,
                'trace_id': '',
                'span_id': '',
                'raw': {'host': host, 'app': app, 'pid': pid}
            }
        return None

    def _parse_logfmt(self, line: str) -> Dict[str, Any]:
        """解析Logfmt格式日志"""
        pairs = re.findall(self.LOGFMT_PATTERN, line)
        data = {k: v.strip('"') for k, v in pairs}
        return {
            'timestamp': self._parse_iso_timestamp(data.get('timestamp', data.get('time', ''))),
            'level': data.get('level', 'INFO').upper(),
            'message': data.get('msg', data.get('message', '')),
            'trace_id': data.get('trace_id', ''),
            'span_id': data.get('span_id', ''),
            'raw': data
        }

    def _parse_custom(self, line: str) -> Dict[str, Any]:
        """解析自定义应用日志格式"""
        match = re.match(self.CUSTOM_PATTERN, line)
        if match:
            timestamp, level, message = match.groups()
            return {
                'timestamp': self._parse_iso_timestamp(timestamp),
                'level': level.upper(),
                'message': message,
                'trace_id': '',
                'span_id': '',
                'raw': {}
            }
        return None

    def _parse_plain(self, line: str) -> Dict[str, Any]:
        """解析纯文本日志"""
        return {
            'timestamp': datetime.now(),
            'level': self._detect_level(line),
            'message': line,
            'trace_id': '',
            'span_id': '',
            'raw': {}
        }

    def _extract_timestamp(self, data: dict) -> datetime:
        """从字典中提取时间戳"""
        for key in ['timestamp', 'time', '@timestamp', 'datetime']:
            if key in data:
                return self._parse_iso_timestamp(str(data[key]))
        return datetime.now()

    def _parse_iso_timestamp(self, ts: str) -> datetime:
        """解析ISO格式时间戳"""
        try:
            # 处理各种ISO格式
            ts = ts.replace('Z', '+00:00')
            return datetime.fromisoformat(ts)
        except:
            try:
                # 尝试常见格式
                return datetime.strptime(ts.split('.')[0], '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.now()

    def _parse_clf_timestamp(self, ts: str) -> datetime:
        """解析CLF格式时间戳: 01/Jan/2025:12:00:00 +0000"""
        try:
            return datetime.strptime(ts.split()[0], '%d/%b/%Y:%H:%M:%S')
        except:
            return datetime.now()

    def _parse_syslog_timestamp(self, ts: str) -> datetime:
        """解析Syslog格式时间戳: Jan 1 12:00:00"""
        try:
            current_year = datetime.now().year
            return datetime.strptime(f"{current_year} {ts}", '%Y %b %d %H:%M:%S')
        except:
            return datetime.now()

    def _detect_level(self, message: str) -> str:
        """从消息中检测日志级别"""
        message_lower = message.lower()
        if any(word in message_lower for word in ['error', 'exception', 'fatal', 'critical']):
            return 'ERROR'
        elif any(word in message_lower for word in ['warn', 'warning']):
            return 'WARN'
        elif any(word in message_lower for word in ['debug', 'trace']):
            return 'DEBUG'
        return 'INFO'

    def get_format_name(self) -> str:
        """获取检测到的格式名称"""
        return self.supported_formats.get(self.format_detected, '未知格式')


class AnomalyDetector:
    """异常检测器 - 使用AI和统计方法检测异常"""

    def __init__(self) -> None:
        self.baseline_error_rate = 0
        self.known_errors = set()
        self.anomalies = []
        self.error_patterns = defaultdict(int)

    def detect_error_spike(self, time_series: Dict[datetime, int]) -> List[Dict]:
        """检测错误突增"""
        if not time_series:
            return []

        values = list(time_series.values())
        self.baseline_error_rate = sum(values) / len(values) if values else 0
        std_dev = self._calculate_std_dev(values)

        spikes = []
        for timestamp, count in time_series.items():
            # 使用3-sigma规则检测异常
            threshold = self.baseline_error_rate + (3 * std_dev)
            if count > max(threshold, self.baseline_error_rate * 2):
                spikes.append({
                    'type': 'error_spike',
                    'severity': 'critical',
                    'timestamp': timestamp,
                    'count': count,
                    'baseline': self.baseline_error_rate,
                    'threshold': threshold,
                    'multiplier': count / self.baseline_error_rate if self.baseline_error_rate > 0 else 0
                })

        return spikes

    def detect_new_errors(self, errors: List[str]) -> List[Dict]:
        """检测新出现的错误类型"""
        new_errors = []
        for error in errors:
            # 提取错误模式（去除变化的部分如ID、时间戳等）
            pattern = self._extract_error_pattern(error)

            if pattern not in self.known_errors:
                new_errors.append({
                    'type': 'new_error',
                    'severity': 'high',
                    'error': error,
                    'pattern': pattern
                })
                self.known_errors.add(pattern)

            self.error_patterns[pattern] += 1

        return new_errors

    def detect_security_threats(self, logs: List[Dict]) -> List[Dict]:
        """检测安全威胁"""
        threats = []

        # 检测暴力破解（短时间大量登录失败）
        login_failures = defaultdict(list)
        sql_injection_attempts = []
        suspicious_paths = []

        for log in logs:
            message = log['message'].lower()

            # 登录失败检测
            if 'login' in message and any(word in message for word in ['fail', 'denied', 'invalid']):
                ip = log['raw'].get('ip', 'unknown')
                login_failures[ip].append(log['timestamp'])

            # SQL注入检测
            if any(pattern in message for pattern in ['union select', 'drop table', '1=1', 'or 1=1']):
                sql_injection_attempts.append({
                    'timestamp': log['timestamp'],
                    'message': log['message'],
                    'ip': log['raw'].get('ip', 'unknown')
                })

            # 可疑路径访问
            path = log['raw'].get('path', '')
            if any(suspicious in path.lower() for suspicious in ['../', 'etc/passwd', 'admin', 'phpinfo']):
                suspicious_paths.append({
                    'timestamp': log['timestamp'],
                    'path': path,
                    'ip': log['raw'].get('ip', 'unknown')
                })

        # 暴力破解威胁
        for ip, timestamps in login_failures.items():
            if len(timestamps) > 10:
                time_window = (max(timestamps) - min(timestamps)).total_seconds() / 60
                threats.append({
                    'type': 'brute_force',
                    'severity': 'critical' if len(timestamps) > 50 else 'high',
                    'ip': ip,
                    'attempts': len(timestamps),
                    'time_window_minutes': time_window,
                    'message': f'可能的暴力破解攻击：IP {ip} 在 {time_window:.1f} 分钟内有 {len(timestamps)} 次登录失败'
                })

        # SQL注入威胁
        if sql_injection_attempts:
            threats.append({
                'type': 'sql_injection',
                'severity': 'critical',
                'attempts': len(sql_injection_attempts),
                'details': sql_injection_attempts[:5],
                'message': f'检测到 {len(sql_injection_attempts)} 次疑似SQL注入攻击'
            })

        # 可疑路径访问
        if suspicious_paths:
            threats.append({
                'type': 'path_traversal',
                'severity': 'high',
                'attempts': len(suspicious_paths),
                'details': suspicious_paths[:5],
                'message': f'检测到 {len(suspicious_paths)} 次可疑路径访问'
            })

        return threats

    def detect_performance_anomalies(self, logs: List[Dict]) -> List[Dict]:
        """检测性能异常"""
        anomalies = []
        response_times = []

        for log in logs:
            # 从日志中提取响应时间
            raw = log.get('raw', {})
            if 'response_time' in raw:
                response_times.append(float(raw['response_time']))
            elif 'duration' in raw:
                response_times.append(float(raw['duration']))

        if response_times:
            avg_time = sum(response_times) / len(response_times)
            std_dev = self._calculate_std_dev(response_times)

            slow_requests = [t for t in response_times if t > avg_time + (3 * std_dev)]

            if slow_requests:
                anomalies.append({
                    'type': 'slow_response',
                    'severity': 'medium',
                    'count': len(slow_requests),
                    'average_time': avg_time,
                    'threshold': avg_time + (3 * std_dev),
                    'message': f'检测到 {len(slow_requests)} 个慢响应请求'
                })

        return anomalies

    def _extract_error_pattern(self, error: str) -> str:
        """提取错误模式（去除变化的部分）"""
        # 移除数字、UUID、时间戳等
        pattern = re.sub(r'\d+', 'N', error)
        pattern = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'UUID', pattern)
        pattern = re.sub(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}', 'TIMESTAMP', pattern)
        return pattern

    def _calculate_std_dev(self, values: List[float]) -> float:
        """计算标准差"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5


class EventCorrelator:
    """事件关联器 - 关联分布式追踪事件"""

    def __init__(self) -> None:
        self.traces = defaultdict(list)
        self.event_chains = []

    def correlate_events(self, logs: List[Dict]) -> Dict[str, Any]:
        """关联事件，重建调用链"""
        # 按trace_id分组
        for log in logs:
            trace_id = log.get('trace_id', '')
            if trace_id:
                self.traces[trace_id].append(log)

        # 构建事件链
        chains = []
        for trace_id, events in self.traces.items():
            if len(events) > 1:
                # 按时间排序
                events.sort(key=lambda x: x['timestamp'])

                chain = {
                    'trace_id': trace_id,
                    'event_count': len(events),
                    'start_time': events[0]['timestamp'],
                    'end_time': events[-1]['timestamp'],
                    'duration': (events[-1]['timestamp'] - events[0]['timestamp']).total_seconds(),
                    'events': events,
                    'has_error': any(e['level'] in ['ERROR', 'CRITICAL'] for e in events)
                }
                chains.append(chain)

        # 找出最长和有错误的调用链
        chains.sort(key=lambda x: x['duration'], reverse=True)
        error_chains = [c for c in chains if c['has_error']]

        return {
            'total_traces': len(self.traces),
            'correlated_chains': len(chains),
            'longest_chains': chains[:5],
            'error_chains': error_chains[:5],
            'avg_chain_length': sum(c['event_count'] for c in chains) / len(chains) if chains else 0
        }

    def build_timeline(self, logs: List[Dict], time_window: int = 60) -> List[Dict]:
        """重建时间线（按时间窗口分组事件）"""
        if not logs:
            return []

        # 按时间排序
        sorted_logs = sorted(logs, key=lambda x: x['timestamp'])

        timeline = []
        current_window = None
        current_events = []

        for log in sorted_logs:
            if not current_window:
                current_window = log['timestamp']
                current_events = [log]
            else:
                # 检查是否在同一时间窗口
                if (log['timestamp'] - current_window).total_seconds() <= time_window:
                    current_events.append(log)
                else:
                    # 保存当前窗口
                    timeline.append({
                        'window_start': current_window,
                        'event_count': len(current_events),
                        'error_count': sum(1 for e in current_events if e['level'] in ['ERROR', 'CRITICAL']),
                        'events': current_events
                    })
                    # 开始新窗口
                    current_window = log['timestamp']
                    current_events = [log]

        # 保存最后一个窗口
        if current_events:
            timeline.append({
                'window_start': current_window,
                'event_count': len(current_events),
                'error_count': sum(1 for e in current_events if e['level'] in ['ERROR', 'CRITICAL']),
                'events': current_events
            })

        return timeline


class LogAnalyzer:
    """日志分析器 - 主分析引擎"""

    def __init__(self) -> None:
        self.parser = LogParser()
        self.detector = AnomalyDetector()
        self.correlator = EventCorrelator()
        self.logs = []
        self.stats = {
            'total_lines': 0,
            'parsed_lines': 0,
            'parse_errors': 0,
            'time_range': {'start': None, 'end': None}
        }

    def analyze_file(self, file_path: str, enable_correlation: bool = True) -> Dict[str, Any]:
        """分析日志文件

        Args:
            file_path: 日志文件路径
            enable_correlation: 是否启用事件关联（分布式追踪）
        """
        path = Path(file_path)

        if not path.exists():
            return {'error': f'文件不存在: {file_path}'}

        # 读取并解析日志
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                self.stats['total_lines'] += 1
                parsed = self.parser.parse_line(line)
                if parsed:
                    self.logs.append(parsed)
                    self.stats['parsed_lines'] += 1

                    # 更新时间范围
                    ts = parsed['timestamp']
                    if not self.stats['time_range']['start'] or ts < self.stats['time_range']['start']:
                        self.stats['time_range']['start'] = ts
                    if not self.stats['time_range']['end'] or ts > self.stats['time_range']['end']:
                        self.stats['time_range']['end'] = ts

        self.stats['parse_errors'] = self.parser.parse_errors

        # 执行分析
        return self._generate_report(enable_correlation)

    def _generate_report(self, enable_correlation: bool) -> Dict[str, Any]:
        """生成分析报告"""
        # 统计错误
        error_logs = [log for log in self.logs if log['level'] in ['ERROR', 'CRITICAL', 'FATAL']]

        # 按时间分组统计错误（5分钟窗口）
        error_time_series = defaultdict(int)
        for log in error_logs:
            time_bucket = log['timestamp'].replace(minute=log['timestamp'].minute // 5 * 5, second=0, microsecond=0)
            error_time_series[time_bucket] += 1

        # 提取错误消息
        error_messages = [log['message'] for log in error_logs]

        # 异常检测
        error_spikes = self.detector.detect_error_spike(error_time_series)
        new_errors = self.detector.detect_new_errors(error_messages)
        security_threats = self.detector.detect_security_threats(self.logs)
        performance_anomalies = self.detector.detect_performance_anomalies(self.logs)

        # 统计最常见的错误
        error_counter = Counter(error_messages)
        top_errors = error_counter.most_common(10)

        # 日志级别分布
        level_distribution = Counter(log['level'] for log in self.logs)

        # 事件关联（如果启用）
        correlation_result = None
        timeline = None
        if enable_correlation:
            correlation_result = self.correlator.correlate_events(self.logs)
            # timeline = self.correlator.build_timeline(error_logs, time_window=300)  # 5分钟窗口

        # 错误模式分析
        error_patterns = self._analyze_error_patterns()

        return {
            'summary': {
                'file_format': self.parser.get_format_name(),
                'total_lines': self.stats['total_lines'],
                'parsed_lines': self.stats['parsed_lines'],
                'parse_success_rate': f"{(self.stats['parsed_lines'] / self.stats['total_lines'] * 100):.1f}%" if self.stats['total_lines'] > 0 else '0%',
                'time_range': {
                    'start': self.stats['time_range']['start'].isoformat() if self.stats['time_range']['start'] else None,
                    'end': self.stats['time_range']['end'].isoformat() if self.stats['time_range']['end'] else None,
                    'duration_hours': (self.stats['time_range']['end'] - self.stats['time_range']['start']).total_seconds() / 3600 if self.stats['time_range']['start'] and self.stats['time_range']['end'] else 0
                },
                'error_count': len(error_logs),
                'error_rate': f"{(len(error_logs) / self.stats['parsed_lines'] * 100):.2f}%" if self.stats['parsed_lines'] > 0 else '0%'
            },
            'level_distribution': dict(level_distribution),
            'anomalies': {
                'error_spikes': error_spikes,
                'new_errors': new_errors,
                'security_threats': security_threats,
                'performance_anomalies': performance_anomalies
            },
            'top_errors': [{'message': msg, 'count': count} for msg, count in top_errors],
            'error_patterns': error_patterns,
            'correlation': correlation_result,
            'timeline': timeline,
            'recommendations': self._generate_recommendations(error_spikes, new_errors, security_threats, performance_anomalies)
        }

    def _analyze_error_patterns(self) -> Dict[str, Any]:
        """分析错误模式"""
        patterns = defaultdict(int)
        for pattern, count in self.detector.error_patterns.items():
            patterns[pattern] = count

        # 排序找出最常见的错误模式
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)

        return {
            'total_patterns': len(patterns),
            'top_patterns': [{'pattern': p, 'count': c} for p, c in sorted_patterns[:10]]
        }

    def _generate_recommendations(self, spikes, new_errors, threats, perf_anomalies) -> List[str]:
        """生成修复建议"""
        recommendations = []

        if spikes:
            recommendations.append(f"🔴 检测到 {len(spikes)} 个错误突增时段，建议检查对应时间的系统负载和数据库连接")

        if new_errors:
            recommendations.append(f"🟠 发现 {len(new_errors)} 个新错误类型，建议立即调查根本原因")

        if threats:
            for threat in threats:
                if threat['type'] == 'brute_force':
                    recommendations.append(f"🔒 检测到暴力破解攻击，建议立即封禁IP并启用速率限制")
                elif threat['type'] == 'sql_injection':
                    recommendations.append(f"🚨 检测到SQL注入攻击，建议立即检查输入验证和参数化查询")
                elif threat['type'] == 'path_traversal':
                    recommendations.append(f"⚠️ 检测到路径遍历攻击，建议加强路径验证和访问控制")

        if perf_anomalies:
            recommendations.append(f"📊 检测到 {len(perf_anomalies)} 个性能异常，建议优化慢查询和增加缓存")

        if not recommendations:
            recommendations.append("✅ 未检测到明显异常，日志运行正常")

        return recommendations


def print_report(report: Dict[str, Any], verbose: bool = False) -> Any:
    """打印分析报告"""
    print("=" * 80)
    print("日志分析报告")
    print("=" * 80)
    print()

    # 概要信息
    summary = report['summary']
    print(f"📊 概要信息:")
    print(f"   日志格式: {summary['file_format']}")
    print(f"   总行数: {summary['total_lines']:,}")
    print(f"   解析成功: {summary['parsed_lines']:,} ({summary['parse_success_rate']})")
    print(f"   时间范围: {summary['time_range']['start']} 至 {summary['time_range']['end']}")
    print(f"   时间跨度: {summary['time_range']['duration_hours']:.2f} 小时")
    print(f"   错误数量: {summary['error_count']:,} ({summary['error_rate']})")
    print()

    # 日志级别分布
    print(f"📈 日志级别分布:")
    for level, count in sorted(report['level_distribution'].items()):
        print(f"   {level}: {count:,}")
    print()

    # 异常检测
    anomalies = report['anomalies']

    if anomalies['error_spikes']:
        print(f"🔴 错误突增 ({len(anomalies['error_spikes'])} 个):")
        for spike in anomalies['error_spikes'][:5]:
            print(f"   时间: {spike['timestamp']}")
            print(f"   错误数: {spike['count']} (基线: {spike['baseline']:.1f}, 阈值: {spike['threshold']:.1f})")
        print()

    if anomalies['new_errors']:
        print(f"🟠 新错误类型 ({len(anomalies['new_errors'])} 个):")
        for error in anomalies['new_errors'][:5]:
            print(f"   {error['error'][:100]}")
        print()

    if anomalies['security_threats']:
        print(f"🔒 安全威胁 ({len(anomalies['security_threats'])} 个):")
        for threat in anomalies['security_threats']:
            print(f"   [{threat['severity'].upper()}] {threat['message']}")
        print()

    if anomalies['performance_anomalies']:
        print(f"📊 性能异常 ({len(anomalies['performance_anomalies'])} 个):")
        for anomaly in anomalies['performance_anomalies']:
            print(f"   {anomaly['message']}")
        print()

    # 错误模式
    if report['error_patterns']['top_patterns']:
        print(f"🔍 Top 错误模式:")
        for i, pattern in enumerate(report['error_patterns']['top_patterns'][:5], 1):
            print(f"   {i}. [{pattern['count']:,}次] {pattern['pattern'][:80]}")
        print()

    # Top错误
    if report['top_errors']:
        print(f"📋 Top 10 错误:")
        for i, error in enumerate(report['top_errors'], 1):
            print(f"   {i}. [{error['count']:,}次] {error['message'][:80]}")
        print()

    # 事件关联
    if report.get('correlation'):
        corr = report['correlation']
        print(f"🔗 事件关联分析:")
        print(f"   总追踪数: {corr['total_traces']}")
        print(f"   关联链数: {corr['correlated_chains']}")
        print(f"   平均链长: {corr['avg_chain_length']:.1f}")
        if corr['error_chains']:
            print(f"   错误链数: {len(corr['error_chains'])}")
        print()

    # 时间线
    if report.get('timeline') and verbose:
        print(f"📅 错误时间线:")
        for window in report['timeline'][:10]:
            print(f"   {window['window_start']}: {window['error_count']} 个错误")
        print()

    # 建议
    print(f"💡 修复建议:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    print()


def main() -> Any:
    try:
        """CLI入口"""
        import argparse
    except Exception as e:
        logger.error(f"执行出错: {e}")
        return 1

    parser = argparse.ArgumentParser(description='智能日志分析工具')
    parser.add_argument('file', help='日志文件路径')
    parser.add_argument('--json', action='store_true', help='输出JSON格式报告')
    parser.add_argument('--output', '-o', help='保存报告到文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出模式')
    parser.add_argument('--no-correlation', action='store_true', help='禁用事件关联分析')

    args = parser.parse_args()

    print(f"正在分析日志文件: {args.file}")
    print()

    analyzer = LogAnalyzer()
    report = analyzer.analyze_file(args.file, enable_correlation=not args.no_correlation)

    if 'error' in report:
        print(f"错误: {report['error']}")
        sys.exit(1)

    if args.json:
        output = json.dumps(report, indent=2, ensure_ascii=False, default=str)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"JSON报告已保存至: {args.output}")
        else:
            print(output)
    else:
        print_report(report, verbose=args.verbose)

        if args.output:
            output_file = Path(args.output)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            print(f"JSON报告已保存至: {output_file}")


if __name__ == '__main__':
    main()
