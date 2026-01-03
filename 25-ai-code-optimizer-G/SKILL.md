---
name: 25-ai-code-optimizer-G
description: AI code optimizer for performance analysis and optimization suggestions. Supports time complexity analysis (Big-O), algorithm optimization suggestions (O(n²)→O(n log n)), memory leak detection (heap analysis), bundle size optimization (Tree Shaking/Code Splitting), AI-driven refactoring (pattern recognition). Use for performance optimization, algorithm improvement, code refactoring.
---

# AI Code Optimizer

**Version**: 2.0.0
**Category**: AI Enhancement
**Priority**: P1 (Core Capability)
**Last Updated**: 2025-01-12

---

## Description

The AI Code Optimizer is an intelligent performance analysis and optimization tool that leverages AI to automatically detect performance bottlenecks, suggest algorithmic improvements, identify memory leaks, and optimize bundle sizes. It provides actionable refactoring recommendations backed by complexity analysis, best practices, and measurable performance impact predictions.

**Core Capabilities**:

- **Performance Analysis**: Automatic time complexity analysis (Big O notation), space complexity optimization, hot path identification with execution profiling, runtime performance prediction
- **Algorithm Optimization**: Detect O(n²) → O(n log n) improvement opportunities, optimal data structure recommendations, parallel processing suggestions, recursive → iterative conversions
- **Memory Optimization**: Memory leak detection with heap profiling, object pooling recommendations, lazy loading strategies, garbage collection pressure analysis
- **Bundle Size Optimization**: Tree shaking opportunities, code splitting strategies, dynamic import suggestions, unused code detection, dependency weight analysis
- **Database Query Optimization**: N+1 query problem detection, index recommendations, query plan analysis, ORM performance anti-patterns
- **AI-Powered Refactoring**: Pattern-based code smell detection, automated refactoring suggestions with before/after comparisons, best practice citations with links to documentation

---

## Instructions

### When to Activate

This skill should activate when users:

1. Request **"optimize code performance"**, **"improve algorithm efficiency"**, **"reduce memory usage"**, **"make this faster"**
2. Mention **"code is slow"**, **"bundle size too large"**, **"memory leak"**, **"performance bottleneck"**, **"high CPU usage"**
3. Need **"performance analysis"**, **"profiling results explanation"**, **"optimization recommendations"**, **"complexity analysis"**
4. Ask **"how to speed this up"**, **"reduce bundle size"**, **"fix performance issues"**, **"optimize database queries"**
5. Require **"code review for performance"**, **"refactoring suggestions"**, **"best practices for optimization"**

### Execution Flow

```mermaid
flowchart TD
    Start([User Requests Code Optimization]) --> ParseCode[Parse Code & Dependencies]
    ParseCode --> AnalyzeType{Analysis Type}

    AnalyzeType --> PerfAnalysis[Performance Analysis]
    AnalyzeType --> MemoryAnalysis[Memory Analysis]
    AnalyzeType --> BundleAnalysis[Bundle Analysis]
    AnalyzeType --> DBAnalysis[Database Analysis]

    PerfAnalysis --> Complexity[Calculate Time Complexity]
    Complexity --> HotPath[Identify Hot Paths]
    HotPath --> AlgoCheck[Check Algorithm Efficiency]

    MemoryAnalysis --> HeapProfile[Analyze Heap Usage]
    HeapProfile --> LeakDetect[Detect Memory Leaks]
    LeakDetect --> GCPressure[Analyze GC Pressure]

    BundleAnalysis --> DependencyGraph[Build Dependency Graph]
    DependencyGraph --> TreeShake[Identify Tree Shaking Opportunities]
    TreeShake --> CodeSplit[Suggest Code Splitting]

    DBAnalysis --> QueryAnalysis[Analyze Query Patterns]
    QueryAnalysis --> N1Detect[Detect N+1 Queries]
    N1Detect --> IndexCheck[Check Missing Indexes]

    AlgoCheck --> AIPatternMatch[AI Pattern Matching]
    GCPressure --> AIPatternMatch
    CodeSplit --> AIPatternMatch
    IndexCheck --> AIPatternMatch

    AIPatternMatch --> BestPractices[Match Against Best Practices]
    BestPractices --> GenerateOptimizations[Generate Optimization Suggestions]

    GenerateOptimizations --> CalculateImpact[Calculate Performance Impact]
    CalculateImpact --> PrioritizeIssues[Prioritize by Impact & Effort]

    PrioritizeIssues --> GenerateCode[Generate Optimized Code]
    GenerateCode --> CompareBeforeAfter[Before/After Comparison]
    CompareBeforeAfter --> ValidateOptimization[Validate Optimizations]

    ValidateOptimization --> OutputReport[Generate Optimization Report]
    OutputReport --> End([Return Recommendations])
```

---

## Input/Output Interface

### TypeScript Interface

