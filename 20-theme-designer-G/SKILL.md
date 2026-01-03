---
name: 20-theme-designer-G
description: Theme designer for creating and managing application theme systems. Supports Light/Dark mode generation, Design Tokens generation (color/font/spacing), multi-format output (CSS Variables/SCSS/Tailwind/CSS-in-JS), WCAG contrast validation, runtime theme switching. Use for theme system design, Design Tokens management, brand consistency.
---

# Theme Designer

**Version**: 2.0.0
**Category**: UI/UX Design
**Priority**: P1
**Last Updated**: 2025-01-15

## Description

The Theme Designer is a comprehensive skill that creates, manages, and switches application theme systems. It supports light/dark modes, brand customization, high-contrast themes, and generates complete design tokens (Design Tokens) in multiple formats. The skill automatically validates accessibility standards, generates color palettes, and provides runtime theme switching capabilities.

### Core Capabilities

1. **Theme System Management**
   - Light/dark mode themes
   - High-contrast mode
   - Brand customization themes
   - Multi-theme coexistence
   - Runtime theme switching

2. **Design Tokens Generation**
   - Color systems (primary, semantic, neutral)
   - Spacing systems (4px/8px grid)
   - Typography systems (fonts, sizes, line-height)
   - Shadow systems
   - Border radius systems
   - Animation systems (duration, easing)

3. **Multi-Format Output**
   - CSS Variables (custom properties)
   - SCSS Variables
   - Tailwind CSS Config
   - Styled Components Theme
   - JSON Design Tokens
   - Platform-specific (iOS/Android)

4. **Dynamic Features**
   - Real-time theme switching
   - Smooth transition animations
   - User preference persistence
   - System theme synchronization
   - Prefers-color-scheme detection

5. **Accessibility Tools**
   - Color palette generation from base color
   - WCAG contrast ratio checking (AA/AAA)
   - High-contrast theme generation
   - Color blindness simulation
   - Theme preview generator

## Instructions

### When to Use

Trigger this skill when you need to:
- Create a new theme system from scratch
- Implement dark mode for an application
- Perform brand visual updates
- Support multiple theme switching
- Standardize design tokens across teams
- Generate accessible color palettes
- Migrate from hard-coded colors to design tokens

### Execution Flow

```mermaid
graph TB
    A[Start: Theme Request] --> B{Input Type}
    B -->|Base Color| C[Generate Color Palette]
    B -->|Full Spec| D[Parse Theme Spec]

    C --> E[Create Color Scales]
    D --> E

    E --> F[Generate Typography Tokens]
    F --> G[Generate Spacing Tokens]
    G --> H[Generate Other Tokens]

    H --> I{Dark Mode?}
    I -->|Yes| J[Generate Dark Variant]
    I -->|No| K[Skip Dark Mode]

    J --> L[Validate Accessibility]
    K --> L

    L --> M{WCAG Compliance}
    M -->|Pass| N[Generate Output Files]
    M -->|Fail| O[Adjust Colors for Contrast]

    O --> L

    N --> P{Output Formats}
    P -->|CSS Variables| Q[Generate CSS]
    P -->|SCSS| R[Generate SCSS]
    P -->|Tailwind| S[Generate Tailwind Config]
    P -->|Styled Components| T[Generate Theme Object]
    P -->|JSON| U[Generate Design Tokens JSON]

    Q --> V[Compile All Formats]
    R --> V
    S --> V
    T --> V
    U --> V

    V --> W{Generate Preview?}
    W -->|Yes| X[Create Preview HTML]
    W -->|No| Y[Skip Preview]

    X --> Z[Package Output]
    Y --> Z

    Z --> AA[Return Theme System]
    AA --> AB[End]
```

### Input Parameters

