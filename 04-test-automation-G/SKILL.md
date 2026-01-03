---
name: 04-test-automation-G
description: Test automation expert that generates unit/integration/E2E tests with 80%+ coverage. Supports AAA pattern, boundary testing, BDD (Given-When-Then), auto-generated mocks and fixtures, coverage analysis. Use for TDD development, refactoring safety, CI/CD quality gates.
---

# test-automation - 测试自动化专家

**版本**: 2.0.0
**优先级**: P0
**类别**: 核心开发流程

## 描述

测试自动化专家Skill，为代码自动生成全面的测试套件，包括单元测试、集成测试、E2E测试和BDD测试。能够分析代码逻辑自动生成边界值测试、异常处理测试，并估算测试覆盖率，目标达到80%以上的代码覆盖率。

### 核心能力

1. **单元测试**: 为每个函数/方法生成独立测试用例，覆盖正常和异常路径
2. **集成测试**: 测试API端点、数据库交互、第三方服务集成
3. **E2E测试**: 生成Playwright/Cypress端到端测试，模拟真实用户行为
4. **BDD测试**: 从Gherkin场景生成pytest-bdd/Cucumber可执行代码
5. **边界测试**: 自动识别边界条件并生成相应测试用例

---

## Instructions

当用户需要生成测试代码时，你将作为测试专家执行以下流程：

### 触发条件
- 用户说"生成测试"或"创建单元测试"
- 用户说"为这个函数写测试"
- 用户说"E2E测试"或"集成测试"
- 用户提供BDD场景并要求生成可执行测试
- 用户说"提高测试覆盖率"

### 测试生成流程

#### 1. 代码分析
- 识别函数/方法的输入参数类型
- 分析返回值类型和可能的异常
- 识别依赖项（数据库、外部API、文件系统）
- 提取业务逻辑分支（if/else、循环、异常处理）

#### 2. 测试用例设计

**AAA模式** (Arrange-Act-Assert):
```python
def test_example():
    # Arrange: 准备测试数据和环境
    user_data = {"email": "test@example.com"}

    # Act: 执行被测试的操作
    result = create_user(user_data)

    # Assert: 验证结果
    assert result.email == "test@example.com"
```

**测试类型矩阵**:

| 测试类型 | 适用场景 | 工具 | 运行速度 |
|---------|---------|------|---------|
| 单元测试 | 纯函数、业务逻辑 | pytest, jest | 快 (毫秒级) |
| 集成测试 | API端点、数据库操作 | pytest + TestClient, Supertest | 中 (秒级) |
| E2E测试 | 用户流程、UI交互 | Playwright, Cypress | 慢 (分钟级) |
| BDD测试 | 需求验收 | pytest-bdd, Cucumber | 中 (秒级) |
| 性能测试 | 负载、压力测试 | Locust, k6 | 慢 (分钟级) |

#### 3. 边界值测试

自动生成边界值测试：
- **数值**: 最小值、最大值、零、负数、小数
- **字符串**: 空字符串、超长字符串、特殊字符、Unicode
- **列表**: 空列表、单元素、大量元素
- **时间**: 过去、未来、边界时间(午夜、年底)

**示例**:
```python
def test_age_validation_boundary():
    # 正常值
    assert validate_age(18) == True
    assert validate_age(65) == True

    # 边界值
    assert validate_age(17) == False  # 最小值-1
    assert validate_age(18) == True   # 最小值
    assert validate_age(100) == True  # 最大值
    assert validate_age(101) == False # 最大值+1

    # 异常值
    assert validate_age(-1) == False
    assert validate_age(0) == False
```

#### 4. Mock和Fixture

**Pytest Fixtures**:
```python
import pytest
from sqlalchemy import create_engine
from app.database import Base

@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def test_user(test_db):
    """创建测试用户"""
    user = User(email="test@example.com", username="testuser")
    test_db.add(user)
    test_db.commit()
    yield user
    test_db.delete(user)
    test_db.commit()
```

**Mocking外部服务**:
```python
from unittest.mock import Mock, patch

@patch('app.services.email.send_email')
def test_user_registration_sends_email(mock_send_email):
    """测试注册时发送邮件"""
    mock_send_email.return_value = True

    user = register_user("test@example.com", "password")

    mock_send_email.assert_called_once_with(
        to="test@example.com",
        subject="Welcome",
        template="welcome.html"
    )
```

#### 5. 覆盖率分析

