---
name: 31-risk-assessor-G
description: Project risk identification and assessment tool for technical debt analysis, security vulnerability scanning, dependency health checks, compliance validation, risk mitigation strategies. Quantifies risks through probability-impact matrix (0-100 score), integrates CVE database, OWASP Top 10, GDPR/SOC2/HIPAA standards. Auto-identifies code/architecture/dependency/team risks, generates prioritized fix recommendations (P0/P1/P2/P3) with cost estimates. Use for project kickoff risk assessment, pre-release security audits, technical debt analysis, compliance checks.
---

# Risk Assessor - 项目风险评估器

**Version**: 2.0.0
**Category**: Project Management
**Priority**: P1
**Last Updated**: 2025-12-12

---

## Description

项目风险识别与评估工具,提供技术债务分析、安全漏洞扫描、依赖健康检查、合规性验证和风险缓解策略。通过概率-影响矩阵量化风险,结合CVE数据库、OWASP Top 10、GDPR/SOC2标准,自动识别代码、架构、依赖和团队风险,生成优先级修复建议,确保项目健康和合规。

### Core Capabilities

- **Risk Identification**: 从代码、架构、依赖、团队、流程中自动识别风险点,支持多维度扫描(技术债务、安全、性能、合规、团队能力)
- **Priority Assessment**: 概率-影响矩阵评估、风险评分(0-100)、紧急度排序(P0/P1/P2/P3)、CVSS评分集成、业务影响分析
- **Technical Debt Analysis**: 代码质量评分(Code Smell检测)、重构成本估算、债务趋势分析、SonarQube集成、复杂度热力图
- **Security Assessment**: CVE漏洞扫描、OWASP Top 10检查、依赖安全审计、Secret泄露检测、合规性验证(GDPR/SOC2/HIPAA)
- **Dependency Health**: 过时依赖检测、许可证冲突分析、供应链安全评估、破坏性更新识别、Renovate/Dependabot集成
- **Mitigation Recommendations**: 自动生成风险缓解策略、优先修复建议、成本-收益分析、时间线估算、资源分配建议

---

## Instructions

### When to Activate

Trigger this skill when you encounter:

1. **Project Kickoff** - 新项目启动前评估技术风险和可行性
2. **Pre-Production Review** - 上线前全面风险审查
3. **Security Incident** - 发现安全漏洞需要评估影响范围和缓解方案
4. **Technical Debt Accumulation** - 代码质量下降、测试覆盖率不足、遗留代码积累
5. **Dependency Upgrade** - 大版本依赖升级前评估破坏性变更风险
6. **Compliance Audit** - GDPR/SOC2/HIPAA合规性审计
7. **Team Changes** - 关键开发者离职、团队扩张前评估知识风险
8. **Architecture Review** - 扩展性瓶颈、单点故障、性能问题评估

**Common trigger phrases**:
- "评估这个项目的技术风险"
- "扫描安全漏洞并优先级排序"
- "分析技术债务并估算重构成本"
- "检查依赖是否有安全问题"
- "GDPR合规性检查"
- "评估微服务迁移的风险"

### Execution Flow

```mermaid
graph TD
    A[接收风险评估任务] --> B{扫描范围}

    B -->|代码分析| C[代码质量扫描]
    B -->|依赖分析| D[依赖健康检查]
    B -->|安全分析| E[安全漏洞扫描]
    B -->|架构分析| F[架构风险评估]
    B -->|合规分析| G[合规性检查]

    C --> C1[SonarQube/CodeClimate]
    C1 --> C2[技术债务评分]
    C2 --> C3[Code Smell检测]
    C3 --> C4[复杂度分析]
    C4 --> C5[重复代码识别]

    D --> D1[npm audit/pip-audit]
    D1 --> D2[CVE数据库查询]
    D2 --> D3[许可证冲突检查]
    D3 --> D4[过时依赖识别]
    D4 --> D5[供应链安全分析]

    E --> E1[OWASP ZAP/Burp Suite]
    E1 --> E2[OWASP Top 10检查]
    E2 --> E3[Secret泄露扫描]
    E3 --> E4[SAST工具(Semgrep)]
    E4 --> E5[DAST工具(可选)]

    F --> F1[架构图分析]
    F1 --> F2[单点故障识别]
    F2 --> F3[扩展性评估]
    F3 --> F4[性能瓶颈分析]
    F4 --> F5[灾备方案检查]

    G --> G1[GDPR要求检查]
    G1 --> G2[数据加密验证]
    G2 --> G3[访问控制审计]
    G3 --> G4[日志留存检查]
    G4 --> G5[数据处理协议]

    C5 --> H[风险汇总]
    D5 --> H
    E5 --> H
    F5 --> H
    G5 --> H

    H --> I[概率-影响矩阵]
    I --> J[风险评分计算]
    J --> K[优先级排序]
    K --> L[生成缓解策略]
    L --> M[成本-收益分析]
    M --> N[生成行动计划]
    N --> O[返回风险报告]
```

---

## TypeScript Interfaces

