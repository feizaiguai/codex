---
name: 19-ui-component-generator-G
description: UI component generator for auto-generating frontend component code. Supports multiple frameworks (React/Vue/Angular/Svelte), atomic design (Atoms/Molecules/Organisms), accessibility-first (auto-add ARIA attributes), complete test suite (Jest/Vitest/Cypress), Storybook integration. Use for component library development, rapid UI prototyping, design system implementation.
---

# UI Component Generator

**Version**: 2.0.0
**Category**: UI/UX Design
**Priority**: P1
**Last Updated**: 2025-01-15

## Description

The UI Component Generator is an advanced skill that automatically generates production-ready frontend UI component code based on design specifications or requirements. It supports multiple frameworks (React, Vue, Angular, Svelte, Web Components), follows atomic design principles, includes comprehensive styling solutions, and generates complete test suites with accessibility standards built-in.

### Core Capabilities

1. **Multi-Framework Support**
   - React (Function Components + Hooks)
   - Vue 3 (Composition API)
   - Angular (Standalone Components)
   - Svelte (Reactive Components)
   - Web Components (Standards-based)

2. **Component Architecture**
   - Atomic components (Button, Input, Icon, Badge)
   - Molecular components (SearchBar, Dropdown, Card)
   - Organism components (Form, DataTable, Modal)
   - Layout components (Grid, Flex, Container)

3. **Styling Solutions**
   - CSS Modules (scoped styles)
   - Styled Components / Emotion (CSS-in-JS)
   - Tailwind CSS (utility-first)
   - SCSS/LESS (preprocessors)
   - Hybrid approaches

4. **Accessibility First**
   - ARIA attributes automatically added
   - Keyboard navigation support
   - Screen reader optimization
   - Color contrast validation (WCAG)
   - Focus management

5. **Comprehensive Testing**
   - Unit tests (Jest/Vitest)
   - Component tests (React Testing Library/Vue Test Utils)
   - Accessibility tests (axe-core)
   - Visual regression tests (Storybook)
   - E2E test examples

## Instructions

### When to Use

Trigger this skill when you need to:
- Rapidly generate UI components for development
- Implement components from design mockups
- Build a design system component library
- Migrate components to a new framework
- Create accessible, production-ready components
- Generate components with complete test coverage

### Execution Flow

```mermaid
graph TB
    A[Start: Component Request] --> B{Design Source}
    B -->|Figma URL| C[Parse Figma Design]
    B -->|Image URL| D[Analyze Design Image]
    B -->|Specification| E[Parse Spec]

    C --> F[Extract Design Tokens]
    D --> F
    E --> F

    F --> G[Generate Component Structure]
    G --> H[Select Framework Template]
    H --> I{Framework?}

    I -->|React| J[Generate React Component]
    I -->|Vue| K[Generate Vue Component]
    I -->|Angular| L[Generate Angular Component]
    I -->|Svelte| M[Generate Svelte Component]
    I -->|Web Component| N[Generate Web Component]

    J --> O[Apply Styling Method]
    K --> O
    L --> O
    M --> O
    N --> O

    O --> P{Include Tests?}
    P -->|Yes| Q[Generate Test Suite]
    P -->|No| R[Skip Tests]

    Q --> S[Generate Storybook Stories]
    R --> S

    S --> T[Validate Accessibility]
    T --> U{A11y Score}

    U -->|< 90| V[Add A11y Fixes]
    U -->|>= 90| W[Generate Documentation]

    V --> W
    W --> X[Package Output Files]
    X --> Y[Return Complete Component]
    Y --> Z[End]
```

### Input Parameters

```typescript
interface UIComponentGeneratorInput {
  /**
   * Component specification
   */
  component: {
    /** Component name (e.g., "Button", "DataTable") */
    name: string;

    /** Component type following atomic design */
    type: 'atomic' | 'molecular' | 'organism' | 'layout';

    /** Functional description of the component */
    description: string;
  };

  /**
   * Target framework configuration
   */
  framework: {
    /** Framework name */
    name: 'react' | 'vue' | 'angular' | 'svelte' | 'web-component';

    /** Framework version (e.g., "18.2", "3.4") */
    version?: string;

    /** Use TypeScript for generated code */
    typescript: boolean;
  };

  /**
   * Styling configuration
   */
  styling: {
    /** Styling method to use */
    method: 'css-modules' | 'styled-components' | 'tailwind' | 'scss' | 'css-in-js';

    /** Theme configuration */
    theme?: {
      /** Color palette */
      colors?: Record<string, string>;

      /** Spacing scale */
      spacing?: Record<string, string>;

      /** Typography settings */
      typography?: {
        fontFamily?: Record<string, string>;
        fontSize?: Record<string, string>;
        lineHeight?: Record<string, number>;
        fontWeight?: Record<string, number>;
      };
    };
  };

  /**
   * Component features and variants
   */
  features: {
    /** Component variants (e.g., ['primary', 'secondary', 'danger']) */
    variants?: string[];

    /** Size options (e.g., ['sm', 'md', 'lg']) */
    sizes?: string[];

    /** State variations (e.g., ['loading', 'disabled', 'error']) */
    states?: string[];

    /** Accessibility features */
    accessibility?: {
      /** Generate ARIA labels */
      ariaLabels?: boolean;

      /** Include keyboard navigation */
      keyboardNav?: boolean;

      /** Optimize for screen readers */
      screenReader?: boolean;
    };
  };

  /**
   * Output configuration
   */
  output: {
    /** Generate test files */
    includeTests?: boolean;

    /** Generate Storybook stories */
    includeStorybook?: boolean;

    /** Generate documentation */
    includeDocs?: boolean;

    /** File organization strategy */
    fileStructure?: 'single' | 'modular';
  };

  /**
   * Design source (optional)
   */
  design?: {
    /** Figma design URL */
    figmaUrl?: string;

    /** Design image URL */
    imageUrl?: string;

    /** Manual specifications */
    specifications?: {
      width?: string;
      height?: string;
      padding?: string;
      borderRadius?: string;
      colors?: Record<string, string>;
    };
  };
}
```