```typescript
interface ThemeDesignerInput {
  /**
   * Theme metadata
   */
  theme: {
    /** Theme name (e.g., "light", "dark", "brand") */
    name: string;

    /** Theme type */
    type: 'light' | 'dark' | 'high-contrast' | 'custom';

    /** Optional description */
    description?: string;
  };

  /**
   * Base color configuration
   */
  baseColor?: {
    /** Primary brand color (#hex format) */
    primary: string;

    /** Auto-generate color palette */
    generatePalette?: boolean;

    /** Number of color steps (default: 10) */
    paletteSteps?: number;
  };

  /**
   * Color palette configuration
   */
  colors?: {
    /** Semantic colors */
    semantic?: {
      success?: string;
      warning?: string;
      error?: string;
      info?: string;
    };

    /** Neutral colors */
    neutral?: {
      black?: string;
      white?: string;
      grays?: string[];  // Gray scale array
    };

    /** Custom colors */
    custom?: Record<string, string>;
  };

  /**
   * Typography configuration
   */
  typography?: {
    /** Font families */
    fontFamily?: {
      sans?: string;
      serif?: string;
      mono?: string;
    };

    /** Font size settings */
    fontSize?: {
      /** Base font size */
      base?: string;

      /** Type scale ratio (e.g., 1.25 for Major Third) */
      scale?: number;
    };

    /** Line height settings */
    lineHeight?: {
      tight?: number;
      normal?: number;
      relaxed?: number;
    };

    /** Font weights */
    fontWeight?: Record<string, number>;
  };

  /**
   * Spacing configuration
   */
  spacing?: {
    /** Base spacing unit (e.g., 4 or 8) */
    base?: number;

    /** Spacing scale multipliers */
    scale?: number[];
  };

  /**
   * Border configuration
   */
  borders?: {
    /** Border radius values */
    radius?: {
      sm?: string;
      md?: string;
      lg?: string;
      full?: string;
    };

    /** Border widths */
    width?: Record<string, string>;
  };

  /**
   * Shadow configuration
   */
  shadows?: {
    sm?: string;
    md?: string;
    lg?: string;
    xl?: string;
  };

  /**
   * Animation configuration
   */
  animation?: {
    /** Duration values */
    duration?: Record<string, string>;

    /** Easing functions */
    easing?: Record<string, string>;
  };

  /**
   * Output configuration
   */
  output: {
    /** Output formats to generate */
    formats: ('css-variables' | 'scss' | 'tailwind' | 'styled-components' | 'json')[];

    /** Include dark mode variant */
    includeDarkMode?: boolean;

    /** Include accessibility checks */
    includeAccessibility?: boolean;

    /** Generate preview page */
    generatePreview?: boolean;
  };

  /**
   * Accessibility configuration
   */
  accessibility?: {
    /** Enforce WCAG contrast standards */
    enforceContrast?: boolean;

    /** Contrast level (AA or AAA) */
    contrastLevel?: 'AA' | 'AAA';

    /** Generate high-contrast variant */
    generateHighContrast?: boolean;
  };
}
```

### Output Format

```typescript
interface ThemeDesignerOutput {
  /** Whether generation was successful */
  success: boolean;

  /**
   * Generated theme details
   */
  theme: {
    /** Theme name */
    name: string;

    /** Theme type */
    type: string;

    /**
     * Design tokens
     */
    tokens: {
      /** Color tokens */
      colors: {
        /** Primary color scale */
        primary: Record<string, string>;  // { 50: '#...', 100: '#...', ..., 900: '#...' }

        /** Semantic colors */
        semantic: Record<string, string>;

        /** Neutral colors */
        neutral: Record<string, string>;
      };

      /** Typography tokens */
      typography: {
        fontFamily: Record<string, string>;
        fontSize: Record<string, string>;
        lineHeight: Record<string, string>;
        fontWeight: Record<string, number>;
      };

      /** Spacing tokens */
      spacing: Record<string, string>;

      /** Border tokens */
      borders: {
        radius: Record<string, string>;
        width: Record<string, string>;
      };

      /** Shadow tokens */
      shadows: Record<string, string>;

      /** Animation tokens */
      animation: {
        duration: Record<string, string>;
        easing: Record<string, string>;
      };
    };

    /**
     * Generated files
     */
    files: Array<{
      /** Output format */
      format: string;

      /** File path */
      path: string;

      /** File content */
      content: string;
    }>;

    /**
     * Preview information
     */
    preview?: {
      /** Preview page URL */
      url: string;

      /** Components included in preview */
      components: string[];
    };

    /**
     * Accessibility audit results
     */
    accessibility: {
      /** Contrast check results */
      contrastChecks: Array<{
        /** Color combination (e.g., "primary-500 on white") */
        combination: string;

        /** Contrast ratio */
        ratio: number;

        /** WCAG level achieved */
        level: 'AA' | 'AAA' | 'fail';

        /** Whether it passes */
        passes: boolean;
      }>;

      /** Recommendations for improvement */
      recommendations: string[];
    };
  };

  /**
   * Generation metadata
   */
  metadata: {
    /** Generation timestamp */
    generatedAt: string;

    /** Total number of tokens */
    totalTokens: number;

    /** Formats generated */
    formats: string[];
  };
}
```