```typescript
/**
 * Input configuration for AI code optimization analysis
 */
interface AICodeOptimizerInput {
  /**
   * Source code to analyze (can be single function, file, or entire codebase)
   */
  code: {
    /**
     * Source code content
     */
    content: string;

    /**
     * Programming language
     */
    language: 'javascript' | 'typescript' | 'python' | 'java' | 'go' | 'rust' | 'csharp' | 'ruby';

    /**
     * Framework context (helps AI understand framework-specific patterns)
     */
    framework?: 'react' | 'vue' | 'angular' | 'express' | 'django' | 'spring-boot' | 'rails';

    /**
     * Entry point file path (for bundle analysis)
     */
    entryPoint?: string;

    /**
     * Additional context files
     */
    relatedFiles?: Array<{
      path: string;
      content: string;
    }>;
  };

  /**
   * Analysis scope and focus areas
   */
  analysis: {
    /**
     * Types of analysis to perform
     */
    types: Array<'performance' | 'memory' | 'bundle-size' | 'database' | 'security' | 'best-practices'>;

    /**
     * Depth of analysis
     * @default 'moderate'
     */
    depth?: 'quick' | 'moderate' | 'deep';

    /**
     * Focus on specific performance metrics
     */
    focus?: {
      /**
       * Time complexity threshold (e.g., warn if O(n²) or worse)
       */
      complexityThreshold?: 'O(n log n)' | 'O(n²)' | 'O(n³)';

      /**
       * Memory usage threshold (MB)
       */
      memoryThreshold?: number;

      /**
       * Bundle size threshold (KB)
       */
      bundleSizeThreshold?: number;

      /**
       * Minimum improvement percentage to report
       * @default 10
       */
      minImprovementPercent?: number;
    };
  };

  /**
   * Profiling data (optional, if available)
   */
  profiling?: {
    /**
     * Execution time profiling results
     */
    performance?: {
      /**
       * Function execution times (ms)
       */
      executionTimes: Record<string, number>;

      /**
       * Call counts
       */
      callCounts: Record<string, number>;

      /**
       * Hot paths
       */
      hotPaths?: string[];
    };

    /**
     * Memory profiling results
     */
    memory?: {
      /**
       * Heap snapshots
       */
      heapSize: number;

      /**
       * Retained size per object type
       */
      retainedSize: Record<string, number>;

      /**
       * Leak suspects
       */
      leakSuspects?: Array<{
        object: string;
        retainedSize: number;
        references: number;
      }>;
    };

    /**
     * Bundle analysis results
     */
    bundle?: {
      /**
       * Total bundle size (bytes)
       */
      totalSize: number;

      /**
       * Gzip size (bytes)
       */
      gzipSize?: number;

      /**
       * Module sizes
       */
      modules: Array<{
        name: string;
        size: number;
      }>;
    };
  };

  /**
   * Database schema context (for query optimization)
   */
  database?: {
    /**
     * Database type
     */
    type: 'postgresql' | 'mysql' | 'mongodb' | 'sqlite' | 'mssql';

    /**
     * Table schemas
     */
    schema?: Array<{
      table: string;
      columns: Array<{
        name: string;
        type: string;
        indexed: boolean;
      }>;
    }>;

    /**
     * Query execution plans (if available)
     */
    queryPlans?: Array<{
      query: string;
      plan: string;
      executionTime: number;
    }>;
  };

  /**
   * Optimization constraints and preferences
   */
  constraints?: {
    /**
     * Target runtime environment
     */
    targetEnvironment?: 'browser' | 'node' | 'mobile' | 'serverless';

    /**
     * Browser/Node version targets
     */
    targetVersions?: string[];

    /**
     * Maximum acceptable complexity (for trade-offs)
     */
    maxComplexity?: 'simple' | 'moderate' | 'complex';

    /**
     * Prefer readability over performance
     */
    prioritizeReadability?: boolean;

    /**
     * Allow breaking changes
     */
    allowBreakingChanges?: boolean;

    /**
     * Frameworks/libraries not allowed
     */
    excludedDependencies?: string[];
  };

  /**
   * Optimization goals
   */
  goals?: {
    /**
     * Target performance improvement (%)
     */
    performanceImprovement?: number;

    /**
     * Target memory reduction (%)
     */
    memoryReduction?: number;

    /**
     * Target bundle size reduction (%)
     */
    bundleSizeReduction?: number;

    /**
     * Acceptable increase in code complexity
     */
    acceptableComplexityIncrease?: number;
  };
}

/**
 * Output from AI code optimization analysis
 */
interface AICodeOptimizerOutput {
  /**
   * Summary of analysis results
   */
  summary: {
    /**
     * Overall optimization score (0-100)
     */
    score: number;

    /**
     * Total issues found
     */
    issuesFound: number;

    /**
     * Critical issues (must fix)
     */
    criticalCount: number;

    /**
     * High priority issues (should fix)
     */
    highCount: number;

    /**
     * Medium priority issues (nice to have)
     */
    mediumCount: number;

    /**
     * Estimated total performance improvement
     */
    estimatedImprovement: {
      performance?: string; // "75% faster"
      memory?: string; // "40% less memory"
      bundleSize?: string; // "30% smaller"
    };
  };

  /**
   * Detected issues and optimization opportunities
   */
  issues: Array<{
    /**
     * Issue identifier
     */
    id: string;

    /**
     * Severity level
     */
    severity: 'critical' | 'high' | 'medium' | 'low';

    /**
     * Issue category
     */
    type: 'performance' | 'memory' | 'bundle-size' | 'database' | 'algorithm' | 'security';

    /**
     * Location in code
     */
    location: {
      file?: string;
      line?: number;
      column?: number;
      function?: string;
    };

    /**
     * Problem description
     */
    problem: string;

    /**
     * Detailed explanation
     */
    explanation: string;

    /**
     * Performance impact
     */
    impact: {
      /**
       * Current metrics
       */
      before: {
        metric: string; // e.g., "Execution time", "Memory usage"
        value: string; // e.g., "2.3s", "150MB"
        complexity?: string; // e.g., "O(n²)"
      };

      /**
       * Expected metrics after optimization
       */
      after: {
        metric: string;
        value: string;
        complexity?: string;
      };

      /**
       * Improvement description
       */
      improvement: string; // "96% faster", "50% less memory"

      /**
       * Confidence level
       */
      confidence: 'high' | 'medium' | 'low';
    };

    /**
     * Root cause analysis
     */
    rootCause?: string;

    /**
     * Solution recommendation
     */
    solution: {
      /**
       * Short description
       */
      summary: string;

      /**
       * Detailed explanation
       */
      description: string;

      /**
       * Implementation steps
       */
      steps?: string[];

      /**
       * Effort estimate
       */
      effort: 'trivial' | 'easy' | 'moderate' | 'hard';

      /**
       * Risk level
       */
      risk: 'low' | 'medium' | 'high';
    };

    /**
     * Code snippets
     */
    code?: {
      /**
       * Current (problematic) code
       */
      before: string;

      /**
       * Optimized code
       */
      after: string;

      /**
       * Highlighted changes
       */
      diff?: string;
    };

    /**
     * References to best practices/documentation
     */
    references?: Array<{
      title: string;
      url: string;
      relevance: string;
    }>;

    /**
     * Related issues
     */
    relatedIssues?: string[]; // IDs of related issues
  }>;

  /**
   * Performance complexity analysis
   */
  complexity: {
    /**
     * Time complexity breakdown
     */
    timeComplexity: Array<{
      function: string;
      current: string; // "O(n²)"
      optimal: string; // "O(n log n)"
      recommendation: string;
    }>;

    /**
     * Space complexity breakdown
     */
    spaceComplexity: Array<{
      function: string;
      current: string; // "O(n)"
      optimal: string; // "O(1)"
      recommendation: string;
    }>;

    /**
     * Hot paths (most frequently executed)
     */
    hotPaths: Array<{
      path: string;
      executionCount: number;
      totalTime: number; // ms
      averageTime: number; // ms
      recommendation: string;
    }>;
  };

  /**
   * Memory analysis
   */
  memory?: {
    /**
     * Memory leak detection
     */
    leaks: Array<{
      location: string;
      type: 'event-listener' | 'closure' | 'global-reference' | 'timer' | 'cache';
      severity: 'critical' | 'high' | 'medium';
      description: string;
      fix: string;
    }>;

    /**
     * Large object allocations
     */
    largeAllocations: Array<{
      object: string;
      size: number; // bytes
      frequency: string; // "per request", "on startup"
      optimization: string;
    }>;

    /**
     * GC pressure analysis
     */
    gcPressure?: {
      score: number; // 0-100
      issues: string[];
      recommendations: string[];
    };
  };

  /**
   * Bundle optimization analysis
   */
  bundle?: {
    /**
     * Current bundle metrics
     */
    current: {
      totalSize: number; // bytes
      gzipSize: number; // bytes
      modules: number;
    };

    /**
     * Optimized bundle metrics
     */
    optimized: {
      totalSize: number;
      gzipSize: number;
      reduction: number; // percentage
    };

    /**
     * Tree shaking opportunities
     */
    treeShaking: Array<{
      module: string;
      unusedExports: string[];
      potentialSaving: number; // bytes
    }>;

    /**
     * Code splitting recommendations
     */
    codeSplitting: Array<{
      module: string;
      reason: string;
      strategy: 'dynamic-import' | 'route-based' | 'vendor-split';
      example: string; // code snippet
    }>;

    /**
     * Heavy dependencies
     */
    heavyDependencies: Array<{
      name: string;
      size: number; // bytes
      usage: string; // which features are used
      alternatives: Array<{
        name: string;
        size: number;
        pros: string[];
        cons: string[];
      }>;
    }>;
  };

  /**
   * Database optimization recommendations
   */
  database?: {
    /**
     * N+1 query problems
     */
    n1Queries: Array<{
      location: string;
      description: string;
      solution: string;
      estimatedImprovement: string; // "10x faster"
      codeExample: {
        before: string;
        after: string;
      };
    }>;

    /**
     * Missing indexes
     */
    missingIndexes: Array<{
      table: string;
      columns: string[];
      queryPattern: string;
      estimatedImprovement: string;
      sqlCommand: string; // CREATE INDEX ...
    }>;

    /**
     * Query optimization suggestions
     */
    queryOptimizations: Array<{
      query: string;
      issues: string[];
      optimizedQuery: string;
      explanation: string;
    }>;
  };

  /**
   * Consolidated optimization recommendations
   */
  recommendations: Array<{
    /**
     * Priority ranking
     */
    priority: number; // 1 = highest

    /**
     * Action description
     */
    action: string;

    /**
     * Expected impact
     */
    impact: string;

    /**
     * Implementation effort
     */
    effort: string;

    /**
     * Quick wins (high impact, low effort)
     */
    quickWin: boolean;

    /**
     * Implementation code/commands
     */
    implementation?: string;
  }>;

  /**
   * Best practices compliance
   */
  bestPractices: {
    /**
     * Compliance score (0-100)
     */
    score: number;

    /**
     * Checks performed
     */
    checks: Array<{
      category: string;
      passed: boolean;
      message: string;
      improvement?: string;
    }>;
  };

  /**
   * AI-generated insights
   */
  aiInsights: {
    /**
     * Pattern-based observations
     */
    patterns: string[];

    /**
     * Architectural recommendations
     */
    architecture: string[];

    /**
     * Technology recommendations
     */
    technology: string[];
  };

  /**
   * Benchmarking data (if profiling provided)
   */
  benchmarks?: {
    /**
     * Before optimization
     */
    before: {
      executionTime: number; // ms
      memoryUsage: number; // MB
      throughput?: number; // ops/sec
    };

    /**
     * After optimization (estimated)
     */
    after: {
      executionTime: number;
      memoryUsage: number;
      throughput?: number;
    };

    /**
     * Percentage improvements
     */
    improvements: {
      speed: number; // %
      memory: number; // %
      throughput?: number; // %
    };
  };
}
```