### Output Format

```typescript
interface UIComponentGeneratorOutput {
  /** Whether generation was successful */
  success: boolean;

  /**
   * Generated component details
   */
  component: {
    /** Component name */
    name: string;

    /** Target framework */
    framework: string;

    /**
     * Generated files
     */
    files: {
      /** Main component file */
      component: {
        /** File path */
        path: string;

        /** Component code */
        code: string;
      };

      /** Styles file (if separate) */
      styles?: {
        path: string;
        code: string;
      };

      /** TypeScript types file */
      types?: {
        path: string;
        code: string;
      };

      /** Test file */
      test?: {
        path: string;
        code: string;
      };

      /** Storybook stories file */
      storybook?: {
        path: string;
        code: string;
      };

      /** Documentation file */
      documentation?: {
        path: string;
        content: string;
      };
    };

    /**
     * Component variants information
     */
    variants: Array<{
      /** Variant name */
      name: string;

      /** Props for this variant */
      props: Record<string, any>;

      /** Preview screenshot or code example */
      preview?: string;
    }>;

    /**
     * Accessibility audit results
     */
    accessibility: {
      /** Accessibility score (0-100) */
      score: number;

      /** Accessibility issues found */
      issues: Array<{
        /** Issue severity */
        level: 'error' | 'warning' | 'info';

        /** Issue description */
        message: string;

        /** Suggested fix */
        fix: string;
      }>;
    };

    /**
     * Usage examples
     */
    usage: {
      /** Import statement */
      import: string;

      /** Basic usage example */
      basic: string;

      /** Advanced usage examples */
      advanced: string[];
    };
  };

  /**
   * Generation metadata
   */
  metadata: {
    /** Generation timestamp */
    generatedAt: string;

    /** Total lines of code */
    linesOfCode: number;

    /** Dependencies required */
    dependencies: string[];

    /** Estimated bundle size */
    estimatedSize: string;
  };
}
```

## Usage Examples

### Example 1: Enterprise React Button Component

Generate a production-ready Button component with multiple variants, sizes, states, and complete test coverage.

#### Input

```typescript
const buttonInput: UIComponentGeneratorInput = {
  component: {
    name: 'Button',
    type: 'atomic',
    description: 'A versatile button component with multiple variants, sizes, and states'
  },

  framework: {
    name: 'react',
    version: '18.2',
    typescript: true
  },

  styling: {
    method: 'styled-components',
    theme: {
      colors: {
        primary: '#007bff',
        secondary: '#6c757d',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107'
      },
      spacing: {
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem'
      }
    }
  },

  features: {
    variants: ['primary', 'secondary', 'success', 'danger', 'warning', 'ghost', 'link'],
    sizes: ['sm', 'md', 'lg'],
    states: ['loading', 'disabled'],
    accessibility: {
      ariaLabels: true,
      keyboardNav: true,
      screenReader: true
    }
  },

  output: {
    includeTests: true,
    includeStorybook: true,
    includeDocs: true,
    fileStructure: 'modular'
  }
};

const result = await uiComponentGenerator.execute(buttonInput);
```

#### Output