生成覆盖率报告：
```bash
# Python
pytest --cov=app --cov-report=html --cov-report=term

# JavaScript/TypeScript
jest --coverage

# 分析输出
Coverage report:
- Line coverage: 87%
- Branch coverage: 82%
- Function coverage: 95%
```

**覆盖率改进建议**:
- 识别未覆盖的代码行
- 建议需要添加的测试用例
- 优先级排序（关键路径优先）

### 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| code | string\|object | 是 | - | 要测试的代码或模块 |
| code_language | string | 是 | - | `python`/`typescript`/`javascript`/`go`/`java` |
| test_type | string | 是 | - | `unit`/`integration`/`e2e`/`bdd`/`all` |
| framework | string | 是 | - | `pytest`/`jest`/`mocha`/`playwright`/`cypress` |
| coverage_target | number | 否 | 80 | 目标覆盖率百分比 (0-100) |
| include_edge_cases | boolean | 否 | true | 是否生成边界值测试 |
| mock_external_services | boolean | 否 | true | 是否Mock外部依赖 |
| bdd_scenarios | string | 否 | - | Gherkin格式的BDD场景 |

### 输出格式

```typescript
interface TestGenerationOutput {
  test_files: Array<{
    path: string;              // 测试文件路径
    content: string;           // 测试代码内容
    test_count: number;        // 测试用例数量
  }>;

  coverage_estimate: {
    line_coverage: number;     // 行覆盖率 (%)
    branch_coverage: number;   // 分支覆盖率 (%)
    function_coverage: number; // 函数覆盖率 (%)
  };

  test_cases: Array<{
    name: string;              // 测试用例名称
    type: string;              // 类型: normal/edge_case/error
    description: string;       // 测试说明
  }>;

  missing_coverage: Array<{
    file: string;
    line: number;
    reason: string;            // 为什么未覆盖
    suggestion: string;        // 建议如何测试
  }>;

  setup_instructions: string[]; // 运行测试的命令
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
interface TestAutomationInput {
}
```

### 输出接口

```typescript
interface TestAutomationOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

## Examples

### 示例 1: 为用户注册功能生成完整测试

**用户输入:**
```
为用户注册API生成完整测试，包括单元测试、集成测试和E2E测试。
代码是Python + FastAPI。
```

**Skill输出:**

```markdown
# 用户注册测试套件

## 项目测试结构

```
tests/
├── conftest.py              # Pytest配置和fixtures
├── unit/
│   ├── test_user_crud.py    # CRUD单元测试
│   └── test_password_hash.py # 密码哈希测试
├── integration/
│   └── test_user_api.py     # API集成测试
└── e2e/
    └── test_user_registration_flow.py # E2E测试
```

## tests/conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User