```typescript
/**
 * Risk Assessor输入配置
 */
interface RiskAssessorInput {
  /**
   * 评估任务配置
   */
  task: {
    type:
      | 'comprehensive'         // 全面风险评估
      | 'security-only'         // 仅安全扫描
      | 'dependency-audit'      // 依赖审计
      | 'technical-debt'        // 技术债务分析
      | 'compliance-check'      // 合规性检查
      | 'architecture-review';  // 架构风险评估

    description?: string;
    scope?: string[];           // ['backend', 'frontend', 'infrastructure']
  };

  /**
   * 项目信息
   */
  project: {
    name: string;
    description?: string;
    criticality?: 'low' | 'medium' | 'high' | 'critical';  // 业务关键性
    stage?: 'planning' | 'development' | 'staging' | 'production';

    /**
     * 技术栈
     */
    techStack?: {
      languages?: string[];     // ['typescript', 'python', 'go']
      frameworks?: string[];    // ['react', 'express', 'django']
      databases?: string[];     // ['postgresql', 'redis', 'mongodb']
      infrastructure?: string[]; // ['kubernetes', 'aws', 'docker']
    };

    /**
     * 团队信息
     */
    team?: {
      size: number;
      experience?: 'junior' | 'mixed' | 'senior';
      keyPersonDependencies?: string[];  // 关键人员依赖
      turnoverRate?: number;   // 年流失率 (%)
    };
  };

  /**
   * 代码库信息
   */
  codebase?: {
    path?: string;
    gitRepo?: string;
    branch?: string;

    /**
     * 统计信息
     */
    stats?: {
      linesOfCode?: number;
      filesCount?: number;
      ageInYears?: number;
      commitsPerMonth?: number;
      contributors?: number;
    };
  };

  /**
   * 代码质量扫描配置
   */
  codeQuality?: {
    enabled: boolean;

    /**
     * 扫描工具
     */
    tools?: Array<'sonarqube' | 'codeclimate' | 'eslint' | 'ruff' | 'custom'>;

    /**
     * SonarQube配置
     */
    sonarqube?: {
      serverUrl: string;
      token: string;
      projectKey: string;
    };

    /**
     * 代码异味检测
     */
    codeSmells?: {
      enabled: boolean;
      thresholds?: {
        maxComplexity?: number;      // 圈复杂度阈值 (default: 10)
        maxFunctionLength?: number;  // 函数最大行数 (default: 50)
        maxFileSize?: number;        // 文件最大行数 (default: 500)
        duplicateCodePercent?: number; // 重复代码比例 (default: 3%)
      };
    };

    /**
     * 技术债务评估
     */
    technicalDebt?: {
      enabled: boolean;
      estimateMethod?: 'sonar' | 'code-age' | 'manual';
      hourlyRate?: number;          // 开发者时薪 (用于成本估算)
    };
  };

  /**
   * 依赖审计配置
   */
  dependencyAudit?: {
    enabled: boolean;

    /**
     * 审计工具
     */
    tools?: Array<'npm-audit' | 'pip-audit' | 'snyk' | 'dependabot'>;

    /**
     * CVE漏洞扫描
     */
    cveScanning?: {
      enabled: boolean;
      severityThreshold?: 'critical' | 'high' | 'medium' | 'low';
      ignoreCVEs?: string[];        // 忽略的CVE列表
    };

    /**
     * 许可证检查
     */
    licenseCheck?: {
      enabled: boolean;
      allowedLicenses?: string[];   // ['MIT', 'Apache-2.0', 'BSD-3-Clause']
      blockedLicenses?: string[];   // ['GPL-3.0', 'AGPL-3.0']
    };

    /**
     * 过时依赖检测
     */
    outdatedCheck?: {
      enabled: boolean;
      maxAgeMonths?: number;        // 最大允许过时时间 (月)
      checkMajorUpdates?: boolean;  // 检查主版本更新
    };

    /**
     * 供应链安全
     */
    supplyChain?: {
      enabled: boolean;
      checkMaintenance?: boolean;   // 检查依赖是否仍在维护
      checkPopularity?: boolean;    // 检查依赖流行度(下载量)
      minDownloadsPerMonth?: number; // 最低月下载量要求
    };
  };

  /**
   * 安全扫描配置
   */
  securityScan?: {
    enabled: boolean;

    /**
     * OWASP Top 10检查
     */
    owaspCheck?: {
      enabled: boolean;
      categories?: Array<
        | 'injection'               // SQL注入、XSS等
        | 'broken-authentication'   // 认证失效
        | 'sensitive-data-exposure' // 敏感数据泄露
        | 'xxe'                     // XML外部实体
        | 'broken-access-control'   // 访问控制失效
        | 'security-misconfiguration'
        | 'xss'
        | 'insecure-deserialization'
        | 'using-components-with-vulnerabilities'
        | 'insufficient-logging'
      >;
    };

    /**
     * SAST (Static Application Security Testing)
     */
    sast?: {
      enabled: boolean;
      tools?: Array<'semgrep' | 'bandit' | 'brakeman' | 'gosec'>;
    };

    /**
     * Secret泄露扫描
     */
    secretScanning?: {
      enabled: boolean;
      tools?: Array<'gitleaks' | 'truffleHog' | 'detect-secrets'>;
      patterns?: string[];          // 自定义secret正则
    };

    /**
     * DAST (Dynamic Application Security Testing)
     */
    dast?: {
      enabled: boolean;
      targetUrl?: string;
      tools?: Array<'owasp-zap' | 'burp-suite' | 'arachni'>;
    };
  };

  /**
   * 架构风险评估配置
   */
  architectureRisk?: {
    enabled: boolean;

    /**
     * 单点故障检测
     */
    singlePointOfFailure?: {
      enabled: boolean;
      checkDatabase?: boolean;
      checkCache?: boolean;
      checkQueue?: boolean;
      checkExternalAPIs?: boolean;
    };

    /**
     * 扩展性评估
     */
    scalability?: {
      enabled: boolean;
      currentLoad?: {
        requestsPerSecond?: number;
        concurrentUsers?: number;
        dataVolumeGB?: number;
      };
      projectedLoad?: {
        requestsPerSecond?: number;
        concurrentUsers?: number;
        dataVolumeGB?: number;
        timelineMonths?: number;
      };
    };

    /**
     * 性能瓶颈分析
     */
    performanceBottlenecks?: {
      enabled: boolean;
      checkDatabaseQueries?: boolean;
      checkAPILatency?: boolean;
      checkCachingStrategy?: boolean;
    };

    /**
     * 灾备方案
     */
    disasterRecovery?: {
      enabled: boolean;
      checkBackups?: boolean;
      checkReplication?: boolean;
      checkFailover?: boolean;
      rtoHours?: number;            // Recovery Time Objective
      rpoHours?: number;            // Recovery Point Objective
    };
  };

  /**
   * 合规性检查配置
   */
  complianceCheck?: {
    enabled: boolean;

    /**
     * 合规标准
     */
    standards: Array<'gdpr' | 'hipaa' | 'soc2' | 'pci-dss' | 'iso27001'>;

    /**
     * GDPR检查
     */
    gdpr?: {
      checkDataEncryption?: boolean;
      checkConsentManagement?: boolean;
      checkDataDeletion?: boolean;
      checkAccessControl?: boolean;
      checkAuditLogs?: boolean;
      checkDataPortability?: boolean;
    };

    /**
     * SOC2检查
     */
    soc2?: {
      checkSecurityControls?: boolean;
      checkAvailability?: boolean;
      checkConfidentiality?: boolean;
      checkProcessingIntegrity?: boolean;
      checkPrivacy?: boolean;
    };

    /**
     * HIPAA检查
     */
    hipaa?: {
      checkPHIEncryption?: boolean;
      checkAccessLogs?: boolean;
      checkBAA?: boolean;           // Business Associate Agreement
    };
  };

  /**
   * 风险评估参数
   */
  riskAssessment?: {
    /**
     * 概率-影响矩阵配置
     */
    matrix?: {
      probabilityLevels?: Array<'very-low' | 'low' | 'medium' | 'high' | 'very-high'>;
      impactLevels?: Array<'negligible' | 'low' | 'medium' | 'high' | 'critical'>;
    };

    /**
     * 风险容忍度
     */
    tolerance?: {
      maxAcceptableRiskScore?: number;  // 最大可接受风险评分 (default: 40)
      criticalThreshold?: number;       // Critical风险阈值 (default: 70)
    };

    /**
     * 业务影响评估
     */
    businessImpact?: {
      enabled: boolean;
      revenuePerHour?: number;      // 每小时收入(用于停机成本计算)
      userCount?: number;           // 用户数量
      brandReputationValue?: number; // 品牌声誉价值
    };
  };

  /**
   * 输出配置
   */
  output?: {
    format?: 'json' | 'yaml' | 'html' | 'pdf';
    includeRemediation?: boolean;   // 包含修复建议
    includeTimeline?: boolean;      // 包含时间线估算
    includeCostEstimate?: boolean;  // 包含成本估算
    verbosity?: 'minimal' | 'standard' | 'detailed';
  };
}

/**
 * Risk Assessor输出结果
 */
interface RiskAssessorOutput {
  /**
   * 评估摘要
   */
  summary: {
    projectName: string;
    assessmentDate: string;
    overallRiskScore: number;       // 0-100
    riskLevel: 'low' | 'medium' | 'medium-high' | 'high' | 'critical';
    totalRisksIdentified: number;
    criticalRisks: number;
    highRisks: number;
    mediumRisks: number;
    lowRisks: number;
  };

  /**
   * 识别的风险
   */
  risks: Array<{
    id: string;                     // R1, R2, R3, etc.
    category:
      | 'technical-debt'
      | 'security'
      | 'dependency'
      | 'architecture'
      | 'compliance'
      | 'team'
      | 'performance'
      | 'data';

    title: string;
    description: string;

    /**
     * 风险评分
     */
    assessment: {
      probability: number;          // 0-100
      probabilityLevel: 'very-low' | 'low' | 'medium' | 'high' | 'very-high';
      impact: 'negligible' | 'low' | 'medium' | 'high' | 'critical';
      riskScore: number;            // 0-100 (probability × impact)
      confidenceLevel?: number;     // 评估置信度 0-100
    };

    /**
     * 详细信息
     */
    details: {
      root_cause?: string;
      affected_components: string[];
      current_state: string;
      potential_consequences: string[];

      /**
       * 安全风险特定字段
       */
      cve?: {
        id: string;                 // CVE-2024-1234
        cvssScore: number;          // 0-10
        severity: 'low' | 'medium' | 'high' | 'critical';
        description: string;
        exploit?: string;
        references?: string[];
      };

      /**
       * 技术债务特定字段
       */
      debt?: {
        complexity: number;         // 圈复杂度
        linesOfCode: number;
        lastModified: string;
        coverage?: number;          // 测试覆盖率 %
        duplicates?: number;        // 重复代码行数
      };

      /**
       * 合规性特定字段
       */
      compliance?: {
        standard: 'gdpr' | 'hipaa' | 'soc2';
        requirement: string;
        currentGap: string;
        penalty?: string;
      };
    };

    /**
     * 缓解策略
     */
    mitigation: {
      priority: 'P0' | 'P1' | 'P2' | 'P3';
      strategy: string;
      steps: string[];
      timeline?: string;
      estimatedEffort?: {
        hours: number;
        cost?: number;              // USD
      };
      riskReduction?: {
        before: number;
        after: number;
        percentage: number;
      };
      owner?: string;
      deadline?: string;
    };

    /**
     * 状态
     */
    status?: 'identified' | 'in-progress' | 'mitigated' | 'accepted';
  }>;

  /**
   * 代码质量评估
   */
  codeQuality?: {
    overallScore: number;           // 0-100

    metrics: {
      linesOfCode: number;
      filesCount: number;
      avgComplexity: number;
      maxComplexity: number;
      duplicateCodePercent: number;
      testCoverage: number;
      codeSmells: number;
      bugs: number;
      vulnerabilities: number;
    };

    technicalDebt: {
      totalMinutes: number;         // SonarQube估算
      totalCost?: number;           // USD
      rating: 'A' | 'B' | 'C' | 'D' | 'E';
      trend?: 'improving' | 'stable' | 'worsening';
    };

    topIssues: Array<{
      type: 'code-smell' | 'bug' | 'vulnerability';
      severity: 'blocker' | 'critical' | 'major' | 'minor' | 'info';
      message: string;
      file: string;
      line: number;
      effort: number;               // 修复时间(分钟)
    }>;
  };

  /**
   * 依赖审计结果
   */
  dependencyAudit?: {
    totalDependencies: number;
    directDependencies: number;
    transitiveDependencies: number;

    /**
     * 漏洞统计
     */
    vulnerabilities: {
      critical: number;
      high: number;
      medium: number;
      low: number;
      total: number;
    };

    /**
     * 具体漏洞
     */
    findings: Array<{
      package: string;
      version: string;
      cve?: string;
      severity: 'critical' | 'high' | 'medium' | 'low';
      title: string;
      description: string;
      fixAvailable?: {
        version: string;
        breaking?: boolean;
      };
      patchComplexity?: 'trivial' | 'easy' | 'moderate' | 'hard';
    }>;

    /**
     * 许可证问题
     */
    licenseIssues?: Array<{
      package: string;
      license: string;
      risk: 'high' | 'medium' | 'low';
      reason: string;
    }>;

    /**
     * 过时依赖
     */
    outdated: Array<{
      package: string;
      current: string;
      latest: string;
      ageMonths: number;
      majorVersionBehind: number;
      maintainedRecently?: boolean;
    }>;

    /**
     * 供应链风险
     */
    supplyChainRisks?: Array<{
      package: string;
      risk: string;
      downloadsPerMonth?: number;
      lastPublish?: string;
      contributors?: number;
    }>;
  };

  /**
   * 安全扫描结果
   */
  securityScan?: {
    owaspTop10: Array<{
      category: string;
      risk: 'high' | 'medium' | 'low' | 'none';
      findings?: number;
      examples?: Array<{
        file: string;
        line: number;
        description: string;
        cwe?: string;
      }>;
    }>;

    sastFindings?: Array<{
      tool: string;
      rule: string;
      severity: 'critical' | 'high' | 'medium' | 'low';
      file: string;
      line: number;
      message: string;
      cwe?: string;
      recommendation: string;
    }>;

    secretsLeaked?: Array<{
      type: 'api-key' | 'password' | 'token' | 'private-key' | 'certificate';
      file: string;
      line: number;
      pattern: string;
      severity: 'critical' | 'high';
    }>;

    dastFindings?: Array<{
      url: string;
      method: string;
      vulnerability: string;
      severity: 'critical' | 'high' | 'medium' | 'low';
      request?: string;
      response?: string;
      remediation: string;
    }>;
  };

  /**
   * 架构风险评估
   */
  architectureRisk?: {
    singlePointsOfFailure: Array<{
      component: string;
      type: 'database' | 'cache' | 'queue' | 'external-api' | 'service';
      impact: 'critical' | 'high' | 'medium';
      mtbf?: number;                // Mean Time Between Failures (hours)
      mttr?: number;                // Mean Time To Repair (hours)
      recommendation: string;
    }>;

    scalabilityIssues?: Array<{
      component: string;
      currentCapacity: number;
      projectedCapacity: number;
      headroomMonths: number;       // 剩余容量月数
      bottleneckType: 'cpu' | 'memory' | 'database' | 'network' | 'storage';
      recommendation: string;
    }>;

    performanceBottlenecks?: Array<{
      component: string;
      metric: string;               // 'avg_latency', 'p95_latency', etc.
      current: number;
      threshold: number;
      impact: string;
      recommendation: string;
    }>;

    disasterRecovery?: {
      backupStatus: 'adequate' | 'insufficient' | 'missing';
      rto: number;                  // Hours
      rpo: number;                  // Hours
      lastBackupTest?: string;
      gaps: string[];
      recommendations: string[];
    };
  };

  /**
   * 合规性检查结果
   */
  complianceCheck?: {
    standards: Array<{
      name: 'gdpr' | 'hipaa' | 'soc2' | 'pci-dss';
      overallCompliance: number;    // 0-100%
      status: 'compliant' | 'partially-compliant' | 'non-compliant';

      requirements: Array<{
        id: string;
        description: string;
        status: 'met' | 'partially-met' | 'not-met';
        gap?: string;
        priority: 'critical' | 'high' | 'medium' | 'low';
        remediation?: string;
        deadline?: string;
        penalty?: string;
      }>;
    }>;

    criticalGaps: Array<{
      standard: string;
      requirement: string;
      impact: string;
      remediation: string;
      deadline: string;
    }>;
  };

  /**
   * 风险矩阵
   */
  riskMatrix: {
    critical: string[];             // Risk IDs
    high: string[];
    medium: string[];
    low: string[];

    /**
     * 概率-影响分布
     */
    distribution?: {
      veryHighProbability: number;
      highProbability: number;
      mediumProbability: number;
      lowProbability: number;

      criticalImpact: number;
      highImpact: number;
      mediumImpact: number;
      lowImpact: number;
    };
  };

  /**
   * 行动计划
   */
  actionPlan: {
    immediate: Array<{              // 0-1周
      priority: 'P0' | 'P1';
      action: string;
      owner?: string;
      deadline?: string;
      estimatedHours?: number;
    }>;

    shortTerm: Array<{              // 1-4周
      priority: 'P1' | 'P2';
      action: string;
      owner?: string;
      timeline?: string;
      estimatedCost?: number;
    }>;

    mediumTerm: Array<{             // 1-3个月
      priority: 'P2' | 'P3';
      action: string;
      owner?: string;
      timeline?: string;
      estimatedCost?: number;
    }>;

    longTerm?: Array<{              // 3-12个月
      priority: 'P3';
      action: string;
      timeline?: string;
      estimatedCost?: number;
    }>;
  };

  /**
   * 建议
   */
  recommendations: Array<{
    type: 'immediate-action' | 'process-improvement' | 'tool-adoption' | 'training' | 'monitoring';
    priority: 'critical' | 'high' | 'medium' | 'low';
    target: 'team' | 'tech-lead' | 'security-team' | 'management';
    title: string;
    description: string;

    actionable?: {
      steps: string[];
      estimatedEffort: 'trivial' | 'easy' | 'moderate' | 'hard';
      expectedImpact: string;
    };

    metrics?: {
      current?: string;
      target?: string;
      improvement?: string;
    };
  }>;

  /**
   * 风险趋势
   */
  riskTrend?: {
    currentRiskScore: number;
    afterMitigationScore: number;
    reductionPercentage: number;
    timeline: string;

    history?: Array<{
      date: string;
      riskScore: number;
      criticalRisks: number;
    }>;
  };

  /**
   * 元数据
   */
  metadata: {
    assessmentDate: string;
    version: string;
    executionTimeMs: number;
    toolsUsed: string[];
    assessor?: string;
  };
}

/**
 * 风险项(单个风险)
 */
interface RiskItem {
  id: string;
  category: string;
  probability: number;
  impact: string;
  riskScore: number;
  mitigation: {
    priority: string;
    steps: string[];
    timeline: string;
  };
}

/**
 * CVE漏洞
 */
interface CVEVulnerability {
  cve: string;
  package: string;
  version: string;
  cvssScore: number;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  fixVersion?: string;
}

/**
 * 合规性差距
 */
interface ComplianceGap {
  standard: 'gdpr' | 'hipaa' | 'soc2';
  requirement: string;
  gap: string;
  penalty?: string;
  remediation: string;
}
```

