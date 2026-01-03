#!/usr/bin/env python3
"""
memory_tool 模块
"""


"""
Claude Code 用户记忆管理工具
读取和修改 ~/.claude/CLAUDE.md 中的用户偏好（Claude Code 内置记忆系统）
支持备份、搜索、分类和标签功能
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json
import shutil


class MemoryBackup:
    """记忆备份管理器"""

    def __init__(self, backup_dir: Optional[Path] = None) -> None:
        """初始化备份管理器

        Args:
            backup_dir: 备份目录，默认为 ~/.claude/backups
        """
        if backup_dir:
            self.backup_dir = backup_dir
        else:
            self.backup_dir = Path.home() / '.claude' / 'backups'

        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, source_file: Path, description: str = "") -> str:
        """创建备份

        Args:
            source_file: 源文件路径
            description: 备份描述

        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"CLAUDE_{timestamp}.md"
        backup_path = self.backup_dir / backup_name

        # 复制文件
        shutil.copy2(source_file, backup_path)

        # 保存元数据
        metadata = {
            'timestamp': timestamp,
            'description': description,
            'source': str(source_file),
            'backup': str(backup_path)
        }

        metadata_path = self.backup_dir / f"CLAUDE_{timestamp}.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return str(backup_path)

    def list_backups(self) -> List[Dict[str, str]]:
        """列出所有备份

        Returns:
            备份列表，每个备份包含时间戳、描述等信息
        """
        backups = []
        for metadata_file in sorted(self.backup_dir.glob("CLAUDE_*.json"), reverse=True):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    backups.append(metadata)
            except:
                pass

        return backups

    def restore_backup(self, backup_file: str, target_file: Path) -> bool:
        """恢复备份

        Args:
            backup_file: 备份文件路径
            target_file: 目标文件路径

        Returns:
            是否成功恢复
        """
        try:
            # 创建当前版本的备份
            self.create_backup(target_file, "Before restore")

            # 恢复备份
            shutil.copy2(backup_file, target_file)
            return True
        except Exception as e:
            print(f"恢复失败: {e}", file=sys.stderr)
            return False

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """清理旧备份，保留最新的N个

        Args:
            keep_count: 保留的备份数量

        Returns:
            删除的备份数量
        """
        backups = self.list_backups()
        deleted_count = 0

        for backup in backups[keep_count:]:
            try:
                # 删除备份文件
                backup_path = Path(backup['backup'])
                if backup_path.exists():
                    backup_path.unlink()

                # 删除元数据文件
                metadata_path = backup_path.with_suffix('.json')
                if metadata_path.exists():
                    metadata_path.unlink()

                deleted_count += 1
            except:
                pass

        return deleted_count


class MemorySearch:
    """记忆搜索引擎"""

    def __init__(self, content: str) -> None:
        """初始化搜索引擎

        Args:
            content: CLAUDE.md 文件内容
        """
        self.content = content
        self.sections = self._parse_sections()

    def _parse_sections(self) -> Dict[str, str]:
        """解析所有章节"""
        sections = {}
        pattern = r'^##\s+(.+?)\s*$(.*?)(?=^##\s|\Z)'

        for match in re.finditer(pattern, self.content, re.MULTILINE | re.DOTALL):
            section_name = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_name] = section_content

        return sections

    def search(self, query: str, case_sensitive: bool = False) -> List[Dict[str, str]]:
        """搜索记忆内容

        Args:
            query: 搜索关键词
            case_sensitive: 是否区分大小写

        Returns:
            搜索结果列表
        """
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        for section_name, section_content in self.sections.items():
            # 在章节名中搜索
            if re.search(query, section_name, flags):
                results.append({
                    'type': 'section_name',
                    'section': section_name,
                    'match': section_name,
                    'context': section_content[:200]
                })

            # 在章节内容中搜索
            matches = list(re.finditer(query, section_content, flags))
            for match in matches:
                # 提取上下文
                start = max(0, match.start() - 50)
                end = min(len(section_content), match.end() + 50)
                context = section_content[start:end]

                results.append({
                    'type': 'content',
                    'section': section_name,
                    'match': match.group(),
                    'context': context
                })

        return results

    def search_by_tag(self, tag: str) -> List[Dict[str, str]]:
        """按标签搜索

        Args:
            tag: 标签名（如 #important）

        Returns:
            包含该标签的内容
        """
        tag_pattern = f'#{tag}'
        return self.search(tag_pattern, case_sensitive=False)