```typescript
// Generated: src/components/Button/Button.tsx (200 lines)

import React from 'react';
import styled from 'styled-components';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'ghost' | 'link';

  /** Button size */
  size?: 'sm' | 'md' | 'lg';

  /** Loading state */
  loading?: boolean;

  /** Disabled state */
  disabled?: boolean;

  /** Icon before text */
  leftIcon?: React.ReactNode;

  /** Icon after text */
  rightIcon?: React.ReactNode;

  /** Button content */
  children: React.ReactNode;
}

const StyledButton = styled.button<ButtonProps>`
  /* Base styles */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: inherit;
  font-weight: 500;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  position: relative;

  /* Size variants */
  ${props => props.size === 'sm' && `
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    line-height: 1.25rem;
  `}

  ${props => props.size === 'md' && `
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    line-height: 1.5rem;
  `}

  ${props => props.size === 'lg' && `
    padding: 1rem 2rem;
    font-size: 1.125rem;
    line-height: 1.75rem;
  `}

  /* Color variants */
  ${props => {
    const variantStyles = {
      primary: `
        background-color: ${props.theme.colors.primary};
        color: white;
        &:hover:not(:disabled) {
          background-color: #0056b3;
          transform: translateY(-1px);
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        &:active:not(:disabled) {
          transform: translateY(0);
        }
      `,
      secondary: `
        background-color: ${props.theme.colors.secondary};
        color: white;
        &:hover:not(:disabled) {
          background-color: #545b62;
        }
      `,
      success: `
        background-color: ${props.theme.colors.success};
        color: white;
        &:hover:not(:disabled) {
          background-color: #1e7e34;
        }
      `,
      danger: `
        background-color: ${props.theme.colors.danger};
        color: white;
        &:hover:not(:disabled) {
          background-color: #bd2130;
        }
      `,
      warning: `
        background-color: ${props.theme.colors.warning};
        color: #212529;
        &:hover:not(:disabled) {
          background-color: #e0a800;
        }
      `,
      ghost: `
        background-color: transparent;
        color: ${props.theme.colors.primary};
        border: 1px solid ${props.theme.colors.primary};
        &:hover:not(:disabled) {
          background-color: rgba(0, 123, 255, 0.1);
        }
      `,
      link: `
        background-color: transparent;
        color: ${props.theme.colors.primary};
        text-decoration: underline;
        padding: 0;
        &:hover:not(:disabled) {
          color: #0056b3;
        }
      `
    };

    return variantStyles[props.variant || 'primary'];
  }}

  /* Disabled state */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Loading state */
  ${props => props.loading && `
    cursor: wait;
    opacity: 0.7;
  `}

  /* Focus visible for keyboard navigation */
  &:focus-visible {
    outline: 2px solid ${props => props.theme.colors.primary};
    outline-offset: 2px;
  }
`;

const Spinner = styled.span<{ size?: string }>`
  display: inline-block;
  width: ${props => props.size === 'sm' ? '14px' : props.size === 'lg' ? '20px' : '16px'};
  height: ${props => props.size === 'sm' ? '14px' : props.size === 'lg' ? '20px' : '16px'};
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

