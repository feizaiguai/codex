---
name: 24-cicd-pipeline-builder-G
description: CI/CD pipeline builder for automated pipeline generation. Supports multiple platforms (GitHub Actions/GitLab CI/Jenkins/CircleCI), complete workflow (build→test→security scan→deploy), matrix builds (multi-env/multi-version), security scan integration (SAST/DAST/SCA), deployment strategies (multi-env). Use for CI/CD automation, multi-environment pipelines, quality gate integration.
---

# CI/CD Pipeline Builder

**Version**: 2.0.0
**Category**: DevOps
**Priority**: P1 (Core Capability)
**Last Updated**: 2025-01-12

---

## Description

The CI/CD Pipeline Builder is a comprehensive continuous integration and deployment automation tool that generates production-ready pipeline configurations for multiple platforms including GitHub Actions, GitLab CI, Jenkins, and Azure DevOps. It enables teams to automate the entire software delivery lifecycle from code commit to production deployment with built-in security scanning, testing orchestration, and deployment strategies.

**Core Capabilities**:

- **Multi-Platform Pipeline Generation**: Create pipelines for GitHub Actions (YAML), GitLab CI (.gitlab-ci.yml), Jenkins (Jenkinsfile), Azure Pipelines, CircleCI with consistent patterns
- **Complete Workflow Automation**: Automated code quality checks, unit/integration/E2E testing, security scanning (SAST/DAST), Docker image building, multi-environment deployment
- **Performance Optimization**: Matrix builds for multi-version testing, intelligent caching strategies, parallel job execution, conditional workflows, incremental builds
- **Security Integration**: Secret management (GitHub Secrets, Vault), container image scanning (Trivy, Clair), dependency vulnerability checks, OWASP scanning, license compliance
- **Deployment Strategies**: Blue-green deployments, canary releases, rolling updates, feature flag integration, automated rollback on failure
- **Notification & Monitoring**: Slack/Email/Teams notifications, deployment status updates, automated issue creation on failures, build metrics tracking

---

## Instructions

### When to Activate

This skill should activate when users:

1. Request **"create CI/CD pipeline"**, **"set up GitHub Actions"**, **"configure continuous integration"**, **"automate deployment"**
2. Mention **"build automation"**, **"continuous delivery"**, **"pipeline configuration"**, **"Jenkins setup"**, **"workflow automation"**
3. Need **"Docker build automation"**, **"test automation"**, **"security scanning in CI"**, **"deploy to Kubernetes"**
4. Ask **"how to set up CI/CD"**, **"automate testing"**, **"configure build pipeline"**, **"optimize build speed"**
5. Require **"multi-environment deployment"**, **"staging/production pipeline"**, **"approval workflows"**, **"deployment gates"**

### Execution Flow

```mermaid
flowchart TD
    Start([User Requests CI/CD Pipeline]) --> Analyze[Analyze Project Structure]
    Analyze --> DetectLang[Detect Language & Framework]
    DetectLang --> ChoosePlatform[Select CI Platform]

    ChoosePlatform --> ConfigPipeline[Configure Pipeline Stages]
    ConfigPipeline --> DefineJobs{Define Jobs}

    DefineJobs --> Lint[Code Quality: Lint/Format]
    DefineJobs --> Test[Testing: Unit/Integration/E2E]
    DefineJobs --> Security[Security: SAST/Dependency Scan]
    DefineJobs --> Build[Build: Docker/Binary/Package]
    DefineJobs --> Deploy[Deployment: Staging/Production]

    Lint --> OptimizePerf[Apply Performance Optimizations]
    Test --> OptimizePerf
    Security --> OptimizePerf
    Build --> OptimizePerf

    OptimizePerf --> AddCaching[Add Caching Strategy]
    AddCaching --> ParallelJobs[Configure Parallel Execution]
    ParallelJobs --> MatrixBuild[Set Up Matrix Builds]

    MatrixBuild --> AddSecurity[Integrate Security Checks]
    AddSecurity --> SecretMgmt[Configure Secret Management]
    SecretMgmt --> ImageScan[Add Container Scanning]
    ImageScan --> DependencyScan[Add Dependency Audit]

    DependencyScan --> ConfigDeploy[Configure Deployment]
    ConfigDeploy --> EnvSetup[Set Up Environments]
    EnvSetup --> ApprovalGates[Add Approval Gates]
    ApprovalGates --> Rollback[Configure Rollback Strategy]

    Rollback --> Notifications[Set Up Notifications]
    Notifications --> Generate[Generate Pipeline Config]

    Generate --> ValidateSyntax[Validate YAML/Groovy Syntax]
    ValidateSyntax --> BestPractices[Apply Best Practices]
    BestPractices --> Output[Output Complete Pipeline]

    Output --> End([Return Pipeline Configuration])
```

---

## Input/Output Interface

### TypeScript Interface

