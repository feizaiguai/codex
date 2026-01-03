---
name: 09-accessibility-checker-G
description: Accessibility checker for WCAG 2.1 standard compliance. Supports WCAG A/AA/AAA level checks, keyboard navigation testing, color contrast calculation (WCAG standards), ARIA attribute validation, screen reader compatibility testing. Use for government/public project compliance, accessibility optimization, product accessibility improvement.
---

# accessibility-checker - 无障碍检查专家

**版本**: 2.0.0
**优先级**: P1
**类别**: 质量与安全

---

## 描述

accessibility-checker是专业的无障碍性（可访问性）检查专家，基于WCAG 2.1标准（A/AA/AAA级别）执行全面的可访问性审计。检查键盘导航、屏幕阅读器兼容性、颜色对比度、ARIA属性、语义HTML、表单可访问性等关键方面，确保应用可被所有用户（包括视觉、听觉、运动、认知障碍用户）无障碍使用。为每个违规项提供详细的WCAG引用、影响说明、修复代码和验证方法，帮助团队构建包容性的Web应用。

---

## 核心能力

1. **WCAG合规检查**: 全面检查A/AA/AAA级别标准，涵盖可感知性、可操作性、可理解性、健壮性四大原则
2. **键盘导航测试**: 验证所有交互元素可通过键盘访问，Tab顺序合理，焦点指示清晰
3. **屏幕阅读器兼容**: 检查ARIA属性、alt文本、语义HTML、表单标签
4. **颜色对比度**: 自动计算文本/背景对比度，确保满足4.5:1 (AA) 或 7:1 (AAA)
5. **表单可访问性**: 标签关联、错误提示、必填标记、帮助文本、自动完成提示

---

## Instructions

### WCAG 2.1 四大原则检查

#### 1. 可感知性 (Perceivable)

**1.1 文本替代**
```html
<!-- ❌ 违规：图片缺少alt -->
<img src="logo.png">

<!-- ✅ 修复 -->
<img src="logo.png" alt="Company Logo">

<!-- 装饰性图片 -->
<img src="decorative.png" alt="" role="presentation">
```

**1.4 颜色对比度检查**
```python
def check_contrast_ratio(foreground_hex, background_hex):
    """
    检查颜色对比度是否符合WCAG标准
    AA级别: 4.5:1 (正文), 3:1 (大文本)
    AAA级别: 7:1 (正文), 4.5:1 (大文本)
    """
    # 计算相对亮度
    def get_luminance(hex_color):
        rgb = [int(hex_color[i:i+2], 16)/255 for i in (1, 3, 5)]
        rgb = [(c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4) for c in rgb]
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

    l1 = get_luminance(foreground_hex)
    l2 = get_luminance(background_hex)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    contrast_ratio = (lighter + 0.05) / (darker + 0.05)

    return {
        'ratio': round(contrast_ratio, 2),
        'aa_normal': contrast_ratio >= 4.5,
        'aa_large': contrast_ratio >= 3.0,
        'aaa_normal': contrast_ratio >= 7.0,
        'aaa_large': contrast_ratio >= 4.5
    }

# 示例
result = check_contrast_ratio('#666666', '#FFFFFF')
# {'ratio': 5.74, 'aa_normal': True, 'aaa_normal': False}
```

#### 2. 可操作性 (Operable)

**2.1 键盘可访问**
```html
<!-- ❌ 违规：仅鼠标可点击 -->
<div onclick="handleClick()">Click me</div>

<!-- ✅ 修复：添加键盘支持 -->
<button
  type="button"
  onclick="handleClick()"
  onkeypress="if(event.key==='Enter') handleClick()"
>
  Click me
</button>

<!-- 或使用语义HTML（自动支持键盘） -->
<button type="button" onclick="handleClick()">
  Click me
</button>
```

**2.4 导航辅助**
```html
<!-- 跳转链接 -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- 页面标题 -->
<title>Dashboard - User Profile - MyApp</title>

<!-- 焦点管理 -->
<script>
// 模态框打开时聚焦到标题
function openModal() {
  const modal = document.getElementById('myModal');
  modal.style.display = 'block';
  modal.querySelector('h2').focus();
}
</script>
```

#### 3. 可理解性 (Understandable)

**3.3 输入辅助**
```html
<!-- 表单标签和验证 -->
<form>
  <label for="email">
    Email Address
    <span aria-label="required">*</span>
  </label>
  <input
    type="email"
    id="email"
    name="email"
    required
    aria-required="true"
    aria-describedby="email-error email-help"
    aria-invalid="false"
  >
  <small id="email-help">We'll never share your email</small>
  <div id="email-error" role="alert" style="display:none;"></div>
</form>

<script>
function validateEmail(input) {
  const errorDiv = document.getElementById('email-error');

  if (!input.validity.valid) {
    input.setAttribute('aria-invalid', 'true');
    errorDiv.textContent = 'Please enter a valid email address';
    errorDiv.style.display = 'block';
  } else {
    input.setAttribute('aria-invalid', 'false');
    errorDiv.style.display = 'none';
  }
}
</script>
```