/**
 * Button component with multiple variants, sizes, and states.
 * Fully accessible with ARIA attributes and keyboard navigation support.
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    variant = 'primary',
    size = 'md',
    loading = false,
    disabled = false,
    leftIcon,
    rightIcon,
    children,
    'aria-label': ariaLabel,
    ...props
  }, ref) => {
    const isDisabled = disabled || loading;

    return (
      <StyledButton
        ref={ref}
        variant={variant}
        size={size}
        loading={loading}
        disabled={isDisabled}
        aria-disabled={isDisabled}
        aria-busy={loading}
        aria-label={ariaLabel || (typeof children === 'string' ? children : undefined)}
        {...props}
      >
        {leftIcon && !loading && leftIcon}
        {loading && <Spinner size={size} aria-hidden="true" />}
        <span>{children}</span>
        {rightIcon && !loading && rightIcon}
      </StyledButton>
    );
  }
);

Button.displayName = 'Button';
```

```typescript
// Generated: src/components/Button/Button.test.tsx (150 lines)

import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import { Button } from './Button';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

const theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107'
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem'
  }
};

const renderWithTheme = (ui: React.ReactElement) => {
  return render(<ThemeProvider theme={theme}>{ui}</ThemeProvider>);
};

describe('Button', () => {
  describe('Rendering', () => {
    it('renders with children', () => {
      renderWithTheme(<Button>Click me</Button>);
      expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
    });

    it('renders with left icon', () => {
      renderWithTheme(
        <Button leftIcon={<span data-testid="left-icon">→</span>}>
          Next
        </Button>
      );
      expect(screen.getByTestId('left-icon')).toBeInTheDocument();
    });

    it('renders with right icon', () => {
      renderWithTheme(
        <Button rightIcon={<span data-testid="right-icon">→</span>}>
          Next
        </Button>
      );
      expect(screen.getByTestId('right-icon')).toBeInTheDocument();
    });
  });

  describe('Variants', () => {
    it('applies primary variant styles', () => {
      renderWithTheme(<Button variant="primary">Primary</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveStyle({ backgroundColor: '#007bff' });
    });

    it('applies danger variant styles', () => {
      renderWithTheme(<Button variant="danger">Delete</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveStyle({ backgroundColor: '#dc3545' });
    });

    it('applies ghost variant styles', () => {
      renderWithTheme(<Button variant="ghost">Ghost</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveStyle({ backgroundColor: 'transparent' });
    });
  });

  describe('Sizes', () => {
    it('applies small size styles', () => {
      renderWithTheme(<Button size="sm">Small</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveStyle({ padding: '0.5rem 1rem', fontSize: '0.875rem' });
    });

    it('applies large size styles', () => {
      renderWithTheme(<Button size="lg">Large</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveStyle({ padding: '1rem 2rem', fontSize: '1.125rem' });
    });
  });

  describe('States', () => {
    it('is disabled when disabled prop is true', () => {
      renderWithTheme(<Button disabled>Disabled</Button>);
      expect(screen.getByRole('button')).toBeDisabled();
    });

    it('is disabled when loading', () => {
      renderWithTheme(<Button loading>Loading</Button>);
      expect(screen.getByRole('button')).toBeDisabled();
      expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
    });

    it('shows spinner when loading', () => {
      renderWithTheme(<Button loading>Loading</Button>);
      const spinner = screen.getByRole('button').querySelector('span[aria-hidden="true"]');
      expect(spinner).toBeInTheDocument();
    });

    it('hides icons when loading', () => {
      renderWithTheme(
        <Button loading leftIcon={<span data-testid="icon">→</span>}>
          Loading
        </Button>
      );
      expect(screen.queryByTestId('icon')).not.toBeInTheDocument();
    });
  });

  describe('Interactions', () => {
    it('handles click events', () => {
      const handleClick = jest.fn();
      renderWithTheme(<Button onClick={handleClick}>Click</Button>);

      fireEvent.click(screen.getByRole('button'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not trigger click when disabled', () => {
      const handleClick = jest.fn();
      renderWithTheme(<Button onClick={handleClick} disabled>Click</Button>);

      fireEvent.click(screen.getByRole('button'));
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('does not trigger click when loading', () => {
      const handleClick = jest.fn();
      renderWithTheme(<Button onClick={handleClick} loading>Click</Button>);

      fireEvent.click(screen.getByRole('button'));
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    it('has correct ARIA attributes', () => {
      renderWithTheme(<Button aria-label="Custom label">Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-label', 'Custom label');
    });

    it('sets aria-disabled when disabled', () => {
      renderWithTheme(<Button disabled>Disabled</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('aria-disabled', 'true');
    });

    it('sets aria-busy when loading', () => {
      renderWithTheme(<Button loading>Loading</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
    });

    it('meets accessibility standards', async () => {
      const { container } = renderWithTheme(<Button>Accessible</Button>);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('is keyboard accessible', () => {
      const handleClick = jest.fn();
      renderWithTheme(<Button onClick={handleClick}>Keyboard</Button>);

      const button = screen.getByRole('button');
      button.focus();
      expect(button).toHaveFocus();

      fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' });
      expect(handleClick).toHaveBeenCalled();
    });
  });

  describe('ForwardRef', () => {
    it('forwards ref to button element', () => {
      const ref = React.createRef<HTMLButtonElement>();
      renderWithTheme(<Button ref={ref}>Ref</Button>);

      expect(ref.current).toBeInstanceOf(HTMLButtonElement);
      expect(ref.current?.tagName).toBe('BUTTON');
    });
  });
});
```

```typescript
// Generated: src/components/Button/Button.stories.tsx (100 lines)

import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Atoms/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants, sizes, and states. Fully accessible with keyboard navigation and screen reader support.'
      }
    }
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'success', 'danger', 'warning', 'ghost', 'link'],
      description: 'Button variant'
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Button size'
    },
    loading: {
      control: 'boolean',
      description: 'Loading state'
    },
    disabled: {
      control: 'boolean',
      description: 'Disabled state'
    }
  }
};

export default meta;
type Story = StoryObj<typeof Button>;

// Basic variants
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button'
  }
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button'
  }
};

export const Success: Story = {
  args: {
    variant: 'success',
    children: 'Success Button'
  }
};

export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Danger Button'
  }
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    children: 'Warning Button'
  }
};

export const Ghost: Story = {
  args: {
    variant: 'ghost',
    children: 'Ghost Button'
  }
};

export const Link: Story = {
  args: {
    variant: 'link',
    children: 'Link Button'
  }
};

// Sizes
export const Small: Story = {
  args: {
    size: 'sm',
    children: 'Small Button'
  }
};

export const Medium: Story = {
  args: {
    size: 'md',
    children: 'Medium Button'
  }
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button'
  }
};

// States
export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...'
  }
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button'
  }
};

// With icons
export const WithLeftIcon: Story = {
  args: {
    leftIcon: <span>←</span>,
    children: 'Back'
  }
};

export const WithRightIcon: Story = {
  args: {
    rightIcon: <span>→</span>,
    children: 'Next'
  }
};

// Interactive examples
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="success">Success</Button>
      <Button variant="danger">Danger</Button>
      <Button variant="warning">Warning</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  )
};

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  )
};
```

#### Result Summary

```typescript
{
  success: true,
  component: {
    name: 'Button',
    framework: 'react',
    files: {
      component: {
        path: 'src/components/Button/Button.tsx',
        code: '... (200 lines)'
      },
      types: {
        path: 'src/components/Button/Button.types.ts',
        code: '... (30 lines)'
      },
      test: {
        path: 'src/components/Button/Button.test.tsx',
        code: '... (150 lines)'
      },
      storybook: {
        path: 'src/components/Button/Button.stories.tsx',
        code: '... (100 lines)'
      },
      documentation: {
        path: 'src/components/Button/README.md',
        content: '... (documentation)'
      }
    },
    variants: [
      { name: 'primary', props: { variant: 'primary' } },
      { name: 'secondary', props: { variant: 'secondary' } },
      { name: 'success', props: { variant: 'success' } },
      { name: 'danger', props: { variant: 'danger' } },
      { name: 'warning', props: { variant: 'warning' } },
      { name: 'ghost', props: { variant: 'ghost' } },
      { name: 'link', props: { variant: 'link' } }
    ],
    accessibility: {
      score: 98,
      issues: [
        {
          level: 'info',
          message: 'Consider adding aria-label for icon-only buttons',
          fix: 'Add aria-label prop when children is only an icon'
        }
      ]
    },
    usage: {
      import: "import { Button } from '@/components/Button';",
      basic: '<Button variant="primary">Click me</Button>',
      advanced: [
        '<Button variant="danger" size="lg" loading>Processing...</Button>',
        '<Button variant="ghost" leftIcon={<Icon />}>With Icon</Button>'
      ]
    }
  },
  metadata: {
    generatedAt: '2025-01-15T10:30:00Z',
    linesOfCode: 480,
    dependencies: ['react', 'styled-components'],
    estimatedSize: '3.2 KB (gzipped)'
  }
}
```

**Key Outputs:**
- ✅ Main component: 200 lines with 7 variants, 3 sizes, 2 states
- ✅ Test suite: 150 lines, 15 tests, 95% coverage
- ✅ Storybook: 20 stories covering all combinations
- ✅ Accessibility score: 98/100
- ✅ Estimated bundle: 3.2 KB gzipped
- ✅ Full TypeScript support
- ✅ Comprehensive documentation

---

### Example 2: Vue 3 Multi-Step Form with Tailwind

Generate a complex multi-step form component using Vue 3 Composition API and Tailwind CSS with data persistence.

#### Input

```typescript
const formInput: UIComponentGeneratorInput = {
  component: {
    name: 'MultiStepForm',
    type: 'organism',
    description: 'A multi-step form with validation, progress tracking, and data persistence'
  },

  framework: {
    name: 'vue',
    version: '3.4',
    typescript: true
  },

  styling: {
    method: 'tailwind'
  },

  features: {
    variants: ['horizontal', 'vertical'],
    states: ['loading', 'error', 'success'],
    accessibility: {
      ariaLabels: true,
      keyboardNav: true,
      screenReader: true
    }
  },

  design: {
    figmaUrl: 'https://www.figma.com/file/abc123/Registration-Form',
    specifications: {
      width: '600px',
      padding: '2rem',
      borderRadius: '0.5rem'
    }
  },

  output: {
    includeTests: true,
    includeStorybook: false,
    includeDocs: true,
    fileStructure: 'modular'
  }
};

const result = await uiComponentGenerator.execute(formInput);
```

#### Output (Key File)

```vue
<!-- Generated: src/components/MultiStepForm/MultiStepForm.vue (280 lines) -->

<template>
  <div class="multi-step-form w-full max-w-2xl mx-auto p-8 bg-white rounded-lg shadow-lg">
    <!-- Progress bar -->
    <div class="mb-8">
      <div class="flex justify-between mb-2">
        <span
          v-for="(step, index) in steps"
          :key="index"
          class="text-sm font-medium transition-colors"
          :class="currentStep >= index ? 'text-blue-600' : 'text-gray-400'"
        >
          {{ step.label }}
        </span>
      </div>

      <div class="w-full bg-gray-200 rounded-full h-2">
        <div
          class="bg-blue-600 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${progressPercentage}%` }"
          role="progressbar"
          :aria-valuenow="progressPercentage"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
    </div>

    <!-- Form content -->
    <form @submit.prevent="handleSubmit" novalidate>
      <transition name="fade" mode="out-in">
        <component
          :is="currentStepComponent"
          v-model="formData[currentStep]"
          :errors="errors[currentStep]"
          @validate="validateStep"
        />
      </transition>

      <!-- Error message -->
      <div
        v-if="globalError"
        class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md"
        role="alert"
      >
        {{ globalError }}
      </div>

      <!-- Navigation buttons -->
      <div class="flex justify-between mt-8">
        <button
          v-if="currentStep > 0"
          type="button"
          @click="previousStep"
          class="px-6 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading"
          :aria-label="`Go to ${steps[currentStep - 1]?.label}`"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            Previous
          </span>
        </button>

        <button
          v-if="currentStep < steps.length - 1"
          type="button"
          @click="nextStep"
          class="ml-auto px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading || !isStepValid"
          :aria-label="`Go to ${steps[currentStep + 1]?.label}`"
        >
          <span class="flex items-center gap-2">
            Next
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </span>
        </button>

        <button
          v-else
          type="submit"
          class="ml-auto px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          :disabled="loading || !isStepValid"
          aria-label="Submit form"
        >
          <svg
            v-if="loading"
            class="animate-spin h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Submitting...' : 'Submit' }}</span>
        </button>
      </div>
    </form>

    <!-- Success message -->
    <transition name="fade">
      <div
        v-if="submitted"
        class="mt-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-md"
        role="status"
        aria-live="polite"
      >
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          Form submitted successfully!
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useFormValidation } from '@/composables/useFormValidation';
import { useLocalStorage } from '@/composables/useLocalStorage';

// Step components (would be separate files)
import PersonalInfoStep from './steps/PersonalInfoStep.vue';
import AddressStep from './steps/AddressStep.vue';
import PaymentStep from './steps/PaymentStep.vue';

interface Props {
  /** Form layout variant */
  variant?: 'horizontal' | 'vertical';

  /** Enable data persistence to localStorage */
  persistData?: boolean;

  /** Storage key for persistence */
  storageKey?: string;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'horizontal',
  persistData: true,
  storageKey: 'multi-step-form'
});

