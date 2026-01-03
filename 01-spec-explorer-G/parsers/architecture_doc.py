#!/usr/bin/env python3
"""
架构文档解析器

支持从Markdown架构文档中提取结构化信息：
- 项目目标和背景
- 目标用户和角色
- 核心功能列表
- 技术栈和架构
- 技术挑战和约束
- 非功能性需求
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ArchitectureInfo:
    """从架构文档中提取的结构化信息"""

    # 基本信息
    project_name: str = ""
    raw_content: str = ""

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


def parse_markdown(file_path: str) -> ArchitectureInfo:
    """
    解析Markdown架构文档

    Args:
        file_path: 文档文件路径

    Returns:
        ArchitectureInfo: 提取的结构化信息
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文档文件不存在: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    info = ArchitectureInfo(
        project_name=path.stem,
        raw_content=content
    )

    # 解析各个部分
    _extract_project_info(content, info)
    _extract_users_and_roles(content, info)
    _extract_features(content, info)
    _extract_technical_info(content, info)
    _extract_business_info(content, info)

    return info


def _extract_project_info(content: str, info: ArchitectureInfo):
    """提取项目基本信息"""

    # 提取项目目标
    goal_patterns = [
        r'#+\s*(?:项目)?目标[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'#+\s*(?:项目)?目标\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*(?:Project\s+)?Goal[s]?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in goal_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            info.project_goal = match.group(1).strip()
            break

    # 提取背景信息
    bg_patterns = [
        r'#+\s*(?:项目)?背景[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'#+\s*背景介绍\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*Background\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in bg_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            info.background = match.group(1).strip()
            break

    # 提取价值主张
    value_patterns = [
        r'#+\s*(?:核心)?价值(?:主张)?[：:]?\s*\n+(.*?)(?=\n#+|\Z)',  # 冒号可选
        r'#+\s*Value\s+Proposition\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in value_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            info.value_proposition = match.group(1).strip()
            break


def _extract_users_and_roles(content: str, info: ArchitectureInfo):
    """提取用户和角色信息"""

    # 提取目标用户
    user_patterns = [
        r'#+\s*(?:目标)?用户\s*\n+(.*?)(?=\n#+|\Z)',
        r'#+\s*用户(?:群体|角色)\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*(?:Target\s+)?Users?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in user_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            user_text = match.group(1).strip()
            # 提取列表项（支持 "- **农场主**：描述" 格式）
            users = re.findall(r'[-*]\s*\*?\*?([^：:*\n]+)\*?\*?[：:]', user_text)
            if users:
                info.target_users = [u.strip() for u in users]
            else:
                # 尝试简单列表格式 "- 农场主"
                users = re.findall(r'[-*]\s*([^\n]+)', user_text)
                if users:
                    info.target_users = [u.strip().lstrip('*').rstrip('*').split('：')[0].split(':')[0].strip() for u in users]
            break

    # 提取角色定义
    role_patterns = [
        r'#+\s*(?:用户)?角色[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Roles?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in role_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            role_text = match.group(1).strip()
            roles = re.findall(r'[-*]\s*(?:\*\*)?([^：:*\n]+)(?:\*\*)?[：:]', role_text)
            if roles:
                info.user_roles = [r.strip() for r in roles]
            break


def _extract_features(content: str, info: ArchitectureInfo):
    """提取功能需求"""

    # 提取核心功能
    feature_patterns = [
        r'#+\s*(?:核心)?功能\s*\n+(.*?)(?=\n#+|\Z)',
        r'#+\s*功能(?:需求|列表|清单)\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*(?:Core\s+)?Features?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in feature_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            feature_text = match.group(1).strip()
            # 提取列表项（支持 -、*、数字列表）
            features = re.findall(r'(?:[-*]|\d+\.)\s*([^\n（(]+)', feature_text)
            if features:
                info.core_features = [f.strip().lstrip('`*').rstrip('`*').strip() for f in features if len(f.strip()) > 2]
            break

    # 提取功能需求
    req_patterns = [
        r'#+\s*功能性?需求\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*Functional\s+Requirements?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in req_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            req_text = match.group(1).strip()
            reqs = re.findall(r'[-*]\s*([^\n]+)', req_text)
            if reqs:
                info.functional_requirements = [r.strip() for r in reqs]
            break

    # 提取MVP范围
    mvp_patterns = [
        r'#+\s*MVP\s*(?:范围)?\s*\n+(.*?)(?=\n#+|\Z)',
        r'##\s*MVP\s+Scope\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in mvp_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            mvp_text = match.group(1).strip()
            # 支持 -、*、数字列表
            mvp_items = re.findall(r'(?:[-*]|\d+\.)\s*([^\n（(]+)', mvp_text)
            if mvp_items:
                info.mvp_scope = [m.strip() for m in mvp_items if len(m.strip()) > 2]
            break


def _extract_technical_info(content: str, info: ArchitectureInfo):
    """提取技术信息"""

    # 提取技术栈
    tech_patterns = [
        r'#+\s*技术栈[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'#+\s*Technology\s+Stack\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in tech_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            tech_text = match.group(1).strip()
            # 提取键值对 "前端: React"
            tech_pairs = re.findall(r'[-*]\s*([^：:\n]+)[：:]\s*([^\n]+)', tech_text)
            if tech_pairs:
                info.technical_stack = {k.strip(): v.strip() for k, v in tech_pairs}
            break

    # 提取架构风格
    arch_patterns = [
        r'#+\s*(?:架构|Architecture)(?:风格|Style)?[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'#+\s*System\s+Architecture\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in arch_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            arch_text = match.group(1).strip()
            # 提取第一行或第一段
            first_line = arch_text.split('\n')[0].strip()
            if first_line and not first_line.startswith('#'):
                info.architecture_style = first_line
            break

    # 提取技术挑战
    challenge_patterns = [
        r'#+\s*技术挑战[：:]?\s*\n+(.*?)(?=\n#+|\Z)',  # 冒号可选
        r'#+\s*(?:Technical\s+)?Challenges?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in challenge_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            challenge_text = match.group(1).strip()
            # 支持 -、*、数字列表
            challenges = re.findall(r'(?:[-*]|\d+\.)\s*([^\n]+)', challenge_text)
            if challenges:
                info.technical_challenges = [c.strip() for c in challenges]
            break

    # 提取约束条件
    constraint_patterns = [
        r'#+\s*约束(?:条件)?[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Constraints?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in constraint_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            constraint_text = match.group(1).strip()
            # 支持 -、*、数字列表
            constraints = re.findall(r'(?:[-*]|\d+\.)\s*([^\n]+)', constraint_text)
            if constraints:
                info.constraints = [c.strip() for c in constraints]
            break

    # 提取非功能性需求
    _extract_nonfunctional_requirements(content, info)


def _extract_nonfunctional_requirements(content: str, info: ArchitectureInfo):
    """提取非功能性需求"""

    # 性能需求
    perf_patterns = [
        r'#+\s*性能(?:需求)?[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Performance\s+Requirements?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in perf_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            perf_text = match.group(1).strip()
            perfs = re.findall(r'[-*]\s*([^\n]+)', perf_text)
            if perfs:
                info.performance_requirements = [p.strip() for p in perfs]
            break

    # 安全需求
    sec_patterns = [
        r'#+\s*安全(?:需求)?[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Security\s+Requirements?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in sec_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            sec_text = match.group(1).strip()
            secs = re.findall(r'[-*]\s*([^\n]+)', sec_text)
            if secs:
                info.security_requirements = [s.strip() for s in secs]
            break

    # 可扩展性需求
    scale_patterns = [
        r'#+\s*可扩展性(?:需求)?[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Scalability\s+Requirements?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in scale_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            scale_text = match.group(1).strip()
            scales = re.findall(r'[-*]\s*([^\n]+)', scale_text)
            if scales:
                info.scalability_requirements = [s.strip() for s in scales]
            break


def _extract_business_info(content: str, info: ArchitectureInfo):
    """提取业务信息"""

    # 业务目标
    biz_patterns = [
        r'#+\s*业务目标[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*Business\s+Goals?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in biz_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            biz_text = match.group(1).strip()
            goals = re.findall(r'[-*]\s*([^\n]+)', biz_text)
            if goals:
                info.business_goals = [g.strip() for g in goals]
            break

    # 成功指标
    metric_patterns = [
        r'#+\s*(?:成功)?(?:指标|KPI)[：:]\s*\n(.*?)(?=\n#+|\Z)',
        r'##\s*(?:Success\s+)?Metrics?\s*\n+(.*?)(?=\n##|\Z)'
    ]
    for pattern in metric_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            metric_text = match.group(1).strip()
            metrics = re.findall(r'[-*]\s*([^\n]+)', metric_text)
            if metrics:
                info.success_metrics = [m.strip() for m in metrics]
            break


def summarize_info(info: ArchitectureInfo) -> Dict[str, any]:
    """
    生成架构信息摘要（用于缺口检测）

    Returns:
        Dict: 字段名 -> (是否有值, 值)
    """
    return {
        "project_goal": (bool(info.project_goal), info.project_goal),
        "target_users": (bool(info.target_users), info.target_users),
        "value_proposition": (bool(info.value_proposition), info.value_proposition),
        "core_features": (bool(info.core_features), info.core_features),
        "mvp_scope": (bool(info.mvp_scope), info.mvp_scope),
        "technical_challenges": (bool(info.technical_challenges), info.technical_challenges),
    }


def detect_missing_fields(info: ArchitectureInfo) -> List[str]:
    """
    检测缺失的关键字段

    Returns:
        List[str]: 缺失字段的描述列表
    """
    missing = []

    if not info.project_goal:
        missing.append("项目目标")

    if not info.target_users and not info.user_roles:
        missing.append("目标用户/角色")

    if not info.value_proposition:
        missing.append("核心价值主张")

    if not info.core_features and not info.functional_requirements:
        missing.append("核心功能")

    if not info.mvp_scope:
        missing.append("MVP范围")

    return missing