class MemoryOrganizer:
    """记忆组织器 - 分类和标签管理"""

    def __init__(self) -> None:
        self.categories = {
            '语言偏好': ['language', 'output', 'communication'],
            '编码规范': ['code', 'style', 'format', 'convention'],
            '工具配置': ['tool', 'config', 'setting'],
            '工作习惯': ['workflow', 'habit', 'preference'],
            '项目设置': ['project', 'repository', 'git']
        }

    def suggest_category(self, content: str) -> str:
        """根据内容建议分类

        Args:
            content: 内容文本

        Returns:
            建议的分类名称
        """
        content_lower = content.lower()
        scores = {}

        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            scores[category] = score

        # 返回得分最高的分类
        best_category = max(scores.items(), key=lambda x: x[1])
        return best_category[0] if best_category[1] > 0 else '其他设置'

    def add_tags(self, content: str, tags: List[str]) -> str:
        """为内容添加标签

        Args:
            content: 原始内容
            tags: 标签列表

        Returns:
            添加标签后的内容
        """
        # 在内容末尾添加标签
        tag_line = ' '.join(f'#{tag}' for tag in tags)
        return f"{content}\n\n{tag_line}"

    def extract_tags(self, content: str) -> List[str]:
        """从内容中提取所有标签

        Args:
            content: 内容文本

        Returns:
            标签列表
        """
        # 匹配 #标签 格式
        pattern = r'#(\w+)'
        return re.findall(pattern, content)