# 测试数据库
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    """提供数据库会话"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """提供测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """测试用户数据"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!"
    }
```

## tests/unit/test_user_crud.py (单元测试)

```python
import pytest
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from pydantic import ValidationError

class TestUserCRUD:
    """用户CRUD操作单元测试"""

    def test_create_user_success(self, db_session):
        """测试成功创建用户"""
        user_data = UserCreate(
            email="newuser@example.com",
            username="newuser",
            password="SecurePass123!"
        )

        user = create_user(db_session, user_data)

        assert user.email == "newuser@example.com"
        assert user.username == "newuser"
        assert user.is_active is True
        assert user.hashed_password != "SecurePass123!"  # 密码应该被哈希
        assert user.id is not None

    def test_create_user_duplicate_email(self, db_session):
        """测试重复邮箱注册失败"""
        # 第一次创建
        user_data = UserCreate(email="dup@example.com", username="user1", password="Pass123!")
        create_user(db_session, user_data)

        # 第二次用相同邮箱
        user_data2 = UserCreate(email="dup@example.com", username="user2", password="Pass123!")

        with pytest.raises(ValueError, match="Email already registered"):
            create_user(db_session, user_data2)

    def test_create_user_duplicate_username(self, db_session):
        """测试重复用户名注册失败"""
        user_data = UserCreate(email="user1@example.com", username="sameuser", password="Pass123!")
        create_user(db_session, user_data)

        user_data2 = UserCreate(email="user2@example.com", username="sameuser", password="Pass123!")

        with pytest.raises(ValueError, match="Username already taken"):
            create_user(db_session, user_data2)

    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "missing-at-sign.com",
        "@no-local-part.com",
        "no-domain@",
        "spaces in@email.com",
        ""
    ])
    def test_create_user_invalid_email(self, db_session, invalid_email):
        """测试无效邮箱格式被拒绝"""
        with pytest.raises(ValidationError):
            UserCreate(email=invalid_email, username="user", password="Pass123!")

    @pytest.mark.parametrize("weak_password", [
        "123",            # 太短
        "password",       # 无数字无大写
        "PASSWORD",       # 无小写无数字
        "Pass123",        # 太短
        "   ",            # 仅空格
    ])
    def test_create_user_weak_password(self, db_session, weak_password):
        """测试弱密码被拒绝"""
        with pytest.raises(ValidationError, match="Password too weak"):
            UserCreate(email="test@example.com", username="user", password=weak_password)

    def test_create_user_username_length_validation(self, db_session):
        """测试用户名长度验证"""
        # 太短
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", username="ab", password="Pass123!")

        # 太长
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", username="a" * 51, password="Pass123!")

        # 正常长度
        user_data = UserCreate(email="test@example.com", username="validuser", password="Pass123!")
        user = create_user(db_session, user_data)
        assert user.username == "validuser"

    def test_get_user_by_email(self, db_session):
        """测试通过邮箱查询用户"""
        user_data = UserCreate(email="find@example.com", username="findme", password="Pass123!")
        created_user = create_user(db_session, user_data)

        found_user = get_user_by_email(db_session, "find@example.com")

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == "find@example.com"

    def test_get_user_by_email_not_found(self, db_session):
        """测试查询不存在的邮箱返回None"""
        result = get_user_by_email(db_session, "nonexistent@example.com")
        assert result is None
```

## tests/unit/test_password_hash.py

```python
import pytest
from app.core.security import get_password_hash, verify_password

class TestPasswordSecurity:
    """密码安全功能测试"""

    def test_password_hash_is_different_from_original(self):
        """测试密码哈希与原密码不同"""
        password = "MySecurePassword123!"
        hashed = get_password_hash(password)

        assert hashed != password
        assert len(hashed) > len(password)

    def test_same_password_different_hashes(self):
        """测试相同密码生成不同哈希（salt机制）"""
        password = "SamePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2  # 因为salt不同

    def test_verify_correct_password(self):
        """测试验证正确密码"""
        password = "CorrectPassword123!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """测试验证错误密码"""
        password = "CorrectPassword123!"
        hashed = get_password_hash(password)

        assert verify_password("WrongPassword123!", hashed) is False

    def test_verify_case_sensitive(self):
        """测试密码验证区分大小写"""
        password = "CaseSensitive123!"
        hashed = get_password_hash(password)

        assert verify_password("casesensitive123!", hashed) is False
```

## tests/integration/test_user_api.py (集成测试)

```python
import pytest
from fastapi import status

class TestUserRegistrationAPI:
    """用户注册API集成测试"""

    def test_register_endpoint_success(self, client):
        """测试注册端点成功场景"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["is_active"] is True
        assert "id" in data
        assert "hashed_password" not in data  # 不应返回密码

    def test_register_endpoint_duplicate_email(self, client):
        """测试重复邮箱注册返回409"""
        # 第一次注册
        client.post(
            "/api/v1/auth/register",
            json={"email": "dup@example.com", "username": "user1", "password": "Pass123!"}
        )

        # 第二次用相同邮箱
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "dup@example.com", "username": "user2", "password": "Pass123!"}
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already registered" in response.json()["detail"].lower()

    def test_register_endpoint_invalid_data(self, client):
        """测试无效数据返回422"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "u",  # 太短
                "password": "123"  # 太弱
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any(e["loc"] == ["body", "email"] for e in errors)

    def test_register_endpoint_missing_fields(self, client):
        """测试缺少必填字段返回422"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com"}  # 缺少username和password
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_and_login_flow(self, client):
        """测试注册后能立即登录"""
        # 注册
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "logintest@example.com",
                "username": "loginuser",
                "password": "SecurePass123!"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED

        # 登录
        login_response = client.post(
            "/api/v1/auth/login",
            data={  # 注意：OAuth2使用form data
                "username": "logintest@example.com",
                "password": "SecurePass123!"
            }
        )

        assert login_response.status_code == status.HTTP_200_OK
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

    def test_register_rate_limiting(self, client):
        """测试注册接口防暴力破解(限流)"""
        # 连续注册100次
        for i in range(100):
            response = client.post(
                "/api/v1/auth/register",
                json={
                    "email": f"user{i}@example.com",
                    "username": f"user{i}",
                    "password": "Pass123!"
                }
            )

            # 前50个应该成功，后面应该被限流
            if i < 50:
                assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_409_CONFLICT]
            else:
                # 触发限流
                if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    break