---

## Usage Examples

### Example 1: React Component Performance Optimization

**Scenario**: A React data table component renders slowly with large datasets (1000+ rows). Need to identify performance bottlenecks and apply optimizations.

**Input**:

```typescript
const input: AICodeOptimizerInput = {
  code: {
    content: `
// Slow implementation
function DataTable({ data }) {
  return (
    <table>
      {data.map(row => (
        <tr key={row.id}>
          {Object.values(row).map((cell, idx) => (
            <td key={idx}>{computeExpensiveFormat(cell)}</td>
          ))}
        </tr>
      ))}
    </table>
  );
}

function computeExpensiveFormat(value) {
  // Complex formatting: currency, dates, numbers
  if (typeof value === 'number') {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  }
  if (value instanceof Date) {
    return new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(value);
  }
  return String(value);
}
`,
    language: 'typescript',
    framework: 'react'
  },

  analysis: {
    types: ['performance', 'memory', 'best-practices'],
    depth: 'deep',
    focus: {
      complexityThreshold: 'O(n²)',
      minImprovementPercent: 20
    }
  },

  profiling: {
    performance: {
      executionTimes: {
        'DataTable': 2300, // 2.3 seconds for 100 rows x 10 columns
        'computeExpensiveFormat': 2.5 // 2.5ms per call, called 1000 times
      },
      callCounts: {
        'computeExpensiveFormat': 1000
      }
    }
  },

  constraints: {
    targetEnvironment: 'browser',
    prioritizeReadability: false,
    allowBreakingChanges: false
  },

  goals: {
    performanceImprovement: 80, // Target 80% faster
    memoryReduction: 30
  }
};
```

**Output**:

