"""
27-explainability-analyzer 测试脚本
"""

from engine import ExplainabilityAnalyzer


def test_explainability():
    """测试可解释性分析"""
    analyzer = ExplainabilityAnalyzer()

    predictions = [1, 0, 1, 1, 0]
    features = [
        {'age': 25, 'income': 50000, 'gender': 'M'},
        {'age': 35, 'income': 70000, 'gender': 'F'},
        {'age': 45, 'income': 90000, 'gender': 'M'},
    ]

    report = analyzer.analyze('test_model', predictions, features)

    print("可解释性分析测试")
    print(f"评分: {report.interpretability_score:.1f}/100")
    print(f"特征数: {len(report.feature_importances)}")
    print(f"偏差检测: {len(report.bias_results)}")
    print()

    assert report.interpretability_score >= 0
    assert len(report.feature_importances) > 0


if __name__ == '__main__':
    print("=" * 80)
    print("AI可解释性分析器测试")
    print("=" * 80)
    print()
    test_explainability()
    print("✓ 测试通过")
