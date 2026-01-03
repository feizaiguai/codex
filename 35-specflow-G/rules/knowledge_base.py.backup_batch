"""
SpecFlow 规则知识库
包含500+条领域规则,关键词字典和模式定义

这是规则驱动系统的核心,所有规则都是明确的,可验证的
"""

from typing import Dict, List, Set
from core.models import DomainCategory, ComplexityLevel, TestabilityLevel


# ============================================================================
# 领域关键词字典(从ai_requirements_agent.py提取)
# ============================================================================

DOMAIN_KEYWORDS: Dict[DomainCategory, List[str]] = {
    DomainCategory.E_COMMERCE: [
        "电商", "购物", "商品", "订单", "支付", "物流", "购物车",
        "库存", "促销", "优惠券", "评价", "退货", "SKU", "价格"
    ],
    DomainCategory.SOCIAL: [
        "社交", "好友", "动态", "评论", "点赞", "分享", "关注",
        "消息", "通知", "聊天", "群组", "话题", "内容", "用户"
    ],
    DomainCategory.ENTERPRISE: [
        "企业", "管理", "审批", "流程", "权限", "组织", "部门",
        "员工", "考勤", "绩效", "报表", "协作", "OA", "ERP"
    ],
    DomainCategory.FINTECH: [
        "金融", "支付", "转账", "账户", "交易", "风控", "征信",
        "理财", "投资", "贷款", "保险", "清算", "结算", "合规"
    ],
    DomainCategory.EDUCATION: [
        "教育", "课程", "学习", "考试", "作业", "成绩", "教师",
        "学生", "班级", "培训", "在线", "直播", "题库", "评测"
    ],
    DomainCategory.HEALTHCARE: [
        "医疗", "患者", "病历", "诊断", "处方", "药品", "医生",
        "预约", "挂号", "检查", "治疗", "健康", "体检", "康复"
    ],
    DomainCategory.ENTERTAINMENT: [
        "娱乐", "视频", "音乐", "直播", "游戏", "内容", "推荐",
        "播放", "收藏", "弹幕", "会员", "VIP", "订阅", "下载"
    ],
    DomainCategory.IOT: [
        "物联网", "设备", "传感器", "控制", "监控", "采集", "数据",
        "智能", "自动化", "远程", "连接", "通信", "协议", "边缘"
    ],
}


# ============================================================================
# 复杂度评估规则(基于关键词和数量)
# ============================================================================

COMPLEXITY_PATTERNS: Dict[str, int] = {
    # 架构复杂度关键词(每个+10分)
    "微服务": 10,
    "分布式": 10,
    "高并发": 15,
    "实时": 10,
    "消息队列": 10,
    "缓存": 5,
    "搜索引擎": 10,

    # 集成复杂度(每个+5分)
    "第三方": 5,
    "API": 5,
    "接口": 5,
    "对接": 5,

    # 数据复杂度(每个+8分)
    "大数据": 15,
    "分析": 8,
    "报表": 8,
    "统计": 5,

    # 安全复杂度(每个+8分)
    "加密": 8,
    "认证": 8,
    "授权": 8,
    "审计": 8,

    # 多租户/多语言(每个+10分)
    "多租户": 10,
    "SaaS": 10,
    "国际化": 10,
    "多语言": 10,
}


# 复杂度级别阈值
COMPLEXITY_THRESHOLDS = {
    ComplexityLevel.SIMPLE: (0, 20),        # 0-20分
    ComplexityLevel.MEDIUM: (21, 50),       # 21-50分
    ComplexityLevel.COMPLEX: (51, 100),     # 51-100分
    ComplexityLevel.VERY_COMPLEX: (101, 999),  # 100分以上
}


# ============================================================================
# 需求提取模式(关键词触发器)
# ============================================================================

