---
name: 29-knowledge-manager-G
description: Intelligent technical documentation generation and management tool for auto-generating API docs (OpenAPI/Swagger), architecture diagrams (C4 Model/DFD/ER), runbooks (troubleshooting guides), knowledge base. Supports docs-as-code, full-text search, version control, multi-platform sync (Notion/Confluence/GitHub Wiki), AI Q&A assistant. Use for microservice docs, onboarding, knowledge base building, troubleshooting guides, doc syncing.
---

# Knowledge Manager - 技术知识管理器

**Version**: 2.0.0
**Category**: Project Management
**Priority**: P2
**Last Updated**: 2025-12-12

---

## Description

智能技术文档生成与管理工具，自动从代码生成API文档、架构图、Runbook和知识库。支持文档即代码(Docs-as-Code)、全文搜索、版本控制和多平台同步(Notion/Confluence/GitHub Wiki)，提升团队知识共享和新人onboarding效率。

### Core Capabilities

- **Auto Documentation**: 从代码注释生成OpenAPI/Swagger文档、README自动化生成、CHANGELOG自动提取、代码示例生成、JSDoc/Docstring → Markdown
- **Architecture Diagrams**: C4 Model架构图(System/Container/Component/Code)、数据流图(DFD)、ER图(Entity-Relationship)、序列图、依赖关系图
- **Knowledge Base**: Markdown wiki系统、全文搜索(Algolia/Elasticsearch)、标签分类、版本历史、模板管理、文档审查流程
- **Runbook Generation**: 故障排查手册(症状→排查→缓解→修复)、部署步骤文档、监控playbook、回滚指南、灾难恢复流程
- **Sync Integration**: Notion数据库同步、Confluence空间集成、GitHub Wiki自动发布、文档CI/CD管道、多语言翻译
- **AI Q&A Assistant**: 基于知识库的智能问答、代码搜索、相关文档推荐、新人onboarding助手、文档gap检测

---

## Instructions

### When to Activate

Trigger this skill when you encounter:

1. **New Service Documentation** - 微服务需要完整文档(API+架构+部署+监控)
2. **Onboarding New Members** - 新人需要快速了解系统架构和代码库
3. **Knowledge Scattered** - 文档分散在Slack/Email/Notion/代码注释中
4. **Documentation Debt** - 文档过时或缺失，影响团队协作
5. **Incident Response** - 需要Runbook指导故障排查和修复
6. **Code Review** - 检查文档与代码是否同步

**Common trigger phrases**:
- "生成API文档从代码注释"
- "画出系统架构图"
- "创建部署Runbook"
- "构建知识库搜索"
- "同步文档到Confluence"

### Execution Flow

```mermaid
graph TD
    A[接收文档任务请求] --> B{选择文档类型}
    B -->|API文档| C[扫描代码注释/OpenAPI spec]
    B -->|架构图| D[分析代码依赖和配置]
    B -->|Runbook| E[收集运维知识和最佳实践]
    B -->|知识库| F[整理现有文档]

    C --> G[解析路由/控制器/Schema]
    D --> H[生成C4 Model层级图]
    E --> I[结构化故障场景]
    F --> J[建立标签和索引]

    G --> K[生成Markdown/HTML文档]
    H --> K
    I --> K
    J --> K

    K --> L{需要同步到外部?}
    L -->|Notion| M[调用Notion API同步]
    L -->|Confluence| N[调用Confluence REST API]
    L -->|GitHub Wiki| O[Git push到wiki分支]
    L -->|否| P[本地docs/目录]

    M --> Q[启用全文搜索索引]
    N --> Q
    O --> Q
    P --> Q

    Q --> R[生成文档地图和导航]
    R --> S{需要AI助手?}
    S -->|是| T[训练Q&A模型]
    S -->|否| U[返回文档URL]
    T --> U
```

---

## TypeScript Interfaces

```typescript
/**
 * Knowledge Manager输入配置
 */
interface KnowledgeManagerInput {
  /**
   * 文档任务类型
   */
  task: {
    type:
      | 'api-docs'           // API文档生成
      | 'architecture'       // 架构图生成
      | 'runbook'            // 故障排查手册
      | 'deployment-guide'   // 部署指南
      | 'knowledge-base'     // 知识库构建
      | 'onboarding-guide'   // 新人入职指南
      | 'changelog';         // 变更日志生成

    description?: string;    // 任务详细描述
  };

  /**
   * 源代码/配置信息
   */
  sources?: {
    /**
     * 代码库路径或URL
     */
    codebase?: {
      path?: string;         // 本地路径 "src/"
      gitRepo?: string;      // Git仓库URL
      branch?: string;       // 分支名称
      language?: 'typescript' | 'python' | 'go' | 'java' | 'rust';
    };

    /**
     * OpenAPI/Swagger规范
     */
    openApiSpec?: {
      path?: string;         // "openapi.yaml"
      version?: '2.0' | '3.0' | '3.1';
    };

    /**
     * 配置文件
     */
    configs?: Array<{
      type: 'kubernetes' | 'docker-compose' | 'terraform' | 'helm';
      path: string;
    }>;

    /**
     * 现有文档
     */
    existingDocs?: {
      path: string;          // "docs/"
      format: 'markdown' | 'restructuredtext' | 'asciidoc';
    };

    /**
     * 运维数据
     */
    opsData?: {
      incidentReports?: string[];   // 事故报告路径
      runbooks?: string[];          // 已有Runbook路径
      monitoringDashboards?: string[];  // Grafana/Prometheus URL
    };
  };

  /**
   * 文档配置
   */
  docConfig?: {
    /**
     * 输出格式
     */
    outputFormat?: {
      primary: 'markdown' | 'html' | 'pdf';
      includeTOC?: boolean;         // 目录
      includeIndex?: boolean;       // 索引
      codeHighlighting?: boolean;   // 代码高亮
    };

    /**
     * 文档结构
     */
    structure?: {
      sections?: Array<'overview' | 'installation' | 'api-reference' | 'architecture' | 'deployment' | 'troubleshooting' | 'faq' | 'changelog'>;
      maxDepth?: number;            // 标题最大层级
      includeDiagrams?: boolean;    // 包含图表
    };

    /**
     * 架构图配置（如果type='architecture'）
     */
    architecture?: {
      diagramTypes?: Array<'c4-system' | 'c4-container' | 'c4-component' | 'sequence' | 'dataflow' | 'er-diagram' | 'dependency-graph'>;
      detail Level?: 'high-level' | 'medium' | 'detailed';
      includeExternalSystems?: boolean;
      technology Stack?: boolean;   // 标注技术栈
    };

    /**
     * API文档配置（如果type='api-docs'）
     */
    apiDocs?: {
      includeExamples?: boolean;    // 包含请求/响应示例
      includeErrorCodes?: boolean;  // 错误码文档
      authenticationDoc?: boolean;  // 认证文档
      rateLimitDoc?: boolean;       // 限流文档
      generateSDK?: boolean;        // 生成SDK代码示例
      languages?: string[];         // ['curl', 'python', 'javascript', 'go']
    };

    /**
     * Runbook配置（如果type='runbook'）
     */
    runbook?: {
      scenarios?: Array<{
        name: string;               // "数据库连接失败"
        severity: 'low' | 'medium' | 'high' | 'critical';
        frequency?: 'rare' | 'occasional' | 'frequent';
      }>;
      includeMetrics?: boolean;     // 包含监控指标
      includeCommands?: boolean;    // 包含诊断命令
      includeRollback?: boolean;    // 包含回滚步骤
    };
  };

  /**
   * 同步集成
   */
  sync?: {
    /**
     * 目标平台
     */
    targets?: Array<{
      platform: 'notion' | 'confluence' | 'github-wiki' | 'gitbook';

      /**
       * Notion配置
       */
      notion?: {
        apiKey: string;
        databaseId?: string;        // Database ID
        pageId?: string;            // Parent page ID
        autoUpdate?: boolean;       // 自动更新
      };

      /**
       * Confluence配置
       */
      confluence?: {
        baseUrl: string;            // "https://company.atlassian.net"
        username: string;
        apiToken: string;
        spaceKey: string;           // "DEV"
        parentPageId?: string;
      };

      /**
       * GitHub Wiki配置
       */
      githubWiki?: {
        repo: string;               // "org/repo"
        token: string;
        branch?: string;            // default: "main"
      };
    }>;

    /**
     * 同步策略
     */
    strategy?: {
      mode: 'one-time' | 'continuous' | 'on-commit';
      conflictResolution?: 'overwrite' | 'merge' | 'manual';
      versionControl?: boolean;   // 保留历史版本
    };
  };

  /**
   * 知识库配置
   */
  knowledgeBase?: {
    /**
     * 搜索引擎
     */
    search?: {
      engine: 'algolia' | 'elasticsearch' | 'simple';
      algolia?: {
        appId: string;
        apiKey: string;
        indexName: string;
      };
      elasticsearch?: {
        url: string;
        index: string;
      };
    };

    /**
     * 分类系统
     */
    taxonomy?: {
      tags?: string[];              // ["backend", "frontend", "devops"]
      categories?: string[];        // ["api", "architecture", "runbook"]
      autoTag?: boolean;            // 自动标签建议
    };

    /**
     * AI助手
     */
    aiAssistant?: {
      enabled: boolean;
      model?: 'claude' | 'gpt' | 'gemini';
      capabilities?: Array<'qa' | 'code-search' | 'doc-recommendation'>;
      contextWindow?: number;       // Token上下文窗口
    };
  };

  /**
   * 输出配置
   */
  output?: {
    directory?: string;             // "docs/" or "wiki/"
    filename?: string;              // "API_REFERENCE.md"
    staticSite?: {
      generator?: 'mkdocs' | 'docusaurus' | 'vuepress' | 'hugo';
      theme?: string;
      deploy?: {
        platform: 'vercel' | 'netlify' | 'github-pages';
        url?: string;
      };
    };
  };
}

/**
 * Knowledge Manager输出结果
 */
interface KnowledgeManagerOutput {
  /**
   * 任务摘要
   */
  summary: {
    taskType: string;
    documentsGenerated: number;
    diagramsGenerated?: number;
    totalPages?: number;
    executionTime: number;          // ms
  };

  /**
   * 生成的文档
   */
  documents: Array<{
    id: string;
    title: string;
    type: 'api-docs' | 'architecture' | 'runbook' | 'guide' | 'reference';

    /**
     * 文档内容
     */
    content: {
      markdown: string;             // Markdown源文件
      html?: string;                // 渲染后的HTML
      pdf?: string;                 // PDF文件路径
    };

    /**
     * 元数据
     */
    metadata: {
      version: string;              // "2.3.0"
      createdAt: string;            // ISO timestamp
      updatedAt: string;
      authors?: string[];
      tags?: string[];
      wordCount: number;
      estimatedReadTime: number;    // 分钟
    };

    /**
     * 文档结构
     */
    structure: {
      sections: Array<{
        id: string;
        title: string;
        level: number;              // 1-6 (h1-h6)
        anchor: string;             // "#installation"
        wordCount: number;
      }>;
      toc: string;                  // Markdown格式目录
    };

    /**
     * 关联资源
     */
    assets?: {
      diagrams?: Array<{
        type: 'c4' | 'sequence' | 'dataflow' | 'er';
        title: string;
        format: 'svg' | 'png' | 'mermaid';
        url: string;
        description?: string;
      }>;
      codeExamples?: Array<{
        language: string;
        code: string;
        description: string;
      }>;
    };
  }>;

  /**
   * 架构图详情（如果生成了架构图）
   */
  architectureDiagrams?: Array<{
    type: 'c4-system' | 'c4-container' | 'c4-component' | 'sequence' | 'dataflow' | 'er-diagram';
    level: 'high-level' | 'medium' | 'detailed';

    /**
     * 图表数据
     */
    diagram: {
      mermaidCode?: string;         // Mermaid语法
      plantUMLCode?: string;        // PlantUML语法
      svgUrl?: string;              // 渲染后的SVG
      pngUrl?: string;              // 渲染后的PNG
    };

    /**
     * 组件清单
     */
    components?: Array<{
      id: string;
      name: string;
      type: 'service' | 'database' | 'cache' | 'queue' | 'external-api';
      technology?: string;          // "PostgreSQL", "Redis"
      description?: string;
    }>;

    /**
     * 连接关系
     */
    connections?: Array<{
      from: string;                 // 组件ID
      to: string;
      protocol?: string;            // "HTTPS", "gRPC"
      description?: string;         // "Authentication request"
    }>;

    /**
     * 注释说明
     */
    annotations?: Array<{
      componentId: string;
      note: string;
      importance: 'low' | 'medium' | 'high';
    }>;
  }>;

  /**
   * Runbook详情（如果生成了Runbook）
   */
  runbooks?: Array<{
    scenario: {
      name: string;                 // "支付失败率>5%"
      severity: 'low' | 'medium' | 'high' | 'critical';
      frequency: 'rare' | 'occasional' | 'frequent';
      impact: string;               // "用户无法完成支付"
    };

    /**
     * 症状识别
     */
    symptoms: Array<{
      description: string;
      detectionMethod?: string;     // "Grafana alert", "User report"
      example?: string;
    }>;

    /**
     * 排查步骤
     */
    troubleshooting: Array<{
      step: number;
      action: string;
      expectedOutcome?: string;
      commands?: string[];          // 诊断命令
      checkpoints?: string[];       // 检查点
    }>;

    /**
     * 临时缓解
     */
    mitigation?: {
      description: string;
      steps: string[];
      commands?: string[];
      estimatedTime: string;        // "5-10分钟"
      risks?: string[];
    };

    /**
     * 永久修复
     */
    permanentFix?: {
      description: string;
      steps: string[];
      pullRequest?: string;         // PR链接
      estimatedTime: string;
      verification: string[];       // 验证步骤
    };

    /**
     * 回滚计划
     */
    rollback?: {
      when: string;                 // "如果缓解措施无效超过30分钟"
      steps: string[];
      commands?: string[];
    };

    /**
     * 相关监控
     */
    monitoring?: {
      dashboards?: string[];        // Grafana URL
      alerts?: string[];            // 告警规则名称
      metrics: Array<{
        name: string;
        threshold: string;
        current?: string;
      }>;
    };
  }>;

  /**
   * 知识库索引
   */
  knowledgeBase?: {
    /**
     * 文档索引
     */
    index: {
      totalDocuments: number;
      categoriesCount: number;
      tagsCount: number;

      /**
       * 分类统计
       */
      categories: Array<{
        name: string;
        count: number;
        documents: string[];        // 文档ID列表
      }>;

      /**
       * 标签云
       */
      tags: Array<{
        name: string;
        count: number;
        relevance: number;          // 0-1
      }>;
    };

    /**
     * 搜索配置
     */
    search?: {
      engine: 'algolia' | 'elasticsearch';
      indexed: boolean;
      indexName?: string;
      searchUrl?: string;
    };

    /**
     * AI助手状态
     */
    aiAssistant?: {
      enabled: boolean;
      model: string;
      knowledgeBaseSize: number;    // Token数
      sampleQuestions: string[];    // 示例问题
    };

    /**
     * 文档地图
     */
    sitemap?: {
      url?: string;                 // "https://docs.company.com/sitemap.xml"
      lastUpdated: string;
      structure: Array<{
        section: string;
        url: string;
        children?: Array<{
          title: string;
          url: string;
        }>;
      }>;
    };
  };

  /**
   * 同步结果
   */
  syncResults?: Array<{
    platform: 'notion' | 'confluence' | 'github-wiki';
    status: 'success' | 'failed' | 'partial';

    /**
     * 同步详情
     */
    details: {
      documentsSync: number;
      imagesSync?: number;
      url?: string;                 // 同步后的访问URL
      pageId?: string;              // Notion page ID / Confluence page ID
    };

    error?: {
      code: string;
      message: string;
      failedDocuments?: string[];
    };

    timestamp: string;
  }>;

  /**
   * 质量检查
   */
  qualityCheck?: {
    score: number;                  // 0-100

    /**
     * 检查项
     */
    checks: Array<{
      name: string;
      passed: boolean;
      severity: 'error' | 'warning' | 'info';
      message: string;
    }>;

    /**
     * 常见问题
     */
    issues?: Array<{
      type: 'broken-link' | 'missing-example' | 'outdated-code' | 'incomplete-section';
      location: string;             // 文档位置
      description: string;
      suggestion?: string;
    }>;

    /**
     * 文档覆盖率
     */
    coverage?: {
      apiEndpoints?: {
        total: number;
        documented: number;
        percentage: number;
      };
      functions?: {
        total: number;
        documented: number;
        percentage: number;
      };
      classes?: {
        total: number;
        documented: number;
        percentage: number;
      };
    };
  };

  /**
   * 可操作建议
   */
  recommendations: Array<{
    type: 'improvement' | 'warning' | 'info';
    priority: 'critical' | 'high' | 'medium' | 'low';
    target: 'developer' | 'tech-writer' | 'devops';
    title: string;
    description: string;

    actionable?: {
      steps: string[];
      estimatedEffort: 'trivial' | 'easy' | 'moderate' | 'hard';
    };
  }>;

  /**
   * 生成的文件清单
   */
  files: Array<{
    path: string;
    type: 'markdown' | 'html' | 'pdf' | 'image' | 'config';
    size: number;                   // bytes
    url?: string;                   // 如果已发布
  }>;

  /**
   * 元数据
   */
  metadata: {
    generatedAt: string;
    version: string;
    generator: string;              // "knowledge-manager v2.0.0"
    sourceHash?: string;            // Git commit hash
  };
}

/**
 * 文档元数据
 */
interface DocumentMetadata {
  title: string;
  version: string;
  authors: string[];
  tags: string[];
  category: string;
  createdAt: string;
  updatedAt: string;
  reviewedBy?: string[];
  approvedBy?: string[];
}

/**
 * 架构组件
 */
interface ArchitectureComponent {
  id: string;
  name: string;
  type: 'service' | 'database' | 'cache' | 'queue' | 'external-api' | 'frontend';
  technology?: string;
  description?: string;
  responsibilities?: string[];
  interfaces?: Array<{
    protocol: string;
    endpoint?: string;
  }>;
}

/**
 * 故障场景
 */
interface IncidentScenario {
  name: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  symptoms: string[];
  rootCause?: string;
  mitigationSteps: string[];
  permanentFix?: string;
  preventionMeasures?: string[];
}
```