```

## tests/e2e/test_user_registration_flow.py (E2E测试)

```python
import pytest
from playwright.sync_api import expect, Page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """配置浏览器上下文"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "zh-CN"
    }

class TestUserRegistrationE2E:
    """用户注册完整流程E2E测试"""

    def test_successful_registration_flow(self, page: Page):
        """测试完整注册流程 - 成功场景"""
        # 1. 访问首页
        page.goto("http://localhost:3000")

        # 2. 点击注册按钮
        page.click("text=注册")
        expect(page).to_have_url("http://localhost:3000/register")

        # 3. 填写注册表单
        page.fill("input[name='email']", "e2euser@example.com")
        page.fill("input[name='username']", "e2euser")
        page.fill("input[name='password']", "SecurePass123!")
        page.fill("input[name='password_confirm']", "SecurePass123!")

        # 4. 勾选同意条款
        page.check("input[type='checkbox'][name='agree_terms']")

        # 5. 提交表单
        page.click("button[type='submit']")

        # 6. 等待并验证成功消息
        success_message = page.locator(".alert-success")
        expect(success_message).to_be_visible()
        expect(success_message).to_contain_text("注册成功")

        # 7. 验证自动跳转到登录页
        expect(page).to_have_url("http://localhost:3000/login", timeout=5000)

        # 8. 验证显示提示信息
        expect(page.locator(".info-message")).to_contain_text("请查收验证邮件")

    def test_registration_validation_errors(self, page: Page):
        """测试表单验证错误提示"""
        page.goto("http://localhost:3000/register")

        # 输入无效邮箱
        page.fill("input[name='email']", "invalid-email")
        page.fill("input[name='username']", "user")
        page.fill("input[name='password']", "123")  # 弱密码
        page.click("button[type='submit']")

        # 验证错误提示
        expect(page.locator(".error[data-field='email']")).to_contain_text("邮箱格式不正确")
        expect(page.locator(".error[data-field='password']")).to_contain_text("密码强度不足")

    def test_password_strength_indicator(self, page: Page):
        """测试密码强度指示器"""
        page.goto("http://localhost:3000/register")

        password_input = page.locator("input[name='password']")
        strength_indicator = page.locator(".password-strength")

        # 弱密码
        password_input.fill("123")
        expect(strength_indicator).to_have_class(/weak/)
        expect(strength_indicator).to_contain_text("弱")

        # 中等密码
        password_input.fill("Pass123")
        expect(strength_indicator).to_have_class(/medium/)
        expect(strength_indicator).to_contain_text("中等")

        # 强密码
        password_input.fill("SecurePass123!")
        expect(strength_indicator).to_have_class(/strong/)
        expect(strength_indicator).to_contain_text("强")

    def test_duplicate_email_error(self, page: Page):
        """测试重复邮箱错误提示"""
        email = f"duplicate-{pytest.timestamp()}@example.com"

        # 第一次注册
        page.goto("http://localhost:3000/register")
        page.fill("input[name='email']", email)
        page.fill("input[name='username']", "user1")
        page.fill("input[name='password']", "SecurePass123!")
        page.fill("input[name='password_confirm']", "SecurePass123!")
        page.check("input[name='agree_terms']")
        page.click("button[type='submit']")
        expect(page).to_have_url("http://localhost:3000/login", timeout=5000)

        # 第二次用相同邮箱注册
        page.goto("http://localhost:3000/register")
        page.fill("input[name='email']", email)
        page.fill("input[name='username']", "user2")
        page.fill("input[name='password']", "SecurePass123!")
        page.fill("input[name='password_confirm']", "SecurePass123!")
        page.check("input[name='agree_terms']")
        page.click("button[type='submit']")

        # 验证错误提示
        expect(page.locator(".alert-error")).to_contain_text("该邮箱已被注册")
```

## 运行测试

### 单元测试
```bash
pytest tests/unit/ -v --cov=app --cov-report=html
```

### 集成测试
```bash
pytest tests/integration/ -v
```

### E2E测试
```bash
# 先启动开发服务器
npm run dev

# 运行Playwright测试
pytest tests/e2e/ --headed
```

### 完整测试套件
```bash
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing
```

## 覆盖率估算

```
预计覆盖率: 89.7%
- 行覆盖率 (Line Coverage): 90%
- 分支覆盖率 (Branch Coverage): 87%
- 函数覆盖率 (Function Coverage): 95%

测试用例统计:
- 单元测试: 18个
- 集成测试: 6个
- E2E测试: 4个
- 总计: 28个测试用例
```

## 缺失覆盖分析

### app/crud/user.py:45-47 (未覆盖)
```python
except DatabaseConnectionError as e:
    logger.error(f"Database connection failed: {e}")
    raise
```

**原因**: 数据库连接异常很难在单元测试中模拟
**建议**: 添加集成测试Mock数据库连接失败

### app/services/email.py:78-82 (未覆盖)
```python
except SMTPException as e:
    logger.warning(f"Email sending failed: {e}")
    # 记录失败但不抛出异常
    return False
```

**原因**: SMTP服务Mock不完整
**建议**: 使用unittest.mock.patch模拟SMTP异常

### app/api/users.py:102 (未覆盖)
```python
if user.is_deleted:
    raise HTTPException(410, "User account deleted")
```

**原因**: 测试数据中没有已删除用户
**建议**: 添加测试用例创建已删除用户并尝试操作
```

---

### 示例 2: BDD测试生成 (从Gherkin到可执行代码)

**用户输入:**
```
将以下Gherkin场景转换为pytest-bdd可执行测试：

Feature: 用户购物车
  Scenario: 添加商品到购物车
    Given 用户已登录
    And 商品"iPhone 15"库存充足
    When 用户将"iPhone 15"添加到购物车
    Then 购物车中有1件商品
    And 购物车总价为5999元
```

**Skill输出:**

```python
# features/shopping_cart.feature (Gherkin)
Feature: 用户购物车
  作为一个登录用户
  我想要将商品添加到购物车
  以便稍后购买

  Scenario: 添加商品到购物车
    Given 用户已登录
    And 商品"iPhone 15"库存充足
    When 用户将"iPhone 15"添加到购物车
    Then 购物车中有1件商品
    And 购物车总价为5999元

  Scenario: 购物车数量增加
    Given 用户已登录
    And 购物车中已有1件"iPhone 15"
    When 用户再次添加"iPhone 15"到购物车
    Then 购物车中有2件"iPhone 15"
    And 购物车总价为11998元

  Scenario: 购物车库存不足
    Given 用户已登录
    And 商品"iPhone 15"仅剩1件
    And 购物车中已有1件"iPhone 15"
    When 用户尝试再次添加"iPhone 15"
    Then 系统提示"库存不足"
    And 购物车数量不变

# tests/bdd/test_shopping_cart.py (pytest-bdd实现)
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app.models import User, Product, CartItem
from app.services.cart import CartService

# 加载feature文件
scenarios('../../features/shopping_cart.feature')

@pytest.fixture
def cart_service(db_session):
    """购物车服务"""
    return CartService(db_session)

@pytest.fixture
def context():
    """测试上下文，存储场景间的状态"""
    return {}

# === Given步骤 ===

@given("用户已登录", target_fixture="logged_in_user")
def user_logged_in(db_session):
    """创建并登录一个测试用户"""
    user = User(email="test@example.com", username="testuser")
    db_session.add(user)
    db_session.commit()
    return user

@given(parsers.parse('商品"{product_name}"库存充足'), target_fixture="product")
def product_in_stock(db_session, product_name):
    """创建库存充足的商品"""
    product = Product(
        name=product_name,
        sku=f"SKU-{product_name}",
        price=5999.00,
        stock=100
    )
    db_session.add(product)
    db_session.commit()
    return product

@given(parsers.parse('购物车中已有{count:d}件"{product_name}"'))
def existing_cart_item(db_session, logged_in_user, product, count, cart_service):
    """预先添加商品到购物车"""
    cart_service.add_to_cart(logged_in_user.id, product.id, count)

@given(parsers.parse('商品"{product_name}"仅剩{count:d}件'))
def product_low_stock(db_session, product_name, count):
    """创建低库存商品"""
    product = Product(
        name=product_name,
        sku=f"SKU-{product_name}",
        price=5999.00,
        stock=count
    )
    db_session.add(product)
    db_session.commit()
    return product

# === When步骤 ===

@when(parsers.parse('用户将"{product_name}"添加到购物车'))
def add_to_cart(logged_in_user, product, cart_service, context):
    """执行添加到购物车操作"""
    try:
        result = cart_service.add_to_cart(logged_in_user.id, product.id, quantity=1)
        context['cart_result'] = result
        context['error'] = None
    except Exception as e:
        context['error'] = str(e)

@when(parsers.parse('用户再次添加"{product_name}"到购物车'))
def add_to_cart_again(logged_in_user, product, cart_service, context):
    """再次添加相同商品"""
    try:
        result = cart_service.add_to_cart(logged_in_user.id, product.id, quantity=1)
        context['cart_result'] = result
        context['error'] = None
    except Exception as e:
        context['error'] = str(e)

@when(parsers.parse('用户尝试再次添加"{product_name}"'))
def try_add_to_cart(logged_in_user, product, cart_service, context):
    """尝试添加（可能失败）"""
    try:
        result = cart_service.add_to_cart(logged_in_user.id, product.id, quantity=1)
        context['cart_result'] = result
        context['error'] = None
    except ValueError as e:
        context['error'] = str(e)

# === Then步骤 ===

@then(parsers.parse('购物车中有{count:d}件商品'))
def verify_cart_count(logged_in_user, cart_service, count):
    """验证购物车商品数量"""
    cart = cart_service.get_cart(logged_in_user.id)
    total_items = sum(item.quantity for item in cart.items)
    assert total_items == count, f"Expected {count} items, got {total_items}"

@then(parsers.parse('购物车总价为{price:d}元'))
def verify_cart_total(logged_in_user, cart_service, price):
    """验证购物车总价"""
    cart = cart_service.get_cart(logged_in_user.id)
    total = cart.calculate_total()
    assert total == price, f"Expected total {price}, got {total}"

@then(parsers.parse('购物车中有{count:d}件"{product_name}"'))
def verify_specific_item_count(logged_in_user, product, cart_service, count):
    """验证特定商品数量"""
    cart = cart_service.get_cart(logged_in_user.id)
    item = next((i for i in cart.items if i.product_id == product.id), None)
    assert item is not None, f"Product {product.name} not in cart"
    assert item.quantity == count, f"Expected {count}, got {item.quantity}"

@then(parsers.parse('系统提示"{message}"'))
def verify_error_message(context, message):
    """验证错误提示"""
    assert context.get('error') is not None, "Expected error but got none"
    assert message in context['error'], f"Expected '{message}' in error, got: {context['error']}"

@then("购物车数量不变")
def verify_cart_unchanged(logged_in_user, cart_service, context):
    """验证购物车未发生变化"""
    # 这个断言依赖于前面存储的状态
    # 实际实现中可能需要在given步骤中保存初始状态
    pass
```

**运行BDD测试**:
```bash
pytest tests/bdd/test_shopping_cart.py -v --gherkin-terminal-reporter
```

**输出示例**:
```
Feature: 用户购物车

  Scenario: 添加商品到购物车
    Given 用户已登录
    And 商品"iPhone 15"库存充足
    When 用户将"iPhone 15"添加到购物车
    Then 购物车中有1件商品
    And 购物车总价为5999元
    ✓ PASSED

  Scenario: 购物车数量增加
    ...
    ✓ PASSED

  Scenario: 购物车库存不足
    ...
    ✓ PASSED

3 scenarios passed, 0 failed
15 steps passed, 0 failed
```

---

## 最佳实践

1. **遵循测试金字塔**
   - 70% 单元测试（快速、独立）
   - 20% 集成测试（覆盖关键路径）
   - 10% E2E测试（验证完整流程）

2. **测试命名清晰**
   - 使用`test_<功能>_<场景>_<预期结果>`格式
   - 例如：`test_create_user_duplicate_email_returns_409`

3. **测试独立性**
   - 每个测试应独立运行，不依赖其他测试
   - 使用fixtures清理测试数据
   - 避免共享可变状态

4. **Mock外部依赖**
   - 数据库：使用内存数据库或事务回滚
   - 外部API：使用Mock/Stub
   - 时间：使用freezegun固定时间

5. **持续维护**
   - 代码变更时同步更新测试
   - 定期审查并删除过时测试
   - 监控测试覆盖率趋势

---

## 相关Skills

- **code-generator** (代码生成): 为生成的代码自动创建测试
- **code-review** (代码审查): 测试代码也需要审查质量
- **debugger-assistant** (调试助手): 测试失败时协助调试
- **quality-gate** (质量门控): 设置覆盖率阈值

---

## 版本历史

- **2.0.0** (2025-12-12): 重构设计，增强BDD支持和E2E测试生成
- **1.0.0** (2025-01-01): 初始版本
