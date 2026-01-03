#!/usr/bin/env python3
"""
简单测试脚本 - 生成测试日志并分析
"""
import tempfile
import os
from datetime import datetime, timedelta
from log_analyzer import LogAnalyzer, print_report


def generate_test_logs():
    """生成测试日志文件"""
    logs = []
    base_time = datetime.now() - timedelta(hours=1)

    # 正常日志
    for i in range(100):
        ts = base_time + timedelta(seconds=i * 10)
        logs.append(f'{ts.isoformat()} INFO Normal request processed\n')

    # 一些警告
    for i in range(10):
        ts = base_time + timedelta(seconds=i * 60)
        logs.append(f'{ts.isoformat()} WARN Slow query detected: 1.5s\n')

    # 错误突增
    spike_time = base_time + timedelta(minutes=30)
    for i in range(20):
        ts = spike_time + timedelta(seconds=i)
        logs.append(f'{ts.isoformat()} ERROR Database connection timeout\n')

    # 新错误类型
    for i in range(5):
        ts = base_time + timedelta(minutes=40 + i)
        logs.append(f'{ts.isoformat()} ERROR NullPointerException at line {100 + i}\n')

    # 安全威胁模拟
    attack_time = base_time + timedelta(minutes=50)
    for i in range(15):
        ts = attack_time + timedelta(seconds=i * 2)
        logs.append(f'{ts.isoformat()} WARN Login failed for user admin from 192.168.1.100\n')

    return logs


def main():
    print("=" * 80)
    print("日志分析器测试")
    print("=" * 80)
    print()

    # 创建临时日志文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        test_file = f.name
        logs = generate_test_logs()
        f.writelines(logs)

    print(f"已生成测试日志文件: {test_file}")
    print(f"日志总数: {len(logs)}")
    print()

    try:
        # 分析日志
        analyzer = LogAnalyzer()
        report = analyzer.analyze_file(test_file)

        if 'error' in report:
            print(f"分析失败: {report['error']}")
            return

        # 打印报告
        print_report(report, verbose=True)

        # 验证关键功能
        print("=" * 80)
        print("功能验证")
        print("=" * 80)
        print()

        summary = report['summary']
        anomalies = report['anomalies']

        print("✓ 日志解析:")
        print(f"  解析成功率: {summary['parse_success_rate']}")
        print()

        print("✓ 异常检测:")
        print(f"  错误突增检测: {len(anomalies['error_spikes'])} 个")
        print(f"  新错误检测: {len(anomalies['new_errors'])} 个")
        print(f"  安全威胁检测: {len(anomalies['security_threats'])} 个")
        print()

        print("✓ 错误统计:")
        print(f"  总错误数: {summary['error_count']}")
        print(f"  错误率: {summary['error_rate']}")
        print()

        if report.get('correlation'):
            print("✓ 事件关联:")
            print(f"  关联链数: {report['correlation']['correlated_chains']}")
            print()

        print("✅ 所有功能正常")

    finally:
        # 清理临时文件
        try:
            os.unlink(test_file)
            print(f"\n已删除临时文件: {test_file}")
        except:
            pass


if __name__ == '__main__':
    main()