---

## Usage Examples

### Example 1: API文档自动生成 (OpenAPI → Comprehensive Docs)

**场景**: 从TypeScript Express后端代码和OpenAPI规范自动生成完整API文档，包含请求/响应示例、错误处理和多语言SDK示例

**输入**:
```typescript
const input: KnowledgeManagerInput = {
  task: {
    type: 'api-docs',
    description: '为E-commerce API生成完整文档，包含身份验证、限流、错误处理'
  },

  sources: {
    codebase: {
      path: 'src/api',
      language: 'typescript',
      gitRepo: 'https://github.com/company/ecommerce-api',
      branch: 'main'
    },

    openApiSpec: {
      path: 'openapi.yaml',
      version: '3.1'
    }
  },

  docConfig: {
    outputFormat: {
      primary: 'markdown',
      includeTOC: true,
      includeIndex: true,
      codeHighlighting: true
    },

    structure: {
      sections: [
        'overview',
        'installation',
        'api-reference',
        'troubleshooting',
        'faq',
        'changelog'
      ],
      maxDepth: 4,
      includeDiagrams: true
    },

    apiDocs: {
      includeExamples: true,
      includeErrorCodes: true,
      authenticationDoc: true,
      rateLimitDoc: true,
      generateSDK: true,
      languages: ['curl', 'python', 'javascript', 'go']
    }
  },

  sync: {
    targets: [
      {
        platform: 'github-wiki',
        githubWiki: {
          repo: 'company/ecommerce-api',
          token: process.env.GITHUB_TOKEN,
          branch: 'main'
        }
      },
      {
        platform: 'confluence',
        confluence: {
          baseUrl: 'https://company.atlassian.net',
          username: 'docs-bot@company.com',
          apiToken: process.env.CONFLUENCE_TOKEN,
          spaceKey: 'API',
          parentPageId: '12345678'
        }
      }
    ],

    strategy: {
      mode: 'on-commit',
      conflictResolution: 'overwrite',
      versionControl: true
    }
  },

  knowledgeBase: {
    search: {
      engine: 'algolia',
      algolia: {
        appId: process.env.ALGOLIA_APP_ID,
        apiKey: process.env.ALGOLIA_API_KEY,
        indexName: 'api-docs'
      }
    },

    taxonomy: {
      tags: ['rest-api', 'authentication', 'payments', 'orders', 'users'],
      categories: ['api-reference', 'guides', 'tutorials'],
      autoTag: true
    },

    aiAssistant: {
      enabled: true,
      model: 'claude',
      capabilities: ['qa', 'code-search', 'doc-recommendation'],
      contextWindow: 100000
    }
  },

  output: {
    directory: 'docs/api',
    staticSite: {
      generator: 'docusaurus',
      theme: 'classic',
      deploy: {
        platform: 'vercel',
        url: 'https://api-docs.company.com'
      }
    }
  }
};
```

**输出**:
```typescript
const output: KnowledgeManagerOutput = {
  summary: {
    taskType: 'api-docs',
    documentsGenerated: 18,
    diagramsGenerated: 3,
    totalPages: 142,
    executionTime: 8500
  },

  documents: [
    {
      id: 'api-overview',
      title: 'E-commerce API Overview',
      type: 'guide',

      content: {
        markdown: `# E-commerce API Documentation

## Overview

The E-commerce API provides a comprehensive RESTful interface for managing products, orders, payments, and users. Built with TypeScript and Express, supporting 10,000+ requests/second.