## Usage Examples

### Example 1: Brand Theme from Single Color

Generate complete light and dark theme systems from a single brand color with full accessibility validation.

#### Input

```typescript
const brandThemeInput: ThemeDesignerInput = {
  theme: {
    name: 'corporate',
    type: 'light',
    description: 'Corporate brand theme with blue primary color'
  },

  baseColor: {
    primary: '#3b82f6',          // Brand blue
    generatePalette: true,
    paletteSteps: 10             // Generate 50, 100, 200, ..., 900
  },

  colors: {
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#06b6d4'
    },
    neutral: {
      black: '#0f172a',
      white: '#ffffff'
      // grays will be auto-generated
    }
  },

  typography: {
    fontFamily: {
      sans: 'Inter, system-ui, -apple-system, sans-serif',
      serif: 'Georgia, serif',
      mono: 'Menlo, Monaco, monospace'
    },
    fontSize: {
      base: '16px',
      scale: 1.25                // Major Third scale
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    }
  },

  spacing: {
    base: 4,                     // 4px base unit
    scale: [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64]
  },

  borders: {
    radius: {
      sm: '0.125rem',
      md: '0.375rem',
      lg: '0.5rem',
      full: '9999px'
    },
    width: {
      thin: '1px',
      medium: '2px',
      thick: '4px'
    }
  },

  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
  },

  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms'
    },
    easing: {
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
  },

  output: {
    formats: ['css-variables', 'scss', 'tailwind', 'json'],
    includeDarkMode: true,
    includeAccessibility: true,
    generatePreview: true
  },

  accessibility: {
    enforceContrast: true,
    contrastLevel: 'AA',
    generateHighContrast: false
  }
};

const result = await themeDesigner.execute(brandThemeInput);
```

#### Output

```css
/* Generated: theme-light.css (150 lines) */

:root {
  /* Primary colors - Auto-generated palette */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;  /* Base color */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;

  /* Semantic colors */
  --color-success: #10b981;
  --color-success-light: #34d399;
  --color-success-dark: #059669;

  --color-warning: #f59e0b;
  --color-warning-light: #fbbf24;
  --color-warning-dark: #d97706;

  --color-error: #ef4444;
  --color-error-light: #f87171;
  --color-error-dark: #dc2626;

  --color-info: #06b6d4;
  --color-info-light: #22d3ee;
  --color-info-dark: #0891b2;

  /* Neutral colors - Auto-generated gray scale */
  --color-neutral-50: #f8fafc;
  --color-neutral-100: #f1f5f9;
  --color-neutral-200: #e2e8f0;
  --color-neutral-300: #cbd5e1;
  --color-neutral-400: #94a3b8;
  --color-neutral-500: #64748b;
  --color-neutral-600: #475569;
  --color-neutral-700: #334155;
  --color-neutral-800: #1e293b;
  --color-neutral-900: #0f172a;

  /* Typography */
  --font-sans: Inter, system-ui, -apple-system, sans-serif;
  --font-serif: Georgia, serif;
  --font-mono: Menlo, Monaco, monospace;

  /* Font sizes - Using Major Third scale (1.25) */
  --font-size-xs: 0.64rem;      /* 10.24px */
  --font-size-sm: 0.8rem;       /* 12.8px */
  --font-size-base: 1rem;       /* 16px */
  --font-size-lg: 1.25rem;      /* 20px */
  --font-size-xl: 1.5625rem;    /* 25px */
  --font-size-2xl: 1.953rem;    /* 31.25px */
  --font-size-3xl: 2.441rem;    /* 39px */

  /* Line heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Font weights */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Spacing - 4px base unit */
  --spacing-0: 0;
  --spacing-1: 0.25rem;         /* 4px */
  --spacing-2: 0.5rem;          /* 8px */
  --spacing-3: 0.75rem;         /* 12px */
  --spacing-4: 1rem;            /* 16px */
  --spacing-5: 1.25rem;         /* 20px */
  --spacing-6: 1.5rem;          /* 24px */
  --spacing-8: 2rem;            /* 32px */
  --spacing-10: 2.5rem;         /* 40px */
  --spacing-12: 3rem;           /* 48px */
  --spacing-16: 4rem;           /* 64px */

  /* Border radius */
  --border-radius-sm: 0.125rem;
  --border-radius-md: 0.375rem;
  --border-radius-lg: 0.5rem;
  --border-radius-full: 9999px;

  /* Border width */
  --border-width-thin: 1px;
  --border-width-medium: 2px;
  --border-width-thick: 4px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  --easing-in: cubic-bezier(0.4, 0, 1, 1);
  --easing-out: cubic-bezier(0, 0, 0.2, 1);
  --easing-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

```css
/* Generated: theme-dark.css (Dark mode overrides) */