```typescript
/**
 * Input configuration for CI/CD pipeline generation
 */
interface CICDPipelineBuilderInput {
  /**
   * Target CI/CD platform
   * @default 'github-actions'
   */
  platform: 'github-actions' | 'gitlab-ci' | 'jenkins' | 'azure-pipelines' | 'circleci';

  /**
   * Primary programming language/framework
   * @example 'node', 'python', 'java', 'go', 'rust', 'ruby'
   */
  language: string;

  /**
   * Framework-specific configuration
   */
  framework?: {
    name: string; // 'express', 'django', 'spring-boot', 'rails'
    version?: string;
    buildTool?: string; // 'npm', 'gradle', 'maven', 'cargo'
  };

  /**
   * Pipeline stages configuration
   */
  stages: Array<{
    /**
     * Stage name (lint, test, build, deploy)
     */
    name: string;

    /**
     * Jobs to execute in this stage
     */
    jobs: Array<{
      /**
       * Job identifier
       */
      name: string;

      /**
       * Execution steps (parallel or sequential)
       */
      steps: string[];

      /**
       * Target environment (for deployment jobs)
       */
      environment?: 'development' | 'staging' | 'production';

      /**
       * Require manual approval before execution
       */
      requiresApproval?: boolean;

      /**
       * Job timeout in minutes
       * @default 30
       */
      timeout?: number;

      /**
       * Retry configuration
       */
      retry?: {
        maxAttempts: number;
        backoff?: 'linear' | 'exponential';
      };
    }>;

    /**
     * Run stage in parallel with others
     */
    parallel?: boolean;

    /**
     * Continue pipeline even if this stage fails
     */
    allowFailure?: boolean;
  }>;

  /**
   * Testing configuration
   */
  testing?: {
    /**
     * Unit test configuration
     */
    unit?: {
      command: string;
      coverage?: {
        enabled: boolean;
        threshold?: number; // minimum coverage %
        report?: 'codecov' | 'coveralls' | 'sonarqube';
      };
    };

    /**
     * Integration test configuration
     */
    integration?: {
      command: string;
      services?: string[]; // ['postgres', 'redis', 'mongodb']
    };

    /**
     * End-to-end test configuration
     */
    e2e?: {
      command: string;
      browser?: 'chromium' | 'firefox' | 'webkit' | 'all';
      headless?: boolean;
      parallelism?: number; // number of parallel test runners
    };

    /**
     * Performance testing
     */
    performance?: {
      command: string;
      thresholds?: {
        maxLatency?: number; // ms
        minThroughput?: number; // req/s
      };
    };
  };

  /**
   * Build configuration
   */
  build?: {
    /**
     * Build output type
     */
    type: 'docker' | 'binary' | 'package' | 'static-site';

    /**
     * Dockerfile path (for Docker builds)
     */
    dockerfile?: string;

    /**
     * Multi-architecture builds
     * @example ['linux/amd64', 'linux/arm64']
     */
    platforms?: string[];

    /**
     * Build arguments
     */
    buildArgs?: Record<string, string>;

    /**
     * Output artifact configuration
     */
    artifacts?: {
      paths: string[];
      retention?: number; // days to keep artifacts
    };

    /**
     * Container registry configuration
     */
    registry?: {
      provider: 'ghcr' | 'dockerhub' | 'ecr' | 'gcr' | 'acr';
      repository: string;
      tagStrategy: 'branch' | 'semver' | 'commit-sha' | 'custom';
      customTag?: string;
    };
  };

  /**
   * Security scanning configuration
   */
  security?: {
    /**
     * Static Application Security Testing
     */
    sast?: {
      enabled: boolean;
      tool?: 'semgrep' | 'sonarqube' | 'snyk' | 'codeql';
      severityThreshold?: 'low' | 'medium' | 'high' | 'critical';
    };

    /**
     * Dynamic Application Security Testing
     */
    dast?: {
      enabled: boolean;
      tool?: 'zap' | 'burp' | 'arachni';
      targetUrl?: string;
    };

    /**
     * Dependency vulnerability scanning
     */
    dependencyCheck?: {
      enabled: boolean;
      tool?: 'npm-audit' | 'snyk' | 'dependabot' | 'trivy';
      autoFix?: boolean; // automatically create PRs for fixes
    };

    /**
     * Secret scanning in code and commits
     */
    secretScanning?: {
      enabled: boolean;
      tool?: 'gitleaks' | 'trufflehog' | 'detect-secrets';
      failOnLeak?: boolean;
    };

    /**
     * Container image scanning
     */
    containerScan?: {
      enabled: boolean;
      tool?: 'trivy' | 'clair' | 'anchore' | 'aqua';
      severityThreshold?: 'low' | 'medium' | 'high' | 'critical';
    };

    /**
     * License compliance checking
     */
    licenseCheck?: {
      enabled: boolean;
      allowed?: string[]; // ['MIT', 'Apache-2.0', 'BSD-3-Clause']
      denied?: string[]; // ['GPL-3.0', 'AGPL-3.0']
    };
  };

  /**
   * Deployment configuration
   */
  deployment?: {
    /**
     * Deployment targets
     */
    targets: Array<{
      /**
       * Environment name
       */
      environment: 'development' | 'staging' | 'production' | string;

      /**
       * Deployment platform
       */
      platform: 'kubernetes' | 'aws-ecs' | 'aws-lambda' | 'vercel' | 'netlify' | 'heroku' | 'azure-app-service';

      /**
       * Deployment strategy
       */
      strategy?: 'rolling-update' | 'blue-green' | 'canary' | 'recreate';

      /**
       * Manual approval required
       */
      requiresApproval?: boolean;

      /**
       * Secrets required for deployment
       */
      secrets?: string[]; // ['AWS_ACCESS_KEY', 'KUBE_CONFIG']

      /**
       * Health check configuration
       */
      healthCheck?: {
        url: string;
        timeout: number; // seconds
        retries: number;
      };

      /**
       * Rollback configuration
       */
      rollback?: {
        automatic?: boolean;
        conditions?: {
          errorRate?: number; // % threshold
          healthCheckFailures?: number;
        };
      };

      /**
       * Post-deployment actions
       */
      postDeploy?: {
        runMigrations?: boolean;
        warmupCache?: boolean;
        notifyStakeholders?: boolean;
      };
    }>;
  };

  /**
   * Performance optimization settings
   */
  optimization?: {
    /**
     * Caching strategy
     */
    caching?: {
      dependencies?: boolean; // cache node_modules, pip cache, etc.
      docker?: {
        layers?: boolean; // Docker layer caching
        registry?: boolean; // push/pull cache images
      };
      custom?: Array<{
        key: string;
        paths: string[];
      }>;
    };

    /**
     * Matrix build configuration
     */
    matrix?: {
      enabled: boolean;
      dimensions?: {
        os?: string[]; // ['ubuntu-latest', 'windows-latest', 'macos-latest']
        nodeVersion?: string[]; // ['16', '18', '20']
        pythonVersion?: string[]; // ['3.9', '3.10', '3.11']
      };
      failFast?: boolean; // stop all jobs if one fails
    };

    /**
     * Parallel execution
     */
    parallelism?: {
      maxJobs?: number; // maximum concurrent jobs
      strategy?: 'fast-fail' | 'complete-all';
    };
  };

  /**
   * Notification configuration
   */
  notifications?: {
    /**
     * Slack notifications
     */
    slack?: {
      webhookUrl: string;
      channel?: string;
      events?: ('success' | 'failure' | 'started' | 'deployment')[];
      mentions?: {
        onFailure?: string[]; // ['@team-lead', '@oncall']
        onSuccess?: string[];
      };
    };

    /**
     * Email notifications
     */
    email?: {
      recipients: string[];
      events?: ('success' | 'failure' | 'deployment')[];
    };

    /**
     * Microsoft Teams notifications
     */
    teams?: {
      webhookUrl: string;
      events?: ('success' | 'failure' | 'deployment')[];
    };

    /**
     * Create GitHub/GitLab issues on failure
     */
    issueCreation?: {
      enabled: boolean;
      labels?: string[]; // ['ci-failure', 'bug']
      assignees?: string[];
      template?: string;
    };
  };

  /**
   * Trigger configuration
   */
  triggers?: {
    /**
     * Branch patterns to trigger on
     */
    branches?: string[]; // ['main', 'develop', 'release/*']

    /**
     * Pull request events
     */
    pullRequest?: {
      enabled: boolean;
      targetBranches?: string[];
      types?: ('opened' | 'synchronize' | 'reopened')[];
    };

    /**
     * Tag/release triggers
     */
    tags?: {
      enabled: boolean;
      pattern?: string; // 'v*.*.*'
    };

    /**
     * Schedule (cron) triggers
     */
    schedule?: {
      enabled: boolean;
      cron: string; // '0 2 * * *' for 2am daily
      timezone?: string;
    };

    /**
     * Manual workflow dispatch
     */
    manual?: {
      enabled: boolean;
      inputs?: Record<string, {
        description: string;
        required: boolean;
        default?: string;
      }>;
    };
  };

  /**
   * Environment variables
   */
  environment?: {
    /**
     * Global environment variables
     */
    global?: Record<string, string>;

    /**
     * Environment-specific variables
     */
    perEnvironment?: Record<string, Record<string, string>>;
  };

  /**
   * Advanced configuration
   */
  advanced?: {
    /**
     * Custom scripts to inject
     */
    customScripts?: {
      preBuild?: string;
      postBuild?: string;
      preDeploy?: string;
      postDeploy?: string;
    };

    /**
     * Conditional execution
     */
    conditions?: {
      skipCI?: string; // regex to match in commit message
      runOnlyOn?: string[]; // file paths that trigger pipeline
    };

    /**
     * Resource limits
     */
    resources?: {
      cpu?: string; // '2' or '2000m'
      memory?: string; // '4Gi'
    };
  };
}

/**
 * Output from CI/CD pipeline generation
 */
interface CICDPipelineBuilderOutput {
  /**
   * Generated pipeline configuration content
   */
  config: {
    /**
     * File path where config should be saved
     */
    filePath: string;

    /**
     * Configuration content (YAML or Groovy)
     */
    content: string;

    /**
     * Syntax validation result
     */
    valid: boolean;

    /**
     * Validation errors if any
     */
    errors?: string[];
  };

  /**
   * Additional files to create
   */
  additionalFiles?: Array<{
    path: string;
    content: string;
    description: string;
  }>;

  /**
   * Pipeline metadata
   */
  metadata: {
    /**
     * Platform identifier
     */
    platform: string;

    /**
     * Estimated build time
     */
    estimatedBuildTime: {
      min: number; // minutes
      max: number;
      withCache: number;
    };

    /**
     * Cost estimation (if applicable)
     */
    costEstimate?: {
      perBuild: number; // USD
      monthly: number; // assuming X builds/month
      currency: string;
      assumptions: string[];
    };

    /**
     * Number of jobs/stages
     */
    jobCount: number;
    stageCount: number;

    /**
     * Parallelism degree
     */
    maxParallelJobs: number;
  };

  /**
   * Security analysis
   */
  security: {
    /**
     * Security score (0-100)
     */
    score: number;

    /**
     * Security features enabled
     */
    features: string[];

    /**
     * Security recommendations
     */
    recommendations: string[];

    /**
     * Secrets detected in configuration
     */
    secretsDetected: Array<{
      type: string;
      location: string;
      severity: 'low' | 'medium' | 'high' | 'critical';
      recommendation: string;
    }>;
  };

  /**
   * Performance optimization summary
   */
  optimization: {
    /**
     * Caching enabled
     */
    cachingEnabled: boolean;

    /**
     * Cache hit rate estimate
     */
    estimatedCacheHitRate?: number; // %

    /**
     * Time saved by caching
     */
    cachingTimeSaving?: number; // minutes

    /**
     * Parallel jobs configured
     */
    parallelJobsCount: number;

    /**
     * Optimizations applied
     */
    appliedOptimizations: string[];

    /**
     * Further optimization suggestions
     */
    suggestions: string[];
  };

  /**
   * Best practices compliance
   */
  bestPractices: {
    /**
     * Overall compliance score
     */
    score: number; // 0-100

    /**
     * Checks performed
     */
    checks: Array<{
      name: string;
      passed: boolean;
      severity: 'info' | 'warning' | 'error';
      message: string;
      fix?: string;
    }>;
  };

  /**
   * Setup instructions
   */
  setup: {
    /**
     * Prerequisites
     */
    prerequisites: string[];

    /**
     * Step-by-step setup guide
     */
    steps: Array<{
      order: number;
      title: string;
      description: string;
      commands?: string[];
    }>;

    /**
     * Required secrets/variables to configure
     */
    requiredSecrets: Array<{
      name: string;
      description: string;
      example?: string;
      required: boolean;
    }>;

    /**
     * Documentation links
     */
    documentation: string[];
  };

  /**
   * Validation and testing
   */
  validation: {
    /**
     * Local testing commands
     */
    localTest?: string;

    /**
     * Dry-run command
     */
    dryRun?: string;

    /**
     * Validation checklist
     */
    checklist: string[];
  };
}
```

