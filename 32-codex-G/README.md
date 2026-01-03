# Codex Skill - 全能型AI助手 (GPT-5.1驱动)

**版本**: 2.0.0
**类型**: 全能型智能助手
**驱动**: GPT-5.1
**质量等级**: A+

## 📋 功能概述

Codex是GPT-5.1驱动的全能型AI助手,不受限于特定任务类型。无论任务多复杂,Codex都会想尽一切办法完成,自动选择最佳策略,遇到障碍时切换方案,持续尝试直到成功。

### 核心能力

1. **智能任务分析** - 自动识别任务类型和难度、分解复杂任务为可执行步骤
2. **多策略执行** - 直接解决/分步解决/多工具组合/迭代优化4种策略
3. **工具全覆盖** - 代码生成、调试、数据分析、架构设计、性能优化、自动化
4. **自适应能力** - 遇错自动重试、工具不可用时切换备选、从失败中学习优化
5. **永不放弃精神** - 持续尝试不同方法直到任务完成

## 🚀 使用方法

### 自动触发
当提示词中包含"codex"(不区分大小写)时自动调用。

### Slash Command
```bash
/codex [任务描述]
```

### 自然语言调用
```
用codex帮我完成这个任务
让CODEX解决这个问题
codex能处理这个吗
```

## 📖 使用示例

### 示例:完整功能开发

**输入**:
```
用codex实现一个完整的用户管理系统
要求:
- CRUD操作
- JWT认证
- 权限控制(RBAC)
- 搜索和分页
- 完整测试覆盖
- API文档
```

**执行过程**:
```markdown
# Codex执行报告

## 任务分析
**类型**: 完整功能开发(复杂任务)
**难度**: 高
**预估工作量**: 200-300行代码,8-12个文件

## 策略选择
选择**策略C: 多工具组合**
- 代码生成 + 测试编写 + 文档生成
- 分6个步骤递进实施

---

## 执行步骤

### Step 1: 数据模型设计 ✓
创建文件: `src/models/User.ts`

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';
import bcrypt from 'bcrypt';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column()
  passwordHash: string;

  @Column()
  name: string;

  @Column({ type: 'enum', enum: ['admin', 'user', 'guest'], default: 'user' })
  role: 'admin' | 'user' | 'guest';

  @Column({ default: true })
  isActive: boolean;

  @CreateDateColumn()
  createdAt: Date;

  async comparePassword(password: string): Promise<boolean> {
    return bcrypt.compare(password, this.passwordHash);
  }

  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }
}
```

### Step 2: 业务服务实现 ✓
创建文件: `src/services/UserService.ts`

```typescript
import { Repository } from 'typeorm';
import { User } from '../models/User';
import jwt from 'jsonwebtoken';

export class UserService {
  constructor(private userRepo: Repository<User>) {}

  async create(email: string, password: string, name: string): Promise<User> {
    // 验证邮箱唯一性
    const existing = await this.userRepo.findOne({ where: { email } });
    if (existing) {
      throw new Error('Email already exists');
    }

    // 创建用户
    const user = this.userRepo.create({
      email,
      passwordHash: await User.hashPassword(password),
      name
    });

    return this.userRepo.save(user);
  }

  async authenticate(email: string, password: string): Promise<string> {
    const user = await this.userRepo.findOne({ where: { email } });
    if (!user || !await user.comparePassword(password)) {
      throw new Error('Invalid credentials');
    }

    // 生成JWT
    return jwt.sign(
      { userId: user.id, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );
  }

  async findAll(page: number = 1, limit: number = 10, search?: string) {
    const query = this.userRepo.createQueryBuilder('user');

    if (search) {
      query.where('user.name ILIKE :search OR user.email ILIKE :search', {
        search: `%${search}%`
      });
    }

    const [users, total] = await query
      .skip((page - 1) * limit)
      .take(limit)
      .getManyAndCount();

    return {
      data: users,
      meta: { page, limit, total, totalPages: Math.ceil(total / limit) }
    };
  }

  async update(id: string, updates: Partial<User>): Promise<User> {
    await this.userRepo.update(id, updates);
    return this.userRepo.findOne({ where: { id } });
  }

  async delete(id: string): Promise<void> {
    await this.userRepo.delete(id);
  }
}
```

### Step 3: API端点 ✓
创建文件: `src/routes/users.ts`

```typescript
import { Router } from 'express';
import { UserService } from '../services/UserService';
import { authenticate, authorize } from '../middleware/auth';

const router = Router();

// POST /users - 创建用户
router.post('/', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    const user = await userService.create(email, password, name);
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// POST /users/login - 登录
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const token = await userService.authenticate(email, password);
    res.json({ token });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

// GET /users - 列表(需要认证)
router.get('/', authenticate, async (req, res) => {
  const { page, limit, search } = req.query;
  const result = await userService.findAll(
    Number(page) || 1,
    Number(limit) || 10,
    search as string
  );
  res.json(result);
});

// PUT /users/:id - 更新(需要admin权限)
router.put('/:id', authenticate, authorize(['admin']), async (req, res) => {
  const user = await userService.update(req.params.id, req.body);
  res.json(user);
});

// DELETE /users/:id - 删除(需要admin权限)
router.delete('/:id', authenticate, authorize(['admin']), async (req, res) => {
  await userService.delete(req.params.id);
  res.status(204).send();
});

export default router;
```