[data-theme="dark"] {
  /* Inverted primary colors for dark mode */
  --color-primary-50: #1e3a8a;
  --color-primary-100: #1e40af;
  --color-primary-200: #1d4ed8;
  --color-primary-300: #2563eb;
  --color-primary-400: #3b82f6;
  --color-primary-500: #60a5fa;  /* Lightened for dark backgrounds */
  --color-primary-600: #93c5fd;
  --color-primary-700: #bfdbfe;
  --color-primary-800: #dbeafe;
  --color-primary-900: #eff6ff;

  /* Inverted neutral colors */
  --color-neutral-50: #0f172a;
  --color-neutral-100: #1e293b;
  --color-neutral-200: #334155;
  --color-neutral-300: #475569;
  --color-neutral-400: #64748b;
  --color-neutral-500: #94a3b8;
  --color-neutral-600: #cbd5e1;
  --color-neutral-700: #e2e8f0;
  --color-neutral-800: #f1f5f9;
  --color-neutral-900: #f8fafc;

  /* Adjusted semantic colors for dark mode */
  --color-success: #34d399;
  --color-warning: #fbbf24;
  --color-error: #f87171;
  --color-info: #22d3ee;

  /* Adjusted shadows for dark mode (stronger) */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.6);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.7);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.8);
}
```

```javascript
// Generated: tailwind.config.js

module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a'
        },
        success: {
          DEFAULT: '#10b981',
          light: '#34d399',
          dark: '#059669'
        },
        warning: {
          DEFAULT: '#f59e0b',
          light: '#fbbf24',
          dark: '#d97706'
        },
        error: {
          DEFAULT: '#ef4444',
          light: '#f87171',
          dark: '#dc2626'
        },
        neutral: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['Georgia', 'serif'],
        mono: ['Menlo', 'Monaco', 'monospace']
      },
      fontSize: {
        xs: '0.64rem',
        sm: '0.8rem',
        base: '1rem',
        lg: '1.25rem',
        xl: '1.5625rem',
        '2xl': '1.953rem',
        '3xl': '2.441rem'
      },
      spacing: {
        '0': '0',
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '8': '2rem',
        '10': '2.5rem',
        '12': '3rem',
        '16': '4rem'
      },
      borderRadius: {
        sm: '0.125rem',
        DEFAULT: '0.375rem',
        md: '0.375rem',
        lg: '0.5rem',
        full: '9999px'
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
      }
    }
  },
  darkMode: 'class'
};
```

#### Accessibility Report

```typescript
console.log('♿ Accessibility Checks:\n');

result.theme.accessibility.contrastChecks.forEach(check => {
  const icon = check.passes ? '✓' : '✗';
  const level = check.passes ? `(${check.level})` : '(fail)';
  console.log(`${icon} ${check.combination}: ${check.ratio.toFixed(2)}:1 ${level}`);
});

