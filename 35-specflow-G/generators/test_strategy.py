"""
测试策略生成器
负责生成 05-测试策略.md
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, UserStory, TestCase


class TestStrategyGenerator(BaseGenerator):
    """测试策略生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成测试策略文档

        context 必需字段:
            - user_stories: List[UserStory]
            - test_cases: List[TestCase] (可选)
        """
        # 1. 提取数据
        user_stories: List[UserStory] = context['user_stories']
        test_cases: List[TestCase] = context.get('test_cases', [])

        # 2. 准备模板数据
        template_data = {
            'story_count': len(user_stories),
            'test_case_count': len(test_cases),
            'test_cases': test_cases,
        }

        # 3. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('test_strategy.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 4. 创建Document对象
        return Document(
            type=DocumentType.TEST_STRATEGY,
            title="测试策略",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=18000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 测试概览
        parts.append(f"## 测试概览\n\n")
        parts.append(f"**用户故事数**: {data['story_count']}\n")
        parts.append(f"**测试用例数**: {data['test_case_count']}\n\n")
        parts.append("本文档定义了完整的测试策略,确保系统质量.\n\n")

        # 测试金字塔
        parts.append(self._get_test_pyramid())

        # 测试用例
        if data['test_case_count'] > 0:
            parts.append(f"## 测试用例\n\n")
            parts.append(f"共{data['test_case_count']}个测试用例(显示前10个):\n\n")
            for tc in data['test_cases'][:10]:
                parts.append(f"### {tc.id}: {tc.name}\n\n")
                parts.append(f"- **类型**: {tc.test_type.value}\n")
                parts.append(f"- **优先级**: {tc.priority.value}\n")
                parts.append(f"- **前置条件**: {tc.preconditions}\n")
                parts.append(f"- **测试步骤**: {tc.steps}\n")
                parts.append(f"- **预期结果**: {tc.expected_result}\n\n")

        # 测试用例模板
        parts.append(self._get_test_template())

        return "".join(parts)

    def _get_test_pyramid(self) -> str:
        """获取测试金字塔章节"""
        return r"""## 测试金字塔

```
        /\
       /E2E\        10% - 端到端测试
      /------\
     /Integration\ 30% - 集成测试
    /------------\
   /  Unit Tests  \ 60% - 单元测试
  /----------------\
```

### 单元测试
- 覆盖所有核心业务逻辑
- 目标覆盖率: 80%+

### 集成测试
- 测试模块间接口
- 数据库集成测试

### 端到端测试
- 关键用户旅程
- 冒烟测试

"""

    def _get_test_template(self) -> str:
        """获取测试模板章节"""
        return """## 测试用例编写模板

### 单元测试用例模板
```python
def test_example():
    # Arrange(准备)
    input_data = create_test_data()

    # Act(执行)
    result = function_under_test(input_data)

    # Assert(断言)
    assert result == expected_value
    assert result.is_valid()
```

### 集成测试用例模板
```gherkin
Feature: 用户注册功能

  Scenario: 成功注册新用户
    Given 数据库中不存在该用户
    When 用户提交有效的注册表单
    Then 系统创建新用户记录
      And 发送欢迎邮件
      And 跳转到首页
```

### 边界值测试指南
- **最小值**: 测试最小合法值
- **最大值**: 测试最大合法值
- **边界值**: 测试边界两侧的值
- **非法值**: 测试非法输入的错误处理

### 测试数据准备
- **正常数据**: 覆盖常见使用场景
- **边界数据**: 覆盖临界值
- **异常数据**: 覆盖错误场景
- **安全数据**: 覆盖注入攻击等安全测试
"""