---

## Usage Examples

### Example 1: GitHub Actions Complete Pipeline - Node.js Microservice

**Scenario**: Create a production-ready CI/CD pipeline for a Node.js Express microservice with comprehensive testing, security scanning, Docker build, and multi-environment deployment to Kubernetes.

**Input**:

```typescript
const input: CICDPipelineBuilderInput = {
  platform: 'github-actions',
  language: 'node',
  framework: {
    name: 'express',
    version: '18',
    buildTool: 'npm'
  },

  stages: [
    {
      name: 'quality',
      jobs: [
        { name: 'lint', steps: ['eslint', 'prettier-check'] },
        { name: 'type-check', steps: ['typescript'] }
      ],
      parallel: true
    },
    {
      name: 'test',
      jobs: [
        {
          name: 'unit-test',
          steps: ['jest'],
          retry: { maxAttempts: 2, backoff: 'linear' }
        },
        { name: 'integration-test', steps: ['supertest'] }
      ]
    },
    {
      name: 'security',
      jobs: [
        { name: 'sast', steps: ['semgrep'] },
        { name: 'dependency-audit', steps: ['npm-audit'] }
      ],
      parallel: true
    },
    {
      name: 'build',
      jobs: [
        { name: 'docker-build', steps: ['docker-build', 'docker-push'] }
      ]
    },
    {
      name: 'deploy',
      jobs: [
        {
          name: 'deploy-staging',
          steps: ['kubectl-apply'],
          environment: 'staging'
        },
        {
          name: 'deploy-production',
          steps: ['kubectl-apply'],
          environment: 'production',
          requiresApproval: true
        }
      ]
    }
  ],

  testing: {
    unit: {
      command: 'npm test',
      coverage: {
        enabled: true,
        threshold: 85,
        report: 'codecov'
      }
    },
    integration: {
      command: 'npm run test:integration',
      services: ['postgres', 'redis']
    },
    e2e: {
      command: 'npm run test:e2e',
      browser: 'chromium',
      headless: true,
      parallelism: 3
    }
  },

  build: {
    type: 'docker',
    dockerfile: 'Dockerfile',
    platforms: ['linux/amd64', 'linux/arm64'],
    registry: {
      provider: 'ghcr',
      repository: 'company/payment-service',
      tagStrategy: 'semver'
    }
  },

  security: {
    sast: {
      enabled: true,
      tool: 'semgrep',
      severityThreshold: 'high'
    },
    dependencyCheck: {
      enabled: true,
      tool: 'npm-audit',
      autoFix: true
    },
    secretScanning: {
      enabled: true,
      tool: 'gitleaks',
      failOnLeak: true
    },
    containerScan: {
      enabled: true,
      tool: 'trivy',
      severityThreshold: 'critical'
    }
  },

  deployment: {
    targets: [
      {
        environment: 'staging',
        platform: 'kubernetes',
        strategy: 'rolling-update',
        requiresApproval: false,
        secrets: ['KUBE_CONFIG_STAGING', 'DATABASE_URL'],
        healthCheck: {
          url: 'https://staging-api.company.com/health',
          timeout: 30,
          retries: 3
        },
        postDeploy: {
          runMigrations: true,
          warmupCache: true,
          notifyStakeholders: false
        }
      },
      {
        environment: 'production',
        platform: 'kubernetes',
        strategy: 'canary',
        requiresApproval: true,
        secrets: ['KUBE_CONFIG_PROD', 'DATABASE_URL', 'STRIPE_API_KEY'],
        healthCheck: {
          url: 'https://api.company.com/health',
          timeout: 60,
          retries: 5
        },
        rollback: {
          automatic: true,
          conditions: {
            errorRate: 5, // rollback if error rate > 5%
            healthCheckFailures: 2
          }
        },
        postDeploy: {
          runMigrations: true,
          warmupCache: true,
          notifyStakeholders: true
        }
      }
    ]
  },

  optimization: {
    caching: {
      dependencies: true,
      docker: {
        layers: true,
        registry: true
      }
    },
    matrix: {
      enabled: true,
      dimensions: {
        nodeVersion: ['18', '20']
      },
      failFast: false
    },
    parallelism: {
      maxJobs: 5,
      strategy: 'fast-fail'
    }
  },

  notifications: {
    slack: {
      webhookUrl: '${{ secrets.SLACK_WEBHOOK }}',
      channel: '#deployments',
      events: ['failure', 'deployment'],
      mentions: {
        onFailure: ['@team-backend', '@oncall'],
        onSuccess: []
      }
    },
    issueCreation: {
      enabled: true,
      labels: ['ci-failure', 'needs-investigation'],
      assignees: ['@team-lead']
    }
  },

  triggers: {
    branches: ['main', 'develop', 'release/*'],
    pullRequest: {
      enabled: true,
      targetBranches: ['main', 'develop'],
      types: ['opened', 'synchronize']
    },
    tags: {
      enabled: true,
      pattern: 'v*.*.*'
    },
    schedule: {
      enabled: true,
      cron: '0 2 * * *', // 2am daily for nightly tests
      timezone: 'UTC'
    }
  },

  environment: {
    global: {
      NODE_ENV: 'production',
      LOG_LEVEL: 'info'
    },
    perEnvironment: {
      staging: {
        API_URL: 'https://staging-api.company.com'
      },
      production: {
        API_URL: 'https://api.company.com'
      }
    }
  }
};
```