interface Emits {
  /** Emitted when form is submitted */
  (e: 'submit', data: any): void;

  /** Emitted when step changes */
  (e: 'stepChange', step: number): void;

  /** Emitted when form data changes */
  (e: 'update:modelValue', data: any): void;
}

const emit = defineEmits<Emits>();

// State
const currentStep = ref(0);
const loading = ref(false);
const submitted = ref(false);
const globalError = ref('');
const formData = ref<Record<number, any>>({
  0: {},
  1: {},
  2: {}
});
const errors = ref<Record<number, any>>({});

// Steps configuration
const steps = [
  { label: 'Personal Info', component: PersonalInfoStep },
  { label: 'Address', component: AddressStep },
  { label: 'Payment', component: PaymentStep }
];

// Computed
const currentStepComponent = computed(() => steps[currentStep.value].component);
const progressPercentage = computed(() => ((currentStep.value + 1) / steps.length) * 100);
const isStepValid = computed(() => {
  const stepErrors = errors.value[currentStep.value];
  return !stepErrors || Object.keys(stepErrors).length === 0;
});

// Data persistence
onMounted(() => {
  if (props.persistData) {
    const { get } = useLocalStorage(props.storageKey);
    const savedData = get();

    if (savedData) {
      formData.value = savedData.formData || formData.value;
      currentStep.value = savedData.currentStep || 0;
    }
  }
});

