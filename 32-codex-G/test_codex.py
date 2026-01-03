"""32-codex 测试"""
from engine import Codex, Task, TaskType

def test_codex():
    codex = Codex()
    task = Task("创建排序函数", TaskType.CODE_GENERATION, {}, [])
    solution = codex.solve(task)
    print(f"解决方案: {solution.approach}")
    assert solution.success

if __name__ == '__main__':
    print("Codex测试")
    test_codex()
    print("✓ 测试通过")
