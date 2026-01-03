"""
DESIGN_DRAFT.md 解析器
解析01-spec-explorer输出的设计草稿文档（V2.0格式）

增强特性（P1-1）：
- 容错机制：支持宽松匹配
- 详细错误提示：指明具体哪一章解析失败
- 防御性编程：处理格式变化
"""
import re
from typing import Dict, List, Optional, Tuple
from core.models import DesignDraft


class DesignDraftParser:
    """设计草稿解析器（适配01-spec-explorer V2.0输出格式）"""

    def __init__(self):
        """初始化解析器"""
        self.content = ""
        self.chapters = {}

    def parse_file(self, file_path: str) -> DesignDraft:
        """
        解析DESIGN_DRAFT.md文件

        Args:
            file_path: 文件路径

        Returns:
            DesignDraft对象

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 解析失败
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"设计草稿文件不存在: {file_path}")
        except Exception as e:
            raise ValueError(f"读取文件失败: {e}")

        return self.parse_content(self.content)

    def parse_content(self, content: str) -> DesignDraft:
        """
        解析Markdown内容

        Args:
            content: Markdown文本

        Returns:
            DesignDraft对象
        """
        self.content = content

        # 第一步：分割章节（适配新格式）
        try:
            self._split_chapters()
        except Exception as e:
            raise ValueError(f"章节分割失败: {e}")

        # 第二步：解析各章节
        try:
            project_name, core_value, target_users, user_scale = self._parse_chapter1()
        except Exception as e:
            raise ValueError(f"第1章（需求概览）解析失败: {e}\n请检查Markdown格式")

        try:
            features = self._parse_chapter2()
        except Exception as e:
            raise ValueError(f"第2章（Impact Mapping）解析失败: {e}\n请检查功能列表格式")

        try:
            user_stories, workflows = self._parse_chapter3()
        except Exception as e:
            raise ValueError(f"第3章（Flow Modeling）解析失败: {e}\n请检查用户故事格式")

        try:
            entities, value_objects, aggregates, contexts = self._parse_chapter4()
        except Exception as e:
            raise ValueError(f"第4章（Domain Modeling）解析失败: {e}\n请检查领域模型格式")

        # 第5章（BDD/ATDD场景）是可选的，不作为必需数据

        # 构建DesignDraft对象
        return DesignDraft(
            project_name=project_name,
            core_value=core_value,
            target_users=target_users,
            user_scale=user_scale,
            features=features,
            entities=entities,
            value_objects=value_objects,
            aggregates=aggregates,
            contexts=contexts,
            user_stories=user_stories,
            workflows=workflows
        )

    def _split_chapters(self):
        """
        分割章节（适配01-spec-explorer V2.0格式）
        使用宽松匹配，支持多种标题格式
        """
        chapter_patterns = {
            "需求概览": r"##\s*第?1章[：:]\s*需求概览.*?\n(.*?)(?=##\s*第?[2-9]章|$)",
            "Impact Mapping": r"##\s*第?2章[：:]\s*Impact\s*Mapping.*?\n(.*?)(?=##\s*第?[3-9]章|$)",
            "Flow Modeling": r"##\s*第?3章[：:]\s*Flow\s*Modeling.*?\n(.*?)(?=##\s*第?[4-9]章|$)",
            "Domain Modeling": r"##\s*第?4章[：:]\s*Domain\s*Modeling.*?\n(.*?)(?=##\s*第?[5-9]章|##\s*附录|$)",
            "BDD/ATDD": r"##\s*第?5章[：:]\s*BDD/ATDD.*?\n(.*?)(?=##\s*附录|$)"
        }

        for title, pattern in chapter_patterns.items():
            match = re.search(pattern, self.content, re.DOTALL | re.IGNORECASE)

            if match:
                self.chapters[title] = match.group(1).strip()
            else:
                # BDD/ATDD 章节是可选的
                if title != "BDD/ATDD":
                    raise ValueError(
                        f"未找到章节: {title}\n"
                        f"请确认Markdown文档包含标题 '## 第X章：{title}'"
                    )

    def _parse_chapter1(self) -> Tuple[str, str, str, str]:
        """
        解析第1章：需求概览

        Returns:
            (project_name, core_value, target_users, user_scale)
        """
        content = self.chapters.get("需求概览", "")

        # 提取项目名称（从文档标题或元信息中）
        # 尝试从标题提取
        title_match = re.search(r"#\s*(.+?)\s+设计草稿", self.content, re.MULTILINE)
        if title_match:
            project_name = title_match.group(1).strip()
        else:
            # 从元信息提取
            meta_match = re.search(r"项目名称[：:]\s*(.+)", self.content, re.MULTILINE)
            if meta_match:
                project_name = meta_match.group(1).strip()
            else:
                raise ValueError("未找到项目名称字段")

        # 提取核心价值（从核心问题或价值主张提取）
        core_value = self._extract_field(content, r"###\s*核心问题.*?\n(.+)")
        if not core_value:
            core_value = self._extract_field(content, r"###\s*价值主张.*?\n(.+)")
        if not core_value:
            core_value = project_name  # 默认使用项目名称

        # 提取目标用户
        target_users = self._extract_field(content, r"###\s*目标用户.*?\n(.+)")
        if not target_users:
            target_users = "通用用户"

        # 提取用户规模（从价值主张或核心问题中推断）
        user_scale = self._infer_user_scale(content)

        return project_name, core_value, target_users, user_scale

    def _parse_chapter2(self) -> List[Dict[str, str]]:
        """
        解析第2章：Impact Mapping（目标与价值）

        Returns:
            功能列表（从交付物映射中提取）
        """
        content = self.chapters.get("Impact Mapping", "")
        features = []

        # 从交付物映射中提取功能
        deliverable_section = self._extract_section(content, "交付物映射")
        if deliverable_section:
            # 匹配列表项
            items = re.findall(r"\d+\.\s*(.+)", deliverable_section)
            for idx, item in enumerate(items, 1):
                features.append({
                    "id": f"F{idx:02d}",
                    "name": item.strip(),
                    "priority": "P0" if idx <= 3 else "P1"
                })

        return features

    def _parse_chapter3(self) -> Tuple[List[Dict], List[Dict]]:
        """
        解析第3章：Flow Modeling（流程与事件）

        Returns:
            (user_stories, workflows)
        """
        content = self.chapters.get("Flow Modeling", "")

        # 解析用户故事（从User Story Mapping提取）
        user_stories = []
        us_section = self._extract_section(content, "用户故事列表")
        if us_section:
            # 匹配表格行
            table_rows = re.findall(
                r"\|\s*US-(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|",
                us_section
            )
            for row in table_rows:
                us_id, title, description, priority = row
                user_stories.append({
                    "id": f"US-{us_id}",
                    "title": title.strip(),
                    "description": description.strip(),
                    "priority": priority.strip()
                })

        # 解析工作流（从Event Storming提取）
        workflows = []
        event_section = self._extract_section(content, "Event Storming")
        if event_section:
            # 匹配领域事件
            events = re.findall(r"[-\*]\s*\*\*(.+?)\*\*[（\(]触发[：:](.+?)[）\)]", event_section)
            for idx, (event_name, trigger) in enumerate(events, 1):
                workflows.append({
                    "id": f"WF-{idx:02d}",
                    "name": event_name.strip(),
                    "trigger": trigger.strip()
                })

        return user_stories, workflows

    def _parse_chapter4(self) -> Tuple[List[Dict], List[str], List[Dict], List[Dict]]:
        """
        解析第4章：Domain Modeling（结构与实体）

        Returns:
            (entities, value_objects, aggregates, contexts)
        """
        content = self.chapters.get("Domain Modeling", "")

        # 解析核心实体
        entities = self._parse_entities(content)

        # 解析值对象
        value_objects = self._parse_value_objects(content)

        # 解析聚合根
        aggregates = self._parse_aggregates(content)

        # 解析限界上下文
        contexts = self._parse_contexts(content)

        return entities, value_objects, aggregates, contexts

    def _parse_entities(self, content: str) -> List[Dict]:
        """解析核心实体"""
        entities = []

        entity_section = self._extract_section(content, "核心实体")
        if not entity_section:
            return entities

        # 匹配实体块：**实体名**:
        entity_blocks = re.findall(
            r"\*\*(.+?)\*\*:\s*\n- 属性[：:](.+?)\n- 行为[：:](.+?)(?=\n\*\*|\n###|$)",
            entity_section,
            re.DOTALL
        )

        for entity_name, attrs_str, behaviors_str in entity_blocks:
            # 解析属性
            attributes = [attr.strip() for attr in attrs_str.split(',') if attr.strip()]

            # 解析行为
            behaviors = [bhv.strip() for bhv in behaviors_str.split(',') if bhv.strip()]

            entities.append({
                "name": entity_name.strip(),
                "attributes": attributes,
                "behaviors": behaviors
            })

        return entities

    def _parse_value_objects(self, content: str) -> List[str]:
        """解析值对象"""
        value_objects = []

        vo_section = self._extract_section(content, "值对象")
        if not vo_section:
            return value_objects

        # 匹配列表项
        items = re.findall(r"[-\*]\s*\*\*(.+?)\*\*[：:]", vo_section)
        value_objects = [item.strip() for item in items if item.strip()]

        return value_objects

    def _parse_aggregates(self, content: str) -> List[Dict]:
        """解析聚合根"""
        aggregates = []

        agg_section = self._extract_section(content, "聚合根")
        if not agg_section:
            return aggregates

        # 匹配聚合根块
        agg_blocks = re.findall(
            r"\*\*(.+?)\*\*:\s*\n- 包含[：:](.+?)\n- 不变式[：:](.+?)(?=\n\*\*|\n###|$)",
            agg_section,
            re.DOTALL
        )

        for agg_name, entities_str, invariants_str in agg_blocks:
            # 解析包含的实体
            entities = [e.strip() for e in entities_str.split(',') if e.strip()]

            # 解析不变式
            invariants = [inv.strip() for inv in invariants_str.split(',') if inv.strip()]

            aggregates.append({
                "name": agg_name.strip(),
                "entities": entities,
                "invariants": invariants
            })

        return aggregates

    def _parse_contexts(self, content: str) -> List[Dict]:
        """解析限界上下文"""
        contexts = []

        context_section = self._extract_section(content, "限界上下文")
        if not context_section:
            return contexts

        # 匹配上下文块
        context_blocks = re.findall(
            r"\*\*(.+?)\*\*:\s*\n- 职责[：:](.+?)\n- 实体[：:](.+?)(?=\n\*\*|\n###|$)",
            context_section,
            re.DOTALL
        )

        for context_name, responsibility, entities_str in context_blocks:
            # 解析实体列表
            entities = [e.strip() for e in entities_str.split(',') if e.strip()]

            contexts.append({
                "name": context_name.strip(),
                "responsibility": responsibility.strip(),
                "entities": entities
            })

        return contexts

    # ===================== 辅助方法 =====================

    def _extract_field(self, content: str, pattern: str) -> str:
        """提取单个字段"""
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if match:
            result = match.group(1).strip()
            # 清理可能的markdown格式
            result = result.split('\n')[0]  # 只取第一行
            return result
        return ""

    def _extract_section(self, content: str, section_name: str) -> str:
        """提取章节内容"""
        pattern = rf"###\s*{re.escape(section_name)}.*?\n(.*?)(?=###|$)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""

    def _infer_user_scale(self, content: str) -> str:
        """从描述中推断用户规模"""
        # 提取百分比（如 降低成本30%）
        percentages = re.findall(r"(\d+)%", content)
        if percentages:
            # 根据目标百分比推断规模
            target = int(percentages[0])
            if target >= 50:
                return "10000+"
            elif target >= 30:
                return "1000-10000"
            else:
                return "100-1000"

        # 提取用户数量
        numbers = re.findall(r"(\d+)(?:\s*[-~至到]\s*(\d+))?\s*[人用户]", content)
        if numbers:
            if numbers[0][1]:  # 范围
                return f"{numbers[0][0]}-{numbers[0][1]}"
            else:  # 单个数字
                return numbers[0][0]

        return "1000-10000"  # 默认中等规模


# ===================== 便捷函数 =====================

def parse_design_draft(file_path: str) -> DesignDraft:
    """
    便捷函数：解析DESIGN_DRAFT.md文件

    Args:
        file_path: 文件路径

    Returns:
        DesignDraft对象
    """
    parser = DesignDraftParser()
    return parser.parse_file(file_path)
