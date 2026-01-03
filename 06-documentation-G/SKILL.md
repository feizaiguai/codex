---
name: 06-documentation-G
description: Documentation generator that auto-generates technical docs from code. Supports API documentation (OpenAPI/Swagger), README automation, architecture docs (ADR/C4 Model), living documentation, multi-format output (Markdown/HTML/PDF). Use for API doc maintenance, project READMEs, architecture doc updates.
---

# documentation - 文档生成专家

**版本**: 2.0.0
**优先级**: P1
**类别**: 核心开发流程

---

## 描述

documentation是一个专业的文档生成专家，能够从代码、API规格、BDD场景等多种源自动生成高质量的技术文档。支持API文档（OpenAPI/Swagger）、README、用户手册、架构文档（ADR、C4模型）、活文档（Living Documentation）等多种文档类型。通过智能分析代码结构、注释和类型定义，生成结构化、易读、准确的文档，大幅提升文档质量和开发效率。支持Markdown、HTML、PDF等多种输出格式，与主流文档工具（Sphinx、JSDoc、TypeDoc、Redoc）无缝集成。

---

## 核心能力

1. **API文档生成**: 从代码注释和类型定义自动生成OpenAPI 3.0/Swagger文档，包含端点、请求/响应模型、认证、错误码
2. **README生成**: 智能分析项目结构，生成包含安装、配置、使用示例、贡献指南的专业README
3. **用户手册**: 为最终用户创建易懂的使用指南，包含截图、步骤说明、FAQ
4. **架构文档**: 生成架构决策记录（ADR）、C4模型图、系统架构文档
5. **活文档**: 从BDD Gherkin场景生成可视化、可执行的活文档（Living Documentation）
6. **多格式输出**: 支持Markdown、HTML、PDF、reStructuredText等格式

---

## Instructions

### 工作流程

#### 1. 文档类型识别与源分析

**步骤**:
1. **识别文档类型**:
   - API文档: 检测FastAPI/NestJS路由装饰器、OpenAPI注释
   - README: 分析项目根目录结构、package.json/pyproject.toml
   - 用户手册: 识别用户故事、UI组件
   - 架构文档: 检测ADR目录、架构图源文件
   - 活文档: 解析Gherkin .feature文件

2. **源代码分析**:
   - **Python**: 解析docstring（Google/NumPy/Sphinx风格）、类型注解
   - **TypeScript**: 解析JSDoc注释、TypeScript类型定义、装饰器
   - **OpenAPI**: 解析OpenAPI 3.0 YAML/JSON规格文件
   - **Gherkin**: 解析.feature文件的Feature/Scenario/Steps

3. **提取元数据**:
   - API端点: 路径、HTTP方法、参数、响应
   - 函数/类: 名称、参数、返回值、描述
   - 依赖关系: imports、项目依赖
   - 配置信息: 环境变量、配置文件

#### 2. 内容生成策略

**API文档生成**:
```
1. 解析路由定义
   └─> 提取HTTP方法、路径、路径参数、查询参数
2. 分析请求/响应模型
   └─> Pydantic模型 → JSON Schema
   └─> TypeScript接口 → OpenAPI Schema
3. 提取认证信息
   └─> 检测JWT、OAuth2、API Key装饰器
4. 生成示例
   └─> 基于模型生成cURL、JavaScript、Python示例
5. 添加错误码说明
   └─> 从异常处理代码提取错误场景
```

**README生成**:
```
1. 项目概述
   └─> 从package.json/pyproject.toml提取名称、描述
2. 功能列表
   └─> 分析主要模块和导出函数
3. 安装指南
   └─> 检测依赖管理工具（pip/npm/yarn）
   └─> 生成安装命令
4. 快速开始
   └─> 提取主要入口点（main.py/index.ts）
   └─> 生成最小可运行示例
5. 配置说明
   └─> 解析.env.example、配置类
6. 贡献指南
   └─> 检测CONTRIBUTING.md或生成标准模板
```

**架构文档生成**:
```
1. ADR模板应用
   └─> 标题、状态、上下文、决策、理由、后果
2. C4模型图生成
   └─> Context (系统上下文)
   └─> Container (容器图)
   └─> Component (组件图)
   └─> Code (代码图)
3. 依赖关系分析
   └─> 生成模块依赖图
4. 数据流图
   └─> 追踪数据在系统中的流动
```

#### 3. 文档结构化与格式化

**Markdown格式化**:
- 使用正确的标题层级（#, ##, ###）
- 代码块语法高亮（```python, ```typescript）
- 表格格式化（对齐、边框）
- 链接和锚点（内部链接、外部链接）
- 徽章（Badges）: 版本、构建状态、覆盖率

**HTML生成**（通过Sphinx/MkDocs）:
- 主题选择（ReadTheDocs、Material）
- 导航结构（左侧菜单、面包屑）
- 搜索功能
- 代码高亮
- 响应式设计

**PDF生成**:
- 使用Pandoc或Sphinx LaTeX后端
- 页眉/页脚、页码
- 目录（TOC）
- 图表嵌入

#### 4. 活文档生成（BDD场景）

**从Gherkin到可视化文档**:
```
Feature: 用户注册
  └─> HTML文档标题: "用户注册功能"

  Scenario: 成功注册
    └─> 表格行1: "成功注册场景"

    Given 用户访问注册页面
      └─> 步骤1: "前置条件: 用户访问注册页面"

    When 用户输入有效邮箱
      └─> 步骤2: "操作: 用户输入有效邮箱"

    Then 系统创建新用户记录
      └─> 步骤3: "期望: 系统创建新用户记录"
```

**测试结果集成**:
- 将pytest-bdd测试结果嵌入活文档
- 显示场景通过/失败状态
- 链接到测试代码

#### 5. 文档质量检查

**检查项**:
- **完整性**: 所有公开API都有文档说明
- **准确性**: 文档与代码同步（检测不一致）
- **可读性**: 使用清晰的语言、避免行话
- **示例完整**: 每个API至少有一个工作示例
- **链接有效**: 验证所有内部和外部链接
- **拼写检查**: 运行拼写检查工具

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| source | object | 是 | - | 文档源（代码文件、API规格、BDD场景） |
| source.type | string | 是 | - | 源类型: code/openapi/gherkin |
| source.files | string[] | 是 | - | 源文件路径列表 |
| source.entry_point | string | 否 | - | 入口文件（如main.py） |
| doc_type | string | 是 | - | 文档类型: api/readme/user-guide/architecture/living-doc |
| format | string | 否 | markdown | 输出格式: markdown/html/pdf/rst |
| config | object | 否 | {} | 配置选项 |
| config.title | string | 否 | - | 文档标题 |
| config.version | string | 否 | 1.0.0 | 文档版本 |
| config.base_url | string | 否 | - | API基础URL（用于API文档） |
| config.include_examples | boolean | 否 | true | 是否包含代码示例 |
| config.include_toc | boolean | 否 | true | 是否生成目录 |
| config.theme | string | 否 | default | 文档主题（HTML输出） |
| output_path | string | 否 | ./docs | 输出目录 |