```typescript
{
  summary: {
    score: 35, // Low score indicates significant optimization opportunities
    issuesFound: 4,
    criticalCount: 1,
    highCount: 2,
    mediumCount: 1,
    estimatedImprovement: {
      performance: "96% faster (2.3s → 85ms)",
      memory: "45% less memory (reduced re-renders)",
      bundleSize: "N/A"
    }
  },

  issues: [
    {
      id: "PERF-001",
      severity: "critical",
      type: "performance",
      location: {
        file: "DataTable.tsx",
        line: 6,
        function: "DataTable"
      },

      problem: "Expensive computation on every render",
      explanation: "computeExpensiveFormat() is called 1,000 times per render (100 rows × 10 columns). With data updates, this causes severe performance degradation.",

      impact: {
        before: {
          metric: "Render time",
          value: "2,300ms",
          complexity: "O(rows × columns) per render"
        },
        after: {
          metric: "Render time",
          value: "85ms",
          complexity: "O(rows × columns) once, then O(1) on re-renders"
        },
        improvement: "96% faster (27x speedup)",
        confidence: "high"
      },

      rootCause: "React re-renders call computeExpensiveFormat for every cell on every render, even when data hasn't changed. Intl formatters are being recreated on every call.",

      solution: {
        summary: "Use useMemo to cache formatted data",
        description: "Memoize the formatted data so expensive computations only run when the data prop changes. Additionally, create formatters once outside the component to avoid recreation.",
        steps: [
          "Create formatters at module level (outside component)",
          "Use useMemo to cache formatted data",
          "Only recompute when data changes",
          "Use stable keys instead of array indices"
        ],
        effort: "easy",
        risk: "low"
      },

      code: {
        before: `function DataTable({ data }) {
  return (
    <table>
      {data.map(row => (
        <tr key={row.id}>
          {Object.values(row).map((cell, idx) => (
            <td key={idx}>{computeExpensiveFormat(cell)}</td>
          ))}
        </tr>
      ))}
    </table>
  );
}`,

        after: `import { useMemo } from 'react';

// Create formatters once at module level
const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
});
const dateFormatter = new Intl.DateTimeFormat('en-US', {
  dateStyle: 'medium'
});

function computeExpensiveFormat(value) {
  if (typeof value === 'number') {
    return currencyFormatter.format(value);
  }
  if (value instanceof Date) {
    return dateFormatter.format(value);
  }
  return String(value);
}

function DataTable({ data }) {
  // Memoize formatted data - only recomputes when data changes
  const formattedData = useMemo(() => {
    return data.map(row => ({
      id: row.id,
      cells: Object.entries(row)
        .filter(([key]) => key !== 'id')
        .map(([key, value]) => ({
          key,
          formatted: computeExpensiveFormat(value)
        }))
    }));
  }, [data]);

  return (
    <table>
      {formattedData.map(row => (
        <tr key={row.id}>
          {row.cells.map(cell => (
            <td key={cell.key}>{cell.formatted}</td>
          ))}
        </tr>
      ))}
    </table>
  );
}`,

        diff: `+ import { useMemo } from 'react';