class ClaudeMemoryManager:
    """管理 Claude Code 内置用户记忆系统（CLAUDE.md）"""

    def __init__(self, claude_md_path: Optional[str] = None) -> None:
        """初始化记忆管理器

        Args:
            claude_md_path: CLAUDE.md 文件路径，默认为 ~/.claude/CLAUDE.md
        """
        if claude_md_path:
            self.claude_md_path = Path(claude_md_path)
        else:
            home = Path.home()
            self.claude_md_path = home / '.claude' / 'CLAUDE.md'

        self.content = self._load_content()
        self.backup_manager = MemoryBackup()
        self.search_engine = MemorySearch(self.content)
        self.organizer = MemoryOrganizer()

    def _load_content(self) -> str:
        """加载 CLAUDE.md 文件内容"""
        if not self.claude_md_path.exists():
            # 如果文件不存在，创建默认内容
            self.claude_md_path.parent.mkdir(parents=True, exist_ok=True)
            default_content = """# 用户偏好设置

## 语言偏好

- 默认输出语言：中文

## 输出风格

- 清晰、简洁、专业
"""
            self._save_content(default_content)
            return default_content

        try:
            with open(self.claude_md_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"错误：无法读取 CLAUDE.md: {e}", file=sys.stderr)
            return ""

    def _save_content(self, content: str, create_backup: bool = True) -> bool:
        """保存 CLAUDE.md 文件内容

        Args:
            content: 要保存的内容
            create_backup: 是否创建备份

        Returns:
            是否保存成功
        """
        try:
            # 创建备份
            if create_backup and self.claude_md_path.exists():
                self.backup_manager.create_backup(
                    self.claude_md_path,
                    f"Auto backup before save at {datetime.now().isoformat()}"
                )

            # 保存新内容
            with open(self.claude_md_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 更新内部状态
            self.content = content
            self.search_engine = MemorySearch(content)

            return True
        except Exception as e:
            print(f"错误：无法保存 CLAUDE.md: {e}", file=sys.stderr)
            return False

    def show_all(self) -> str:
        """显示所有用户偏好"""
        return self.content

    def get_section(self, section_name: str) -> Optional[str]:
        """获取特定章节内容

        Args:
            section_name: 章节名称（如 "语言偏好", "输出风格"）

        Returns:
            章节内容，如果不存在返回 None
        """
        pattern = rf'^##\s+{re.escape(section_name)}\s*$(.*?)(?=^##\s|\Z)'
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL)

        if match:
            return match.group(1).strip()
        return None

    def add_preference(self, category: str, preference: str, tags: Optional[List[str]] = None) -> bool:
        """添加用户偏好到指定类别

        Args:
            category: 类别名称（如 "语言偏好", "输出风格", "编码风格"等）
            preference: 偏好内容（Markdown 格式）
            tags: 可选的标签列表

        Returns:
            是否成功保存
        """
        # 添加标签
        if tags:
            preference = self.organizer.add_tags(preference, tags)

        # 检查类别是否存在
        section_pattern = rf'^##\s+{re.escape(category)}\s*$'

        if re.search(section_pattern, self.content, re.MULTILINE):
            # 类别存在，在该类别下添加内容
            lines = self.content.split('\n')
            new_lines = []
            in_target_section = False
            section_inserted = False

            for i, line in enumerate(lines):
                new_lines.append(line)

                if re.match(section_pattern, line):
                    in_target_section = True
                    continue

                if in_target_section:
                    if line.startswith('##') or i == len(lines) - 1:
                        new_lines.insert(-1, f"\n{preference}")
                        section_inserted = True
                        in_target_section = False

            if not section_inserted and in_target_section:
                new_lines.append(f"\n{preference}")

            new_content = '\n'.join(new_lines)
        else:
            # 类别不存在，创建新类别
            if not self.content.endswith('\n\n'):
                self.content += '\n\n'

            new_content = self.content + f"""## {category}

{preference}
"""

        return self._save_content(new_content)

    def update_preference(self, category: str, new_content: str) -> bool:
        """更新指定类别的全部内容

        Args:
            category: 类别名称
            new_content: 新的内容

        Returns:
            是否成功保存
        """
        section_pattern = rf'^##\s+{re.escape(category)}\s*$(.*?)(?=^##\s|\Z)'

        if not re.search(section_pattern, self.content, re.MULTILINE | re.DOTALL):
            # 类别不存在，添加新类别
            return self.add_preference(category, new_content)

        # 替换该类别的内容
        replacement = f"## {category}\n\n{new_content}\n"
        new_content_str = re.sub(
            section_pattern,
            replacement,
            self.content,
            flags=re.MULTILINE | re.DOTALL
        )

        return self._save_content(new_content_str)

    def delete_section(self, section_name: str) -> bool:
        """删除指定章节

        Args:
            section_name: 章节名称

        Returns:
            是否成功删除
        """
        section_pattern = rf'^##\s+{re.escape(section_name)}\s*$(.*?)(?=^##\s|\Z)'

        if not re.search(section_pattern, self.content, re.MULTILINE | re.DOTALL):
            return False

        new_content = re.sub(
            section_pattern,
            '',
            self.content,
            flags=re.MULTILINE | re.DOTALL
        ).strip() + '\n'

        return self._save_content(new_content)

    def search(self, query: str, case_sensitive: bool = False) -> List[Dict[str, str]]:
        """搜索记忆内容

        Args:
            query: 搜索关键词
            case_sensitive: 是否区分大小写

        Returns:
            搜索结果列表
        """
        return self.search_engine.search(query, case_sensitive)

    def search_by_tag(self, tag: str) -> List[Dict[str, str]]:
        """按标签搜索

        Args:
            tag: 标签名

        Returns:
            搜索结果
        """
        return self.search_engine.search_by_tag(tag)

    def list_all_tags(self) -> List[str]:
        """列出所有标签

        Returns:
            所有标签的列表
        """
        all_tags = set()
        for section_content in self.search_engine.sections.values():
            tags = self.organizer.extract_tags(section_content)
            all_tags.update(tags)

        return sorted(all_tags)

    def create_backup(self, description: str = "") -> str:
        """创建备份

        Args:
            description: 备份描述

        Returns:
            备份文件路径
        """
        return self.backup_manager.create_backup(self.claude_md_path, description)

    def list_backups(self) -> List[Dict[str, str]]:
        """列出所有备份"""
        return self.backup_manager.list_backups()

    def restore_backup(self, backup_file: str) -> bool:
        """恢复备份

        Args:
            backup_file: 备份文件路径

        Returns:
            是否成功恢复
        """
        success = self.backup_manager.restore_backup(backup_file, self.claude_md_path)
        if success:
            self.content = self._load_content()
            self.search_engine = MemorySearch(self.content)
        return success

    def get_path(self) -> str:
        """获取 CLAUDE.md 文件路径"""
        return str(self.claude_md_path)

    def get_statistics(self) -> Dict[str, Any]:
        """获取记忆统计信息

        Returns:
            统计信息字典
        """
        lines = self.content.split('\n')
        sections = self.search_engine.sections
        all_tags = self.list_all_tags()

        return {
            'total_lines': len(lines),
            'total_sections': len(sections),
            'total_tags': len(all_tags),
            'total_characters': len(self.content),
            'sections': list(sections.keys()),
            'tags': all_tags,
            'last_modified': datetime.fromtimestamp(
                self.claude_md_path.stat().st_mtime
            ).isoformat() if self.claude_md_path.exists() else None
        }


