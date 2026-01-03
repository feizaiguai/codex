"""05-code-review 测试"""
from engine import CodeReviewer, ComplexityAnalyzer, SecurityScanner

def test_review():
    print("=== 测试代码审查 ===\n")

    # 创建测试文件
    test_code = '''
def complex_function(x, y):
    if x > 0:
        if y > 0:
            if x > y:
                return x
            else:
                return y
        else:
            return x
    else:
        return 0

password = "hardcoded123"  # 安全问题
'''

    with open('test_code.py', 'w') as f:
        f.write(test_code)

    reviewer = CodeReviewer()
    result = reviewer.review_file('test_code.py')

    print(f"质量评分: {result['quality_score']['score']}/100")
    print(f"问题数: {result['quality_score']['total_issues']}")

    import os
    os.remove('test_code.py')

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_review()