/*
Output:
♿ Accessibility Checks:

✓ primary-500 on white: 4.51:1 (AA)
✓ primary-600 on white: 6.23:1 (AA)
✓ primary-700 on white: 8.59:1 (AAA)
✗ primary-400 on white: 2.93:1 (fail)
✓ white on primary-600: 6.23:1 (AA)
✓ success on white: 3.37:1 (AA Large Text)
✓ error on white: 4.54:1 (AA)
✓ neutral-700 on white: 8.32:1 (AAA)
*/

// Recommendations
console.log('\n💡 Recommendations:\n');
result.theme.accessibility.recommendations.forEach(rec => {
  console.log(`   - ${rec}`);
});

/*
Output:
💡 Recommendations:

   - Use primary-500 or darker for text on white backgrounds
   - Consider primary-600 for better accessibility (AAA compliant)
   - Avoid using primary-400 for small text (fails WCAG AA)
   - Success color passes for large text (18px+) but consider darker shade for small text
*/
```

#### Result Summary

**Generated Files:**
- ✅ `theme-light.css` (150 lines) - CSS Variables for light mode
- ✅ `theme-dark.css` (80 lines) - Dark mode overrides
- ✅ `theme.scss` (120 lines) - SCSS variables
- ✅ `tailwind.config.js` (90 lines) - Tailwind configuration
- ✅ `design-tokens.json` (200 lines) - Platform-agnostic tokens
- ✅ `preview.html` - Interactive theme preview

**Accessibility:**
- ✅ 87 design tokens generated
- ✅ 23 contrast combinations checked
- ⚠️ 2 warnings (primary-400 for small text)
- ✅ Overall WCAG AA compliant

**Key Metrics:**
- ✅ 10-step color palette
- ✅ 7 font sizes with perfect scale
- ✅ 17 spacing values
- ✅ 4 shadow levels
- ✅ Light + Dark themes

---

### Example 2: Dynamic Theme Switching Implementation

Implement runtime theme switching with smooth transitions and user preference persistence.

#### TypeScript Implementation

```typescript
// Generated: ThemeSwitcher.ts (150 lines)

type Theme = 'light' | 'dark' | 'auto';

class ThemeSwitcher {
  private currentTheme: Theme = 'auto';
  private mediaQuery: MediaQueryList;
  private readonly STORAGE_KEY = 'theme-preference';

  constructor() {
    // Initialize media query for system theme
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // Load saved preference
    const savedTheme = localStorage.getItem(this.STORAGE_KEY) as Theme | null;
    this.currentTheme = savedTheme || 'auto';

    // Listen for system theme changes
    this.mediaQuery.addEventListener('change', this.handleSystemThemeChange.bind(this));

    // Apply initial theme
    this.applyTheme();
  }

  /**
   * Set the theme preference
   */
  setTheme(theme: Theme): void {
    this.currentTheme = theme;
    localStorage.setItem(this.STORAGE_KEY, theme);
    this.applyTheme();

    // Dispatch custom event for components to listen
    window.dispatchEvent(new CustomEvent('theme-change', {
      detail: {
        theme: this.getEffectiveTheme(),
        preference: theme
      }
    }));
  }

  /**
   * Get current theme preference
   */
  getCurrentTheme(): Theme {
    return this.currentTheme;
  }

  /**
   * Get the actual applied theme (resolving 'auto')
   */
  getEffectiveTheme(): 'light' | 'dark' {
    if (this.currentTheme === 'auto') {
      return this.mediaQuery.matches ? 'dark' : 'light';
    }
    return this.currentTheme;
  }

  /**
   * Apply the theme to the document
   */
  private applyTheme(): void {
    const effectiveTheme = this.getEffectiveTheme();

    // Add transition class for smooth switching
    document.documentElement.classList.add('theme-transitioning');

    // Set data-theme attribute
    document.documentElement.setAttribute('data-theme', effectiveTheme);

    // Update meta theme-color for mobile browsers
    this.updateMetaThemeColor(effectiveTheme);

    // Remove transition class after animation
    setTimeout(() => {
      document.documentElement.classList.remove('theme-transitioning');
    }, 300);
  }

