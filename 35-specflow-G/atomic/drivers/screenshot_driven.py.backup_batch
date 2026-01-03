"""
截图驱动模式

从UI设计稿/原型图/功能描述生成原子组件规格
适用于:UI组件,视觉组件,交互组件
"""

from typing import List, Dict
from ..schema import AtomicComponent, AtomicProp, AtomicUISpec, AtomicInteraction


class ScreenshotDrivenDriver:
    """截图驱动生成器"""

    def __init__(self):
        # UI模式映射(当前版本仅支持常用模式)
        self.ui_patterns = {
            "user": self._generate_user_card,
            "auth": self._generate_auth_button,
            "search": self._generate_search_component,
        }

    def generate_component_specs(
        self,
        design_draft: Dict,
        context: Dict = None
    ) -> List[AtomicComponent]:
        """
        从DESIGN_DRAFT和UI模式生成原子组件

        Args:
            design_draft: 设计草稿数据
            context: 额外上下文(技术栈,约束等)

        Returns:
            List[AtomicComponent]: 原子组件列表
        """
        components = []

        # 从核心功能推断UI组件
        features = design_draft.get("core_features", [])
        for feature in features:
            feature_lower = feature.lower()

            # 识别常见UI模式
            if any(keyword in feature_lower for keyword in ["用户", "列表", "管理"]):
                components.append(self._generate_user_card(feature))

            if any(keyword in feature_lower for keyword in ["登录", "登出", "注册"]):
                components.append(self._generate_auth_button(feature))

            if any(keyword in feature_lower for keyword in ["表单", "输入", "创建", "编辑"]):
                components.append(self._generate_form_component_from_feature(feature))

            if any(keyword in feature_lower for keyword in ["搜索", "筛选", "查询"]):
                components.append(self._generate_search_component(feature))

        # 去重(基于组件名称)
        unique_components = {}
        for comp in components:
            if comp and comp.name not in unique_components:
                unique_components[comp.name] = comp

        return list(unique_components.values())

    def _generate_user_card(self, feature: str) -> AtomicComponent:
        """生成用户卡片组件"""
        return AtomicComponent(
            name="UserCard",
            purpose="显示用户基本信息与在线状态",
            component_type="UI",
            category="Card",
            props=[
                AtomicProp("avatarUrl", "string", required=True, description="用户头像URL"),
                AtomicProp("fullName", "string", required=True, description="用户全名"),
                AtomicProp("role", "'admin'|'staff'|'viewer'", required=True, description="用户角色"),
                AtomicProp("isOnline", "boolean", required=True, description="是否在线")
            ],
            ui=AtomicUISpec(
                layout="左侧头像(48x48圆形) 右侧姓名+角色徽章,下方状态点(8px)",
                styles=["Inter 16px semibold", "badge gray-100", "gap-3"],
                states=["idle", "loading-skeleton", "error"]
            ),
            data={
                "source": "props",
                "contracts": ["稳定接口,不抛异常", "头像URL失败使用占位图"]
            },
            interactions=[
                AtomicInteraction("click", "emit('selectUser', userId)")
            ],
            dependencies=["components/ui/Badge", "LoadingSkeleton"],
            constraints=[
                "无阻塞渲染(使用虚拟滚动)",
                "ARIA标签完整(aria-label='用户卡片:{fullName}')",
                "响应式设计(移动端适配)"
            ],
            edge_cases=[
                "无头像使用占位图(首字母圆圈)",
                "姓名过长显示省略号(>20字符)",
                "头像加载失败显示默认图标",
                "role值异常默认显示'viewer'"
            ],
            acceptance=[
                "通过无障碍审查(WCAG 2.1 AA级别)",
                "截图与设计稿100%对齐",
                "单元测试覆盖率>90%",
                "支持dark mode"
            ],
            telemetry={"log": True, "fields": ["renderTimeMs", "interactionCount"]},
            examples=["用户列表", "成员管理", "搜索结果"]
        )

    def _generate_auth_button(self, feature: str) -> AtomicComponent:
        """生成认证按钮组件"""
        if "登出" in feature or "logout" in feature.lower():
            return AtomicComponent(
                name="LogoutButton",
                purpose="触发用户登出流程",
                component_type="UI",
                category="Button",
                props=[
                    AtomicProp("loading", "boolean", required=False, default="false", description="加载状态"),
                    AtomicProp("onLogout", "() => Promise<void>", required=True, description="登出回调")
                ],
                ui=AtomicUISpec(
                    layout="按钮(红色,Outline风格)",
                    styles=["text-red-600", "border-red-600", "hover:bg-red-50"],
                    states=["idle", "loading", "error"]
                ),
                data={
                    "source": "props",
                    "contracts": ["onLogout必须返回Promise"]
                },
                interactions=[
                    AtomicInteraction("click", "调用onLogout() → 显示loading → 成功后跳转")
                ],
                dependencies=[],
                constraints=["防止重复点击(防抖)", "keyboard accessible (Enter/Space)"],
                edge_cases=["网络失败回滚", "重复点击防抖(500ms)"],
                acceptance=[
                    "点击后显示loading状态",
                    "成功后清除session",
                    "失败后显示错误提示",
                    "通过Playwright测试"
                ],
                examples=["顶部导航栏", "用户菜单"]
            )
        else:
            # 登录按钮
            return AtomicComponent(
                name="LoginButton",
                purpose="触发用户登录流程",
                component_type="UI",
                category="Button",
                props=[
                    AtomicProp("loading", "boolean", required=False, default="false"),
                    AtomicProp("disabled", "boolean", required=False, default="false"),
                    AtomicProp("onClick", "() => void", required=True)
                ],
                ui=AtomicUISpec(
                    layout="主按钮(Primary风格)",
                    styles=["bg-blue-600", "text-white", "hover:bg-blue-700"],
                    states=["idle", "loading", "disabled"]
                ),
                data={"source": "props"},
                interactions=[AtomicInteraction("click", "调用onClick()")],
                dependencies=[],
                constraints=["focus visible", "keyboard accessible"],
                edge_cases=["disabled状态不可点击"],
                acceptance=["点击触发登录", "disabled状态正确显示"],
                examples=["登录页面", "注册表单"]
            )

    def _generate_form_component_from_feature(self, feature: str) -> AtomicComponent:
        """从功能描述生成表单组件"""
        return AtomicComponent(
            name="DynamicForm",
            purpose=f"支持{feature}的动态表单",
            component_type="UI",
            category="Form",
            props=[
                AtomicProp("schema", "FormSchema", required=True, description="表单Schema"),
                AtomicProp("initialValues", "object", required=False, default="{}"),
                AtomicProp("onSubmit", "(values) => Promise<void>", required=True)
            ],
            ui=AtomicUISpec(
                layout="垂直布局,每个字段占一行",
                styles=["gap-4", "max-width-2xl"],
                states=["idle", "validating", "submitting", "error", "success"]
            ),
            data={
                "source": "schema + initialValues",
                "contracts": ["schema必须符合JSONSchema标准"]
            },
            interactions=[
                AtomicInteraction("input", "实时验证"),
                AtomicInteraction("submit", "调用onSubmit(values)")
            ],
            dependencies=["FormField", "Validation"],
            constraints=[
                "支持自定义验证规则",
                "错误提示国际化",
                "无障碍完整(label/error关联)"
            ],
            edge_cases=[
                "必填字段为空显示错误",
                "提交失败回滚",
                "长表单分步骤"
            ],
            acceptance=[
                "验证规则正确执行",
                "提交成功清空表单",
                "错误提示位置正确"
            ],
            examples=["创建用户", "编辑配置"]
        )

    def _generate_search_component(self, feature: str) -> AtomicComponent:
        """生成搜索组件"""
        return AtomicComponent(
            name="SearchBar",
            purpose="提供搜索和筛选功能",
            component_type="UI",
            category="Input",
            props=[
                AtomicProp("placeholder", "string", required=False, default="'搜索...'"),
                AtomicProp("onSearch", "(query: string) => void", required=True),
                AtomicProp("debounce", "number", required=False, default="300", description="防抖延迟(ms)")
            ],
            ui=AtomicUISpec(
                layout="输入框 + 搜索图标 + 清除按钮",
                styles=["border-gray-300", "rounded-lg", "px-4 py-2"],
                states=["idle", "typing", "searching"]
            ),
            data={
                "source": "props",
                "contracts": ["debounce必须>0"]
            },
            interactions=[
                AtomicInteraction("input", "防抖后触发onSearch"),
                AtomicInteraction("clear", "清空输入并触发onSearch('')")
            ],
            dependencies=[],
            constraints=["支持键盘快捷键(/或Cmd+K)", "focus自动选中"],
            edge_cases=["空查询返回全部", "特殊字符转义"],
            acceptance=["防抖正常工作", "清除按钮正确显示", "快捷键可用"],
            examples=["商品搜索", "用户筛选"]
        )

    def _generate_card_component(self, name: str, context: Dict) -> AtomicComponent:
        """生成通用卡片组件"""
        # TODO: 根据context生成具体卡片
        pass

    def _generate_button_component(self, name: str, context: Dict) -> AtomicComponent:
        """生成通用按钮组件"""
        # TODO: 根据context生成具体按钮
        pass

    def _generate_list_component(self, name: str, context: Dict) -> AtomicComponent:
        """生成通用列表组件"""
        # TODO: 根据context生成具体列表
        pass

    def _generate_modal_component(self, name: str, context: Dict) -> AtomicComponent:
        """生成通用模态框组件"""
        # TODO: 根据context生成具体模态框
        pass

    def _generate_nav_component(self, name: str, context: Dict) -> AtomicComponent:
        """生成通用导航组件"""
        # TODO: 根据context生成具体导航
        pass