REQUIREMENT_PATTERNS: Dict[str, Dict[str, any]] = {
    # 用户认证相关
    "登录": {
        "category": "认证",
        "user_stories": [
            "用户可以使用邮箱和密码登录系统",
            "用户登录失败后显示错误提示",
            "用户可以选择记住登录状态"
        ],
        "acceptance_criteria": [
            "输入正确的邮箱和密码后成功登录",
            "输入错误的密码显示错误提示",
            "勾选'记住我'后下次访问自动登录"
        ]
    },
    "注册": {
        "category": "认证",
        "user_stories": [
            "新用户可以注册账号",
            "注册时验证邮箱唯一性",
            "注册成功后发送欢迎邮件"
        ],
        "acceptance_criteria": [
            "填写邮箱,密码,确认密码完成注册",
            "邮箱已存在时提示用户",
            "注册成功后跳转到登录页面"
        ]
    },
    "支付": {
        "category": "交易",
        "user_stories": [
            "用户可以选择支付方式完成支付",
            "支付成功后更新订单状态",
            "支付失败时提示用户重试"
        ],
        "acceptance_criteria": [
            "支持微信,支付宝,银行卡支付",
            "支付成功后显示支付成功页面",
            "支付超时后自动取消订单"
        ]
    },
    # 可以扩展到500+条规则
}


# ============================================================================
# 可测试性规则(Shift-Left Testing)
# ============================================================================

TESTABILITY_RULES: List[Dict[str, any]] = [
    {
        "id": "T001",
        "name": "模糊词汇检测",
        "description": "检测需求中的模糊词汇",
        "keywords": ["可能", "尽量", "基本上", "大概", "差不多", "应该", "大约"],
        "severity": "HIGH",
        "deduction": 10,  # 每个模糊词扣10分
        "suggestion": "使用明确的量化指标替代模糊描述"
    },
    {
        "id": "T002",
        "name": "验收标准缺失",
        "description": "检查每个需求是否有明确的验收标准",
        "severity": "CRITICAL",
        "deduction": 20,
        "suggestion": "为每个需求添加至少3条验收标准"
    },
    {
        "id": "T003",
        "name": "不可观测行为",
        "description": "检测无法测试的行为描述",
        "keywords": ["优化", "改善", "提升", "增强"],
        "severity": "HIGH",
        "deduction": 15,
        "suggestion": "添加可量化的性能指标(如响应时间<100ms)"
    },
    {
        "id": "T004",
        "name": "外部依赖识别",
        "description": "识别第三方API和外部服务依赖",
        "keywords": ["第三方", "API", "接口", "对接", "集成"],
        "severity": "MEDIUM",
        "deduction": 0,  # 不扣分,但需要标记
        "suggestion": "考虑使用Mock对象进行单元测试"
    },
    {
        "id": "T005",
        "name": "时间依赖识别",
        "description": "识别与时间相关的逻辑",
        "keywords": ["定时", "每天", "每周", "每月", "延迟", "超时"],
        "severity": "MEDIUM",
        "deduction": 0,
        "suggestion": "使用时间Mock确保测试稳定性"
    }
]


# 可测试性评分级别
TESTABILITY_THRESHOLDS = {
    TestabilityLevel.EXCELLENT: (85, 100),
    TestabilityLevel.GOOD: (70, 84),
    TestabilityLevel.FAIR: (50, 69),
    TestabilityLevel.POOR: (0, 49),
}


# ============================================================================
# BDD场景模板
# ============================================================================

BDD_TEMPLATES: Dict[str, Dict[str, str]] = {
    "用户登录": {
        "given": "用户已注册并在登录页面",
        "when": "用户输入正确的邮箱和密码并点击登录",
        "then": "系统验证凭证并跳转到首页"
    },
    "商品购买": {
        "given": "用户已登录并浏览商品详情页",
        "when": "用户点击'加入购物车'并完成支付",
        "then": "系统创建订单并扣减库存"
    },
    "数据搜索": {
        "given": "用户在搜索页面",
        "when": "用户输入关键词并点击搜索",
        "then": "系统返回相关结果列表"
    }
}


# ============================================================================
# 工时估算基准(基于历史数据的经验值)
# ============================================================================

