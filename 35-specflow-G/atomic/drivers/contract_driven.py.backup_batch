"""
契约驱动模式

从API契约生成接口规格和集成测试
适用于:RESTful API,GraphQL,gRPC等
"""

from typing import List, Dict


class ContractDrivenDriver:
    """契约驱动生成器"""

    def generate_api_specs(
        self,
        api_design: Dict
    ) -> List[Dict]:
        """
        从API设计生成OpenAPI规格

        Args:
            api_design: API设计数据

        Returns:
            List[Dict]: API规格列表
        """
        specs = []

        # 从功能推断API端点
        features = api_design.get("features", [])
        entities = api_design.get("entities", [])

        # 为每个实体生成CRUD端点
        for entity in entities:
            entity_specs = self._generate_entity_endpoints(entity)
            specs.extend(entity_specs)

        # 为特定功能生成自定义端点
        for feature in features:
            custom_specs = self._generate_feature_endpoints(feature)
            if custom_specs:
                specs.extend(custom_specs)

        # 如果没有明确的设计,生成默认端点
        if not specs:
            specs = self._generate_default_endpoints()

        return specs

    def _generate_entity_endpoints(self, entity: str) -> List[Dict]:
        """为实体生成CRUD端点"""
        entity_lower = entity.lower()
        entity_path = f"/{entity_lower}s"

        return [
            # GET /entities - 列表
            {
                "endpoint": entity_path,
                "method": "GET",
                "summary": f"获取{entity}列表",
                "request": {
                    "query_params": {
                        "page": {"type": "number", "default": 1},
                        "limit": {"type": "number", "default": 20},
                        "sort": {"type": "string", "optional": True},
                        "filter": {"type": "object", "optional": True}
                    },
                    "headers": {
                        "Authorization": "Bearer {token}"
                    }
                },
                "response": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "data": f"{entity}[]",
                            "total": "number",
                            "page": "number",
                            "limit": "number"
                        }
                    },
                    "401": {"error": "Unauthorized"},
                    "500": {"error": "Internal Server Error"}
                },
                "contract_tests": [
                    "正常请求返回200",
                    "无token返回401",
                    "分页参数正确工作",
                    "过滤参数正确工作"
                ]
            },
            # GET /entities/:id - 详情
            {
                "endpoint": f"{entity_path}/{{id}}",
                "method": "GET",
                "summary": f"获取{entity}详情",
                "request": {
                    "path_params": {"id": "UUID"},
                    "headers": {"Authorization": "Bearer {token}"}
                },
                "response": {
                    "200": {
                        "description": "成功",
                        "schema": {
                            "id": "UUID",
                            "created_at": "timestamp",
                            "updated_at": "timestamp"
                        }
                    },
                    "404": {"error": f"{entity} not found"},
                    "401": {"error": "Unauthorized"}
                },
                "contract_tests": [
                    "存在的ID返回200",
                    "不存在的ID返回404",
                    "无token返回401"
                ]
            },
            # POST /entities - 创建
            {
                "endpoint": entity_path,
                "method": "POST",
                "summary": f"创建{entity}",
                "request": {
                    "headers": {"Authorization": "Bearer {token}"},
                    "body": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {}
                    }
                },
                "response": {
                    "201": {
                        "description": "创建成功",
                        "schema": {"id": "UUID"}
                    },
                    "400": {"error": "Bad Request", "details": "array"},
                    "401": {"error": "Unauthorized"},
                    "409": {"error": "Conflict (duplicate)"}
                },
                "contract_tests": [
                    "有效数据返回201",
                    "缺失必填字段返回400",
                    "重复数据返回409",
                    "无token返回401"
                ]
            },
            # PUT /entities/:id - 更新
            {
                "endpoint": f"{entity_path}/{{id}}",
                "method": "PUT",
                "summary": f"更新{entity}",
                "request": {
                    "path_params": {"id": "UUID"},
                    "headers": {"Authorization": "Bearer {token}"},
                    "body": {"type": "object"}
                },
                "response": {
                    "200": {"description": "更新成功"},
                    "404": {"error": f"{entity} not found"},
                    "400": {"error": "Bad Request"},
                    "401": {"error": "Unauthorized"}
                },
                "contract_tests": [
                    "有效数据返回200",
                    "不存在的ID返回404",
                    "无效数据返回400"
                ]
            },
            # DELETE /entities/:id - 删除
            {
                "endpoint": f"{entity_path}/{{id}}",
                "method": "DELETE",
                "summary": f"删除{entity}",
                "request": {
                    "path_params": {"id": "UUID"},
                    "headers": {"Authorization": "Bearer {token}"}
                },
                "response": {
                    "204": {"description": "删除成功"},
                    "404": {"error": f"{entity} not found"},
                    "401": {"error": "Unauthorized"}
                },
                "contract_tests": [
                    "存在的ID返回204",
                    "不存在的ID返回404",
                    "无token返回401"
                ]
            }
        ]

    def _generate_feature_endpoints(self, feature: str) -> List[Dict]:
        """为特定功能生成自定义端点"""
        feature_lower = feature.lower()

        # 登录端点
        if "登录" in feature or "login" in feature_lower:
            return [{
                "endpoint": "/auth/login",
                "method": "POST",
                "summary": "用户登录",
                "request": {
                    "body": {
                        "type": "object",
                        "required": ["email", "password"],
                        "properties": {
                            "email": {"type": "string", "format": "email"},
                            "password": {"type": "string", "minLength": 8}
                        }
                    }
                },
                "response": {
                    "200": {
                        "description": "登录成功",
                        "schema": {
                            "token": "string",
                            "user": "User",
                            "expires_at": "timestamp"
                        }
                    },
                    "401": {"error": "Invalid credentials"},
                    "400": {"error": "Bad Request"}
                },
                "contract_tests": [
                    "有效凭证返回200和token",
                    "无效凭证返回401",
                    "缺失字段返回400",
                    "邮箱格式错误返回400"
                ]
            }]

        # 登出端点
        if "登出" in feature or "logout" in feature_lower:
            return [{
                "endpoint": "/auth/logout",
                "method": "POST",
                "summary": "用户登出",
                "request": {
                    "headers": {"Authorization": "Bearer {token}"}
                },
                "response": {
                    "200": {"description": "登出成功"},
                    "401": {"error": "Unauthorized"}
                },
                "contract_tests": [
                    "有效token返回200",
                    "无效token返回401"
                ]
            }]

        # 搜索端点
        if "搜索" in feature or "search" in feature_lower:
            return [{
                "endpoint": "/search",
                "method": "GET",
                "summary": "全局搜索",
                "request": {
                    "query_params": {
                        "q": {"type": "string", "required": True},
                        "type": {"type": "string", "optional": True},
                        "limit": {"type": "number", "default": 10}
                    }
                },
                "response": {
                    "200": {
                        "description": "搜索结果",
                        "schema": {
                            "results": "array",
                            "total": "number"
                        }
                    },
                    "400": {"error": "Missing query parameter"}
                },
                "contract_tests": [
                    "有效查询返回结果",
                    "空查询返回400",
                    "limit参数工作正常"
                ]
            }]

        return []

    def _generate_default_endpoints(self) -> List[Dict]:
        """生成默认端点(用户相关)"""
        return self._generate_entity_endpoints("User")

    def generate_openapi_spec(
        self,
        api_specs: List[Dict],
        info: Dict = None
    ) -> Dict:
        """
        生成完整的OpenAPI 3.0规格

        Args:
            api_specs: API规格列表
            info: API信息

        Returns:
            Dict: OpenAPI 3.0 JSON
        """
        if info is None:
            info = {
                "title": "API Documentation",
                "version": "1.0.0",
                "description": "Auto-generated API documentation"
            }

        paths = {}

        for spec in api_specs:
            endpoint = spec["endpoint"]
            method = spec["method"].lower()

            if endpoint not in paths:
                paths[endpoint] = {}

            paths[endpoint][method] = {
                "summary": spec.get("summary", ""),
                "parameters": self._convert_params_to_openapi(spec.get("request", {})),
                "requestBody": self._convert_body_to_openapi(spec.get("request", {})),
                "responses": self._convert_responses_to_openapi(spec.get("response", {})),
                "x-contract-tests": spec.get("contract_tests", [])
            }

        return {
            "openapi": "3.0.0",
            "info": info,
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }

    def _convert_params_to_openapi(self, request: Dict) -> List[Dict]:
        """转换参数为OpenAPI格式"""
        parameters = []

        # Path参数
        path_params = request.get("path_params", {})
        for name, type_info in path_params.items():
            parameters.append({
                "name": name,
                "in": "path",
                "required": True,
                "schema": {"type": type_info.lower() if isinstance(type_info, str) else "string"}
            })

        # Query参数
        query_params = request.get("query_params", {})
        for name, param_info in query_params.items():
            if isinstance(param_info, dict):
                parameters.append({
                    "name": name,
                    "in": "query",
                    "required": not param_info.get("optional", False),
                    "schema": {"type": param_info.get("type", "string")}
                })

        return parameters

    def _convert_body_to_openapi(self, request: Dict) -> Dict:
        """转换请求体为OpenAPI格式"""
        body = request.get("body", {})
        if not body:
            return None

        return {
            "required": True,
            "content": {
                "application/json": {
                    "schema": body
                }
            }
        }

    def _convert_responses_to_openapi(self, response: Dict) -> Dict:
        """转换响应为OpenAPI格式"""
        responses = {}

        for status_code, response_data in response.items():
            responses[status_code] = {
                "description": response_data.get("description", ""),
                "content": {
                    "application/json": {
                        "schema": response_data.get("schema", response_data)
                    }
                }
            }

        return responses