  /**
   * Update meta theme-color tag
   */
  private updateMetaThemeColor(theme: 'light' | 'dark'): void {
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    const color = theme === 'dark' ? '#0f172a' : '#ffffff';

    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', color);
    } else {
      const meta = document.createElement('meta');
      meta.name = 'theme-color';
      meta.content = color;
      document.head.appendChild(meta);
    }
  }

  /**
   * Handle system theme changes (when preference is 'auto')
   */
  private handleSystemThemeChange(e: MediaQueryListEvent): void {
    if (this.currentTheme === 'auto') {
      this.applyTheme();
    }
  }

  /**
   * Clean up event listeners
   */
  destroy(): void {
    this.mediaQuery.removeEventListener('change', this.handleSystemThemeChange.bind(this));
  }
}

// Singleton instance
export const themeSwitcher = new ThemeSwitcher();
```

```css
/* Generated: theme-transitions.css (Smooth transitions) */

.theme-transitioning,
.theme-transitioning *,
.theme-transitioning *::before,
.theme-transitioning *::after {
  transition: background-color 300ms ease-in-out,
              color 300ms ease-in-out,
              border-color 300ms ease-in-out,
              box-shadow 300ms ease-in-out !important;
  transition-delay: 0ms !important;
}

/* Prevent flash of unstyled content */
html:not([data-theme]) {
  visibility: hidden;
}

html[data-theme] {
  visibility: visible;
}
```

```tsx
// React Component Example
import React, { useState, useEffect } from 'react';
import { themeSwitcher } from './ThemeSwitcher';

export function ThemeToggle() {
  const [theme, setTheme] = useState(themeSwitcher.getCurrentTheme());
  const [effectiveTheme, setEffectiveTheme] = useState(themeSwitcher.getEffectiveTheme());

  useEffect(() => {
    const handleThemeChange = (e: CustomEvent) => {
      setEffectiveTheme(e.detail.theme);
    };

    window.addEventListener('theme-change', handleThemeChange as EventListener);
    return () => {
      window.removeEventListener('theme-change', handleThemeChange as EventListener);
    };
  }, []);

  const handleChange = (newTheme: 'light' | 'dark' | 'auto') => {
    themeSwitcher.setTheme(newTheme);
    setTheme(newTheme);
  };

  return (
    <div className="theme-toggle flex gap-2 p-2 bg-neutral-100 dark:bg-neutral-800 rounded-lg">
      <button
        onClick={() => handleChange('light')}
        className={`px-4 py-2 rounded transition-colors ${
          theme === 'light'
            ? 'bg-white dark:bg-neutral-700 shadow'
            : 'hover:bg-neutral-200 dark:hover:bg-neutral-700'
        }`}
        aria-label="Light mode"
        aria-pressed={theme === 'light'}
      >
        ☀️ Light
      </button>

      <button
        onClick={() => handleChange('auto')}
        className={`px-4 py-2 rounded transition-colors ${
          theme === 'auto'
            ? 'bg-white dark:bg-neutral-700 shadow'
            : 'hover:bg-neutral-200 dark:hover:bg-neutral-700'
        }`}
        aria-label="Auto mode"
        aria-pressed={theme === 'auto'}
      >
        🌓 Auto
      </button>

      <button
        onClick={() => handleChange('dark')}
        className={`px-4 py-2 rounded transition-colors ${
          theme === 'dark'
            ? 'bg-white dark:bg-neutral-700 shadow'
            : 'hover:bg-neutral-200 dark:hover:bg-neutral-700'
        }`}
        aria-label="Dark mode"
        aria-pressed={theme === 'dark'}
      >
        🌙 Dark
      </button>

      <div className="ml-auto flex items-center text-sm text-neutral-600 dark:text-neutral-400">
        Current: {effectiveTheme}
      </div>
    </div>
  );
}
```

#### Usage

```typescript
// Initialize theme switcher (automatically applied)
import { themeSwitcher } from './ThemeSwitcher';

// Change theme programmatically
themeSwitcher.setTheme('dark');
themeSwitcher.setTheme('light');
themeSwitcher.setTheme('auto');  // Follow system preference

