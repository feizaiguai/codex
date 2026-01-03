"""31-risk-assessor 测试"""
from engine import RiskAssessor

def test_risk_assessment():
    assessor = RiskAssessor()
    assessment = assessor.assess(
        "测试项目",
        {'complexity': 25, 'test_coverage': 70},
        ['old-package'],
        ['GDPR']
    )
    print(f"风险评估: {len(assessment.risks)}个风险")
    print(f"总体分数: {assessment.overall_risk_score:.2f}")
    assert len(assessment.risks) > 0

if __name__ == '__main__':
    print("风险评估测试")
    test_risk_assessment()
    print("✓ 测试通过")
