"""10-quality-gate 测试"""
from engine import QualityGate

def test_quality_gate():
    print("=== 测试质量门控 ===\n")

    gate = QualityGate()

    # 测试通过场景
    result = gate.evaluate(
        coverage=85.0,
        avg_complexity=8.0,
        security_score=95.0,
        critical_vulns=0,
        code='def example(): pass'
    )

    print(f"质量评估:")
    print(f"  通过: {result.passed}")
    print(f"  总分: {result.score}/100")
    print(f"  覆盖率: {result.metrics.coverage}%")
    print(f"  可维护性: {result.metrics.maintainability}")

    # 测试未通过场景
    result2 = gate.evaluate(
        coverage=60.0,  # 低于阈值
        avg_complexity=15.0,  # 过高
        security_score=75.0,  # 低分
        critical_vulns=2,  # 有漏洞
        code='def example(): pass'
    )

    print(f"\n未通过场景:")
    print(f"  通过: {result2.passed}")
    print(f"  失败检查: {result2.failed_checks}")

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_quality_gate()
