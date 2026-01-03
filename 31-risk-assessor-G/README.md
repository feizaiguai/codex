# Risk Assessor Skill - 项目风险评估器

**版本**: 2.0.0
**类型**: 项目管理
**质量等级**: A+

## 📋 功能概述

项目风险识别与评估工具,提供技术债务分析、安全漏洞扫描、依赖健康检查和合规性验证。通过概率-影响矩阵量化风险,生成优先级修复建议和成本估算。

### 核心能力

1. **风险识别** - 代码、架构、依赖、团队风险的多维度扫描
2. **优先级评估** - 概率-影响矩阵、风险评分(0-100)、紧急度排序(P0/P1/P2/P3)
3. **技术债务分析** - Code Smell检测、重构成本估算、SonarQube集成
4. **安全评估** - CVE漏洞扫描、OWASP Top 10检查、依赖审计、合规验证
5. **依赖健康** - 过时依赖检测、许可证冲突、供应链安全、Renovate集成

## 🚀 使用方法

### Slash Command
```bash
/assess-risk [项目名称]
```

### 自然语言调用
```
评估这个项目的技术风险
扫描安全漏洞并优先级排序
分析技术债务并估算重构成本
检查依赖是否有安全问题
GDPR合规性检查
```

## 📖 使用示例

### 示例:项目全面风险评估

**输入**:
```
项目: E-Commerce Backend
范围: 全面评估
技术栈: Node.js, PostgreSQL, Redis
团队: 5人,混合经验
阶段: Production
```

**输出**:
```markdown
# E-Commerce Backend 风险评估报告

**评估日期**: 2025-12-15
**评估范围**: 全面风险评估
**项目阶段**: Production
**关键性**: 🔴 Critical (年营收$5M+)

---

## 📊 风险总览

**整体风险评分**: 58/100 (中等风险)

| 类别 | 评分 | 等级 | 关键问题数 |
|------|------|------|-----------|
| 🔒 安全 | 42/100 | 🔴 高风险 | 3个P0, 8个P1 |
| 💳 技术债务 | 65/100 | 🟡 中等 | 12个Code Smells |
| 📦 依赖健康 | 70/100 | 🟡 中等 | 15个过时依赖 |
| 🏗️ 架构 | 55/100 | 🟡 中等 | 2个单点故障 |
| 👥 团队 | 80/100 | 🟢 低风险 | 1个关键人员依赖 |
| ⚖️ 合规 | 45/100 | 🔴 高风险 | GDPR部分不合规 |

---

## 🔴 P0 紧急风险 (需要立即处理)

### 1. SQL注入漏洞 (安全)

**位置**: `src/services/ProductService.ts:87`

**问题代码**:
```typescript
const query = `SELECT * FROM products WHERE category = '${category}'`;
const result = await db.query(query);
```

**风险评分**: 95/100
- **概率**: 高 (易被攻击)
- **影响**: 严重 (数据库完全暴露)
- **CVSS评分**: 9.8 (Critical)

**攻击场景**:
```bash
# 攻击者输入
category = "electronics' OR '1'='1"

# 实际执行SQL
SELECT * FROM products WHERE category = 'electronics' OR '1'='1'
# 返回所有产品,包括未发布的
```

**修复建议**:
```typescript
// 使用参数化查询
const query = 'SELECT * FROM products WHERE category = $1';
const result = await db.query(query, [category]);

// 或使用ORM
const result = await Product.findAll({ where: { category } });
```

**修复成本**: 2小时 (影响5个文件)
**责任人**: @bob (Backend Lead)
**截止日期**: 2025-12-16 (24小时内)

---

### 2. 过时的OpenSSL依赖 (安全)

**依赖**: `openssl@1.1.1g` (当前版本) → `openssl@3.0.0` (推荐)

**CVE漏洞**:
- CVE-2022-3602: 严重 (CVSS 9.8) - 缓冲区溢出
- CVE-2022-3786: 高 (CVSS 7.5) - DoS攻击

**影响范围**: HTTPS连接、JWT签名验证

**修复建议**:
```bash
# 升级OpenSSL
npm update openssl

