"""
Layer 2: Flow Modeling（流程与事件）

使用启发式规则识别事件和用户故事（无需AI）
"""

from core.models import ClarifiedContext, ImpactModel, FlowModel, DomainEvent, JourneyStage, UserStory, Priority


def analyze_flow(context: ClarifiedContext, impact: ImpactModel) -> FlowModel:
    """
    构建流程模型

    Args:
        context: 澄清后的需求上下文
        impact: Impact Mapping模型

    Returns:
        FlowModel: 流程模型
    """

    print("\n🔄 Layer 2: Flow Modeling（流程与事件）")
    print("-" * 60)

    # Event Storming - 使用启发式规则
    events = _identify_events(context, impact)

    # User Story Mapping - 基于规则划分阶段
    journey_stages = _map_user_journey(context, impact)
    user_stories = _generate_user_stories(context, journey_stages, impact)

    # 更新journey_stages的stories字段
    for story in user_stories:
        for stage in journey_stages:
            if stage.name == story.stage:
                stage.stories.append(story.id)

    model = FlowModel(
        events=events,
        journey_stages=journey_stages,
        user_stories=user_stories
    )

    print(f"✅ 领域事件: {len(events)}个")
    print(f"✅ 旅程阶段: {len(journey_stages)}个")
    print(f"✅ 用户故事: {len(user_stories)}个")

    return model


def _identify_events(context: ClarifiedContext, impact: ImpactModel) -> list[DomainEvent]:
    """使用启发式规则识别领域事件"""
    events = []

    # 规则1：从交付物生成事件
    for deliverable in impact.deliverables[:8]:
        # 提取核心功能名（优先取冒号前的部分，否则取前10个字符）
        core_name = deliverable
        if "：" in deliverable or ":" in deliverable:
            core_name = deliverable.split("：")[0].split(":")[0].strip()
        elif len(deliverable) > 15:
            # 如果太长，取前10个字符
            core_name = deliverable[:10]

        # 去除标点符号和停用词
        core_name = core_name.replace(" ", "").replace("模块", "").replace("功能", "").replace("、", "").replace("，", "")

        event_name = core_name + "Completed"
        trigger_name = "Complete" + core_name
        events.append(DomainEvent(
            name=event_name,
            trigger=trigger_name,
            description=f"当{deliverable}完成时触发"
        ))

    # 规则2：如果事件少于5个，添加通用事件
    if len(events) < 5:
        generic_events = [
            ("ProcessStarted", "StartProcess", "流程启动"),
            ("DataValidated", "ValidateData", "数据验证完成"),
            ("ResultGenerated", "GenerateResult", "结果生成"),
            ("NotificationSent", "SendNotification", "通知发送")
        ]
        for name, trigger, desc in generic_events[:5-len(events)]:
            events.append(DomainEvent(name=name, trigger=trigger, description=desc))

    return events[:10]  # 最多10个


def _map_user_journey(context: ClarifiedContext, impact: ImpactModel) -> list[JourneyStage]:
    """使用规则划分用户旅程"""
    num_deliverables = len(impact.deliverables)

    if num_deliverables <= 3:
        return [
            JourneyStage(name="准备阶段", stories=[]),
            JourneyStage(name="执行阶段", stories=[]),
            JourneyStage(name="完成阶段", stories=[])
        ]
    elif num_deliverables <= 6:
        return [
            JourneyStage(name="注册/登录", stories=[]),
            JourneyStage(name="配置", stories=[]),
            JourneyStage(name="核心操作", stories=[]),
            JourneyStage(name="查看结果", stories=[])
        ]
    else:
        return [
            JourneyStage(name="启动", stories=[]),
            JourneyStage(name="配置", stories=[]),
            JourneyStage(name="执行", stories=[]),
            JourneyStage(name="监控", stories=[]),
            JourneyStage(name="完成", stories=[])
        ]


def _generate_user_stories(context: ClarifiedContext, stages: list[JourneyStage], impact: ImpactModel) -> list[UserStory]:
    """基于规则生成用户故事"""
    stories = []
    story_id = 1

    # 为每个阶段生成2-3个故事
    stories_per_stage = 2 if len(stages) > 4 else 3

    for stage in stages:
        for j in range(stories_per_stage):
            # 从角色中循环选择
            actor = impact.actors[j % len(impact.actors)].name if impact.actors else "用户"

            # 生成故事
            story = UserStory(
                id=f"US-{story_id:03d}",
                title=f"{stage.name}相关功能{j+1}",
                description=f"作为{actor}，我想完成{stage.name}的操作，以便达成业务目标",
                priority=Priority.P0 if story_id <= 5 else Priority.P1,
                stage=stage.name
            )
            stories.append(story)
            story_id += 1

            if story_id > 15:  # 最多15个故事
                break

        if story_id > 15:
            break

    return stories
