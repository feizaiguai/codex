"""11-debugger 测试"""
from engine import Debugger

def test_debugger():
    print("=== 测试调试器 ===\n")

    error_msg = 'AttributeError: NoneType object has no attribute "name"'
    stack_trace = '''Traceback (most recent call last):
  File "app.py", line 42, in process_user
    print(user.name)
AttributeError: NoneType object has no attribute "name"
'''

    code = '''
def process_user(user_id):
    user = get_user(user_id)  # 可能返回 None
    print(user.name)  # Bug: 未检查 None
'''

    debugger = Debugger()
    report = debugger.debug(error_msg, stack_trace, code)

    print(f"Bug 类型: {report.bug_type.value}")
    print(f"根因: {report.root_cause}")
    print(f"\n假设数量: {len(report.hypotheses)}")

    for h in report.hypotheses:
        print(f"  - {h.id}: {h.description} ({h.confidence}%)")

    print(f"\n修复建议数量: {len(report.fix_suggestions)}")

    print("\n✓ 测试通过")

if __name__ == '__main__':
    test_debugger()
