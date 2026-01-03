# Theme Designer Skill - 主题设计器

**版本**: 2.0.0
**类型**: UI/UX设计
**质量等级**: A+

## 📋 功能概述

创建和管理应用主题系统,支持深色模式和Design Tokens。

### 核心能力

1. **Light/Dark模式** - 自动生成深浅两套完整主题
2. **Design Tokens生成** - 颜色/字体/间距/阴影标准化
3. **多格式输出** - CSS Variables/SCSS/Tailwind/CSS-in-JS
4. **WCAG对比度验证** - 自动检查颜色对比度AA/AAA标准
5. **运行时主题切换** - 平滑过渡动画和偏好持久化

## 🚀 使用方法

### Slash Command
```bash
/design-theme [主题名] --mode=[light|dark|both]
```

### 自然语言调用
```
创建一套深色主题
生成主题的Design Tokens
为应用添加主题切换功能
```

## 📖 使用示例

### 示例:创建完整主题系统
**输入**:
```
/design-theme --primary=#3b82f6 --generate-dark --output=css,tailwind
```

**输出**:
- ✅ Light主题:
  - 主色调: #3b82f6 (蓝色)
  - 10级色阶: 50-900
  - 语义色: success/warning/error/info
  - 中性色: 灰度0-100
- ✅ Dark主题:
  - 自动生成深色变体
  - WCAG AAA对比度 ✓
  - 护眼模式优化
- ✅ 生成文件:
  - `theme-light.css` (CSS Variables)
  - `theme-dark.css` (CSS Variables)
  - `tailwind.config.js` (Tailwind配置)
  - `theme-switcher.ts` (切换逻辑)
  - `preview.html` (主题预览)

## 🎨 主题系统结构

### Design Tokens层级
```
Design Tokens
├── Colors (颜色系统)
│   ├── Brand Colors (品牌色)
│   │   ├── primary-50 ~ primary-900
│   │   ├── secondary-50 ~ secondary-900
│   │   └── accent-50 ~ accent-900
│   ├── Semantic Colors (语义色)
│   │   ├── success (成功)
│   │   ├── warning (警告)
│   │   ├── error (错误)
│   │   └── info (信息)
│   └── Neutral Colors (中性色)
│       ├── gray-50 ~ gray-900
│       ├── black
│       └── white
│
├── Typography (字体系统)
│   ├── Font Family (字体族)
│   ├── Font Size (字号)
│   ├── Line Height (行高)
│   └── Font Weight (字重)
│
├── Spacing (间距系统)
│   └── 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64
│
├── Shadow (阴影系统)
│   ├── sm, md, lg, xl, 2xl
│   └── inner, none
│
├── Border Radius (圆角系统)
│   └── none, sm, md, lg, full
│
└── Animation (动画系统)
    ├── Duration (时长)
    └── Easing (缓动)
```

## 🌈 颜色生成算法

### 自动色阶生成
```typescript
// 从单个品牌色生成完整色阶
const primary = '#3b82f6'; // 基准色 (500)

// 自动生成10级色阶:
primary-50:  #eff6ff  (最浅)
primary-100: #dbeafe
primary-200: #bfdbfe
primary-300: #93c5fd
primary-400: #60a5fa
primary-500: #3b82f6  ← 基准色
primary-600: #2563eb
primary-700: #1d4ed8
primary-800: #1e40af
primary-900: #1e3a8a  (最深)
```

### 语义色自动映射
```typescript
// 根据品牌色自动选择合适的语义色
{
  success: '#10b981', // 绿色
  warning: '#f59e0b', // 橙色
  error: '#ef4444',   // 红色
  info: '#3b82f6'     // 蓝色 (使用primary)
}
```

## 🌙 深色模式生成

### 自动深色变体
```css
/* Light Mode */
:root {
  --color-background: #ffffff;
  --color-text: #1f2937;
  --color-primary: #3b82f6;
  --color-border: #e5e7eb;
}

/* Dark Mode (自动生成) */
[data-theme="dark"] {
  --color-background: #111827;
  --color-text: #f9fafb;
  --color-primary: #60a5fa;      /* 提亮20% */
  --color-border: #374151;
}
```

### WCAG对比度验证
```typescript
// 自动验证文字和背景对比度
const results = {
  lightMode: {
    textOnBackground: {
      ratio: 16.2,
      level: 'AAA' // ✅ 超过7:1
    }
  },
  darkMode: {
    textOnBackground: {
      ratio: 14.8,
      level: 'AAA' // ✅ 超过7:1
    }
  }
};
```