#### 4. 健壮性 (Robust)

**4.1 兼容性**
```html
<!-- ARIA角色和属性 -->
<nav role="navigation" aria-label="Main">
  <ul role="list">
    <li role="listitem">
      <a href="/">Home</a>
    </li>
  </ul>
</nav>

<!-- 自定义组件ARIA -->
<div
  role="button"
  tabindex="0"
  aria-pressed="false"
  onkeypress="if(event.key==='Enter'||event.key===' ') toggle()"
>
  Toggle
</div>
```

---

## 输入参数

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| target | string | 是 | - | HTML文件路径或URL |
| wcag_level | string | 否 | AA | WCAG级别: A/AA/AAA |
| guidelines | string[] | 否 | all | 特定指南: perceivable/operable/understandable/robust |
| browser_testing | boolean | 否 | false | 是否启动浏览器自动化测试 |
| screen_reader_test | boolean | 否 | false | 是否模拟屏幕阅读器 |

---

## 输出格式

```typescript
interface AccessibilityOutput {
  compliance_score: number;           // 0-100合规评分
  wcag_level: 'A' | 'AA' | 'AAA';
  summary: {
    violations_count: number;
    warnings_count: number;
    passed_count: number;
    inapplicable_count: number;
  };
  violations: Violation[];
  warnings: Warning[];
  passed: PassedCheck[];
  recommendations: Recommendation[];
}

interface Violation {
  id: string;
  wcag_criterion: string;             // "1.4.3" (对比度)
  wcag_level: 'A' | 'AA' | 'AAA';
  severity: 'critical' | 'serious' | 'moderate' | 'minor';
  description: string;
  impact: string;                     // 对用户的影响
  elements: Element[];                // 受影响的元素
  fix_recommendation: string;
  code_example: string;               // 修复代码示例
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
interface AccessibilityCheckerInput {{
  // ... 其他字段
}}
```

### 输出接口

```typescript
interface AccessibilityCheckerOutput extends BaseOutput {{
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}}
```

---

## Examples

### 示例：完整无障碍表单检查

**当前HTML**:
```html
<div class="login-form">
  <input type="email" placeholder="Email">
  <input type="password" placeholder="Password">
  <button>Login</button>
</div>
```

**检查报告**:
```markdown
# 无障碍性检查报告

**合规评分**: 35/100 ⚠️ 不合格
**WCAG级别**: AA

## 严重违规 (5个)

### 1. 缺少表单标签 [WCAG 3.3.2 Level A]
**影响**: 屏幕阅读器用户无法理解输入框用途
**修复**:
```html
<label for="email">Email Address</label>
<input type="email" id="email" name="email" aria-required="true">
```

### 2. 颜色对比度不足 [WCAG 1.4.3 Level AA]
**当前**: 占位符 #999 对比度 2.8:1
**要求**: 4.5:1
**修复**: 使用 #666 (对比度 5.7:1)

## 完整修复代码

```html
<form method="post" novalidate aria-labelledby="login-heading">
  <h1 id="login-heading">Login</h1>

  <div role="alert" aria-live="polite" id="form-errors"></div>

  <div>
    <label for="email">
      Email Address
      <span aria-label="required">*</span>
    </label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-help"
      autocomplete="email"
    >
    <small id="email-help">We'll never share your email</small>
  </div>

  <div>
    <label for="password">Password</label>
    <input
      type="password"
      id="password"
      name="password"
      required
      aria-required="true"
      autocomplete="current-password"
    >
  </div>

  <button type="submit">
    Log in to your account
  </button>
</form>
```
```

---

## Best Practices

### 1. 使用语义HTML
```html
<!-- ❌ 避免 -->
<div class="button" onclick="...">Click</div>

<!-- ✅ 推荐 -->
<button type="button" onclick="...">Click</button>
```

### 2. 提供文本替代
- 图片：alt属性
- 图标按钮：aria-label
- 视频：字幕和文字稿

### 3. 确保键盘可访问
- Tab顺序合理
- 焦点可见
- 支持快捷键

### 4. 测试工具
- axe DevTools (浏览器扩展)
- Lighthouse (Chrome)
- NVDA/JAWS (屏幕阅读器)

---

## Related Skills

- `frontend-generator`: 生成可访问的UI组件
- `code-review`: 审查代码可访问性
- `test-automation`: 自动化可访问性测试

---

## Version History

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 2.0.0 | 2025-12-12 | WCAG 2.1完整支持、自动化测试 |
| 1.0.0 | 2025-06-01 | 初始版本 |
