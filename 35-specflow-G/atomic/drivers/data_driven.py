"""
数据驱动模式

从数据模型生成数据库Schema和迁移脚本
适用于:数据库设计,ORM模型,数据迁移
"""

from typing import List, Dict


class DataDrivenDriver:
    """数据驱动生成器"""

    def generate_database_schema(
        self,
        domain_models: List[Dict]
    ) -> Dict:
        """
        从领域模型生成数据库Schema

        Args:
            domain_models: 领域模型列表

        Returns:
            Dict: 数据库Schema(包括表,索引,迁移脚本)
        """
        tables = []
        relations = []

        for model in domain_models:
            model_type = model.get("type", "entity")

            if model_type in ["entity", "aggregate_root"]:
                table = self._generate_table_from_model(model)
                tables.append(table)

                # 识别关系
                model_relations = self._extract_relations(model)
                relations.extend(model_relations)

        return {
            "database": {
                "type": "PostgreSQL",  # 默认使用PostgreSQL
                "tables": tables,
                "relations": relations,
                "indexes": self._generate_indexes(tables),
                "constraints": self._generate_constraints(tables, relations)
            },
            "migrations": {
                "up": self._generate_up_migrations(tables, relations),
                "down": self._generate_down_migrations(tables)
            },
            "orm_models": self._generate_orm_models(tables, relations)
        }

    def _generate_table_from_model(self, model: Dict) -> Dict:
        """从领域模型生成表结构"""
        name = model.get("name", "").lower()
        if not name.endswith('s'):
            name += "s"

        properties = model.get("properties", {})
        columns = []

        # 自动添加id列
        columns.append({
            "name": "id",
            "type": "UUID",
            "primary_key": True,
            "nullable": False,
            "default": "gen_random_uuid()"
        })

        # 从properties生成列
        for prop_name, prop_info in properties.items():
            if prop_name == "id":
                continue  # 跳过,已经添加

            if isinstance(prop_info, dict):
                column = self._property_to_column(prop_name, prop_info)
            else:
                column = self._property_to_column(prop_name, {"type": prop_info})

            columns.append(column)

        # 自动添加时间戳
        if not any(col["name"] in ["created_at", "updated_at"] for col in columns):
            columns.append({
                "name": "created_at",
                "type": "TIMESTAMP",
                "nullable": False,
                "default": "CURRENT_TIMESTAMP"
            })
            columns.append({
                "name": "updated_at",
                "type": "TIMESTAMP",
                "nullable": False,
                "default": "CURRENT_TIMESTAMP"
            })

        return {
            "name": name,
            "columns": columns,
            "comment": f"{model.get('name', '')} table"
        }

    def _property_to_column(self, name: str, prop_info: Dict) -> Dict:
        """将属性转换为列定义"""
        prop_type = prop_info.get("type", "string")
        sql_type = self._map_type_to_sql(prop_type)

        column = {
            "name": name,
            "type": sql_type,
            "nullable": not prop_info.get("required", False),
            "description": prop_info.get("description", "")
        }

        # 添加默认值
        if "default" in prop_info:
            column["default"] = prop_info["default"]

        # 添加唯一约束
        if prop_info.get("unique", False):
            column["unique"] = True

        return column

    def _map_type_to_sql(self, domain_type: str) -> str:
        """映射领域类型到SQL类型"""
        type_mapping = {
            "UUID": "UUID",
            "string": "VARCHAR(255)",
            "text": "TEXT",
            "number": "INTEGER",
            "integer": "INTEGER",
            "decimal": "DECIMAL(10,2)",
            "float": "FLOAT",
            "boolean": "BOOLEAN",
            "timestamp": "TIMESTAMP",
            "date": "DATE",
            "time": "TIME",
            "json": "JSONB",
            "array": "TEXT[]",
            # 值对象类型
            "Email": "VARCHAR(255)",
            "Money": "DECIMAL(10,2)",
            "Phone": "VARCHAR(20)",
            "URL": "TEXT",
            "enum": "VARCHAR(50)",
            # 特殊类型
            "UserRole": "VARCHAR(50)",
            "ProductStatus": "VARCHAR(50)",
            "OrderStatus": "VARCHAR(50)"
        }
        return type_mapping.get(domain_type, "TEXT")

    def _extract_relations(self, model: Dict) -> List[Dict]:
        """从模型提取关系"""
        relations = []
        name = model.get("name", "").lower()
        properties = model.get("properties", {})

        for prop_name, prop_info in properties.items():
            if isinstance(prop_info, dict):
                prop_type = prop_info.get("type", "")
            else:
                prop_type = prop_info

            # 检测外键(ID结尾)
            if prop_name.endswith("_id") and "UUID" in prop_type:
                related_table = prop_name[:-3]  # 去掉_id
                if not related_table.endswith('s'):
                    related_table += "s"

                relations.append({
                    "from_table": name + "s" if not name.endswith('s') else name,
                    "from_column": prop_name,
                    "to_table": related_table,
                    "to_column": "id",
                    "type": "many_to_one"
                })

        return relations

    def _generate_indexes(self, tables: List[Dict]) -> List[Dict]:
        """生成索引"""
        indexes = []

        for table in tables:
            table_name = table["name"]

            for column in table["columns"]:
                col_name = column["name"]

                # 主键自动索引,跳过
                if column.get("primary_key"):
                    continue

                # 为外键创建索引
                if col_name.endswith("_id"):
                    indexes.append({
                        "name": f"idx_{table_name}_{col_name}",
                        "table": table_name,
                        "columns": [col_name],
                        "type": "btree"
                    })

                # 为唯一列创建唯一索引
                if column.get("unique"):
                    indexes.append({
                        "name": f"idx_{table_name}_{col_name}_unique",
                        "table": table_name,
                        "columns": [col_name],
                        "type": "btree",
                        "unique": True
                    })

            # 为created_at创建索引(常用于排序)
            if any(col["name"] == "created_at" for col in table["columns"]):
                indexes.append({
                    "name": f"idx_{table_name}_created_at",
                    "table": table_name,
                    "columns": ["created_at"],
                    "type": "btree"
                })

        return indexes

    def _generate_constraints(self, tables: List[Dict], relations: List[Dict]) -> List[Dict]:
        """生成约束"""
        constraints = []

        # 外键约束
        for relation in relations:
            constraints.append({
                "name": f"fk_{relation['from_table']}_{relation['from_column']}",
                "type": "foreign_key",
                "table": relation["from_table"],
                "column": relation["from_column"],
                "ref_table": relation["to_table"],
                "ref_column": relation["to_column"],
                "on_delete": "CASCADE",
                "on_update": "CASCADE"
            })

        return constraints

    def _generate_up_migrations(self, tables: List[Dict], relations: List[Dict]) -> List[str]:
        """生成UP迁移脚本"""
        migrations = []

        # 启用UUID扩展
        migrations.append("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

        # 创建表
        for table in tables:
            columns_sql = []

            for col in table["columns"]:
                col_sql = f"{col['name']} {col['type']}"

                if col.get("primary_key"):
                    col_sql += " PRIMARY KEY"

                if not col.get("nullable", True):
                    col_sql += " NOT NULL"

                if "default" in col:
                    col_sql += f" DEFAULT {col['default']}"

                if col.get("unique"):
                    col_sql += " UNIQUE"

                columns_sql.append(col_sql)

            create_table = f"CREATE TABLE {table['name']} (\n  " + ",\n  ".join(columns_sql) + "\n);"
            migrations.append(create_table)

            # 添加表注释
            if table.get("comment"):
                migrations.append(f"COMMENT ON TABLE {table['name']} IS '{table['comment']}';")

        # 添加外键
        for relation in relations:
            alter_table = f"""ALTER TABLE {relation['from_table']}
ADD CONSTRAINT fk_{relation['from_table']}_{relation['from_column']}
FOREIGN KEY ({relation['from_column']})
REFERENCES {relation['to_table']}({relation['to_column']})
ON DELETE CASCADE
ON UPDATE CASCADE;"""
            migrations.append(alter_table)

        # 创建索引
        indexes = self._generate_indexes(tables)
        for idx in indexes:
            unique = "UNIQUE " if idx.get("unique") else ""
            create_index = f"CREATE {unique}INDEX {idx['name']} ON {idx['table']}({', '.join(idx['columns'])});"
            migrations.append(create_index)

        return migrations

    def _generate_down_migrations(self, tables: List[Dict]) -> List[str]:
        """生成DOWN迁移脚本"""
        migrations = []

        # 按相反顺序删除表
        for table in reversed(tables):
            migrations.append(f"DROP TABLE IF EXISTS {table['name']} CASCADE;")

        return migrations

    def _generate_orm_models(self, tables: List[Dict], relations: List[Dict]) -> Dict:
        """生成ORM模型代码"""
        models = {}

        for table in tables:
            table_name = table["name"]
            class_name = self._table_name_to_class_name(table_name)

            # 生成字段
            fields = []
            for col in table["columns"]:
                field_type = self._sql_to_orm_type(col["type"])
                field_def = f"{col['name']}: {field_type}"

                if col.get("primary_key"):
                    field_def += " (Primary Key)"
                if not col.get("nullable", True):
                    field_def += " (Required)"
                if col.get("unique"):
                    field_def += " (Unique)"

                fields.append(field_def)

            # 生成关系
            related_fields = []
            for rel in relations:
                if rel["from_table"] == table_name:
                    related_class = self._table_name_to_class_name(rel["to_table"])
                    related_fields.append(f"{rel['from_column'][:-3]}: {related_class}")

            models[class_name] = {
                "table": table_name,
                "fields": fields,
                "relations": related_fields
            }

        return models

    def _table_name_to_class_name(self, table_name: str) -> str:
        """表名转换为类名"""
        # users -> User
        name = table_name.rstrip('s')
        return name.capitalize()

    def _sql_to_orm_type(self, sql_type: str) -> str:
        """SQL类型转换为ORM类型"""
        type_mapping = {
            "UUID": "UUID",
            "VARCHAR": "String",
            "TEXT": "Text",
            "INTEGER": "Integer",
            "DECIMAL": "Decimal",
            "FLOAT": "Float",
            "BOOLEAN": "Boolean",
            "TIMESTAMP": "DateTime",
            "DATE": "Date",
            "TIME": "Time",
            "JSONB": "JSON"
        }

        for sql, orm in type_mapping.items():
            if sql in sql_type:
                return orm

        return "String"
