#!/usr/bin/env python3
"""
多格式需求文档解析器

支持从多种格式的需求输入中提取结构化信息：
- AI聊天记录（ChatGPT、Claude等）
- 需求列表（Bullet points）
- 用户故事集
- 自由文本描述
- Markdown架构文档（已有）

统一输出标准化的需求字典，用于DESIGN_DRAFT生成
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class RequirementInfo:
    """从需求文档中提取的结构化信息"""

    # 基本信息
    project_name: str = ""
    raw_content: str = ""
    source_format: str = ""  # 检测到的格式类型

    # 需求相关
    project_goal: str = ""
    background: str = ""
    target_users: List[str] = field(default_factory=list)
    user_roles: List[str] = field(default_factory=list)
    value_proposition: str = ""

    # 功能相关
    core_features: List[str] = field(default_factory=list)
    functional_requirements: List[str] = field(default_factory=list)
    mvp_scope: List[str] = field(default_factory=list)

    # 技术相关
    technical_stack: Dict[str, str] = field(default_factory=dict)
    architecture_style: str = ""
    technical_challenges: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    # 非功能性需求
    performance_requirements: List[str] = field(default_factory=list)
    security_requirements: List[str] = field(default_factory=list)
    scalability_requirements: List[str] = field(default_factory=list)

    # 业务相关
    business_goals: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)


class RequirementDocParser:
    """统一需求文档解析器"""

    SUPPORTED_FORMATS = [
        "chat_transcript",    # AI聊天记录
        "requirement_list",   # 需求列表
        "user_stories",       # 用户故事
        "free_text",          # 自由文本
        "markdown_doc",       # 标准架构文档（使用现有解析器）
    ]

    def parse(self, content: str, format_hint: str = "auto") -> RequirementInfo:
        """
        解析任意格式的需求文档

        Args:
            content: 文档内容（字符串或文件路径）
            format_hint: 格式提示（auto表示自动识别）

        Returns:
            RequirementInfo: 标准化的需求信息
        """
        # 判断是文件路径还是内容
        if len(content) < 500 and (Path(content).exists() if content else False):
            # 可能是文件路径
            try:
                path = Path(content)
                with open(path, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                project_name = path.stem
            except:
                # 不是有效路径，当作内容处理
                text_content = content
                project_name = ""
        else:
            # 直接是内容
            text_content = content
            project_name = ""

        # 1. 自动识别格式
        if format_hint == "auto":
            format_hint = self._detect_format(text_content)

        # 2. 调用对应解析器
        info = RequirementInfo(
            project_name=project_name,
            raw_content=text_content,
            source_format=format_hint
        )

        if format_hint == "chat_transcript":
            self._parse_chat_transcript(text_content, info)
        elif format_hint == "requirement_list":
            self._parse_requirement_list(text_content, info)
        elif format_hint == "user_stories":
            self._parse_user_stories(text_content, info)
        elif format_hint == "free_text":
            self._parse_free_text(text_content, info)
        elif format_hint == "markdown_doc":
            # 使用现有的architecture_doc解析器
            from .architecture_doc import parse_markdown
            arch_info = parse_markdown(content) if Path(content).exists() else None
            if arch_info:
                self._convert_from_architecture_info(arch_info, info)
            else:
                # 如果不是文件，尝试解析markdown内容
                self._parse_markdown_content(text_content, info)

        return info

    def _detect_format(self, content: str) -> str:
        """自动识别文档格式"""
        # 聊天记录特征：User:/Assistant:、Human:/AI:等
        if any(pattern in content for pattern in ["User:", "Assistant:", "Human:", "AI:", "Claude:", "ChatGPT:"]):
            return "chat_transcript"

        # 用户故事特征：作为...我希望...以便...
        if re.search(r'(?:作为|As\s+a).*?(?:我希望|I\s+want).*?(?:以便|so\s+that)', content, re.IGNORECASE):
            return "user_stories"

        # 需求列表特征：多个以-或*开头的列表项
        lines = content.strip().split('\n')
        bullet_lines = [l for l in lines if l.strip().startswith(('-', '*', '•'))]
        if len(bullet_lines) > 3:
            return "requirement_list"

        # Markdown文档特征：有标题结构
        if re.search(r'^#+\s+', content, re.MULTILINE):
            return "markdown_doc"

        # 默认为自由文本
        return "free_text"

    def _parse_chat_transcript(self, content: str, info: RequirementInfo):
        """解析AI聊天记录"""
        # 提取用户的需求陈述
        user_messages = []
        ai_messages = []

        # 匹配各种聊天格式
        patterns = [
            r'(?:User|Human|用户)[：:]\s*(.*?)(?=(?:User|Human|Assistant|AI|Claude|ChatGPT|用户|助手)[：:]|\Z)',
            r'(?:Assistant|AI|Claude|ChatGPT|助手)[：:]\s*(.*?)(?=(?:User|Human|Assistant|AI|Claude|ChatGPT|用户|助手)[：:]|\Z)',
        ]

        # 提取User消息
        for match in re.finditer(patterns[0], content, re.DOTALL | re.IGNORECASE):
            msg = match.group(1).strip()
            if msg:
                user_messages.append(msg)

        # 提取AI消息
        for match in re.finditer(patterns[1], content, re.DOTALL | re.IGNORECASE):
            msg = match.group(1).strip()
            if msg:
                ai_messages.append(msg)

        # 合并所有用户消息作为需求来源
        all_user_content = '\n\n'.join(user_messages)

        # 从用户消息中提取结构化信息
        self._extract_from_text(all_user_content, info)

        # 从AI消息中提取补充信息（AI可能总结了需求）
        all_ai_content = '\n\n'.join(ai_messages)
        self._extract_supplementary_info(all_ai_content, info)

    def _parse_requirement_list(self, content: str, info: RequirementInfo):
        """解析需求列表（bullet points）"""
        lines = content.strip().split('\n')
        features = []
        requirements = []
        users = []
        challenges = []

        current_section = None

        for line in lines:
            line = line.strip()

            # 检测章节标题
            if re.match(r'^#+\s*(.+)', line):
                title = re.match(r'^#+\s*(.+)', line).group(1).lower()
                if '功能' in title or 'feature' in title:
                    current_section = 'features'
                elif '用户' in title or 'user' in title:
                    current_section = 'users'
                elif '挑战' in title or 'challenge' in title:
                    current_section = 'challenges'
                elif '需求' in title or 'requirement' in title:
                    current_section = 'requirements'
                continue

            # 提取列表项
            if line.startswith(('-', '*', '•', '+')):
                item = line.lstrip('-*•+ ').strip()
                if not item:
                    continue

                # 根据当前章节归类
                if current_section == 'features':
                    features.append(item)
                elif current_section == 'users':
                    users.append(item.split('：')[0].split(':')[0])
                elif current_section == 'challenges':
                    challenges.append(item)
                elif current_section == 'requirements':
                    requirements.append(item)
                else:
                    # 未明确章节，根据内容猜测
                    if any(keyword in item for keyword in ['用户', '角色', 'user', 'role']):
                        users.append(item.split('：')[0].split(':')[0])
                    elif any(keyword in item for keyword in ['功能', 'feature', '模块', 'module']):
                        features.append(item)
                    else:
                        requirements.append(item)

        info.core_features = features if features else info.core_features
        info.functional_requirements = requirements if requirements else info.functional_requirements
        info.target_users = users if users else info.target_users
        info.technical_challenges = challenges if challenges else info.technical_challenges

        # 尝试提取项目目标（第一段非列表文本）
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith(('-', '*', '•', '+', '#'))]
        if paragraphs:
            info.project_goal = paragraphs[0]

    def _parse_user_stories(self, content: str, info: RequirementInfo):
        """解析用户故事集"""
        # 匹配用户故事格式：作为...我希望...以便...
        stories = re.findall(
            r'(?:作为|As\s+a)\s*([^，,\n]+).*?(?:我希望|I\s+want)\s*([^，,\n]+).*?(?:以便|so\s+that)\s*([^。.\n]+)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        users = set()
        features = []
        goals = []

        for role, action, benefit in stories:
            role = role.strip()
            action = action.strip()
            benefit = benefit.strip()

            users.add(role)
            features.append(action)
            if benefit:
                goals.append(benefit)

        info.target_users = list(users)
        info.core_features = features
        if goals:
            info.value_proposition = '; '.join(set(goals))

        # 提取项目目标（第一段概述文本）
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('#', '-', '*', '•')) and '作为' not in line and 'As a' not in line.lower():
                if len(line) > 20:
                    info.project_goal = line
                    break

    def _parse_free_text(self, content: str, info: RequirementInfo):
        """解析自由文本描述"""
        # 提取关键信息
        self._extract_from_text(content, info)

    def _parse_markdown_content(self, content: str, info: RequirementInfo):
        """解析Markdown格式的内容（不是文件）"""
        # 与architecture_doc类似的逻辑，但适用于内容字符串
        self._extract_from_text(content, info)

        # 提取标题作为项目名（如果有）
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if title_match:
            info.project_name = title_match.group(1).strip()

    def _extract_from_text(self, text: str, info: RequirementInfo):
        """从文本中提取结构化信息（通用方法）"""
        # 提取项目目标/描述
        goal_keywords = ['目标', '目的', '要做', '想做', '打算', 'goal', 'objective', 'purpose', 'want to', 'plan to']
        for keyword in goal_keywords:
            pattern = rf'(?:{keyword})[：:\s]+(.*?)(?:\n|。|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info.project_goal = match.group(1).strip()
                break

        # 如果没找到，取第一句话作为目标
        if not info.project_goal:
            sentences = re.split(r'[。\n]', text.strip())
            if sentences:
                info.project_goal = sentences[0].strip()

        # 提取功能列表
        feature_keywords = ['功能', '模块', '包括', '需要', 'feature', 'module', 'include', 'need']
        for keyword in feature_keywords:
            # 查找关键词后的列表
            pattern = rf'{keyword}[：:\s]+(.*?)(?:\n\n|\Z)'
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                feature_text = match.group(1)
                # 提取列表项
                items = re.findall(r'(?:[-*•+]|\d+\.)\s*([^\n]+)', feature_text)
                if items:
                    info.core_features.extend([item.strip() for item in items])
                    break

        # 提取用户类型
        user_keywords = ['用户', '角色', '面向', 'user', 'role', 'for']
        for keyword in user_keywords:
            pattern = rf'{keyword}[：:\s]+(.*?)(?:\n|。|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                user_text = match.group(1).strip()
                # 分割多个用户
                users = re.split(r'[、，,和及&]', user_text)
                info.target_users.extend([u.strip() for u in users if u.strip()])
                break

        # 提取技术栈
        tech_keywords = ['技术栈', '技术', '使用', 'tech stack', 'technology', 'using']
        for keyword in tech_keywords:
            pattern = rf'{keyword}[：:\s]+(.*?)(?:\n|。|$)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tech_text = match.group(1).strip()
                # 简单分割
                techs = re.split(r'[、，,]', tech_text)
                for tech in techs:
                    if tech.strip():
                        # 简单归类
                        if any(kw in tech.lower() for kw in ['react', 'vue', 'angular', 'frontend', '前端']):
                            info.technical_stack['前端'] = tech.strip()
                        elif any(kw in tech.lower() for kw in ['node', 'python', 'java', 'go', 'backend', '后端']):
                            info.technical_stack['后端'] = tech.strip()
                        elif any(kw in tech.lower() for kw in ['mysql', 'postgres', 'mongodb', 'database', '数据库']):
                            info.technical_stack['数据库'] = tech.strip()
                        else:
                            info.technical_stack['其他'] = tech.strip()
                break

    def _extract_supplementary_info(self, text: str, info: RequirementInfo):
        """从补充文本（如AI回复）中提取额外信息"""
        # 如果主要信息已经提取，这里可以补充缺失的部分
        if not info.value_proposition:
            # 查找价值主张相关内容
            value_keywords = ['价值', '好处', '优势', 'value', 'benefit', 'advantage']
            for keyword in value_keywords:
                pattern = rf'{keyword}[：:\s]+(.*?)(?:\n|。|$)'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    info.value_proposition = match.group(1).strip()
                    break

    def _convert_from_architecture_info(self, arch_info, req_info: RequirementInfo):
        """从ArchitectureInfo转换为RequirementInfo"""
        req_info.project_name = arch_info.project_name
        req_info.project_goal = arch_info.project_goal
        req_info.background = arch_info.background
        req_info.target_users = arch_info.target_users
        req_info.user_roles = arch_info.user_roles
        req_info.value_proposition = arch_info.value_proposition
        req_info.core_features = arch_info.core_features
        req_info.functional_requirements = arch_info.functional_requirements
        req_info.mvp_scope = arch_info.mvp_scope
        req_info.technical_stack = arch_info.technical_stack
        req_info.architecture_style = arch_info.architecture_style
        req_info.technical_challenges = arch_info.technical_challenges
        req_info.constraints = arch_info.constraints
        req_info.performance_requirements = arch_info.performance_requirements
        req_info.security_requirements = arch_info.security_requirements
        req_info.scalability_requirements = arch_info.scalability_requirements
        req_info.business_goals = arch_info.business_goals
        req_info.success_metrics = arch_info.success_metrics

    def to_dict(self, info: RequirementInfo) -> Dict:
        """转换为标准字典格式（用于DESIGN_DRAFT生成）"""
        return {
            "project_name": info.project_name,
            "source_format": info.source_format,
            "project_goal": info.project_goal,
            "background": info.background,
            "target_users": info.target_users,
            "user_roles": info.user_roles,
            "value_proposition": info.value_proposition,
            "core_features": info.core_features,
            "functional_requirements": info.functional_requirements,
            "mvp_scope": info.mvp_scope,
            "technical_stack": info.technical_stack,
            "architecture_style": info.architecture_style,
            "technical_challenges": info.technical_challenges,
            "constraints": info.constraints,
            "performance_requirements": info.performance_requirements,
            "security_requirements": info.security_requirements,
            "scalability_requirements": info.scalability_requirements,
            "business_goals": info.business_goals,
            "success_metrics": info.success_metrics,
        }


# 便捷函数
def parse_requirement(content: str, format_hint: str = "auto") -> Dict:
    """
    解析需求文档的便捷函数

    Args:
        content: 文档内容或文件路径
        format_hint: 格式提示

    Returns:
        Dict: 标准化的需求字典
    """
    parser = RequirementDocParser()
    info = parser.parse(content, format_hint)
    return parser.to_dict(info)