## 📦 多格式输出

### 1. CSS Variables
```css
/* theme-light.css */
:root {
  /* Colors */
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;

  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-size-base: 1rem;
  --line-height-normal: 1.5;

  /* Spacing */
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Shadow */
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Border Radius */
  --radius-md: 0.375rem;

  /* Animation */
  --duration-normal: 200ms;
  --easing-ease: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 2. Tailwind Config
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          // ... 500-900
        },
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem'
      }
    }
  }
};
```

### 3. Styled Components Theme
```typescript
// theme.ts
export const lightTheme = {
  colors: {
    primary: '#3b82f6',
    background: '#ffffff',
    text: '#1f2937'
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: {
      base: '1rem',
      lg: '1.125rem'
    }
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem'
  }
};

export const darkTheme = {
  ...lightTheme,
  colors: {
    ...lightTheme.colors,
    background: '#111827',
    text: '#f9fafb'
  }
};
```

### 4. JSON Design Tokens
```json
{
  "color": {
    "primary": {
      "500": { "value": "#3b82f6", "type": "color" },
      "600": { "value": "#2563eb", "type": "color" }
    }
  },
  "typography": {
    "fontFamily": {
      "sans": { "value": "Inter, system-ui, sans-serif", "type": "fontFamily" }
    }
  }
}
```

## 🔄 运行时主题切换

### 基础切换逻辑
```typescript
// theme-switcher.ts
class ThemeManager {
  private currentTheme: 'light' | 'dark' = 'light';

  constructor() {
    // 读取用户偏好
    this.currentTheme = this.getPreferredTheme();
    this.applyTheme(this.currentTheme);
  }

  // 获取用户偏好 (优先级: localStorage > 系统 > 默认)
  getPreferredTheme(): 'light' | 'dark' {
    const stored = localStorage.getItem('theme');
    if (stored) return stored as 'light' | 'dark';

    // 检测系统主题偏好
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }

    return 'light';
  }

  // 应用主题
  applyTheme(theme: 'light' | 'dark') {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    this.currentTheme = theme;
  }

  // 切换主题
  toggle() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.applyTheme(newTheme);
  }

  // 监听系统主题变化
  watchSystemTheme() {
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
          this.applyTheme(e.matches ? 'dark' : 'light');
        }
      });
  }
}

// 使用
const themeManager = new ThemeManager();
themeManager.watchSystemTheme();
```

### 平滑过渡动画
```css
/* 主题切换过渡 */
:root {
  --transition-theme: 200ms ease;
}

* {
  transition:
    background-color var(--transition-theme),
    color var(--transition-theme),
    border-color var(--transition-theme);
}
```

## 🎯 实际案例

### 案例1: 企业品牌主题
```typescript
{
  baseColor: {
    primary: '#0066cc', // 企业蓝
    generatePalette: true
  },
  theme: {
    name: 'corporate',
    type: 'light'
  },
  output: {
    formats: ['css-variables', 'scss'],
    generateDark: true
  }
}

// 输出: 完整的企业主题系统 + 深色模式
```

### 案例2: 高对比度主题 (无障碍)
```typescript
{
  theme: {
    name: 'high-contrast',
    type: 'high-contrast'
  },
  accessibility: {
    minimumContrast: 7.0, // WCAG AAA
    validateAll: true
  }
}

// 所有颜色对比度 >= 7:1
```

### 案例3: 多品牌主题系统
```typescript
{
  themes: [
    { name: 'brand-a', primary: '#3b82f6' },
    { name: 'brand-b', primary: '#10b981' },
    { name: 'brand-c', primary: '#f59e0b' }
  ],
  output: {
    formats: ['css-variables'],
    separateFiles: true // 每个品牌独立文件
  }
}

// 输出: brand-a.css, brand-b.css, brand-c.css
```

## 🛠️ 最佳实践

1. **使用CSS Variables**: 最佳性能和浏览器支持
2. **验证对比度**: 确保文字可读性
3. **系统主题同步**: 尊重用户系统偏好
4. **平滑过渡**: 避免闪烁体验
5. **持久化偏好**: localStorage保存用户选择

## 🔗 与其他 Skills 配合

- `ui-component-generator`: 组件应用主题
- `accessibility-checker`: 深度无障碍验证
- `design-system-manager`: 主题版本管理

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
