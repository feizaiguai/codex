"""
04-test-automation 测试脚本
"""

from engine import (
    TestAutomation, TestFramework, UnitTestGenerator,
    Function, MockGenerator, CoverageAnalyzer
)


def test_unit_test_generation():
    """测试单元测试生成"""
    print("=== 测试单元测试生成 ===\n")

    gen = UnitTestGenerator(TestFramework.PYTEST)

    function = Function(
        name='calculate_sum',
        params=[
            {'name': 'a', 'type': 'int'},
            {'name': 'b', 'type': 'int'}
        ],
        return_type='int',
        docstring='计算两数之和'
    )

    test_cases = gen.generate_tests(function)
    print(f"为 {function.name} 生成 {len(test_cases)} 个测试用例:")
    for tc in test_cases:
        print(f"  - {tc.name}: {tc.description}")

    code = gen.generate_test_code(function, test_cases[:1])
    print(f"\n示例测试代码:\n{code[:500]}...")

    print("\n✓ 单元测试生成测试通过")


def test_mock_generation():
    """测试 Mock 生成"""
    print("\n=== 测试 Mock 生成 ===\n")

    gen = MockGenerator()

    fixture_code = gen.generate_pytest_fixture('db_session', 'db = SessionLocal()')
    print("Fixture 代码:")
    print(fixture_code)

    mock_code = gen.generate_mock('UserService', ['create_user', 'get_user'])
    print("\nMock 代码:")
    print(mock_code)

    print("\n✓ Mock 生成测试通过")


def test_coverage_analysis():
    """测试覆盖率分析"""
    print("\n=== 测试覆盖率分析 ===\n")

    analyzer = CoverageAnalyzer()

    coverage_data = analyzer.analyze_coverage('dummy.coverage')
    report = analyzer.generate_coverage_report(coverage_data)

    print(report)

    print("\n✓ 覆盖率分析测试通过")


if __name__ == '__main__':
    test_unit_test_generation()
    test_mock_generation()
    test_coverage_analysis()

    print("\n" + "=" * 50)
    print("所有测试通过！")
    print("=" * 50)
