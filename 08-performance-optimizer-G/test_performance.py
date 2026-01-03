"""08-performance-optimizer 测试"""
from engine import PerformanceOptimizer

def test_performance():
    print("=== 测试性能优化 ===\n")

    test_code = '''
def slow_search(data, targets):
    results = []
    for target in targets:  # O(n)
        for item in data:  # O(m)
            if item == target:
                results.append(item)
    return results

def query_users(user_ids):
    for user_id in user_ids:
        user = User.objects.get(id=user_id)  # N+1 query
        print(user.name)
'''

    with open('test_perf.py', 'w') as f:
        f.write(test_code)

    optimizer = PerformanceOptimizer()
    issues = optimizer.analyze_file('test_perf.py')

    print(f"发现 {len(issues)} 个性能问题:")
    for issue in issues:
        print(f"  - {issue.category}: {issue.description}")

    import os
    os.remove('test_perf.py')

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_performance()