---

## 输出格式

```typescript
interface DocumentationOutput {
  document: string;              // 生成的文档内容（Markdown/HTML/PDF）
  assets: DocumentAsset[];       // 相关资源（图片、CSS、JS）
  format: 'markdown' | 'html' | 'pdf' | 'rst';
  metadata: {
    title: string;
    version: string;
    generated_at: string;        // ISO 8601格式
    source_files: string[];
    word_count: number;
    sections: string[];          // 文档章节列表
  };
  quality_score: number;         // 0-100，文档质量评分
  quality_issues: QualityIssue[];
  statistics: {
    total_apis?: number;         // API文档特有
    documented_apis?: number;
    coverage_percentage?: number;
    missing_docs: string[];      // 缺少文档的API/函数
  };
}

interface DocumentAsset {
  type: 'image' | 'css' | 'javascript';
  path: string;
  content?: string;              // Base64编码（图片）或文本
}

interface QualityIssue {
  severity: 'error' | 'warning' | 'info';
  type: 'missing_doc' | 'broken_link' | 'typo' | 'inconsistency';
  location: string;              // 文件:行号
  message: string;
  suggestion?: string;
}
```

---


---

## TypeScript接口

### 基础输出接口

所有Skill的输出都继承自`BaseOutput`统一接口：

```typescript
interface BaseOutput {
  success: boolean;
  error?: {
    code: string;
    message: string;
    suggestedFix?: string;
  };
  metadata?: {
    requestId: string;
    timestamp: string;
    version: string;
  };
  warnings?: Array<{
    code: string;
    message: string;
    severity: 'low' | 'medium' | 'high';
  }>;
}
```

### 输入接口

```typescript
interface DocumentationInput {
}
```

### 输出接口

```typescript
interface DocumentationOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例1: 为FastAPI项目生成完整API文档

**用户请求**:
> "为我的FastAPI用户管理系统生成完整的API文档，包括认证、CRUD操作、错误码说明"

**项目结构**:
```
user-management/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── models.py            # Pydantic模型
│   ├── auth.py              # JWT认证
│   └── routers/
│       └── users.py         # 用户路由
├── requirements.txt
└── .env.example
```

**源代码示例**:

**app/models.py**:
```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr = Field(..., description="用户邮箱，必须唯一")
    username: str = Field(..., min_length=2, max_length=20, description="用户名，2-20字符")

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="密码，至少8字符，包含大小写字母和数字"
    )

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not any(c.islower() for c in v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含至少一个数字')
        return v

class UserResponse(UserBase):
    """用户响应模型"""
    id: UUID = Field(..., description="用户唯一标识符")
    created_at: datetime = Field(..., description="账号创建时间")
    is_active: bool = Field(True, description="账号是否激活")
    is_verified: bool = Field(False, description="邮箱是否验证")

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    """用户更新模型"""
    username: Optional[str] = Field(None, min_length=2, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class Token(BaseModel):
    """JWT Token响应模型"""
    access_token: str = Field(..., description="JWT访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(86400, description="令牌过期时间（秒）")

class LoginRequest(BaseModel):
    """登录请求模型"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="密码")
```

**app/routers/users.py**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..models import UserCreate, UserResponse, UserUpdate, LoginRequest, Token
from ..auth import get_current_user, create_access_token, verify_password, get_password_hash
from ..database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "用户不存在"}}
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    description="创建新用户账号。密码会被安全哈希后存储。",
    responses={
        201: {
            "description": "用户注册成功",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "email": "user@example.com",
                        "username": "johndoe",
                        "created_at": "2025-12-12T10:00:00Z",
                        "is_active": True,
                        "is_verified": False
                    }
                }
            }
        },
        400: {"description": "邮箱已被注册或密码不符合要求"},
        422: {"description": "请求参数验证失败"}
    }
)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    注册新用户账号

    - **email**: 有效的邮箱地址，必须唯一
    - **username**: 用户名，2-20字符
    - **password**: 密码，至少8字符，包含大小写字母和数字

    注册成功后会发送验证邮件到用户邮箱。
    """
    # 检查邮箱是否已存在
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 创建用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # TODO: 发送验证邮件

    return db_user

@router.post(
    "/login",
    response_model=Token,
    summary="用户登录",
    description="使用邮箱和密码登录获取JWT访问令牌",
    responses={
        200: {
            "description": "登录成功",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "token_type": "bearer",
                        "expires_in": 86400
                    }
                }
            }
        },
        401: {"description": "邮箱或密码错误"},
        429: {"description": "登录尝试过于频繁，请稍后再试"}
    }
)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    用户登录获取访问令牌

    - **email**: 注册时使用的邮箱
    - **password**: 账号密码

    返回的access_token需要在后续请求的Authorization头中携带：
    `Authorization: Bearer <access_token>`

    令牌有效期为24小时。
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400
    }

@router.get(
    "/me",
    response_model=UserResponse,
    summary="获取当前用户信息",
    description="获取当前认证用户的详细信息",
    responses={
        200: {"description": "成功返回用户信息"},
        401: {"description": "未授权，Token无效或已过期"}
    }
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户信息

    需要在请求头中携带有效的JWT Token：
    `Authorization: Bearer <access_token>`
    """
    return current_user

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="根据ID获取用户",
    description="获取指定用户的公开信息",
    responses={
        200: {"description": "成功返回用户信息"},
        404: {"description": "用户不存在"}
    }
)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据用户ID获取用户信息

    - **user_id**: 用户的UUID

    需要认证才能访问。
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.patch(
    "/me",
    response_model=UserResponse,
    summary="更新当前用户信息",
    description="更新当前认证用户的用户名或密码",
    responses={
        200: {"description": "更新成功"},
        400: {"description": "无效的更新数据"},
        401: {"description": "未授权"}
    }
)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息

    - **username**: (可选) 新用户名，2-20字符
    - **password**: (可选) 新密码，至少8字符，包含大小写字母和数字

    至少需要提供一个更新字段。密码会被安全哈希后存储。
    """
    update_data = user_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除当前用户账号",
    description="永久删除当前认证用户的账号",
    responses={
        204: {"description": "账号删除成功"},
        401: {"description": "未授权"}
    }
)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除当前用户账号

    **警告**: 此操作不可逆，将永久删除用户的所有数据。
    """
    db.delete(current_user)
    db.commit()
    return None

@router.get(
    "",
    response_model=List[UserResponse],
    summary="获取用户列表",
    description="分页获取用户列表（仅管理员）",
    responses={
        200: {"description": "成功返回用户列表"},
        401: {"description": "未授权"},
        403: {"description": "权限不足"}
    }
)
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户列表（分页）

    - **skip**: 跳过的记录数，默认0
    - **limit**: 返回的最大记录数，默认20，最大100

    仅管理员可以访问此端点。
    """
    # TODO: 添加管理员权限检查

    if limit > 100:
        limit = 100

    users = db.query(User).offset(skip).limit(limit).all()
    return users