watch([formData, currentStep], () => {
  if (props.persistData) {
    const { set } = useLocalStorage(props.storageKey);
    set({
      formData: formData.value,
      currentStep: currentStep.value
    });
  }

  emit('update:modelValue', formData.value);
}, { deep: true });

// Methods
const validateStep = (stepErrors: any) => {
  errors.value[currentStep.value] = stepErrors;
};

const nextStep = () => {
  if (isStepValid.value && currentStep.value < steps.length - 1) {
    currentStep.value++;
    emit('stepChange', currentStep.value);

    // Focus first input in next step
    setTimeout(() => {
      const firstInput = document.querySelector('input, select, textarea') as HTMLElement;
      firstInput?.focus();
    }, 100);
  }
};

const previousStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
    emit('stepChange', currentStep.value);
  }
};

const handleSubmit = async () => {
  if (!isStepValid.value) {
    globalError.value = 'Please fix all errors before submitting';
    return;
  }

  loading.value = true;
  globalError.value = '';

  try {
    // Combine all step data
    const fullData = Object.values(formData.value).reduce(
      (acc, step) => ({ ...acc, ...step }),
      {}
    );

    // Emit submit event
    emit('submit', fullData);

    // Mark as submitted
    submitted.value = true;

    // Clear persisted data after successful submission
    if (props.persistData) {
      const { remove } = useLocalStorage(props.storageKey);
      remove();
    }

    // Reset form after 3 seconds
    setTimeout(() => {
      formData.value = { 0: {}, 1: {}, 2: {} };
      currentStep.value = 0;
      submitted.value = false;
    }, 3000);

  } catch (error) {
    console.error('Form submission error:', error);
    globalError.value = error instanceof Error ? error.message : 'An error occurred';
  } finally {
    loading.value = false;
  }
};

// Keyboard navigation
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    globalError.value = '';
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown);
});

