"""
BDD/ATDD场景生成器

使用模板生成Gherkin场景（无需AI）
"""

from core.models import FlowModel, DomainModel, GherkinScenario, AcceptanceCriteria, Priority


def generate_bdd_scenarios(flow: FlowModel, domain: DomainModel) -> list[GherkinScenario]:
    """
    生成Given-When-Then场景

    Args:
        flow: 流程模型
        domain: 领域模型

    Returns:
        list[GherkinScenario]: BDD场景列表
    """

    print("\n📝 生成BDD/ATDD场景...")
    print("-" * 60)

    scenarios = []

    # 为前8个P0/P1故事生成场景
    important_stories = [s for s in flow.user_stories if s.priority in [Priority.P0, Priority.P1]][:8]

    for story in important_stories:
        # 生成成功路径场景
        success_scenario = _generate_success_scenario(story, domain)
        scenarios.append(success_scenario)

        # 为P0故事生成异常路径场景
        if story.priority == Priority.P0:
            error_scenario = _generate_error_scenario(story, domain)
            scenarios.append(error_scenario)

    print(f"✅ 生成BDD场景: {len(scenarios)}个")

    return scenarios


def _generate_success_scenario(story, domain) -> GherkinScenario:
    """使用模板生成成功路径场景"""
    # 从故事描述中提取角色
    actor = "用户"
    if "作为" in story.description:
        parts = story.description.split("作为")
        if len(parts) > 1:
            actor_part = parts[1].split("，")[0].split(",")[0]
            actor = actor_part.strip()

    # 根据故事阶段选择场景模板
    if "登录" in story.title or "注册" in story.title or "准备" in story.stage:
        given = ["系统处于就绪状态", f"{actor}拥有有效的账户信息"]
        when = [f"{actor}提交{story.title}请求", "系统验证输入数据"]
        then = ["验证通过", "系统完成操作", f"{actor}收到成功反馈"]
    elif "配置" in story.title or "设置" in story.title or "配置" in story.stage:
        given = [f"{actor}已登录系统", "系统允许配置操作"]
        when = [f"{actor}打开{story.title}界面", f"{actor}修改配置参数", "保存配置"]
        then = ["配置保存成功", "系统应用新配置", f"{actor}看到更新后的设置"]
    elif "查看" in story.title or "监控" in story.title or "完成" in story.stage:
        given = [f"{actor}已登录系统", "系统中存在相关数据"]
        when = [f"{actor}请求查看{story.title}数据", "系统检索数据"]
        then = ["数据检索成功", "系统展示数据", f"{actor}看到正确的信息"]
    else:
        # 默认模板（执行类操作）
        given = [f"{actor}已登录系统", "系统处于就绪状态", "必要的前置条件已满足"]
        when = [f"{actor}发起{story.title}操作", "系统处理请求", "系统验证数据"]
        then = ["处理成功", "系统保存结果", f"{actor}收到成功通知"]

    return GherkinScenario(
        feature=story.title,
        scenario=f"{story.title} - 成功路径",
        as_a=actor,
        i_want=f"完成{story.title}",
        so_that="达成业务目标",
        given=given,
        when=when,
        then=then
    )


def _generate_error_scenario(story, domain) -> GherkinScenario:
    """使用模板生成异常路径场景"""
    actor = "用户"
    if "作为" in story.description:
        parts = story.description.split("作为")
        if len(parts) > 1:
            actor_part = parts[1].split("，")[0].split(",")[0]
            actor = actor_part.strip()

    # 通用异常场景模板
    given = [f"{actor}已登录系统", "系统处于就绪状态"]
    when = [f"{actor}提交无效的{story.title}请求", "系统检测到数据错误"]
    then = ["系统拒绝请求", "返回错误提示", f"{actor}看到友好的错误信息", "系统状态保持一致"]

    return GherkinScenario(
        feature=story.title,
        scenario=f"{story.title} - 异常处理",
        as_a=actor,
        i_want=f"系统能正确处理{story.title}的异常情况",
        so_that="保证系统稳定性",
        given=given,
        when=when,
        then=then
    )


def generate_acceptance_criteria(flow: FlowModel) -> list[AcceptanceCriteria]:
    """
    生成验收标准

    Args:
        flow: 流程模型

    Returns:
        list[AcceptanceCriteria]: 验收标准列表
    """

    criteria_list = []

    for story in flow.user_stories:
        # 基于优先级生成不同的验收标准
        if story.priority == Priority.P0:
            criteria = AcceptanceCriteria(
                story_id=story.id,
                criteria=[
                    f"✅ AC1: {story.title}功能正常运行，无阻塞性bug",
                    f"✅ AC2: 成功路径测试通过率100%",
                    f"✅ AC3: 异常处理正确，系统不崩溃",
                    f"✅ AC4: 性能符合要求（响应时间<2秒）",
                    f"✅ AC5: 用户界面友好，操作流畅"
                ]
            )
        else:
            criteria = AcceptanceCriteria(
                story_id=story.id,
                criteria=[
                    f"✅ AC1: {story.title}功能正常运行",
                    f"✅ AC2: 主要测试场景通过",
                    f"✅ AC3: 基本错误处理正确"
                ]
            )

        criteria_list.append(criteria)

    return criteria_list