# 验证版本
node -p "process.versions.openssl"
```

**破坏性变更**: 无
**修复成本**: 1小时 (测试HTTPS/JWT功能)
**截止日期**: 2025-12-17 (48小时内)

---

### 3. GDPR数据删除权未实现 (合规)

**问题**: 用户删除账号后,订单历史和个人信息未被删除或匿名化

**GDPR条款**: Article 17 (Right to Erasure / "被遗忘权")

**风险**:
- 法律: GDPR罚款最高€20M或年营收4%
- 声誉: 数据泄露事件影响品牌
- 审计: SOC2审计可能失败

**当前实现**:
```typescript
// src/services/UserService.ts:120
async deleteUser(userId: string) {
  await User.destroy({ where: { id: userId } });
  // ❌ 问题: orders表中仍包含user_id和个人信息
}
```

**修复建议**:
```typescript
async deleteUser(userId: string) {
  await db.transaction(async (t) => {
    // 1. 匿名化订单数据
    await Order.update(
      {
        user_email: 'deleted@example.com',
        user_name: 'Deleted User',
        shipping_address: null
      },
      { where: { user_id: userId }, transaction: t }
    );

    // 2. 删除用户敏感数据
    await User.destroy({ where: { id: userId }, transaction: t });

    // 3. 记录删除日志(审计用)
    await AuditLog.create({
      action: 'USER_DELETED',
      user_id: userId,
      timestamp: new Date()
    }, { transaction: t });
  });
}
```

**修复成本**: 8小时 (实现+测试+审查)
**责任人**: @alice (Privacy Lead)
**截止日期**: 2025-12-20 (5天内)

---

## 🟡 P1 高优先级风险 (本月处理)

### 4. 订单服务单点故障 (架构)

**问题**: Order Service只有1个实例,宕机导致整站无法下单

**风险评分**: 75/100
- **概率**: 中 (历史宕机2次/月)
- **影响**: 高 (年营收损失$10K/小时)

**当前架构**:
```
User → API Gateway → Order Service (1 instance) → PostgreSQL
```

**问题**:
- CPU使用率峰值90% (周五晚高峰)
- 内存泄漏导致每周重启1次
- 无负载均衡,无冗余

**修复建议**:
```yaml
# kubernetes部署: 增加副本和健康检查
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3  # 从1 → 3
  template:
    spec:
      containers:
      - name: order-service
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**修复成本**: 16小时 (配置K8s + 负载测试)
**预算**: $300/月 (额外2个实例)
**截止日期**: 2025-12-31

---

### 5-11. 其他P1风险
- [P1-5] 缺少数据库备份策略
- [P1-6] Redis单点故障
- [P1-7] 日志留存不符合GDPR要求(>90天)
- [P1-8] 密码复杂度策略过弱
- [P1-9] API缺少速率限制
- [P1-10] 依赖包含2个高危CVE
- [P1-11] 测试覆盖率不足(68% < 80%目标)

---

## 🟢 P2 中优先级风险 (本季度处理)

### 12. 技术债务: 重复代码 (Code Duplication)

**检测结果**: 47个重复代码块 (>10行)

**示例**:
```typescript
// src/services/OrderService.ts:120
// src/services/InvoiceService.ts:89
// src/services/RefundService.ts:45
// 🔁 重复3次
const tax = subtotal * 0.08;
const shipping = subtotal > 100 ? 0 : 10;
const total = subtotal + tax + shipping;
```

**影响**:
- 维护成本高(修改需要3个地方)
- Bug风险(一处忘记更新)

**重构建议**:
```typescript
// src/utils/pricing.ts
export class PricingCalculator {
  static calculateTotal(subtotal: number, options?: PricingOptions) {
    const tax = subtotal * (options?.taxRate ?? 0.08);
    const shipping = subtotal > (options?.freeShippingThreshold ?? 100) ? 0 : 10;
    return subtotal + tax + shipping;
  }
}
```

**重构成本**: 12小时
**收益**: 减少50行重复代码,提升可维护性

---

## 📊 概率-影响矩阵

```
影响
高 |     [P1-5]           [P0-1]
   |                      [P0-2]
   |     [P1-4]           [P0-3]
   |
中 | [P2-15]  [P2-12]  [P1-8]
   |          [P2-14]  [P1-9]
   |
低 | [P3-20]  [P3-18]  [P2-16]
   |__________|_________|________
     低        中        高
              概率
```

**优先级规则**:
- **P0**: 高影响 + 高概率 → 立即处理
- **P1**: 高影响 或 (中影响+高概率) → 本月处理
- **P2**: 中影响 → 本季度处理
- **P3**: 低影响 → Backlog

---

## 💰 修复成本估算