**Output**:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline - Payment Service

on:
  push:
    branches:
      - main
      - develop
      - 'release/*'
    tags:
      - 'v*.*.*'
  pull_request:
    branches:
      - main
      - develop
    types:
      - opened
      - synchronize
  schedule:
    - cron: '0 2 * * *'  # 2am UTC daily
  workflow_dispatch:

env:
  NODE_VERSION: '18'
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  NODE_ENV: 'production'
  LOG_LEVEL: 'info'

jobs:
  # Quality Stage - Parallel Execution
  lint:
    name: Code Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Check code formatting
        run: npm run prettier:check

  type-check:
    name: TypeScript Type Checking
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npx tsc --noEmit

  # Test Stage
  unit-test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: [lint, type-check]
    strategy:
      matrix:
        node-version: ['18', '20']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage
        continue-on-error: false

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unit-tests
          fail_ci_if_error: true

      - name: Check coverage threshold
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 85" | bc -l) )); then
            echo "Coverage $COVERAGE% is below threshold 85%"
            exit 1
          fi

  integration-test:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [lint, type-check]
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: payment_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run database migrations
        run: npm run migrate
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/payment_test

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/payment_test
          REDIS_URL: redis://localhost:6379

  e2e-test:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: [unit-test, integration-test]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          CI: true

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7

  # Security Stage - Parallel Execution
  sast-scan:
    name: SAST Security Scanning
    runs-on: ubuntu-latest
    needs: [lint, type-check]
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
          severity: ERROR
        env:
          SEMGREP_RULES: auto

      - name: Upload SARIF results
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: semgrep.sarif

  dependency-audit:
    name: Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    needs: [lint, type-check]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Check for outdated dependencies
        run: npm outdated || true

      - name: Create PR for dependency updates
        if: github.event_name == 'schedule'
        uses: dependabot/fetch-metadata@v1

  secret-scan:
    name: Secret Scanning
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_ENABLE_SUMMARY: true

  # Build Stage
  docker-build:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    needs: [unit-test, integration-test, sast-scan, dependency-audit, secret-scan]
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v'))
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.DOCKER_REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            NODE_VERSION=${{ env.NODE_VERSION }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VCS_REF=${{ github.sha }}

      - name: Scan Docker image with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy scan results
        if: always()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: trivy-results.sarif

  # Deploy Stage
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: docker-build
    environment:
      name: staging
      url: https://staging-api.company.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/payment-service \
            payment-service=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

          kubectl rollout status deployment/payment-service --namespace=staging --timeout=5m

      - name: Run database migrations
        run: |
          kubectl exec -n staging deployment/payment-service -- npm run migrate
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL_STAGING }}

      - name: Health check
        run: |
          for i in {1..10}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://staging-api.company.com/health)
            if [ $STATUS -eq 200 ]; then
              echo "✅ Health check passed"
              exit 0
            fi
            echo "⏳ Waiting for service... ($i/10)"
            sleep 30
          done
          echo "❌ Health check failed"
          exit 1

      - name: Warm up cache
        run: |
          kubectl exec -n staging deployment/payment-service -- npm run cache:warmup

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://api.company.com
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}

      - name: Create deployment backup
        run: |
          kubectl get deployment payment-service -n production -o yaml > deployment-backup-${{ github.sha }}.yaml

      - name: Deploy to Kubernetes (Canary Strategy)
        run: |
          # Deploy canary version (10% traffic)
          kubectl set image deployment/payment-service-canary \
            payment-service=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

          kubectl rollout status deployment/payment-service-canary -n production --timeout=5m

      - name: Monitor canary metrics
        run: |
          echo "⏳ Monitoring canary deployment for 5 minutes..."
          sleep 300

          # Check error rate from Prometheus/CloudWatch
          ERROR_RATE=$(curl -s "http://prometheus.company.internal/api/v1/query?query=rate(http_errors_total[5m])" | jq '.data.result[0].value[1]' -r)

          if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
            echo "❌ Error rate ${ERROR_RATE}% exceeds threshold 5%"
            echo "🔄 Rolling back canary deployment"
            kubectl rollout undo deployment/payment-service-canary -n production
            exit 1
          fi

          echo "✅ Canary metrics healthy, proceeding with full rollout"

      - name: Full production rollout
        run: |
          kubectl set image deployment/payment-service \
            payment-service=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

          kubectl rollout status deployment/payment-service -n production --timeout=10m

      - name: Run database migrations
        run: |
          kubectl exec -n production deployment/payment-service -- npm run migrate
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Production health check
        run: |
          for i in {1..15}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.company.com/health)
            if [ $STATUS -eq 200 ]; then
              echo "✅ Production health check passed"
              exit 0
            fi
            echo "⏳ Waiting for service... ($i/15)"
            sleep 60
          done
          echo "❌ Production health check failed - ROLLING BACK"
          kubectl rollout undo deployment/payment-service -n production
          exit 1

      - name: Warm up production cache
        run: |
          kubectl exec -n production deployment/payment-service -- npm run cache:warmup

      - name: Notify stakeholders
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "✅ Production Deployment Successful",
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": "🚀 Payment Service Deployed to Production"
                  }
                },
                {
                  "type": "section",
                  "fields": [
                    {
                      "type": "mrkdwn",
                      "text": "*Version:*\n${{ github.sha }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Deployed by:*\n${{ github.actor }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Commit:*\n<${{ github.event.head_commit.url }}|${{ github.event.head_commit.message }}>"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*URL:*\n<https://api.company.com|Production>"
                    }
                  ]
                }
              ]
            }

      - name: Create deployment record
        if: success()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.repos.createDeployment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: context.sha,
              environment: 'production',
              auto_merge: false,
              required_contexts: []
            });

  # Failure notification
  notify-failure:
    name: Notify on Failure
    runs-on: ubuntu-latest
    needs: [lint, type-check, unit-test, integration-test, sast-scan, dependency-audit, docker-build, deploy-staging, deploy-production]
    if: failure()
    steps:
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "❌ CI/CD Pipeline Failed",
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": "⚠️ Payment Service Pipeline Failure"
                  }
                },
                {
                  "type": "section",
                  "fields": [
                    {
                      "type": "mrkdwn",
                      "text": "*Branch:*\n${{ github.ref_name }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Triggered by:*\n${{ github.actor }}"
                    },
                    {
                      "type": "mrkdwn",
                      "text": "*Workflow:*\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                    }
                  ]
                },
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "<!channel> @team-backend @oncall - Pipeline failed, please investigate"
                  }
                }
              ]
            }

      - name: Create failure issue
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `CI/CD Pipeline Failure - ${context.sha.substring(0, 7)}`,
              body: `## Pipeline Failure Report\n\n**Workflow:** ${context.workflow}\n**Run:** ${context.runId}\n**Branch:** ${context.ref}\n**Commit:** ${context.sha}\n**Actor:** ${context.actor}\n\n[View workflow run](${context.serverUrl}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId})`,
              labels: ['ci-failure', 'needs-investigation'],
              assignees: ['team-lead']
            });
