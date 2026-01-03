#!/usr/bin/env python3
"""
system_monitor 模块
"""


"""
System Monitor - 系统监控工具
监控系统资源、应用性能、依赖服务健康状态
支持 Liveness/Readiness 探针、性能指标（P50/P95/P99）、AI 趋势预测
"""
import psutil
import time
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import deque
import platform
import statistics


import logging

class PercentileCalculator:
    """百分位数计算器"""

    @staticmethod
    def calculate(values: List[float]) -> Dict[str, float]:
        if True:
            """计算 P50/P90/P95/P99 百分位数"""
        if not values:
            return {'p50': 0, 'p90': 0, 'p95': 0, 'p99': 0, 'avg': 0, 'max': 0, 'min': 0}

        sorted_values = sorted(values)
        length = len(sorted_values)

        def percentile(p: float) -> float:
            if True:
                index = int(length * p)
            if index >= length:
                return sorted_values[-1]
            return sorted_values[index]

        return {
            'p50': percentile(0.50),
            'p90': percentile(0.90),
            'p95': percentile(0.95),
            'p99': percentile(0.99),
            'avg': sum(values) / length,
            'max': max(values),
            'min': min(values)
        }


class ResourceMonitor:
    """系统资源监控"""

    def __init__(self, history_size: int = 60) -> None:
        if True:
            self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.disk_io_history = deque(maxlen=history_size)
        self.network_io_history = deque(maxlen=history_size)

    def get_cpu_metrics(self) -> Dict[str, Any]:
        if True:
            """获取CPU指标"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        cpu_percpu = psutil.cpu_percent(interval=0, percpu=True)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)

        self.cpu_history.append(cpu_percent)

        # 计算CPU百分位数
        percentiles = PercentileCalculator.calculate(list(self.cpu_history))

        return {
            'usage_percent': cpu_percent,
            'per_cpu': cpu_percpu,
            'count': cpu_count,
            'frequency': {
                'current': cpu_freq.current if cpu_freq else 0,
                'min': cpu_freq.min if cpu_freq else 0,
                'max': cpu_freq.max if cpu_freq else 0
            },
            'load_average': {
                '1min': load_avg[0],
                '5min': load_avg[1],
                '15min': load_avg[2]
            },
            'percentiles': percentiles,
            'status': self._get_status(cpu_percent, 70, 90),
            'trend': self._calculate_trend(list(self.cpu_history))
        }

    def get_memory_metrics(self) -> Dict[str, Any]:
        if True:
            """获取内存指标"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.memory_history.append(memory.percent)

        # 计算内存百分位数
        percentiles = PercentileCalculator.calculate(list(self.memory_history))

        return {
            'total': self._format_bytes(memory.total),
            'total_bytes': memory.total,
            'used': self._format_bytes(memory.used),
            'used_bytes': memory.used,
            'available': self._format_bytes(memory.available),
            'available_bytes': memory.available,
            'percent': memory.percent,
            'swap': {
                'total': self._format_bytes(swap.total),
                'used': self._format_bytes(swap.used),
                'free': self._format_bytes(swap.free),
                'percent': swap.percent
            },
            'percentiles': percentiles,
            'status': self._get_status(memory.percent, 80, 90),
            'trend': self._calculate_trend(list(self.memory_history))
        }

    def get_disk_metrics(self) -> List[Dict[str, Any]]:
        """获取磁盘指标"""
        partitions = psutil.disk_partitions()
        disk_metrics = []

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                io_counters = psutil.disk_io_counters(perdisk=False)

                disk_metrics.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': self._format_bytes(usage.total),
                    'total_bytes': usage.total,
                    'used': self._format_bytes(usage.used),
                    'used_bytes': usage.used,
                    'free': self._format_bytes(usage.free),
                    'free_bytes': usage.free,
                    'percent': usage.percent,
                    'io': {
                        'read_count': io_counters.read_count if io_counters else 0,
                        'write_count': io_counters.write_count if io_counters else 0,
                        'read_bytes': self._format_bytes(io_counters.read_bytes) if io_counters else '0B',
                        'write_bytes': self._format_bytes(io_counters.write_bytes) if io_counters else '0B'
                    },
                    'status': self._get_status(usage.percent, 80, 90)
                })
            except PermissionError:
                continue

        return disk_metrics

    def get_network_metrics(self) -> Dict[str, Any]:
        if True:
            """获取网络指标"""
        net_io = psutil.net_io_counters()
        connections = len(psutil.net_connections())

        # 获取每个网卡的统计
        net_io_per_nic = psutil.net_io_counters(pernic=True)

        return {
            'bytes_sent': self._format_bytes(net_io.bytes_sent),
            'bytes_sent_raw': net_io.bytes_sent,
            'bytes_recv': self._format_bytes(net_io.bytes_recv),
            'bytes_recv_raw': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout,
            'drop_in': net_io.dropin,
            'drop_out': net_io.dropout,
            'connections': connections,
            'per_nic': {nic: {
                'bytes_sent': self._format_bytes(stats.bytes_sent),
                'bytes_recv': self._format_bytes(stats.bytes_recv),
            } for nic, stats in net_io_per_nic.items()},
            'status': '✅ 正常' if net_io.errin + net_io.errout < 100 else '⚠️ 警告'
        }

    def _format_bytes(self, bytes_value: int) -> str:
        if True:
            """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f}PB"

    def _get_status(self, value: float, warning_threshold: float, critical_threshold: float) -> str:
        if True:
            """获取状态标识"""
        if value < warning_threshold:
            return '✅ 正常'
        elif value < critical_threshold:
            return '⚠️ 警告'
        else:
            return '🔴 严重'

    def _calculate_trend(self, history: List[float]) -> str:
        if True:
            """计算趋势"""
        if len(history) < 2:
            return '→ 稳定'

        # 简单的线性趋势
        recent = sum(history[-10:]) / min(10, len(history))
        older = sum(history[:10]) / min(10, len(history))

        if recent > older * 1.1:
            return '↗ 上升'
        elif recent < older * 0.9:
            return '↘ 下降'
        else:
            return '→ 稳定'


class ProcessMonitor:
    """进程监控"""

    def get_top_processes(self, limit: int = 5, sort_by: str = 'cpu') -> List[Dict[str, Any]]:
        """获取资源使用最高的进程

        Args:
            limit: 返回进程数量
            sort_by: 排序依据 ('cpu' or 'memory')
        """
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'] or 0,
                    'memory_percent': proc.info['memory_percent'] or 0,
                    'status': proc.info['status'],
                    'uptime': self._format_uptime(proc.info['create_time'])
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # 按指定字段排序
        sort_key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
        processes.sort(key=lambda x: x[sort_key], reverse=True)
        return processes[:limit]

    def _format_uptime(self, create_time: float) -> str:
        if True:
            """格式化运行时间"""
        uptime_seconds = time.time() - create_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


class HealthProbe:
    """健康探针 - Kubernetes 风格的 Liveness/Readiness 检查"""

    def __init__(self) -> None:
        if True:
            self.checks = {
            'cpu': {'threshold': 95, 'critical': True},
            'memory': {'threshold': 95, 'critical': True},
            'disk': {'threshold': 90, 'critical': True},
            'network': {'threshold': None, 'critical': False}
        }

    def liveness_probe(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if True:
            """存活探针 - 检查系统是否存活（critical问题会导致失败）"""
        issues = []
        is_alive = True

        # 检查CPU
        if metrics['cpu']['usage_percent'] > self.checks['cpu']['threshold']:
            issues.append(f"CPU使用率过高: {metrics['cpu']['usage_percent']}%")
            if self.checks['cpu']['critical']:
                is_alive = False

        # 检查内存
        if metrics['memory']['percent'] > self.checks['memory']['threshold']:
            issues.append(f"内存使用率过高: {metrics['memory']['percent']}%")
            if self.checks['memory']['critical']:
                is_alive = False

        # 检查磁盘
        for disk in metrics['disk']:
            if disk['percent'] > self.checks['disk']['threshold']:
                issues.append(f"磁盘空间不足 ({disk['mountpoint']}): {disk['percent']}%")
                if self.checks['disk']['critical']:
                    is_alive = False

        return {
            'alive': is_alive,
            'status': 'healthy' if is_alive else 'unhealthy',
            'issues': issues,
            'timestamp': datetime.now().isoformat()
        }

    def readiness_probe(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if True:
            """就绪探针 - 检查系统是否准备好接收流量（包含非critical问题）"""
        issues = []
        warnings = []
        is_ready = True

        # 检查CPU（更宽松的阈值）
        if metrics['cpu']['usage_percent'] > 90:
            issues.append(f"CPU负载过高: {metrics['cpu']['usage_percent']}%")
            is_ready = False
        elif metrics['cpu']['usage_percent'] > 70:
            warnings.append(f"CPU负载偏高: {metrics['cpu']['usage_percent']}%")

        # 检查内存
        if metrics['memory']['percent'] > 90:
            issues.append(f"内存不足: {metrics['memory']['percent']}%")
            is_ready = False
        elif metrics['memory']['percent'] > 80:
            warnings.append(f"内存偏高: {metrics['memory']['percent']}%")

        # 检查磁盘
        for disk in metrics['disk']:
            if disk['percent'] > 85:
                issues.append(f"磁盘空间不足 ({disk['mountpoint']}): {disk['percent']}%")
                is_ready = False
            elif disk['percent'] > 75:
                warnings.append(f"磁盘空间偏低 ({disk['mountpoint']}): {disk['percent']}%")

        # 检查网络错误
        if metrics['network']['errors_in'] + metrics['network']['errors_out'] > 1000:
            warnings.append(f"网络错误数偏高: {metrics['network']['errors_in'] + metrics['network']['errors_out']}")

        return {
            'ready': is_ready,
            'status': 'ready' if is_ready else 'not_ready',
            'issues': issues,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat()
        }


class TrendPredictor:
    """趋势预测器 - 使用简单的线性回归预测资源使用"""

    def __init__(self) -> None:
        if True:
            self.predictions = {}

    def predict_resource_usage(self, current_percent: float, trend: str, history: List[float]) -> Dict[str, Any]:
        if True:
            """预测资源使用趋势

        Args:
            current_percent: 当前使用率
            trend: 趋势（上升/下降/稳定）
            history: 历史数据

        Returns:
            预测结果和建议
        """
        predictions = {}
        recommendations = []

        # 计算增长率
        if len(history) >= 2:
            growth_rate = self._calculate_growth_rate(history)
        else:
            growth_rate = 0

        # 预测未来使用率
        predictions['1h'] = min(100, max(0, current_percent + growth_rate * 1))
        predictions['6h'] = min(100, max(0, current_percent + growth_rate * 6))
        predictions['24h'] = min(100, max(0, current_percent + growth_rate * 24))
        predictions['7d'] = min(100, max(0, current_percent + growth_rate * 24 * 7))

        # 生成建议
        if predictions['24h'] > 95:
            recommendations.append("🚨 紧急：预计24小时内资源耗尽")
            recommendations.append("建议立即扩容或优化")
        elif predictions['7d'] > 90:
            recommendations.append("🔴 警告：预计7天内资源将达到临界")
            recommendations.append("建议3天内进行扩容规划")
        elif predictions['7d'] > 80:
            recommendations.append("⚠️ 注意：资源使用呈上升趋势")
            recommendations.append("建议关注资源使用情况")

        # 容量规划建议
        if current_percent > 80:
            required_capacity = self._calculate_required_capacity(current_percent, predictions['7d'])
            recommendations.append(f"💡 建议扩容 {required_capacity}% 以保证未来7天稳定运行")

        return {
            'current': current_percent,
            'growth_rate': growth_rate,
            'predictions': predictions,
            'recommendations': recommendations,
            'trend': trend
        }

    def _calculate_growth_rate(self, history: List[float]) -> float:
        if True:
            """计算增长率（每小时）"""
        if len(history) < 2:
            return 0

        # 使用最近的数据点计算趋势
        recent_points = list(history)[-20:]
        if len(recent_points) < 2:
            return 0

        # 简单线性回归
        n = len(recent_points)
        x = list(range(n))
        y = recent_points

        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0

        slope = numerator / denominator
        return slope

    def _calculate_required_capacity(self, current: float, future: float) -> int:
        if True:
            """计算所需扩容百分比"""
        if future <= current:
            return 0
        # 保留20%缓冲
        required = ((future - current) * 1.2)
        return max(20, int(required))


class SystemMonitor:
    """系统监控主类"""

    def __init__(self) -> None:
        if True:
            self.resource_monitor = ResourceMonitor()
        self.process_monitor = ProcessMonitor()
        self.health_probe = HealthProbe()
        self.trend_predictor = TrendPredictor()

    def run_health_check(self) -> Dict[str, Any]:
        if True:
            """运行完整的健康检查"""
        # 收集指标
        cpu = self.resource_monitor.get_cpu_metrics()
        memory = self.resource_monitor.get_memory_metrics()
        disk = self.resource_monitor.get_disk_metrics()
        network = self.resource_monitor.get_network_metrics()
        top_processes_cpu = self.process_monitor.get_top_processes(limit=5, sort_by='cpu')
        top_processes_mem = self.process_monitor.get_top_processes(limit=5, sort_by='memory')

        # 组装所有指标
        all_metrics = {
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'network': network
        }

        # 健康探针
        liveness = self.health_probe.liveness_probe(all_metrics)
        readiness = self.health_probe.readiness_probe(all_metrics)

        # 趋势预测
        memory_prediction = self.trend_predictor.predict_resource_usage(
            memory['percent'],
            memory['trend'],
            list(self.resource_monitor.memory_history)
        )

        cpu_prediction = self.trend_predictor.predict_resource_usage(
            cpu['usage_percent'],
            cpu['trend'],
            list(self.resource_monitor.cpu_history)
        )

        # 整体健康状态
        overall_health = self._calculate_overall_health(liveness, readiness)

        return {
            'health_status': overall_health,
            'probes': {
                'liveness': liveness,
                'readiness': readiness
            },
            'system_resources': {
                'cpu': cpu,
                'memory': memory,
                'disk': disk,
                'network': network
            },
            'top_processes': {
                'by_cpu': top_processes_cpu,
                'by_memory': top_processes_mem
            },
            'predictions': {
                'memory': memory_prediction,
                'cpu': cpu_prediction
            },
            'system_info': {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            },
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_overall_health(self, liveness: Dict, readiness: Dict) -> Dict[str, Any]:
        if True:
            """计算整体健康状态"""
        issues = []
        warnings = []

        if not liveness['alive']:
            status = '🔴 严重'
            issues.extend(liveness['issues'])
        elif not readiness['ready']:
            status = '⚠️ 警告'
            issues.extend(readiness['issues'])
            warnings.extend(readiness.get('warnings', []))
        else:
            status = '✅ 健康'
            warnings.extend(readiness.get('warnings', []))

        return {
            'status': status,
            'liveness': liveness['alive'],
            'readiness': readiness['ready'],
            'critical_issues': issues,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat()
        }


def print_report(report: Dict[str, Any], show_percentiles: bool = False) -> Any:
    if True:
        """打印监控报告"""
    print("=" * 80)
    print("系统监控报告")
    print("=" * 80)
    print(f"生成时间: {report['timestamp']}")
    print()

    # 整体健康状态
    health = report['health_status']
    print(f"整体健康状态: {health['status']}")
    print(f"  Liveness:  {'✅ 存活' if health['liveness'] else '❌ 不存活'}")
    print(f"  Readiness: {'✅ 就绪' if health['readiness'] else '❌ 未就绪'}")
    print()

    if health['critical_issues']:
        print("🔴 严重问题:")
        for issue in health['critical_issues']:
            print(f"   {issue}")
        print()

    if health['warnings']:
        print("⚠️ 警告:")
        for warning in health['warnings']:
            print(f"   {warning}")
        print()

    # 系统资源
    resources = report['system_resources']

    print("📊 系统资源:")
    print()

    # CPU
    cpu = resources['cpu']
    print(f"  CPU:")
    print(f"    使用率: {cpu['usage_percent']:.1f}% {cpu['status']} {cpu['trend']}")
    print(f"    核心数: {cpu['count']}")
    print(f"    负载: {cpu['load_average']['1min']:.2f} / {cpu['load_average']['5min']:.2f} / {cpu['load_average']['15min']:.2f}")
    if show_percentiles:
        p = cpu['percentiles']
        print(f"    百分位: P50={p['p50']:.1f}% P95={p['p95']:.1f}% P99={p['p99']:.1f}%")
    print()

    # 内存
    memory = resources['memory']
    print(f"  内存:")
    print(f"    使用率: {memory['percent']:.1f}% {memory['status']} {memory['trend']}")
    print(f"    已用: {memory['used']} / {memory['total']}")
    print(f"    可用: {memory['available']}")
    print(f"    Swap: {memory['swap']['percent']:.1f}% ({memory['swap']['used']} / {memory['swap']['total']})")
    if show_percentiles:
        p = memory['percentiles']
        print(f"    百分位: P50={p['p50']:.1f}% P95={p['p95']:.1f}% P99={p['p99']:.1f}%")
    print()

    # 磁盘
    print(f"  磁盘:")
    for disk in resources['disk']:
        print(f"    {disk['mountpoint']} ({disk['device']}):")
        print(f"      使用率: {disk['percent']:.1f}% {disk['status']}")
        print(f"      已用: {disk['used']} / {disk['total']}")
        print(f"      可用: {disk['free']}")
    print()

    # 网络
    network = resources['network']
    print(f"  网络:")
    print(f"    发送: {network['bytes_sent']} ({network['packets_sent']:,} 包)")
    print(f"    接收: {network['bytes_recv']} ({network['packets_recv']:,} 包)")
    print(f"    连接数: {network['connections']}")
    print(f"    错误: 发送 {network['errors_out']}, 接收 {network['errors_in']}")
    print()

    # Top进程
    print("🔝 资源使用Top 5:")
    print()
    print("  按CPU:")
    for i, proc in enumerate(report['top_processes']['by_cpu'], 1):
        print(f"   {i}. PID {proc['pid']}: {proc['name']}")
        print(f"      CPU: {proc['cpu_percent']:.1f}%, 内存: {proc['memory_percent']:.1f}%, 运行: {proc['uptime']}")
    print()

    print("  按内存:")
    for i, proc in enumerate(report['top_processes']['by_memory'], 1):
        print(f"   {i}. PID {proc['pid']}: {proc['name']}")
        print(f"      CPU: {proc['cpu_percent']:.1f}%, 内存: {proc['memory_percent']:.1f}%, 运行: {proc['uptime']}")
    print()

    # 趋势预测
    print("🔮 资源使用预测:")
    print()

    # CPU预测
    cpu_pred = report['predictions']['cpu']
    print(f"  CPU:")
    print(f"    当前: {cpu_pred['current']:.1f}%")
    print(f"    增长率: {cpu_pred['growth_rate']:.2f}%/小时")
    print(f"    预测: 1小时={cpu_pred['predictions']['1h']:.1f}% | 6小时={cpu_pred['predictions']['6h']:.1f}% | 24小时={cpu_pred['predictions']['24h']:.1f}% | 7天={cpu_pred['predictions']['7d']:.1f}%")

    # 内存预测
    mem_pred = report['predictions']['memory']
    print(f"  内存:")
    print(f"    当前: {mem_pred['current']:.1f}%")
    print(f"    增长率: {mem_pred['growth_rate']:.2f}%/小时")
    print(f"    预测: 1小时={mem_pred['predictions']['1h']:.1f}% | 6小时={mem_pred['predictions']['6h']:.1f}% | 24小时={mem_pred['predictions']['24h']:.1f}% | 7天={mem_pred['predictions']['7d']:.1f}%")
    print()

    # 建议
    all_recommendations = cpu_pred['recommendations'] + mem_pred['recommendations']
    if all_recommendations:
        print("💡 容量规划建议:")
        for rec in all_recommendations:
            print(f"   {rec}")
        print()

    # 系统信息
    info = report['system_info']
    print("💻 系统信息:")
    print(f"   平台: {info['platform']} {info['platform_version']}")
    print(f"   架构: {info['architecture']}")
    print(f"   主机名: {info['hostname']}")
    print(f"   Python: {info['python_version']}")
    print(f"   启动时间: {info['boot_time']}")
    print()


def continuous_monitor(interval: int = 5, duration: int = 60) -> Any:
    """连续监控模式"""
    monitor = SystemMonitor()
    start_time = time.time()

    print(f"开始连续监控（间隔: {interval}秒, 持续: {duration}秒）")
    print("按 Ctrl+C 停止")
    print()

    try:
        while time.time() - start_time < duration:
            report = monitor.run_health_check()

            # 简化输出
            health = report['health_status']
            cpu = report['system_resources']['cpu']
            memory = report['system_resources']['memory']

            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"{health['status']} | "
                  f"CPU: {cpu['usage_percent']:.1f}% {cpu['status']} | "
                  f"内存: {memory['percent']:.1f}% {memory['status']} | "
                  f"Live: {'✅' if health['liveness'] else '❌'} Ready: {'✅' if health['readiness'] else '❌'}")

            if health['critical_issues']:
                for issue in health['critical_issues']:
                    print(f"  🔴 {issue}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print()
        print("监控已停止")


def main() -> Any:
    try:
        """CLI入口"""
        import argparse
    except Exception as e:
        logger.error(f"执行出错: {e}")
        return 1

    parser = argparse.ArgumentParser(description='系统监控工具')
    parser.add_argument('--health-check', action='store_true', help='运行一次完整的健康检查')
    parser.add_argument('--continuous', action='store_true', help='连续监控模式')
    parser.add_argument('--interval', type=int, default=5, help='连续监控的采样间隔（秒）')
    parser.add_argument('--duration', type=int, default=60, help='连续监控的持续时间（秒）')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    parser.add_argument('--percentiles', action='store_true', help='显示百分位数统计')

    args = parser.parse_args()

    if args.continuous:
        continuous_monitor(args.interval, args.duration)
    else:
        # 默认运行健康检查
        monitor = SystemMonitor()
        report = monitor.run_health_check()

        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
        else:
            print_report(report, show_percentiles=args.percentiles)


if __name__ == '__main__':
    main()


# Resource management example
if False:  # noqa
    with open("example.txt", "r") as f:
        pass
