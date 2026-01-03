"""
原子级规格Schema定义

参考: C:\\Users\\bigbao\\Desktop\\原子级.txt

定义了原子组件,原子任务等核心数据结构
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class AtomicProp:
    """原子组件属性"""
    name: str
    type: str  # 'string' | 'number' | 'boolean' | 'array' | 'object' | 自定义类型
    required: bool
    default: Optional[str] = None
    description: str = ""

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "default": self.default,
            "description": self.description
        }


@dataclass
class AtomicUISpec:
    """原子UI规格"""
    layout: str  # 布局描述:"左侧头像(48x48圆形) 右侧姓名+角色徽章"
    styles: List[str]  # 样式列表:["Inter 16px semibold", "badge gray-100"]
    states: List[str]  # 状态列表:["idle", "loading", "error"]

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "layout": self.layout,
            "styles": self.styles,
            "states": self.states
        }


@dataclass
class AtomicInteraction:
    """原子交互规格"""
    event: str  # 事件名称:"click", "hover", "submit"
    result: str  # 触发结果:"emit('selectUser')", "调用API", "更新状态"

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "event": self.event,
            "result": self.result
        }


@dataclass
class AtomicComponent:
    """原子组件完整规格"""
    name: str
    purpose: str  # 一句话描述要解决的问题与场景
    props: List[AtomicProp]
    ui: AtomicUISpec
    data: Dict  # 数据契约:{"source": "props", "contracts": [...]}
    interactions: List[AtomicInteraction]
    dependencies: List[str]  # 依赖的现有组件:["components/ui/Badge", "LoadingSkeleton"]
    constraints: List[str]  # 性能,可访问性,国际化约束
    edge_cases: List[str]  # 边界情况:["长文本", "缺失数据", "网络错误"]
    acceptance: List[str]  # 验收标准
    telemetry: Optional[Dict] = None  # 日志和监控:{"log": true, "fields": [...]}

    # 扩展字段
    component_type: str = "UI"  # UI | Logic | Data | Service
    category: str = ""  # 组件分类:Card | Button | Form | List等
    examples: List[str] = field(default_factory=list)  # 使用示例

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "purpose": self.purpose,
            "type": self.component_type,
            "category": self.category,
            "props": [p.to_dict() for p in self.props],
            "ui": self.ui.to_dict(),
            "data": self.data,
            "interactions": [i.to_dict() for i in self.interactions],
            "dependencies": self.dependencies,
            "constraints": self.constraints,
            "edge_cases": self.edge_cases,
            "acceptance": self.acceptance,
            "telemetry": self.telemetry,
            "examples": self.examples
        }


@dataclass
class AtomicAction:
    """原子动作规格"""
    name: str
    params: Dict
    level: str = "normal"  # normal | sensitive | system

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "params": self.params,
            "level": self.level
        }


@dataclass
class AtomicTask:
    """原子任务规格"""
    goal: str  # 任务目标
    context: Dict  # 上下文:{"files": [...], "tech": [...], "domain": "..."}
    artifacts: List[str]  # 产出物:["component", "script", "doc"]
    actions: List[AtomicAction]  # 动作列表
    components: List[AtomicComponent]  # 涉及的组件
    security: Dict  # 安全要求
    acceptance_criteria: List[str]  # 验收标准
    output: Dict  # 输出规格

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "goal": self.goal,
            "context": self.context,
            "artifacts": self.artifacts,
            "actions": [a.to_dict() for a in self.actions],
            "components": [c.to_dict() for c in self.components],
            "security": self.security,
            "acceptance_criteria": self.acceptance_criteria,
            "output": self.output
        }


@dataclass
class AtomicSpecification:
    """原子级规格文档集合"""
    components: List[AtomicComponent] = field(default_factory=list)  # UI原子组件
    tasks: List[AtomicTask] = field(default_factory=list)  # 原子任务
    contracts: List[Dict] = field(default_factory=list)  # API契约
    models: List[Dict] = field(default_factory=list)  # 数据模型
    scenarios: List[Dict] = field(default_factory=list)  # BDD场景
    workflows: List[Dict] = field(default_factory=list)  # 业务流程

    # 元数据
    project_name: str = ""
    generated_at: str = ""
    driving_modes_used: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "project_name": self.project_name,
            "generated_at": self.generated_at,
            "driving_modes_used": self.driving_modes_used,
            "components": [c.to_dict() for c in self.components],
            "tasks": [t.to_dict() for t in self.tasks],
            "contracts": self.contracts,
            "models": self.models,
            "scenarios": self.scenarios,
            "workflows": self.workflows
        }

    def get_summary(self) -> Dict:
        """获取摘要统计"""
        return {
            "components_count": len(self.components),
            "tasks_count": len(self.tasks),
            "contracts_count": len(self.contracts),
            "models_count": len(self.models),
            "scenarios_count": len(self.scenarios),
            "workflows_count": len(self.workflows),
            "driving_modes": self.driving_modes_used
        }