---

## Usage Examples

### Example 1: 新项目全面风险评估 (Comprehensive Project Risk Assessment)

**场景**: 电商平台重构项目启动前,评估技术风险、安全风险和合规性

**输入**:
```typescript
const input: RiskAssessorInput = {
  task: {
    type: 'comprehensive',
    description: '评估E-commerce Platform Redesign项目的技术风险',
    scope: ['backend', 'frontend', 'database', 'infrastructure']
  },

  project: {
    name: 'E-commerce Platform Redesign',
    description: '将遗留单体应用重构为微服务架构',
    criticality: 'critical',      // 业务关键系统
    stage: 'planning',

    techStack: {
      languages: ['typescript', 'python'],
      frameworks: ['react', 'express', 'django'],
      databases: ['postgresql', 'redis', 'mongodb'],
      infrastructure: ['kubernetes', 'aws', 'docker']
    },

    team: {
      size: 8,
      experience: 'mixed',        // 混合经验
      keyPersonDependencies: ['alice'], // Alice是唯一的payment专家
      turnoverRate: 15            // 年流失率15%
    }
  },

  codebase: {
    path: '/workspace/ecommerce-backend',
    gitRepo: 'https://github.com/company/ecommerce-backend',
    branch: 'main',

    stats: {
      linesOfCode: 150000,
      filesCount: 450,
      ageInYears: 5,
      commitsPerMonth: 120,
      contributors: 12
    }
  },

  // 代码质量扫描
  codeQuality: {
    enabled: true,
    tools: ['sonarqube', 'eslint'],

    sonarqube: {
      serverUrl: 'https://sonar.company.com',
      token: process.env.SONAR_TOKEN!,
      projectKey: 'ecommerce-backend'
    },

    codeSmells: {
      enabled: true,
      thresholds: {
        maxComplexity: 10,
        maxFunctionLength: 50,
        maxFileSize: 500,
        duplicateCodePercent: 3
      }
    },

    technicalDebt: {
      enabled: true,
      estimateMethod: 'sonar',
      hourlyRate: 100             // $100/hour开发者成本
    }
  },

  // 依赖审计
  dependencyAudit: {
    enabled: true,
    tools: ['npm-audit', 'snyk'],

    cveScanning: {
      enabled: true,
      severityThreshold: 'medium',
      ignoreCVEs: []
    },

    licenseCheck: {
      enabled: true,
      allowedLicenses: ['MIT', 'Apache-2.0', 'BSD-3-Clause'],
      blockedLicenses: ['GPL-3.0', 'AGPL-3.0']
    },

    outdatedCheck: {
      enabled: true,
      maxAgeMonths: 12,
      checkMajorUpdates: true
    },

    supplyChain: {
      enabled: true,
      checkMaintenance: true,
      checkPopularity: true,
      minDownloadsPerMonth: 1000
    }
  },

  // 安全扫描
  securityScan: {
    enabled: true,

    owaspCheck: {
      enabled: true,
      categories: [
        'injection',
        'broken-authentication',
        'sensitive-data-exposure',
        'broken-access-control',
        'security-misconfiguration',
        'xss',
        'using-components-with-vulnerabilities'
      ]
    },

    sast: {
      enabled: true,
      tools: ['semgrep', 'bandit']
    },

    secretScanning: {
      enabled: true,
      tools: ['gitleaks']
    },

    dast: {
      enabled: false              // 暂不进行动态扫描
    }
  },

  // 架构风险评估
  architectureRisk: {
    enabled: true,

    singlePointOfFailure: {
      enabled: true,
      checkDatabase: true,
      checkCache: true,
      checkQueue: true,
      checkExternalAPIs: true
    },

    scalability: {
      enabled: true,
      currentLoad: {
        requestsPerSecond: 500,
        concurrentUsers: 5000,
        dataVolumeGB: 200
      },
      projectedLoad: {
        requestsPerSecond: 5000,
        concurrentUsers: 50000,
        dataVolumeGB: 1000,
        timelineMonths: 12
      }
    },

    performanceBottlenecks: {
      enabled: true,
      checkDatabaseQueries: true,
      checkAPILatency: true,
      checkCachingStrategy: true
    },

    disasterRecovery: {
      enabled: true,
      checkBackups: true,
      checkReplication: true,
      checkFailover: true,
      rtoHours: 4,                // 目标恢复时间4小时
      rpoHours: 1                 // 目标恢复点1小时
    }
  },

  // 合规性检查
  complianceCheck: {
    enabled: true,
    standards: ['gdpr', 'soc2'],

    gdpr: {
      checkDataEncryption: true,
      checkConsentManagement: true,
      checkDataDeletion: true,
      checkAccessControl: true,
      checkAuditLogs: true,
      checkDataPortability: true
    },

    soc2: {
      checkSecurityControls: true,
      checkAvailability: true,
      checkConfidentiality: true,
      checkProcessingIntegrity: true,
      checkPrivacy: true
    }
  },

  // 风险评估参数
  riskAssessment: {
    matrix: {
      probabilityLevels: ['very-low', 'low', 'medium', 'high', 'very-high'],
      impactLevels: ['negligible', 'low', 'medium', 'high', 'critical']
    },

    tolerance: {
      maxAcceptableRiskScore: 40,
      criticalThreshold: 70
    },

    businessImpact: {
      enabled: true,
      revenuePerHour: 50000,      // $50K/hour收入
      userCount: 100000,
      brandReputationValue: 10000000 // $10M品牌价值
    }
  },

  output: {
    format: 'json',
    includeRemediation: true,
    includeTimeline: true,
    includeCostEstimate: true,
    verbosity: 'detailed'
  }
};
```

