"""
Layer 3: Domain Modeling（结构与实体）

使用启发式规则识别实体、值对象、聚合根和限界上下文（无需AI）
"""

from core.models import ClarifiedContext, FlowModel, DomainModel, Entity, ValueObject, Aggregate, BoundedContext


def analyze_domain(context: ClarifiedContext, flow: FlowModel) -> DomainModel:
    """
    构建领域模型

    Args:
        context: 澄清后的需求上下文
        flow: 流程模型

    Returns:
        DomainModel: 领域模型
    """

    print("\n🏗️  Layer 3: Domain Modeling（结构与实体）")
    print("-" * 60)

    # 使用规则识别各层元素
    entities = _identify_entities(flow)
    value_objects = _identify_value_objects(entities)
    aggregates = _identify_aggregates(entities)
    bounded_contexts = _identify_bounded_contexts(entities, flow, context)

    model = DomainModel(
        entities=entities,
        value_objects=value_objects,
        aggregates=aggregates,
        bounded_contexts=bounded_contexts
    )

    print(f"✅ 核心实体: {len(entities)}个")
    print(f"✅ 值对象: {len(value_objects)}个")
    print(f"✅ 聚合根: {len(aggregates)}个")
    print(f"✅ 限界上下文: {len(bounded_contexts)}个")

    return model


def _identify_entities(flow: FlowModel) -> list[Entity]:
    """使用规则从事件中提取实体"""
    entities = []
    seen = set()

    # 规则1：从事件名称中提取实体
    for event in flow.events:
        name = event.name.replace("Completed", "").replace("Started", "").replace("Created", "").strip()
        if name and name not in seen:
            entities.append(Entity(
                name=name,
                attributes=["id", "name", "status", "createdAt", "updatedAt"],
                behaviors=["create()", "update()", "delete()", "validate()"],
                description=f"从事件{event.name}提取的实体"
            ))
            seen.add(name)

    # 规则2：如果实体少于3个，添加通用实体
    if len(entities) < 3:
        generic_entities = [
            ("User", ["id", "username", "email", "role", "createdAt"], ["login()", "logout()", "updateProfile()", "resetPassword()"]),
            ("Session", ["id", "userId", "token", "expiresAt", "createdAt"], ["create()", "validate()", "revoke()", "refresh()"]),
            ("Record", ["id", "data", "type", "status", "timestamp"], ["save()", "retrieve()", "update()", "archive()"])
        ]
        for name, attrs, behaviors in generic_entities[:3 - len(entities)]:
            if name not in seen:
                entities.append(Entity(name=name, attributes=attrs, behaviors=behaviors, description="通用实体"))
                seen.add(name)

    return entities[:8]  # 最多8个实体


def _identify_value_objects(entities: list[Entity]) -> list[ValueObject]:
    """基于实体识别值对象"""
    value_objects = []

    # 规则：为每个实体生成1个值对象（基于实体的属性）
    for entity in entities[:5]:  # 最多5个
        vo_name = f"{entity.name}Info"
        value_objects.append(ValueObject(
            name=vo_name,
            fields=entity.attributes[:3] if len(entity.attributes) >= 3 else entity.attributes,
            description=f"{entity.name}的值对象表示"
        ))

    # 添加通用值对象
    if len(value_objects) < 3:
        value_objects.extend([
            ValueObject(name="Status", fields=["code", "message", "timestamp"], description="状态值对象"),
            ValueObject(name="Address", fields=["street", "city", "country"], description="地址值对象")
        ])

    return value_objects[:5]


def _identify_aggregates(entities: list[Entity]) -> list[Aggregate]:
    """基于实体识别聚合根"""
    aggregates = []

    if not entities:
        return aggregates

    # 规则：每2-3个实体组成1个聚合
    for i in range(0, min(len(entities), 6), 3):
        root_entity = entities[i]
        contained = [e.name for e in entities[i+1:min(i+3, len(entities))]]

        aggregates.append(Aggregate(
            root=root_entity.name,
            entities=contained,
            invariants=[
                f"{root_entity.name}必须有效",
                f"{root_entity.name}的状态必须一致"
            ],
            description=f"以{root_entity.name}为根的聚合"
        ))

    return aggregates[:3]  # 最多3个聚合


def _identify_bounded_contexts(entities: list[Entity], flow: FlowModel, context: ClarifiedContext) -> list[BoundedContext]:
    """基于实体数量和业务逻辑划分限界上下文"""
    bounded_contexts = []
    num_entities = len(entities)

    if num_entities <= 3:
        # 简单项目：单一上下文
        bounded_contexts.append(BoundedContext(
            name="核心业务上下文",
            entities=[e.name for e in entities],
            responsibilities="处理所有核心业务逻辑"
        ))
    elif num_entities <= 6:
        # 中等项目：2个上下文
        mid = num_entities // 2
        bounded_contexts.extend([
            BoundedContext(
                name="核心业务上下文",
                entities=[e.name for e in entities[:mid]],
                responsibilities="处理核心业务流程和主要功能"
            ),
            BoundedContext(
                name="支持服务上下文",
                entities=[e.name for e in entities[mid:]],
                responsibilities="提供支持性服务和辅助功能"
            )
        ])
    else:
        # 复杂项目：3个上下文
        third = num_entities // 3
        bounded_contexts.extend([
            BoundedContext(
                name="核心业务上下文",
                entities=[e.name for e in entities[:third]],
                responsibilities="核心业务逻辑和领域规则"
            ),
            BoundedContext(
                name="用户管理上下文",
                entities=[e.name for e in entities[third:third*2]],
                responsibilities="用户认证、授权和个人信息管理"
            ),
            BoundedContext(
                name="系统支持上下文",
                entities=[e.name for e in entities[third*2:]],
                responsibilities="系统配置、监控和辅助服务"
            )
        ])

    return bounded_contexts
