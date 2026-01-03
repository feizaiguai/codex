#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================
Skill List Maintainer - 技能列表维护工具
功能：管理Claude Code技能路由系统的skills.json配置文件
支持：添加、更新、删除、查看技能配置
================================================================
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class SkillMaintainer:
    """技能列表维护器类"""

    def __init__(self, skills_json_path=None):
        """初始化维护器"""
        if skills_json_path is None:
            # 默认路径：上级目录的skill-router/skills.json
            current_dir = Path(__file__).parent
            skills_json_path = current_dir.parent / "skill-router" / "skills.json"

        self.skills_json_path = Path(skills_json_path)
        self.backup_dir = self.skills_json_path.parent / "backups"
        self.skills_data = {}
        self.config = {}

        # 确保备份目录存在
        self.backup_dir.mkdir(exist_ok=True)

        # 加载配置
        self.load_config()

    def load_config(self):
        """加载技能配置文件"""
        if not self.skills_json_path.exists():
            print(f"⚠️ 配置文件不存在，将创建新文件: {self.skills_json_path}")
            self.skills_data = {}
            self.config = {
                "matchMode": "keyword",
                "caseSensitive": False,
                "enablePatternMatch": True,
                "defaultSkill": None,
                "logMatches": True,
            }
            self.save_config()
            return

        try:
            with open(self.skills_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.skills_data = data.get("skills", {})
                self.config = data.get("config", {})

            print(f"✅ 成功加载 {len(self.skills_data)} 个技能配置")
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            raise
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            raise

    def save_config(self):
        """保存技能配置文件"""
        # 先备份
        self.backup_config()

        # 准备数据
        data = {
            "version": "1.0.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "skills": self.skills_data,
            "config": self.config,
        }

        try:
            # 写入文件
            with open(self.skills_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✅ 配置已保存: {self.skills_json_path}")
            return True
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return False

    def backup_config(self):
        """备份配置文件"""
        if not self.skills_json_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"skills_{timestamp}.json"

        try:
            shutil.copy2(self.skills_json_path, backup_path)
            print(f"📦 已备份到: {backup_path}")

            # 清理旧备份（只保留最近10个）
            self.cleanup_old_backups(keep=10)

        except Exception as e:
            print(f"⚠️ 备份失败: {e}")

    def cleanup_old_backups(self, keep=10):
        """清理旧备份文件"""
        try:
            backups = sorted(
                self.backup_dir.glob("skills_*.json"), key=lambda p: p.stat().st_mtime
            )

            # 删除旧备份
            for backup in backups[:-keep]:
                backup.unlink()
                print(f"🗑️ 删除旧备份: {backup.name}")

        except Exception as e:
            print(f"⚠️ 清理备份失败: {e}")

    def validate_skill_data(self, skill_name: str, skill_data: Dict) -> bool:
        """
        验证技能数据格式
        :param skill_name: 技能名称
        :param skill_data: 技能数据
        :return: 是否有效
        """
        required_fields = ["type", "enforcement", "priority", "description"]

        # 检查必需字段
        for field in required_fields:
            if field not in skill_data:
                print(f"❌ 缺少必需字段: {field}")
                return False

        # 验证type
        valid_types = ["domain", "utility", "general"]
        if skill_data["type"] not in valid_types:
            print(f"❌ 无效的type: {skill_data['type']}，必须是: {valid_types}")
            return False

        # 验证priority
        valid_priorities = ["high", "medium", "low"]
        if skill_data["priority"] not in valid_priorities:
            print(
                f"❌ 无效的priority: {skill_data['priority']}，必须是: {valid_priorities}"
            )
            return False

        # 验证enforcement
        valid_enforcements = ["suggest", "require", "optional"]
        if skill_data["enforcement"] not in valid_enforcements:
            print(
                f"❌ 无效的enforcement: {skill_data['enforcement']}，必须是: {valid_enforcements}"
            )
            return False

        # 检查promptTriggers
        if "promptTriggers" not in skill_data:
            print("⚠️ 缺少promptTriggers字段，将使用空触发器")
            skill_data["promptTriggers"] = {"keywords": [], "patterns": []}

        return True

    def add_skill(
        self,
        skill_name: str,
        skill_type: str = "domain",
        priority: str = "medium",
        description: str = "",
        keywords: List[str] = None,
        patterns: List[str] = None,
        enforcement: str = "suggest",
    ) -> bool:
        """
        添加新技能
        :param skill_name: 技能名称
        :param skill_type: 类型（domain/utility/general）
        :param priority: 优先级（high/medium/low）
        :param description: 描述
        :param keywords: 触发关键词列表
        :param patterns: 正则表达式模式列表
        :param enforcement: 强制模式
        :return: 是否成功
        """
        if skill_name in self.skills_data:
            print(f"⚠️ 技能已存在: {skill_name}，请使用update_skill更新")
            return False

        # 创建技能数据
        skill_data = {
            "type": skill_type,
            "enforcement": enforcement,
            "priority": priority,
            "description": description,
            "promptTriggers": {
                "keywords": keywords or [],
                "patterns": patterns or [],
            },
        }

        # 验证数据
        if not self.validate_skill_data(skill_name, skill_data):
            return False

        # 添加技能
        self.skills_data[skill_name] = skill_data

        # 保存
        if self.save_config():
            print(f"✅ 成功添加技能: {skill_name}")
            return True

        return False

    def update_skill(
        self,
        skill_name: str,
        skill_type: Optional[str] = None,
        priority: Optional[str] = None,
        description: Optional[str] = None,
        add_keywords: List[str] = None,
        remove_keywords: List[str] = None,
        add_patterns: List[str] = None,
        remove_patterns: List[str] = None,
        enforcement: Optional[str] = None,
    ) -> bool:
        """
        更新现有技能
        :param skill_name: 技能名称
        :param skill_type: 新类型（可选）
        :param priority: 新优先级（可选）
        :param description: 新描述（可选）
        :param add_keywords: 要添加的关键词
        :param remove_keywords: 要删除的关键词
        :param add_patterns: 要添加的模式
        :param remove_patterns: 要删除的模式
        :param enforcement: 新的强制模式（可选）
        :return: 是否成功
        """
        if skill_name not in self.skills_data:
            print(f"❌ 技能不存在: {skill_name}")
            return False

        skill_data = self.skills_data[skill_name]

        # 更新字段
        if skill_type is not None:
            skill_data["type"] = skill_type

        if priority is not None:
            skill_data["priority"] = priority

        if description is not None:
            skill_data["description"] = description

        if enforcement is not None:
            skill_data["enforcement"] = enforcement

        # 更新关键词
        if add_keywords:
            keywords = skill_data.get("promptTriggers", {}).get("keywords", [])
            for kw in add_keywords:
                if kw not in keywords:
                    keywords.append(kw)
            skill_data.setdefault("promptTriggers", {})["keywords"] = keywords

        if remove_keywords:
            keywords = skill_data.get("promptTriggers", {}).get("keywords", [])
            keywords = [kw for kw in keywords if kw not in remove_keywords]
            skill_data.setdefault("promptTriggers", {})["keywords"] = keywords

        # 更新模式
        if add_patterns:
            patterns = skill_data.get("promptTriggers", {}).get("patterns", [])
            for p in add_patterns:
                if p not in patterns:
                    patterns.append(p)
            skill_data.setdefault("promptTriggers", {})["patterns"] = patterns

        if remove_patterns:
            patterns = skill_data.get("promptTriggers", {}).get("patterns", [])
            patterns = [p for p in patterns if p not in remove_patterns]
            skill_data.setdefault("promptTriggers", {})["patterns"] = patterns

        # 验证数据
        if not self.validate_skill_data(skill_name, skill_data):
            return False

        # 保存
        if self.save_config():
            print(f"✅ 成功更新技能: {skill_name}")
            return True

        return False

    def remove_skill(self, skill_name: str) -> bool:
        """
        删除技能
        :param skill_name: 技能名称
        :return: 是否成功
        """
        if skill_name not in self.skills_data:
            print(f"❌ 技能不存在: {skill_name}")
            return False

        # 删除技能
        del self.skills_data[skill_name]

        # 保存
        if self.save_config():
            print(f"✅ 成功删除技能: {skill_name}")
            return True

        return False

    def list_skills(self, skill_name: Optional[str] = None):
        """
        列出技能
        :param skill_name: 特定技能名称（可选）
        """
        if skill_name:
            # 显示特定技能
            if skill_name in self.skills_data:
                print(f"\n📍 技能: {skill_name}")
                print("-" * 50)
                self._print_skill_info(skill_name, self.skills_data[skill_name])
            else:
                print(f"❌ 技能不存在: {skill_name}")
        else:
            # 显示所有技能
            print(f"\n📋 共有 {len(self.skills_data)} 个技能:\n")

            # 按优先级分组
            by_priority = {"high": [], "medium": [], "low": []}

            for name, data in self.skills_data.items():
                priority = data.get("priority", "low")
                by_priority[priority].append((name, data))

            # 输出
            for priority in ["high", "medium", "low"]:
                if by_priority[priority]:
                    print(f"⭐ {priority.upper()} 优先级:")
                    for name, data in by_priority[priority]:
                        self._print_skill_info(name, data, indent=2)
                    print()

    def _print_skill_info(self, name: str, data: Dict, indent: int = 0):
        """打印技能信息"""
        prefix = " " * indent
        print(f"{prefix}• {name}")
        print(f"{prefix}  类型: {data.get('type', 'N/A')}")
        print(f"{prefix}  优先级: {data.get('priority', 'N/A')}")
        print(f"{prefix}  描述: {data.get('description', 'N/A')}")

        triggers = data.get("promptTriggers", {})
        keywords = triggers.get("keywords", [])
        if keywords:
            print(f"{prefix}  关键词: {', '.join(keywords)}")

        patterns = triggers.get("patterns", [])
        if patterns:
            print(f"{prefix}  模式: {len(patterns)} 个正则表达式")

    def parse_natural_language_command(self, command: str):
        """
        解析自然语言命令
        :param command: 用户输入的命令
        """
        command = command.strip()

        # 添加技能
        if "添加技能" in command or "新建技能" in command:
            self._parse_add_command(command)

        # 更新技能
        elif "更新技能" in command or "修改技能" in command:
            self._parse_update_command(command)

        # 删除技能
        elif "删除技能" in command or "移除技能" in command:
            self._parse_remove_command(command)

        # 查看技能
        elif "显示" in command or "查看" in command or "列出" in command:
            self._parse_list_command(command)

        else:
            print("❌ 无法识别的命令")
            print("支持的命令:")
            print("  - 添加技能: <技能名称>, 关键词: <关键词列表>")
            print("  - 更新技能: <技能名称>, 添加关键词: <关键词>")
            print("  - 删除技能: <技能名称>")
            print("  - 显示所有技能")

    def _parse_add_command(self, command: str):
        """解析添加命令"""
        # 提取技能名称
        name_match = re.search(r"[添加新建]技能[:：]?\s*([^,，\n]+)", command)
        if not name_match:
            print("❌ 无法提取技能名称")
            return

        skill_name = name_match.group(1).strip()

        # 提取关键词
        keywords_match = re.search(r"关键词[:：]?\s*([^,，\n]+)", command)
        keywords = []
        if keywords_match:
            keywords_str = keywords_match.group(1).strip()
            keywords = [kw.strip() for kw in re.split(r"[,，]", keywords_str)]

        # 提取描述
        desc_match = re.search(r"描述[:：]?\s*([^\n]+)", command)
        description = desc_match.group(1).strip() if desc_match else ""

        # 提取优先级
        priority = "medium"
        if "高优先级" in command or "priority:high" in command.lower():
            priority = "high"
        elif "低优先级" in command or "priority:low" in command.lower():
            priority = "low"

        # 提取类型
        skill_type = "domain"
        if "工具" in command or "utility" in command.lower():
            skill_type = "utility"
        elif "通用" in command or "general" in command.lower():
            skill_type = "general"

        # 添加技能
        self.add_skill(
            skill_name=skill_name,
            skill_type=skill_type,
            priority=priority,
            description=description,
            keywords=keywords,
        )

    def _parse_update_command(self, command: str):
        """解析更新命令"""
        # 提取技能名称
        name_match = re.search(r"[更新修改]技能[:：]?\s*([^,，\n]+)", command)
        if not name_match:
            print("❌ 无法提取技能名称")
            return

        skill_name = name_match.group(1).strip()

        # 提取要添加的关键词
        add_kw_match = re.search(r"添加关键词[:：]?\s*([^\n]+)", command)
        add_keywords = []
        if add_kw_match:
            kw_str = add_kw_match.group(1).strip()
            add_keywords = [kw.strip() for kw in re.split(r"[,，]", kw_str)]

        # 提取要删除的关键词
        remove_kw_match = re.search(r"删除关键词[:：]?\s*([^\n]+)", command)
        remove_keywords = []
        if remove_kw_match:
            kw_str = remove_kw_match.group(1).strip()
            remove_keywords = [kw.strip() for kw in re.split(r"[,，]", kw_str)]

        # 提取新描述
        desc_match = re.search(r"[修改新]描述[:：]?\s*([^\n]+)", command)
        description = desc_match.group(1).strip() if desc_match else None

        # 更新技能
        self.update_skill(
            skill_name=skill_name,
            description=description,
            add_keywords=add_keywords if add_keywords else None,
            remove_keywords=remove_keywords if remove_keywords else None,
        )

    def _parse_remove_command(self, command: str):
        """解析删除命令"""
        # 提取技能名称
        name_match = re.search(r"[删除移除]技能[:：]?\s*([^\n,，]+)", command)
        if not name_match:
            print("❌ 无法提取技能名称")
            return

        skill_name = name_match.group(1).strip()

        # 删除技能
        self.remove_skill(skill_name)

    def _parse_list_command(self, command: str):
        """解析查看命令"""
        # 检查是否指定了特定技能
        name_match = re.search(r"[查看显示列出]技能[:：]?\s*([^\n,，]+)", command)

        if name_match:
            skill_name = name_match.group(1).strip()
            self.list_skills(skill_name)
        else:
            self.list_skills()


def main():
    """主函数"""
    import sys

    print("=" * 60)
    print("Claude Code Skill List Maintainer")
    print("技能列表维护工具")
    print("=" * 60)
    print()

    # 创建维护器
    maintainer = SkillMaintainer()

    # 如果有命令行参数，则作为命令执行
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        maintainer.parse_natural_language_command(command)
    else:
        # 交互模式
        print("进入交互模式（输入 'exit' 或 'quit' 退出）")
        print()

        while True:
            try:
                command = input("💬 请输入命令: ").strip()

                if command.lower() in ["exit", "quit", "退出"]:
                    print("👋 再见！")
                    break

                if not command:
                    continue

                maintainer.parse_natural_language_command(command)
                print()

            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