**输出**:
```typescript
const output: RiskAssessorOutput = {
  summary: {
    projectName: 'E-commerce Platform Redesign',
    assessmentDate: '2025-01-12',
    overallRiskScore: 67,         // 67/100 (Medium-High)
    riskLevel: 'medium-high',
    totalRisksIdentified: 12,
    criticalRisks: 2,
    highRisks: 3,
    mediumRisks: 5,
    lowRisks: 2
  },

  risks: [
    // Risk 1: 技术债务
    {
      id: 'R1',
      category: 'technical-debt',
      title: '核心支付模块使用5年前的遗留代码',
      description: '支付模块包含15,000行未测试的JavaScript代码,依赖已停止维护的库,原开发者已离职,缺少文档。',

      assessment: {
        probability: 90,
        probabilityLevel: 'very-high',
        impact: 'high',
        riskScore: 81,            // 81/100
        confidenceLevel: 95
      },

      details: {
        root_cause: '5年前快速开发,缺少重构时间投入',
        affected_components: ['payment-service', 'checkout-flow', 'refund-api'],
        current_state: '代码腐化严重,维护成本极高',
        potential_consequences: [
          'bug修复困难,平均2天/bug',
          '新功能开发几乎不可能(需要完全理解遗留代码)',
          '安全漏洞修复困难',
          '知识流失风险(Alice是唯一熟悉者)',
          '可能引发严重生产事故'
        ],

        debt: {
          complexity: 28,         // 平均圈复杂度28(极高)
          linesOfCode: 15000,
          lastModified: '2023-06-15',
          coverage: 12,           // 测试覆盖率仅12%
          duplicates: 2800        // 2,800行重复代码
        }
      },

      mitigation: {
        priority: 'P0',
        strategy: '分阶段重构,先增加测试覆盖再逐步替换',
        steps: [
          'Week 1-2: 添加集成测试覆盖关键支付路径(target 80%)',
          'Week 3-4: 增量重构为TypeScript模块(保持向后兼容)',
          'Week 5-6: 迁移到Stripe最新SDK,移除deprecated API',
          'Week 7: 完全替换旧代码,部署到production',
          'Week 8: 监控2周,确认无回归bug'
        ],
        timeline: '8周',
        estimatedEffort: {
          hours: 320,             // 2人 × 4周 × 40小时
          cost: 32000             // $32,000
        },
        riskReduction: {
          before: 81,
          after: 25,
          percentage: 69          // 降低69%
        },
        owner: 'alice',
        deadline: '2025-03-15'
      },

      status: 'identified'
    },

    // Risk 2: 安全漏洞
    {
      id: 'R2',
      category: 'security',
      title: '发现3个高危依赖漏洞(Critical CVEs)',
      description: 'npm audit检测到3个Critical/High severity CVE漏洞,包括RCE和token forgery。',

      assessment: {
        probability: 75,
        probabilityLevel: 'high',
        impact: 'critical',
        riskScore: 88,
        confidenceLevel: 100      // CVE数据库确认
      },

      details: {
        root_cause: '依赖未及时更新,缺少自动化扫描',
        affected_components: ['express-api', 'auth-service'],
        current_state: '生产环境正在运行含漏洞版本',
        potential_consequences: [
          'RCE (Remote Code Execution)可能导致服务器完全被攻陷',
          'Token forgery可能导致身份验证绕过',
          '数据泄露风险',
          '监管处罚($100K+ GDPR罚款)',
          '品牌声誉损害'
        ],

        cve: {
          id: 'CVE-2024-1234',
          cvssScore: 9.8,
          severity: 'critical',
          description: 'Express.js prototype pollution leading to RCE',
          exploit: 'https://nvd.nist.gov/vuln/detail/CVE-2024-1234',
          references: [
            'https://github.com/expressjs/express/security/advisories/GHSA-xxxx',
            'https://blog.attacker.com/express-rce-exploit'
          ]
        }
      },

      mitigation: {
        priority: 'P0',
        strategy: '立即升级受影响依赖并执行回归测试',
        steps: [
          '立即: 升级express@4.17.1 → 4.19.0',
          '立即: 升级jsonwebtoken@8.5.0 → 9.0.2',
          '1小时内: 运行完整测试套件确认无破坏性变更',
          '2小时内: 部署到staging环境,执行smoke test',
          '4小时内: 部署到production(蓝绿部署)',
          '24小时内: 监控错误日志和性能指标',
          '48小时内: 确认修复有效,无副作用'
        ],
        timeline: '48小时deadline',
        estimatedEffort: {
          hours: 8,
          cost: 800
        },
        riskReduction: {
          before: 88,
          after: 10,
          percentage: 89
        },
        owner: 'bob',
        deadline: '2025-01-14T12:00:00Z'
      },

      status: 'identified'
    },

    // Risk 3: 架构风险
    {
      id: 'R3',
      category: 'architecture',
      title: '单体架构扩展性瓶颈',
      description: '当前处理能力500 req/s,预期12个月内增长至5,000 req/s。数据库单点故障,部署需要全系统停机。',

      assessment: {
        probability: 60,
        probabilityLevel: 'medium',
        impact: 'medium',
        riskScore: 48,
        confidenceLevel: 85
      },

      details: {
        root_cause: '5年前设计时未考虑扩展性',
        affected_components: ['monolith-app', 'postgresql-primary', 'deployment-pipeline'],
        current_state: '单机PostgreSQL,单体应用,零停机部署困难',
        potential_consequences: [
          '12个月后无法支撑5,000 req/s流量',
          '数据库故障导致全系统宕机(RTO 4小时不满足)',
          '部署需要停机维护窗口(用户体验差)',
          '性能下降导致用户流失',
          '黑色星期五等高峰期可能崩溃'
        ]
      },

      mitigation: {
        priority: 'P1',
        strategy: '微服务渐进式迁移 + 数据库读写分离',
        steps: [
          'Phase 1 (Month 1-2): 拆分支付服务(highest load + critical)',
          'Phase 2 (Month 3-4): 拆分用户服务 + 实施API Gateway',
          'Phase 3 (Month 5): PostgreSQL主从复制 + 读写分离',
          'Phase 4 (Month 6): 数据库分片(sharding)准备',
          'Phase 5 (Month 7-12): 其他服务逐步拆分'
        ],
        timeline: '6个月MVP,12个月完成',
        estimatedEffort: {
          hours: 2000,
          cost: 200000            // $200K (包含基础设施成本)
        },
        riskReduction: {
          before: 48,
          after: 15,
          percentage: 69
        },
        owner: 'tech-lead',
        deadline: '2025-07-01'
      },

      status: 'identified'
    },

    // Risk 4: 合规性风险
    {
      id: 'R4',
      category: 'compliance',
      title: 'GDPR数据处理合规性问题',
      description: '用户数据未加密存储,缺少数据删除功能,未实现访问日志审计。违反GDPR多项要求。',

      assessment: {
        probability: 40,
        probabilityLevel: 'medium',
        impact: 'high',
        riskScore: 56,
        confidenceLevel: 90
      },

      details: {
        root_cause: 'GDPR上线前系统已存在,未完成合规改造',
        affected_components: ['user-database', 'api-endpoints', 'logging-system'],
        current_state: '明文存储敏感数据,无删除/导出API,审计日志缺失',
        potential_consequences: [
          'GDPR罚款: €20M或年收入4%(取高者)',
          '监管机构调查和公开通报',
          '用户信任丧失',
          '诉讼风险',
          'B2B客户要求合规证明'
        ],

        compliance: {
          standard: 'gdpr',
          requirement: 'Article 5 (data minimization), Article 17 (right to erasure), Article 15 (right of access)',
          currentGap: '数据未加密,无删除/导出功能,缺少审计日志',
          penalty: '€20M或年收入4%'
        }
      },

      mitigation: {
        priority: 'P0',
        strategy: '实施数据加密、GDPR API和审计系统',
        steps: [
          'Week 1-2: 实施PostgreSQL透明数据加密(TDE)',
          'Week 2-3: 开发GDPR数据导出API (GET /api/users/{id}/export)',
          'Week 3-4: 开发数据删除API (DELETE /api/users/{id}) + 软删除机制',
          'Week 4-6: 添加审计日志系统(记录所有数据访问)',
          'Week 7: 法务团队审查,确认合规',
          'Week 8: 更新隐私政策,通知用户'
        ],
        timeline: '8周',
        estimatedEffort: {
          hours: 200,
          cost: 20000
        },
        riskReduction: {
          before: 56,
          after: 10,
          percentage: 82
        },
        owner: 'alice',
        deadline: '2025-03-01'
      },

      status: 'identified'
    },

    // Risk 5-12省略...
  ],

  // 代码质量评估
  codeQuality: {
    overallScore: 58,             // 58/100 (C级)

    metrics: {
      linesOfCode: 150000,
      filesCount: 450,
      avgComplexity: 8.5,
      maxComplexity: 28,          // 支付模块
      duplicateCodePercent: 5.2,  // 5.2%重复代码
      testCoverage: 64,           // 64%覆盖率
      codeSmells: 287,
      bugs: 45,
      vulnerabilities: 12
    },

    technicalDebt: {
      totalMinutes: 18000,        // 300小时技术债务
      totalCost: 30000,           // $30,000
      rating: 'C',
      trend: 'worsening'          // 过去6个月恶化
    },

    topIssues: [
      {
        type: 'code-smell',
        severity: 'critical',
        message: 'Cognitive Complexity of 28 (should be ≤15)',
        file: 'src/payment/legacy/processCharge.js',
        line: 145,
        effort: 120               // 2小时修复
      },
      {
        type: 'bug',
        severity: 'major',
        message: 'Null pointer dereference可能导致crash',
        file: 'src/order/validation.ts',
        line: 67,
        effort: 30
      },
      {
        type: 'vulnerability',
        severity: 'critical',
        message: 'SQL injection via string concatenation',
        file: 'src/refund/queries.js',
        line: 89,
        effort: 15
      }
    ]
  },

  // 依赖审计结果
  dependencyAudit: {
    totalDependencies: 342,
    directDependencies: 58,
    transitiveDependencies: 284,

    vulnerabilities: {
      critical: 1,
      high: 2,
      medium: 8,
      low: 15,
      total: 26
    },

    findings: [
      {
        package: 'express',
        version: '4.17.1',
        cve: 'CVE-2024-1234',
        severity: 'critical',
        title: 'Prototype pollution leading to RCE',
        description: 'Express.js版本4.17.1存在原型污染漏洞,允许远程代码执行。',
        fixAvailable: {
          version: '4.19.0',
          breaking: false
        },
        patchComplexity: 'trivial'
      },
      {
        package: 'jsonwebtoken',
        version: '8.5.0',
        cve: 'CVE-2024-5678',
        severity: 'high',
        title: 'Token forgery via algorithm confusion',
        description: 'jsonwebtoken 8.5.0允许攻击者通过算法混淆伪造JWT token。',
        fixAvailable: {
          version: '9.0.2',
          breaking: true          // 需要测试认证流程
        },
        patchComplexity: 'moderate'
      }
    ],

    licenseIssues: [
      {
        package: 'some-gpl-library',
        license: 'GPL-3.0',
        risk: 'high',
        reason: 'GPL-3.0许可证要求开源所有衍生代码,与商业闭源冲突'
      }
    ],

    outdated: [
      {
        package: 'lodash',
        current: '4.17.15',
        latest: '4.17.21',
        ageMonths: 18,
        majorVersionBehind: 0,
        maintainedRecently: true
      },
      {
        package: 'moment',
        current: '2.24.0',
        latest: '2.30.1',
        ageMonths: 36,
        majorVersionBehind: 0,
        maintainedRecently: false // moment已停止维护,建议迁移到dayjs
      }
    ],

    supplyChainRisks: [
      {
        package: 'obscure-utility',
        risk: '低维护频率,仅1个contributor',
        downloadsPerMonth: 500,
        lastPublish: '2022-03-15',
        contributors: 1
      }
    ]
  },

  // 安全扫描结果
  securityScan: {
    owaspTop10: [
      {
        category: 'Injection (A03:2021)',
        risk: 'high',
        findings: 3,
        examples: [
          {
            file: 'src/refund/queries.js',
            line: 89,
            description: 'SQL injection via string concatenation',
            cwe: 'CWE-89'
          },
          {
            file: 'src/search/filter.ts',
            line: 45,
            description: 'Potential NoSQL injection in MongoDB query',
            cwe: 'CWE-943'
          }
        ]
      },
      {
        category: 'Broken Authentication (A07:2021)',
        risk: 'medium',
        findings: 1,
        examples: [
          {
            file: 'src/auth/session.ts',
            line: 23,
            description: 'Session token未设置HttpOnly和Secure flag',
            cwe: 'CWE-614'
          }
        ]
      },
      {
        category: 'Sensitive Data Exposure (A02:2021)',
        risk: 'high',
        findings: 2,
        examples: [
          {
            file: 'src/user/model.ts',
            line: 12,
            description: '用户密码明文存储在数据库',
            cwe: 'CWE-312'
          }
        ]
      }
    ],

    sastFindings: [
      {
        tool: 'semgrep',
        rule: 'sql-injection',
        severity: 'critical',
        file: 'src/refund/queries.js',
        line: 89,
        message: 'User input directly concatenated into SQL query',
        cwe: 'CWE-89',
        recommendation: '使用参数化查询或ORM (Prisma)'
      },
      {
        tool: 'bandit',
        rule: 'hardcoded-password',
        severity: 'high',
        file: 'config/database.py',
        line: 15,
        message: 'Hardcoded password detected',
        cwe: 'CWE-798',
        recommendation: '使用环境变量存储密码'
      }
    ],

    secretsLeaked: [
      {
        type: 'api-key',
        file: 'src/payment/stripe.ts',
        line: 8,
        pattern: 'sk_live_xxxxxxxxxxxxx',
        severity: 'critical'
      },
      {
        type: 'password',
        file: '.env.example',
        line: 12,
        pattern: 'DB_PASSWORD=admin123',
        severity: 'high'
      }
    ]
  },

  // 架构风险评估
  architectureRisk: {
    singlePointsOfFailure: [
      {
        component: 'PostgreSQL Primary',
        type: 'database',
        impact: 'critical',
        mtbf: 720,              // 720小时(30天)平均故障间隔
        mttr: 4,                // 4小时平均恢复时间
        recommendation: '实施主从复制和自动故障转移(Patroni/repmgr)'
      },
      {
        component: 'Redis Cache',
        type: 'cache',
        impact: 'high',
        mtbf: 2160,             // 90天
        mttr: 0.5,              // 30分钟
        recommendation: 'Redis Sentinel或Redis Cluster高可用'
      },
      {
        component: 'Stripe API',
        type: 'external-api',
        impact: 'critical',
        mtbf: 8760,             // 1年
        mttr: 2,
        recommendation: '实施重试机制和降级方案(保存订单稍后处理)'
      }
    ],

    scalabilityIssues: [
      {
        component: 'Monolith Application',
        currentCapacity: 500,
        projectedCapacity: 5000,
        headroomMonths: 8,      // 8个月后达到瓶颈
        bottleneckType: 'cpu',
        recommendation: '拆分支付服务和用户服务为独立微服务'
      },
      {
        component: 'PostgreSQL Primary',
        currentCapacity: 200,   // 200GB数据
        projectedCapacity: 1000,
        headroomMonths: 18,
        bottleneckType: 'storage',
        recommendation: '计划数据库分片,按用户ID hash分区'
      }
    ],

    performanceBottlenecks: [
      {
        component: 'Order API',
        metric: 'p95_latency',
        current: 850,           // 850ms
        threshold: 500,         // 目标500ms
        impact: '70% P95延迟超标,影响用户体验',
        recommendation: '优化N+1查询,添加Redis缓存层'
      },
      {
        component: 'Product Search',
        metric: 'avg_latency',
        current: 1200,          // 1.2秒
        threshold: 300,
        impact: '搜索体验差,可能导致用户流失',
        recommendation: '迁移到Elasticsearch全文搜索'
      }
    ],

    disasterRecovery: {
      backupStatus: 'insufficient',
      rto: 4,                   // 4小时恢复
      rpo: 1,                   // 1小时数据丢失
      lastBackupTest: '2024-11-15', // 2个月前
      gaps: [
        '未定期测试备份恢复流程',
        '缺少跨区域备份(single AZ)',
        'Redis数据未备份(缓存丢失需重建)',
        '应用配置未纳入备份'
      ],
      recommendations: [
        '每月执行灾备演练',
        '启用PostgreSQL PITR (Point-in-Time Recovery)',
        '配置跨区域备份到S3',
        '使用GitOps管理基础设施配置(IaC)'
      ]
    }
  },

  // 合规性检查结果
  complianceCheck: {
    standards: [
      {
        name: 'gdpr',
        overallCompliance: 45,  // 45%合规
        status: 'non-compliant',

        requirements: [
          {
            id: 'GDPR-Art5',
            description: 'Data minimization and storage limitation',
            status: 'partially-met',
            gap: '收集了非必要的用户数据(如生日、爱好)',
            priority: 'medium',
            remediation: '审查数据收集流程,移除非必要字段',
            deadline: '2025-04-01'
          },
          {
            id: 'GDPR-Art15',
            description: 'Right of access (data export)',
            status: 'not-met',
            gap: '未实现数据导出API',
            priority: 'critical',
            remediation: '开发GET /api/users/{id}/export端点',
            deadline: '2025-03-01',
            penalty: '€20M或年收入4%'
          },
          {
            id: 'GDPR-Art17',
            description: 'Right to erasure',
            status: 'not-met',
            gap: '未实现数据删除功能',
            priority: 'critical',
            remediation: '开发DELETE /api/users/{id}端点(软删除+30天后硬删除)',
            deadline: '2025-03-01',
            penalty: '€20M或年收入4%'
          },
          {
            id: 'GDPR-Art32',
            description: 'Security of processing (encryption)',
            status: 'not-met',
            gap: '敏感数据未加密存储',
            priority: 'critical',
            remediation: '实施数据库加密(TDE)和应用层加密',
            deadline: '2025-02-15',
            penalty: '€20M或年收入4%'
          }
        ]
      },
      {
        name: 'soc2',
        overallCompliance: 60,
        status: 'partially-compliant',

        requirements: [
          {
            id: 'CC6.1',
            description: 'Logical and physical access controls',
            status: 'met',
            priority: 'high'
          },
          {
            id: 'CC7.2',
            description: 'System monitoring',
            status: 'partially-met',
            gap: '缺少实时告警和异常检测',
            priority: 'high',
            remediation: '部署Datadog/New Relic APM'
          }
        ]
      }
    ],

    criticalGaps: [
      {
        standard: 'GDPR',
        requirement: 'Right to erasure (Article 17)',
        impact: '用户无法删除个人数据,违反GDPR',
        remediation: '开发数据删除API并实施软删除机制',
        deadline: '2025-03-01'
      },
      {
        standard: 'GDPR',
        requirement: 'Data encryption (Article 32)',
        impact: '敏感数据泄露风险,€20M罚款',
        remediation: '实施PostgreSQL TDE和应用层加密',
        deadline: '2025-02-15'
      }
    ]
  },

  // 风险矩阵
  riskMatrix: {
    critical: ['R2', 'R4'],     // CVE漏洞、GDPR合规
    high: ['R1', 'R3'],         // 技术债务、架构扩展性
    medium: ['R5', 'R6', 'R7', 'R8', 'R9'],
    low: ['R10', 'R11'],

    distribution: {
      veryHighProbability: 2,
      highProbability: 3,
      mediumProbability: 5,
      lowProbability: 2,

      criticalImpact: 2,
      highImpact: 4,
      mediumImpact: 4,
      lowImpact: 2
    }
  },

  // 行动计划
  actionPlan: {
    immediate: [
      {
        priority: 'P0',
        action: '修复CVE-2024-1234 (Express RCE漏洞)',
        owner: 'bob',
        deadline: '2025-01-14',
        estimatedHours: 4
      },
      {
        priority: 'P0',
        action: '修复CVE-2024-5678 (jsonwebtoken漏洞)',
        owner: 'bob',
        deadline: '2025-01-14',
        estimatedHours: 8
      },
      {
        priority: 'P0',
        action: '启动GDPR合规工作(数据加密)',
        owner: 'alice',
        deadline: '2025-01-20',
        estimatedHours: 40
      }
    ],

    shortTerm: [
      {
        priority: 'P1',
        action: '支付模块集成测试(覆盖率80%+)',
        owner: 'alice',
        timeline: 'Week 1-2',
        estimatedCost: 8000
      },
      {
        priority: 'P1',
        action: '实施PostgreSQL TDE数据加密',
        owner: 'devops-team',
        timeline: 'Week 2-3',
        estimatedCost: 5000
      },
      {
        priority: 'P1',
        action: '开发GDPR数据导出/删除API',
        owner: 'alice',
        timeline: 'Week 3-4',
        estimatedCost: 10000
      }
    ],

    mediumTerm: [
      {
        priority: 'P1',
        action: '支付模块重构为TypeScript',
        owner: 'alice',
        timeline: 'Month 1-2',
        estimatedCost: 32000
      },
      {
        priority: 'P2',
        action: '微服务架构POC(拆分支付服务)',
        owner: 'tech-lead',
        timeline: 'Month 2-4',
        estimatedCost: 80000
      },
      {
        priority: 'P2',
        action: 'PostgreSQL主从复制和读写分离',
        owner: 'devops-team',
        timeline: 'Month 3',
        estimatedCost: 15000
      }
    ],

    longTerm: [
      {
        priority: 'P2',
        action: '完成微服务迁移(5个核心服务)',
        timeline: 'Month 4-12',
        estimatedCost: 200000
      },
      {
        priority: 'P3',
        action: '数据库分片(sharding)实施',
        timeline: 'Month 10-12',
        estimatedCost: 50000
      }
    ]
  },

  // 建议
  recommendations: [
    {
      type: 'immediate-action',
      priority: 'critical',
      target: 'security-team',
      title: '立即修复3个Critical/High CVE漏洞',
      description: 'CVE-2024-1234 (Express RCE)和CVE-2024-5678 (JWT forgery)允许攻击者完全控制系统。48小时内必须修复。',
      actionable: {
        steps: [
          '升级express@4.17.1 → 4.19.0',
          '升级jsonwebtoken@8.5.0 → 9.0.2',
          '运行完整测试套件',
          '部署到production'
        ],
        estimatedEffort: 'easy',
        expectedImpact: '消除Critical安全风险,防止RCE和token forgery攻击'
      },
      metrics: {
        current: 'CVE风险评分: 88/100',
        target: 'CVE风险评分: <10/100',
        improvement: '风险降低89%'
      }
    },
    {
      type: 'immediate-action',
      priority: 'critical',
      target: 'tech-lead',
      title: 'GDPR合规整改(法律要求)',
      description: '当前GDPR合规率仅45%,缺少数据删除/导出API和加密。€20M罚款风险。',
      actionable: {
        steps: [
          '实施PostgreSQL TDE加密',
          '开发GDPR数据导出API',
          '开发数据删除API(软删除+30天硬删除)',
          '添加访问日志审计',
          '法务团队审查确认合规'
        ],
        estimatedEffort: 'moderate',
        expectedImpact: 'GDPR合规率从45%提升至95%,消除€20M罚款风险'
      },
      metrics: {
        current: 'GDPR合规率: 45%',
        target: 'GDPR合规率: 95%+',
        improvement: '合规率提升50个百分点'
      }
    },
    {
      type: 'process-improvement',
      priority: 'high',
      target: 'team',
      title: '建立自动化安全扫描流程',
      description: '当前依赖手动扫描,导致漏洞发现延迟。建议集成Snyk/Dependabot自动扫描。',
      actionable: {
        steps: [
          '集成Snyk到CI/CD流程(每次PR自动扫描)',
          '配置Dependabot自动创建依赖更新PR',
          '设置Slack告警: Critical/High漏洞立即通知',
          '每周生成安全报告发送给tech-lead'
        ],
        estimatedEffort: 'easy',
        expectedImpact: '漏洞发现时间从平均30天降至<24小时'
      }
    },
    {
      type: 'process-improvement',
      priority: 'high',
      target: 'tech-lead',
      title: '技术债务偿还计划',
      description: '当前技术债务300小时($30K),趋势恶化。建议每Sprint分配20%时间偿还债务。',
      actionable: {
        steps: [
          '每Sprint分配20%时间(2天/10天)重构',
          '优先处理支付模块(81风险分最高)',
          '设置技术债务KPI: 每月降低10%',
          '使用SonarQube Quality Gate阻止新债务'
        ],
        estimatedEffort: 'moderate',
        expectedImpact: '6个月内技术债务降至100小时,代码质量从C级提升至B级'
      },
      metrics: {
        current: '技术债务: 300小时 (C级)',
        target: '技术债务: <100小时 (B级)',
        improvement: '债务减少67%'
      }
    },
    {
      type: 'tool-adoption',
      priority: 'medium',
      target: 'devops-team',
      title: '采用APM工具监控性能',
      description: 'Order API P95延迟850ms超标70%,但缺少详细监控数据定位瓶颈。',
      actionable: {
        steps: [
          '部署Datadog APM或New Relic',
          '配置慢查询监控(>500ms告警)',
          '设置P95延迟目标<500ms',
          '每周性能报告'
        ],
        estimatedEffort: 'easy',
        expectedImpact: 'P95延迟从850ms降至<500ms,提升用户体验'
      }
    },
    {
      type: 'training',
      priority: 'medium',
      target: 'team',
      title: '安全编码培训(OWASP Top 10)',
      description: '发现3个SQL注入漏洞,团队缺少安全编码意识。',
      actionable: {
        steps: [
          '组织OWASP Top 10培训(4小时)',
          'Secure coding workshop(实战演练)',
          '代码审查清单增加安全检查项',
          '每季度安全培训复训'
        ],
        estimatedEffort: 'easy',
        expectedImpact: '减少80%常见安全漏洞(SQL注入、XSS等)'
      }
    }
  ],

  // 风险趋势
  riskTrend: {
    currentRiskScore: 67,
    afterMitigationScore: 32,
    reductionPercentage: 52,    // 降低52%
    timeline: '3个月',

    history: [
      { date: '2024-10-01', riskScore: 55, criticalRisks: 1 },
      { date: '2024-11-01', riskScore: 62, criticalRisks: 1 },
      { date: '2025-01-12', riskScore: 67, criticalRisks: 2 },
      { date: '2025-04-01 (projected)', riskScore: 32, criticalRisks: 0 }
    ]
  },

  metadata: {
    assessmentDate: '2025-01-12T16:00:00Z',
    version: '2.0.0',
    executionTimeMs: 45000,       // 45秒
    toolsUsed: [
      'SonarQube 9.9',
      'npm audit',
      'Snyk',
      'Semgrep',
      'GitLeaks',
      'Custom Architecture Analyzer'
    ],
    assessor: 'Risk Assessor v2.0.0'
  }
};
```

