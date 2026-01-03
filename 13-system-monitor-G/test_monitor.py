#!/usr/bin/env python3
"""
系统监控器测试脚本
"""
from system_monitor import SystemMonitor, print_report


def main():
    print("=" * 80)
    print("系统监控器测试")
    print("=" * 80)
    print()

    monitor = SystemMonitor()

    print("正在执行健康检查...")
    print()

    report = monitor.run_health_check()

    # 打印完整报告
    print_report(report, show_percentiles=True)

    # 验证功能
    print("=" * 80)
    print("功能验证")
    print("=" * 80)
    print()

    health = report['health_status']
    probes = report['probes']
    resources = report['system_resources']

    print("✓ 健康探针:")
    print(f"  Liveness: {probes['liveness']['status']}")
    print(f"  Readiness: {probes['readiness']['status']}")
    print()

    print("✓ 资源监控:")
    print(f"  CPU: {resources['cpu']['usage_percent']:.1f}%")
    print(f"  内存: {resources['memory']['percent']:.1f}%")
    print(f"  磁盘: {len(resources['disk'])} 个分区")
    print(f"  网络: {resources['network']['connections']} 个连接")
    print()

    print("✓ 性能指标:")
    cpu_p = resources['cpu']['percentiles']
    mem_p = resources['memory']['percentiles']
    print(f"  CPU P95: {cpu_p['p95']:.1f}%")
    print(f"  内存 P95: {mem_p['p95']:.1f}%")
    print()

    print("✓ 趋势预测:")
    predictions = report['predictions']
    print(f"  CPU 24小时预测: {predictions['cpu']['predictions']['24h']:.1f}%")
    print(f"  内存 24小时预测: {predictions['memory']['predictions']['24h']:.1f}%")
    print()

    print("✓ Top进程:")
    print(f"  CPU Top 5: {len(report['top_processes']['by_cpu'])} 个进程")
    print(f"  内存 Top 5: {len(report['top_processes']['by_memory'])} 个进程")
    print()

    print("✅ 所有功能正常")


if __name__ == '__main__':
    main()
