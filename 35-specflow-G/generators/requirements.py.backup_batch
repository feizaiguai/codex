"""
需求规格生成器
负责生成 01-需求规格.md
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, RequirementItem, UserStory


class RequirementsGenerator(BaseGenerator):
    """需求规格生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成需求规格文档

        context 必需字段:
            - requirements: List[RequirementItem]
            - user_stories: List[UserStory]
        """
        # 1. 提取数据
        requirements: List[RequirementItem] = context['requirements']
        user_stories: List[UserStory] = context['user_stories']

        # 2. 分类需求
        func_reqs = [r for r in requirements if r.type.value == "功能性需求"]
        non_func_reqs = [r for r in requirements if r.type.value == "非功能性需求"]

        # 3. 准备模板数据
        template_data = {
            'func_count': len(func_reqs),
            'func_reqs': func_reqs,
            'non_func_count': len(non_func_reqs),
            'non_func_reqs': non_func_reqs,
            'story_count': len(user_stories),
            'user_stories': user_stories,
        }

        # 4. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('requirements.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        # 如果模板渲染结果为空,使用内置生成
        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 5. 创建Document对象
        return Document(
            type=DocumentType.REQUIREMENTS,
            title="需求规格说明",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=20000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 功能性需求
        parts.append(f"## 功能性需求\n\n")
        parts.append(f"共{data['func_count']}个功能性需求:\n\n")

        for req in data['func_reqs']:
            parts.append(f"### {req.id}: {req.title}\n\n")
            parts.append(f"{req.description}\n\n")
            parts.append(f"**优先级**: {req.priority.value}\n\n")

        # 非功能性需求
        parts.append(f"## 非功能性需求\n\n")

        if data['non_func_count'] > 0:
            parts.append(f"共{data['non_func_count']}个非功能性需求:\n\n")
            for req in data['non_func_reqs']:
                parts.append(f"### {req.id}: {req.title}\n\n")
                parts.append(f"{req.description}\n\n")
                parts.append(f"**优先级**: {req.priority.value}\n\n")
        else:
            parts.append("暂无非功能性需求\n\n")

        # 用户故事
        parts.append(f"## 用户故事\n\n")
        parts.append(f"共{data['story_count']}个用户故事:\n\n")

        for us in data['user_stories']:
            parts.append(f"### {us.id}: {us.i_want}\n\n")
            parts.append(f"- **作为**: {us.as_a}\n")
            parts.append(f"- **我想要**: {us.i_want}\n")
            parts.append(f"- **以便**: {us.so_that}\n")
            parts.append(f"- **优先级**: {us.priority.value}\n\n")
            parts.append("**验收标准**:\n")
            for ac in us.acceptance_criteria:
                parts.append(f"- {ac}\n")
            parts.append("\n")

        # 验收标准指南
        parts.append(self._get_acceptance_guidelines())

        return "".join(parts)

    def _get_acceptance_guidelines(self) -> str:
        """获取验收标准指南(静态内容)"""
        return """## 验收标准编写指南(INVEST原则)

### INVEST原则检查清单
-  **Independent(独立性)**: 故事之间相互独立,可独立开发和测试
-  **Negotiable(可协商)**: 需求细节可以讨论和调整
-  **Valuable(有价值)**: 为用户或业务带来明确价值
-  **Estimable(可估算)**: 可以合理估算工作量
-  **Small(小)**: 故事足够小,可在一个迭代内完成
-  **Testable(可测试)**: 有明确的验收标准,可验证完成

### 验收标准模板(推荐使用BDD格式)
```gherkin
Given [前置条件]
When [用户操作]
Then [预期结果]
And [额外验证点]
```

### 验收标准示例
```gherkin
Scenario: 用户成功下单
  Given 用户已登录系统
    And 购物车中有3件商品
  When 用户点击"结算"按钮
  Then 系统跳转到结算页面
    And 显示订单总金额
    And 提供支付方式选项
```
"""