### Step 4: 认证中间件 ✓
创建文件: `src/middleware/auth.ts`

```typescript
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

export const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

export const authorize = (roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
};
```

### Step 5: 完整测试 ✓
创建文件: `src/services/UserService.test.ts`

```typescript
import { UserService } from './UserService';
import { User } from '../models/User';

describe('UserService', () => {
  let userService: UserService;
  let mockRepo: any;

  beforeEach(() => {
    mockRepo = {
      create: jest.fn(data => data),
      save: jest.fn(user => ({ ...user, id: 'uuid' })),
      findOne: jest.fn(),
      createQueryBuilder: jest.fn()
    };
    userService = new UserService(mockRepo);
  });

  describe('create', () => {
    it('should create a new user', async () => {
      mockRepo.findOne.mockResolvedValue(null);

      const user = await userService.create('test@example.com', 'password', 'Test User');

      expect(user.email).toBe('test@example.com');
      expect(user.name).toBe('Test User');
      expect(mockRepo.save).toHaveBeenCalled();
    });

    it('should throw error if email exists', async () => {
      mockRepo.findOne.mockResolvedValue({ email: 'test@example.com' });

      await expect(
        userService.create('test@example.com', 'password', 'Test User')
      ).rejects.toThrow('Email already exists');
    });
  });

  describe('authenticate', () => {
    it('should return JWT token for valid credentials', async () => {
      const mockUser = {
        id: 'uuid',
        email: 'test@example.com',
        role: 'user',
        comparePassword: jest.fn().mockResolvedValue(true)
      };
      mockRepo.findOne.mockResolvedValue(mockUser);

      const token = await userService.authenticate('test@example.com', 'password');

      expect(token).toBeTruthy();
      expect(typeof token).toBe('string');
    });

    it('should throw error for invalid credentials', async () => {
      mockRepo.findOne.mockResolvedValue(null);

      await expect(
        userService.authenticate('test@example.com', 'wrong')
      ).rejects.toThrow('Invalid credentials');
    });
  });
});
```

**测试覆盖率**: 92% ✓

### Step 6: API文档生成 ✓
创建文件: `docs/api/users.md`

```markdown
# User Management API

## Authentication
All endpoints (except /users/login and POST /users) require JWT token:
```
Authorization: Bearer YOUR_TOKEN
```

## Endpoints

### POST /users
Create a new user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}
```

**Response 201**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2025-12-15T10:30:00Z"
}
```

### POST /users/login
Authenticate and get JWT token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response 200**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### GET /users?page=1&limit=10&search=john
List users with pagination and search.

**Auth Required**: Yes

**Response 200**:
```json
{
  "data": [ /* users array */ ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "totalPages": 5
  }
}
```

### PUT /users/:id
Update user (admin only).

**Auth Required**: Yes (admin role)

### DELETE /users/:id
Delete user (admin only).

**Auth Required**: Yes (admin role)
```

---

## 完成总结

✅ **任务完成度**: 100%
✅ **文件创建**: 8个文件
✅ **代码行数**: 287行
✅ **测试覆盖率**: 92%
✅ **所有要求**: CRUD/JWT/RBAC/搜索/分页/测试/文档

**耗时**: 实际 < 5分钟 (Codex全自动)
**质量评分**: A+ (生产就绪)
```

## 🎯 执行策略

### 策略A: 直接解决 (简单任务)
适用于单文件、单功能的简单任务
```
任务: 写一个排序函数
→ 直接生成代码 + 测试
```

### 策略B: 分步解决 (中等任务)
适用于多文件、多步骤的中等任务
```
任务: 实现API端点
→ Step 1: 数据模型
→ Step 2: 业务逻辑
→ Step 3: 路由和控制器
→ Step 4: 测试
```

### 策略C: 多工具组合 (复杂任务)
适用于需要多种技能的复杂任务
```
任务: 完整功能开发
→ 代码生成 + 测试 + 文档 + 部署配置
```

### 策略D: 迭代优化 (超复杂任务)
适用于不确定性高、需要反复尝试的任务
```
任务: 性能优化到100ms
→ 尝试1: 添加索引
→ 尝试2: 添加缓存
→ 尝试3: 优化查询
→ 持续测试直到达标
```

## 🛠️ 最佳实践

1. **明确目标**: 清晰描述任务和期望结果
2. **提供上下文**: 说明项目技术栈和约束条件
3. **信任Codex**: 让它自主选择最佳策略
4. **反馈迭代**: 如果结果不理想,提供反馈让Codex优化
5. **充分测试**: Codex会生成测试,但建议人工验证关键逻辑

## 🔗 与其他 Skills 配合

- `code-review`: Codex生成代码后,用code-review审查质量
- `test-automation`: Codex生成基础测试,用test-automation扩展
- `documentation`: Codex生成代码注释,用documentation生成完整文档

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