// Expose methods for parent component
defineExpose({
  nextStep,
  previousStep,
  goToStep: (step: number) => {
    if (step >= 0 && step < steps.length) {
      currentStep.value = step;
    }
  },
  reset: () => {
    formData.value = { 0: {}, 1: {}, 2: {} };
    currentStep.value = 0;
    errors.value = {};
    submitted.value = false;
    globalError.value = '';
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Ensure smooth transitions */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
```

#### Result Summary

**Generated Files:**
- ✅ MultiStepForm.vue (280 lines)
- ✅ steps/PersonalInfoStep.vue (80 lines)
- ✅ steps/AddressStep.vue (75 lines)
- ✅ steps/PaymentStep.vue (90 lines)
- ✅ composables/useFormValidation.ts (120 lines)
- ✅ composables/useLocalStorage.ts (60 lines)
- ✅ MultiStepForm.test.ts (120 lines, 18 tests)
- ✅ README.md (documentation)

**Features:**
- ✅ 3-step form with progress indicator
- ✅ Data persistence to localStorage
- ✅ Step validation and navigation
- ✅ Loading and error states
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Accessibility score: 96/100
- ✅ Test coverage: 92%
- ✅ Tailwind CSS styling
- ✅ Full TypeScript support

---

### Example 3: Complete Design System (20 Components)

Generate an entire design system with 20 components, unified theme, and NPM package configuration.

#### Input

```typescript
const designSystemInput = {
  components: [
    // Atomic components
    { name: 'Button', type: 'atomic' },
    { name: 'Input', type: 'atomic' },
    { name: 'Checkbox', type: 'atomic' },
    { name: 'Radio', type: 'atomic' },
    { name: 'Select', type: 'atomic' },
    { name: 'TextArea', type: 'atomic' },
    { name: 'Switch', type: 'atomic' },
    { name: 'Badge', type: 'atomic' },
    { name: 'Avatar', type: 'atomic' },
    { name: 'Icon', type: 'atomic' },

    // Molecular components
    { name: 'Tooltip', type: 'molecular' },
    { name: 'Dropdown', type: 'molecular' },
    { name: 'Modal', type: 'molecular' },
    { name: 'Card', type: 'molecular' },
    { name: 'Alert', type: 'molecular' },
    { name: 'Tabs', type: 'molecular' },
    { name: 'Accordion', type: 'molecular' },
    { name: 'Pagination', type: 'molecular' },
    { name: 'Breadcrumb', type: 'molecular' },
    { name: 'SearchBar', type: 'molecular' }
  ],

  framework: {
    name: 'react',
    version: '18.2',
    typescript: true
  },

  styling: {
    method: 'css-modules',
    theme: {
      colors: {
        primary: '#3b82f6',
        secondary: '#64748b',
        success: '#10b981',
        danger: '#ef4444',
        warning: '#f59e0b',
        info: '#06b6d4'
      },
      spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem'
      },
      typography: {
        fontFamily: {
          sans: 'Inter, system-ui, sans-serif',
          mono: 'Menlo, Monaco, monospace'
        },
        fontSize: {
          xs: '0.75rem',
          sm: '0.875rem',
          base: '1rem',
          lg: '1.125rem',
          xl: '1.25rem'
        }
      }
    }
  },

  output: {
    includeTests: true,
    includeStorybook: true,
    includeDocs: true,
    fileStructure: 'modular',
    bundleConfig: {
      treeshaking: true,
      minification: true,
      generateTypes: true
    }
  }
};

// Batch generate all components
const results = await Promise.all(
  designSystemInput.components.map(component =>
    uiComponentGenerator.execute({
      component: {
        ...component,
        description: `${component.name} component for design system`
      },
      framework: designSystemInput.framework,
      styling: designSystemInput.styling,
      features: {
        variants: ['primary', 'secondary'],
        sizes: ['sm', 'md', 'lg'],
        accessibility: {
          ariaLabels: true,
          keyboardNav: true,
          screenReader: true
        }
      },
      output: designSystemInput.output
    })
  )
);
```

#### Result Summary

```typescript
// Generated package.json
{
  "name": "@mycompany/ui-components",
  "version": "1.0.0",
  "description": "A comprehensive React component library",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsup src/index.ts --dts --format cjs,esm",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  },
  "peerDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "exports": {
    ".": "./dist/index.js",
    "./Button": "./dist/Button/index.js",
    "./Input": "./dist/Input/index.js",
    "./Card": "./dist/Card/index.js"
    // ... other components
  },
  "sideEffects": ["**/*.css"]
}

// Summary statistics
const summary = {
  totalComponents: 20,
  totalFiles: 120,  // 20 components × 6 files each
  totalTests: 20,   // One test suite per component
  totalStories: 60, // ~3 stories per component
  averageAccessibilityScore: 97.2,
  totalLinesOfCode: 12450,
  estimatedBundleSize: 45.3  // KB (gzipped)
};

console.log('📦 Design System Generation Complete!');
console.log(`✅ ${summary.totalComponents} components generated`);
console.log(`📁 ${summary.totalFiles} files created`);
console.log(`🧪 ${summary.totalTests} test suites`);
console.log(`📚 ${summary.totalStories} Storybook stories`);
console.log(`♿ Average accessibility: ${summary.averageAccessibilityScore}/100`);
console.log(`📊 Total code: ${summary.totalLinesOfCode.toLocaleString()} lines`);
console.log(`📦 Estimated bundle: ${summary.estimatedBundleSize} KB (gzipped)`);
```

**Generated Structure:**
```
@mycompany/ui-components/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.module.css
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   ├── Button.types.ts
│   │   │   └── index.ts
│   │   ├── Input/
│   │   │   └── ... (same structure)
│   │   └── ... (18 more components)
│   ├── theme/
│   │   ├── colors.ts
│   │   ├── spacing.ts
│   │   └── typography.ts
│   └── index.ts
├── dist/ (built files)
├── .storybook/
│   ├── main.ts
│   └── preview.ts
├── package.json
├── README.md
├── CHANGELOG.md
└── tsconfig.json
```

**Key Results:**
- ✅ 20 production-ready components
- ✅ 120 files total
- ✅ 97.2 average accessibility score
- ✅ Full TypeScript support
- ✅ Tree-shakeable bundle
- ✅ Comprehensive Storybook
- ✅ NPM package ready
- ✅ 12,450 lines of quality code

## Best Practices

### 1. Component Design Principles

```typescript
// ✅ DO: Single Responsibility
const Button = ({ onClick, children }) => (
  <button onClick={onClick}>{children}</button>
);

// ❌ DON'T: Multiple Responsibilities
const ButtonWithForm = ({ onSubmit, children }) => (
  <form onSubmit={onSubmit}>
    <button>{children}</button>
  </form>
);
```

```typescript
// ✅ DO: Composition over Inheritance
const IconButton = ({ icon, ...props }) => (
  <Button {...props}>
    <Icon name={icon} />
  </Button>
);

// ❌ DON'T: Deep Inheritance
class IconButton extends Button extends BaseButton { }
```

```typescript
// ✅ DO: Provide Sensible Defaults
interface ButtonProps {
  variant?: 'primary' | 'secondary';  // Default will be 'primary'
  size?: 'sm' | 'md' | 'lg';          // Default will be 'md'
}

const Button = ({ variant = 'primary', size = 'md' }) => { };
```

### 2. Accessibility First

```typescript
// ✅ DO: Include ARIA attributes
<button
  aria-label="Close dialog"
  aria-pressed={isPressed}
  aria-disabled={isDisabled}
>
  Close
</button>

// ✅ DO: Support keyboard navigation
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    onClick();
  }
};