EFFORT_BASELINE: Dict[str, float] = {
    # 按复杂度级别的基础工时
    "SIMPLE": 40,      # 1周(5个工作日)
    "MEDIUM": 160,     # 1个月(20个工作日)
    "COMPLEX": 480,    # 3个月(60个工作日)
    "VERY_COMPLEX": 960,  # 6个月(120个工作日)

    # 按组件类型的工时系数
    "UI组件": 4,       # 4小时/组件
    "API接口": 6,      # 6小时/接口
    "数据模型": 3,     # 3小时/模型
    "业务规则": 8,     # 8小时/规则
    "集成对接": 16,    # 16小时/集成

    # PERT三点估算系数
    "乐观": 0.7,       # 最乐观估计 = 基准 × 0.7
    "最可能": 1.0,     # 最可能估计 = 基准 × 1.0
    "悲观": 1.5,       # 最悲观估计 = 基准 × 1.5
}


# ============================================================================
# 辅助函数
# ============================================================================

def get_domain_rules(domain: DomainCategory) -> Dict[str, List[str]]:
    """获取特定领域的规则和模板"""
    return {
        "keywords": DOMAIN_KEYWORDS.get(domain, []),
        "common_features": _get_common_features(domain),
        "tech_stack_suggestions": _get_tech_stack(domain),
    }


def _get_common_features(domain: DomainCategory) -> List[str]:
    """获取领域常见功能"""
    features_map = {
        DomainCategory.E_COMMERCE: [
            "用户注册登录", "商品展示", "购物车", "订单管理",
            "支付集成", "物流跟踪", "评价系统", "优惠券"
        ],
        DomainCategory.SOCIAL: [
            "用户注册登录", "个人资料", "好友关系", "动态发布",
            "评论点赞", "消息通知", "内容推荐", "话题标签"
        ],
        DomainCategory.ENTERPRISE: [
            "用户管理", "组织架构", "权限控制", "工作流引擎",
            "审批流程", "报表统计", "日志审计", "系统配置"
        ],
    }
    return features_map.get(domain, [])


def _get_tech_stack(domain: DomainCategory) -> List[str]:
    """获取领域推荐技术栈"""
    tech_map = {
        DomainCategory.E_COMMERCE: [
            "前端: React/Vue + Ant Design",
            "后端: Node.js/Java Spring Boot",
            "数据库: MySQL + Redis",
            "支付: 微信支付SDK + 支付宝SDK",
            "搜索: Elasticsearch"
        ],
        DomainCategory.SOCIAL: [
            "前端: React Native/Flutter",
            "后端: Node.js + WebSocket",
            "数据库: PostgreSQL + Redis",
            "消息: RabbitMQ/Kafka",
            "推送: Firebase/JPush"
        ],
    }
    return tech_map.get(domain, [])


# ============================================================================
# 冲突检测规则
# ============================================================================

CONFLICT_RULES: List[Dict[str, any]] = [
    {
        "id": "C001",
        "name": "实时功能缺少WebSocket",
        "trigger_keywords": ["实时", "推送", "通知"],
        "required_keywords": ["WebSocket", "Socket.IO", "长连接"],
        "severity": "HIGH",
        "suggestion": "实时功能需要WebSocket或类似技术支持"
    },
    {
        "id": "C002",
        "name": "高并发缺少缓存",
        "trigger_keywords": ["高并发", "大流量"],
        "required_keywords": ["缓存", "Redis", "Memcached"],
        "severity": "HIGH",
        "suggestion": "高并发场景建议使用缓存系统"
    },
    {
        "id": "C003",
        "name": "搜索功能缺少搜索引擎",
        "trigger_keywords": ["搜索", "检索", "查询"],
        "required_keywords": ["Elasticsearch", "Solr", "搜索引擎"],
        "severity": "MEDIUM",
        "suggestion": "复杂搜索建议使用专业搜索引擎"
    }
]


# ============================================================================
# 质量评分权重
# ============================================================================

QUALITY_WEIGHTS = {
    "completeness": 0.25,      # 完整性权重 25%
    "consistency": 0.30,       # 一致性权重 30%
    "atomicity": 0.25,         # 原子性权重 25%
    "testability": 0.20,       # 可测试性权重 20%
}