```

**Output Metadata**:

```typescript
{
  config: {
    filePath: '.github/workflows/ci-cd.yml',
    content: '...' // as shown above
    valid: true,
    errors: []
  },

  additionalFiles: [
    {
      path: '.github/dependabot.yml',
      content: `version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10`,
      description: 'Dependabot configuration for automated dependency updates'
    },
    {
      path: '.dockerignore',
      content: `node_modules
npm-debug.log
.git
.env
coverage
*.md`,
      description: 'Docker ignore file to reduce image size'
    }
  ],

  metadata: {
    platform: 'github-actions',
    estimatedBuildTime: {
      min: 8,
      max: 15,
      withCache: 4
    },
    costEstimate: {
      perBuild: 0,
      monthly: 0,
      currency: 'USD',
      assumptions: [
        'Public repository (free GitHub Actions)',
        'Estimated 50 builds/month',
        'Average 10 minutes per build'
      ]
    },
    jobCount: 15,
    stageCount: 5,
    maxParallelJobs: 5
  },

  security: {
    score: 95,
    features: [
      'SAST scanning with Semgrep',
      'Dependency vulnerability scanning',
      'Secret detection with Gitleaks',
      'Container image scanning with Trivy',
      'Automated security updates via Dependabot'
    ],
    recommendations: [
      '✅ All critical security checks enabled',
      '✅ Secret scanning prevents credential leaks',
      '✅ Container images scanned before deployment',
      '💡 Consider adding DAST scanning for runtime vulnerabilities',
      '💡 Enable GitHub Advanced Security for private repositories'
    ],
    secretsDetected: []
  },

  optimization: {
    cachingEnabled: true,
    estimatedCacheHitRate: 80,
    cachingTimeSaving: 6, // minutes per build
    parallelJobsCount: 5,
    appliedOptimizations: [
      'NPM dependency caching (cache hit rate ~80%)',
      'Docker layer caching with GitHub Actions cache',
      'Parallel execution of lint, type-check, and security scans',
      'Matrix build for Node.js 18 and 20',
      'Multi-arch Docker builds (amd64, arm64) in single job'
    ],
    suggestions: [
      '💡 Consider caching Playwright browser binaries',
      '💡 Use self-hosted runners for faster builds if budget allows',
      '💡 Implement smart test selection to run only affected tests'
    ]
  },

  bestPractices: {
    score: 92,
    checks: [
      {
        name: 'Dependency caching',
        passed: true,
        severity: 'info',
        message: 'NPM dependencies are cached for faster builds'
      },
      {
        name: 'Security scanning',
        passed: true,
        severity: 'info',
        message: 'Multiple security scans configured (SAST, dependency, secrets, container)'
      },
      {
        name: 'Test coverage threshold',
        passed: true,
        severity: 'info',
        message: 'Coverage threshold set to 85%'
      },
      {
        name: 'Production deployment approval',
        passed: true,
        severity: 'info',
        message: 'Manual approval required for production deployments'
      },
      {
        name: 'Health checks',
        passed: true,
        severity: 'info',
        message: 'Health checks configured for both staging and production'
      },
      {
        name: 'Automated rollback',
        passed: true,
        severity: 'info',
        message: 'Canary deployment with automatic rollback on errors'
      },
      {
        name: 'Hardcoded secrets',
        passed: false,
        severity: 'warning',
        message: 'Ensure all secrets use ${{ secrets.* }} syntax',
        fix: 'Replace any hardcoded values with GitHub Secrets'
      }
    ]
  },

  setup: {
    prerequisites: [
      'GitHub repository with admin access',
      'Kubernetes cluster with kubectl access',
      'Container registry (GitHub Container Registry recommended)',
      'Slack webhook URL for notifications (optional)',
      'Codecov account for coverage reporting (optional)'
    ],

    steps: [
      {
        order: 1,
        title: 'Configure GitHub Secrets',
        description: 'Add required secrets in repository settings',
        commands: [
          'Go to Settings > Secrets and variables > Actions',
          'Add new repository secrets as listed below'
        ]
      },
      {
        order: 2,
        title: 'Commit workflow file',
        description: 'Add the generated workflow to your repository',
        commands: [
          'mkdir -p .github/workflows',
          'cp ci-cd.yml .github/workflows/',
          'git add .github/workflows/ci-cd.yml',
          'git commit -m "ci: add GitHub Actions CI/CD pipeline"',
          'git push'
        ]
      },
      {
        order: 3,
        title: 'Configure environments',
        description: 'Set up staging and production environments with protection rules',
        commands: [
          'Go to Settings > Environments',
          'Create "staging" environment',
          'Create "production" environment with required reviewers'
        ]
      },
      {
        order: 4,
        title: 'Verify pipeline execution',
        description: 'Check that the workflow runs successfully',
        commands: [
          'Go to Actions tab in GitHub',
          'Monitor the first pipeline run',
          'Fix any configuration issues'
        ]
      }
    ],

    requiredSecrets: [
      {
        name: 'KUBE_CONFIG_STAGING',
        description: 'Base64-encoded kubeconfig for staging Kubernetes cluster',
        example: 'cat ~/.kube/staging-config | base64',
        required: true
      },
      {
        name: 'KUBE_CONFIG_PROD',
        description: 'Base64-encoded kubeconfig for production Kubernetes cluster',
        example: 'cat ~/.kube/prod-config | base64',
        required: true
      },
      {
        name: 'DATABASE_URL_STAGING',
        description: 'PostgreSQL connection string for staging',
        example: 'postgresql://user:pass@staging-db.example.com:5432/payment',
        required: true
      },
      {
        name: 'DATABASE_URL',
        description: 'PostgreSQL connection string for production',
        example: 'postgresql://user:pass@prod-db.example.com:5432/payment',
        required: true
      },
      {
        name: 'STRIPE_API_KEY',
        description: 'Stripe API key for production',
        required: true
      },
      {
        name: 'SLACK_WEBHOOK',
        description: 'Slack webhook URL for notifications',
        example: 'https://hooks.slack.com/services/T00000000/B00000000/XXXX',
        required: false
      },
      {
        name: 'GITHUB_TOKEN',
        description: 'Automatically provided by GitHub Actions',
        required: false
      }
    ],

    documentation: [
      'https://docs.github.com/en/actions',
      'https://docs.docker.com/build/ci/github-actions/',
      'https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/'
    ]
  },

  validation: {
    localTest: 'act -j unit-test',  // Using 'act' to test GitHub Actions locally
    dryRun: 'gh workflow run ci-cd.yml --ref $(git branch --show-current)',
    checklist: [
      '✅ Workflow syntax is valid YAML',
      '✅ All required secrets are configured',
      '✅ Environment protection rules are set',
      '✅ Docker registry authentication works',
      '✅ Kubernetes credentials are valid',
      '✅ Health check URLs are accessible',
      '✅ Notification webhooks are working',
      '✅ Test coverage meets threshold',
      '✅ Security scans complete successfully',
      '✅ Deployment to staging succeeds',
      '✅ Production deployment requires approval'
    ]
  }
}
```

**Performance Impact**:
- **Build time**: 8-15 minutes without cache, 4-6 minutes with cache (60% improvement)
- **Parallel efficiency**: 5 jobs run concurrently, reducing total time by ~40%
- **Cache hit rate**: ~80% for dependencies, saving 6 minutes per build
- **Multi-arch builds**: 2 architectures (amd64, arm64) in single job using QEMU

---

### Example 2: GitLab CI - Python Django Microservice with PostgreSQL

**Scenario**: Create a GitLab CI pipeline for a Django REST API with database migrations, pytest testing, Docker build to AWS ECR, and deployment to ECS.

**Input**:

```typescript
const input: CICDPipelineBuilderInput = {
  platform: 'gitlab-ci',
  language: 'python',
  framework: {
    name: 'django',
    version: '3.11',
    buildTool: 'pip'
  },

  stages: [
    {
      name: 'test',
      jobs: [
        { name: 'pytest', steps: ['pytest', 'coverage'] },
        { name: 'flake8', steps: ['lint'] }
      ],
      parallel: true
    },
    {
      name: 'security',
      jobs: [
        { name: 'bandit', steps: ['security-scan'] },
        { name: 'safety', steps: ['dependency-check'] }
      ],
      parallel: true
    },
    {
      name: 'build',
      jobs: [
        { name: 'docker-build', steps: ['docker-build', 'ecr-push'] }
      ]
    },
    {
      name: 'deploy',
      jobs: [
        { name: 'deploy-ecs', steps: ['ecs-deploy'], environment: 'production' }
      ]
    }
  ],

  testing: {
    unit: {
      command: 'pytest tests/ -v --cov=app --cov-report=xml',
      coverage: {
        enabled: true,
        threshold: 80,
        report: 'codecov'
      }
    }
  },

  build: {
    type: 'docker',
    dockerfile: 'Dockerfile',
    registry: {
      provider: 'ecr',
      repository: '123456789012.dkr.ecr.us-east-1.amazonaws.com/django-api',
      tagStrategy: 'commit-sha'
    }
  },

  security: {
    sast: {
      enabled: true,
      tool: 'semgrep',
      severityThreshold: 'high'
    },
    dependencyCheck: {
      enabled: true,
      tool: 'snyk'
    }
  },

  deployment: {
    targets: [
      {
        environment: 'production',
        platform: 'aws-ecs',
        strategy: 'rolling-update',
        secrets: ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'],
        healthCheck: {
          url: 'https://api.example.com/health',
          timeout: 60,
          retries: 3
        },
        postDeploy: {
          runMigrations: true
        }
      }
    ]
  },

  optimization: {
    caching: {
      dependencies: true,
      docker: {
        layers: true
      }
    }
  },

  notifications: {
    slack: {
      webhookUrl: '$SLACK_WEBHOOK_URL',
      events: ['failure', 'deployment']
    }
  },

  triggers: {
    branches: ['main', 'develop']
  }
};
```

**Output**:

```yaml
# .gitlab-ci.yml
image: python:3.11-slim

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DOCKER_DRIVER: overlay2
  AWS_DEFAULT_REGION: us-east-1
  ECR_REGISTRY: 123456789012.dkr.ecr.us-east-1.amazonaws.com
  IMAGE_NAME: django-api