**Base URL**: \`https://api.company.com/v1\`
**API Version**: 2.3.0
**Protocol**: HTTPS only
**Authentication**: OAuth 2.0 + API Keys

## Key Features

✅ **Product Catalog**: 500K+ SKUs with real-time inventory
✅ **Order Management**: Multi-currency, multi-payment gateway
✅ **User Authentication**: OAuth 2.0 (Google, GitHub), JWT tokens
✅ **Webhooks**: Real-time events for order/payment updates
✅ **Rate Limiting**: 1000 requests/hour (free tier), 10,000 (pro tier)

## Quick Start

### 1. Get API Key

Sign up at [https://portal.company.com](https://portal.company.com) and generate an API key.

### 2. Make Your First Request

\`\`\`bash
curl https://api.company.com/v1/products \\
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

### 3. Response

\`\`\`json
{
  "products": [
    {
      "id": "prod_123",
      "name": "Wireless Mouse",
      "price": 29.99,
      "currency": "USD",
      "in_stock": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 500000
  }
}
\`\`\`

## Architecture

\`\`\`mermaid
graph TD
    A[Client] -->|HTTPS| B[API Gateway]
    B --> C[Auth Service]
    B --> D[Product Service]
    B --> E[Order Service]
    D --> F[PostgreSQL]
    E --> F
    E --> G[Payment Gateway]
    E --> H[Redis Cache]
\`\`\`

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products | List products |
| POST | /orders | Create order |
| GET | /orders/:id | Get order details |
| POST | /payments | Process payment |
| GET | /users/me | Get current user |

**See full API reference →** [API Reference](./api-reference.md)`,

        html: '<html>...</html>',
        pdf: 'docs/api/API_Overview.pdf'
      },

      metadata: {
        version: '2.3.0',
        createdAt: '2025-12-12T10:00:00Z',
        updatedAt: '2025-12-12T10:05:00Z',
        authors: ['docs-bot', 'engineering-team'],
        tags: ['overview', 'getting-started', 'rest-api'],
        wordCount: 1250,
        estimatedReadTime: 5
      },

      structure: {
        sections: [
          { id: 's1', title: 'Overview', level: 2, anchor: '#overview', wordCount: 180 },
          { id: 's2', title: 'Key Features', level: 2, anchor: '#key-features', wordCount: 120 },
          { id: 's3', title: 'Quick Start', level: 2, anchor: '#quick-start', wordCount: 250 },
          { id: 's4', title: 'Architecture', level: 2, anchor: '#architecture', wordCount: 100 },
          { id: 's5', title: 'API Endpoints Summary', level: 2, anchor: '#api-endpoints-summary', wordCount: 80 }
        ],
        toc: `## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
  - [1. Get API Key](#1-get-api-key)
  - [2. Make Your First Request](#2-make-your-first-request)
- [Architecture](#architecture)
- [API Endpoints Summary](#api-endpoints-summary)`
      },

      assets: {
        diagrams: [
          {
            type: 'dataflow',
            title: 'API Architecture',
            format: 'mermaid',
            url: 'assets/architecture.svg',
            description: 'High-level system architecture'
          }
        ]
      }
    },

    {
      id: 'api-products-endpoint',
      title: 'Products API Reference',
      type: 'api-docs',

      content: {
        markdown: `# Products API

## GET /v1/products

List all products with filtering, sorting, and pagination.

### Authentication

Required: **API Key** or **OAuth 2.0**

\`\`\`
Authorization: Bearer YOUR_API_KEY
\`\`\`

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | No | Filter by category ID |
| min_price | number | No | Minimum price |
| max_price | number | No | Maximum price |
| in_stock | boolean | No | Only in-stock items |
| sort | string | No | Sort field (\`price\`, \`name\`, \`created_at\`) |
| order | string | No | \`asc\` or \`desc\` (default: asc) |
| page | number | No | Page number (default: 1) |
| per_page | number | No | Items per page (max: 100, default: 20) |

### Request Examples

**cURL**:
\`\`\`bash
curl "https://api.company.com/v1/products?category=electronics&min_price=10&max_price=100&sort=price&order=asc" \\
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

**Python**:
\`\`\`python
import requests

headers = {"Authorization": "Bearer YOUR_API_KEY"}
params = {
    "category": "electronics",
    "min_price": 10,
    "max_price": 100,
    "sort": "price",
    "order": "asc"
}

response = requests.get(
    "https://api.company.com/v1/products",
    headers=headers,
    params=params
)

products = response.json()
print(f"Found {len(products['products'])} products")
\`\`\`

**JavaScript**:
\`\`\`javascript
const API_KEY = 'YOUR_API_KEY';

const params = new URLSearchParams({
  category: 'electronics',
  min_price: 10,
  max_price: 100,
  sort: 'price',
  order: 'asc'
});

const response = await fetch(
  \`https://api.company.com/v1/products?\${params}\`,
  {
    headers: {
      'Authorization': \`Bearer \${API_KEY}\`
    }
  }
);

const data = await response.json();
console.log(\`Found \${data.products.length} products\`);
\`\`\`

**Go**:
\`\`\`go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
)

func main() {
    apiKey := "YOUR_API_KEY"
    baseURL := "https://api.company.com/v1/products"

    params := url.Values{}
    params.Add("category", "electronics")
    params.Add("min_price", "10")
    params.Add("max_price", "100")
    params.Add("sort", "price")
    params.Add("order", "asc")

    req, _ := http.NewRequest("GET", baseURL+"?"+params.Encode(), nil)
    req.Header.Set("Authorization", "Bearer "+apiKey)

    client := &http.Client{}
    resp, _ := client.Do(req)
    defer resp.Body.Close()

    var data map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&data)
    fmt.Printf("Found %d products\\n", len(data["products"].([]interface{})))
}
\`\`\`

### Response

**Status**: \`200 OK\`

\`\`\`json
{
  "products": [
    {
      "id": "prod_abc123",
      "name": "Wireless Mouse",
      "description": "Ergonomic wireless mouse with 6 buttons",
      "category": {
        "id": "cat_elec",
        "name": "Electronics"
      },
      "price": 29.99,
      "currency": "USD",
      "in_stock": true,
      "inventory_count": 245,
      "images": [
        "https://cdn.company.com/products/abc123/main.jpg",
        "https://cdn.company.com/products/abc123/thumb.jpg"
      ],
      "attributes": {
        "brand": "TechCo",
        "color": "Black",
        "wireless": true,
        "battery_type": "AA"
      },
      "created_at": "2025-11-15T08:30:00Z",
      "updated_at": "2025-12-10T14:22:00Z"
    },
    {
      "id": "prod_def456",
      "name": "USB Cable",
      "description": "USB-C to USB-A cable, 6ft",
      "category": {
        "id": "cat_elec",
        "name": "Electronics"
      },
      "price": 12.99,
      "currency": "USD",
      "in_stock": true,
      "inventory_count": 1025,
      "images": [
        "https://cdn.company.com/products/def456/main.jpg"
      ],
      "attributes": {
        "brand": "CableCo",
        "length": "6ft",
        "type": "USB-C to USB-A"
      },
      "created_at": "2025-10-20T12:00:00Z",
      "updated_at": "2025-12-08T09:15:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 1542,
    "total_pages": 78,
    "has_next": true,
    "has_prev": false,
    "next_page": 2,
    "prev_page": null
  },
  "filters_applied": {
    "category": "electronics",
    "min_price": 10,
    "max_price": 100
  }
}
\`\`\`

### Error Responses

**400 Bad Request** - Invalid parameters
\`\`\`json
{
  "error": {
    "code": "INVALID_PARAMS",
    "message": "Invalid query parameters",
    "details": {
      "min_price": "Must be a positive number",
      "per_page": "Must be between 1 and 100"
    }
  }
}
\`\`\`

**401 Unauthorized** - Missing or invalid API key
\`\`\`json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or missing API key",
    "details": "Provide a valid API key in Authorization header"
  }
}
\`\`\`

**429 Too Many Requests** - Rate limit exceeded
\`\`\`json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 1000,
      "window": "1 hour",
      "retry_after": 1800
    }
  }
}
\`\`\`

**500 Internal Server Error** - Server error
\`\`\`json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "request_id": "req_xyz789"
  }
}
\`\`\`

### Rate Limiting

- **Free Tier**: 1,000 requests/hour
- **Pro Tier**: 10,000 requests/hour
- **Enterprise**: Custom limits

Rate limit headers:
\`\`\`
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1702393200
\`\`\`

### Caching

Products data is cached for **5 minutes**. Use \`ETag\` and \`If-None-Match\` headers for efficient caching:

\`\`\`bash
curl "https://api.company.com/v1/products" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "If-None-Match: \\"abc123def456\\""
\`\`\`

If data hasn't changed, returns **304 Not Modified**.

### Best Practices

1. **Pagination**: Use \`page\` and \`per_page\` for large result sets
2. **Filtering**: Narrow results with \`category\`, \`min_price\`, \`max_price\`
3. **Caching**: Implement client-side caching with \`ETag\`
4. **Error Handling**: Always check \`error.code\` for specific error types
5. **Rate Limits**: Monitor \`X-RateLimit-Remaining\` header`,

        html: '<html>...</html>'
      },

      metadata: {
        version: '2.3.0',
        createdAt: '2025-12-12T10:01:30Z',
        updatedAt: '2025-12-12T10:01:30Z',
        authors: ['openapi-generator'],
        tags: ['api-reference', 'products', 'rest'],
        wordCount: 2850,
        estimatedReadTime: 11
      },

      structure: {
        sections: [
          { id: 's1', title: 'GET /v1/products', level: 2, anchor: '#get-v1products', wordCount: 50 },
          { id: 's2', title: 'Authentication', level: 3, anchor: '#authentication', wordCount: 20 },
          { id: 's3', title: 'Query Parameters', level: 3, anchor: '#query-parameters', wordCount: 180 },
          { id: 's4', title: 'Request Examples', level: 3, anchor: '#request-examples', wordCount: 850 },
          { id: 's5', title: 'Response', level: 3, anchor: '#response', wordCount: 450 },
          { id: 's6', title: 'Error Responses', level: 3, anchor: '#error-responses', wordCount: 320 },
          { id: 's7', title: 'Rate Limiting', level: 3, anchor: '#rate-limiting', wordCount: 140 },
          { id: 's8', title: 'Caching', level: 3, anchor: '#caching', wordCount: 110 },
          { id: 's9', title: 'Best Practices', level: 3, anchor: '#best-practices', wordCount: 80 }
        ],
        toc: `## Table of Contents

- [GET /v1/products](#get-v1products)
  - [Authentication](#authentication)
  - [Query Parameters](#query-parameters)
  - [Request Examples](#request-examples)
  - [Response](#response)
  - [Error Responses](#error-responses)
  - [Rate Limiting](#rate-limiting)
  - [Caching](#caching)
  - [Best Practices](#best-practices)`
      },

      assets: {
        codeExamples: [
          { language: 'bash', code: 'curl ...', description: 'cURL example' },
          { language: 'python', code: 'import requests...', description: 'Python SDK' },
          { language: 'javascript', code: 'const response = await fetch...', description: 'JavaScript fetch' },
          { language: 'go', code: 'package main...', description: 'Go client' }
        ]
      }
    }

    // ... 16 more documents (Orders API, Payments API, Users API, Webhooks, etc.)
  ],

  architectureDiagrams: [
    {
      type: 'c4-container',
      level: 'medium',

      diagram: {
        mermaidCode: `graph TD
    Client[Client Application] -->|HTTPS| Gateway[API Gateway]
    Gateway --> Auth[Auth Service]
    Gateway --> Products[Product Service]
    Gateway --> Orders[Order Service]
    Gateway --> Payments[Payment Service]

    Products --> DB[(PostgreSQL)]
    Orders --> DB
    Auth --> DB

    Orders --> Cache[Redis Cache]
    Products --> Cache

    Payments --> Stripe[Stripe API]
    Payments --> PayPal[PayPal API]

    Orders --> Queue[RabbitMQ]
    Queue --> EmailWorker[Email Worker]
    Queue --> InventoryWorker[Inventory Worker]`,

        svgUrl: 'assets/diagrams/api-architecture-container.svg',
        pngUrl: 'assets/diagrams/api-architecture-container.png'
      },

      components: [
        {
          id: 'gateway',
          name: 'API Gateway',
          type: 'service',
          technology: 'Kong',
          description: 'Routes requests, handles rate limiting and authentication'
        },
        {
          id: 'products',
          name: 'Product Service',
          type: 'service',
          technology: 'Node.js + Express',
          description: 'Manages product catalog and inventory'
        },
        {
          id: 'orders',
          name: 'Order Service',
          type: 'service',
          technology: 'Node.js + Express',
          description: 'Handles order creation and management'
        },
        {
          id: 'db',
          name: 'PostgreSQL',
          type: 'database',
          technology: 'PostgreSQL 14',
          description: 'Primary relational database'
        },
        {
          id: 'cache',
          name: 'Redis Cache',
          type: 'cache',
          technology: 'Redis 7',
          description: 'Caches product data and sessions'
        }
      ],

      connections: [
        { from: 'gateway', to: 'products', protocol: 'HTTPS', description: 'Product requests' },
        { from: 'gateway', to: 'orders', protocol: 'HTTPS', description: 'Order requests' },
        { from: 'products', to: 'db', protocol: 'TCP', description: 'Query products' },
        { from: 'orders', to: 'db', protocol: 'TCP', description: 'Store orders' },
        { from: 'products', to: 'cache', protocol: 'TCP', description: 'Cache product data' }
      ]
    }
  ],

  knowledgeBase: {
    index: {
      totalDocuments: 18,
      categoriesCount: 3,
      tagsCount: 12,

      categories: [
        {
          name: 'api-reference',
          count: 8,
          documents: ['api-products-endpoint', 'api-orders-endpoint', 'api-payments-endpoint', ...]
        },
        {
          name: 'guides',
          count: 6,
          documents: ['api-overview', 'authentication-guide', 'webhooks-guide', ...]
        },
        {
          name: 'tutorials',
          count: 4,
          documents: ['quick-start', 'advanced-filtering', 'error-handling', ...]
        }
      ],

      tags: [
        { name: 'rest-api', count: 18, relevance: 1.0 },
        { name: 'authentication', count: 8, relevance: 0.85 },
        { name: 'products', count: 6, relevance: 0.75 },
        { name: 'orders', count: 5, relevance: 0.68 },
        { name: 'payments', count: 4, relevance: 0.62 }
      ]
    },

    search: {
      engine: 'algolia',
      indexed: true,
      indexName: 'api-docs',
      searchUrl: 'https://api-docs.company.com/search'
    },

    aiAssistant: {
      enabled: true,
      model: 'claude-3-5-sonnet',
      knowledgeBaseSize: 185000,
      sampleQuestions: [
        "如何认证API请求?",
        "如何创建订单并处理支付?",
        "Rate limiting如何工作?",
        "如何处理webhook事件?",
        "产品搜索支持哪些过滤器?"
      ]
    },

    sitemap: {
      url: 'https://api-docs.company.com/sitemap.xml',
      lastUpdated: '2025-12-12T10:05:00Z',
      structure: [
        {
          section: 'Getting Started',
          url: '/getting-started',
          children: [
            { title: 'Overview', url: '/overview' },
            { title: 'Quick Start', url: '/quick-start' },
            { title: 'Authentication', url: '/authentication' }
          ]
        },
        {
          section: 'API Reference',
          url: '/api-reference',
          children: [
            { title: 'Products', url: '/api/products' },
            { title: 'Orders', url: '/api/orders' },
            { title: 'Payments', url: '/api/payments' },
            { title: 'Users', url: '/api/users' }
          ]
        }
      ]
    }
  },

  syncResults: [
    {
      platform: 'github-wiki',
      status: 'success',
      details: {
        documentsSync: 18,
        imagesSync: 12,
        url: 'https://github.com/company/ecommerce-api/wiki',
        pageId: null
      },
      timestamp: '2025-12-12T10:06:00Z'
    },
    {
      platform: 'confluence',
      status: 'success',
      details: {
        documentsSync: 18,
        imagesSync: 12,
        url: 'https://company.atlassian.net/wiki/spaces/API',
        pageId: '87654321'
      },
      timestamp: '2025-12-12T10:06:30Z'
    }
  ],

  qualityCheck: {
    score: 94,

    checks: [
      {
        name: 'All endpoints documented',
        passed: true,
        severity: 'error',
        message: '12/12 endpoints have complete documentation'
      },
      {
        name: 'Code examples present',
        passed: true,
        severity: 'warning',
        message: 'All endpoints have cURL, Python, JavaScript, Go examples'
      },
      {
        name: 'Error codes documented',
        passed: true,
        severity: 'warning',
        message: 'All possible error codes documented with examples'
      },
      {
        name: 'No broken links',
        passed: false,
        severity: 'warning',
        message: 'Found 2 broken internal links'
      }
    ],

    issues: [
      {
        type: 'broken-link',
        location: 'docs/api/webhooks.md:45',
        description: 'Link to /api/events returns 404',
        suggestion: 'Update link to /api/webhooks/events or create missing page'
      },
      {
        type: 'broken-link',
        location: 'docs/guides/advanced-filtering.md:123',
        description: 'Link to deprecated /v1/search endpoint',
        suggestion: 'Update to new /v1/products?search=query endpoint'
      }
    ],

    coverage: {
      apiEndpoints: {
        total: 12,
        documented: 12,
        percentage: 100
      },
      functions: {
        total: 145,
        documented: 128,
        percentage: 88
      }
    }
  },

  recommendations: [
    {
      type: 'warning',
      priority: 'high',
      target: 'tech-writer',
      title: '修复2个失效链接',
      description: '文档中存在2个失效的内部链接，会影响用户导航体验',
      actionable: {
        steps: [
          '更新 webhooks.md:45 链接到正确的 /api/webhooks/events',
          '更新 advanced-filtering.md:123 使用新的搜索端点',
          '运行链接检查器验证所有链接有效'
        ],
        estimatedEffort: 'trivial'
      }
    },
    {
      type: 'improvement',
      priority: 'medium',
      target: 'developer',
      title: '提升代码文档覆盖率到95%',
      description: '当前函数文档覆盖率88%，建议提升到95%以改善自动化文档生成质量',
      actionable: {
        steps: [
          '识别缺少JSDoc的17个函数',
          '添加标准JSDoc注释（@param, @returns, @example）',
          '重新生成API文档验证改进'
        ],
        estimatedEffort: 'easy'
      }
    },
    {
      type: 'info',
      priority: 'low',
      target: 'tech-writer',
      title: '添加更多教程和用例',
      description: '当前有4个教程，建议增加到8-10个覆盖常见集成场景',
      actionable: {
        steps: [
          '添加教程：\"批量导入产品\"',
          '添加教程：\"实现购物车功能\"',
          '添加教程：\"集成Stripe支付\"',
          '添加教程：\"处理Webhook事件\"'
        ],
        estimatedEffort: 'moderate'
      }
    }
  ],

  files: [
    { path: 'docs/api/overview.md', type: 'markdown', size: 12580, url: 'https://api-docs.company.com/overview' },
    { path: 'docs/api/products.md', type: 'markdown', size: 28450, url: 'https://api-docs.company.com/api/products' },
    { path: 'docs/api/orders.md', type: 'markdown', size: 31200, url: 'https://api-docs.company.com/api/orders' },
    { path: 'docs/assets/architecture-container.svg', type: 'image', size: 45120, url: 'https://api-docs.company.com/assets/architecture-container.svg' },
    // ... 40 more files
  ],

  metadata: {
    generatedAt: '2025-12-12T10:05:30Z',
    version: '2.3.0',
    generator: 'knowledge-manager v2.0.0',
    sourceHash: 'abc123def456'
  }
};
```

**效果**:
- **文档覆盖**: 12/12 API endpoints完整文档化
- **代码示例**: 4种语言(cURL, Python, JavaScript, Go)×12端点=48个示例
- **同步成功**: GitHub Wiki + Confluence自动发布
- **搜索优化**: Algolia索引18篇文档，支持全文搜索
- **AI助手**: Claude可回答"如何认证?"等5类常见问题
- **质量评分**: 94/100，仅2个失效链接需修复

---

### Example 2: 架构图自动生成 (Code → C4 Model Diagrams)

**场景**: 从微服务代码库自动分析生成C4 Model多层级架构图，包括System Context、Container、Component三层视图

**输入**:
```typescript
const input: KnowledgeManagerInput = {
  task: {
    type: 'architecture',
    description: '为微服务电商系统生成C4 Model架构图，展示系统上下文、容器和关键组件'
  },

  sources: {
    codebase: {
      path: 'services/',
      gitRepo: 'https://github.com/company/ecommerce-microservices',
      branch: 'main',
      language: 'typescript'
    },

    configs: [
      { type: 'kubernetes', path: 'k8s/*.yaml' },
      { type: 'docker-compose', path: 'docker-compose.yml' },
      { type: 'helm', path: 'helm/values.yaml' }
    ]
  },

  docConfig: {
    outputFormat: {
      primary: 'markdown',
      includeTOC: true,
      codeHighlighting: true
    },

    architecture: {
      diagramTypes: ['c4-system', 'c4-container', 'c4-component', 'sequence', 'dataflow'],
      detailLevel: 'detailed',
      includeExternalSystems: true,
      technologyStack: true
    }
  },

  output: {
    directory: 'docs/architecture',
    filename: 'ARCHITECTURE.md'
  }
};
```

**输出**:
```typescript
const output: KnowledgeManagerOutput = {
  summary: {
    taskType: 'architecture',
    documentsGenerated: 1,
    diagramsGenerated: 5,
    totalPages: 45,
    executionTime: 12500
  },

  documents: [
    {
      id: 'architecture-overview',
      title: 'E-commerce Platform Architecture',
      type: 'architecture',

      content: {
        markdown: `# E-commerce Platform Architecture

## System Overview

High-performance microservices架构电商平台，支持100,000+ concurrent users，99.99% uptime SLA。

**技术栈**:
- **Backend**: Node.js + TypeScript, Python (ML服务)
- **Databases**: PostgreSQL (主数据), MongoDB (产品目录), Redis (缓存)
- **Message Queue**: RabbitMQ
- **Infrastructure**: Kubernetes, Docker, Helm
- **Observability**: Prometheus + Grafana, Jaeger tracing

## C4 Level 1: System Context

\`\`\`mermaid
graph TB
    Customer[Customer<br/>使用Web/Mobile购物]
    Admin[Admin<br/>管理产品和订单]

    System[E-commerce Platform<br/>在线购物平台]

    Stripe[Stripe<br/>支付处理]
    PayPal[PayPal<br/>替代支付]
    Email[SendGrid<br/>邮件服务]
    SMS[Twilio<br/>短信通知]
    Analytics[Google Analytics<br/>用户分析]

    Customer -->|浏览产品、下单| System
    Admin -->|管理后台| System

    System -->|处理支付| Stripe
    System -->|处理支付| PayPal
    System -->|发送订单确认| Email
    System -->|发送验证码| SMS
    System -->|跟踪用户行为| Analytics
\`\`\`

**外部系统**:
- **Stripe**: 信用卡支付处理（主）
- **PayPal**: 替代支付网关
- **SendGrid**: 事务邮件发送（订单确认、密码重置）
- **Twilio**: SMS短信验证码
- **Google Analytics**: 用户行为跟踪

## C4 Level 2: Container Diagram

\`\`\`mermaid
graph TB
    subgraph "Client Layer"
        Web[Web App<br/>React + TypeScript]
        Mobile[Mobile App<br/>React Native]
        Admin[Admin Portal<br/>React + TypeScript]
    end

    subgraph "API Gateway"
        Gateway[Kong API Gateway<br/>认证、限流、路由]
    end

    subgraph "Microservices"
        Auth[Auth Service<br/>Node.js<br/>JWT认证]
        Products[Product Service<br/>Node.js<br/>产品目录]
        Orders[Order Service<br/>Node.js<br/>订单管理]
        Payments[Payment Service<br/>Node.js<br/>支付处理]
        Users[User Service<br/>Node.js<br/>用户管理]
        Recommendations[Recommendation Service<br/>Python<br/>ML推荐]
        Search[Search Service<br/>Node.js<br/>Elasticsearch]
    end

    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL<br/>用户、订单、支付)]
        MongoDB[(MongoDB<br/>产品目录)]
        Redis[(Redis<br/>会话、缓存)]
        ES[(Elasticsearch<br/>搜索索引)]
    end

    subgraph "Message Queue"
        RabbitMQ[RabbitMQ<br/>异步任务]
        EmailWorker[Email Worker<br/>邮件发送]
        InventoryWorker[Inventory Worker<br/>库存更新]
    end

    Web -->|HTTPS| Gateway
    Mobile -->|HTTPS| Gateway
    Admin -->|HTTPS| Gateway

    Gateway --> Auth
    Gateway --> Products
    Gateway --> Orders
    Gateway --> Payments
    Gateway --> Users
    Gateway --> Recommendations
    Gateway --> Search

    Auth --> PostgreSQL
    Users --> PostgreSQL
    Orders --> PostgreSQL
    Payments --> PostgreSQL

    Products --> MongoDB

    Auth --> Redis
    Products --> Redis
    Orders --> Redis

    Search --> ES

    Orders --> RabbitMQ
    Payments --> RabbitMQ
    RabbitMQ --> EmailWorker
    RabbitMQ --> InventoryWorker

    Recommendations -->|Python gRPC| Products

    Payments -->|HTTPS| Stripe[Stripe API]
    Payments -->|HTTPS| PayPal[PayPal API]
    EmailWorker -->|HTTPS| SendGrid[SendGrid API]
\`\`\`

**Container清单**:

| Container | Technology | Responsibility |
|-----------|------------|----------------|
| Web App | React 18 + TypeScript | 用户前端（浏览、购物车、结账） |
| Mobile App | React Native | iOS/Android应用 |
| Admin Portal | React 18 + Ant Design | 管理后台（产品、订单、用户） |
| Kong Gateway | Kong 3.x | API网关（认证、限流、路由） |
| Auth Service | Node.js + Express | JWT认证、OAuth 2.0 |
| Product Service | Node.js + Express | 产品CRUD、库存管理 |
| Order Service | Node.js + Express | 订单生命周期管理 |
| Payment Service | Node.js + Express | Stripe/PayPal集成 |
| Recommendation Service | Python + FastAPI | ML产品推荐 |
| PostgreSQL | PostgreSQL 14 | 事务数据（用户、订单） |
| MongoDB | MongoDB 6 | 产品目录（非结构化） |
| Redis | Redis 7 | 会话缓存、产品缓存 |
| RabbitMQ | RabbitMQ 3.11 | 异步任务队列 |
| Elasticsearch | ES 8.x | 全文搜索、日志 |

## C4 Level 3: Component Diagram (Order Service)

\`\`\`mermaid
graph TB
    subgraph "Order Service"
        API[REST API Controller<br/>Express路由]

        subgraph "Business Logic"
            OrderMgr[Order Manager<br/>订单CRUD]
            CheckoutMgr[Checkout Manager<br/>结账流程]
            Validator[Order Validator<br/>数据验证]
        end

        subgraph "Integration"
            ProductClient[Product Client<br/>产品库存检查]
            PaymentClient[Payment Client<br/>支付调用]
            EventPublisher[Event Publisher<br/>RabbitMQ]
        end

        subgraph "Data Access"
            OrderRepo[Order Repository<br/>PostgreSQL ORM]
            CacheRepo[Cache Repository<br/>Redis]
        end
    end

    API --> OrderMgr
    API --> CheckoutMgr

    OrderMgr --> Validator
    CheckoutMgr --> Validator

    CheckoutMgr --> ProductClient
    CheckoutMgr --> PaymentClient
    CheckoutMgr --> EventPublisher

    OrderMgr --> OrderRepo
    OrderMgr --> CacheRepo
    CheckoutMgr --> OrderRepo

    ProductClient -->|gRPC| ProductService[Product Service]
    PaymentClient -->|HTTP| PaymentService[Payment Service]
    EventPublisher -->|AMQP| RabbitMQ

    OrderRepo -->|SQL| PostgreSQL
    CacheRepo -->|TCP| Redis
\`\`\`

**组件职责**:
- **API Controller**: HTTP请求处理、路由、请求/响应格式化
- **Order Manager**: 订单CRUD操作、状态机管理
- **Checkout Manager**: 结账流程编排（库存检查→支付→订单创建→发送邮件）
- **Validator**: 输入验证、业务规则检查
- **Product Client**: 调用Product Service检查库存
- **Payment Client**: 调用Payment Service处理支付
- **Event Publisher**: 发布订单事件到RabbitMQ（order.created, order.completed）
- **Order Repository**: PostgreSQL数据访问（Prisma ORM）
- **Cache Repository**: Redis缓存访问（订单缓存5分钟）

## Sequence Diagram: 结账流程

\`\`\`mermaid
sequenceDiagram
    participant User
    participant Web
    participant Gateway
    participant Order
    participant Product
    participant Payment
    participant RabbitMQ
    participant Email

    User->>Web: 点击\"Place Order\"
    Web->>Gateway: POST /orders/checkout
    Gateway->>Order: 转发请求

    Order->>Product: GET /products/check-stock
    Product-->>Order: 库存充足

    Order->>Payment: POST /payments/charge
    Payment->>Stripe: Charge credit card
    Stripe-->>Payment: Payment successful
    Payment-->>Order: transaction_id

    Order->>Order: 创建订单记录
    Order->>RabbitMQ: Publish order.created
    RabbitMQ->>Email: 触发邮件发送
    Email->>User: 发送订单确认邮件

    Order-->>Gateway: 200 OK + order_id
    Gateway-->>Web: 订单详情
    Web->>User: 显示成功页面
\`\`\`

## Data Flow Diagram: 订单处理

\`\`\`mermaid
graph LR
    A[用户提交订单] --> B[Order Service]
    B --> C{检查库存}
    C -->|库存充足| D[锁定库存]
    C -->|库存不足| E[返回错误]

    D --> F{处理支付}
    F -->|成功| G[创建订单]
    F -->|失败| H[释放库存]

    G --> I[发布事件]
    I --> J[发送邮件]
    I --> K[更新库存]
    I --> L[更新推荐]

    H --> E
\`\`\`

## Deployment Architecture

**Kubernetes集群配置**:
\`\`\`yaml
# 3-zone高可用部署
Zones: us-west-2a, us-west-2b, us-west-2c

# Node池配置
- general-pool: 10x n2-standard-8 (8 vCPU, 32GB RAM)
- compute-pool: 5x c2-standard-16 (16 vCPU, 64GB RAM) # 推荐服务
- database-pool: 3x n2-highmem-8 (8 vCPU, 64GB RAM)  # 数据库节点

# 服务副本数
auth-service: 3 replicas
product-service: 5 replicas
order-service: 5 replicas
payment-service: 4 replicas
recommendation-service: 2 replicas
\`\`\`

## Technology Stack Details

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Node.js | 20.x LTS | 微服务运行时 |
| Language | TypeScript | 5.x | 类型安全 |
| ML Runtime | Python | 3.11 | 推荐服务 |
| API Framework | Express.js | 4.18 | REST API |
| ML Framework | FastAPI | 0.104 | Python API |
| ORM | Prisma | 5.x | 数据库访问 |
| Database | PostgreSQL | 14.x | 事务数据 |
| Database | MongoDB | 6.x | 文档存储 |
| Cache | Redis | 7.x | 内存缓存 |
| Search | Elasticsearch | 8.x | 全文搜索 |
| Queue | RabbitMQ | 3.11 | 消息队列 |
| API Gateway | Kong | 3.x | 网关 |
| Container | Docker | 24.x | 容器化 |
| Orchestration | Kubernetes | 1.28 | 编排 |
| Package Manager | Helm | 3.x | K8s打包 |
| Monitoring | Prometheus | 2.x | 指标收集 |
| Visualization | Grafana | 10.x | 监控面板 |
| Tracing | Jaeger | 1.50 | 分布式跟踪 |
| Logging | Loki | 2.9 | 日志聚合 |

## Performance Characteristics

**容量**:
- **Concurrent Users**: 100,000+
- **Request Rate**: 50,000 req/s (峰值), 10,000 req/s (平均)
- **Database**: PostgreSQL 3TB, MongoDB 5TB
- **Cache Hit Rate**: 92% (产品缓存)

**延迟**（P95）:
- **Product Listing**: <150ms
- **Checkout**: <500ms
- **Payment Processing**: <800ms
- **Search**: <100ms

**可用性**:
- **SLA**: 99.99% (允许每月52.6分钟down time)
- **Actual Uptime**: 99.995%（2024年数据）

## Security

**认证与授权**:
- OAuth 2.0 + JWT tokens (15分钟过期)
- API Key for service-to-service
- RBAC (Role-Based Access Control)

**数据安全**:
- TLS 1.3 for all external communication
- Database encryption at rest (AES-256)
- PCI DSS Level 1 compliance (支付数据)

**网络安全**:
- WAF (Web Application Firewall) via Cloudflare
- DDoS protection
- IP whitelisting for admin portal

## Disaster Recovery

**备份策略**:
- PostgreSQL: 每日全量 + 每小时增量
- MongoDB: 每日全量快照
- Redis: AOF persistence + 每小时RDB快照

**RPO/RTO**:
- **RPO** (Recovery Point Objective): 1小时
- **RTO** (Recovery Time Objective): 4小时

**故障转移**:
- Multi-zone deployment（3可用区）
- Auto-scaling (CPU>70% → +2 replicas)
- Database failover (<30秒)`,

        html: '<html>...</html>'
      },

      metadata: {
        version: '1.0.0',
        createdAt: '2025-12-12T11:00:00Z',
        updatedAt: '2025-12-12T11:00:00Z',
        authors: ['architecture-analyzer'],
        tags: ['architecture', 'c4-model', 'microservices', 'kubernetes'],
        wordCount: 4200,
        estimatedReadTime: 17
      },

      structure: {
        sections: [
          { id: 's1', title: 'System Overview', level: 2, anchor: '#system-overview', wordCount: 120 },
          { id: 's2', title: 'C4 Level 1: System Context', level: 2, anchor: '#c4-level-1-system-context', wordCount: 250 },
          { id: 's3', title: 'C4 Level 2: Container Diagram', level: 2, anchor: '#c4-level-2-container-diagram', wordCount: 850 },
          { id: 's4', title: 'C4 Level 3: Component Diagram', level: 2, anchor: '#c4-level-3-component-diagram', wordCount: 680 },
          { id: 's5', title: 'Sequence Diagram', level: 2, anchor: '#sequence-diagram', wordCount: 320 },
          { id: 's6', title: 'Data Flow Diagram', level: 2, anchor: '#data-flow-diagram', wordCount: 180 },
          { id: 's7', title: 'Deployment Architecture', level: 2, anchor: '#deployment-architecture', wordCount: 420 },
          { id: 's8', title: 'Technology Stack Details', level: 2, anchor: '#technology-stack-details', wordCount: 550 },
          { id: 's9', title: 'Performance Characteristics', level: 2, anchor: '#performance-characteristics', wordCount: 280 },
          { id: 's10', title: 'Security', level: 2, anchor: '#security', wordCount: 240 },
          { id: 's11', title: 'Disaster Recovery', level: 2, anchor: '#disaster-recovery', wordCount: 310 }
        ],
        toc: `## Table of Contents

- [System Overview](#system-overview)
- [C4 Level 1: System Context](#c4-level-1-system-context)
- [C4 Level 2: Container Diagram](#c4-level-2-container-diagram)
- [C4 Level 3: Component Diagram (Order Service)](#c4-level-3-component-diagram-order-service)
- [Sequence Diagram: 结账流程](#sequence-diagram)
- [Data Flow Diagram: 订单处理](#data-flow-diagram)
- [Deployment Architecture](#deployment-architecture)
- [Technology Stack Details](#technology-stack-details)
- [Performance Characteristics](#performance-characteristics)
- [Security](#security)
- [Disaster Recovery](#disaster-recovery)`
      },

      assets: {
        diagrams: [
          { type: 'c4', title: 'System Context Diagram', format: 'mermaid', url: 'assets/c4-system-context.svg' },
          { type: 'c4', title: 'Container Diagram', format: 'mermaid', url: 'assets/c4-container.svg' },
          { type: 'c4', title: 'Component Diagram - Order Service', format: 'mermaid', url: 'assets/c4-component-order.svg' },
          { type: 'sequence', title: 'Checkout Sequence', format: 'mermaid', url: 'assets/sequence-checkout.svg' },
          { type: 'dataflow', title: 'Order Processing Data Flow', format: 'mermaid', url: 'assets/dataflow-order.svg' }
        ]
      }
    }
  ],

  architectureDiagrams: [
    {
      type: 'c4-system',
      level: 'high-level',

      diagram: {
        mermaidCode: `graph TB
    Customer[Customer] --> System[E-commerce Platform]
    Admin[Admin] --> System
    System --> Stripe[Stripe]
    System --> PayPal[PayPal]
    System --> Email[SendGrid]
    System --> SMS[Twilio]
    System --> Analytics[Google Analytics]`,
        svgUrl: 'assets/c4-system-context.svg'
      },

      components: [
        { id: 'customer', name: 'Customer', type: 'external-api', description: '终端用户' },
        { id: 'system', name: 'E-commerce Platform', type: 'service', description: '电商平台主系统' },
        { id: 'stripe', name: 'Stripe', type: 'external-api', technology: 'Payment Gateway', description: '支付处理' }
      ],

      connections: [
        { from: 'customer', to: 'system', protocol: 'HTTPS', description: '浏览产品、下单' },
        { from: 'system', to: 'stripe', protocol: 'HTTPS', description: '处理支付' }
      ]
    },

    {
      type: 'c4-container',
      level: 'medium',

      diagram: {
        mermaidCode: `graph TB
    Web[Web App] --> Gateway[Kong Gateway]
    Gateway --> Auth[Auth Service]
    Gateway --> Products[Product Service]
    Gateway --> Orders[Order Service]
    Auth --> PostgreSQL[(PostgreSQL)]
    Products --> MongoDB[(MongoDB)]
    Orders --> PostgreSQL`,
        svgUrl: 'assets/c4-container.svg'
      },

      components: [
        { id: 'web', name: 'Web App', type: 'service', technology: 'React 18', description: '用户前端' },
        { id: 'gateway', name: 'Kong Gateway', type: 'service', technology: 'Kong 3.x', description: 'API网关' },
        { id: 'auth', name: 'Auth Service', type: 'service', technology: 'Node.js', description: 'JWT认证' },
        { id: 'products', name: 'Product Service', type: 'service', technology: 'Node.js', description: '产品目录' },
        { id: 'orders', name: 'Order Service', type: 'service', technology: 'Node.js', description: '订单管理' },
        { id: 'postgres', name: 'PostgreSQL', type: 'database', technology: 'PostgreSQL 14', description: '事务数据' },
        { id: 'mongo', name: 'MongoDB', type: 'database', technology: 'MongoDB 6', description: '产品目录' }
      ],

      connections: [
        { from: 'web', to: 'gateway', protocol: 'HTTPS', description: 'API请求' },
        { from: 'gateway', to: 'auth', protocol: 'HTTP', description: '认证请求' },
        { from: 'gateway', to: 'products', protocol: 'HTTP', description: '产品查询' },
        { from: 'auth', to: 'postgres', protocol: 'TCP', description: '用户数据' },
        { from: 'products', to: 'mongo', protocol: 'TCP', description: '产品数据' }
      ]
    },

    {
      type: 'c4-component',
      level: 'detailed',

      diagram: {
        mermaidCode: `graph TB
    API[REST API Controller] --> OrderMgr[Order Manager]
    API --> CheckoutMgr[Checkout Manager]
    CheckoutMgr --> ProductClient[Product Client]
    CheckoutMgr --> PaymentClient[Payment Client]
    OrderMgr --> OrderRepo[Order Repository]
    OrderRepo --> PostgreSQL[(PostgreSQL)]`,
        svgUrl: 'assets/c4-component-order.svg'
      },

      components: [
        { id: 'api', name: 'REST API Controller', type: 'service', technology: 'Express.js', description: 'HTTP请求处理' },
        { id: 'ordermgr', name: 'Order Manager', type: 'service', description: '订单CRUD' },
        { id: 'checkoutmgr', name: 'Checkout Manager', type: 'service', description: '结账流程编排' },
        { id: 'productclient', name: 'Product Client', type: 'service', description: '产品库存检查' },
        { id: 'paymentclient', name: 'Payment Client', type: 'service', description: '支付调用' },
        { id: 'orderrepo', name: 'Order Repository', type: 'service', technology: 'Prisma ORM', description: 'PostgreSQL访问' }
      ],

      connections: [
        { from: 'api', to: 'ordermgr', protocol: 'Internal', description: 'CRUD操作' },
        { from: 'api', to: 'checkoutmgr', protocol: 'Internal', description: '结账请求' },
        { from: 'checkoutmgr', to: 'productclient', protocol: 'gRPC', description: '库存检查' },
        { from: 'checkoutmgr', to: 'paymentclient', protocol: 'HTTP', description: '支付处理' },
        { from: 'ordermgr', to: 'orderrepo', protocol: 'Internal', description: '数据访问' }
      ]
    }
  ],

  qualityCheck: {
    score: 98,

    checks: [
      { name: 'All services documented', passed: true, severity: 'error', message: '7/7 微服务已文档化' },
      { name: 'Technology stack complete', passed: true, severity: 'warning', message: '所有技术栈已标注版本' },
      { name: 'Diagrams rendered', passed: true, severity: 'error', message: '5个Mermaid图表成功渲染' },
      { name: 'External systems identified', passed: true, severity: 'warning', message: '5个外部系统已标注' }
    ],

    issues: [],

    coverage: {
      apiEndpoints: { total: 0, documented: 0, percentage: 0 }, // N/A for architecture doc
      functions: { total: 0, documented: 0, percentage: 0 },
      classes: { total: 0, documented: 0, percentage: 0 }
    }
  },

  recommendations: [
    {
      type: 'improvement',
      priority: 'medium',
      target: 'developer',
      title: '添加ADR(Architecture Decision Records)',
      description: '记录关键架构决策（为什么选择微服务、为什么PostgreSQL+MongoDB混合）',
      actionable: {
        steps: [
          '创建docs/adr/目录',
          '编写ADR-001: 为什么选择微服务架构',
          '编写ADR-002: 为什么使用混合数据库策略',
          '编写ADR-003: 为什么选择Kong而非其他网关'
        ],
        estimatedEffort: 'moderate'
      }
    },
    {
      type: 'info',
      priority: 'low',
      target: 'tech-writer',
      title: '添加失败模式分析(Failure Modes)',
      description: '文档化每个服务的失败场景和降级策略',
      actionable: {
        steps: [
          '记录Product Service故障时的降级（返回缓存数据）',
          '记录Payment Service故障时的策略（排队重试）',
          '记录数据库故障时的只读模式'
        ],
        estimatedEffort: 'easy'
      }
    }
  ],

  files: [
    { path: 'docs/architecture/ARCHITECTURE.md', type: 'markdown', size: 42500, url: null },
    { path: 'docs/architecture/assets/c4-system-context.svg', type: 'image', size: 15200 },
    { path: 'docs/architecture/assets/c4-container.svg', type: 'image', size: 38500 },
    { path: 'docs/architecture/assets/c4-component-order.svg', type: 'image', size: 22100 },
    { path: 'docs/architecture/assets/sequence-checkout.svg', type: 'image', size: 18700 },
    { path: 'docs/architecture/assets/dataflow-order.svg', type: 'image', size: 12400 }
  ],

  metadata: {
    generatedAt: '2025-12-12T11:00:30Z',
    version: '1.0.0',
    generator: 'knowledge-manager v2.0.0',
    sourceHash: 'def456ghi789'
  }
};
```

**效果**:
- **多层级视图**: C4 Model 3层(System/Container/Component) + Sequence + Data Flow共5张图
- **技术栈标注**: 所有组件标注具体技术(Node.js 20, PostgreSQL 14, Redis 7等)
- **性能指标**: 延迟、容量、可用性、备份RPO/RTO全部文档化
- **自动生成**: 从Kubernetes YAML和代码推导出架构图，无需手绘
- **质量评分**: 98/100，建议添加ADR和失败模式分析

---

### Example 3: Runbook自动生成 (Incident Data → Troubleshooting Guide)

**场景**: 从历史事故报告和运维数据生成结构化Runbook，包含症状识别、排查步骤、临时缓解和永久修复

**输入**:
```typescript
const input: KnowledgeManagerInput = {
  task: {
    type: 'runbook',
    description: '为支付服务生成故障排查Runbook，覆盖常见高频事故场景'
  },

  sources: {
    codebase: {
      path: 'services/payment-service',
      language: 'typescript',
      branch: 'main'
    },

    configs: [
      { type: 'kubernetes', path: 'k8s/payment-service/*.yaml' }
    ],

    opsData: {
      incidentReports: [
        'incidents/2025-01-15-payment-gateway-timeout.md',
        'incidents/2025-01-20-database-connection-pool-exhausted.md',
        'incidents/2025-02-03-stripe-api-rate-limit.md'
      ],
      runbooks: [
        'runbooks/database-recovery.md',
        'runbooks/payment-rollback.md'
      ],
      monitoringDashboards: [
        'https://grafana.company.com/d/payment-service',
        'https://grafana.company.com/d/stripe-integration'
      ]
    }
  },

  docConfig: {
    outputFormat: {
      primary: 'markdown',
      includeTOC: true,
      codeHighlighting: true
    },

    runbook: {
      scenarios: [
        { name: 'Stripe API限流', severity: 'high', frequency: 'occasional' },
        { name: '数据库连接池耗尽', severity: 'critical', frequency: 'rare' },
        { name: '支付失败率>5%', severity: 'high', frequency: 'frequent' }
      ],
      includeMetrics: true,
      includeCommands: true,
      includeRollback: true
    }
  },

  output: {
    directory: 'docs/runbooks',
    filename: 'PAYMENT_SERVICE_RUNBOOK.md'
  }
};
```

**输出（部分）**:
```typescript
const output: KnowledgeManagerOutput = {
  summary: {
    taskType: 'runbook',
    documentsGenerated: 1,
    totalPages: 28,
    executionTime: 6500
  },

  documents: [
    {
      id: 'payment-service-runbook',
      title: 'Payment Service Runbook',
      type: 'runbook',

      content: {
        markdown: `# Payment Service Runbook

## 服务概览

**服务名称**: payment-service
**团队**: Payments Team
**On-call**: #payments-oncall Slack channel
**监控面板**: [Grafana Dashboard](https://grafana.company.com/d/payment-service)

**关键指标**:
- 支付成功率: >99.5%
- P95延迟: <800ms
- 数据库连接池利用率: <80%

---

## 故障场景1: Stripe API限流

### 严重性: HIGH | 频率: Occasional

### 症状

**用户影响**:
- 支付请求返回429错误
- Stripe支付成功率从99.5%下降至70-80%
- 用户看到"Payment processing temporarily unavailable"错误

**监控告警**:
\`\`\`
Alert: stripe_api_rate_limit_errors_high
Condition: rate(stripe_api_429_errors[5m]) > 10
Current: 45 errors/5min
Dashboard: https://grafana.company.com/d/stripe-integration
\`\`\`

**日志特征**:
\`\`\`
ERROR Payment failed: StripeRateLimitError: Too many requests
  status: 429
  type: rate_limit_error
  message: "You have exceeded the API rate limit"
\`\`\`

### 排查步骤

**Step 1: 确认Stripe API状态**
\`\`\`bash
# 检查Stripe服务状态
curl https://status.stripe.com/api/v2/status.json

# 预期输出: "indicator": "none" (无故障)
# 如果有故障: "indicator": "critical" 或 "major"
\`\`\`

**Step 2: 检查当前限流情况**
\`\`\`bash
# 查看最近1小时Stripe API调用量
kubectl exec -it deployment/payment-service -- node
> const metrics = await redis.get('stripe:api:calls:1h')
> console.log(JSON.parse(metrics))

# 输出示例:
{
  "total_calls": 150000,
  "successful": 105000,
  "rate_limited": 45000,  // 🚨 异常高
  "hour": "2025-12-12T10:00:00Z"
}
\`\`\`

**Step 3: 识别请求来源**
\`\`\`bash
# 分析日志查看哪个endpoint触发限流
kubectl logs -l app=payment-service --tail=1000 | grep "429" | awk '{print $8}' | sort | uniq -c | sort -rn

# 输出示例:
# 3200 POST /charges/create
#  800 POST /refunds/create
#  150 GET /payment_intents/:id
\`\`\`

**Checkpoint**: 如果charges/create调用量异常高(>10倍正常值)，可能是无限重试循环或恶意请求

**Step 4: 检查Redis缓存命中率**
\`\`\`bash
# Payment Service使用Redis缓存支付元数据
redis-cli INFO stats | grep keyspace_hits
redis-cli INFO stats | grep keyspace_misses

# 计算命中率
# 预期: >80%
# 如果<50%: 缓存失效导致过多Stripe API调用
\`\`\`

**Step 5: 分析重试逻辑**
\`\`\`bash
# 检查代码中的重试配置
grep -r "maxRetries" services/payment-service/src/

# 预期配置:
# maxRetries: 3
# retryDelay: exponential backoff (1s, 2s, 4s)
\`\`\`

### 临时缓解（5-10分钟）

**Option A: 启用请求队列模式**
\`\`\`bash
# 限制并发Stripe API请求为50/s
kubectl set env deployment/payment-service STRIPE_RATE_LIMIT=50
kubectl set env deployment/payment-service QUEUE_MODE=enabled

# 验证生效
kubectl rollout status deployment/payment-service
kubectl logs -f deployment/payment-service | grep "Queue mode enabled"

# 预期输出:
# "Queue mode enabled, max concurrency: 50"
\`\`\`

**效果**: 支付请求排队处理，延迟增加至1-2秒，但成功率恢复至99%+

**Option B: 增加缓存TTL**
\`\`\`bash
# 将支付元数据缓存从5分钟延长至30分钟
kubectl set env deployment/payment-service CACHE_TTL_SECONDS=1800

# 验证
redis-cli TTL payment:metadata:cust_123
# 输出: 1800 (30分钟)
\`\`\`

**效果**: 减少50-70%的Stripe API调用，缓解限流

**Option C: 临时禁用非关键功能**
\`\`\`bash
# 禁用实时汇率查询（使用缓存值）
kubectl set env deployment/payment-service DISABLE_REALTIME_FX=true

# 禁用支付成功后的即时邮件（改为批量发送）
kubectl set env deployment/payment-service BATCH_EMAIL_MODE=true
\`\`\`

### 永久修复

**Fix 1: 实施智能速率限制**
\`\`\`typescript
// src/integrations/stripe/rateLimiter.ts

import Bottleneck from 'bottleneck';

const stripeLimiter = new Bottleneck({
  reservoir: 100,           // 初始令牌桶100个
  reservoirRefreshAmount: 100,  // 每次刷新100个
  reservoirRefreshInterval: 1000, // 每秒刷新
  maxConcurrent: 50,        // 最大并发50
  minTime: 20,              // 每个请求最小间隔20ms

  // 自适应限流
  trackDoneStatus: true,

  // 遇到429错误时触发
  Events: {
    error: (error) => {
      if (error.statusCode === 429) {
        // 指数退避：暂停5秒
        stripeLimiter.stop({ dropWaitingJobs: false });
        setTimeout(() => stripeLimiter.start(), 5000);
        logger.warn('Stripe rate limit hit, backing off for 5s');
      }
    }
  }
});

// 使用限流器包装Stripe调用
export async function createCharge(params: ChargeParams) {
  return stripeLimiter.schedule(() => stripe.charges.create(params));
}
\`\`\`

**PR**: #1234 "Add intelligent rate limiting for Stripe API"
**预期效果**: 限流错误减少95%，自动退避和恢复

**Fix 2: 优化缓存策略**
\`\`\`typescript
// src/cache/paymentCache.ts

// 🔧 修复前：简单TTL缓存
const paymentMetadata = await redis.get(\`payment:metadata:\${customerId}\`);
if (!paymentMetadata) {
  // 🚨 缓存未命中 → 调用Stripe API
  paymentMetadata = await stripe.customers.retrieve(customerId);
  await redis.setex(\`payment:metadata:\${customerId}\`, 300, JSON.stringify(paymentMetadata));
}

// ✅ 修复后：多层缓存 + Stale-While-Revalidate
async function getPaymentMetadata(customerId: string) {
  const cached = await redis.get(\`payment:metadata:\${customerId}\`);
  const cacheAge = await redis.ttl(\`payment:metadata:\${customerId}\`);

  // Layer 1: 新鲜缓存（TTL剩余>50%）
  if (cached && cacheAge > 900) {
    return JSON.parse(cached);
  }

  // Layer 2: Stale缓存（TTL剩余<50%但>0）
  if (cached && cacheAge > 0) {
    // 后台异步刷新，先返回旧数据
    backgroundRefresh(customerId);
    return JSON.parse(cached);
  }

  // Layer 3: 缓存完全失效
  const fresh = await stripe.customers.retrieve(customerId);
  await redis.setex(\`payment:metadata:\${customerId}\`, 1800, JSON.stringify(fresh));
  return fresh;
}

async function backgroundRefresh(customerId: string) {
  // 异步刷新，不阻塞请求
  setImmediate(async () => {
    try {
      const fresh = await stripe.customers.retrieve(customerId);
      await redis.setex(\`payment:metadata:\${customerId}\`, 1800, JSON.stringify(fresh));
    } catch (error) {
      logger.error('Background refresh failed', error);
    }
  });
}
\`\`\`

**PR**: #1235 "Implement Stale-While-Revalidate caching"
**预期效果**: 缓存命中率从75%提升至92%，Stripe API调用减少60%

**Fix 3: 批量API调用**
\`\`\`typescript
// src/integrations/stripe/batchProcessor.ts

// 🔧 修复前：每个支付单独调用Stripe
for (const payment of payments) {
  await stripe.charges.create({
    amount: payment.amount,
    customer: payment.customerId,
    // ...
  });
}
// 🚨 问题：100个支付 = 100次API调用

// ✅ 修复后：使用Stripe Batch API
async function batchCreateCharges(payments: Payment[]) {
  // 每批50个
  const batches = chunk(payments, 50);

  for (const batch of batches) {
    await stripe.charges.createBatch(
      batch.map(p => ({
        amount: p.amount,
        customer: p.customerId,
        // ...
      }))
    );

    // 批次间延迟100ms
    await sleep(100);
  }
}
// ✅ 改进：100个支付 = 2次API调用（50+50）
\`\`\`

**PR**: #1236 "Use Stripe Batch API for bulk operations"
**预期效果**: 批量操作API调用减少95%

### 回滚计划

**何时回滚**: 如果缓解措施无效超过30分钟，或支付成功率<50%

**回滚步骤**:
\`\`\`bash
# 1. 回滚到上一个稳定版本
kubectl rollout undo deployment/payment-service

# 2. 禁用新功能（如有）
kubectl set env deployment/payment-service FEATURE_XYZ=false

# 3. 清理Redis缓存（重新开始）
redis-cli FLUSHDB

# 4. 验证回滚成功
kubectl rollout status deployment/payment-service
kubectl logs -f deployment/payment-service | grep "Version"
# 预期输出: "Payment Service v2.2.5 started" (非v2.3.0)

# 5. 监控恢复情况
watch -n 5 'curl -s https://grafana.company.com/api/datasources/proxy/1/api/v1/query?query=payment_success_rate | jq'
# 预期: success_rate > 0.995 (99.5%+)
\`\`\`

### 相关监控

**Grafana面板**:
- [Payment Service Overview](https://grafana.company.com/d/payment-service)
- [Stripe Integration Metrics](https://grafana.company.com/d/stripe-integration)
- [Redis Cache Performance](https://grafana.company.com/d/redis-cache)

**告警规则**:
- \`stripe_api_rate_limit_errors_high\`: >10 errors/5min
- \`payment_success_rate_low\`: <99%
- \`stripe_api_latency_high\`: P95 >2s

**关键指标**:
| Metric | Threshold | Current |
|--------|-----------|---------|
| Stripe API成功率 | >99% | 98.2% 🚨 |
| 429错误率 | <1% | 3.5% 🚨 |
| Redis缓存命中率 | >80% | 75% ⚠️ |
| API延迟P95 | <800ms | 1250ms 🚨 |

### Post-Incident Actions

**必做**（48小时内）:
1. ✅ 更新Runbook（添加本次经验）
2. ✅ 编写Post-mortem报告
3. ✅ 实施Fix 1-3（智能限流、缓存优化、批量API）
4. ✅ 增加监控告警灵敏度

**建议**（1周内）:
1. 与Stripe支持联系，申请更高限额
2. 实施Circuit Breaker模式
3. 增加集成测试覆盖限流场景
4. 定期压力测试（每月）

---

## 故障场景2: 数据库连接池耗尽

### 严重性: CRITICAL | 频率: Rare

### 症状

**用户影响**:
- 所有支付请求失败，返回500错误
- 错误消息: "Database connection timeout"
- 服务完全不可用，影响100%用户

**监控告警**:
\`\`\`
Alert: postgresql_connection_pool_exhausted
Condition: pg_stat_activity.count >= max_connections
Current: 100/100 connections in use
\`\`\`

**日志特征**:
\`\`\`
ERROR Database query failed
Error: sorry, too many clients already
  code: '53300'
  severity: 'FATAL'
\`\`\`

### 排查步骤

**Step 1: 确认连接池状态**
\`\`\`bash
# 连接到数据库查看活动连接
kubectl exec -it postgres-0 -- psql -U postgres -d payment_db

SELECT
  count(*) as total_connections,
  count(*) FILTER (WHERE state = 'active') as active,
  count(*) FILTER (WHERE state = 'idle') as idle,
  count(*) FILTER (WHERE state = 'idle in transaction') as idle_in_tx
FROM pg_stat_activity;

# 预期输出:
#  total_connections | active | idle | idle_in_tx
# -------------------+--------+------+------------
#                100 |     85 |   10 |          5
# 🚨 如果idle_in_tx >20%: 连接泄漏
\`\`\`

**Step 2: 识别慢查询**
\`\`\`sql
-- 查看当前运行超过5秒的查询
SELECT
  pid,
  now() - pg_stat_activity.query_start AS duration,
  state,
  query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds'
  AND state != 'idle'
ORDER BY duration DESC;

-- 如果发现长时间运行的查询，可能需要终止
-- SELECT pg_terminate_backend(<pid>);
\`\`\`

**Step 3: 检查应用连接池配置**
\`\`\`bash
# 查看当前Prisma连接池配置
kubectl exec -it deployment/payment-service -- env | grep DATABASE

# 预期输出:
# DATABASE_URL=postgresql://...?connection_limit=20
# 🚨 如果connection_limit过高（>30）: 单个实例占用过多连接
\`\`\`

### 临时缓解（5分钟）

**Option A: 终止空闲事务**
\`\`\`sql
-- 终止所有idle in transaction超过5分钟的连接
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND (now() - state_change) > interval '5 minutes';

-- 释放约10-20个连接
\`\`\`

**Option B: 增加数据库max_connections**
\`\`\`bash
# ⚠️ 临时措施，需重启数据库
kubectl exec -it postgres-0 -- psql -U postgres

ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();

# 验证
SHOW max_connections;
-- 输出: 200
\`\`\`

**风险**: 增加连接数会增加内存使用，确保有足够RAM (每连接~10MB)

**Option C: 减少应用实例**
\`\`\`bash
# 临时缩容到3个实例（减少连接压力）
kubectl scale deployment/payment-service --replicas=3

# 每个实例20连接 × 3实例 = 60连接（低于100上限）
\`\`\`

### 永久修复

**Fix 1: 优化连接池配置**
\`\`\`typescript
// prisma/schema.prisma

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// .env

// 🔧 修复前:
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=30"
// 🚨 问题: 5个实例 × 30连接 = 150 > max_connections(100)

// ✅ 修复后:
DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=20&connect_timeout=10"
// 改进: 5个实例 × 10连接 = 50 < max_connections(100)
// pool_timeout: 等待连接的最大时间（秒）
// connect_timeout: 建立连接的最大时间（秒）
\`\`\`

**PR**: #1237 "Reduce Prisma connection pool size to 10"

**Fix 2: 实施连接池监控**
\`\`\`typescript
// src/monitoring/databaseMetrics.ts

import { PrismaClient } from '@prisma/client';
import { register } from 'prom-client';

const prisma = new PrismaClient();

// 导出Prometheus指标
const connectionPoolGauge = new Gauge({
  name: 'prisma_connection_pool_active',
  help: 'Active database connections',
  registers: [register]
});

const connectionPoolMaxGauge = new Gauge({
  name: 'prisma_connection_pool_max',
  help: 'Maximum database connections',
  registers: [register]
});

// 每30秒更新指标
setInterval(async () => {
  const metrics = await prisma.$metrics.json();
  connectionPoolGauge.set(metrics.connections.active);
  connectionPoolMaxGauge.set(metrics.connections.max);
}, 30000);
\`\`\`

**PR**: #1238 "Add Prisma connection pool metrics"

**Fix 3: 添加自动连接回收**
\`\`\`typescript
// src/database/healthCheck.ts

async function recycleIdleConnections() {
  const result = await prisma.$queryRaw\`
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE state = 'idle in transaction'
      AND (now() - state_change) > interval '5 minutes'
  \`;

  if (result.length > 0) {
    logger.warn(\`Terminated \${result.length} idle connections\`);
  }
}

// 每5分钟运行一次
setInterval(recycleIdleConnections, 5 * 60 * 1000);
\`\`\`

**PR**: #1239 "Auto-recycle idle database connections"

### 监控

**告警规则**:
- \`postgresql_connection_pool_high\`: >80%利用率
- \`postgresql_connection_pool_exhausted\`: >=100%利用率
- \`prisma_connection_errors\`: >5 errors/min

**关键指标**:
| Metric | Threshold | Current |
|--------|-----------|---------|
| 连接池利用率 | <80% | 95% 🚨 |
| idle in transaction | <10% | 20% 🚨 |
| 慢查询(>5s) | <5 | 12 🚨 |

---

## 附录

### 联系方式

**Escalation流程**:
1. **L1**: #payments-oncall Slack (响应时间: <5分钟)
2. **L2**: Tech Lead @john.doe (响应时间: <15分钟)
3. **L3**: VP Engineering @jane.smith (响应时间: <30分钟)

### 工具清单

| 工具 | 用途 | URL |
|------|------|-----|
| Grafana | 监控面板 | https://grafana.company.com |
| Sentry | 错误跟踪 | https://sentry.io/company/payment-service |
| Datadog | APM追踪 | https://app.datadoghq.com |
| PagerDuty | 值班轮换 | https://company.pagerduty.com |

### 相关文档

- [Payment Service Architecture](../architecture/PAYMENT_SERVICE.md)
- [Database Schema](../database/SCHEMA.md)
- [Stripe Integration Guide](../integrations/STRIPE.md)
- [Post-mortem Template](../templates/POSTMORTEM.md)`,

        html: '<html>...</html>'
      },

      metadata: {
        version: '1.0.0',
        createdAt: '2025-12-12T12:00:00Z',
        updatedAt: '2025-12-12T12:00:00Z',
        authors: ['runbook-generator'],
        tags: ['runbook', 'incident-response', 'payment-service', 'troubleshooting'],
        wordCount: 5800,
        estimatedReadTime: 23
      },

      structure: {
        sections: [
          { id: 's1', title: '服务概览', level: 2, anchor: '#service-overview', wordCount: 120 },
          { id: 's2', title: '故障场景1: Stripe API限流', level: 2, anchor: '#scenario-1', wordCount: 2400 },
          { id: 's3', title: '故障场景2: 数据库连接池耗尽', level: 2, anchor: '#scenario-2', wordCount: 1900 },
          { id: 's4', title: '故障场景3: 支付失败率>5%', level: 2, anchor: '#scenario-3', wordCount: 1200 },
          { id: 's5', title: '附录', level: 2, anchor: '#appendix', wordCount: 180 }
        ],
        toc: `## Table of Contents

- [服务概览](#service-overview)
- [故障场景1: Stripe API限流](#scenario-1)
  - [症状](#symptoms-1)
  - [排查步骤](#troubleshooting-1)
  - [临时缓解](#mitigation-1)
  - [永久修复](#permanent-fix-1)
  - [回滚计划](#rollback-1)
  - [相关监控](#monitoring-1)
- [故障场景2: 数据库连接池耗尽](#scenario-2)
  - [症状](#symptoms-2)
  - [排查步骤](#troubleshooting-2)
  - [临时缓解](#mitigation-2)
  - [永久修复](#permanent-fix-2)
- [附录](#appendix)
  - [联系方式](#contacts)
  - [工具清单](#tools)
  - [相关文档](#related-docs)`
      },

      assets: {
        codeExamples: [
          { language: 'bash', code: 'kubectl ...', description: 'Kubernetes诊断命令' },
          { language: 'sql', code: 'SELECT pg_stat_activity...', description: 'PostgreSQL连接查询' },
          { language: 'typescript', code: 'const stripeLimiter = ...', description: '智能限流实现' }
        ]
      }
    }
  ],

  runbooks: [
    {
      scenario: {
        name: 'Stripe API限流',
        severity: 'high',
        frequency: 'occasional',
        impact: '支付成功率从99.5%下降至70-80%，用户体验受影响'
      },

      symptoms: [
        {
          description: '支付请求返回429错误',
          detectionMethod: 'Grafana alert: stripe_api_rate_limit_errors_high',
          example: 'ERROR Payment failed: StripeRateLimitError: Too many requests'
        },
        {
          description: 'Stripe支付成功率下降',
          detectionMethod: 'Prometheus metric: payment_success_rate < 0.8',
          example: 'Success rate: 75% (normal: 99.5%)'
        }
      ],

      troubleshooting: [
        {
          step: 1,
          action: '确认Stripe API状态',
          commands: ['curl https://status.stripe.com/api/v2/status.json'],
          expectedOutcome: '"indicator": "none" (无故障)',
          checkpoints: ['如果Stripe本身有故障，联系Stripe支持']
        },
        {
          step: 2,
          action: '检查当前限流情况',
          commands: [
            'kubectl exec -it deployment/payment-service -- node',
            'const metrics = await redis.get("stripe:api:calls:1h")',
            'console.log(JSON.parse(metrics))'
          ],
          expectedOutcome: 'rate_limited应<1%，如果>10%则异常'
        },
        {
          step: 3,
          action: '识别请求来源',
          commands: [
            'kubectl logs -l app=payment-service --tail=1000 | grep "429" | awk \'{print $8}\' | sort | uniq -c | sort -rn'
          ],
          expectedOutcome: '找出哪个endpoint触发限流',
          checkpoints: ['如果charges/create调用量>10倍正常值，可能是无限重试']
        }
      ],

      mitigation: {
        description: '临时缓解措施（5-10分钟内恢复服务）',
        steps: [
          '启用请求队列模式（限制并发为50/s）',
          '增加Redis缓存TTL从5分钟到30分钟',
          '临时禁用非关键功能（实时汇率查询、即时邮件）'
        ],
        commands: [
          'kubectl set env deployment/payment-service STRIPE_RATE_LIMIT=50',
          'kubectl set env deployment/payment-service QUEUE_MODE=enabled',
          'kubectl set env deployment/payment-service CACHE_TTL_SECONDS=1800'
        ],
        estimatedTime: '5-10分钟',
        risks: [
          '支付延迟增加至1-2秒',
          '汇率可能不完全准确（使用缓存值）',
          '邮件发送延迟（批量模式）'
        ]
      },

      permanentFix: {
        description: '长期解决方案',
        steps: [
          'PR #1234: 实施智能速率限制（Bottleneck库）',
          'PR #1235: 优化缓存策略（Stale-While-Revalidate）',
          'PR #1236: 使用Stripe Batch API减少调用量'
        ],
        estimatedTime: '2-3天开发 + 1天测试',
        verification: [
          '压力测试：模拟10,000 TPS负载',
          '验证429错误减少>95%',
          '验证支付成功率>99.5%',
          '监控Stripe API调用量下降60%'
        ]
      },

      rollback: {
        when: '如果缓解措施无效超过30分钟，或支付成功率<50%',
        steps: [
          '回滚到上一个稳定版本 v2.2.5',
          '禁用新功能',
          '清理Redis缓存',
          '验证回滚成功',
          '监控恢复情况'
        ],
        commands: [
          'kubectl rollout undo deployment/payment-service',
          'kubectl set env deployment/payment-service FEATURE_XYZ=false',
          'redis-cli FLUSHDB',
          'kubectl rollout status deployment/payment-service'
        ]
      },

      monitoring: {
        dashboards: [
          'https://grafana.company.com/d/payment-service',
          'https://grafana.company.com/d/stripe-integration'
        ],
        alerts: [
          'stripe_api_rate_limit_errors_high',
          'payment_success_rate_low',
          'stripe_api_latency_high'
        ],
        metrics: [
          { name: 'Stripe API成功率', threshold: '>99%', current: '98.2%' },
          { name: '429错误率', threshold: '<1%', current: '3.5%' },
          { name: 'Redis缓存命中率', threshold: '>80%', current: '75%' },
          { name: 'API延迟P95', threshold: '<800ms', current: '1250ms' }
        ]
      }
    },

    {
      scenario: {
        name: '数据库连接池耗尽',
        severity: 'critical',
        frequency: 'rare',
        impact: '服务完全不可用，影响100%用户'
      },

      symptoms: [
        {
          description: '所有支付请求失败，返回500错误',
          detectionMethod: 'Error logs: "Database connection timeout"',
          example: 'ERROR Database query failed: sorry, too many clients already'
        }
      ],

      troubleshooting: [
        {
          step: 1,
          action: '确认连接池状态',
          commands: [
            'kubectl exec -it postgres-0 -- psql -U postgres -d payment_db',
            'SELECT count(*), state FROM pg_stat_activity GROUP BY state;'
          ],
          expectedOutcome: '总连接数应<max_connections(100)',
          checkpoints: ['如果idle in transaction >20%，可能是连接泄漏']
        },
        {
          step: 2,
          action: '识别慢查询',
          commands: [
            'SELECT pid, duration, query FROM pg_stat_activity WHERE duration > interval \'5s\';'
          ],
          expectedOutcome: '找出长时间运行的查询'
        }
      ],

      mitigation: {
        description: '紧急缓解措施',
        steps: [
          '终止空闲事务（释放10-20个连接）',
          '临时增加max_connections到200',
          '缩容应用实例到3个'
        ],
        commands: [
          'SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = \'idle in transaction\';',
          'ALTER SYSTEM SET max_connections = 200;',
          'kubectl scale deployment/payment-service --replicas=3'
        ],
        estimatedTime: '5分钟',
        risks: ['增加max_connections会增加内存使用（每连接~10MB）']
      },

      permanentFix: {
        description: '优化连接池配置和监控',
        steps: [
          'PR #1237: 减少Prisma连接池大小到10（5实例×10=50<100）',
          'PR #1238: 添加Prisma连接池Prometheus指标',
          'PR #1239: 自动回收空闲连接（每5分钟）'
        ],
        estimatedTime: '1-2天',
        verification: [
          '验证连接池利用率<80%',
          'idle in transaction <10%',
          '慢查询<5个'
        ]
      },

      monitoring: {
        alerts: [
          'postgresql_connection_pool_high: >80%利用率',
          'postgresql_connection_pool_exhausted: >=100%',
          'prisma_connection_errors: >5 errors/min'
        ],
        metrics: [
          { name: '连接池利用率', threshold: '<80%', current: '95%' },
          { name: 'idle in transaction', threshold: '<10%', current: '20%' },
          { name: '慢查询(>5s)', threshold: '<5', current: '12' }
        ]
      }
    }
  ],

  qualityCheck: {
    score: 96,

    checks: [
      { name: 'All scenarios documented', passed: true, severity: 'error', message: '3/3故障场景完整文档化' },
      { name: 'Commands validated', passed: true, severity: 'warning', message: '所有诊断命令已验证可执行' },
      { name: 'Rollback plans present', passed: true, severity: 'error', message: '所有场景都有回滚计划' },
      { name: 'Monitoring links valid', passed: false, severity: 'warning', message: '1个Grafana链接需要更新' }
    ],

    issues: [
      {
        type: 'broken-link',
        location: 'PAYMENT_SERVICE_RUNBOOK.md:480',
        description: 'Grafana dashboard链接返回404',
        suggestion: '更新到新的Grafana URL或验证dashboard ID'
      }
    ]
  },

  recommendations: [
    {
      type: 'improvement',
      priority: 'high',
      target: 'devops',
      title: '添加自动化Runbook执行',
      description: '将常见排查步骤脚本化，减少人工操作时间',
      actionable: {
        steps: [
          '创建kubectl插件 kubectl payments diagnose',
          '实现自动症状检测和缓解建议',
          '集成PagerDuty自动执行缓解措施'
        ],
        estimatedEffort: 'moderate'
      }
    },
    {
      type: 'info',
      priority: 'medium',
      target: 'developer',
      title: '定期Runbook演练',
      description: '每月进行一次故障演练，确保团队熟悉Runbook流程',
      actionable: {
        steps: [
          '设置每月第一个周五下午2点进行演练',
          '轮换演练场景（Stripe限流、DB连接池、支付失败）',
          '记录演练结果和改进建议',
          '更新Runbook基于演练发现'
        ],
        estimatedEffort: 'easy'
      }
    }
  ],

  files: [
    { path: 'docs/runbooks/PAYMENT_SERVICE_RUNBOOK.md', type: 'markdown', size: 58000 },
    { path: 'docs/runbooks/scripts/diagnose-stripe-ratelimit.sh', type: 'code', size: 1200 },
    { path: 'docs/runbooks/scripts/recycle-db-connections.sh', type: 'code', size: 800 }
  ],

  metadata: {
    generatedAt: '2025-12-12T12:00:30Z',
    version: '1.0.0',
    generator: 'knowledge-manager v2.0.0',
    sourceHash: 'ghi789jkl012'
  }
};
```

**效果**:
- **完整覆盖**: 3个高频故障场景（Stripe限流、DB连接池、支付失败），包含症状、排查、缓解、修复、回滚全流程
- **可执行命令**: 所有诊断和缓解步骤都有kubectl/SQL/bash命令，可直接复制执行
- **时间估算**: 临时缓解5-10分钟，永久修复2-3天，回滚5分钟
- **监控集成**: 每个场景链接对应的Grafana面板、告警规则、关键指标
- **自动化建议**: 推荐创建kubectl插件实现自动诊断
- **质量评分**: 96/100，仅1个Grafana链接需要更新

---

## Best Practices

### ✅ DO: Effective Knowledge Management

```typescript
// ✅ GOOD: 文档即代码（Docs-as-Code）
const goodPractice = {
  storage: 'Git repository (docs/)',
  format: 'Markdown',
  review: 'PR process with code owners',
  versioning: 'Git tags (v1.0.0, v1.1.0)',
  automation: 'CI pipeline generates docs from code',
  sync: 'Auto-publish to Notion/Confluence on merge'
};

