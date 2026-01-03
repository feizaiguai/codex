"""
交互式需求澄清模块

支持两种模式：
1. 文本输入模式：从用户描述开始交互
2. 文档输入模式：从架构文档提取信息，按需补充
"""

from core.models import ClarifiedContext
from parsers.architecture_doc import parse_markdown, detect_missing_fields, ArchitectureInfo
from typing import Optional


def clarify_from_document(doc_path: str, interactive: bool = True) -> ClarifiedContext:
    """
    从架构文档开始澄清（推荐模式）

    Args:
        doc_path: 架构文档路径
        interactive: 是否交互式补充缺失信息（默认True）

    Returns:
        ClarifiedContext: 澄清后的需求上下文
    """
    print("\n" + "=" * 60)
    print("📄 架构文档解析模式")
    print("=" * 60 + "\n")

    # 解析架构文档
    print(f"📖 正在解析文档: {doc_path}")
    arch_info = parse_markdown(doc_path)
    print(f"✅ 文档解析完成\n")

    # 从架构信息构建上下文
    context = _build_context_from_architecture(arch_info)

    # 检测缺失字段
    missing_fields = detect_missing_fields(arch_info)

    if missing_fields:
        print(f"⚠️  检测到 {len(missing_fields)} 个关键信息缺失:")
        for field in missing_fields:
            print(f"   - {field}")
        print()

        if interactive:
            print("💡 让我们通过交互式问答补充这些信息\n")
            _ask_missing_fields(context, missing_fields)
        else:
            print("ℹ️  非交互模式，将使用默认值或推断值\n")
    else:
        print("✅ 架构文档信息完整，无需额外澄清\n")

    print("=" * 60)
    print("✅ 需求澄清完成")
    print("=" * 60 + "\n")

    return context


def clarify_requirements(raw_input: str, interactive: bool = True) -> ClarifiedContext:
    """
    从文本描述开始澄清（原有模式）

    Args:
        raw_input: 用户的原始输入
        interactive: 是否使用交互模式（默认True）

    Returns:
        ClarifiedContext: 澄清后的需求上下文
    """

    print("\n" + "=" * 60)
    print("🔍 需求澄清阶段（Discovery-First + Example Mapping）")
    print("=" * 60 + "\n")

    context = ClarifiedContext(raw_input=raw_input)

    if not interactive:
        # 非交互模式：使用启发式规则提取
        return _clarify_non_interactive(raw_input)

    # 第1轮：核心问题
    print("📌 第1轮：核心问题\n")
    print("❓ 这个项目要解决什么核心问题？请用1-2句话描述具体的使用场景。\n")
    answer1 = _get_user_input()
    context.core_problem = answer1 if answer1 else raw_input

    # 第2轮：目标用户
    print("\n📌 第2轮：目标用户\n")
    print("❓ 主要用户是谁？他们会如何使用这个系统？（可以列出多个角色，用顿号分隔）\n")
    answer2 = _get_user_input()
    context.target_users = answer2 if answer2 else "通用用户"

    # 第3轮：价值主张
    print("\n📌 第3轮：价值主张\n")
    print("❓ 对用户的核心价值是什么？能否用量化指标描述？（如：提升效率50%、降低成本30%）\n")
    answer3 = _get_user_input()
    context.value_proposition = answer3 if answer3 else context.core_problem

    # 第4轮（可选）：技术挑战
    if _needs_technical_detail(context):
        print("\n📌 第4轮：技术挑战\n")
        print("❓ 最大的技术挑战或风险是什么？（如：高并发、数据安全、实时性要求）\n")
        answer4 = _get_user_input()
        context.technical_challenges = answer4

    # 第5轮（可选）：MVP范围
    if _needs_mvp_scope(context):
        print("\n📌 第5轮：MVP范围\n")
        print("❓ MVP应该包含哪些核心功能？请按优先级列出（用顿号或逗号分隔）\n")
        answer5 = _get_user_input()
        context.mvp_scope = answer5

    print("\n" + "=" * 60)
    print("✅ 需求澄清完成")
    print("=" * 60 + "\n")

    return context


def _build_context_from_architecture(arch_info: ArchitectureInfo) -> ClarifiedContext:
    """
    从架构信息构建澄清上下文

    Args:
        arch_info: 解析的架构信息

    Returns:
        ClarifiedContext: 上下文对象
    """
    # 合并用户信息
    users = arch_info.target_users or arch_info.user_roles
    target_users_str = "、".join(users) if users else "待定义用户"

    # 合并功能信息
    features = arch_info.mvp_scope or arch_info.core_features or arch_info.functional_requirements
    mvp_scope_str = "、".join(features[:10]) if features else "待定义范围"  # 最多10个

    # 技术挑战
    challenges = arch_info.technical_challenges or []
    tech_challenges_str = "、".join(challenges) if challenges else "待识别"

    return ClarifiedContext(
        raw_input=arch_info.project_goal or arch_info.background or arch_info.project_name,
        core_problem=arch_info.project_goal or arch_info.background or "待明确",
        target_users=target_users_str,
        value_proposition=arch_info.value_proposition or arch_info.project_goal or "待定义",
        technical_challenges=tech_challenges_str,
        mvp_scope=mvp_scope_str
    )


