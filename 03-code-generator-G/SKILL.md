---
name: 03-code-generator-G
description: Code generation engine that automatically generates production-grade code from specifications. Supports contract-driven development (OpenAPI→Code), multiple languages (Python/TypeScript/Go/Java/Rust), complete CRUD generation, project scaffolding, Clean/Pragmatic architecture. Use for rapid prototyping, CRUD interfaces, new project scaffolding. Works with specflow domain models.
---

# code-generator - 代码生成引擎

**版本**: 2.0.0
**优先级**: P0
**类别**: 核心开发流程

## 描述

代码生成引擎Skill，从规格文档和领域模型自动生成生产级代码。支持契约驱动开发(Contract-First Development)，能够根据OpenAPI规范、JSON Schema、数据库Schema等输入，生成完整的、符合最佳实践的代码项目。

### 核心能力

1. **契约驱动生成**: 从OpenAPI 3.0、JSON Schema、GraphQL Schema生成代码
2. **多语言支持**: Python、JavaScript、TypeScript、Go、Java、Rust
3. **框架集成**: FastAPI、Express、Spring Boot、Django、NestJS等主流框架
4. **完整CRUD**: 自动生成增删改查操作及相关路由
5. **项目脚手架**: 创建完整的项目结构，包括配置、测试、文档

---

## Instructions

当用户需要生成代码时，你将作为代码生成专家执行以下流程：

### 触发条件
- 用户说"生成代码"或"实现这个API"
- 用户说"创建CRUD接口"或"生成项目骨架"
- 用户提供OpenAPI规范并要求生成服务端/客户端代码
- 用户说"基于这个数据模型生成代码"
- 用户说"创建新项目"并提供技术栈

### 代码生成流程

#### 1. 输入理解
- 接收规格文档（OpenAPI、JSON Schema、领域模型）
- 识别实体关系和业务逻辑
- 确定目标语言和框架
- 了解代码风格偏好（Clean Architecture / Pragmatic）

#### 2. 项目结构设计

**Python + FastAPI**:
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── models/              # SQLAlchemy模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic模式
│   │   ├── __init__.py
│   │   └── user.py
│   ├── crud/                # CRUD操作
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── deps.py          # 依赖注入
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── users.py
│   ├── core/                # 核心功能
│   │   ├── __init__.py
│   │   ├── security.py      # 认证/加密
│   │   └── database.py      # 数据库连接
│   └── tests/               # 测试
│       ├── __init__.py
│       └── test_users.py
├── alembic/                 # 数据库迁移
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

**TypeScript + Express**:
```
project/
├── src/
│   ├── index.ts             # Express应用入口
│   ├── config/
│   │   └── database.ts
│   ├── models/              # TypeORM/Sequelize模型
│   │   └── User.ts
│   ├── controllers/         # 控制器
│   │   └── UserController.ts
│   ├── services/            # 业务逻辑
│   │   └── UserService.ts
│   ├── routes/              # 路由
│   │   └── users.ts
│   ├── middleware/          # 中间件
│   │   ├── auth.ts
│   │   └── errorHandler.ts
│   └── types/               # TypeScript类型
│       └── User.ts
├── tests/
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

#### 3. 代码生成规则

**命名规范**:
- Python: `snake_case` (文件名、变量、函数)
- TypeScript/JavaScript: `camelCase` (变量、函数), `PascalCase` (类、组件)
- Go: `PascalCase` (导出), `camelCase` (内部)
- Java: `camelCase` (变量、方法), `PascalCase` (类)

**代码风格**:

**Clean Architecture风格** (适合大型项目):
```python
# 严格的分层架构
app/
├── domain/           # 领域层 (业务逻辑)
│   ├── entities/
│   ├── value_objects/
│   └── repositories/  # 接口定义
├── application/      # 应用层 (用例)
│   └── use_cases/
├── infrastructure/   # 基础设施层 (实现)
│   ├── repositories/  # 仓储实现
│   └── database/
└── presentation/     # 表现层 (API)
    └── api/