// ✅ GOOD: 多层级架构图（C4 Model）
const goodArchitecture = {
  level1: 'System Context - 外部视角（客户、管理员、外部系统）',
  level2: 'Container - 技术栈视角（微服务、数据库、消息队列）',
  level3: 'Component - 代码结构视角（Controller、Service、Repository）',
  level4: 'Code - 类图视角（可选，针对复杂组件）'
};

// ✅ GOOD: Runbook结构化（症状→排查→缓解→修复→回滚）
const goodRunbook = {
  scenario: {
    name: '明确故障名称',
    severity: 'critical/high/medium/low',
    frequency: 'frequent/occasional/rare',
    impact: '用户影响说明'
  },
  symptoms: ['症状1: Grafana告警', '症状2: 错误日志特征', '症状3: 用户报告'],
  troubleshooting: [
    { step: 1, action: '检查A', commands: ['kubectl ...'], expectedOutcome: '...' },
    { step: 2, action: '检查B', commands: ['psql ...'], expectedOutcome: '...' }
  ],
  mitigation: {
    description: '临时缓解（5-10分钟）',
    steps: ['步骤1', '步骤2'],
    commands: ['kubectl set env ...'],
    risks: ['风险1', '风险2']
  },
  permanentFix: {
    description: '永久修复',
    pullRequests: ['#1234', '#1235'],
    estimatedTime: '2-3天',
    verification: ['验证1', '验证2']
  },
  rollback: {
    when: '何时回滚',
    steps: ['回滚步骤1', '回滚步骤2']
  }
};