// Get current theme
const current = themeSwitcher.getCurrentTheme();     // 'light' | 'dark' | 'auto'
const effective = themeSwitcher.getEffectiveTheme(); // 'light' | 'dark' (resolved)

// Listen to theme changes
window.addEventListener('theme-change', (e: CustomEvent) => {
  console.log('Theme changed to:', e.detail.theme);
  console.log('User preference:', e.detail.preference);
});
```

---

### Example 3: Multi-Brand Theme System

Create multiple brand themes for white-label products with runtime loading.

#### Input

```typescript
const brands = [
  {
    name: 'Client A',
    primary: '#3b82f6',  // Blue
    logo: '/logos/client-a.svg'
  },
  {
    name: 'Client B',
    primary: '#10b981',  // Green
    logo: '/logos/client-b.svg'
  },
  {
    name: 'Client C',
    primary: '#8b5cf6',  // Purple
    logo: '/logos/client-c.svg'
  }
];

// Generate theme for each brand
const brandThemes = await Promise.all(
  brands.map(brand =>
    themeDesigner.execute({
      theme: {
        name: brand.name.toLowerCase().replace(/\s+/g, '-'),
        type: 'light'
      },
      baseColor: {
        primary: brand.primary,
        generatePalette: true
      },
      output: {
        formats: ['css-variables'],
        includeDarkMode: true
      }
    })
  )
);
```

#### Dynamic Brand Loader

```typescript
// BrandThemeLoader.ts

interface BrandConfig {
  name: string;
  primary: string;
  logo: string;
}

class BrandThemeLoader {
  private currentBrand: string | null = null;
  private readonly brands: Map<string, BrandConfig> = new Map();

  constructor(brands: BrandConfig[]) {
    brands.forEach(brand => {
      const id = brand.name.toLowerCase().replace(/\s+/g, '-');
      this.brands.set(id, brand);
    });
  }

  /**
   * Load a brand's theme
   */
  async loadBrand(brandId: string): Promise<void> {
    const brand = this.brands.get(brandId);

    if (!brand) {
      throw new Error(`Brand "${brandId}" not found`);
    }

    // Create link element for theme CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `/themes/${brandId}/theme.css`;
    link.id = 'brand-theme';

    // Remove old theme
    const oldTheme = document.getElementById('brand-theme');
    if (oldTheme) {
      oldTheme.remove();
    }

    // Add new theme
    document.head.appendChild(link);

    // Wait for CSS to load
    await new Promise<void>((resolve, reject) => {
      link.onload = () => resolve();
      link.onerror = () => reject(new Error(`Failed to load theme for ${brandId}`));
    });

    // Update logo
    const logoElement = document.querySelector('.brand-logo') as HTMLImageElement;
    if (logoElement) {
      logoElement.src = brand.logo;
      logoElement.alt = `${brand.name} logo`;
    }

    // Update document title
    document.title = `${brand.name} - Application`;

    // Store current brand
    this.currentBrand = brandId;
    localStorage.setItem('selected-brand', brandId);

    // Dispatch event
    window.dispatchEvent(new CustomEvent('brand-change', {
      detail: { brandId, brand }
    }));

    console.log(`✅ Loaded theme for brand: ${brand.name}`);
  }

  /**
   * Get current brand
   */
  getCurrentBrand(): string | null {
    return this.currentBrand;
  }

  /**
   * Get brand configuration
   */
  getBrandConfig(brandId: string): BrandConfig | undefined {
    return this.brands.get(brandId);
  }

  /**
   * List all available brands
   */
  listBrands(): BrandConfig[] {
    return Array.from(this.brands.values());
  }
}

// Usage
const loader = new BrandThemeLoader(brands);

// Load brand A
await loader.loadBrand('client-a');  // Blue theme

// Switch to brand B
await loader.loadBrand('client-b');  // Green theme

// Switch to brand C
await loader.loadBrand('client-c');  // Purple theme
```

#### Generated File Structure

```
/themes/
  /client-a/
    theme-light.css      (Blue primary)
    theme-dark.css
    favicon.ico
  /client-b/
    theme-light.css      (Green primary)
    theme-dark.css
    favicon.ico
  /client-c/
    theme-light.css      (Purple primary)
    theme-dark.css
    favicon.ico
