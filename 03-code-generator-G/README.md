# 03-code-generator - 代码生成引擎

从规格文档自动生成生产级代码

## 核心功能

- **OpenAPI 规范生成 REST API**
- **多语言支持**: Python/TypeScript/Go/Java/Rust
- **完整 CRUD 接口**
- **Clean/Pragmatic 架构**
- **项目脚手架**

## 使用方法

### 从 OpenAPI 生成代码

```bash
python handler.py --openapi openapi.json --lang python --framework fastapi --output ./generated
```

### 生成 CRUD 接口

```bash
python handler.py --entity User --lang python --framework fastapi --output ./generated
```

### 生成项目脚手架

```bash
python handler.py --scaffold my-project --lang python --framework fastapi --output ./projects
```

## 支持的语言和框架

- **Python**: FastAPI, Django
- **TypeScript**: Express, NestJS
- **Go**: Gin, Echo
- **Java**: Spring Boot
- **Rust**: Actix-web

## 测试

```bash
python test_codegen.py
```