cache:
  key: "${CI_COMMIT_REF_SLUG}"
  paths:
    - .cache/pip
    - venv/

stages:
  - test
  - security
  - build
  - deploy

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install --upgrade pip
  - pip install -r requirements.txt

# Test Stage
pytest:
  stage: test
  services:
    - postgres:14
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_pass
    DATABASE_URL: postgresql://test_user:test_pass@postgres:5432/test_db
  script:
    - python manage.py migrate --no-input
    - pytest tests/ -v --cov=app --cov-report=xml --cov-report=html
    - coverage report --fail-under=80
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
    paths:
      - htmlcov/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

flake8:
  stage: test
  script:
    - pip install flake8
    - flake8 app/ --max-line-length=120 --statistics
  only:
    - main
    - develop
    - merge_requests

# Security Stage
bandit:
  stage: security
  script:
    - pip install bandit
    - bandit -r app/ -f json -o bandit-report.json
  artifacts:
    reports:
      sast: bandit-report.json
    expire_in: 1 week
  allow_failure: false
  only:
    - main
    - develop

safety:
  stage: security
  script:
    - pip install safety
    - safety check --json --output safety-report.json
  artifacts:
    paths:
      - safety-report.json
    expire_in: 1 week
  allow_failure: false
  only:
    - main
    - develop

semgrep:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config=auto --json --output=semgrep.json app/
  artifacts:
    reports:
      sast: semgrep.json
    expire_in: 1 week
  only:
    - main
    - develop

# Build Stage
docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - apk add --no-cache python3 py3-pip
    - pip3 install awscli
    - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
  script:
    - docker build --cache-from $ECR_REGISTRY/$IMAGE_NAME:latest -t $ECR_REGISTRY/$IMAGE_NAME:$CI_COMMIT_SHA -t $ECR_REGISTRY/$IMAGE_NAME:latest .
    - docker push $ECR_REGISTRY/$IMAGE_NAME:$CI_COMMIT_SHA
    - docker push $ECR_REGISTRY/$IMAGE_NAME:latest
  only:
    - main

# Deploy Stage
deploy-ecs:
  stage: deploy
  image: python:3.11-slim
  before_script:
    - pip install awscli
  script:
    # Update ECS task definition with new image
    - |
      TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition django-api-task --region $AWS_DEFAULT_REGION)
      NEW_TASK_DEF=$(echo $TASK_DEFINITION | jq --arg IMAGE "$ECR_REGISTRY/$IMAGE_NAME:$CI_COMMIT_SHA" '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) | del(.registeredAt) | del(.registeredBy)')
      NEW_TASK_INFO=$(aws ecs register-task-definition --region $AWS_DEFAULT_REGION --cli-input-json "$NEW_TASK_DEF")
      NEW_REVISION=$(echo $NEW_TASK_INFO | jq '.taskDefinition.revision')

    # Update ECS service
    - aws ecs update-service --cluster django-api-cluster --service django-api-service --task-definition django-api-task:$NEW_REVISION --region $AWS_DEFAULT_REGION

    # Wait for deployment to complete
    - aws ecs wait services-stable --cluster django-api-cluster --services django-api-service --region $AWS_DEFAULT_REGION

    # Run database migrations
    - |
      TASK_ARN=$(aws ecs run-task \
        --cluster django-api-cluster \
        --task-definition django-api-task:$NEW_REVISION \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
        --overrides '{"containerOverrides":[{"name":"django-api","command":["python","manage.py","migrate","--no-input"]}]}' \
        --region $AWS_DEFAULT_REGION | jq -r '.tasks[0].taskArn')

      aws ecs wait tasks-stopped --cluster django-api-cluster --tasks $TASK_ARN --region $AWS_DEFAULT_REGION

    # Health check
    - |
      for i in {1..10}; do
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
        if [ $STATUS -eq 200 ]; then
          echo "✅ Health check passed"
          exit 0
        fi
        echo "⏳ Waiting for service... ($i/10)"
        sleep 30
      done
      echo "❌ Health check failed"
      exit 1
  environment:
    name: production
    url: https://api.example.com
  only:
    - main
  when: manual