```

#### Result Summary

**Generated:**
- ✅ 3 brand themes (6 CSS files total)
- ✅ Each with light + dark mode
- ✅ Dynamic theme loader
- ✅ Runtime brand switching
- ✅ Logo and branding updates
- ✅ LocalStorage persistence

**Features:**
- ✅ Zero page reload switching
- ✅ Automatic logo updates
- ✅ Brand configuration management
- ✅ Event system for theme changes
- ✅ Error handling for missing themes

## Best Practices

### 1. Color System Design

```typescript
// ✅ DO: Use HSL for easier manipulation
const generatePalette = (baseHue: number) => {
  return {
    50: `hsl(${baseHue}, 95%, 95%)`,
    100: `hsl(${baseHue}, 95%, 90%)`,
    // ... auto-generate with consistent saturation and lightness
    900: `hsl(${baseHue}, 80%, 20%)`
  };
};

// ✅ DO: Adjust colors for dark mode (don't just invert)
const darkModeColors = {
  // Lighter for dark backgrounds
  primary: '#60a5fa',  // Instead of #3b82f6
  // Reduce saturation
  success: '#34d399',  // Instead of #10b981
};

// ❌ DON'T: Use random colors without system
const colors = {
  primary: '#3b82f6',
  secondary: '#ff6b6b',  // No relationship to primary
};
```

### 2. Design Token Organization

```typescript
// ✅ DO: Use semantic naming
const tokens = {
  'color-text-primary': 'var(--color-neutral-900)',
  'color-text-secondary': 'var(--color-neutral-600)',
  'color-bg-primary': 'var(--color-white)',
  'color-border': 'var(--color-neutral-200)'
};

// ✅ DO: Layer tokens (primitive → semantic → component)
// Primitive
const primitiveTokens = {
  'color-blue-500': '#3b82f6'
};

// Semantic
const semanticTokens = {
  'color-primary': 'var(--color-blue-500)'
};

// Component
const componentTokens = {
  'button-bg-primary': 'var(--color-primary)'
};
```

### 3. Theme Switching Implementation

```typescript
// ✅ DO: Use CSS variables for runtime switching
:root {
  --color-bg: white;
}

[data-theme="dark"] {
  --color-bg: black;
}

// ✅ DO: Add smooth transitions
.theme-transitioning * {
  transition: background-color 300ms ease, color 300ms ease;
}

// ✅ DO: Save user preference
localStorage.setItem('theme-preference', theme);

// ✅ DO: Respect system preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
```

### 4. Accessibility Standards

```typescript
// ✅ DO: Check WCAG contrast ratios
function checkContrast(foreground: string, background: string): number {
  // Calculate contrast ratio
  const ratio = calculateContrastRatio(foreground, background);

  // WCAG AA: 4.5:1 for normal text, 3:1 for large text
  // WCAG AAA: 7:1 for normal text, 4.5:1 for large text

  return ratio;
}

// ✅ DO: Provide high-contrast alternative
[data-theme="high-contrast"] {
  --color-text: #000000;        // Pure black
  --color-bg: #ffffff;          // Pure white
  --color-border: #000000;      // 21:1 contrast
}

// ✅ DO: Test with color blindness simulators
// Use tools like Stark or accessible-colors npm package
```

## Related Skills

- **ui-component-generator** (Skill 20): Generate components using theme tokens
- **design-system-manager** (Skill 22): Manage theme versions and documentation
- **code-generator** (Skill 01): Generate theme-related utility code

## Changelog

### Version 2.0.0 (2025-01-15)
- Complete redesign with design tokens approach
- Added multi-format output (CSS Variables, SCSS, Tailwind, Styled Components, JSON)
- Enhanced color palette generation with HSL
- Added WCAG contrast checking and recommendations
- Implemented dynamic theme switching utilities
- Added multi-brand theme support
- Improved dark mode color adjustment algorithms

### Version 1.0.0 (2024-06-01)
- Initial release with CSS Variables support
- Basic light/dark mode switching
- Manual color palette d
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
interface ThemeDesignerInput {
}
```

### 输出接口

```typescript
interface ThemeDesignerOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

efinition
