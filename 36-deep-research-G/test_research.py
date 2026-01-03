#!/usr/bin/env python3
"""
36-deep-research 测试套件

测试覆盖：
1. 核心功能测试（搜索、分析、报告生成）
2. Token 估算和分割测试
3. 命令行参数解析测试
4. 边界条件测试
5. 错误处理测试
"""

import sys
import asyncio
import pytest
from pathlib import Path
from typing import List

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from deep_research import (
    DeepResearchOrchestrator,
    ClaudeSearcher,
    GeminiSearcher,
    CodexSearcher,
    CredibilityScorer,
    GapAnalyzer,
    ReportGenerator,
    SearchResult,
    AISearchResults,
    Gap,
    estimate_tokens,
    split_report_by_tokens
)
from handler import parse_arguments, get_query_from_args, generate_output_filename


# =============================================================================
# 测试：Token 估算和分割
# =============================================================================

def test_estimate_tokens():
    """测试 token 估算功能"""
    print("测试 token 估算...")

    # 测试短文本
    short_text = "Hello World"
    tokens = estimate_tokens(short_text)
    assert tokens > 0
    assert tokens < 10

    # 测试长文本
    long_text = "A" * 10000
    tokens = estimate_tokens(long_text)
    assert tokens > 1000
    assert tokens < 10000

    # 测试中英文混合
    mixed_text = "这是一个测试 This is a test " * 100
    tokens = estimate_tokens(mixed_text)
    assert tokens > 0

    print(f"  ✓ 短文本: {estimate_tokens(short_text)} tokens")
    print(f"  ✓ 长文本: {estimate_tokens(long_text)} tokens")
    print(f"  ✓ 混合文本: {estimate_tokens(mixed_text)} tokens")


def test_split_report_by_tokens():
    """测试报告分割功能"""
    print("\n测试报告分割...")

    # 生成一个超过限制的报告
    header = "# Test Report\n\n" + "Metadata\n" * 20
    content = "Content line\n" * 1000
    report = header + content

    # 不需要分割
    parts = split_report_by_tokens(report, max_tokens=100000)
    assert len(parts) == 1
    print(f"  ✓ 小报告不分割: {len(parts)} 部分")

    # 需要分割
    parts = split_report_by_tokens(report, max_tokens=5000)
    assert len(parts) > 1

    # 验证每个部分都不超过限制
    for i, part in enumerate(parts, 1):
        tokens = estimate_tokens(part)
        assert tokens <= 5500  # 允许一些误差
        print(f"  ✓ Part {i}: {tokens} tokens (限制 5000)")

    # 验证所有部分都包含标题
    for part in parts:
        assert "Test Report" in part
        assert "Part" in part


def test_split_empty_report():
    """测试空报告分割"""
    print("\n测试空报告分割...")

    parts = split_report_by_tokens("", max_tokens=20000)
    assert len(parts) == 1
    assert parts[0] == ""
    print("  ✓ 空报告处理正确")


# =============================================================================
# 测试：可信度评分
# =============================================================================

def test_credibility_scorer():
    """测试可信度评分器"""
    print("\n测试可信度评分...")

    # 官方文档 - 最高分
    official_result = {'url': 'https://docs.python.org/3/library/asyncio.html'}
    score = CredibilityScorer.calculate_score(official_result)
    assert score == 100
    print(f"  ✓ 官方文档: {score}/100")

    # GitHub 项目 - 高分
    github_result = {'url': 'https://github.com/python/cpython'}
    score = CredibilityScorer.calculate_score(github_result)
    assert score == 90
    print(f"  ✓ GitHub 项目: {score}/100")

    # StackOverflow - 中高分
    stackoverflow_result = {'url': 'https://stackoverflow.com/questions/12345/test'}
    score = CredibilityScorer.calculate_score(stackoverflow_result)
    assert score == 80
    print(f"  ✓ StackOverflow: {score}/100")

    # 技术博客 - 中等分
    blog_result = {'url': 'https://medium.com/test-article'}
    score = CredibilityScorer.calculate_score(blog_result)
    assert score == 75
    print(f"  ✓ 技术博客: {score}/100")

    # 未知网站 - 默认分
    unknown_result = {'url': 'https://example.com/test'}
    score = CredibilityScorer.calculate_score(unknown_result)
    assert score == 60
    print(f"  ✓ 未知网站: {score}/100")


# =============================================================================
# 测试：Codex 搜索策略
# =============================================================================

def test_codex_is_code_searchable():
    """测试 Codex 代码搜索判断逻辑"""
    print("\n测试 Codex 代码搜索判断...")

    # 适合代码搜索
    assert CodexSearcher.is_code_searchable("Python async programming") == True
    assert CodexSearcher.is_code_searchable("React hooks implementation") == True
    assert CodexSearcher.is_code_searchable("JavaScript async await") == True
    print("  ✓ 代码查询识别正确")

    # 不适合代码搜索（理论）
    assert CodexSearcher.is_code_searchable("academic survey of ML") == False
    assert CodexSearcher.is_code_searchable("research paper theory") == False
    assert CodexSearcher.is_code_searchable("arxiv literature review") == False
    print("  ✓ 理论查询识别正确")

    # 工具/库查询
    assert CodexSearcher.is_code_searchable("best Python libraries") == True
    assert CodexSearcher.is_code_searchable("React framework") == True
    print("  ✓ 工具查询识别正确")