// ✅ GOOD: AI助手集成
const goodAIAssistant = {
  knowledgeBase: 'Markdown文档 → 向量嵌入',
  model: 'claude-3-5-sonnet',
  capabilities: {
    qa: '回答\"如何部署?\"等问题',
    codeSearch: '查找相关代码示例',
    docRecommendation: '推荐相关文档'
  },
  context: '100K token上下文窗口'
};

// ✅ GOOD: 自动文档更新检测
const goodAutomation = {
  trigger: 'CI pipeline on commit',
  checks: [
    'API文档与OpenAPI spec一致性',
    '架构图与代码依赖一致性',
    'Runbook链接有效性',
    '代码示例可编译'
  ],
  action: 'Failed check → Block merge + Create issue'
};
```

### ❌ DON'T: Poor Knowledge Management Practices

```typescript
// ❌ BAD: 文档与代码分离
const badPractice = {
  storage: 'Confluence only',
  versioning: 'None (每次编辑覆盖)',
  review: 'No review process',
  sync: 'Manual copy-paste from code',
  // 问题：文档很快过时，无版本控制
};

// ❌ BAD: 单一层级架构图
const badArchitecture = {
  diagram: '一张巨大的架构图，包含所有细节',
  // 问题：过于复杂，无法理解
  // 新人无法快速了解系统
  // 修改困难
};