+
+ // Create formatters once at module level
+ const currencyFormatter = new Intl.NumberFormat(...);
+ const dateFormatter = new Intl.DateTimeFormat(...);
+
  function DataTable({ data }) {
+   const formattedData = useMemo(() => {
+     return data.map(row => ({ ... }));
+   }, [data]);
+
    return (
      <table>
-       {data.map(row => (
+       {formattedData.map(row => (
          <tr key={row.id}>
-           {Object.values(row).map((cell, idx) => (
-             <td key={idx}>{computeExpensiveFormat(cell)}</td>
+           {row.cells.map(cell => (
+             <td key={cell.key}>{cell.formatted}</td>
            ))}
          </tr>
        ))}
      </table>
    );
  }`
      },

      references: [
        {
          title: "React useMemo Hook",
          url: "https://react.dev/reference/react/useMemo",
          relevance: "Caching expensive computations"
        },
        {
          title: "Optimizing Performance - React Docs",
          url: "https://react.dev/learn/render-and-commit#optimizing-performance",
          relevance: "Avoiding unnecessary renders"
        }
      ]
    },

    {
      id: "PERF-002",
      severity: "high",
      type: "performance",
      location: {
        line: 5,
        column: 32
      },

      problem: "Using array index as React key",
      explanation: "Using array indices as keys can cause React to mis-identify elements when data changes, leading to unnecessary re-renders and potential state bugs.",

      impact: {
        before: {
          metric: "Re-render efficiency",
          value: "Poor - all cells re-render on data change"
        },
        after: {
          metric: "Re-render efficiency",
          value: "Optimized - only changed cells re-render"
        },
        improvement: "40% fewer DOM operations",
        confidence: "high"
      },

      solution: {
        summary: "Use stable, unique keys",
        description: "Use column names as keys (cell.key in optimized code) to give React stable identifiers for reconciliation.",
        effort: "trivial",
        risk: "low"
      }
    },

    {
      id: "PERF-003",
      severity: "high",
      type: "best-practices",
      location: {
        function: "DataTable"
      },

      problem: "Missing React.memo for component optimization",
      explanation: "Component will re-render even when parent re-renders with the same props. For expensive components, this wastes resources.",

      solution: {
        summary: "Wrap component with React.memo",
        description: "Use React.memo to prevent unnecessary re-renders when props haven't changed.",
        steps: [
          "Wrap DataTable with React.memo",
          "Use custom comparison function if needed for deep prop comparison"
        ],
        effort: "trivial",
        risk: "low"
      },

      code: {
        after: `export const DataTable = React.memo(function DataTable({ data }) {
  // ... component code
});`
      }
    },

    {
      id: "MEM-001",
      severity: "medium",
      type: "memory",

      problem: "Large data virtualization opportunity",
      explanation: "Rendering 1,000+ rows creates thousands of DOM nodes, increasing memory usage and slowing down browser interactions.",

      solution: {
        summary: "Implement virtual scrolling for large datasets",
        description: "Use react-window or react-virtualized to render only visible rows, reducing DOM nodes from 1,000+ to ~20.",
        effort: "moderate",
        risk: "low"
      },

      code: {
        after: `import { FixedSizeList as List } from 'react-window';

function VirtualizedDataTable({ data }) {
  const Row = ({ index, style }) => {
    const row = formattedData[index];
    return (
      <div style={style} className="row">
        {row.cells.map(cell => (
          <span key={cell.key}>{cell.formatted}</span>
        ))}
      </div>
    );
  };

  return (
    <List
      height={600}
      itemCount={formattedData.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </List>
  );
}`
      },

      references: [
        {
          title: "react-window",
          url: "https://github.com/bvaughn/react-window",
          relevance: "Virtualized list rendering"
        }
      ]
    }
  ],

  complexity: {
    timeComplexity: [
      {
        function: "DataTable render",
        current: "O(n × m) per render (n=rows, m=columns)",
        optimal: "O(n × m) initial, O(1) subsequent renders with memoization",
        recommendation: "Apply useMemo caching"
      },
      {
        function: "computeExpensiveFormat",
        current: "O(1) per call, but called n×m times",
        optimal: "O(1) per call, called only when data changes",
        recommendation: "Memoize at higher level"
      }
    ],

    spaceComplexity: [
      {
        function: "DataTable",
        current: "O(n × m) DOM nodes",
        optimal: "O(visible_rows × m) with virtualization",
        recommendation: "Implement virtual scrolling for n > 100"
      }
    ],

    hotPaths: [
      {
        path: "DataTable → map → map → computeExpensiveFormat",
        executionCount: 1000,
        totalTime: 2300,
        averageTime: 2.3,
        recommendation: "Critical path - prioritize optimization"
      }
    ]
  },

  recommendations: [
    {
      priority: 1,
      action: "Apply useMemo to cache formatted data",
      impact: "96% faster rendering (2.3s → 85ms)",
      effort: "5-10 minutes",
      quickWin: true,
      implementation: "See PERF-001 optimized code"
    },
    {
      priority: 2,
      action: "Create Intl formatters at module level",
      impact: "15% additional speedup",
      effort: "2 minutes",
      quickWin: true,
      implementation: "Move formatter creation outside component"
    },
    {
      priority: 3,
      action: "Wrap component with React.memo",
      impact: "Prevent unnecessary parent-triggered re-renders",
      effort: "1 minute",
      quickWin: true,
      implementation: "export const DataTable = React.memo(...)"
    },
    {
      priority: 4,
      action: "Implement virtual scrolling (if data > 100 rows)",
      impact: "90% memory reduction, smoother scrolling",
      effort: "30-60 minutes",
      quickWin: false,
      implementation: "Use react-window library"
    }
  ],

  bestPractices: {
    score: 40,
    checks: [
      {
        category: "Performance",
        passed: false,
        message: "Expensive computations not memoized",
        improvement: "Use useMemo for expensive operations"
      },
      {
        category: "React Keys",
        passed: false,
        message: "Using array indices as keys",
        improvement: "Use stable, unique identifiers"
      },
      {
        category: "Component Optimization",
        passed: false,
        message: "Missing React.memo wrapper",
        improvement: "Wrap expensive components with React.memo"
      },
      {
        category: "Large Lists",
        passed: false,
        message: "Rendering 1000+ rows without virtualization",
        improvement: "Use react-window for virtual scrolling"
      }
    ]
  },

  aiInsights: {
    patterns: [
      "🔍 Detected anti-pattern: Expensive computation in render path",
      "🔍 Common performance issue: O(n×m) operations on every render",
      "🔍 Framework-specific: React re-render optimization opportunity"
    ],

    architecture: [
      "💡 Consider separating data formatting logic into a custom hook",
      "💡 For very large datasets (>10,000 rows), consider server-side pagination",
      "💡 If data updates frequently, debounce updates to reduce re-renders"
    ],

    technology: [
      "📦 Recommend: react-window for virtualization (22KB gzipped)",
      "📦 Alternative: react-virtualized (larger but more features)",
      "📦 Consider: Web Workers for formatting if CPU-bound"
    ]
  },

  benchmarks: {
    before: {
      executionTime: 2300, // ms
      memoryUsage: 45, // MB (DOM nodes)
      throughput: 0.43 // renders/sec
    },
    after: {
      executionTime: 85, // ms
      memoryUsage: 25, // MB (cached data)
      throughput: 11.76 // renders/sec
    },
    improvements: {
      speed: 96, // 96% faster
      memory: 44, // 44% less memory
      throughput: 2635 // 26x more renders/sec
    }
  }
}
```

**Performance Impact**:
- **Before**: 2,300ms render time, poor user experience
- **After**: 85ms render time, smooth and responsive
- **Improvement**: 96% faster (27x speedup)
- **Implementation time**: ~15 minutes for all optimizations
- **Risk**: Low (non-breaking changes)

---

### Example 2: Node.js API Bundle Size Optimization

**Scenario**: A serverless function has a 50MB deployment package, exceeding AWS Lambda limits. Need to identify and remove unnecessary dependencies.

**Input**:

```typescript
const input: AICodeOptimizerInput = {
  code: {
    content: `
import express from 'express';
import _ from 'lodash'; // Entire lodash library
import moment from 'moment'; // Heavy date library
import axios from 'axios';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const app = express();

app.post('/upload', async (req, res) => {
  const timestamp = moment().format('YYYY-MM-DD');
  const filename = \`upload-\${timestamp}.json\`;

  const data = _.pick(req.body, ['name', 'email', 'message']);

  const s3 = new S3Client({ region: 'us-east-1' });
  await s3.send(new PutObjectCommand({
    Bucket: 'uploads',
    Key: filename,
    Body: JSON.stringify(data)
  }));

  res.json({ success: true });
});

export default app;
`,
    language: 'typescript',
    framework: 'express',
    entryPoint: 'src/index.ts'
  },

  analysis: {
    types: ['bundle-size', 'performance'],
    depth: 'deep'
  },

  profiling: {
    bundle: {
      totalSize: 52428800, // 50MB
      gzipSize: 18874368, // 18MB
      modules: [
        { name: 'lodash', size: 544768 },
        { name: 'moment', size: 411648 },
        { name: 'express', size: 208896 },
        { name: '@aws-sdk/client-s3', size: 1048576 },
        { name: 'axios', size: 114688 }
      ]
    }
  },

  constraints: {
    targetEnvironment: 'serverless',
    targetVersions: ['node18']
  },

  goals: {
    bundleSizeReduction: 60 // Target 60% smaller
  }
};
```

**Output**:

```typescript
{
  summary: {
    score: 25,
    issuesFound: 5,
    criticalCount: 2,
    highCount: 2,
    mediumCount: 1,
    estimatedImprovement: {
      bundleSize: "72% smaller (50MB → 14MB)"
    }
  },

  issues: [
    {
      id: "BUNDLE-001",
      severity: "critical",
      type: "bundle-size",

      problem: "Importing entire lodash library for one function",
      explanation: "The entire lodash library (544KB) is imported when only _.pick (2KB) is used.",

      impact: {
        before: {
          metric: "Lodash bundle size",
          value: "544KB"
        },
        after: {
          metric: "Lodash bundle size",
          value: "0KB (use native JS)"
        },
        improvement: "544KB saved (100% reduction)",
        confidence: "high"
      },

      solution: {
        summary: "Replace with native JavaScript",
        description: "Object destructuring can replace _.pick with zero dependencies.",
        effort: "trivial",
        risk: "low"
      },

      code: {
        before: `import _ from 'lodash';
const data = _.pick(req.body, ['name', 'email', 'message']);`,

        after: `// Native JavaScript - zero dependencies
const { name, email, message } = req.body;
const data = { name, email, message };`
      }
    },

    {
      id: "BUNDLE-002",
      severity: "critical",
      type: "bundle-size",

      problem: "Using moment.js (411KB) for simple date formatting",
      explanation: "moment.js is a legacy, heavy library. Modern alternatives are 10x smaller.",

      impact: {
        before: {
          metric: "Date library size",
          value: "411KB"
        },
        after: {
          metric: "Date library size",
          value: "0KB (native Intl)"
        },
        improvement: "411KB saved",
        confidence: "high"
      },

      solution: {
        summary: "Use native Date/Intl or date-fns",
        description: "Native Intl.DateTimeFormat or lightweight date-fns-tz (6KB) are better options.",
        effort: "easy",
        risk: "low"
      },

      code: {
        before: `import moment from 'moment';
const timestamp = moment().format('YYYY-MM-DD');`,

        after: `// Option 1: Native JavaScript (0KB)
const timestamp = new Date().toISOString().split('T')[0];

// Option 2: date-fns (6KB, tree-shakeable)
import { format } from 'date-fns';
const timestamp = format(new Date(), 'yyyy-MM-dd');`
      },

      references: [
        {
          title: "You Don't Need Momentjs",
          url: "https://github.com/you-dont-need/You-Dont-Need-Momentjs",
          relevance: "Modern alternatives to moment.js"
        }
      ]
    },

    {
      id: "BUNDLE-003",
      severity: "high",
      type: "bundle-size",

      problem: "AWS SDK v3 not tree-shaken properly",
      explanation: "AWS SDK client-s3 includes many unused operations. Ensure tree-shaking is configured correctly.",

      impact: {
        before: {
          metric: "AWS SDK size",
          value: "1MB"
        },
        after: {
          metric: "AWS SDK size",
          value: "450KB (tree-shaken)"
        },
        improvement: "550KB saved",
        confidence: "medium"
      },

      solution: {
        summary: "Verify tree-shaking configuration",
        description: "Ensure bundler (webpack/esbuild) has sideEffects: false in package.json and uses ES modules.",
        effort: "easy",
        risk: "low"
      }
    }
  ],

  bundle: {
    current: {
      totalSize: 52428800, // 50MB
      gzipSize: 18874368, // 18MB
      modules: 127
    },

    optimized: {
      totalSize: 14680064, // 14MB
      gzipSize: 5767168, // 5.5MB
      reduction: 72 // 72% reduction
    },

    treeShaking: [
      {
        module: 'lodash',
        unusedExports: ['all 299 functions except pick'],
        potentialSaving: 544000 // bytes
      },
      {
        module: '@aws-sdk/client-s3',
        unusedExports: ['ListBuckets', 'GetObject', ...],
        potentialSaving: 550000
      }
    ],

    codeSplitting: [
      {
        module: '@aws-sdk/client-s3',
        reason: "S3 client only used in one route",
        strategy: 'dynamic-import',
        example: `app.post('/upload', async (req, res) => {
  // Dynamic import - only loaded when route is hit
  const { S3Client, PutObjectCommand } = await import('@aws-sdk/client-s3');
  const s3 = new S3Client({ region: 'us-east-1' });
  // ...
});`
      }
    ],

    heavyDependencies: [
      {
        name: 'moment',
        size: 411648,
        usage: "Only .format('YYYY-MM-DD')",
        alternatives: [
          {
            name: 'native Date',
            size: 0,
            pros: ['Zero dependencies', 'Built-in'],
            cons: ['Less features']
          },
          {
            name: 'date-fns',
            size: 6144,
            pros: ['Tree-shakeable', 'Modern', 'Modular'],
            cons: ['Requires import']
          },
          {
            name: 'day.js',
            size: 2048,
            pros: ['Moment.js compatible API', 'Tiny'],
            cons: ['Smaller ecosystem']
          }
        ]
      },
      {
        name: 'lodash',
        size: 544768,
        usage: "Only _.pick",
        alternatives: [
          {
            name: 'native JS destructuring',
            size: 0,
            pros: ['Zero cost', 'Native'],
            cons: ['Different syntax']
          },
          {
            name: 'lodash-es',
            size: 2048, // only the used function
            pros: ['Tree-shakeable', 'Same API'],
            cons: ['Still dependency']
          }
        ]
      }
    ]
  },

  recommendations: [
    {
      priority: 1,
      action: "Remove moment.js, use native Date",
      impact: "411KB saved",
      effort: "5 minutes",
      quickWin: true,
      implementation: "Replace moment().format() with new Date().toISOString().split('T')[0]"
    },
    {
      priority: 2,
      action: "Remove lodash, use native destructuring",
      impact: "544KB saved",
      effort: "2 minutes",
      quickWin: true,
      implementation: "Use const { name, email, message } = req.body"
    },
    {
      priority: 3,
      action: "Configure AWS SDK tree-shaking",
      impact: "550KB saved",
      effort: "10 minutes",
      quickWin: true,
      implementation: "Update bundler config to enable sideEffects: false"
    },
    {
      priority: 4,
      action: "Use dynamic imports for S3 client",
      impact: "Faster cold start",
      effort: "5 minutes",
      quickWin: true,
      implementation: "await import('@aws-sdk/client-s3')"
    }
  ],

  aiInsights: {
    patterns: [
      "🔍 Detected: Over-importing from utility libraries",
      "🔍 Pattern: Legacy heavy libraries (moment.js) still in use",
      "🔍 Opportunity: Modern JavaScript can replace most utilities"
    ],

    technology: [
      "📦 Recommend: date-fns over moment.js (67x smaller)",
      "📦 Recommend: Native JS over lodash for simple operations",
      "📦 Consider: esbuild for faster, smaller bundles vs webpack"
    ]
  }
}
```

**Bundle Impact**:
- **Before**: 50MB total, 18MB gzipped
- **After**: 14MB total, 5.5MB gzipped
- **Reduction**: 72% smaller (under AWS Lambda 50MB limit)
- **Cold start improvement**: 40% faster (less code to load)

---

### Example 3: Database N+1 Query Optimization

**Scenario**: An API endpoint loads user posts and comments, causing 100+ database queries. Need to identify and fix N+1 query problems.

**Input**:

```typescript
const input: AICodeOptimizerInput = {
  code: {
    content: `
async function getPostsWithComments(userId) {
  // Query 1: Fetch all posts by user
  const posts = await Post.find({ userId });

  // N+1 Problem: One query per post for comments
  for (const post of posts) {
    post.comments = await Comment.find({ postId: post.id });
  }

  // Another N+1 Problem: One query per comment for author
  for (const post of posts) {
    for (const comment of post.comments) {
      comment.author = await User.findById(comment.authorId);
    }
  }

  return posts;
}
`,
    language: 'typescript',
    framework: 'express'
  },

  analysis: {
    types: ['database', 'performance'],
    depth: 'deep'
  },

  database: {
    type: 'postgresql',
    schema: [
      {
        table: 'posts',
        columns: [
          { name: 'id', type: 'uuid', indexed: true },
          { name: 'userId', type: 'uuid', indexed: true },
          { name: 'title', type: 'text', indexed: false }
        ]
      },
      {
        table: 'comments',
        columns: [
          { name: 'id', type: 'uuid', indexed: true },
          { name: 'postId', type: 'uuid', indexed: true },
          { name: 'authorId', type: 'uuid', indexed: true }
        ]
      },
      {
        table: 'users',
        columns: [
          { name: 'id', type: 'uuid', indexed: true },
          { name: 'name', type: 'text', indexed: false }
        ]
      }
    ]
  },

  profiling: {
    performance: {
      executionTimes: {
        'getPostsWithComments': 3200 // 3.2 seconds for 50 posts with 1000 comments
      }
    }
  }
};
```

**Output** (abbreviated):

```typescript
{
  summary: {
    score: 15,
    issuesFound: 2,
    criticalCount: 2,
    estimatedImprovement: {
      performance: "98% faster (3.2s → 65ms)",
      database: "1051 queries → 3 queries"
    }
  },

  issues: [
    {
      id: "DB-001",
      severity: "critical",
      type: "database",

      problem: "N+1 query problem: fetching comments",
      explanation: "For 50 posts, this creates 50 separate queries to fetch comments instead of one batched query.",

      impact: {
        before: {
          metric: "Database queries",
          value: "1 + 50 = 51 queries"
        },
        after: {
          metric: "Database queries",
          value: "1 + 1 = 2 queries"
        },
        improvement: "96% fewer queries (10x faster)",
        confidence: "high"
      },

      solution: {
        summary: "Use eager loading with JOIN or IN query",
        description: "Fetch all comments for all posts in a single query.",
        effort: "easy",
        risk: "low"
      },

      code: {
        before: `for (const post of posts) {
  post.comments = await Comment.find({ postId: post.id });
}`,

        after: `// Option 1: Using ORM eager loading (Sequelize/TypeORM)
const posts = await Post.find({ userId })
  .include({ model: Comment });

// Option 2: Manual batching
const postIds = posts.map(p => p.id);
const allComments = await Comment.find({ postId: { $in: postIds } });

// Group comments by postId
const commentsByPost = _.groupBy(allComments, 'postId');
posts.forEach(post => {
  post.comments = commentsByPost[post.id] || [];
});`
      }
    },

    {
      id: "DB-002",
      severity: "critical",
      type: "database",

      problem: "Nested N+1 query problem: fetching authors",
      explanation: "For 1000 comments, creates 1000 separate queries to fetch authors.",

      impact: {
        before: {
          metric: "Author queries",
          value: "1000 queries"
        },
        after: {
          metric: "Author queries",
          value: "1 query"
        },
        improvement: "99.9% fewer queries",
        confidence: "high"
      },

      code: {
        after: `// Fetch all unique authors in one query
const authorIds = [...new Set(allComments.map(c => c.authorId))];
const authors = await User.find({ id: { $in: authorIds } });
const authorsById = _.keyBy(authors, 'id');

allComments.forEach(comment => {
  comment.author = authorsById[comment.authorId];
});`
      }
    }
  ],

  database: {
    n1Queries: [
      {
        location: "getPostsWithComments:6",
        description: "Loading comments in loop: 50 queries",
        solution: "Use Post.find().include(Comment) or batch with $in query",
        estimatedImprovement: "10x faster",
        codeExample: {
          before: "await Comment.find({ postId: post.id })",
          after: "await Comment.find({ postId: { $in: postIds } })"
        }
      },
      {
        location: "getPostsWithComments:12",
        description: "Loading authors in nested loop: 1000 queries",
        solution: "Batch load all unique authors with single $in query",
        estimatedImprovement: "50x faster",
        codeExample: {
          before: "await User.findById(comment.authorId)",
          after: "await User.find({ id: { $in: authorIds } })"
        }
      }
    ],

    missingIndexes: [],

    queryOptimizations: [
      {
        query: "Comment.find({ postId: post.id })",
        issues: ["Executed in loop (N+1 problem)"],
        optimizedQuery: "Comment.find({ postId: { $in: [id1, id2, ...] } })",
        explanation: "Batch all postIds into single query with $in operator"
      }
    ]
  },

  recommendations: [
    {
      priority: 1,
      action: "Fix N+1 query for comments",
      impact: "96% fewer database queries",
      effort: "10 minutes",
      quickWin: true
    },
    {
      priority: 2,
      action: "Fix nested N+1 query for authors",
      impact: "99.9% fewer author queries",
      effort: "15 minutes",
      quickWin: true
    },
    {
      priority: 3,
      action: "Use ORM eager loading if available",
      impact: "Cleaner code, same performance",
      effort: "5 minutes",
      quickWin: true
    }
  ],

  benchmarks: {
    before: {
      executionTime: 3200, // ms
      throughput: 0.31 // requests/sec
    },
    after: {
      executionTime: 65, // ms
      throughput: 15.38 // requests/sec
    },
    improvements: {
      speed: 98, // 98% faster
      throughput: 4858 // 49x more throughput
    }
  }
}
```

**Database Performance Impact**:
- **Before**: 1,051 queries (1 + 50 + 1000)
- **After**: 3 queries (posts, comments, authors)
- **Speedup**: 49x faster (3.2s → 65ms)

---

## Best Practices

### DO ✅

```typescript
// DO: Profile before optimizing
const start = performance.now();
const result = heavyComputation();
console.log(`Execution time: ${performance.now() - start}ms`);

// DO: Measure impact of optimizations
const before = measurePerformance();
applyOptimization();
const after = measurePerformance();
console.log(`Improvement: ${((before - after) / before * 100).toFixed(1)}%`);

// DO: Use memoization for expensive computations
const expensiveResult = useMemo(() => {
  return complexCalculation(data);
}, [data]);

// DO: Batch database queries
const userIds = posts.map(p => p.userId);
const users = await User.find({ id: { $in: userIds } });

// DO: Use native JavaScript when possible
// ❌ import _ from 'lodash'
// ✅ Native JS
const picked = { name, email } = user;

// DO: Lazy load heavy dependencies
const heavyLibrary = await import('heavy-library');

// DO: Implement virtual scrolling for large lists
<VirtualList itemCount={10000} itemSize={50}>
  {Row}
</VirtualList>

// DO: Cache at appropriate levels
// Module-level cache for constants
const formatter = new Intl.NumberFormat();

// Component-level cache for data
const memoizedData = useMemo(() => transform(data), [data]);

// DO: Use indexes on frequently queried columns
CREATE INDEX idx_user_email ON users(email);

// DO: Prefer O(n) or O(n log n) algorithms
// ✅ O(n) - Set lookup
const set = new Set(array);
if (set.has(value)) { ... }

// ❌ O(n²) - Nested loops
for (const item1 of array1) {
  for (const item2 of array2) { ... }
}
```

### DON'T ❌

```typescript
// DON'T: Premature optimization
// ❌ Optimizing before measuring
function ultraOptimizedButUnreadable() { ... }

// ✅ Write clear code first, optimize if needed
function clearAndMaintainable() { ... }

// DON'T: Optimize without profiling
// ❌ Guessing what's slow
"I think this function is slow, let me optimize it"

// ✅ Measure first
const profile = runProfiler();
optimizeHotPaths(profile.slowest());

// DON'T: Create memory leaks with closures
// ❌ Closure captures large object
function processBigData(data) {
  return () => {
    console.log(data.length); // Entire 'data' retained
  };
}

// ✅ Only capture what you need
function processBigData(data) {
  const length = data.length;
  return () => {
    console.log(length); // Only number retained
  };
}

// DON'T: Use array methods inefficiently
// ❌ Multiple passes
const result = array
  .filter(x => x > 0)
  .map(x => x * 2)
  .filter(x => x < 100);

// ✅ Single pass
const result = array.reduce((acc, x) => {
  const transformed = x * 2;
  if (x > 0 && transformed < 100) {
    acc.push(transformed);
  }
  return acc;
}, []);

// DON'T: Import entire libraries
// ❌ 500KB for one function
import _ from 'lodash';
const result = _.debounce(fn, 100);

// ✅ Tree-shakeable import
import debounce from 'lodash-es/debounce';

// DON'T: Recreate objects in render
// ❌ New object every render
<Component style={{ margin: 10 }} />

// ✅ Memoize stable objects
const style = useMemo(() => ({ margin: 10 }), []);
<Component style={style} />

// DON'T: Ignore database indexing
// ❌ Full table scan on every query
SELECT * FROM users WHERE email = 'user@example.com';
// Without index on 'email' column

// ✅ Create appropriate indexes
CREATE INDEX idx_user_email ON users(email);

// DON'T: Fetch unnecessary data
// ❌ Loading all columns
SELECT * FROM products WHERE category = 'electronics';

// ✅ Select only needed columns
SELECT id, name, price FROM products WHERE category = 'electronics';

// DON'T: Block the event loop (Node.js)
// ❌ Synchronous heavy computation
const result = heavySync Computation();

// ✅ Use async or Worker Threads
const result = await heavyAsyncComputation();

// DON'T: Ignore bundle size
// ❌ Moment.js (411KB)
import moment from 'moment';

// ✅ date-fns (6KB, tree-shakeable)
import { format } from 'date-fns';
```

---

## Related Skills

- **performance-monitor** (Skill 10): Real-time performance monitoring that feeds profiling data into AI Code Optimizer for continuous optimization
- **code-reviewer** (Skill 4): Automated code review that flags performance anti-patterns before they reach production
- **test-generator** (Skill 3): Generates performance benchmarks and regression tests to validate optimization improvements
- **architecture-designer** (Skill 6): Provides architectural patterns that inherently avoid performance pitfalls
- **database-manager** (Skill 11): Database schema optimization and query plan analysis for backend optimization
- **bundler-optimizer**: Webpack/Vite/Rollup configuration optimization for frontend bundle size reduction

---

## Changelog

### Version 2.0.0 (2025-01-12)
- Initial release of AI Code Optimizer
- Performance analysis with Big O complexity detection
- Algorithm optimization recommendations with before/after comparisons
- Memory leak detection and GC pressure analysis
- Bundle size optimization with tree-shaking and code-splitting suggestions
- Database N+1 query detection and batching recommendations
- AI-powered pattern matching against performance best practices
- Three comprehensive production examples (React, Node.js bundle, Database)
- Complete TypeScript interfaces with 60+ analysis options
- Measurable performance impact predictions with confiden
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
interface AICodeOptimizerInput {

  safetyChecks: {
    requireTests: boolean;
    runTestsBeforeApply: boolean;
    minCoverage: number;
    rollbackOnFailure: boolean;
    allowBreakingChanges: boolean;
  };
}
```

### 输出接口

```typescript
interface AICodeOptimizerOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段

  testResults?: {
    beforeRefactor: {
      passed: number;
      failed: number;
      skipped: number;
      coverage: number;
      runtime: number;
    };
    afterRefactor: {
      passed: number;
      failed: number;
      skipped: number;
      coverage: number;
      runtime: number;
    };
    regressionDetected: boolean;
    performanceChange: number;
    safeToApply: boolean;
  };
}
```

---

ce levels