| 优先级 | 数量 | 总工时 | 成本(@ $80/h) | 预算 |
|--------|------|--------|---------------|------|
| P0 | 3 | 11小时 | $880 | $1,000 |
| P1 | 8 | 64小时 | $5,120 | $6,000 |
| P2 | 12 | 96小时 | $7,680 | $8,000 |
| **总计** | **23** | **171小时** | **$13,680** | **$15,000** |

**建议预算分配**:
- Q1 2026: $7,000 (P0+P1优先)
- Q2 2026: $8,000 (P2)

---

## 📅 行动计划

### 本周 (12/16 - 12/20)
- [ ] [P0-1] 修复SQL注入漏洞 (@bob)
- [ ] [P0-2] 升级OpenSSL依赖 (@david)

### 本月 (12月)
- [ ] [P0-3] 实现GDPR数据删除 (@alice)
- [ ] [P1-4] Order Service高可用 (@david)
- [ ] [P1-5] 配置数据库备份 (@charlie)

### 本季度 (Q1 2026)
- [ ] 处理所有P1风险 (8个)
- [ ] 处理高优先级P2风险 (6个)

---

## 🎯 风险趋势

**与上次评估对比** (30天前):
- ✅ 改善: 测试覆盖率 62% → 68% (+6%)
- ⚠️ 恶化: 安全评分 55 → 42 (-13, 新增CVE)
- ⚠️ 恶化: 过时依赖 8 → 15 (+7)

**建议**:
1. 启用Renovate自动更新依赖
2. 集成Snyk到CI/CD扫描CVE
3. 每月运行一次全面风险评估

---

## 📚 合规检查清单

### GDPR (General Data Protection Regulation)
- [ ] ✅ 数据加密传输 (TLS 1.3)
- [ ] ❌ 数据加密存储 (仅密码加密,其他明文)
- [ ] ❌ 数据删除权 (Right to Erasure)
- [ ] ✅ 数据可携权 (可导出JSON)
- [ ] ⚠️ 数据留存策略 (日志留存>90天,超标)
- [ ] ✅ 同意管理 (Cookie consent)

**合规度**: 60% (需改进)

### SOC2 Type II
- [ ] ✅ 访问控制 (RBAC)
- [ ] ⚠️ 审计日志 (缺少敏感操作日志)
- [ ] ✅ 备份恢复 (每日备份)
- [ ] ❌ 灾难恢复计划 (未文档化)
- [ ] ✅ 安全培训 (年度培训)

**合规度**: 70% (接近达标)

---

**下次评估**: 2026-01-15 (30天后)
**负责人**: @bob (Backend Lead)
**审核人**: @charlie (Security Lead)
```

## 🎯 风险评分方法

### 概率评估
```
低概率 (1-3分): 发生可能性 < 10%
中概率 (4-7分): 发生可能性 10-50%
高概率 (8-10分): 发生可能性 > 50%

示例:
- SQL注入: 9分 (公开代码,易被发现)
- 单点故障: 6分 (历史宕机2次/月)
- 团队离职: 3分 (稳定团队,离职率<10%)
```

### 影响评估
```
低影响 (1-3分): 损失 < $1K 或 < 1小时停机
中影响 (4-7分): 损失 $1K-$50K 或 1-8小时停机
高影响 (8-10分): 损失 > $50K 或 > 8小时停机

示例:
- 数据泄露: 10分 (GDPR罚款 + 声誉损失)
- 订单服务宕机: 8分 ($10K/小时营收损失)
- UI显示bug: 2分 (用户体验略差,无营收影响)
```

### 风险评分
```
风险评分 = (概率 × 影响) × 10

示例:
- SQL注入: (9 × 10) × 10 = 900 / 10 = 90分
- 单点故障: (6 × 8) × 10 = 480 / 10 = 48分
```

## 🛠️ 最佳实践

1. **定期评估**: 每月进行一次风险评估,保持风险可见性
2. **自动化扫描**: 集成Snyk/Dependabot到CI/CD自动检测依赖漏洞
3. **优先级驱动**: 按P0→P1→P2顺序处理,不要被P3分散精力
4. **成本意识**: 评估修复成本vs风险损失,做理性决策
5. **追踪趋势**: 对比历史评估,识别风险增长趋势

## 🔗 与其他 Skills 配合

- `security-audit`: 深度安全审计和渗透测试
- `code-review`: 代码质量和安全审查
- `project-planner`: 将风险修复加入项目计划

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