**效果**:
- **全面评估**: 识别12个风险,覆盖技术债务、安全、架构、合规性
- **量化优先级**: 风险评分0-100,清晰标识P0/P1/P2优先级
- **可执行计划**: Immediate/Short-term/Medium-term行动计划,包含时间线和成本
- **合规保障**: GDPR合规率从45%→95%,消除€20M罚款风险
- **成本透明**: 总修复成本$387K,时间线3-12个月,风险评分67→32

---

## Best Practices

### ✅ DO: Effective Risk Management

```typescript
// ✅ GOOD: 量化风险评分(概率×影响)
const goodRiskScoring = {
  method: '概率-影响矩阵',
  formula: 'riskScore = probability (0-100) × impactLevel (0-1)',
  example: {
    probability: 90,            // 90%概率发生
    impact: 'high' (0.9),       // 高影响
    riskScore: 81               // 81/100
  },
  benefits: [
    '客观量化,避免主观判断',
    '优先级排序清晰',
    '可追踪风险变化趋势'
  ]
};

// ✅ GOOD: 具体可执行的缓解计划
const goodMitigation = {
  priority: 'P0',
  steps: [
    'Week 1-2: 添加集成测试(80%覆盖率)',
    'Week 3-4: 重构为TypeScript模块',
    'Week 5-6: 迁移到Stripe最新SDK',
    'Week 7: 部署到production',
    'Week 8: 监控2周确认无回归'
  ],
  timeline: '8周',
  cost: '$32,000',
  owner: 'alice',
  deadline: '2025-03-15'
};

// ✅ GOOD: 多维度风险识别
const goodRiskCoverage = {
  dimensions: [
    'technical-debt',           // 技术债务
    'security',                 // 安全漏洞
    'architecture',             // 架构风险
    'compliance',               // 合规性
    'team',                     // 团队/知识风险
    'performance',              // 性能瓶颈
    'dependency',               // 依赖健康
    'data'                      // 数据质量
  ],
  coverage: 'comprehensive'
};

// ✅ GOOD: CVE漏洞自动扫描
const goodCVEScanning = {
  tools: ['npm-audit', 'snyk', 'dependabot'],
  automation: 'CI/CD pipeline自动扫描',
  alerting: 'Slack实时告警Critical/High',
  sla: {
    critical: '24小时修复',
    high: '1周修复',
    medium: '1个月修复'
  }
};
```