# =============================================================================
# 测试：差距分析
# =============================================================================

def test_gap_analyzer():
    """测试差距分析器"""
    print("\n测试差距分析...")

    # 创建模拟的搜索结果
    claude_results = AISearchResults(
        ai_name="Claude",
        query="test",
        results=[
            SearchResult(title="Documentation Guide", url="https://example.com/1", snippet="test", score=90, credibility=100),
            SearchResult(title="Tutorial", url="https://example.com/2", snippet="test", score=85, credibility=90)
        ]
    )

    gemini_results = AISearchResults(
        ai_name="Gemini",
        query="test",
        results=[
            SearchResult(title="Architecture Design", url="https://example.com/3", snippet="test", score=88, credibility=95)
        ]
    )

    codex_results = AISearchResults(
        ai_name="Codex",
        query="test",
        results=[]
    )

    gaps = GapAnalyzer.identify_gaps(claude_results, gemini_results, codex_results, "test query")

    # 应该识别出缺失的主题
    assert len(gaps) > 0
    assert any(gap.topic == 'performance' for gap in gaps)
    assert any(gap.topic == 'security' for gap in gaps)

    print(f"  ✓ 识别到 {len(gaps)} 个差距")
    for gap in gaps:
        print(f"    - {gap.topic}: {gap.gap_type} (优先级 {gap.priority})")


# =============================================================================
# 测试：命令行参数解析
# =============================================================================

def test_generate_output_filename():
    """测试输出文件名生成"""
    print("\n测试文件名生成...")

    # 无用户指定文件名
    filename = generate_output_filename("test query", None)
    assert filename.startswith("research_")
    assert filename.endswith(".md")
    print(f"  ✓ 自动生成: {filename}")

    # 有用户指定文件名
    filename = generate_output_filename("test query", "my_report.md")
    assert filename == "my_report.md"
    print(f"  ✓ 用户指定: {filename}")

    # 分段文件名
    filename = generate_output_filename("test query", "my_report.md", part=2)
    assert filename == "my_report_part2.md"
    print(f"  ✓ 分段文件: {filename}")

    # 超长查询截断
    long_query = "A" * 100
    filename = generate_output_filename(long_query, None)
    assert len(filename) < 100
    print(f"  ✓ 长查询截断: {filename}")


# =============================================================================
# 测试：报告生成
# =============================================================================

def test_report_generator():
    """测试报告生成器"""
    print("\n测试报告生成...")

    # 创建测试数据
    claude_results = AISearchResults(
        ai_name="Claude",
        query="test",
        results=[
            SearchResult(title="Test1", url="https://example.com/1", snippet="snippet1", score=90, credibility=100, source="claude")
        ],
        total_results=1
    )

    gemini_results = AISearchResults(
        ai_name="Gemini",
        query="test",
        results=[],
        total_results=0
    )

    codex_results = AISearchResults(
        ai_name="Codex",
        query="test",
        results=[],
        total_results=0
    )

    report = ReportGenerator.generate_markdown(
        query="test query",
        claude_results=claude_results,
        gemini_results=gemini_results,
        codex_results=codex_results,
        gap_results=[],
        gaps=[],
        total_time=10.5
    )

    # 验证报告结构
    assert "test query" in report
    assert "深度研究报告" in report
    assert "元数据" in report
    assert "执行摘要" in report
    assert "Claude" in report
    assert "10.5" in report  # 总耗时

    print("  ✓ 报告结构完整")
    print(f"  ✓ 报告长度: {len(report)} 字符")


# =============================================================================
# 测试：去重和排序
# =============================================================================

def test_deduplicate_and_sort():
    """测试去重和排序功能"""
    print("\n测试去重和排序...")

    results = [
        SearchResult(title="A", url="https://example.com/1", snippet="", score=80, credibility=90),
        SearchResult(title="B", url="https://example.com/2", snippet="", score=85, credibility=100),
        SearchResult(title="C", url="https://example.com/1", snippet="", score=90, credibility=95),  # 重复 URL
        SearchResult(title="D", url="https://example.com/3", snippet="", score=70, credibility=80),
    ]

    unique = ReportGenerator._deduplicate_and_sort(results)

    # 应该去除重复的 URL
    assert len(unique) == 3

    # 应该按可信度降序排序
    assert unique[0].credibility == 100
    assert unique[1].credibility == 90
    assert unique[2].credibility == 80

    print(f"  ✓ 去重: {len(results)} → {len(unique)}")
    print(f"  ✓ 排序: 可信度依次为 {[r.credibility for r in unique]}")


# =============================================================================
# 主测试运行器
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("=" * 80)
    print("运行 36-deep-research 测试套件")
    print("=" * 80)

    # Token 估算和分割测试
    test_estimate_tokens()
    test_split_report_by_tokens()
    test_split_empty_report()

    # 可信度评分测试
    test_credibility_scorer()

    # Codex 搜索策略测试
    test_codex_is_code_searchable()

    # 差距分析测试
    test_gap_analyzer()

    # 命令行参数测试
    test_generate_output_filename()

    # 报告生成测试
    test_report_generator()

    # 去重和排序测试
    test_deduplicate_and_sort()

    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
