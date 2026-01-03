"""33-gemini 测试"""
from engine import GeminiAssistant, GeminiTask, TaskCategory

def test_gemini():
    assistant = GeminiAssistant()
    task = GeminiTask("优化查询性能", TaskCategory.DIAGNOSIS, {})
    result = assistant.execute(task)
    print(f"执行结果: {result.strategy}")
    assert result.success

if __name__ == '__main__':
    print("Gemini测试")
    test_gemini()
    print("✓ 测试通过")