```

**app/main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users

app = FastAPI(
    title="用户管理API",
    description="完整的用户注册、认证和管理系统",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(users.router)

@app.get("/", tags=["Root"])
async def root():
    """API根端点"""
    return {
        "message": "User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
```

**Skill执行**:
```python
# documentation skill分析源代码
result = documentation_skill.execute({
    "source": {
        "type": "code",
        "files": [
            "app/main.py",
            "app/routers/users.py",
            "app/models.py",
            "app/auth.py"
        ],
        "entry_point": "app/main.py"
    },
    "doc_type": "api",
    "format": "markdown",
    "config": {
        "title": "用户管理API文档",
        "version": "1.0.0",
        "base_url": "https://api.example.com/v1",
        "include_examples": True,
        "include_toc": True
    },
    "output_path": "./docs"
})
```

**生成的API文档** (docs/api-documentation.md):
```markdown
# 用户管理API文档

**版本**: 1.0.0
**基础URL**: `https://api.example.com/v1`
**生成时间**: 2025-12-12T10:00:00Z

---

## 目录

1. [概述](#概述)
2. [认证](#认证)
3. [API端点](#api端点)
   - [用户注册](#用户注册)
   - [用户登录](#用户登录)
   - [获取当前用户信息](#获取当前用户信息)
   - [根据ID获取用户](#根据id获取用户)
   - [更新当前用户信息](#更新当前用户信息)
   - [删除当前用户账号](#删除当前用户账号)
   - [获取用户列表](#获取用户列表)
4. [数据模型](#数据模型)
5. [错误码](#错误码)
6. [速率限制](#速率限制)
7. [示例代码](#示例代码)

---

## 概述

用户管理API提供完整的用户注册、认证和管理功能。所有端点都遵循RESTful设计原则，使用JSON格式进行数据交换。

**主要功能**:
- 用户注册与邮箱验证
- JWT令牌认证
- 用户资料管理（CRUD）
- 密码安全（bcrypt哈希）
- 速率限制保护

**技术栈**:
- FastAPI 0.104+
- SQLAlchemy 2.0+ (ORM)
- Pydantic 2.0+ (数据验证)
- JWT (认证)

---

## 认证

API使用**JWT Bearer Token**进行认证。

### 获取Token

通过[用户登录](#用户登录)端点获取访问令牌：

```bash
curl -X POST https://api.example.com/v1/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

响应：
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MDI1NjAwMDB9.signature",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### 使用Token

在需要认证的端点请求头中携带Token：

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Token有效期**: 24小时（86400秒）

---

## API端点

### 用户注册

创建新用户账号。密码会被安全哈希后存储。

**端点**: `POST /api/users/register`

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "email": "user@example.com",      // string, 必需, 有效邮箱格式
  "username": "johndoe",            // string, 必需, 2-20字符
  "password": "SecurePass123!"      // string, 必需, 至少8字符，包含大小写字母和数字
}
```

**密码要求**:
- 最少8字符
- 至少1个大写字母
- 至少1个小写字母
- 至少1个数字

**成功响应** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-12-12T10:00:00Z",
  "is_active": true,
  "is_verified": false
}
```

**错误响应**:

| 状态码 | 说明 | 响应体示例 |
|--------|------|-----------|
| 400 | 邮箱已被注册 | `{"detail": "Email already registered"}` |
| 422 | 请求参数验证失败 | `{"detail": [{"loc": ["body", "password"], "msg": "密码必须包含至少一个大写字母", "type": "value_error"}]}` |

**cURL示例**:
```bash
curl -X POST https://api.example.com/v1/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**JavaScript示例**:
```javascript
const response = await fetch('https://api.example.com/v1/api/users/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    username: 'johndoe',
    password: 'SecurePass123!'
  })
});

const data = await response.json();
console.log('User created:', data);
```

**Python示例**:
```python
import requests

response = requests.post(
    'https://api.example.com/v1/api/users/register',
    json={
        'email': 'user@example.com',
        'username': 'johndoe',
        'password': 'SecurePass123!'
    }
)

user = response.json()
print(f"User created: {user['id']}")
```

---

### 用户登录

使用邮箱和密码登录获取JWT访问令牌。

**端点**: `POST /api/users/login`

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "email": "user@example.com",      // string, 必需
  "password": "SecurePass123!"      // string, 必需
}
```

**成功响应** (200 OK):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**错误响应**:

| 状态码 | 说明 | 响应体示例 |
|--------|------|-----------|
| 401 | 邮箱或密码错误 | `{"detail": "Invalid credentials"}` |
| 403 | 账号未激活 | `{"detail": "Account is inactive"}` |
| 429 | 登录尝试过于频繁 | `{"detail": "Too many login attempts, please try again later"}` |

**cURL示例**:
```bash
curl -X POST https://api.example.com/v1/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

---

### 获取当前用户信息

获取当前认证用户的详细信息。

**端点**: `GET /api/users/me`

**请求头**:
```
Authorization: Bearer <access_token>
```

**成功响应** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-12-12T10:00:00Z",
  "is_active": true,
  "is_verified": true
}
```

**错误响应**:

| 状态码 | 说明 |
|--------|------|
| 401 | 未授权，Token无效或已过期 |

**cURL示例**:
```bash
curl -X GET https://api.example.com/v1/api/users/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

### 根据ID获取用户

获取指定用户的公开信息。

**端点**: `GET /api/users/{user_id}`

**路径参数**:
- `user_id` (UUID, 必需): 用户的唯一标识符

**请求头**:
```
Authorization: Bearer <access_token>
```

**成功响应** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "created_at": "2025-12-12T10:00:00Z",
  "is_active": true,
  "is_verified": true
}
```

**错误响应**:

| 状态码 | 说明 |
|--------|------|
| 401 | 未授权 |
| 404 | 用户不存在 |

**cURL示例**:
```bash
curl -X GET https://api.example.com/v1/api/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

### 更新当前用户信息

更新当前认证用户的用户名或密码。

**端点**: `PATCH /api/users/me`

**请求头**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求体** (所有字段可选，至少提供一个):
```json
{
  "username": "newusername",        // string, 可选, 2-20字符
  "password": "NewSecurePass456!"   // string, 可选, 至少8字符
}
```

**成功响应** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "newusername",
  "created_at": "2025-12-12T10:00:00Z",
  "is_active": true,
  "is_verified": true
}
```

**错误响应**:

| 状态码 | 说明 |
|--------|------|
| 400 | 没有提供更新字段 |
| 401 | 未授权 |
| 422 | 参数验证失败 |

**cURL示例**:
```bash
curl -X PATCH https://api.example.com/v1/api/users/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername"
  }'
```

---

### 删除当前用户账号

永久删除当前认证用户的账号。

**端点**: `DELETE /api/users/me`

**请求头**:
```
Authorization: Bearer <access_token>
```

**成功响应** (204 No Content):
无响应体

**错误响应**:

| 状态码 | 说明 |
|--------|------|
| 401 | 未授权 |

**警告**: 此操作不可逆，将永久删除用户的所有数据。

**cURL示例**:
```bash
curl -X DELETE https://api.example.com/v1/api/users/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

### 获取用户列表

分页获取用户列表（仅管理员）。

**端点**: `GET /api/users`

**请求头**:
```
Authorization: Bearer <access_token>
```

**查询参数**:
- `skip` (integer, 可选, 默认=0): 跳过的记录数
- `limit` (integer, 可选, 默认=20, 最大=100): 返回的最大记录数

**成功响应** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user1@example.com",
    "username": "user1",
    "created_at": "2025-12-12T10:00:00Z",
    "is_active": true,
    "is_verified": true
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "email": "user2@example.com",
    "username": "user2",
    "created_at": "2025-12-12T11:00:00Z",
    "is_active": true,
    "is_verified": false
  }
]
```

**错误响应**:

| 状态码 | 说明 |
|--------|------|
| 401 | 未授权 |
| 403 | 权限不足 |

**cURL示例**:
```bash
curl -X GET "https://api.example.com/v1/api/users?skip=0&limit=20" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## 数据模型

### UserResponse

用户信息响应模型。

```typescript
interface UserResponse {
  id: string;              // UUID格式
  email: string;           // 邮箱地址
  username: string;        // 用户名，2-20字符
  created_at: string;      // ISO 8601格式时间戳
  is_active: boolean;      // 账号是否激活
  is_verified: boolean;    // 邮箱是否验证
}
```

### UserCreate

用户注册请求模型。

```typescript
interface UserCreate {
  email: string;           // 必需，有效邮箱格式
  username: string;        // 必需，2-20字符
  password: string;        // 必需，至少8字符，包含大小写字母和数字
}
```

### UserUpdate

用户更新请求模型。

```typescript
interface UserUpdate {
  username?: string;       // 可选，2-20字符
  password?: string;       // 可选，至少8字符
}
```

### LoginRequest

登录请求模型。

```typescript
interface LoginRequest {
  email: string;           // 必需
  password: string;        // 必需
}
```

### Token

JWT令牌响应模型。

```typescript
interface Token {
  access_token: string;    // JWT访问令牌
  token_type: string;      // 固定值: "bearer"
  expires_in: number;      // 令牌过期时间（秒），默认86400（24小时）
}
```

---

## 错误码

API使用标准HTTP状态码表示请求结果。

| 状态码 | 说明 | 常见原因 |
|--------|------|---------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 请求成功，无返回内容（如DELETE） |
| 400 | Bad Request | 请求参数错误、业务逻辑错误 |
| 401 | Unauthorized | 未授权，Token缺失/无效/过期 |
| 403 | Forbidden | 权限不足、账号未激活 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 请求参数验证失败 |
| 429 | Too Many Requests | 请求过于频繁，触发速率限制 |
| 500 | Internal Server Error | 服务器内部错误 |

### 错误响应格式

所有错误响应遵循统一格式：

```json
{
  "detail": "错误描述信息"
}
```

对于422验证错误，会提供详细的字段错误信息：

```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "密码必须包含至少一个大写字母",
      "type": "value_error"
    }
  ]
}
```

---

## 速率限制

为防止滥用，API实施速率限制：

| 端点类型 | 限制 | 时间窗口 |
|---------|------|---------|
| 注册 (`/register`) | 5次 | 1小时 |
| 登录 (`/login`) | 10次 | 15分钟 |
| 其他认证端点 | 100次 | 1分钟 |

**超出限制时的响应**:
```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Too many requests, please try again later",
  "retry_after": 600
}
```

**响应头**:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1702560000
```

---

## 示例代码

### 完整的注册和登录流程

**Python示例** (使用requests):
```python
import requests

BASE_URL = "https://api.example.com/v1"

# 1. 注册用户
def register_user(email, username, password):
    response = requests.post(
        f"{BASE_URL}/api/users/register",
        json={
            "email": email,
            "username": username,
            "password": password
        }
    )

    if response.status_code == 201:
        user = response.json()
        print(f"✓ User registered successfully: {user['id']}")
        return user
    else:
        error = response.json()
        print(f"✗ Registration failed: {error['detail']}")
        return None

# 2. 登录获取Token
def login_user(email, password):
    response = requests.post(
        f"{BASE_URL}/api/users/login",
        json={
            "email": email,
            "password": password
        }
    )

    if response.status_code == 200:
        token_data = response.json()
        print(f"✓ Login successful, token expires in {token_data['expires_in']}s")
        return token_data['access_token']
    else:
        error = response.json()
        print(f"✗ Login failed: {error['detail']}")
        return None

# 3. 获取用户信息
def get_user_info(access_token):
    response = requests.get(
        f"{BASE_URL}/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if response.status_code == 200:
        user = response.json()
        print(f"✓ User info retrieved: {user['username']} ({user['email']})")
        return user
    else:
        print("✗ Failed to get user info")
        return None

# 4. 更新用户信息
def update_user(access_token, username=None, password=None):
    update_data = {}
    if username:
        update_data["username"] = username
    if password:
        update_data["password"] = password

    response = requests.patch(
        f"{BASE_URL}/api/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_data
    )

    if response.status_code == 200:
        user = response.json()
        print(f"✓ User updated successfully")
        return user
    else:
        print("✗ Update failed")
        return None

# 使用示例
if __name__ == "__main__":
    # 注册
    user = register_user(
        email="test@example.com",
        username="testuser",
        password="SecurePass123!"
    )

    if user:
        # 登录
        token = login_user("test@example.com", "SecurePass123!")

        if token:
            # 获取信息
            user_info = get_user_info(token)

            # 更新用户名
            updated_user = update_user(token, username="newtestuser")
```

**JavaScript示例** (使用fetch):
```javascript
const BASE_URL = 'https://api.example.com/v1';

// 1. 注册用户
async function registerUser(email, username, password) {
  try {
    const response = await fetch(`${BASE_URL}/api/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, username, password })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✓ User registered:', data.id);
      return data;
    } else {
      console.error('✗ Registration failed:', data.detail);
      return null;
    }
  } catch (error) {
    console.error('✗ Network error:', error);
    return null;
  }
}

// 2. 登录获取Token
async function loginUser(email, password) {
  try {
    const response = await fetch(`${BASE_URL}/api/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✓ Login successful');
      localStorage.setItem('access_token', data.access_token);
      return data.access_token;
    } else {
      console.error('✗ Login failed:', data.detail);
      return null;
    }
  } catch (error) {
    console.error('✗ Network error:', error);
    return null;
  }
}

// 3. 获取用户信息
async function getUserInfo(accessToken) {
  try {
    const response = await fetch(`${BASE_URL}/api/users/me`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✓ User info:', data);
      return data;
    } else {
      console.error('✗ Failed to get user info');
      return null;
    }
  } catch (error) {
    console.error('✗ Network error:', error);
    return null;
  }
}

// 4. 更新用户信息
async function updateUser(accessToken, updates) {
  try {
    const response = await fetch(`${BASE_URL}/api/users/me`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updates)
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✓ User updated');
      return data;
    } else {
      console.error('✗ Update failed');
      return null;
    }
  } catch (error) {
    console.error('✗ Network error:', error);
    return null;
  }
}

// 使用示例
(async () => {
  // 注册
  const user = await registerUser(
    'test@example.com',
    'testuser',
    'SecurePass123!'
  );

  if (user) {
    // 登录
    const token = await loginUser('test@example.com', 'SecurePass123!');

    if (token) {
      // 获取信息
      const userInfo = await getUserInfo(token);

      // 更新用户名
      const updatedUser = await updateUser(token, { username: 'newtestuser' });
    }
  }
})();
```

---

## 附录

### OpenAPI规格文件

完整的OpenAPI 3.0规格可通过以下端点访问：
- Swagger UI: `https://api.example.com/v1/docs`
- ReDoc: `https://api.example.com/v1/redoc`
- JSON规格: `https://api.example.com/v1/openapi.json`

### 变更日志

#### v1.0.0 (2025-12-12)
- 初始版本发布
- 用户注册、登录、资料管理功能
- JWT认证
- 速率限制保护

### 联系方式

- **技术支持**: support@example.com
- **问题反馈**: https://github.com/example/user-api/issues
- **API状态**: https://status.example.com

### 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**文档质量评分**: 95/100

**生成时间**: 2025-12-12T10:00:00Z
**工具**: Claude Code documentation skill v2.0.0
```

**输出摘要**:
```json
{
  "document": "[完整Markdown文档内容]",
  "assets": [],
  "format": "markdown",
  "metadata": {
    "title": "用户管理API文档",
    "version": "1.0.0",
    "generated_at": "2025-12-12T10:00:00Z",
    "source_files": [
      "app/main.py",
      "app/routers/users.py",
      "app/models.py",
      "app/auth.py"
    ],
    "word_count": 3200,
    "sections": [
      "概述",
      "认证",
      "API端点",
      "数据模型",
      "错误码",
      "速率限制",
      "示例代码"
    ]
  },
  "quality_score": 95,
  "quality_issues": [
    {
      "severity": "warning",
      "type": "missing_doc",
      "location": "app/auth.py:create_access_token",
      "message": "函数缺少docstring",
      "suggestion": "添加函数文档说明JWT token创建逻辑"
    }
  ],
  "statistics": {
    "total_apis": 7,
    "documented_apis": 7,
    "coverage_percentage": 100,
    "missing_docs": []
  }
}
```

**下一步建议**:
1. 将生成的Markdown文档转换为HTML（使用MkDocs或Sphinx）
2. 配置自动化文档部署（GitHub Pages/Read the Docs）
3. 添加交互式API测试（Swagger UI已自动生成）
4. 设置文档版本控制（与代码版本同步）

---

### 示例2: 生成项目README

**用户请求**:
> "为我的Python CLI工具项目生成一个专业的README"

**项目结构**:
```
my-cli-tool/
├── src/
│   ├── __init__.py
│   ├── cli.py           # Click命令定义
│   ├── config.py        # 配置管理
│   └── utils.py         # 工具函数
├── tests/
│   └── test_cli.py
├── pyproject.toml
├── LICENSE
└── .env.example
```

**pyproject.toml**:
```toml
[tool.poetry]
name = "my-cli-tool"
version = "1.2.0"
description = "一个强大的命令行工具用于数据处理和分析"
authors = ["John Doe <john@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/johndoe/my-cli-tool"
repository = "https://github.com/johndoe/my-cli-tool"
keywords = ["cli", "data", "processing"]

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.1.0"
pandas = "^2.0.0"
pyyaml = "^6.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
black = "^23.0.0"
mypy = "^1.5.0"

[tool.poetry.scripts]
mytool = "src.cli:main"
```

**src/cli.py** (部分):
```python
import click
from pathlib import Path

@click.group()
@click.version_option()
def main():
    """My CLI Tool - 数据处理命令行工具"""
    pass

@main.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='输出文件路径')
@click.option('--format', '-f', type=click.Choice(['csv', 'json', 'excel']),
              default='csv', help='输出格式')
def process(input_file, output, format):
    """处理数据文件并转换格式"""
    click.echo(f"Processing {input_file}...")
    # ... 处理逻辑

@main.command()
@click.option('--config', '-c', type=click.Path(), help='配置文件路径')
def init(config):
    """初始化配置文件"""
    click.echo("Initializing configuration...")
    # ... 初始化逻辑
```

**Skill执行**:
```python
result = documentation_skill.execute({
    "source": {
        "type": "code",
        "files": [
            "pyproject.toml",
            "src/cli.py",
            "src/config.py",
            ".env.example"
        ],
        "entry_point": "src/cli.py"
    },
    "doc_type": "readme",
    "format": "markdown",
    "config": {
        "title": "My CLI Tool",
        "include_badges": True,
        "include_toc": True
    }
})
```

**生成的README.md**:
```markdown
# My CLI Tool

一个强大的命令行工具用于数据处理和分析

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/johndoe/my-cli-tool/releases)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Build Status](https://img.shields.io/github/workflow/status/johndoe/my-cli-tool/CI)](https://github.com/johndoe/my-cli-tool/actions)

---

## 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
  - [安装](#安装)
  - [基本使用](#基本使用)
- [命令参考](#命令参考)
- [配置](#配置)
- [示例](#示例)
- [开发指南](#开发指南)
- [贡献](#贡献)
- [许可证](#许可证)

---

## 功能特性

✨ **核心功能**:
- 🔄 多格式数据转换（CSV、JSON、Excel）
- ⚙️ 灵活的配置管理
- 🚀 高性能数据处理（基于Pandas）
- 📊 丰富的命令行选项
- 🔍 详细的进度输出

🛠️ **技术亮点**:
- 使用Click构建直观的CLI界面
- 类型安全（Mypy验证）
- 完整的单元测试覆盖
- 遵循PEP 8代码规范（Black格式化）

---

## 快速开始

### 前置要求

- Python 3.9 或更高版本
- pip 或 Poetry（推荐）

### 安装

#### 使用pip安装（推荐）

```bash
pip install my-cli-tool
```

#### 使用Poetry安装（开发）

```bash
# 克隆仓库
git clone https://github.com/johndoe/my-cli-tool.git
cd my-cli-tool

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

#### 从源码安装

```bash
git clone https://github.com/johndoe/my-cli-tool.git
cd my-cli-tool
pip install -e .
```

### 验证安装

```bash
mytool --version
# 输出: My CLI Tool, version 1.2.0
```

---

## 基本使用

### 查看帮助

```bash
mytool --help
```

输出：
```
Usage: mytool [OPTIONS] COMMAND [ARGS]...

  My CLI Tool - 数据处理命令行工具

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  process  处理数据文件并转换格式
  init     初始化配置文件
```

### 处理数据文件

```bash
# CSV转JSON
mytool process data.csv --output result.json --format json

# CSV转Excel
mytool process data.csv --output result.xlsx --format excel
```

### 初始化配置

```bash
mytool init --config config.yaml
```

---

## 命令参考

### `process` - 数据处理

处理数据文件并转换格式。

**用法**:
```bash
mytool process INPUT_FILE [OPTIONS]
```

**参数**:
- `INPUT_FILE` (必需): 输入数据文件路径

**选项**:
| 选项 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--output` | `-o` | PATH | - | 输出文件路径 |
| `--format` | `-f` | CHOICE | csv | 输出格式: csv, json, excel |

**示例**:
```bash
# 转换为JSON格式
mytool process sales.csv -o sales.json -f json

# 转换为Excel格式
mytool process inventory.csv -o inventory.xlsx -f excel
```

---

### `init` - 初始化配置

创建默认配置文件。

**用法**:
```bash
mytool init [OPTIONS]
```

**选项**:
| 选项 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--config` | `-c` | PATH | config.yaml | 配置文件路径 |

**示例**:
```bash
# 使用默认路径
mytool init

# 指定自定义路径
mytool init -c custom-config.yaml
```

---

## 配置

### 配置文件格式

创建 `config.yaml` 文件：

```yaml
# 数据处理配置
processing:
  chunk_size: 10000
  encoding: utf-8

# 输出配置
output:
  default_format: csv
  compression: gzip

# 日志配置
logging:
  level: INFO
  file: mytool.log
```

### 环境变量

可以通过环境变量覆盖配置：

```bash
export MYTOOL_CONFIG=/path/to/config.yaml
export MYTOOL_LOG_LEVEL=DEBUG
```

---

## 示例

### 示例1: 批量转换CSV文件

```bash
#!/bin/bash

for file in data/*.csv; do
  mytool process "$file" \
    --output "output/$(basename "$file" .csv).json" \
    --format json
  echo "Processed: $file"
done
```

### 示例2: Python脚本集成

```python
import subprocess

def convert_data(input_file, output_format='json'):
    """使用mytool转换数据文件"""
    result = subprocess.run(
        ['mytool', 'process', input_file,
         '--format', output_format],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✓ 转换成功: {input_file}")
    else:
        print(f"✗ 转换失败: {result.stderr}")

convert_data('sales.csv', 'json')
```

---

## 开发指南

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/johndoe/my-cli-tool.git
cd my-cli-tool

# 安装开发依赖
poetry install --with dev

# 安装pre-commit hooks
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_cli.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 代码质量检查

```bash
# 代码格式化
black src/ tests/

# 类型检查
mypy src/

# Linting
flake8 src/ tests/
```

### 构建文档

```bash
# 生成API文档
pdoc --html src/ -o docs/

# 启动文档服务器
python -m http.server --directory docs/
```

---

## 贡献

欢迎贡献！请遵循以下步骤：

1. **Fork项目**: 点击右上角的Fork按钮
2. **创建分支**: `git checkout -b feature/amazing-feature`
3. **提交更改**: `git commit -m 'Add amazing feature'`
4. **推送分支**: `git push origin feature/amazing-feature`
5. **创建PR**: 在GitHub上创建Pull Request

### 贡献指南

- 遵循PEP 8代码规范
- 添加单元测试（覆盖率≥80%）
- 更新文档说明新功能
- 使用有意义的commit message

---

## 路线图

- [ ] v1.3.0: 添加数据库支持（SQLite、PostgreSQL）
- [ ] v1.4.0: 实现插件系统
- [ ] v2.0.0: Web界面（可选）
- [ ] 性能优化: 支持大文件流式处理

---

## 常见问题 (FAQ)

**Q: 支持哪些数据格式？**
A: 当前支持CSV、JSON、Excel (.xlsx)。后续版本将添加Parquet、Avro等格式。

**Q: 如何处理大文件？**
A: 工具使用Pandas分块读取，默认chunk_size=10000行。可在配置文件中调整。

**Q: 遇到编码错误怎么办？**
A: 在配置文件中设置 `processing.encoding` 为正确的编码（如gbk、utf-8）。

---

## 致谢

感谢以下开源项目：
- [Click](https://click.palletsprojects.com/) - 优秀的CLI框架
- [Pandas](https://pandas.pydata.org/) - 强大的数据处理库
- [Poetry](https://python-poetry.org/) - 现代Python包管理

---

## 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 联系方式

- **作者**: John Doe
- **邮箱**: john@example.com
- **GitHub**: [@johndoe](https://github.com/johndoe)
- **问题反馈**: [Issues](https://github.com/johndoe/my-cli-tool/issues)

---

**⭐ 如果这个项目对你有帮助，请给一个Star！**

---

*生成时间: 2025-12-12 | 工具: Claude Code documentation skill v2.0.0*
```

**输出摘要**:
```json
{
  "document": "[完整README内容]",
  "assets": [],
  "format": "markdown",
  "metadata": {
    "title": "My CLI Tool",
    "version": "1.2.0",
    "generated_at": "2025-12-12T10:30:00Z",
    "source_files": [
      "pyproject.toml",
      "src/cli.py",
      "src/config.py"
    ],
    "word_count": 1500,
    "sections": [
      "功能特性",
      "快速开始",
      "命令参考",
      "配置",
      "示例",
      "开发指南",
      "贡献",
      "FAQ"
    ]
  },
  "quality_score": 92,
  "quality_issues": [
    {
      "severity": "info",
      "type": "missing_section",
      "location": "README.md",
      "message": "建议添加'安全说明'章节",
      "suggestion": "如果工具处理敏感数据，应说明安全措施"
    }
  ],
  "statistics": {
    "documented_commands": 2,
    "missing_docs": []
  }
}
```

---

### 示例3: 生成架构决策记录（ADR）

**用户请求**:
> "为选择GraphQL而不是REST API的架构决策创建ADR文档"

**Skill执行**:
```python
result = documentation_skill.execute({
    "source": {
        "type": "manual",  # 手动提供决策信息
        "decision_context": {
            "title": "为什么选择GraphQL而不是REST API",
            "status": "Accepted",
            "date": "2025-12-12",
            "context": "团队需要为新的移动应用和Web应用提供灵活的API",
            "decision": "采用GraphQL作为主API技术",
            "rationale": [
                "避免过度获取（Over-fetching）和获取不足（Under-fetching）",
                "移动端需要精确控制数据获取以节省带宽",
                "前端团队希望更灵活的数据查询",
                "自动生成API文档和类型定义"
            ],
            "consequences": {
                "positive": [
                    "客户端可以精确请求所需数据",
                    "减少API端点数量",
                    "强类型系统提升开发效率",
                    "内置GraphiQL提供交互式文档"
                ],
                "negative": [
                    "学习曲线较REST陡峭",
                    "N+1查询问题需要DataLoader解决",
                    "缓存策略比REST复杂",
                    "文件上传需要额外配置"
                ]
            },
            "alternatives": [
                {
                    "name": "REST API",
                    "pros": ["简单易懂", "广泛支持", "HTTP缓存"],
                    "cons": ["多次请求", "版本管理复杂", "过度获取"]
                },
                {
                    "name": "gRPC",
                    "pros": ["高性能", "强类型"],
                    "cons": ["浏览器支持差", "调试困难"]
                }
            ]
        }
    },
    "doc_type": "architecture",
    "format": "markdown",
    "config": {
        "template": "adr",
        "numbering": "001"
    }
})
```

**生成的ADR文档** (docs/adr/001-use-graphql-over-rest.md):
```markdown
# ADR-001: 为什么选择GraphQL而不是REST API

**状态**: ✅ Accepted
**日期**: 2025-12-12
**决策者**: 技术架构团队
**相关人员**: 前端团队、后端团队、移动团队

---

## 背景 (Context)

团队正在为新的移动应用和Web应用构建后端API。当前面临以下挑战：

1. **多端支持**: 需要同时支持iOS、Android、Web三个平台
2. **数据需求差异**: 不同客户端对同一资源有不同的数据需求
3. **网络环境**: 移动端用户可能处于弱网环境，需要精确控制数据传输
4. **开发效率**: 前端团队希望能够快速迭代，不依赖后端频繁修改API
5. **文档维护**: REST API文档维护成本高，容易过时

**现状**:
- 现有REST API已有30+端点
- 版本管理复杂（v1、v2并存）
- 移动端经常需要多次请求才能获取完整数据
- 文档更新滞后于代码变更

---

## 决策 (Decision)

**我们决定采用GraphQL作为新应用的主API技术栈。**

具体实施方案：
- 使用Apollo Server（Node.js）或Strawberry（Python）构建GraphQL服务器
- 采用Schema-First设计方法
- 使用DataLoader解决N+1查询问题
- 保留现有REST API用于遗留系统（逐步迁移）

---

## 理由 (Rationale)

### 1. 解决过度获取和获取不足问题

**REST API的痛点**:
```http
# 移动端只需要用户名和头像
GET /api/users/123
Response: {
  "id": 123,
  "username": "johndoe",
  "avatar": "...",
  "email": "...",          # 不需要
  "phone": "...",          # 不需要
  "address": { ... },      # 不需要
  "preferences": { ... }   # 不需要
}

# 获取用户的帖子还需要额外请求
GET /api/users/123/posts
```

**GraphQL解决方案**:
```graphql
# 一次请求获取精确所需数据
query {
  user(id: 123) {
    username
    avatar
    posts(limit: 5) {
      id
      title
      createdAt
    }
  }
}
```

### 2. 提升移动端性能

**带宽节省**:
- REST API平均响应: 8KB（包含大量不需要的字段）
- GraphQL精确查询: 2KB（仅包含需要的字段）
- **节省75%带宽**

**请求次数减少**:
- REST: 用户详情页需要3-4次请求（用户信息、帖子列表、关注者数量、通知）
- GraphQL: 1次请求完成
- **减少网络往返时间**

### 3. 前端开发效率提升

**类型安全**:
```typescript
// 从GraphQL Schema自动生成TypeScript类型
type User = {
  id: string;
  username: string;
  avatar: string;
  posts: Post[];
};

// IDE自动补全和类型检查
const user: User = await graphqlClient.query(...);
```

**自我文档化**:
- GraphiQL/Apollo Studio提供交互式文档
- Schema即文档，永不过时
- 字段级描述和废弃标记

### 4. 简化版本管理

**REST API版本问题**:
```
/api/v1/users/{id}        # 旧版本
/api/v2/users/{id}        # 新版本，返回格式变化
```

**GraphQL渐进式演进**:
```graphql
type User {
  username: String!
  email: String @deprecated(reason: "使用contactEmail代替")
  contactEmail: String   # 新字段，旧字段标记废弃
}
```

---

## 权衡 (Trade-offs)

### 优势 (Positive Consequences)

✅ **客户端灵活性**:
- 客户端完全控制数据获取
- 减少API变更频率
- 快速原型开发

✅ **性能优化**:
- 减少网络请求次数（移动端关键）
- 精确数据获取节省带宽
- 批处理和缓存优化空间大

✅ **开发体验**:
- 强类型系统（Schema定义）
- 自动生成文档（GraphiQL）
- 代码生成工具（graphql-codegen）
- 优秀的工具链（Apollo DevTools）

✅ **协作效率**:
- 前后端通过Schema协作
- 并行开发（Schema先行）
- Mock数据容易生成

### 挑战 (Negative Consequences)

⚠️ **学习曲线**:
- 团队需要学习GraphQL概念（Schema、Resolver、Fragment等）
- **缓解措施**: 组织2周培训，提供内部最佳实践文档

⚠️ **N+1查询问题**:
```graphql
# 容易引发N+1查询
query {
  users {           # 1次查询获取所有用户
    posts {         # N次查询（每个用户查询一次posts）
      comments {    # N*M次查询
        author
      }
    }
  }
}
```
- **缓解措施**: 使用DataLoader批量加载和缓存

⚠️ **缓存复杂性**:
- REST可以利用HTTP缓存（ETag、Last-Modified）
- GraphQL需要自定义缓存策略（Apollo Cache、Relay）
- **缓解措施**: 使用Apollo Client的智能缓存

⚠️ **文件上传**:
- GraphQL本身不支持文件上传
- **缓解措施**: 使用graphql-upload中间件或分离的REST端点

⚠️ **速率限制和安全**:
- 复杂查询可能导致服务器过载
- **缓解措施**:
  - 查询深度限制（max depth: 5）
  - 查询复杂度分析（cost analysis）
  - 持久化查询（仅允许预定义查询）

---

## 替代方案 (Alternatives)

### 方案A: 继续使用REST API

**优点**:
- 团队已熟悉
- HTTP缓存机制成熟
- 调试工具丰富（Postman、cURL）

**缺点**:
- 无法解决过度获取问题
- 版本管理复杂（需要维护v1、v2）
- 移动端性能无法优化
- 文档维护成本高

**为什么拒绝**: 无法满足移动端性能需求，长期维护成本高。

### 方案B: gRPC

**优点**:
- 高性能（Protocol Buffers二进制序列化）
- 强类型（.proto文件定义）
- 流式传输支持

**缺点**:
- 浏览器支持差（需要gRPC-Web代理）
- 调试困难（二进制格式）
- 学习曲线陡峭
- 生态不如GraphQL成熟

**为什么拒绝**: Web端支持不足，不适合我们的多端场景。

---

## 实施计划 (Implementation Plan)

### Phase 1: 基础设施搭建（Week 1-2）
- [ ] 选择GraphQL服务器框架（Apollo Server）
- [ ] 设计Schema（核心实体：User、Post、Comment）
- [ ] 实现基础Resolver
- [ ] 配置DataLoader
- [ ] 设置GraphiQL开发环境

### Phase 2: 核心功能迁移（Week 3-6）
- [ ] 用户认证与授权（JWT）
- [ ] 用户CRUD操作
- [ ] 帖子和评论功能
- [ ] 文件上传（头像、图片）
- [ ] 实时订阅（Subscriptions）

### Phase 3: 性能优化（Week 7-8）
- [ ] DataLoader批量加载优化
- [ ] 查询复杂度限制
- [ ] Apollo Cache配置
- [ ] 性能监控（Apollo Studio）

### Phase 4: 前端集成（Week 9-10）
- [ ] Apollo Client集成（React/Vue）
- [ ] 代码生成配置（graphql-codegen）
- [ ] 移动端SDK集成
- [ ] E2E测试

### Phase 5: 文档和培训（Week 11-12）
- [ ] 编写最佳实践文档
- [ ] 团队培训（Schema设计、Resolver编写）
- [ ] 迁移指南（REST → GraphQL）
- [ ] 生产部署

---

## 成功指标 (Success Metrics)

我们将通过以下指标评估这个决策的成功：

1. **性能指标**:
   - 移动端API请求次数减少≥60%
   - 移动端数据传输量减少≥50%
   - API响应时间≤200ms (P95)

2. **开发效率**:
   - 新功能API开发时间减少≥30%
   - 前端开发等待后端API时间减少≥50%

3. **质量指标**:
   - API文档覆盖率100%（自动生成）
   - 类型错误减少≥80%（TypeScript集成）

4. **采纳度**:
   - 6个月内80%新功能使用GraphQL
   - 团队满意度≥4/5

---

## 相关文档 (References)

- [GraphQL官方文档](https://graphql.org/)
- [Apollo Server文档](https://www.apollographql.com/docs/apollo-server/)
- [DataLoader GitHub](https://github.com/graphql/dataloader)
- [GraphQL最佳实践](https://graphql.org/learn/best-practices/)
- ADR-002: GraphQL Schema设计规范（待编写）
- ADR-003: GraphQL安全和速率限制策略（待编写）

---

## 修订历史 (Revision History)

| 日期 | 版本 | 作者 | 变更说明 |
|------|------|------|---------|
| 2025-12-12 | 1.0 | Tech Team | 初始版本，决策通过 |

---

**下次审查日期**: 2025-06-12（6个月后评估实施效果）

---

*此ADR由Claude Code documentation skill自动生成*
```

**输出摘要**:
```json
{
  "document": "[完整ADR文档]",
  "assets": [],
  "format": "markdown",
  "metadata": {
    "title": "ADR-001: 为什么选择GraphQL而不是REST API",
    "version": "1.0",
    "generated_at": "2025-12-12T11:00:00Z",
    "decision_number": "001",
    "status": "Accepted",
    "word_count": 2000,
    "sections": [
      "背景",
      "决策",
      "理由",
      "权衡",
      "替代方案",
      "实施计划",
      "成功指标"
    ]
  },
  "quality_score": 98,
  "quality_issues": [],
  "statistics": {
    "alternatives_considered": 2,
    "implementation_phases": 5,
    "success_metrics": 4
  }
}
```

---

## Best Practices

### 1. 文档即代码（Docs as Code）

**原则**:
- 文档与代码存储在同一仓库
- 使用版本控制管理文档
- 通过CI/CD自动构建和部署文档
- 代码审查时同时审查文档

**实施**:
```yaml
# .github/workflows/docs.yml
name: Build and Deploy Docs

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'docs/**'

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate API Docs
        run: |
          # 从代码生成API文档
          python -m documentation_skill generate

      - name: Build HTML
        run: |
          mkdocs build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

### 2. 保持文档与代码同步

**技术**:
- 使用Pre-commit Hook检查文档完整性
- 从代码注释自动生成文档
- 设置文档覆盖率阈值

**示例**:
```python
# pre-commit hook: check-docs-coverage
import ast
import sys

def check_documentation_coverage(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    functions = [node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef)]

    documented = sum(1 for func in functions
                     if ast.get_docstring(func))

    coverage = documented / len(functions) * 100

    if coverage < 80:  # 最低80%覆盖率
        print(f"❌ Documentation coverage ({coverage:.1f}%) below threshold (80%)")
        sys.exit(1)
    else:
        print(f"✓ Documentation coverage: {coverage:.1f}%")

check_documentation_coverage('src/api.py')
```

### 3. 分层文档策略

**四层文档模型**:
1. **学习层** (Learning): 教程、快速开始
2. **目标层** (Goal-oriented): How-to指南、常见任务
3. **信息层** (Information): API参考、数据模型
4. **理解层** (Understanding): 架构文档、设计决策（ADR）

**示例结构**:
```
docs/
├── tutorials/           # 学习层
│   ├── getting-started.md
│   └── your-first-api.md
├── how-to/              # 目标层
│   ├── authentication.md
│   └── error-handling.md
├── reference/           # 信息层
│   ├── api/
│   │   └── users.md
│   └── models/
│       └── user.md
└── explanation/         # 理解层
    ├── architecture.md
    └── adr/
        └── 001-graphql.md
```

### 4. 使用示例驱动文档

**原则**:
- 每个API端点至少1个工作示例
- 示例代码可直接复制运行
- 包含常见和边缘场景
- 使用真实数据（脱敏）

**反模式**:
```markdown
❌ 差的文档:
## 创建用户
POST /api/users
Body: user data
```

**最佳实践**:
```markdown
✅ 好的文档:
## 创建用户

**端点**: POST /api/users

**完整示例**:
```bash
curl -X POST https://api.example.com/v1/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "johndoe@example.com",
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**成功响应** (201):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "johndoe@example.com",
  "username": "johndoe"
}
```

**错误场景 - 邮箱已存在** (400):
```json
{
  "detail": "Email already registered"
}
```
```

### 5. 自动化文档质量检查

**检查项**:
- 拼写检查（cSpell、Vale）
- 链接有效性（markdown-link-check）
- 代码示例可执行性（doctest）
- 文档完整性（覆盖率）

**工具集成**:
```bash
# package.json scripts
{
  "scripts": {
    "docs:spell": "cspell 'docs/**/*.md'",
    "docs:links": "markdown-link-check docs/**/*.md",
    "docs:test": "python -m doctest docs/examples/*.md",
    "docs:coverage": "python check_docs_coverage.py"
  }
}
```

---

## Related Skills

- `code-generator`: 为生成的代码自动创建API文档
- `requirements`: 从需求规格生成用户故事和活文档
- `test-automation`: 从测试用例生成测试报告文档
- `code-review`: 检查代码注释和文档字符串的完整性

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | 重大升级：新增活文档生成、ADR模板、多格式输出 |
| 1.5.0 | 2025-10-01 | 添加OpenAPI 3.0支持、改进README生成 |
| 1.0.0 | 2025-06-01 | 初始版本：基础API文档和README生成 |

---

**生成时间**: 2025-12-12T12:00:00Z
**Skill版本**: documentation v2.0.0
**文档字数**: 7,800+
