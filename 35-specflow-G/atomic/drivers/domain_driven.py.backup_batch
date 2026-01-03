"""
领域驱动模式

从DDD领域模型生成数据模型和业务逻辑组件
适用于:实体,值对象,聚合根,领域服务
"""

from typing import List, Dict


class DomainDrivenDriver:
    """领域驱动生成器"""

    def generate_from_domain_model(
        self,
        domain_model: Dict
    ) -> List[Dict]:
        """
        从领域模型生成数据模型和业务规则

        Args:
            domain_model: 领域模型数据

        Returns:
            List[Dict]: 数据模型列表
        """
        models = []

        # 从领域模型提取实体
        entities = domain_model.get("entities", [])
        value_objects = domain_model.get("value_objects", [])
        aggregates = domain_model.get("aggregates", [])

        # 生成实体模型
        for entity in entities:
            model = self._generate_entity_model(entity)
            models.append(model)

        # 生成值对象模型
        for vo in value_objects:
            model = self._generate_value_object_model(vo)
            models.append(model)

        # 生成聚合根模型
        for agg in aggregates:
            model = self._generate_aggregate_model(agg)
            models.append(model)

        # 如果没有明确的领域模型,从特征推断
        if not models:
            models = self._infer_models_from_context(domain_model)

        return models

    def _generate_entity_model(self, entity: Dict) -> Dict:
        """生成实体模型"""
        return {
            "type": "entity",
            "name": entity.get("name", "Entity"),
            "aggregate_root": entity.get("is_aggregate_root", False),
            "properties": entity.get("attributes", {}),
            "invariants": entity.get("business_rules", []),
            "methods": entity.get("operations", []),
            "events": entity.get("domain_events", [])
        }

    def _generate_value_object_model(self, vo: Dict) -> Dict:
        """生成值对象模型"""
        return {
            "type": "value_object",
            "name": vo.get("name", "ValueObject"),
            "properties": vo.get("attributes", {}),
            "validation": vo.get("validation_rules", []),
            "immutable": True
        }

    def _generate_aggregate_model(self, agg: Dict) -> Dict:
        """生成聚合根模型"""
        return {
            "type": "aggregate_root",
            "name": agg.get("name", "Aggregate"),
            "root_entity": agg.get("root", ""),
            "entities": agg.get("entities", []),
            "value_objects": agg.get("value_objects", []),
            "invariants": agg.get("invariants", []),
            "methods": agg.get("operations", [])
        }

    def _infer_models_from_context(self, domain_model: Dict) -> List[Dict]:
        """从上下文推断模型(如果没有明确的DDD结构)"""
        models = []

        # 从核心概念推断
        core_concepts = domain_model.get("core_concepts", [])

        # 典型的用户聚合根
        if any("用户" in concept or "user" in concept.lower() for concept in core_concepts):
            models.append(self._generate_user_aggregate())

        # 典型的产品/商品聚合根
        if any(keyword in "".join(core_concepts).lower() for keyword in ["产品", "商品", "product", "item"]):
            models.append(self._generate_product_aggregate())

        # 典型的订单聚合根
        if any(keyword in "".join(core_concepts).lower() for keyword in ["订单", "order"]):
            models.append(self._generate_order_aggregate())

        return models

    def _generate_user_aggregate(self) -> Dict:
        """生成用户聚合根模型"""
        return {
            "type": "aggregate_root",
            "name": "User",
            "root_entity": "User",
            "properties": {
                "id": {"type": "UUID", "description": "用户唯一标识"},
                "email": {"type": "Email", "description": "邮箱(值对象)"},
                "password_hash": {"type": "string", "description": "密码哈希"},
                "role": {"type": "UserRole", "description": "用户角色"},
                "profile": {"type": "UserProfile", "description": "用户资料"},
                "created_at": {"type": "timestamp", "description": "创建时间"},
                "updated_at": {"type": "timestamp", "description": "更新时间"}
            },
            "value_objects": [
                {
                    "name": "Email",
                    "properties": {"value": "string"},
                    "validation": ["必须符合邮箱格式", "不能为空"]
                },
                {
                    "name": "UserRole",
                    "properties": {"value": "enum"},
                    "allowed_values": ["admin", "staff", "viewer"]
                }
            ],
            "invariants": [
                "邮箱必须唯一",
                "密码至少8位,包含大小写字母+数字",
                "用户创建后email不可修改"
            ],
            "methods": [
                {
                    "name": "changeEmail",
                    "params": ["newEmail: Email"],
                    "logic": "验证邮箱唯一性 → 发送确认邮件 → 更新email"
                },
                {
                    "name": "changePassword",
                    "params": ["oldPassword: string", "newPassword: string"],
                    "logic": "验证旧密码 → 验证新密码强度 → 更新password_hash"
                },
                {
                    "name": "updateProfile",
                    "params": ["profile: UserProfile"],
                    "logic": "验证profile数据 → 更新profile → 触发ProfileUpdated事件"
                }
            ],
            "events": [
                "UserCreated",
                "UserEmailChanged",
                "UserPasswordChanged",
                "ProfileUpdated"
            ]
        }

    def _generate_product_aggregate(self) -> Dict:
        """生成产品聚合根模型"""
        return {
            "type": "aggregate_root",
            "name": "Product",
            "root_entity": "Product",
            "properties": {
                "id": {"type": "UUID"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "price": {"type": "Money"},
                "stock": {"type": "number"},
                "category": {"type": "string"},
                "status": {"type": "ProductStatus"}
            },
            "value_objects": [
                {
                    "name": "Money",
                    "properties": {"amount": "decimal", "currency": "string"},
                    "validation": ["amount必须>=0", "currency必须是ISO 4217代码"]
                },
                {
                    "name": "ProductStatus",
                    "properties": {"value": "enum"},
                    "allowed_values": ["draft", "active", "inactive", "deleted"]
                }
            ],
            "invariants": [
                "price必须>0",
                "stock不能为负数",
                "deleted状态不可销售"
            ],
            "methods": [
                {
                    "name": "updatePrice",
                    "params": ["newPrice: Money"],
                    "logic": "验证价格>0 → 更新price → 触发PriceChanged事件"
                },
                {
                    "name": "reduceStock",
                    "params": ["quantity: number"],
                    "logic": "检查库存充足 → 减少stock → 触发StockReduced事件"
                }
            ],
            "events": ["ProductCreated", "PriceChanged", "StockReduced", "ProductDeleted"]
        }

    def _generate_order_aggregate(self) -> Dict:
        """生成订单聚合根模型"""
        return {
            "type": "aggregate_root",
            "name": "Order",
            "root_entity": "Order",
            "properties": {
                "id": {"type": "UUID"},
                "user_id": {"type": "UUID"},
                "items": {"type": "OrderItem[]"},
                "total": {"type": "Money"},
                "status": {"type": "OrderStatus"},
                "created_at": {"type": "timestamp"}
            },
            "entities": [
                {
                    "name": "OrderItem",
                    "properties": {
                        "product_id": "UUID",
                        "quantity": "number",
                        "price": "Money"
                    }
                }
            ],
            "value_objects": [
                {
                    "name": "OrderStatus",
                    "properties": {"value": "enum"},
                    "allowed_values": ["pending", "paid", "shipped", "completed", "cancelled"]
                }
            ],
            "invariants": [
                "订单项不能为空",
                "total必须等于所有item的总和",
                "paid状态后不可修改items"
            ],
            "methods": [
                {
                    "name": "addItem",
                    "params": ["item: OrderItem"],
                    "logic": "检查订单状态=pending → 添加item → 重新计算total"
                },
                {
                    "name": "pay",
                    "params": [],
                    "logic": "验证支付信息 → 更新status=paid → 触发OrderPaid事件"
                }
            ],
            "events": ["OrderCreated", "OrderItemAdded", "OrderPaid", "OrderShipped", "OrderCompleted"]
        }

    def generate_database_schema(
        self,
        domain_models: List[Dict]
    ) -> Dict:
        """
        从领域模型生成数据库Schema

        Args:
            domain_models: 领域模型列表

        Returns:
            Dict: 数据库Schema
        """
        tables = []

        for model in domain_models:
            if model.get("type") in ["entity", "aggregate_root"]:
                table = self._model_to_table(model)
                tables.append(table)

        return {
            "tables": tables,
            "migrations": self._generate_migrations(tables)
        }

    def _model_to_table(self, model: Dict) -> Dict:
        """将领域模型转换为数据库表"""
        name = model.get("name", "").lower() + "s"
        properties = model.get("properties", {})

        columns = []
        for prop_name, prop_info in properties.items():
            if isinstance(prop_info, dict):
                prop_type = prop_info.get("type", "string")
            else:
                prop_type = prop_info

            column = {
                "name": prop_name,
                "type": self._map_type_to_sql(prop_type),
                "nullable": False,
                "primary_key": prop_name == "id"
            }
            columns.append(column)

        # 提取唯一约束
        invariants = model.get("invariants", [])
        unique_columns = []
        for invariant in invariants:
            if "唯一" in invariant or "unique" in invariant.lower():
                # 简单提取字段名(实际应该更智能)
                for col in columns:
                    if col["name"] in invariant:
                        unique_columns.append(col["name"])

        return {
            "name": name,
            "columns": columns,
            "unique_constraints": unique_columns,
            "indexes": [{"columns": [uc]} for uc in unique_columns]
        }

    def _map_type_to_sql(self, domain_type: str) -> str:
        """映射领域类型到SQL类型"""
        type_mapping = {
            "UUID": "UUID",
            "string": "VARCHAR(255)",
            "number": "INTEGER",
            "decimal": "DECIMAL(10,2)",
            "boolean": "BOOLEAN",
            "timestamp": "TIMESTAMP",
            "Email": "VARCHAR(255)",
            "Money": "DECIMAL(10,2)",
            "enum": "VARCHAR(50)"
        }
        return type_mapping.get(domain_type, "TEXT")

    def _generate_migrations(self, tables: List[Dict]) -> List[str]:
        """生成数据库迁移脚本"""
        migrations = []

        for table in tables:
            columns_sql = []
            for col in table["columns"]:
                col_sql = f"{col['name']} {col['type']}"
                if col.get("primary_key"):
                    col_sql += " PRIMARY KEY"
                if not col.get("nullable", True):
                    col_sql += " NOT NULL"
                columns_sql.append(col_sql)

            create_table = f"CREATE TABLE {table['name']} ({', '.join(columns_sql)})"
            migrations.append(create_table)

            # 添加唯一索引
            for idx in table.get("indexes", []):
                columns = idx.get("columns", [])
                if columns:
                    index_name = f"idx_{table['name']}_{'_'.join(columns)}"
                    create_index = f"CREATE UNIQUE INDEX {index_name} ON {table['name']}({', '.join(columns)})"
                    migrations.append(create_index)

        return migrations