// ✅ DO: Manage focus
useEffect(() => {
  if (isOpen) {
    firstInputRef.current?.focus();
  }
}, [isOpen]);

// ✅ DO: Ensure color contrast
// Use WCAG AA standard (4.5:1 for normal text, 3:1 for large text)
const colors = {
  text: '#000000',     // 21:1 on white
  textSecondary: '#666666'  // 5.74:1 on white
};
```

### 3. Performance Optimization

```typescript
// ✅ DO: Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  // Expensive rendering logic
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.data.id === nextProps.data.id;
});

// ✅ DO: Implement code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Spinner />}>
  <HeavyComponent />
</Suspense>

// ✅ DO: Optimize bundle size
// Use tree-shaking friendly exports
export { Button } from './Button';
export { Input } from './Input';

// ❌ DON'T: Export everything as default
export default { Button, Input, ... };
```

### 4. Testing Strategy

```typescript
// ✅ DO: Test user interactions
it('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click</Button>);

  fireEvent.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

// ✅ DO: Test accessibility
it('meets accessibility standards', async () => {
  const { container } = render(<Button>Accessible</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// ✅ DO: Test all variants
describe.each([
  ['primary', '#007bff'],
  ['danger', '#dc3545'],
  ['success', '#28a745']
])('variant %s', (variant, color) => {
  it(`applies ${variant} styles`, () => {
    render(<Button variant={variant}>Test</Button>);
    expect(screen.getByRole('button')).toHaveStyle({
      backgroundColor: color
    });
  });
});
```

### 5. Documentation Standards

```typescript
/**
 * Button component for user interactions.
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="lg" onClick={handleClick}>
 *   Click Me
 * </Button>
 * ```
 *
 * @param {ButtonProps} props - Component props
 * @returns {JSX.Element} Rendered button element
 */
export const Button: React.FC<ButtonProps> = ({ ... }) => { };
```

## Related Skills

- **theme-designer** (Skill 21): Generate design tokens and themes for components
- **design-system-manager** (Skill 22): Manage component library versions and documentation
- **code-generator** (Skill 01): Base code generation capabilities
- **test-generator** (Skill 04): Generate additional test scenarios

## Changelog

### Version 2.0.0 (2025-01-15)
- Complete redesign with atomic design principles
- Added multi-framework support (React, Vue, Angular, Svelte, Web Components)
- Enhanced accessibility features with WCAG compliance
- Integrated Storybook generation
- Added comprehensive test generation
- Improved styling method flexibility
- Added Figma design integration

### Version 1.0.0 (2024-06-01)
- Initial release with React support
- Basic component generation
- CSS Modules sty
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
interface UIComponentGeneratorInput {

  testing?: {
    enabled: boolean;
    framework: 'vitest' | 'jest' | 'testing-library' | 'cypress';
    coverage: {
      minCoverage: number;
      includeA11y: boolean;
      includeVisualRegression?: boolean;
    };
    testTypes: {
      unit: boolean;
      integration?: boolean;
      e2e?: boolean;
    };
  };
}
```

### 输出接口

```typescript
interface UIComponentGeneratorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段

  testFiles: Array<{
    path: string;
    content: string;
    framework: string;
    testType: 'unit' | 'integration' | 'e2e';
    coverageEstimate: number;
    a11yChecks: string[];
  }>;

  testSummary: {
    totalTests: number;
    unitTests: number;
    integrationTests: number;
    e2eTests: number;
    estimatedCoverage: number;
  };
}
```

---

ling only
