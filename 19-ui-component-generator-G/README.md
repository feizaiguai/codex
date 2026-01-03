# UI Component Generator Skill - UI组件生成器

**版本**: 2.0.0
**类型**: UI/UX设计
**质量等级**: A+

## 📋 功能概述

自动生成生产级前端UI组件代码,支持多框架和完整测试。

### 核心能力

1. **多框架支持** - React/Vue/Angular/Svelte/Web Components全覆盖
2. **原子设计原则** - Atoms/Molecules/Organisms分层设计
3. **无障碍优先** - ARIA属性自动添加,WCAG标准内置
4. **完整测试套件** - Jest/Vitest/Cypress单元+集成+E2E测试
5. **Storybook集成** - 自动生成交互式文档和视觉测试

## 🚀 使用方法

### Slash Command
```bash
/generate-component [组件名] [框架]
```

### 自然语言调用
```
生成一个React按钮组件
创建Vue数据表格组件
```

## 📖 使用示例

### 示例:生成React按钮组件
**输入**:
```
/generate-component Button react --styling=tailwind --tests
```

**输出**:
- ✅ 组件文件:
  - `Button.tsx` (主组件,145行)
  - `Button.module.css` (样式,68行)
  - `Button.test.tsx` (测试,234行)
  - `Button.stories.tsx` (Storybook,89行)
  - `index.ts` (导出,5行)
- ✅ 功能特性:
  - 3种变体: primary/secondary/ghost
  - 4种尺寸: xs/sm/md/lg
  - 5种状态: default/hover/active/disabled/loading
- ✅ 无障碍:
  - ARIA标签完整
  - 键盘导航支持
  - 屏幕阅读器优化
- ✅ 测试覆盖: 98%

## 🎨 支持的框架

### 1. React (函数组件 + Hooks)
```typescript
// Button.tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
      aria-busy={loading}
      aria-disabled={disabled}
    >
      {loading && <span className={styles.spinner} aria-hidden="true" />}
      {children}
    </button>
  );
};
```

### 2. Vue 3 (Composition API)
```vue
<!-- Button.vue -->
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    :aria-busy="loading"
    :aria-disabled="disabled"
    @click="handleClick"
  >
    <span v-if="loading" class="spinner" aria-hidden="true" />
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'xs' | 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
}

const props = withDefaults(defineProps<ButtonProps>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false
});

const emit = defineEmits<{
  click: [];
}>();

const buttonClasses = computed(() => [
  'button',
  `button--${props.variant}`,
  `button--${props.size}`
]);

const handleClick = () => {
  if (!props.disabled && !props.loading) {
    emit('click');
  }
};
</script>
```

### 3. Angular (Standalone Component)
```typescript
// button.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule],
  template: `
    <button
      [class]="buttonClasses"
      [disabled]="disabled || loading"
      [attr.aria-busy]="loading"
      [attr.aria-disabled]="disabled"
      (click)="handleClick()"
    >
      <span *ngIf="loading" class="spinner" aria-hidden="true"></span>
      <ng-content></ng-content>
    </button>
  `,
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent {
  @Input() variant: 'primary' | 'secondary' | 'ghost' = 'primary';
  @Input() size: 'xs' | 'sm' | 'md' | 'lg' = 'md';
  @Input() disabled: boolean = false;
  @Input() loading: boolean = false;
  @Output() clicked = new EventEmitter<void>();

  get buttonClasses(): string {
    return `button button--${this.variant} button--${this.size}`;
  }

  handleClick(): void {
    if (!this.disabled && !this.loading) {
      this.clicked.emit();
    }
  }
}
```

## 🎯 原子设计层级

### Atomic (原子组件)
最小不可分割的UI单元:
- Button (按钮)
- Input (输入框)
- Icon (图标)
- Badge (徽章)
- Avatar (头像)
- Checkbox (复选框)
- Radio (单选框)

### Molecular (分子组件)
多个原子组件组合:
- SearchBar (搜索栏 = Input + Button + Icon)
- Dropdown (下拉菜单 = Button + Menu + Icon)
- Card (卡片 = Image + Text + Button)
- FormField (表单字段 = Label + Input + ErrorText)

### Organism (组织组件)
复杂的UI区块:
- Form (表单 = 多个FormField + Button)
- DataTable (数据表 = Header + Rows + Pagination)
- Modal (弹窗 = Overlay + Card + Buttons)
- Navigation (导航 = Logo + Menu + User)

## 🎨 样式方案

### 1. CSS Modules (推荐)
```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.button.primary {
  background-color: #3b82f6;
  color: white;
}

.button.primary:hover {
  background-color: #2563eb;
}

.button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 2. Tailwind CSS
```typescript
const Button = ({ variant, size, children }) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100'
  };
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}>
      {children}
    </button>
  );
};
```

### 3. Styled Components
```typescript
import styled from 'styled-components';

const StyledButton = styled.button<{ variant: string; size: string }>`
  display: inline-flex;
  align-items: center;
  padding: ${props => props.size === 'sm' ? '0.375rem 0.75rem' : '0.5rem 1rem'};
  background-color: ${props =>
    props.variant === 'primary' ? '#3b82f6' :
    props.variant === 'secondary' ? '#6b7280' : 'transparent'
  };
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    opacity: 0.9;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
```

## ♿ 无障碍功能

### ARIA属性自动添加
```typescript
<button
  role="button"
  aria-label="提交表单"
  aria-busy={loading}
  aria-disabled={disabled}
  aria-pressed={isPressed}
  aria-describedby="button-description"
>
  提交
</button>
```

### 键盘导航
```typescript
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    onClick?.();
  }
};
```

### 焦点管理
```typescript
useEffect(() => {
  if (autoFocus) {
    buttonRef.current?.focus();
  }
}, [autoFocus]);
```

## 🧪 自动测试生成

### 单元测试
```typescript
// Button.test.tsx
describe('Button', () => {
  it('renders with default props', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('handles click events', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('applies disabled state correctly', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows loading spinner', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });
});
```

### 无障碍测试
```typescript
import { axe } from 'jest-axe';

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Accessible</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## 📚 Storybook自动生成

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost']
    },
    size: {
      control: 'select',
      options: ['xs', 'sm', 'md', 'lg']
    }
  }
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
};

export const AllVariants: Story = {
  render: () => (
    <>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </>
  )
};

export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...'
  }
};
```

## 🛠️ 最佳实践

1. **类型安全**: 使用TypeScript确保props类型正确
2. **无障碍优先**: 始终包含ARIA属性和键盘支持
3. **性能优化**: 使用React.memo或Vue shallowRef
4. **测试覆盖**: 目标覆盖率 > 90%
5. **文档完善**: Storybook + JSDoc注释

## 🔗 与其他 Skills 配合

- `theme-designer`: 应用主题系统到组件
- `design-system-manager`: 组件库版本管理
- `accessibility-checker`: 深度无障碍审查

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
