#!/usr/bin/env python3
"""
19-ui-component-generator 测试套件

测试覆盖：
1. 组件生成（React/Vue）
2. 测试代码生成
3. Storybook 故事生成
4. 无障碍属性添加
5. 原子设计系统生成
6. 边界条件和错误处理
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from engine import (
    ComponentGenerator,
    Framework,
    ComponentType,
    ComponentSpec,
    ComponentProp,
    ComponentEvent,
    ReactGenerator,
    VueGenerator
)


def test_react_component_generation():
    """测试 React 组件生成"""
    print("测试 React 组件生成...")

    spec = ComponentSpec(
        name="Button",
        type=ComponentType.ATOM,
        description="按钮组件",
        props=[
            ComponentProp(name="label", type="string", required=True, description="按钮文本"),
            ComponentProp(name="disabled", type="boolean", default_value=False, description="是否禁用")
        ],
        events=[
            ComponentEvent(name="click", payload_type="MouseEvent", description="点击事件")
        ]
    )

    gen = ComponentGenerator(Framework.REACT)
    files = gen.generate(spec)

    assert "Button.tsx" in files
    assert "Button.test.tsx" in files
    assert "Button.stories.tsx" in files

    # 验证组件代码
    component_code = files["Button.tsx"]
    assert "Button" in component_code
    assert "interface ButtonProps" in component_code
    assert "label" in component_code
    assert "disabled" in component_code
    assert "onClick" in component_code
    assert "displayName" in component_code

    print("  ✓ Button.tsx 生成成功")
    print("  ✓ Button.test.tsx 生成成功")
    print("  ✓ Button.stories.tsx 生成成功")


def test_react_test_generation():
    """测试 React 测试代码生成"""
    print("\n测试 React 测试代码生成...")

    spec = ComponentSpec(
        name="Input",
        type=ComponentType.ATOM,
        description="输入框组件",
        props=[
            ComponentProp(name="value", type="string"),
            ComponentProp(name="placeholder", type="string")
        ],
        events=[
            ComponentEvent(name="change", payload_type="string")
        ],
        accessibility={"role": "textbox"}
    )

    gen = ReactGenerator()
    test_code = gen.generate_test(spec)

    assert "describe('Input'" in test_code
    assert "should render successfully" in test_code
    assert "should have correct display name" in test_code
    assert "should handle value prop" in test_code
    assert "should handle change event" in test_code
    assert "should have proper accessibility attributes" in test_code

    print("  ✓ 测试代码包含基础测试")
    print("  ✓ 测试代码包含属性测试")
    print("  ✓ 测试代码包含事件测试")
    print("  ✓ 测试代码包含无障碍测试")


def test_vue_component_generation():
    """测试 Vue 组件生成"""
    print("\n测试 Vue 组件生成...")

    spec = ComponentSpec(
        name="Card",
        type=ComponentType.MOLECULE,
        description="卡片组件",
        props=[
            ComponentProp(name="title", type="string", required=True),
            ComponentProp(name="elevated", type="boolean", default_value=False)
        ],
        slots=["default"]
    )

    gen = ComponentGenerator(Framework.VUE)
    files = gen.generate(spec)

    assert "Card.vue" in files
    assert "Card.spec.ts" in files

    # 验证组件代码
    component_code = files["Card.vue"]
    assert "<template>" in component_code
    assert "<script setup" in component_code
    assert "<style scoped>" in component_code
    assert "interface Props" in component_code
    assert "title" in component_code
    assert "<slot />" in component_code

    print("  ✓ Card.vue 生成成功")
    print("  ✓ Card.spec.ts 生成成功")
    print("  ✓ 包含模板、脚本、样式")


def test_accessibility_addition():
    """测试无障碍属性添加"""
    print("\n测试无障碍属性添加...")

    # Button 组件
    button_spec = ComponentSpec(
        name="MyButton",
        type=ComponentType.ATOM,
        description="自定义按钮"
    )

    gen = ComponentGenerator()
    enhanced_spec = gen.add_accessibility(button_spec)

    assert enhanced_spec.accessibility.get("role") == "button"
    assert "aria-pressed" in enhanced_spec.accessibility
    print("  ✓ Button 组件添加无障碍属性")

    # Input 组件
    input_spec = ComponentSpec(
        name="MyInput",
        type=ComponentType.ATOM,
        description="自定义输入框"
    )

    enhanced_spec = gen.add_accessibility(input_spec)
    assert enhanced_spec.accessibility.get("role") == "textbox"
    assert "aria-required" in enhanced_spec.accessibility
    print("  ✓ Input 组件添加无障碍属性")

    # Checkbox 组件
    checkbox_spec = ComponentSpec(
        name="MyCheckbox",
        type=ComponentType.ATOM,
        description="自定义复选框"
    )

    enhanced_spec = gen.add_accessibility(checkbox_spec)
    assert enhanced_spec.accessibility.get("role") == "checkbox"
    assert "aria-checked" in enhanced_spec.accessibility
    print("  ✓ Checkbox 组件添加无障碍属性")


def test_atomic_design_system():
    """测试原子设计系统生成"""
    print("\n测试原子设计系统生成...")

    specs = [
        ComponentSpec(name="Button", type=ComponentType.ATOM, description="按钮"),
        ComponentSpec(name="Input", type=ComponentType.ATOM, description="输入框"),
        ComponentSpec(name="Form", type=ComponentType.MOLECULE, description="表单"),
        ComponentSpec(name="LoginForm", type=ComponentType.ORGANISM, description="登录表单"),
    ]

    gen = ComponentGenerator(Framework.REACT)
    files = gen.generate_atomic_system(specs)

    # 验证所有组件文件
    assert "atoms/Button/Button.tsx" in files
    assert "atoms/Input/Input.tsx" in files
    assert "molecules/Form/Form.tsx" in files
    assert "organisms/LoginForm/LoginForm.tsx" in files

    # 验证索引文件
    assert "index.ts" in files
    index_code = files["index.ts"]
    assert "Button" in index_code
    assert "Input" in index_code
    assert "Form" in index_code
    assert "LoginForm" in index_code

    print(f"  ✓ 生成 {len(specs)} 个组件")
    print("  ✓ 生成索引文件")
    print(f"  ✓ 总文件数: {len(files)}")


def test_storybook_generation():
    """测试 Storybook 故事生成"""
    print("\n测试 Storybook 故事生成...")

    spec = ComponentSpec(
        name="Badge",
        type=ComponentType.ATOM,
        description="徽章组件",
        props=[
            ComponentProp(name="color", type="string", default_value="primary", description="颜色"),
            ComponentProp(name="size", type="'small' | 'medium' | 'large'", default_value="medium", description="尺寸"),
            ComponentProp(name="count", type="number", default_value=0, description="数量")
        ]
    )

    gen = ReactGenerator()
    story_code = gen.generate_story(spec)

    assert "Meta" in story_code
    assert "StoryObj" in story_code
    assert "title: 'Components/Atom/Badge'" in story_code
    assert "argTypes" in story_code
    assert "color" in story_code
    assert "size" in story_code
    assert "count" in story_code
    assert "Default: Story" in story_code
    assert "WithCustomProps" in story_code

    print("  ✓ Story 元数据生成正确")
    print("  ✓ argTypes 生成正确")
    print("  ✓ 包含默认故事")
    print("  ✓ 包含自定义故事")


def test_test_value_generation():
    """测试测试值生成"""
    print("\n测试测试值生成...")

    gen = ReactGenerator()

    assert gen._get_test_value("string") == "'test'"
    assert gen._get_test_value("number") == "42"
    assert gen._get_test_value("boolean") == "true"
    assert gen._get_test_value("Array<string>") == "[]"
    assert gen._get_test_value("object") == "{}"
    assert gen._get_test_value("unknown") == "null"

    print("  ✓ string 类型测试值正确")
    print("  ✓ number 类型测试值正确")
    print("  ✓ boolean 类型测试值正确")
    print("  ✓ array 类型测试值正确")
    print("  ✓ object 类型测试值正确")


def test_control_type_generation():
    """测试 Storybook 控件类型生成"""
    print("\n测试 Storybook 控件类型生成...")

    gen = ReactGenerator()

    assert "text" in gen._get_control_type("string")
    assert "number" in gen._get_control_type("number")
    assert "boolean" in gen._get_control_type("boolean")
    assert "color" in gen._get_control_type("color")
    assert "object" in gen._get_control_type("any")

    print("  ✓ 控件类型映射正确")


def test_error_handling():
    """测试错误处理"""
    print("\n测试错误处理...")

    # 不支持的框架
    try:
        gen = ComponentGenerator(Framework.ANGULAR)
        spec = ComponentSpec(name="Test", type=ComponentType.ATOM, description="测试")
        gen.generate(spec)
        assert False, "应该抛出 ValueError"
    except ValueError as e:
        assert "不支持的框架" in str(e)
        print("  ✓ 不支持的框架错误处理正确")


def test_component_with_multiple_props_and_events():
    """测试包含多个属性和事件的组件"""
    print("\n测试复杂组件生成...")

    spec = ComponentSpec(
        name="Select",
        type=ComponentType.ATOM,
        description="下拉选择组件",
        props=[
            ComponentProp(name="value", type="string", required=True),
            ComponentProp(name="options", type="Array<string>", required=True),
            ComponentProp(name="placeholder", type="string", default_value="请选择"),
            ComponentProp(name="disabled", type="boolean", default_value=False),
            ComponentProp(name="multiple", type="boolean", default_value=False),
        ],
        events=[
            ComponentEvent(name="change", payload_type="string", description="值变化"),
            ComponentEvent(name="focus", payload_type="FocusEvent", description="获得焦点"),
            ComponentEvent(name="blur", payload_type="FocusEvent", description="失去焦点"),
        ],
        accessibility={
            "role": "combobox",
            "label": "选择器",
            "describedby": "select-description"
        }
    )

    gen = ComponentGenerator(Framework.REACT)
    files = gen.generate(spec)

    component_code = files["Select.tsx"]
    test_code = files["Select.test.tsx"]

    # 验证所有属性和事件都被包含
    for prop in spec.props:
        assert prop.name in component_code

    for event in spec.events:
        assert event.name.capitalize() in component_code

    # 验证测试包含前3个属性和前2个事件
    assert "should handle value prop" in test_code
    assert "should handle options prop" in test_code
    assert "should handle placeholder prop" in test_code
    assert "should handle change event" in test_code
    assert "should handle focus event" in test_code

    # 验证无障碍属性
    assert 'role="combobox"' in component_code
    assert 'aria-label="选择器"' in component_code
    assert 'aria-describedby="select-description"' in component_code

    print("  ✓ 复杂组件生成成功")
    print("  ✓ 所有属性和事件都被包含")
    print("  ✓ 无障碍属性正确")


def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("运行 19-ui-component-generator 测试套件")
    print("=" * 80 + "\n")

    test_react_component_generation()
    test_react_test_generation()
    test_vue_component_generation()
    test_accessibility_addition()
    test_atomic_design_system()
    test_storybook_generation()
    test_test_value_generation()
    test_control_type_generation()
    test_error_handling()
    test_component_with_multiple_props_and_events()

    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
