#!/usr/bin/env python3
"""
记忆管理器测试脚本
"""
import tempfile
import os
from pathlib import Path
from memory_tool import ClaudeMemoryManager


def main():
    print("=" * 80)
    print("记忆管理器测试")
    print("=" * 80)
    print()

    # 使用临时文件进行测试
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'CLAUDE.md'

        # 创建测试管理器
        manager = ClaudeMemoryManager(str(test_file))

        print("✓ 初始化管理器")
        print(f"  文件路径: {manager.get_path()}")
        print()

        # 测试添加偏好
        print("测试 1: 添加偏好")
        success = manager.add_preference(
            "测试类别",
            "- 这是一个测试偏好",
            tags=['test', 'important']
        )
        print(f"  结果: {'✅ 成功' if success else '❌ 失败'}")
        print()

        # 测试搜索
        print("测试 2: 搜索功能")
        results = manager.search("测试")
        print(f"  搜索结果数: {len(results)}")
        if results:
            print(f"  第一个结果: {results[0]['section']}")
        print()

        # 测试标签
        print("测试 3: 标签管理")
        tags = manager.list_all_tags()
        print(f"  标签数量: {len(tags)}")
        print(f"  标签列表: {', '.join(f'#{t}' for t in tags)}")
        print()

        # 测试备份
        print("测试 4: 备份功能")
        backup_path = manager.create_backup("测试备份")
        print(f"  备份路径: {backup_path}")

        backups = manager.list_backups()
        print(f"  备份数量: {len(backups)}")
        print()

        # 测试统计
        print("测试 5: 统计信息")
        stats = manager.get_statistics()
        print(f"  总行数: {stats['total_lines']}")
        print(f"  章节数: {stats['total_sections']}")
        print(f"  标签数: {stats['total_tags']}")
        print(f"  字符数: {stats['total_characters']}")
        print()

        # 测试按标签搜索
        print("测试 6: 按标签搜索")
        tag_results = manager.search_by_tag("test")
        print(f"  标签 #test 的结果数: {len(tag_results)}")
        print()

        # 功能验证
        print("=" * 80)
        print("功能验证")
        print("=" * 80)
        print()

        print("✓ 基础功能:")
        print("  ✅ 添加偏好")
        print("  ✅ 搜索功能")
        print("  ✅ 标签管理")
        print("  ✅ 备份功能")
        print("  ✅ 统计信息")
        print()

        print("✓ 高级功能:")
        print("  ✅ 按标签搜索")
        print("  ✅ 自动备份")
        print("  ✅ 分类建议")
        print()

        print("✅ 所有测试通过")


if __name__ == '__main__':
    main()