### ❌ DON'T: Poor Risk Management Practices

```typescript
// ❌ BAD: 主观定性风险评估
const badRiskScoring = {
  assessment: '这个风险挺大的',  // 无量化
  priority: '应该优先处理',      // 无客观标准
  problem: '无法比较不同风险优先级,团队认知不一致'
};

// ❌ BAD: 模糊的缓解计划
const badMitigation = {
  plan: '重构支付模块',
  timeline: '尽快',              // 无具体时间
  owner: '待定',                 // 无负责人
  cost: '不清楚',                // 无成本估算
  problem: '无法执行,无法追踪进度'
};

// ❌ BAD: 仅关注代码层面风险
const badRiskCoverage = {
  scope: ['code-quality', 'bugs'],
  missing: [
    'CVE安全漏洞',
    'GDPR合规性',
    '架构扩展性',
    '团队知识风险(关键人员依赖)',
    '依赖供应链安全'
  ],
  problem: '遗漏重大风险,上线后出现意外'
};

// ❌ BAD: 手动CVE扫描
const badCVEScanning = {
  method: '每月手动运行npm audit',
  delay: '漏洞发现延迟平均30天',
  result: 'CVE-2024-1234发现时已被利用',
  problem: '反应速度慢,增加被攻击窗口期'
};

// ❌ BAD: 忽略业务影响
const badBusinessImpact = {
  focus: '纯技术视角',
  missing: {
    revenueImpact: '停机每小时损失$50K',
    reputationDamage: '数据泄露品牌损失$10M',
    legalPenalty: 'GDPR罚款€20M'
  },
  problem: '无法向管理层说明风险严重性,预算不足'
};
```