def main() -> Any:
    try:
        """命令行接口"""
        import argparse
    except Exception as e:
        logger.error(f"执行出错: {e}")
        return 1

    parser = argparse.ArgumentParser(
        description='Claude Code 用户记忆管理工具（操作 CLAUDE.md）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 显示所有用户记忆
  python memory_tool.py show

  # 获取特定章节内容
  python memory_tool.py get "语言偏好"

  # 添加新的偏好到"语言偏好"类别
  python memory_tool.py add "语言偏好" "- 所有输出使用简体中文"

  # 添加带标签的偏好
  python memory_tool.py add "编码规范" "- 使用4空格缩进" --tags style python

  # 搜索记忆内容
  python memory_tool.py search "中文"

  # 按标签搜索
  python memory_tool.py search-tag important

  # 列出所有标签
  python memory_tool.py list-tags

  # 创建备份
  python memory_tool.py backup "手动备份"

  # 列出所有备份
  python memory_tool.py list-backups

  # 恢复备份
  python memory_tool.py restore /path/to/backup.md

  # 显示统计信息
  python memory_tool.py stats
        """
    )

    parser.add_argument('command',
                       choices=['show', 'get', 'add', 'update', 'delete', 'path',
                               'search', 'search-tag', 'list-tags',
                               'backup', 'list-backups', 'restore', 'stats'],
                       help='操作命令')
    parser.add_argument('args', nargs='*', help='命令参数')
    parser.add_argument('--tags', nargs='+', help='标签列表（用于 add 命令）')

    args = parser.parse_args()

    manager = ClaudeMemoryManager()

    if args.command == 'show':
        print("📋 Claude Code 用户记忆（CLAUDE.md）：\n")
        print(manager.show_all())

    elif args.command == 'get':
        if not args.args:
            print("错误：请提供章节名称", file=sys.stderr)
            sys.exit(1)

        category = args.args[0]
        content = manager.get_section(category)
        if content is None:
            print(f"未找到章节：{category}", file=sys.stderr)
            sys.exit(1)

        print(f"## {category}\n\n{content}")

    elif args.command == 'add':
        if len(args.args) < 2:
            print("错误：请提供类别名称和内容", file=sys.stderr)
            sys.exit(1)

        category = args.args[0]
        content = args.args[1].replace('\\n', '\n')

        if manager.add_preference(category, content, tags=args.tags):
            print(f"✅ 已添加到类别 [{category}]")
        else:
            print(f"❌ 添加失败", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'update':
        if len(args.args) < 2:
            print("错误：请提供类别名称和内容", file=sys.stderr)
            sys.exit(1)

        category = args.args[0]
        content = args.args[1].replace('\\n', '\n')

        if manager.update_preference(category, content):
            print(f"✅ 已更新类别 [{category}]")
        else:
            print(f"❌ 更新失败", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'delete':
        if not args.args:
            print("错误：请提供章节名称", file=sys.stderr)
            sys.exit(1)

        category = args.args[0]
        if manager.delete_section(category):
            print(f"✅ 已删除章节：{category}")
        else:
            print(f"❌ 删除失败或章节不存在", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'search':
        if not args.args:
            print("错误：请提供搜索关键词", file=sys.stderr)
            sys.exit(1)

        query = args.args[0]
        results = manager.search(query)

        if not results:
            print(f"未找到匹配 '{query}' 的内容")
            sys.exit(0)

        print(f"找到 {len(results)} 个结果：\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. 章节: {result['section']}")
            print(f"   类型: {result['type']}")
            print(f"   匹配: {result['match']}")
            print(f"   上下文: ...{result['context']}...")
            print()

    elif args.command == 'search-tag':
        if not args.args:
            print("错误：请提供标签名", file=sys.stderr)
            sys.exit(1)

        tag = args.args[0]
        results = manager.search_by_tag(tag)

        if not results:
            print(f"未找到标签 '#{tag}' 的内容")
            sys.exit(0)

        print(f"找到 {len(results)} 个带标签 #{tag} 的结果：\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. 章节: {result['section']}")
            print(f"   {result['context']}")
            print()

    elif args.command == 'list-tags':
        tags = manager.list_all_tags()
        if not tags:
            print("未找到任何标签")
        else:
            print(f"所有标签 ({len(tags)} 个)：\n")
            for tag in tags:
                print(f"  #{tag}")

    elif args.command == 'backup':
        description = args.args[0] if args.args else "手动备份"
        backup_path = manager.create_backup(description)
        print(f"✅ 备份已创建: {backup_path}")

    elif args.command == 'list-backups':
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

    elif args.command == 'restore':
        if not args.args:
            print("错误：请提供备份文件路径", file=sys.stderr)
            sys.exit(1)

        backup_file = args.args[0]
        if manager.restore_backup(backup_file):
            print(f"✅ 已恢复备份: {backup_file}")
        else:
            print(f"❌ 恢复失败", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'stats':
        stats = manager.get_statistics()
        print("📊 记忆统计信息：\n")
        print(f"  总行数: {stats['total_lines']}")
        print(f"  总字符数: {stats['total_characters']}")
        print(f"  章节数: {stats['total_sections']}")
        print(f"  标签数: {stats['total_tags']}")
        print(f"  最后修改: {stats['last_modified']}")
        print(f"\n  章节列表:")
        for section in stats['sections']:
            print(f"    - {section}")
        if stats['tags']:
            print(f"\n  标签列表:")
            for tag in stats['tags']:
                print(f"    #{tag}")

    elif args.command == 'path':
        print(f"📁 CLAUDE.md 文件路径：{manager.get_path()}")


if __name__ == '__main__':
    main()