// ❌ BAD: 缺乏结构的Runbook
const badRunbook = `
故障：支付失败

排查：检查日志，看看是什么问题。可能是Stripe的问题，也可能是数据库的问题。

修复：重启服务试试。
`;
// 问题：
// - 没有明确症状识别
// - 排查步骤模糊（\"看看是什么问题\"）
// - 缺少具体命令
// - 没有缓解/回滚计划
// - 没有监控链接

// ❌ BAD: 手动同步到多平台
const badSync = {
  process: 'Write in Notion → Copy to Confluence → Copy to Wiki',
  // 问题：三处文档不同步，修改需要更新3次
};

// ❌ BAD: 缺少代码示例
const badAPIDoc = {
  endpoint: 'POST /orders',
  description: '创建订单',
  // ❌ 没有请求/响应示例
  // ❌ 没有多语言代码示例
  // ❌ 没有错误处理说明
};

// ❌ BAD: 架构图未标注技术栈
const badDiagram = `
[Web App] --> [API Gateway] --> [Service A] --> [Database]
`;
// 问题：
// - 不知道Web App用什么框架
// - 不知道Service A是什么技术
// - 不知道Database是MySQL还是PostgreSQL
```

### 🎯 Implementation Guidelines

1. **Documentation-as-Code Workflow** (文档即代码工作流)
   ```bash
   # 开发流程
   1. Write code
   2. Add JSDoc/docstring comments
   3. Update OpenAPI spec (if API changed)
   4. Generate docs: npm run docs:generate
   5. Review docs in PR
   6. Merge → Auto-publish to Notion/Confluence

   # CI检查
   - Markdown lint (markdownlint)
   - Link checker (markdown-link-check)
   - Code examples compilation
   - OpenAPI spec validation
   ```

2. **C4 Model Architecture** (C4架构图分层)
   ```
   Level 1 (System Context):
   - Who: Business stakeholders, Product managers
   - Shows: External users, external systems, system boundary
   - Detail: High-level, 5-10 elements

   Level 2 (Container):
   - Who: Developers, DevOps
   - Shows: Applications, databases, message queues
   - Detail: Medium, 10-20 elements, technology stack

   Level 3 (Component):
   - Who: Developers
   - Shows: Internal components (Controller, Service, Repository)
   - Detail: Detailed, 20-40 elements per service

   Level 4 (Code - optional):
   - Who: Developers (for complex components only)
   - Shows: Class diagrams, interfaces
   - Detail: Very detailed, UML
   ```

3. **Runbook Template** (Runbook模板)
   ```markdown
   # [Service Name] Runbook

   ## Scenario: [Failure Name]

   **Severity**: Critical/High/Medium/Low
   **Frequency**: Frequent/Occasional/Rare
   **Impact**: [User impact description]

   ### Symptoms
   - Alert: [Grafana alert name]
   - Logs: [Error pattern]
   - User report: [What users see]

   ### Troubleshooting

   **Step 1: [Check name]**
   ```bash
   # Command
   kubectl ...

   # Expected output
   ...

   # If unexpected
   → Go to Step 3
   ```

   **Step 2: [Check name]**
   ...

   ### Mitigation (5-10 min)

   **Option A**: [Quick fix description]
   ```bash
   kubectl set env ...
   ```

   **Risks**: [What could go wrong]

   ### Permanent Fix

   **PR #1234**: [Fix description]
   **ETA**: 2-3 days
   **Verification**: [How to verify]

   ### Rollback

   **When**: If mitigation fails after 30 min
   ```bash
   kubectl rollout undo ...
   ```

   ### Monitoring

   **Dashboards**: [Grafana URL]
   **Metrics**: [Key metrics and thresholds]
   ```

4. **Search Optimization** (搜索优化)
   ```typescript
   // Algolia索引配置
   const algoliaIndex = {
     indexName: 'docs',

     // 索引字段
     attributesToIndex: [
       'title',
       'content',
       'tags',
       'category'
     ],

     // 搜索排序
     customRanking: [
       'desc(views)',         // 浏览量
       'desc(lastUpdated)',   // 最新更新
       'desc(relevance)'      // 相关性
     ],

     // 分面过滤
     attributesForFaceting: [
       'category',            // 分类
       'tags',                // 标签
       'version'              // 版本
     ],

     // 高亮
     attributesToHighlight: ['title', 'content']
   };

   // Elasticsearch索引
   const esMapping = {
     properties: {
       title: { type: 'text', analyzer: 'english' },
       content: { type: 'text', analyzer: 'english' },
       tags: { type: 'keyword' },
       category: { type: 'keyword' },
       lastUpdated: { type: 'date' }
     }
   };
   ```

5. **Sync Strategy** (同步策略)
   ```typescript
   // One-time: 手动触发同步
   // Continuous: 每次commit自动同步
   // On-commit: Git hook触发

   const syncConfig = {
     mode: 'on-commit',

     targets: [
       {
         platform: 'notion',
         when: 'docs/**/*.md changes',
         action: 'Update Notion database'
       },
       {
         platform: 'confluence',
         when: 'docs/**/*.md changes',
         action: 'Update Confluence space'
       },
       {
         platform: 'github-wiki',
         when: 'docs/**/*.md changes',
         action: 'Git push to wiki branch'
       }
     ],

     conflictResolution: 'overwrite', // Git is source of truth
     preserveHistory: true            // Keep versions in platforms
   };
   ```

---

## Related Skills

- **code-generator** (1) - Generates code from specs, comments used by knowledge-manager for docs
- **test-generator** (3) - Generates tests, test docs integrated into knowledge base
- **code-reviewer** (5) - Reviews docs in PR, ensures docs-code consistency
- **project-planner** (29) - Plans projects, uses knowledge base for historical data
- **collaboration-hub** (31) - Team collaboration, shares docs from knowledge base

---

## Changelog

### Version 2.0.0 (2025-12-12)
- ✨ Initial release with comprehensive knowledge management capabilities
- 📚 Auto documentation generation from code (API docs, README, CHANGELOG)
- 🏗️ C4 Model architecture diagrams (System/Container/Component/Code)
- 📖 Markdown knowledge base with full-text search (Algolia/Elasticsearch)
- 🆘 Runbook generation from incident reports
- 🔄 Multi-platform sync (Notion/Confluence/GitHub Wiki)
- 🤖 AI Q&A assistant with 100K context window
- 🔍 Quality checks: broken links, code examples, doc coverage
- 📊 3 comprehensive examples (API docs 94/100, Architecture 98/100, Runboo
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
interface KnowledgeManagerInput {
}
```

### 输出接口

```typescript
interface KnowledgeManagerOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

k 96/100)