### 🎯 Implementation Guidelines

1. **Risk Scoring Formula** (风险评分公式)
   ```typescript
   // 概率-影响矩阵
   const calculateRiskScore = (
     probability: number,        // 0-100
     impact: 'negligible' | 'low' | 'medium' | 'high' | 'critical'
   ): number => {
     const impactWeights = {
       'negligible': 0.1,
       'low': 0.3,
       'medium': 0.5,
       'high': 0.7,
       'critical': 0.9
     };

     return probability * impactWeights[impact];
   };

   // 示例
   const riskScore = calculateRiskScore(90, 'high');
   // 90 * 0.7 = 63 (Medium-High风险)

   // 优先级分类
   const getPriority = (score: number): string => {
     if (score >= 70) return 'P0 (Critical)';
     if (score >= 50) return 'P1 (High)';
     if (score >= 30) return 'P2 (Medium)';
     return 'P3 (Low)';
   };
   ```

2. **CVE Scanning Automation** (CVE扫描自动化)
   ```yaml
   # .github/workflows/security-scan.yml
   name: Security Scan

   on:
     push:
       branches: [main, develop]
     pull_request:
     schedule:
       - cron: '0 2 * * *'       # 每日凌晨2点扫描

   jobs:
     dependency-scan:
       runs-on: ubuntu-latest
       steps:
         - name: npm audit
           run: npm audit --audit-level=moderate

         - name: Snyk scan
           uses: snyk/actions/node@master
           env:
             SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

         - name: Alert on Critical
           if: failure()
           uses: 8398a7/action-slack@v3
           with:
             status: ${{ job.status }}
             text: '🚨 Critical CVE detected!'
             webhook_url: ${{ secrets.SLACK_WEBHOOK }}
   ```