# Notification on failure
notify-failure:
  stage: .post
  image: curlimages/curl:latest
  script:
    - |
      curl -X POST $SLACK_WEBHOOK_URL \
        -H 'Content-Type: application/json' \
        -d "{\"text\":\"❌ GitLab CI Pipeline Failed\n*Project:* $CI_PROJECT_NAME\n*Branch:* $CI_COMMIT_REF_NAME\n*Commit:* $CI_COMMIT_SHORT_SHA\n*URL:* $CI_PIPELINE_URL\"}"
  when: on_failure
  only:
    - main
    - develop
```

**Key Features**:
- **Service containers**: PostgreSQL for integration tests
- **Multi-stage pipeline**: test → security → build → deploy
- **AWS ECS deployment**: Task definition update + service rolling update
- **Database migrations**: Run as ECS task after deployment
- **Coverage reporting**: Built-in GitLab coverage tracking
- **Docker layer caching**: Speeds up builds by 50%

---

### Example 3: Jenkins Pipeline - Java Spring Boot Microservice

**Scenario**: Create a Jenkinsfile for a Java Spring Boot application with Maven, JUnit tests, SonarQube analysis, Docker build to Artifactory, and deployment to Kubernetes.

**Input**:

```typescript
const input: CICDPipelineBuilderInput = {
  platform: 'jenkins',
  language: 'java',
  framework: {
    name: 'spring-boot',
    version: '17',
    buildTool: 'maven'
  },

  stages: [
    {
      name: 'Build',
      jobs: [{ name: 'maven-build', steps: ['mvn-clean', 'mvn-package'] }]
    },
    {
      name: 'Test',
      jobs: [
        { name: 'unit-tests', steps: ['mvn-test'] },
        { name: 'integration-tests', steps: ['mvn-verify'] }
      ]
    },
    {
      name: 'Quality',
      jobs: [
        { name: 'sonarqube', steps: ['sonar-scan'] }
      ]
    },
    {
      name: 'Security',
      jobs: [
        { name: 'owasp-scan', steps: ['dependency-check'] }
      ]
    },
    {
      name: 'Package',
      jobs: [
        { name: 'docker-build', steps: ['docker-build', 'docker-push'] }
      ]
    },
    {
      name: 'Deploy',
      jobs: [
        { name: 'k8s-deploy', steps: ['kubectl-apply'], environment: 'production' }
      ]
    }
  ],

  testing: {
    unit: {
      command: 'mvn test',
      coverage: {
        enabled: true,
        threshold: 75,
        report: 'sonarqube'
      }
    },
    integration: {
      command: 'mvn verify -Pintegration-tests'
    }
  },

  build: {
    type: 'docker',
    dockerfile: 'Dockerfile',
    registry: {
      provider: 'dockerhub',
      repository: 'company/spring-boot-api',
      tagStrategy: 'semver'
    }
  },

  security: {
    sast: {
      enabled: true,
      tool: 'sonarqube'
    },
    dependencyCheck: {
      enabled: true
    }
  },

  deployment: {
    targets: [
      {
        environment: 'production',
        platform: 'kubernetes',
        strategy: 'rolling-update',
        requiresApproval: true,
        healthCheck: {
          url: 'https://api.company.com/actuator/health',
          timeout: 60,
          retries: 5
        }
      }
    ]
  },

  notifications: {
    email: {
      recipients: ['team@company.com'],
      events: ['failure', 'deployment']
    }
  }
};
```

**Output**:

```groovy
// Jenkinsfile
pipeline {
    agent {
        label 'docker'
    }

    environment {
        MAVEN_OPTS = '-Xmx3072m -Xms1024m'
        JAVA_HOME = '/usr/lib/jvm/java-17-openjdk'
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'company/spring-boot-api'
        KUBE_NAMESPACE = 'production'
        SONAR_HOST_URL = 'https://sonarqube.company.com'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }

    tools {
        maven 'Maven 3.9.0'
        jdk 'OpenJDK 17'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    env.VERSION = sh(returnStdout: true, script: 'mvn help:evaluate -Dexpression=project.version -q -DforceStdout').trim()
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'mvn clean package -DskipTests -T 4'
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'mvn test -T 4'
                    }
                    post {
                        always {
                            junit testResults: '**/target/surefire-reports/*.xml', allowEmptyResults: true
                            jacoco(
                                execPattern: '**/target/jacoco.exec',
                                classPattern: '**/target/classes',
                                sourcePattern: '**/src/main/java',
                                minimumLineCoverage: '75',
                                failOnMissingReports: true
                            )
                        }
                    }
                }

                stage('Integration Tests') {
                    steps {
                        sh 'mvn verify -Pintegration-tests'
                    }
                    post {
                        always {
                            junit testResults: '**/target/failsafe-reports/*.xml', allowEmptyResults: true
                        }
                    }
                }
            }
        }

        stage('Quality Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        mvn sonar:sonar \
                            -Dsonar.projectKey=spring-boot-api \
                            -Dsonar.projectName=spring-boot-api \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN \
                            -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('OWASP Dependency Check') {
                    steps {
                        dependencyCheck additionalArguments: '''
                            --scan .
                            --format ALL
                            --failOnCVSS 7
                            --suppression dependency-check-suppressions.xml
                        ''', odcInstallation: 'OWASP Dependency-Check'

                        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                    }
                }

                stage('Trivy Filesystem Scan') {
                    steps {
                        sh '''
                            trivy fs --severity HIGH,CRITICAL --format json -o trivy-report.json .
                        '''
                    }
                }
            }
        }

        stage('Docker Build') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-hub-credentials') {
                        def app = docker.build("${IMAGE_NAME}:${VERSION}-${GIT_COMMIT_SHORT}", "--build-arg JAR_FILE=target/*.jar .")
                        app.push()
                        app.push('latest')
                    }
                }
            }
        }

        stage('Container Security Scan') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    trivy image --severity HIGH,CRITICAL --format json -o trivy-image-report.json ${IMAGE_NAME}:${VERSION}-${GIT_COMMIT_SHORT}
                """
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy', submitter: 'admin,devops-team'

                withKubeConfig([credentialsId: 'kube-config-prod']) {
                    sh """
                        # Update deployment image
                        kubectl set image deployment/spring-boot-api \
                            spring-boot-api=${IMAGE_NAME}:${VERSION}-${GIT_COMMIT_SHORT} \
                            --namespace=${KUBE_NAMESPACE}

                        # Wait for rollout to complete
                        kubectl rollout status deployment/spring-boot-api \
                            --namespace=${KUBE_NAMESPACE} \
                            --timeout=5m
                    """
                }
            }
        }

        stage('Health Check') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def healthUrl = 'https://api.company.com/actuator/health'
                    def retries = 10
                    def delay = 30

                    for (int i = 1; i <= retries; i++) {
                        def response = sh(returnStatus: true, script: "curl -f -s ${healthUrl}")
                        if (response == 0) {
                            echo "✅ Health check passed"
                            return
                        }
                        echo "⏳ Waiting for service... (${i}/${retries})"
                        sleep(delay)
                    }
                    error("❌ Health check failed after ${retries} attempts")
                }
            }
        }

        stage('Smoke Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'mvn test -Psmoke-tests -Dtest.environment=production'
            }
        }
    }

    post {
        always {
            // Cleanup workspace
            cleanWs()
        }

        success {
            emailext(
                subject: "✅ Jenkins Build #${BUILD_NUMBER} - SUCCESS",
                body: """
                    <h2>Build Successful</h2>
                    <p><b>Job:</b> ${JOB_NAME}</p>
                    <p><b>Build Number:</b> ${BUILD_NUMBER}</p>
                    <p><b>Version:</b> ${VERSION}</p>
                    <p><b>Commit:</b> ${GIT_COMMIT_SHORT}</p>
                    <p><b>URL:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                """,
                to: 'team@company.com',
                mimeType: 'text/html'
            )
        }

        failure {
            emailext(
                subject: "❌ Jenkins Build #${BUILD_NUMBER} - FAILED",
                body: """
                    <h2>Build Failed</h2>
                    <p><b>Job:</b> ${JOB_NAME}</p>
                    <p><b>Build Number:</b> ${BUILD_NUMBER}</p>
                    <p><b>Commit:</b> ${GIT_COMMIT_SHORT}</p>
                    <p><b>URL:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><b>Console Output:</b> <a href="${BUILD_URL}console">${BUILD_URL}console</a></p>
                """,
                to: 'team@company.com',
                mimeType: 'text/html'
            )
        }
    }
}
```

**Key Features**:
- **Parallel testing**: Unit and integration tests run simultaneously
- **SonarQube integration**: Code quality gate blocks deployment if quality drops
- **OWASP Dependency Check**: Fails build on CVSS ≥7 vulnerabilities
- **Manual approval**: Production deployment requires explicit approval
- **Health checks**: Spring Boot Actuator endpoints monitored
- **Comprehensive reporting**: JUnit, JaCoCo coverage, SonarQube, OWASP reports

---

## Best Practices

### DO ✅

```yaml
# DO: Cache dependencies aggressively
cache:
  key: "${CI_COMMIT_REF_SLUG}"
  paths:
    - node_modules/
    - .npm/
    - .cache/

# DO: Use matrix builds for multi-version support
strategy:
  matrix:
    node-version: [16, 18, 20]
    os: [ubuntu-latest, windows-latest]

# DO: Fail fast on critical issues
- name: Security scan
  run: npm audit --audit-level=critical
  # Build stops immediately on critical vulnerabilities

# DO: Separate concerns with multiple jobs
jobs:
  lint:      # Fast feedback (< 1 min)
  test:      # Moderate (2-5 min)
  build:     # Slower (5-10 min)
  deploy:    # Manual approval

# DO: Use secrets management properly
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  # Never: DATABASE_URL: postgresql://user:password@host

# DO: Implement automated rollback
- name: Deploy with rollback
  run: |
    kubectl apply -f deployment.yaml
    kubectl rollout status deployment/app --timeout=5m || \
      (kubectl rollout undo deployment/app && exit 1)

# DO: Add health checks after deployment
- name: Health check
  run: |
    for i in {1..10}; do
      curl -f https://api.com/health && exit 0
      sleep 30
    done
    exit 1

# DO: Tag Docker images semantically
tags: |
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
  type=sha,prefix={{branch}}-

# DO: Use multi-stage Docker builds
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-slim
COPY --from=builder /app/node_modules ./node_modules
# Final image is 70% smaller

# DO: Run tests in parallel when possible
jobs:
  unit-test:
  integration-test:
  e2e-test:
# All run concurrently, saving 60% total time

# DO: Set appropriate timeouts
timeout-minutes: 30
# Prevents stuck jobs from wasting resources

# DO: Use conditional execution
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
# Avoid unnecessary runs

# DO: Collect and archive artifacts
- name: Archive production artifacts
  uses: actions/upload-artifact@v3
  with:
    name: dist
    path: dist/
    retention-days: 7
```

### DON'T ❌

```yaml
# DON'T: Hardcode secrets in workflows
env:
  API_KEY: "sk_live_abc123xyz"  # ❌ NEVER DO THIS
  # Use: API_KEY: ${{ secrets.API_KEY }}

# DON'T: Run all tests sequentially
- run: npm run lint
- run: npm run test:unit
- run: npm run test:integration
# Wastes time; use parallel jobs instead

# DON'T: Skip security scans to save time
# - run: npm audit  # ❌ Commented out
# Security is not optional

# DON'T: Deploy directly to production without gates
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: kubectl apply -f prod.yaml  # ❌ No approval, no staging
# Add environment protection rules

# DON'T: Ignore cache to "avoid stale dependencies"
# - uses: actions/cache@v3  # ❌ Disabled
# Cache is safe with proper cache keys

# DON'T: Use overly broad triggers
on: [push, pull_request, release, create, delete]  # ❌ Runs on everything
# Be specific: on: push: branches: [main]

# DON'T: Build Docker images on every commit
- name: Build Docker
  run: docker build -t app:latest .  # ❌ Even on feature branches
# Use: if: github.ref == 'refs/heads/main'

# DON'T: Ignore exit codes
- run: npm test || true  # ❌ Always succeeds
# Let tests fail the pipeline

# DON'T: Use mutable tags in production
docker pull myapp:latest  # ❌ "latest" can change unexpectedly
# Use: docker pull myapp:v1.2.3 or myapp:sha-abc123

# DON'T: Run long-running tasks without timeout
- run: npm run build  # ❌ Could hang forever
# Use: timeout-minutes: 15

# DON'T: Pollute logs with excessive output
- run: npm install --verbose  # ❌ 10,000 lines of noise
# Use: npm install (only show errors)

# DON'T: Store artifacts indefinitely
retention-days: 365  # ❌ Wastes storage
# Use: retention-days: 7 or 14

# DON'T: Mix staging and production credentials
env:
  API_KEY: ${{ secrets.API_KEY }}  # ❌ Same for all environments
# Use: API_KEY_STAGING, API_KEY_PROD

# DON'T: Skip code review for CI changes
.gitlab-ci.yml changes → Direct push to main  # ❌
# Pipeline configs are code; require review

# DON'T: Use self-signed certificates without verification
curl -k https://api.internal.com  # ❌ -k disables cert check
# Properly configure CA certificates
```

---

## Related Skills

- **deployment-orchestrator** (Skill 23): Handles the actual deployment execution across Kubernetes, AWS Lambda, GCP Cloud Run using strategies like canary, blue-green, rolling updates
- **infrastructure-coder** (Skill 24): Generates Terraform/CloudFormation IaC that the CI/CD pipeline can apply to provision infrastructure
- **test-generator** (Skill 3): Creates comprehensive unit, integration, and E2E tests that are executed in the pipeline's test stage
- **security-scanner** (Skill 8): Provides SAST, DAST, dependency scanning capabilities integrated into CI/CD security stages
- **code-reviewer** (Skill 4): Automated code review that runs as part of PR validation before merging
- **docker-file-generator**: Generates optimized multi-stage Dockerfiles used in the build stage
- **performance-monitor** (Skill 10): Tracks build times, deployment metrics, and provides optimization recommendations
- **knowledge-manager** (Skill 30): Documents CI/CD pipeline architecture and runbooks for troubleshooting

---

## Changelog

### Version 2.0.0 (2025-01-12)
- Initial release of CI/CD Pipeline Builder
- Multi-platform support: GitHub Actions, GitLab CI, Jenkins, Azure Pipelines
- Comprehensive security integration: SAST, DAST, dependency scanning, secret detection, container scanning
- Advanced deployment strategies: blue-green, canary, rolling updates with automated rollback
- Performance optimizations: intelligent caching, parallel job execution, matrix builds
- Complete TypeScript interfaces with 45+ configuration options
- Three detailed production-ready examples (Node.js/GitHub Actions, Python/GitLab CI, Java/Jenkins)
- Best practices documentation with DO/DON'T comparisons
- Notification integrations: Slack, Email, Teams with customizable event
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
interface CICDPipelineBuilderInput {
}
```

### 输出接口

```typescript
interface CICDPipelineBuilderOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

 triggers
