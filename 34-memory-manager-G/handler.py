#!/usr/bin/env python3
"""
handler 模块
"""


"""
Memory Manager Skill Handler
Claude Code Skill 集成接口
"""
from typing import Dict, List, Optional, Any, Tuple, Union

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from memory_tool import ClaudeMemoryManager

LOGGER = logging.getLogger(__name__)


# 命令行参数说明：help="参数帮助文本"
def handle(args: list[str]) -> int:
    """处理命令行参数并执行记忆管理

    Args:
        args: 命令行参数列表（不包括脚本名）

    Returns:
        0 表示成功，非0 表示失败
    """
    if not args or args[0] in ['-h', '--help']:
        print_usage()
        return 0

    command = args[0]
    command_args = args[1:]

    manager = ClaudeMemoryManager()

    try:
        if command == 'show':
            print("📋 Claude Code 用户记忆（CLAUDE.md）：\n")
            print(manager.show_all())

        elif command == 'get':
            if not command_args:
                print("错误：请提供章节名称", file=sys.stderr)
                return 1
            content = manager.get_section(command_args[0])
            if content is None:
                print(f"未找到章节：{command_args[0]}", file=sys.stderr)
                return 1
            print(f"## {command_args[0]}\n\n{content}")

        elif command == 'add':
            if len(command_args) < 2:
                print("错误：请提供类别名称和内容", file=sys.stderr)
                return 1

            category = command_args[0]
            content = command_args[1].replace('\\n', '\n')
            tags = command_args[2:] if len(command_args) > 2 else None

            if manager.add_preference(category, content, tags=tags):
                print(f"✅ 已添加到类别 [{category}]")
            else:
                print(f"❌ 添加失败", file=sys.stderr)
                return 1

        elif command == 'search':
            if not command_args:
                print("错误：请提供搜索关键词", file=sys.stderr)
                return 1

            results = manager.search(command_args[0])
            if not results:
                print(f"未找到匹配 '{command_args[0]}' 的内容")
            else:
                print(f"找到 {len(results)} 个结果：\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. 章节: {result['section']}")
                    print(f"   匹配: {result['match']}")
                    print(f"   上下文: ...{result['context'][:100]}...")
                    print()

        elif command == 'list-tags':
            tags = manager.list_all_tags()
            if not tags:
                print("未找到任何标签")
            else:
                print(f"所有标签 ({len(tags)} 个)：")
                for tag in tags:
                    print(f"  #{tag}")

        elif command == 'backup':
            description = command_args[0] if command_args else "手动备份"
            backup_path = manager.create_backup(description)
            print(f"✅ 备份已创建: {backup_path}")

        elif command == 'list-backups':
            backups = manager.list_backups()
            if not backups:
                print("未找到备份文件")
            else:
                print(f"备份列表 ({len(backups)} 个)：\n")
                for i, backup in enumerate(backups, 1):
                    print(f"{i}. {backup['timestamp']}")
                    print(f"   描述: {backup.get('description', '无')}")
                    print(f"   路径: {backup['backup']}")
                    print()

        elif command == 'stats':
            stats = manager.get_statistics()
            print("📊 记忆统计信息：\n")
            print(f"  总行数: {stats['total_lines']}")
            print(f"  总字符数: {stats['total_characters']}")
            print(f"  章节数: {stats['total_sections']}")
            print(f"  标签数: {stats['total_tags']}")
            print(f"\n  章节列表:")
            for section in stats['sections']:
                print(f"    - {section}")

        else:
            print(f"未知命令: {command}", file=sys.stderr)
            print_usage()
            return 1

        return 0

    except Exception as e:
        LOGGER.error(f"❌ 执行失败: {e}")
        LOGGER.info("💡 建议: 请检查输入参数和环境配置")
        print(f"执行失败: {e}", file=sys.stderr)
        return 1


def print_usage() -> Any:
    """打印使用说明"""
    print("""
记忆管理工具 - 管理 Claude Code 用户记忆（CLAUDE.md）

用法:
    python handler.py <命令> [参数...]

命令:
    show                    显示所有用户记忆
    get <章节名>            获取特定章节内容
    add <类别> <内容> [标签...] 添加新的偏好
    search <关键词>         搜索记忆内容
    list-tags               列出所有标签
    backup [描述]           创建备份
    list-backups            列出所有备份
    stats                   显示统计信息
    -h, --help              显示此帮助信息

示例:
    # 显示所有记忆
    python handler.py show

    # 搜索记忆
    python handler.py search "中文"

    # 添加带标签的偏好
    python handler.py add "编码规范" "- 使用4空格缩进" style python

    # 创建备份
    python handler.py backup "重要修改前的备份"

    # 查看统计信息
    python handler.py stats
""")


if __name__ == '__main__':
    sys.exit(handle(sys.argv[1:]))