def _ask_missing_fields(context: ClarifiedContext, missing_fields: list):
    """
    交互式询问缺失字段

    Args:
        context: 当前上下文
        missing_fields: 缺失字段列表
    """
    field_questions = {
        "项目目标": ("这个项目的主要目标是什么？", "core_problem"),
        "目标用户/角色": ("主要用户是谁？（多个角色用顿号分隔）", "target_users"),
        "核心价值主张": ("对用户的核心价值是什么？", "value_proposition"),
        "核心功能": ("核心功能有哪些？（用顿号或逗号分隔）", "mvp_scope"),
        "MVP范围": ("MVP应该包含哪些功能？（用顿号或逗号分隔）", "mvp_scope"),
    }

    for i, field in enumerate(missing_fields, 1):
        if field in field_questions:
            question, attr = field_questions[field]
            print(f"📌 补充信息 {i}/{len(missing_fields)}: {field}\n")
            print(f"❓ {question}\n")
            answer = _get_user_input()

            if answer and answer != "[用户未提供]":
                setattr(context, attr, answer)
            print()


def _clarify_non_interactive(raw_input: str) -> ClarifiedContext:
    """
    非交互模式：使用启发式规则分析原始输入

    增强版：智能提取关键信息
    """
    import re

    # 提取用户/角色
    users = _extract_users(raw_input)
    target_users_str = "、".join(users) if users else "待定义用户"

    # 提取量化指标（作为价值主张的一部分）
    metrics = _extract_metrics(raw_input)
    value_with_metrics = f"{raw_input[:100]}..." if len(raw_input) > 100 else raw_input
    if metrics:
        value_with_metrics += f" (目标：{', '.join(metrics)})"

    # 提取核心功能
    features = _extract_features(raw_input)
    mvp_scope_str = "、".join(features) if features else raw_input

    # 检测技术挑战关键词
    tech_challenges = _extract_tech_challenges(raw_input)

    return ClarifiedContext(
        raw_input=raw_input,
        core_problem=raw_input,
        target_users=target_users_str,
        value_proposition=value_with_metrics,
        technical_challenges=tech_challenges,
        mvp_scope=mvp_scope_str
    )


def _extract_users(text: str) -> list:
    """从文本中提取用户角色"""
    user_keywords = {
        "学生": "学生", "教师": "教师", "老师": "教师", "家长": "家长",
        "农场主": "农场主", "农民": "农民", "种植户": "种植户",
        "开发者": "开发者", "程序员": "开发者", "工程师": "开发者",
        "管理员": "管理员", "运营": "运营人员", "客服": "客服人员",
        "用户": "用户", "客户": "客户", "消费者": "消费者",
        "医生": "医生", "患者": "患者", "护士": "护士",
        "司机": "司机", "乘客": "乘客", "配送员": "配送员",
    }

    found_users = []
    for keyword, role in user_keywords.items():
        if keyword in text and role not in found_users:
            found_users.append(role)

    return found_users[:5]  # 最多5个角色


def _extract_metrics(text: str) -> list:
    """提取量化指标"""
    import re
    patterns = [
        r'(\d+%)',
        r'提升\s*(\d+%?)',
        r'降低\s*(\d+%?)',
        r'增加\s*(\d+%?)',
        r'减少\s*(\d+%?)',
        r'提高\s*(\d+%?)',
    ]

    metrics = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        metrics.extend(matches)

    return list(set(metrics))[:3]  # 最多3个指标


def _extract_features(text: str) -> list:
    """提取核心功能（基于动词短语）"""
    import re

    # 常见功能动词
    feature_verbs = [
        "监控", "管理", "分析", "预警", "通知", "查询", "搜索", "浏览",
        "上传", "下载", "发布", "编辑", "删除", "创建", "生成", "导出",
        "统计", "报告", "审批", "支付", "登录", "注册", "认证", "授权"
    ]

    features = []
    for verb in feature_verbs:
        # 匹配 "动词+名词" 模式
        pattern = f'{verb}[^，。、；！？\\n]{{2,15}}'
        matches = re.findall(pattern, text)
        for match in matches:
            if match not in features:
                features.append(match.strip())

    return features[:10]  # 最多10个功能


def _extract_tech_challenges(text: str) -> str:
    """提取技术挑战"""
    challenge_keywords = {
        "高并发": "需要处理高并发访问",
        "大规模": "需要支持大规模数据处理",
        "实时": "需要实时响应和处理",
        "分布式": "需要分布式架构",
        "安全": "需要高安全性保障",
        "性能": "需要高性能优化",
        "可扩展": "需要良好的可扩展性",
    }

    challenges = []
    for keyword, desc in challenge_keywords.items():
        if keyword in text:
            challenges.append(desc)

    return "、".join(challenges) if challenges else "待识别"


def _get_user_input() -> str:
    """
    获取用户输入

    Returns:
        str: 用户的回答
    """
    try:
        answer = input("💬 您的回答: ")
        return answer.strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n⚠️ 用户中断，使用默认回答")
        return "[用户未提供]"


def _needs_technical_detail(context: ClarifiedContext) -> bool:
    """
    判断是否需要询问技术细节

    Args:
        context: 当前上下文

    Returns:
        bool: 是否需要
    """
    # 简单规则：如果提到"复杂"、"高性能"、"大规模"等关键词
    keywords = ["复杂", "高性能", "大规模", "分布式", "实时", "安全", "并发"]
    text = f"{context.core_problem} {context.value_proposition}".lower()
    return any(keyword in text for keyword in keywords)


def _needs_mvp_scope(context: ClarifiedContext) -> bool:
    """
    判断是否需要询问MVP范围

    Args:
        context: 当前上下文

    Returns:
        bool: 是否需要
    """
    # 如果mvp_scope看起来是通用默认值，就需要询问
    if not context.mvp_scope:
        return True

    generic_defaults = ["待定义", "待明确", "用户管理", "核心业务", "数据处理"]
    return any(default in context.mvp_scope for default in generic_defaults)
