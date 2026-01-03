"""09-accessibility-checker 测试"""
from engine import AccessibilityChecker, WCAGLevel

def test_accessibility():
    print("=== 测试无障碍检查 ===\n")

    html = '''
<html>
<body>
    <h1>Title</h1>
    <h3>Subtitle</h3>
    <img src="image.jpg">
    <div onClick="doSomething()">Click me</div>
</body>
</html>
'''

    checker = AccessibilityChecker(WCAGLevel.AA)
    issues = checker.check_html(html)

    print(f"发现 {len(issues)} 个无障碍问题:")
    for issue in issues:
        print(f"  - {issue.rule}: {issue.description}")

    # 测试颜色对比度
    result = checker.check_color_contrast('#000000', '#FFFFFF')
    print(f"\n黑白对比度: {result['ratio']}:1 ({result['wcag_aa']})")

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_accessibility()
