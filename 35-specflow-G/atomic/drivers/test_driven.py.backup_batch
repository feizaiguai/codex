"""
测试驱动模式

从BDD场景反推原子组件和验收标准
适用于:功能验证,场景测试,验收标准定义
"""

from typing import List, Dict
from ..schema import AtomicComponent, AtomicProp, AtomicUISpec, AtomicInteraction


class TestDrivenDriver:
    """测试驱动生成器"""

    def generate_from_bdd(
        self,
        bdd_scenarios: List[Dict]
    ) -> List[AtomicComponent]:
        """
        从BDD场景生成原子组件

        Args:
            bdd_scenarios: BDD场景列表

        Returns:
            List[AtomicComponent]: 原子组件列表(补充测试驱动的验收标准)
        """
        components = []

        for scenario in bdd_scenarios:
            feature_name = scenario.get("feature", "")
            scenario_name = scenario.get("scenario", "")
            steps = scenario.get("steps", [])

            # 解析Given-When-Then
            given_steps = [s for s in steps if s.startswith("Given")]
            when_steps = [s for s in steps if s.startswith("When")]
            then_steps = [s for s in steps if s.startswith("Then")]

            # 从When步骤推断组件
            for when_step in when_steps:
                component = self._infer_component_from_step(
                    when_step,
                    given_steps,
                    then_steps,
                    scenario_name
                )
                if component:
                    components.append(component)

        return components

    def _infer_component_from_step(
        self,
        when_step: str,
        given_steps: List[str],
        then_steps: List[str],
        scenario_name: str
    ) -> AtomicComponent:
        """从When步骤推断组件"""

        when_lower = when_step.lower()

        # 登出场景
        if "登出" in when_step or "logout" in when_lower:
            return self._generate_logout_component(given_steps, then_steps, scenario_name)

        # 登录场景
        if "登录" in when_step or "login" in when_lower:
            return self._generate_login_component(given_steps, then_steps, scenario_name)

        # 提交表单场景
        if "提交" in when_step or "submit" in when_lower:
            return self._generate_submit_component(given_steps, then_steps, scenario_name)

        # 点击按钮场景
        if "点击" in when_step or "click" in when_lower:
            return self._generate_button_component(when_step, given_steps, then_steps)

        return None

    def _generate_logout_component(
        self,
        given_steps: List[str],
        then_steps: List[str],
        scenario_name: str
    ) -> AtomicComponent:
        """生成登出按钮组件(测试驱动版本)"""

        # 从Then步骤提取验收标准
        acceptance = []
        for then_step in then_steps:
            # 去掉"Then "前缀
            criterion = then_step.replace("Then ", "").strip()
            acceptance.append(criterion)

        # 如果没有明确验收标准,使用默认值
        if not acceptance:
            acceptance = [
                "点击后显示loading状态",
                "成功后清除session",
                "成功后跳转到登录页",
                "失败后显示错误提示",
                "通过Playwright测试"
            ]

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
            constraints=["防止重复点击(防抖)", "keyboard accessible"],
            edge_cases=["网络失败回滚", "重复点击防抖(500ms)"],
            acceptance=acceptance,  # 使用从BDD提取的验收标准
            telemetry={"log": True, "fields": ["logoutDuration", "errorRate"]},
            examples=[scenario_name]
        )

    def _generate_login_component(
        self,
        given_steps: List[str],
        then_steps: List[str],
        scenario_name: str
    ) -> AtomicComponent:
        """生成登录表单组件(测试驱动版本)"""

        # 从Then步骤提取验收标准
        acceptance = [step.replace("Then ", "").strip() for step in then_steps]

        return AtomicComponent(
            name="LoginForm",
            purpose="用户登录认证表单",
            component_type="UI",
            category="Form",
            props=[
                AtomicProp("onSubmit", "(credentials) => Promise<void>", required=True),
                AtomicProp("loading", "boolean", required=False, default="false")
            ],
            ui=AtomicUISpec(
                layout="垂直布局:邮箱输入 + 密码输入 + 登录按钮",
                styles=["gap-4", "max-w-md"],
                states=["idle", "validating", "submitting", "error"]
            ),
            data={
                "source": "form inputs",
                "contracts": ["邮箱格式验证", "密码长度>=8"]
            },
            interactions=[
                AtomicInteraction("submit", "验证表单 → 调用onSubmit → 处理结果")
            ],
            dependencies=["FormField", "Button"],
            constraints=["支持Enter提交", "错误提示清晰", "password字段隐藏"],
            edge_cases=[
                "邮箱格式错误显示提示",
                "密码过短显示提示",
                "登录失败显示错误",
                "网络超时重试"
            ],
            acceptance=acceptance if acceptance else [
                "邮箱格式验证正常",
                "密码长度验证正常",
                "登录成功跳转",
                "登录失败显示错误"
            ],
            examples=[scenario_name]
        )

    def _generate_submit_component(
        self,
        given_steps: List[str],
        then_steps: List[str],
        scenario_name: str
    ) -> AtomicComponent:
        """生成提交按钮组件"""

        acceptance = [step.replace("Then ", "").strip() for step in then_steps]

        return AtomicComponent(
            name="SubmitButton",
            purpose="表单提交按钮",
            component_type="UI",
            category="Button",
            props=[
                AtomicProp("loading", "boolean", required=False, default="false"),
                AtomicProp("disabled", "boolean", required=False, default="false"),
                AtomicProp("onClick", "() => void", required=True),
                AtomicProp("label", "string", required=False, default="'提交'")
            ],
            ui=AtomicUISpec(
                layout="主按钮(Primary风格)",
                styles=["bg-blue-600", "text-white", "px-6 py-2"],
                states=["idle", "loading", "disabled"]
            ),
            data={"source": "props"},
            interactions=[
                AtomicInteraction("click", "调用onClick()")
            ],
            dependencies=[],
            constraints=["loading时禁用", "disabled时不触发onClick"],
            edge_cases=["重复点击防抖"],
            acceptance=acceptance if acceptance else [
                "点击触发onClick",
                "loading状态显示spinner",
                "disabled状态不可点击"
            ],
            examples=[scenario_name]
        )

    def _generate_button_component(
        self,
        when_step: str,
        given_steps: List[str],
        then_steps: List[str]
    ) -> AtomicComponent:
        """从点击步骤生成通用按钮组件"""

        # 提取按钮名称
        import re
        match = re.search(r'点击["""\'](.*?)["""\']', when_step)
        button_label = match.group(1) if match else "Button"

        acceptance = [step.replace("Then ", "").strip() for step in then_steps]

        return AtomicComponent(
            name=f"{button_label.replace(' ', '')}Button",
            purpose=f"触发{button_label}操作",
            component_type="UI",
            category="Button",
            props=[
                AtomicProp("onClick", "() => void", required=True),
                AtomicProp("disabled", "boolean", required=False, default="false")
            ],
            ui=AtomicUISpec(
                layout="按钮",
                styles=["px-4 py-2"],
                states=["idle", "disabled"]
            ),
            data={"source": "props"},
            interactions=[
                AtomicInteraction("click", "调用onClick()")
            ],
            dependencies=[],
            constraints=["keyboard accessible"],
            edge_cases=["disabled状态不可点击"],
            acceptance=acceptance if acceptance else ["点击触发操作"],
            examples=[when_step]
        )

    def enhance_components_with_bdd(
        self,
        components: List[AtomicComponent],
        bdd_scenarios: List[Dict]
    ) -> List[AtomicComponent]:
        """
        为已有组件增强BDD验收标准

        Args:
            components: 现有组件列表
            bdd_scenarios: BDD场景列表

        Returns:
            List[AtomicComponent]: 增强后的组件列表
        """
        # 为每个组件匹配相关BDD场景
        for component in components:
            related_scenarios = self._find_related_scenarios(component, bdd_scenarios)

            # 从相关场景提取额外的验收标准
            for scenario in related_scenarios:
                steps = scenario.get("steps", [])
                then_steps = [s for s in steps if s.startswith("Then")]

                for then_step in then_steps:
                    criterion = then_step.replace("Then ", "").strip()
                    if criterion and criterion not in component.acceptance:
                        component.acceptance.append(criterion)

        return components

    def _find_related_scenarios(
        self,
        component: AtomicComponent,
        bdd_scenarios: List[Dict]
    ) -> List[Dict]:
        """查找与组件相关的BDD场景"""
        related = []

        # 简单匹配:场景名称包含组件名称关键词
        component_keywords = component.name.lower().replace("button", "").replace("form", "").replace("component", "")

        for scenario in bdd_scenarios:
            scenario_text = scenario.get("scenario", "").lower() + scenario.get("feature", "").lower()
            if component_keywords in scenario_text:
                related.append(scenario)

        return related