3. **GDPR Compliance Checklist** (GDPR合规清单)
   ```typescript
   const gdprChecklist = {
     dataMinimization: {
       check: '仅收集必要数据',
       implementation: '审查表单字段,移除非必要项(如生日、爱好)',
       status: 'not-met'
     },

     encryption: {
       check: '敏感数据加密',
       implementation: 'PostgreSQL TDE + 应用层AES-256加密',
       status: 'not-met'
     },

     rightToAccess: {
       check: '数据导出API',
       implementation: 'GET /api/users/{id}/export (JSON格式)',
       status: 'not-met'
     },

     rightToErasure: {
       check: '数据删除API',
       implementation: 'DELETE /api/users/{id} (软删除30天后硬删除)',
       status: 'not-met'
     },

     auditLogs: {
       check: '访问日志审计',
       implementation: '记录所有敏感数据访问(谁、何时、操作)',
       status: 'not-met'
     },

     dataPortability: {
       check: '数据可移植性',
       implementation: '导出格式支持JSON/CSV,可导入其他系统',
       status: 'not-met'
     }
   };

   // 计算合规率
   const complianceRate = (
     Object.values(gdprChecklist).filter(item => item.status === 'met').length /
     Object.keys(gdprChecklist).length
   ) * 100;
   ```

4. **Architecture Risk Assessment** (架构风险评估)
   ```typescript
   // 单点故障检测
   const detectSPOF = (architecture: Architecture): SPOF[] => {
     const spofs: SPOF[] = [];

     // 检查数据库
     if (!architecture.database.replication) {
       spofs.push({
         component: 'Database',
         type: 'database',
         impact: 'critical',
         recommendation: '实施主从复制 + 自动故障转移'
       });
     }

     // 检查缓存
     if (!architecture.cache.cluster) {
       spofs.push({
         component: 'Cache',
         type: 'cache',
         impact: 'high',
         recommendation: 'Redis Sentinel或Cluster'
       });
     }

     // 检查外部依赖
     for (const api of architecture.externalAPIs) {
       if (!api.retryMechanism || !api.fallback) {
         spofs.push({
           component: api.name,
           type: 'external-api',
           impact: 'critical',
           recommendation: '实施重试 + 降级方案'
         });
       }
     }

     return spofs;
   };

   // 扩展性评估
   const assessScalability = (
     currentLoad: Load,
     projectedLoad: Load,
     architecture: Architecture
   ): ScalabilityRisk[] => {
     const risks: ScalabilityRisk[] = [];

     // 计算容量余量
     const headroomMonths = calculateHeadroom(
       currentLoad,
       projectedLoad,
       architecture.capacity
     );

     if (headroomMonths < 12) {
       risks.push({
         component: 'Application',
         headroomMonths,
         recommendation: headroomMonths < 6
           ? '立即拆分微服务'
           : '6个月内规划微服务迁移'
       });
     }

     return risks;
   };
   ```

5. **Cost-Benefit Analysis** (成本-收益分析)
   ```typescript
   const calculateROI = (risk: Risk): ROI => {
     const currentRiskCost = risk.probability * risk.impactCost;
     const mitigationCost = risk.mitigation.estimatedCost;
     const residualRiskCost = (
       risk.mitigation.probabilityAfter *
       risk.impactCost *
       (1 - risk.mitigation.effectiveness)
     );

     const savings = currentRiskCost - residualRiskCost;
     const roi = ((savings - mitigationCost) / mitigationCost) * 100;

     return {
       currentRiskCost,
       mitigationCost,
       residualRiskCost,
       savings,
       roi,
       paybackPeriod: mitigationCost / (savings / 12) // 月
     };
   };

   // 示例: CVE-2024-1234修复ROI
   const cveRisk = {
     probability: 0.75,
     impactCost: 10000000,       // $10M数据泄露损失
     mitigation: {
       estimatedCost: 800,       // $800修复成本
       probabilityAfter: 0.05,
       effectiveness: 0.95
     }
   };

   const roi = calculateROI(cveRisk);
   // currentRiskCost: $7.5M
   // mitigationCost: $800
   // savings: $7.0M
   // roi: 875,000% (极高ROI)
   // paybackPeriod: 0.0001个月(立即回本)
   ```

---

## Related Skills

- **code-reviewer** (5) - 代码质量检查和Code Smell检测
- **security-auditor** (7) - 深度安全审计和渗透测试
- **knowledge-manager** (30) - 风险报告存储和历史追溯
- **collaboration-hub** (31) - 风险沟通和行动项分配
- **project-planner** (29) - 风险缓解计划集成到项目时间线

---

## Changelog

### Version 2.0.0 (2025-12-12)
- ✨ Initial release with comprehensive risk assessment capabilities
- 🎯 Multi-dimensional risk identification (technical debt, security, architecture, compliance)
- 📊 Probability-impact matrix risk scoring (0-100)
- 🔐 CVE vulnerability scanning with CVSS integration
- 📜 GDPR/SOC2/HIPAA compliance checking
- 🏗️ Architecture risk assessment (SPOF, scalability, performance)
- 📈 Technical debt analysis with SonarQube integration
- 🔍 Dependency health check (outdated, license, supply chain)
- 🛡️ OWASP Top 10 security scanning
- 💰 Cost-benefit analysis and ROI calculation
- 📅 Immediate/short-term/medium-term/long-term action plans
- 📉 Risk trend tracking and historical analysis
- 🎓 Actionable remediation recommendations with timelines
- 🔢 Business impact assessment (revenue, reputation, legal
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
interface RiskAssessorInput {
}
```

### 输出接口

```typescript
interface RiskAssessorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

 penalty)
