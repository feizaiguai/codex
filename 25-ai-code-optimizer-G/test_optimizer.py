"""
25-ai-code-optimizer 测试脚本
"""

from engine import AICodeOptimizer


def test_quadratic_complexity():
    """测试O(n²)复杂度检测"""
    code = """
def find_duplicates(list1, list2):
    duplicates = []
    for item in list1:
        for target in list2:
            if item == target:
                duplicates.append(item)
    return duplicates
"""

    optimizer = AICodeOptimizer()
    report = optimizer.optimize_code(code, "test_quadratic.py")

    print("测试1: O(n²)复杂度检测")
    print(f"时间复杂度: {report.complexity_analysis.time_complexity}")
    print(f"发现问题: {len(report.issues)}个")
    print(f"评分: {report.overall_score}/100")
    print()

    assert "O(n²)" in report.complexity_analysis.time_complexity
    assert len(report.issues) > 0


def test_memory_leak():
    """测试内存泄漏检测"""
    code = """
def process_file(filename):
    f = open(filename, 'r')
    data = f.read()
    return data
"""

    optimizer = AICodeOptimizer()
    report = optimizer.optimize_code(code, "test_memory.py")

    print("测试2: 内存泄漏检测")
    print(f"内存问题: {report.memory_analysis['total_issues']}个")
    print(f"评分: {report.overall_score}/100")
    print()

    assert report.memory_analysis['total_issues'] > 0


def test_optimal_code():
    """测试优化代码"""
    code = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""

    optimizer = AICodeOptimizer()
    report = optimizer.optimize_code(code, "test_optimal.py")

    print("测试3: 优化代码评估")
    print(f"时间复杂度: {report.complexity_analysis.time_complexity}")
    print(f"发现问题: {len(report.issues)}个")
    print(f"评分: {report.overall_score}/100")
    print()

    assert report.overall_score >= 70


def test_full_report():
    """测试完整报告生成"""
    code = """
def nested_loops(n):
    result = []
    for i in range(n):
        for j in range(n):
            result.append(i * j)
    return result
"""

    optimizer = AICodeOptimizer()
    report = optimizer.optimize_code(code, "test_nested.py")

    print("测试4: 完整报告生成")
    report_text = optimizer.generate_report(report)
    print(report_text)
    print()

    assert "O(n²)" in report_text
    assert "优化建议" in report_text or "问题" in report_text


if __name__ == '__main__':
    print("=" * 80)
    print("AI代码优化器测试套件")
    print("=" * 80)
    print()

    try:
        test_quadratic_complexity()
        test_memory_leak()
        test_optimal_code()
        test_full_report()

        print("✓ 所有测试通过")
    except AssertionError as e:
        print(f"✗ 测试失败: {e}")
    except Exception as e:
        print(f"✗ 错误: {e}")
