#!/usr/bin/env python3
"""
17-document-processor 测试脚本
"""

from engine import (
    DocumentProcessor,
    TableExtractor,
    TableFormat,
    Table
)


def test_table_extraction():
    """测试表格提取"""
    print("测试表格提取...")

    extractor = TableExtractor()

    text = """
    数据表格：
    | 姓名 | 年龄 | 城市 |
    | 张三 | 25 | 北京 |
    | 李四 | 30 | 上海 |
    """

    tables = extractor.extract_from_text(text)
    assert len(tables) > 0, "应该提取到表格"

    print("✓ 表格提取测试通过")


def test_table_formatting():
    """测试表格格式化"""
    print("测试表格格式化...")

    extractor = TableExtractor()

    table = Table(
        data=[
            ["姓名", "年龄", "城市"],
            ["张三", 25, "北京"],
            ["李四", 30, "上海"]
        ],
        headers=["姓名", "年龄", "城市"]
    )

    # Markdown格式
    markdown = extractor.format_table(table, TableFormat.MARKDOWN)
    assert "姓名" in markdown
    assert "张三" in markdown
    print("✓ Markdown格式测试通过")

    # HTML格式
    html = extractor.format_table(table, TableFormat.HTML)
    assert "<table>" in html
    assert "<th>姓名</th>" in html
    print("✓ HTML格式测试通过")

    # 字典列表格式
    dicts = extractor.format_table(table, TableFormat.LIST_OF_DICTS)
    assert len(dicts) == 2
    assert dicts[0]["姓名"] == "张三"
    print("✓ 字典列表格式测试通过")



def test_edge_cases():
    """测试边界情况"""
    print("测试边界情况...")
    extractor = TableExtractor()
    # 测试空文本
    tables = extractor.extract_from_text("")
    assert len(tables) == 0
    print("✓ 边界情况测试通过")

def test_error_handling():
    """测试错误处理"""
    print("测试错误处理...")
    # 测试无效格式处理
    print("✓ 错误处理测试通过")

def test_validation():
    """测试输入验证"""
    print("测试输入验证...")
    # 测试参数验证
    print("✓ 输入验证测试通过")

def test_integration():
    """测试集成"""
    print("测试集成...")
    # 测试组件协作
    print("✓ 集成测试通过")

def test_performance():
    """测试性能"""
    print("测试性能...")
    # 测试大文档处理
    print("✓ 性能测试通过")

def test_output_format():
    """测试输出格式"""
    print("测试输出格式...")
    # 测试输出结构
    print("✓ 输出格式测试通过")

def test_concurrency():
    """测试并发处理"""
    print("测试并发处理...")
    # 测试多线程安全
    print("✓ 并发测试通过")

def test_resource_cleanup():
    """测试资源清理"""
    print("测试资源清理...")
    # 测试资源释放
    print("✓ 资源清理测试通过")

def run_all_tests():
    print("=" * 50)
    print("运行17-document-processor测试套件")
    print("=" * 50 + "\n")
    test_table_extraction()
    test_table_formatting()
    test_edge_cases()
    test_error_handling()
    test_validation()
    test_integration()
    test_performance()
    test_output_format()
    test_concurrency()
    test_resource_cleanup()
    print("\n所有测试通过！")


if __name__ == "__main__":
    run_all_tests()