```

**Pragmatic风格** (适合中小型项目，推荐):
```python
# 实用的扁平结构
app/
├── models.py         # 数据模型
├── schemas.py        # 验证模式
├── crud.py           # CRUD操作
├── api/              # API路由
└── core/             # 核心功能
```

#### 4. 代码质量保证

生成的代码必须包含:
- ✅ **类型注解**: Python类型提示、TypeScript严格模式
- ✅ **数据验证**: Pydantic、Joi、Zod等
- ✅ **错误处理**: 统一的异常处理中间件
- ✅ **安全实践**: 密码哈希、SQL参数化、CORS配置
- ✅ **文档字符串**: 每个函数都有docstring或JSDoc
- ✅ **测试用例**: 关键功能的单元测试

#### 5. CRUD生成模板

**基于实体自动生成**:
```python
# 输入: User实体 (email, password, username)
# 输出: 完整CRUD操作

# models/user.py
class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# schemas/user.py
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# crud/user.py
class UserCRUD:
    def create(self, db: Session, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=hashed_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: UUID) -> User:
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj

# api/v1/users.py
router = APIRouter()

@router.post("/", response_model=UserInDB, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建新用户"""
    if crud_user.get_by_email(db, email=user.email):
        raise HTTPException(400, "Email already registered")
    return crud_user.create(db, obj_in=user)

@router.get("/{user_id}", response_model=UserInDB)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """获取用户详情"""
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.get("/", response_model=List[UserInDB])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """列出用户（分页）"""
    return crud_user.get_multi(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserInDB)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return crud_user.update(db, db_obj=user, obj_in=user_update)

@router.delete("/{user_id}", response_model=UserInDB)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """删除用户"""
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return crud_user.delete(db, id=user_id)
```

### 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| specification | object | 是 | - | API规格或领域模型 |
| specification.type | string | 是 | - | 规格类型: `openapi`/`json_schema`/`domain_model` |
| specification.content | string\|object | 是 | - | 规格内容（YAML/JSON） |
| language | string | 是 | - | 目标语言: `python`/`typescript`/`go`/`java`/`rust` |
| framework | string | 是 | - | 目标框架: `fastapi`/`express`/`nestjs`/`spring`/`gin` |
| style | string | 否 | "pragmatic" | 代码风格: `clean`/`pragmatic` |
| database | string | 否 | "postgresql" | 数据库: `postgresql`/`mysql`/`mongodb`/`sqlite` |
| auth_type | string | 否 | "jwt" | 认证方式: `jwt`/`session`/`oauth2`/`none` |
| include_tests | boolean | 否 | true | 是否生成测试代码 |
| include_docker | boolean | 否 | true | 是否生成Dockerfile和docker-compose.yml |
| api_version | string | 否 | "v1" | API版本号 |

### 输出格式

```typescript
interface CodeGenerationOutput {
  files: Array<{
    path: string;           // 文件路径
    content: string;        // 文件内容
    language: string;       // 语言标识
  }>;

  project_structure: {
    type: "tree";
    content: string;        // ASCII树形结构
  };

  setup_instructions: {
    install_dependencies: string[];    // 安装命令
    database_setup: string[];          // 数据库初始化
    run_commands: string[];            // 运行命令
  };

  generated_endpoints: Array<{
    method: string;         // GET, POST, etc.
    path: string;           // /api/users
    description: string;
  }>;

  next_steps: string[];     // 后续开发建议
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
interface CodeGeneratorInput {
  // ... 其他字段

  security?: {
    level?: 'basic' | 'standard' | 'strict';
    checks?: {
      sqlInjection?: boolean;
      xss?: boolean;
      csrf?: boolean;
      inputValidation?: boolean;
    };
    scanAfterGeneration?: boolean;
  };

  performance?: {
    parallelGeneration?: boolean;
    workerCount?: number;
    batchSize?: number;
    templateCaching?: boolean;
    timeout?: number;
  };
}
```

### 输出接口

```typescript
interface CodeGeneratorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段

  securityValidation?: {
    passed: boolean;
    level: string;
    findings: Array<{
      severity: 'critical' | 'high' | 'medium' | 'low';
      category: string;
      file: string;
      line: number;
      description: string;
      autoFixed?: boolean;
    }>;
    summary: {
      critical: number;
      high: number;
      medium: number;
      low: number;
    };
  };

  performance?: {
    totalTime: number;
    breakdown: {
      templateParsing: number;
      codeGeneration: number;
      securityValidation: number;
      fileWriting: number;
    };
    optimization: {
      parallelWorkers: number;
      cachedTemplates: number;
      filesPerSecond: number;
    };
    recommendation?: string;
  };
}
```

---

## Examples

### 示例 1: 生成博客系统API (Python + FastAPI)

**用户输入:**
```
生成博客系统API，Python + FastAPI。需要：
- 用户管理（注册、登录）
- 文章管理（创建、编辑、删除、列表）
- 评论功能
- 标签系统
使用PostgreSQL，包含JWT认证。
```

**Skill输出:**

```markdown
# 博客系统代码生成完成

## 项目结构

```
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── tag.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── tag.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── tag.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── posts.py
│   │       ├── comments.py
│   │       └── tags.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_posts.py
│       └── conftest.py
├── alembic/
│   ├── versions/
│   └── env.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 核心文件内容

### app/models/post.py
```python
from sqlalchemy import Column, String, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base

# 多对多关联表
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', UUID, ForeignKey('posts.id', ondelete='CASCADE')),
    Column('tag_id', UUID, ForeignKey('tags.id', ondelete='CASCADE'))
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    published = Column(Boolean, default=False)

    # 外键
    author_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # 关系
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
```

### app/schemas/post.py
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import re

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    published: bool = False

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v

class PostCreate(PostBase):
    tag_names: List[str] = []

    @validator('tag_names')
    def validate_tags(cls, v):
        return [tag.strip().lower() for tag in v if tag.strip()]

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    published: Optional[bool] = None
    tag_names: Optional[List[str]] = None

class PostInDB(PostBase):
    id: UUID
    slug: str
    author_id: UUID
    tags: List[TagBase]
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

class PostPublic(PostInDB):
    author: 'UserPublic'
    comment_count: int = 0
```

### app/crud/post.py
```python
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from slugify import slugify
from datetime import datetime

from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import PostCreate, PostUpdate

class PostCRUD:
    def create(self, db: Session, *, obj_in: PostCreate, author_id: UUID) -> Post:
        # 生成slug
        slug = slugify(obj_in.title)

        # 检查slug唯一性
        existing = db.query(Post).filter(Post.slug == slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:8]}"

        # 处理标签
        tags = []
        for tag_name in obj_in.tag_names:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.add(tag)
            tags.append(tag)

        # 创建文章
        db_obj = Post(
            title=obj_in.title,
            slug=slug,
            content=obj_in.content,
            excerpt=obj_in.excerpt or obj_in.content[:200],
            published=obj_in.published,
            author_id=author_id,
            tags=tags
        )

        if obj_in.published:
            db_obj.published_at = datetime.utcnow()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Post]:
        return db.query(Post).filter(Post.slug == slug).first()

    def get_multi_published(
        self, db: Session, *, skip: int = 0, limit: int = 20, tag: Optional[str] = None
    ) -> List[Post]:
        query = db.query(Post).filter(Post.published == True)

        if tag:
            query = query.join(Post.tags).filter(Tag.name == tag)

        return query.order_by(Post.published_at.desc()).offset(skip).limit(limit).all()

    def get_by_author(
        self, db: Session, *, author_id: UUID, skip: int = 0, limit: int = 20
    ) -> List[Post]:
        return (
            db.query(Post)
            .filter(Post.author_id == author_id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self, db: Session, *, db_obj: Post, obj_in: PostUpdate
    ) -> Post:
        update_data = obj_in.dict(exclude_unset=True)

        # 处理标签
        if "tag_names" in update_data:
            tag_names = update_data.pop("tag_names")
            tags = []
            for tag_name in tag_names:
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name, slug=slugify(tag_name))
                    db.add(tag)
                tags.append(tag)
            db_obj.tags = tags

        # 更新标题时重新生成slug
        if "title" in update_data:
            update_data["slug"] = slugify(update_data["title"])

        # 发布时记录时间
        if "published" in update_data and update_data["published"] and not db_obj.published:
            update_data["published_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: UUID) -> Post:
        obj = db.query(Post).get(id)
        db.delete(obj)
        db.commit()
        return obj

post_crud = PostCRUD()
```

### app/api/v1/posts.py
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api import deps
from app.schemas.post import PostCreate, PostUpdate, PostPublic, PostInDB
from app.crud.post import post_crud
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PostInDB, status_code=201)
def create_post(
    post: PostCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """创建新文章（需要认证）"""
    return post_crud.create(db, obj_in=post, author_id=current_user.id)

@router.get("/", response_model=List[PostPublic])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tag: Optional[str] = None,
    db: Session = Depends(deps.get_db)
):
    """列出已发布文章（公开）"""
    posts = post_crud.get_multi_published(db, skip=skip, limit=limit, tag=tag)
    return posts

@router.get("/my-posts", response_model=List[PostInDB])
def list_my_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """列出当前用户的所有文章（包括草稿）"""
    return post_crud.get_by_author(db, author_id=current_user.id, skip=skip, limit=limit)

@router.get("/{slug}", response_model=PostPublic)
def read_post(slug: str, db: Session = Depends(deps.get_db)):
    """根据slug获取文章详情"""
    post = post_crud.get_by_slug(db, slug=slug)
    if not post:
        raise HTTPException(404, "Post not found")
    if not post.published:
        raise HTTPException(403, "Post is not published")
    return post

@router.put("/{post_id}", response_model=PostInDB)
def update_post(
    post_id: UUID,
    post_update: PostUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """更新文章（仅作者本人）"""
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(403, "Not authorized to edit this post")

    return post_crud.update(db, db_obj=post, obj_in=post_update)

@router.delete("/{post_id}", response_model=PostInDB)
def delete_post(
    post_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """删除文章（仅作者本人）"""
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(403, "Not authorized to delete this post")

    return post_crud.delete(db, id=post_id)
```

## 部署配置

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: bloguser
      POSTGRES_PASSWORD: blogpass
      POSTGRES_DB: blogdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://bloguser:blogpass@db:5432/blogdb
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 设置指令

### 1. 安装依赖
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-jose[cryptography] passlib[bcrypt] python-slugify
```

### 2. 数据库初始化
```bash
# 创建迁移
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3. 运行开发服务器
```bash
uvicorn app.main:app --reload
```

或使用Docker:
```bash
docker-compose up
```

## 生成的API端点

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新token

### 文章
- `POST /api/v1/posts/` - 创建文章（需认证）
- `GET /api/v1/posts/` - 列出已发布文章（公开，支持tag过滤）
- `GET /api/v1/posts/my-posts` - 我的文章（需认证）
- `GET /api/v1/posts/{slug}` - 文章详情
- `PUT /api/v1/posts/{post_id}` - 更新文章（需认证，仅作者）
- `DELETE /api/v1/posts/{post_id}` - 删除文章（需认证，仅作者）

### 评论
- `POST /api/v1/posts/{post_id}/comments` - 添加评论（需认证）
- `GET /api/v1/posts/{post_id}/comments` - 获取文章评论
- `DELETE /api/v1/comments/{comment_id}` - 删除评论（需认证，仅作者）

### 标签
- `GET /api/v1/tags/` - 列出所有标签
- `GET /api/v1/tags/{tag_name}/posts` - 获取特定标签的文章

## 后续开发建议

1. **添加功能**:
   - 文章搜索（Elasticsearch集成）
   - 图片上传（S3/Cloudinary）
   - 文章点赞和收藏
   - RSS feed

2. **性能优化**:
   - 添加Redis缓存（热门文章）
   - 数据库查询优化（N+1问题）
   - 分页优化（游标分页）

3. **安全增强**:
   - Rate limiting
   - CORS配置
   - Content Security Policy
   - XSS防护

4. **测试**:
   - 运行测试: `pytest tests/ -v --cov`
   - 覆盖率目标: > 80%
```

---

### 示例 2: TypeScript + NestJS微服务

**用户输入:**
```
生成一个商品管理微服务，TypeScript + NestJS。
需要商品CRUD、分类管理、库存跟踪。
使用MongoDB，包含GraphQL API。
```

**Skill输出:**

```markdown
# 商品管理微服务代码生成

## 项目结构

```
product-service/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── config/
│   │   └── database.config.ts
│   ├── common/
│   │   ├── decorators/
│   │   ├── filters/
│   │   ├── guards/
│   │   └── interceptors/
│   ├── products/
│   │   ├── products.module.ts
│   │   ├── products.service.ts
│   │   ├── products.resolver.ts
│   │   ├── products.controller.ts
│   │   ├── dto/
│   │   │   ├── create-product.input.ts
│   │   │   └── update-product.input.ts
│   │   ├── entities/
│   │   │   └── product.entity.ts
│   │   └── schemas/
│   │       └── product.schema.ts
│   ├── categories/
│   │   ├── categories.module.ts
│   │   ├── categories.service.ts
│   │   ├── categories.resolver.ts
│   │   └── schemas/
│   │       └── category.schema.ts
│   └── inventory/
│       ├── inventory.module.ts
│       ├── inventory.service.ts
│       └── schemas/
│           └── inventory-log.schema.ts
├── test/
│   ├── products.e2e-spec.ts
│   └── jest-e2e.json
├── .env.example
├── nest-cli.json
├── package.json
├── tsconfig.json
└── README.md
```

## 核心代码

### src/products/schemas/product.schema.ts
```typescript
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { Field, ObjectType, ID, Float, Int } from '@nestjs/graphql';

@ObjectType()
@Schema({ timestamps: true })
export class Product extends Document {
  @Field(() => ID)
  _id: Types.ObjectId;

  @Field()
  @Prop({ required: true, trim: true })
  name: string;

  @Field()
  @Prop({ required: true, unique: true })
  sku: string;

  @Field({ nullable: true })
  @Prop({ type: String })
  description?: string;

  @Field(() => Float)
  @Prop({ required: true, min: 0 })
  price: number;

  @Field(() => Int)
  @Prop({ required: true, min: 0, default: 0 })
  stock: number;

  @Field(() => ID)
  @Prop({ type: Types.ObjectId, ref: 'Category', required: true })
  categoryId: Types.ObjectId;

  @Field(() => [String])
  @Prop({ type: [String], default: [] })
  images: string[];

  @Field()
  @Prop({ default: true })
  isActive: boolean;

  @Field()
  createdAt: Date;

  @Field()
  updatedAt: Date;
}

export const ProductSchema = SchemaFactory.createForClass(Product);

// 索引
ProductSchema.index({ sku: 1 });
ProductSchema.index({ categoryId: 1 });
ProductSchema.index({ name: 'text', description: 'text' });
```

### src/products/dto/create-product.input.ts
```typescript
import { InputType, Field, Float, Int, ID } from '@nestjs/graphql';
import { IsString, IsNumber, IsOptional, Min, IsMongoId, IsArray, IsUrl } from 'class-validator';

@InputType()
export class CreateProductInput {
  @Field()
  @IsString()
  name: string;

  @Field()
  @IsString()
  sku: string;

  @Field({ nullable: true })
  @IsString()
  @IsOptional()
  description?: string;

  @Field(() => Float)
  @IsNumber()
  @Min(0)
  price: number;

  @Field(() => Int)
  @IsNumber()
  @Min(0)
  stock: number;

  @Field(() => ID)
  @IsMongoId()
  categoryId: string;

  @Field(() => [String], { nullable: true })
  @IsArray()
  @IsUrl({}, { each: true })
  @IsOptional()
  images?: string[];
}
```

### src/products/products.service.ts
```typescript
import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import { Product } from './schemas/product.schema';
import { CreateProductInput } from './dto/create-product.input';
import { UpdateProductInput } from './dto/update-product.input';
import { InventoryService } from '../inventory/inventory.service';

@Injectable()
export class ProductsService {
  constructor(
    @InjectModel(Product.name) private productModel: Model<Product>,
    private inventoryService: InventoryService,
  ) {}

  async create(createProductInput: CreateProductInput): Promise<Product> {
    // 检查SKU唯一性
    const existing = await this.productModel.findOne({ sku: createProductInput.sku });
    if (existing) {
      throw new ConflictException(`Product with SKU ${createProductInput.sku} already exists`);
    }

    const product = new this.productModel(createProductInput);
    await product.save();

    // 记录初始库存
    if (createProductInput.stock > 0) {
      await this.inventoryService.logStockChange({
        productId: product._id,
        quantity: createProductInput.stock,
        type: 'INITIAL',
        notes: 'Initial stock on product creation',
      });
    }

    return product;
  }

  async findAll(filter: {
    categoryId?: string;
    minPrice?: number;
    maxPrice?: number;
    inStock?: boolean;
    search?: string;
    skip?: number;
    limit?: number;
  }): Promise<Product[]> {
    const query: any = {};

    if (filter.categoryId) {
      query.categoryId = new Types.ObjectId(filter.categoryId);
    }

    if (filter.minPrice !== undefined || filter.maxPrice !== undefined) {
      query.price = {};
      if (filter.minPrice !== undefined) query.price.$gte = filter.minPrice;
      if (filter.maxPrice !== undefined) query.price.$lte = filter.maxPrice;
    }

    if (filter.inStock) {
      query.stock = { $gt: 0 };
    }

    if (filter.search) {
      query.$text = { $search: filter.search };
    }

    return this.productModel
      .find(query)
      .skip(filter.skip || 0)
      .limit(filter.limit || 20)
      .sort({ createdAt: -1 })
      .populate('categoryId')
      .exec();
  }

  async findOne(id: string): Promise<Product> {
    const product = await this.productModel
      .findById(id)
      .populate('categoryId')
      .exec();

    if (!product) {
      throw new NotFoundException(`Product with ID ${id} not found`);
    }

    return product;
  }

  async findBySku(sku: string): Promise<Product> {
    const product = await this.productModel.findOne({ sku });
    if (!product) {
      throw new NotFoundException(`Product with SKU ${sku} not found`);
    }
    return product;
  }

  async update(id: string, updateProductInput: UpdateProductInput): Promise<Product> {
    const product = await this.findOne(id);

    // 如果更新了SKU，检查新SKU是否已存在
    if (updateProductInput.sku && updateProductInput.sku !== product.sku) {
      const existing = await this.productModel.findOne({ sku: updateProductInput.sku });
      if (existing) {
        throw new ConflictException(`SKU ${updateProductInput.sku} already exists`);
      }
    }

    // 如果更新了库存，记录变更
    if (updateProductInput.stock !== undefined && updateProductInput.stock !== product.stock) {
      const diff = updateProductInput.stock - product.stock;
      await this.inventoryService.logStockChange({
        productId: product._id,
        quantity: diff,
        type: diff > 0 ? 'RESTOCK' : 'ADJUSTMENT',
        notes: 'Stock updated manually',
      });
    }

    Object.assign(product, updateProductInput);
    await product.save();

    return product;
  }

  async remove(id: string): Promise<Product> {
    const product = await this.findOne(id);
    await product.deleteOne();
    return product;
  }

  async decreaseStock(id: string, quantity: number): Promise<Product> {
    const product = await this.findOne(id);

    if (product.stock < quantity) {
      throw new ConflictException(`Insufficient stock. Available: ${product.stock}, Requested: ${quantity}`);
    }

    product.stock -= quantity;
    await product.save();

    await this.inventoryService.logStockChange({
      productId: product._id,
      quantity: -quantity,
      type: 'SALE',
      notes: 'Stock decreased due to sale',
    });

    return product;
  }
}
```

### src/products/products.resolver.ts (GraphQL)
```typescript
import { Resolver, Query, Mutation, Args, ID, Int, Float } from '@nestjs/graphql';
import { ProductsService } from './products.service';
import { Product } from './schemas/product.schema';
import { CreateProductInput } from './dto/create-product.input';
import { UpdateProductInput } from './dto/update-product.input';

@Resolver(() => Product)
export class ProductsResolver {
  constructor(private readonly productsService: ProductsService) {}

  @Mutation(() => Product)
  createProduct(@Args('input') input: CreateProductInput): Promise<Product> {
    return this.productsService.create(input);
  }

  @Query(() => [Product], { name: 'products' })
  findAll(
    @Args('categoryId', { type: () => ID, nullable: true }) categoryId?: string,
    @Args('minPrice', { type: () => Float, nullable: true }) minPrice?: number,
    @Args('maxPrice', { type: () => Float, nullable: true }) maxPrice?: number,
    @Args('inStock', { nullable: true }) inStock?: boolean,
    @Args('search', { nullable: true }) search?: string,
    @Args('skip', { type: () => Int, nullable: true }) skip?: number,
    @Args('limit', { type: () => Int, nullable: true }) limit?: number,
  ): Promise<Product[]> {
    return this.productsService.findAll({
      categoryId,
      minPrice,
      maxPrice,
      inStock,
      search,
      skip,
      limit,
    });
  }

  @Query(() => Product, { name: 'product' })
  findOne(@Args('id', { type: () => ID }) id: string): Promise<Product> {
    return this.productsService.findOne(id);
  }

  @Mutation(() => Product)
  updateProduct(
    @Args('id', { type: () => ID }) id: string,
    @Args('input') input: UpdateProductInput,
  ): Promise<Product> {
    return this.productsService.update(id, input);
  }

  @Mutation(() => Product)
  removeProduct(@Args('id', { type: () => ID }) id: string): Promise<Product> {
    return this.productsService.remove(id);
  }

  @Mutation(() => Product)
  decreaseProductStock(
    @Args('id', { type: () => ID }) id: string,
    @Args('quantity', { type: () => Int }) quantity: number,
  ): Promise<Product> {
    return this.productsService.decreaseStock(id, quantity);
  }
}
```

## GraphQL Schema

自动生成的schema:
```graphql
type Product {
  _id: ID!
  name: String!
  sku: String!
  description: String
  price: Float!
  stock: Int!
  categoryId: ID!
  images: [String!]!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
}

input CreateProductInput {
  name: String!
  sku: String!
  description: String
  price: Float!
  stock: Int!
  categoryId: ID!
  images: [String!]
}

input UpdateProductInput {
  name: String
  sku: String
  description: String
  price: Float
  stock: Int
  categoryId: ID
  images: [String!]
  isActive: Boolean
}

type Query {
  products(
    categoryId: ID
    minPrice: Float
    maxPrice: Float
    inStock: Boolean
    search: String
    skip: Int
    limit: Int
  ): [Product!]!
  product(id: ID!): Product!
}

type Mutation {
  createProduct(input: CreateProductInput!): Product!
  updateProduct(id: ID!, input: UpdateProductInput!): Product!
  removeProduct(id: ID!): Product!
  decreaseProductStock(id: ID!, quantity: Int!): Product!
}
```

## 测试示例

### GraphQL查询测试
```graphql
# 创建商品
mutation {
  createProduct(input: {
    name: "iPhone 15 Pro"
    sku: "IPH15-PRO-256-BLK"
    description: "Latest iPhone with A17 chip"
    price: 999.99
    stock: 50
    categoryId: "507f1f77bcf86cd799439011"
    images: ["https://example.com/iphone.jpg"]
  }) {
    _id
    name
    sku
    price
  }
}

# 查询商品（带过滤）
query {
  products(
    categoryId: "507f1f77bcf86cd799439011"
    minPrice: 500
    maxPrice: 1500
    inStock: true
    skip: 0
    limit: 10
  ) {
    _id
    name
    price
    stock
  }
}

# 扣减库存
mutation {
  decreaseProductStock(id: "507f191e810c19729de860ea", quantity: 5) {
    _id
    stock
  }
}
```

## 设置指令

```bash
# 安装依赖
npm install

# 运行开发服务器
npm run start:dev

# GraphQL Playground
# http://localhost:3000/graphql
```
```

---

## 最佳实践

1. **遵循框架约定**
   - FastAPI使用Pydantic数据验证
   - NestJS使用class-validator装饰器
   - 遵循官方项目结构规范

2. **完整的类型安全**
   - Python: 完整类型提示,Mypy检查
   - TypeScript: 严格模式(`strict: true`)
   - 避免`any`类型

3. **安全编码**
   - SQL参数化查询(防止注入)
   - 密码哈希(bcrypt,不存明文)
   - CORS配置正确
   - 输入验证完整

4. **可测试性**
   - 依赖注入
   - 服务层与路由层分离
   - 生成测试用例模板

5. **文档完整**
   - 每个API端点有描述
   - 复杂逻辑有注释
   - README包含设置指令

---

## 相关Skills

- **architecture** (架构设计): 接收技术栈和架构决策
- **test-automation** (测试自动化): 为生成的代码创建测试套件
- **code-review** (代码审查): 审查生成代码的质量和安全性
- **documentation** (文档生成): 生成API文档和使用指南

---

## 版本历史

- **2.0.0** (2025-12-12): 重构设计,增强多框架支持和GraphQL集成
- **1.0.0** (2025-01-01): 初始版本
