---
name: 27-explainability-analyzer-G
description: AI explainability analyzer for model decision transparency. Supports SHAP/LIME analysis (feature contribution), feature importance ranking, bias detection (fairness analysis), counterfactual explanation (what-if analysis), compliance reports (GDPR/EU AI Act). Use for ML model debugging, compliance validation, model trustworthiness.
---

# Explainability Analyzer - AI可解释性分析器

**Version**: 2.0.0
**Category**: AI Enhancement
**Priority**: P2
**Last Updated**: 2025-12-12

---

## Description

AI模型可解释性分析工具,提供决策过程透明化、特征重要性分析、偏差检测和置信度评估。支持SHAP/LIME分析、attention可视化、反事实解释(counterfactuals)和公平性审计,确保AI系统符合监管要求并建立用户信任。

### Core Capabilities

- **Decision Explanation**: SHAP (SHapley Additive exPlanations)分析、LIME (Local Interpretable Model-agnostic Explanations)、attention权重可视化、决策树近似
- **Feature Importance**: 全局特征贡献排名、局部特征影响分析、特征交互效应检测、边际贡献计算
- **Bias Detection**: 性别/种族/年龄偏差检测、群体公平性指标(demographic parity, equalized odds)、disparate impact分析
- **Confidence Analysis**: 预测置信区间、不确定性量化(epistemic & aleatoric)、异常检测、校准曲线分析
- **Counterfactual Explanations**: 最小修改建议("如果X改为Y,结果将如何")、可操作性建议、成功概率估算
- **Compliance Reporting**: 自动生成GDPR/CCPA/EU AI Act合规文档、审计追踪、可解释性报告

---

## Instructions

### When to Activate

Trigger this skill when you encounter:

1. **Model Transparency Requirements** - 需要解释AI模型为何做出某个决策
2. **Regulatory Compliance** - GDPR第22条("automated decision-making right to explanation")、EU AI Act高风险系统
3. **Fairness Audits** - 检测和缓解算法偏差
4. **Debugging Model Behavior** - 理解模型在边界情况下的行为
5. **User Trust Building** - 向终端用户解释自动化决策
6. **Model Comparison** - 比较不同模型的可解释性和公平性

**Common trigger phrases**:
- "解释为什么模型拒绝了这个贷款申请"
- "分析模型是否存在性别偏差"
- "生成反事实解释"
- "检查模型置信度"
- "生成GDPR合规报告"

### Execution Flow

```mermaid
graph TD
    A[接收预测结果 + 输入数据] --> B{选择解释方法}
    B -->|黑盒模型| C[LIME局部解释]
    B -->|树模型| D[SHAP TreeExplainer]
    B -->|神经网络| E[SHAP DeepExplainer]
    B -->|Transformer| F[Attention可视化]

    C --> G[计算特征重要性]
    D --> G
    E --> G
    F --> G

    G --> H[生成反事实解释]
    H --> I{需要偏差检测?}

    I -->|是| J[计算公平性指标]
    I -->|否| K[跳过偏差检测]

    J --> L[分析敏感属性影响]
    K --> M[汇总解释结果]
    L --> M

    M --> N[计算置信度和不确定性]
    N --> O[生成可操作建议]
    O --> P{需要合规报告?}

    P -->|是| Q[生成GDPR/AI Act文档]
    P -->|否| R[仅返回技术分析]

    Q --> S[最终输出: 完整可解释性报告]
    R --> S
```

---

## TypeScript Interfaces

```typescript
/**
 * Explainability Analyzer输入配置
 */
interface ExplainabilityAnalyzerInput {
  /**
   * 模型预测信息
   */
  prediction: {
    input: Record<string, any>;     // 输入特征
    output: any;                    // 模型预测结果
    modelType: 'classification' | 'regression' | 'ranking';
    classes?: string[];             // 分类任务的类别列表
    probability?: number | Record<string, number>; // 预测概率
  };

  /**
   * 模型信息
   */
  model: {
    type: 'black-box' | 'tree-based' | 'neural-network' | 'transformer';
    framework?: 'sklearn' | 'tensorflow' | 'pytorch' | 'xgboost' | 'lightgbm';

    /**
     * 模型预测函数（用于LIME/SHAP）
     * @param inputs - 特征向量数组
     * @returns 预测结果数组
     */
    predictFunction?: (inputs: any[][]) => Promise<any[]>;

    /**
     * 模型对象（如果可访问）
     */
    modelObject?: any;
  };

  /**
   * 数据集信息（用于全局解释和偏差检测）
   */
  dataset?: {
    features: Array<{
      name: string;
      type: 'numeric' | 'categorical' | 'boolean';
      description?: string;
      sensitiveAttribute?: boolean; // 标记受保护属性（性别、种族等）
      range?: [number, number];      // 数值型特征范围
      categories?: string[];         // 类别型特征可选值
    }>;
    samples?: Array<Record<string, any>>; // 样本数据（用于统计分析）
    targetColumn?: string;           // 目标变量名称
  };

  /**
   * 解释方法配置
   */
  explanationMethods?: {
    shap?: {
      enabled: boolean;
      explainerType?: 'tree' | 'kernel' | 'deep' | 'linear' | 'partition';
      nSamples?: number;             // SHAP采样数量（default: 100）
    };
    lime?: {
      enabled: boolean;
      nSamples?: number;             // LIME扰动样本数（default: 5000）
      kernelWidth?: number;          // 核宽度
    };
    attention?: {
      enabled: boolean;
      layer?: string;                // Transformer层名称
      head?: number;                 // Attention head索引
    };
    counterfactual?: {
      enabled: boolean;
      maxChanges?: number;           // 最多修改几个特征（default: 3）
      diversityWeight?: number;      // 多样性权重（生成多个解释）
    };
  };

  /**
   * 偏差检测配置
   */
  biasDetection?: {
    enabled: boolean;
    sensitiveAttributes: string[];  // ['gender', 'race', 'age']

    /**
     * 公平性指标
     */
    metrics?: Array<
      | 'demographic-parity'         // 人口统计平等
      | 'equalized-odds'             // 机会均等
      | 'equal-opportunity'          // 平等机会
      | 'disparate-impact'           // 差异影响
      | 'individual-fairness'        // 个体公平
    >;

    /**
     * 敏感属性阈值
     */
    thresholds?: {
      demographicParity?: number;    // 不同群体接受率差异阈值（default: 0.2）
      disparateImpact?: number;      // 差异影响比率（default: 0.8）
    };
  };

  /**
   * 置信度分析配置
   */
  confidenceAnalysis?: {
    enabled: boolean;
    method?: 'bootstrap' | 'bayesian' | 'conformal';
    confidenceLevel?: number;        // 置信水平（default: 0.95）
    nBootstrap?: number;             // Bootstrap采样次数
  };

  /**
   * 合规报告配置
   */
  compliance?: {
    enabled: boolean;
    standards?: Array<'gdpr' | 'ccpa' | 'eu-ai-act' | 'sr-11-7'>;
    includeAuditTrail?: boolean;
    language?: 'en' | 'zh' | 'es' | 'fr' | 'de';
  };

  /**
   * 输出配置
   */
  output?: {
    includeVisualizations?: boolean; // 生成图表（SHAP waterfall, force plot）
    verbosity?: 'minimal' | 'standard' | 'detailed';
    format?: 'json' | 'html' | 'pdf';
  };
}

/**
 * Explainability Analyzer输出结果
 */
interface ExplainabilityAnalyzerOutput {
  /**
   * 决策摘要
   */
  summary: {
    decision: string;                // "approve", "reject", "flag for review"
    confidence: number;              // 0-1
    explainabilityScore: number;     // 0-100, 可解释性评分
    fairnessScore: number;           // 0-100, 公平性评分
    riskLevel: 'low' | 'medium' | 'high';
  };

  /**
   * 特征重要性（局部 - 针对本次预测）
   */
  localExplanation: {
    method: 'shap' | 'lime' | 'attention';

    features: Array<{
      name: string;
      value: any;
      impact: number;                // 对预测的影响（正/负）
      importance: number;            // 绝对重要性（0-1）
      explanation: string;           // 人类可读的解释
      direction: 'positive' | 'negative' | 'neutral';
    }>;

    /**
     * 可视化数据（如启用）
     */
    visualization?: {
      type: 'waterfall' | 'force-plot' | 'bar-chart' | 'attention-heatmap';
      data: any;                     // Chart.js / Plotly数据格式
      imageUrl?: string;             // 生成的图片URL
    };
  };

  /**
   * 全局特征重要性（整个模型）
   */
  globalExplanation?: {
    features: Array<{
      name: string;
      averageImpact: number;
      importanceRank: number;
      description: string;
    }>;

    /**
     * 特征交互效应
     */
    interactions?: Array<{
      features: [string, string];
      interactionStrength: number;
      explanation: string;
    }>;
  };

  /**
   * 反事实解释（"如果...那么..."）
   */
  counterfactuals?: {
    description: string;

    scenarios: Array<{
      id: string;
      changes: Array<{
        feature: string;
        currentValue: any;
        suggestedValue: any;
        changeType: 'increase' | 'decrease' | 'modify';
        feasibility: 'easy' | 'moderate' | 'hard';
        actionable: boolean;
      }>;

      predictedOutcome: {
        decision: string;
        probability: number;
        confidence: number;
      };

      successProbability: number;    // 达成该反事实的可能性
      cost?: number;                 // 实现该变化的成本/努力
    }>;

    recommendation: string;          // 最推荐的反事实场景
  };

  /**
   * 偏差检测结果
   */
  biasAnalysis?: {
    overallFairnessScore: number;    // 0-100

    findings: Array<{
      sensitiveAttribute: string;
      metric: string;                // 'demographic-parity', 'equalized-odds', etc.
      value: number;
      threshold: number;
      passed: boolean;
      severity: 'critical' | 'high' | 'medium' | 'low';
      explanation: string;

      /**
       * 不同群体的统计数据
       */
      groupStatistics?: Record<string, {
        count: number;
        approvalRate?: number;
        falsePositiveRate?: number;
        falseNegativeRate?: number;
      }>;
    }>;

    recommendations: Array<{
      priority: 'critical' | 'high' | 'medium' | 'low';
      issue: string;
      mitigation: string;
      estimatedImpact: string;
    }>;
  };

  /**
   * 置信度和不确定性分析
   */
  confidenceAnalysis?: {
    pointEstimate: number;           // 预测值
    confidenceInterval: {
      lower: number;
      upper: number;
      level: number;                 // 0.95 for 95% CI
    };

    uncertainty: {
      total: number;                 // 总不确定性
      epistemic: number;             // 认知不确定性（模型不确定性）
      aleatoric: number;             // 偶然不确定性（数据噪声）
    };

    calibration: {
      score: number;                 // 0-1, 1=perfect calibration
      bins: Array<{
        predictedProbability: number;
        actualFrequency: number;
        count: number;
      }>;
    };

    outlierScore?: number;           // 输入是否为异常值（0-1）
  };

  /**
   * 可操作建议
   */
  recommendations: Array<{
    type: 'decision-review' | 'model-improvement' | 'applicant-action' | 'compliance';
    priority: 'critical' | 'high' | 'medium' | 'low';
    target: 'user' | 'developer' | 'auditor';
    title: string;
    description: string;

    actionSteps?: {
      steps: string[];
      estimatedTime?: string;
      difficulty?: 'easy' | 'medium' | 'hard';
    };
  }>;

  /**
   * 合规文档（如启用）
   */
  complianceReport?: {
    standard: 'gdpr' | 'ccpa' | 'eu-ai-act';
    generatedAt: string;             // ISO timestamp

    /**
     * GDPR Article 22 - Right to Explanation
     */
    gdprArticle22?: {
      hasHumanInvolved: boolean;
      explanationProvided: boolean;
      contestMechanism: string;
      dataSubjectRights: string[];
    };

    /**
     * EU AI Act - High-risk System Documentation
     */
    euAIAct?: {
      riskCategory: 'minimal' | 'limited' | 'high' | 'unacceptable';
      transparencyObligations: {
        technicalDocumentation: boolean;
        userInformation: boolean;
        humanOversight: boolean;
      };
      conformityAssessment: string;
    };

    auditTrail?: Array<{
      timestamp: string;
      action: string;
      userId?: string;
      details: Record<string, any>;
    }>;

    documentUrl?: string;            // PDF报告URL
  };

  /**
   * 元数据
   */
  metadata: {
    analysisTimestamp: string;
    executionTimeMs: number;
    modelVersion?: string;
    analyzerVersion: string;
  };
}

/**
 * 特征重要性（单个特征）
 */
interface FeatureContribution {
  name: string;
  value: any;
  shapValue?: number;               // SHAP值
  limeWeight?: number;              // LIME权重
  impact: number;                   // 统一的影响分数
  percentageContribution: number;   // 对最终决策的百分比贡献
}

/**
 * 反事实场景
 */
interface CounterfactualScenario {
  changes: Array<{
    feature: string;
    from: any;
    to: any;
  }>;
  newPrediction: any;
  distance: number;                 // 与原始输入的距离
  plausibility: number;             // 0-1
}

/**
 * 公平性指标
 */
interface FairnessMetrics {
  demographicParity: number;        // 0=perfect parity
  equalizedOdds: {
    truePositiveRateDiff: number;
    falsePositiveRateDiff: number;
  };
  disparateImpact: number;          // 0.8-1.25 is acceptable (80% rule)
  individualFairness: number;       // Similar individuals should get similar predictions
}
```

---

## Usage Examples

### Example 1: 信贷审批模型可解释性分析 (Credit Approval Explanation)

**场景**: 解释为什么贷款申请被拒绝,并提供反事实建议帮助申请人改进

**输入**:
```typescript
const input: ExplainabilityAnalyzerInput = {
  prediction: {
    input: {
      age: 28,
      income: 45000,
      credit_score: 650,
      debt_ratio: 0.45,        // 债务收入比45%
      employment_years: 2,
      has_mortgage: false,
      num_credit_cards: 3,
      gender: 'female',
      zip_code: '94102'
    },
    output: 0,                  // 0=拒绝, 1=批准
    modelType: 'classification',
    classes: ['reject', 'approve'],
    probability: {
      reject: 0.73,
      approve: 0.27
    }
  },

  model: {
    type: 'tree-based',
    framework: 'xgboost',
    predictFunction: async (inputs) => {
      // XGBoost模型预测接口
      return model.predict(inputs);
    }
  },

  dataset: {
    features: [
      { name: 'age', type: 'numeric', range: [18, 80] },
      { name: 'income', type: 'numeric', range: [20000, 200000] },
      { name: 'credit_score', type: 'numeric', range: [300, 850] },
      { name: 'debt_ratio', type: 'numeric', range: [0, 1] },
      { name: 'employment_years', type: 'numeric', range: [0, 40] },
      { name: 'has_mortgage', type: 'boolean' },
      { name: 'num_credit_cards', type: 'numeric', range: [0, 20] },
      {
        name: 'gender',
        type: 'categorical',
        categories: ['male', 'female', 'other'],
        sensitiveAttribute: true  // 受保护属性
      },
      { name: 'zip_code', type: 'categorical' }
    ],
    samples: trainDataset,      // 历史训练数据
    targetColumn: 'approved'
  },

  explanationMethods: {
    shap: {
      enabled: true,
      explainerType: 'tree',    // XGBoost支持TreeExplainer（快速）
      nSamples: 100
    },
    counterfactual: {
      enabled: true,
      maxChanges: 3,             // 最多建议修改3个特征
      diversityWeight: 0.5
    }
  },

  biasDetection: {
    enabled: true,
    sensitiveAttributes: ['gender'],
    metrics: ['demographic-parity', 'equalized-odds', 'disparate-impact'],
    thresholds: {
      demographicParity: 0.2,    // 允许20%差异
      disparateImpact: 0.8       // 80% rule
    }
  },

  confidenceAnalysis: {
    enabled: true,
    method: 'bootstrap',
    confidenceLevel: 0.95,
    nBootstrap: 1000
  },

  compliance: {
    enabled: true,
    standards: ['gdpr', 'eu-ai-act'],
    includeAuditTrail: true,
    language: 'zh'
  },

  output: {
    includeVisualizations: true,
    verbosity: 'detailed',
    format: 'json'
  }
};
```

**输出**:
```typescript
const output: ExplainabilityAnalyzerOutput = {
  summary: {
    decision: 'reject',
    confidence: 0.73,
    explainabilityScore: 87,     // High explainability
    fairnessScore: 92,           // No significant bias detected
    riskLevel: 'medium'
  },

  localExplanation: {
    method: 'shap',
    features: [
      {
        name: 'debt_ratio',
        value: 0.45,
        impact: -0.28,           // 负面影响（降低批准概率）
        importance: 0.42,        // 最重要的特征
        explanation: "债务收入比45%显著超过安全阈值35%，这是拒绝的主要原因。高债务比率表明申请人可能难以偿还新贷款。",
        direction: 'negative'
      },
      {
        name: 'credit_score',
        value: 650,
        impact: -0.15,
        importance: 0.23,
        explanation: "信用分650低于推荐的700分最低标准。信用分反映了历史还款记录，较低的分数增加了违约风险。",
        direction: 'negative'
      },
      {
        name: 'employment_years',
        value: 2,
        impact: -0.08,
        importance: 0.12,
        explanation: "工作年限仅2年，低于行业平均5年。较短的工作经历意味着收入稳定性较低。",
        direction: 'negative'
      },
      {
        name: 'income',
        value: 45000,
        impact: +0.12,
        importance: 0.18,
        explanation: "年收入$45,000略高于最低要求$40,000，这是一个正面因素，但不足以抵消其他负面因素。",
        direction: 'positive'
      },
      {
        name: 'age',
        value: 28,
        impact: +0.05,
        importance: 0.08,
        explanation: "年龄28岁处于合理范围，对决策影响较小。",
        direction: 'positive'
      },
      {
        name: 'num_credit_cards',
        value: 3,
        impact: -0.02,
        importance: 0.03,
        explanation: "持有3张信用卡数量适中，影响很小。",
        direction: 'neutral'
      }
    ],

    visualization: {
      type: 'waterfall',
      data: {
        // SHAP waterfall chart数据
        baseValue: 0.27,         // 平均预测概率
        features: [
          { name: 'debt_ratio', value: -0.28 },
          { name: 'credit_score', value: -0.15 },
          { name: 'employment_years', value: -0.08 },
          { name: 'income', value: +0.12 },
          { name: 'age', value: +0.05 }
        ],
        finalValue: 0.27         // 实际预测概率（批准）
      },
      imageUrl: 'https://storage.example.com/shap-waterfall-abc123.png'
    }
  },

  globalExplanation: {
    features: [
      {
        name: 'credit_score',
        averageImpact: 0.31,
        importanceRank: 1,
        description: "信用分是全局最重要的特征，平均贡献31%的决策权重"
      },
      {
        name: 'debt_ratio',
        averageImpact: 0.28,
        importanceRank: 2,
        description: "债务收入比是第二重要特征，高债务比率强烈预示拒绝"
      },
      {
        name: 'income',
        averageImpact: 0.21,
        importanceRank: 3,
        description: "收入水平影响还款能力，贡献21%权重"
      }
    ],

    interactions: [
      {
        features: ['debt_ratio', 'income'],
        interactionStrength: 0.15,
        explanation: "债务比率和收入存在强交互：高收入可以部分抵消高债务比率的负面影响"
      },
      {
        features: ['credit_score', 'employment_years'],
        interactionStrength: 0.08,
        explanation: "长期稳定就业可以提升低信用分申请人的批准概率"
      }
    ]
  },

  counterfactuals: {
    description: "通过以下改变，申请人可以获得贷款批准：",
    scenarios: [
      {
        id: 'cf-1-minimal',
        changes: [
          {
            feature: 'debt_ratio',
            currentValue: 0.45,
            suggestedValue: 0.32,
            changeType: 'decrease',
            feasibility: 'moderate',
            actionable: true
          },
          {
            feature: 'credit_score',
            currentValue: 650,
            suggestedValue: 700,
            changeType: 'increase',
            feasibility: 'moderate',
            actionable: true
          }
        ],
        predictedOutcome: {
          decision: 'approve',
          probability: 0.89,
          confidence: 0.89
        },
        successProbability: 0.92,
        cost: 6              // 估算需要6-12个月
      },
      {
        id: 'cf-2-debt-only',
        changes: [
          {
            feature: 'debt_ratio',
            currentValue: 0.45,
            suggestedValue: 0.28,
            changeType: 'decrease',
            feasibility: 'moderate',
            actionable: true
          }
        ],
        predictedOutcome: {
          decision: 'approve',
          probability: 0.68,
          confidence: 0.68
        },
        successProbability: 0.68,
        cost: 3              // 仅需偿还部分债务
      },
      {
        id: 'cf-3-income-boost',
        changes: [
          {
            feature: 'income',
            currentValue: 45000,
            suggestedValue: 60000,
            changeType: 'increase',
            feasibility: 'hard',
            actionable: true
          },
          {
            feature: 'employment_years',
            currentValue: 2,
            suggestedValue: 4,
            changeType: 'increase',
            feasibility: 'hard',
            actionable: false     // 需要时间积累
          }
        ],
        predictedOutcome: {
          decision: 'approve',
          probability: 0.75,
          confidence: 0.75
        },
        successProbability: 0.35,  // 收入提升困难
        cost: 24             // 可能需要2年
      }
    ],
    recommendation: "推荐方案1（cf-1-minimal）：通过降低债务比率至32%并提升信用分至700，可以将批准概率从27%提升至89%。具体步骤：(1) 偿还$6,000债务或增加收入$9,000以降低债务比率；(2) 按时还款6-12个月提升信用分50分。"
  },

  biasAnalysis: {
    overallFairnessScore: 92,
    findings: [
      {
        sensitiveAttribute: 'gender',
        metric: 'demographic-parity',
        value: 0.03,         // 男女批准率差异仅3%
        threshold: 0.20,
        passed: true,
        severity: 'low',
        explanation: "男性和女性申请人的批准率差异为3%，远低于20%的可接受阈值，表明模型在性别方面公平。",
        groupStatistics: {
          'male': {
            count: 1250,
            approvalRate: 0.42
          },
          'female': {
            count: 1180,
            approvalRate: 0.39
          },
          'other': {
            count: 70,
            approvalRate: 0.41
          }
        }
      },
      {
        sensitiveAttribute: 'gender',
        metric: 'equalized-odds',
        value: 0.05,
        threshold: 0.10,
        passed: true,
        severity: 'low',
        explanation: "不同性别群体的真阳性率和假阳性率差异均小于5%，满足机会均等要求。",
        groupStatistics: {
          'male': {
            count: 1250,
            falsePositiveRate: 0.08,
            falseNegativeRate: 0.12
          },
          'female': {
            count: 1180,
            falsePositiveRate: 0.10,
            falseNegativeRate: 0.14
          }
        }
      },
      {
        sensitiveAttribute: 'gender',
        metric: 'disparate-impact',
        value: 0.93,         // 93% (在0.8-1.25可接受范围内)
        threshold: 0.80,
        passed: true,
        severity: 'low',
        explanation: "女性批准率为男性的93%（39%/42%），符合80%规则（disparate impact ratio ≥ 0.8），未检测到显著差异影响。"
      }
    ],
    recommendations: [
      {
        priority: 'low',
        issue: "女性申请人假阴性率略高（14% vs 12%）",
        mitigation: "考虑增加特征工程，捕捉可能对女性更有利的因素（如教育水平、储蓄习惯）",
        estimatedImpact: "可能提升女性批准率2-3个百分点"
      },
      {
        priority: 'medium',
        issue: "模型整体偏保守（拒绝率58%）",
        mitigation: "调整决策阈值从0.5降至0.45，或重新训练模型增加正样本权重",
        estimatedImpact: "批准率提升至50%，同时保持违约率<5%"
      }
    ]
  },

  confidenceAnalysis: {
    pointEstimate: 0.27,
    confidenceInterval: {
      lower: 0.22,
      upper: 0.32,
      level: 0.95
    },
    uncertainty: {
      total: 0.15,
      epistemic: 0.08,       // 模型不确定性（可通过更多训练数据降低）
      aleatoric: 0.07        // 数据噪声（无法消除）
    },
    calibration: {
      score: 0.93,           // 模型校准良好
      bins: [
        { predictedProbability: 0.1, actualFrequency: 0.09, count: 150 },
        { predictedProbability: 0.3, actualFrequency: 0.28, count: 320 },
        { predictedProbability: 0.5, actualFrequency: 0.51, count: 280 },
        { predictedProbability: 0.7, actualFrequency: 0.72, count: 210 },
        { predictedProbability: 0.9, actualFrequency: 0.89, count: 140 }
      ]
    },
    outlierScore: 0.12       // 不是异常值
  },

  recommendations: [
    {
      type: 'applicant-action',
      priority: 'critical',
      target: 'user',
      title: "建议申请人优先降低债务比率",
      description: "债务收入比45%是拒绝的首要原因。降低至32%以下可显著提升批准概率。",
      actionSteps: {
        steps: [
          "选项1: 偿还$6,000债务（从45%降至32%）",
          "选项2: 增加月收入$750（兼职或加薪）",
          "选项3: 组合方案 - 偿还$3,000债务 + 增加$400月收入"
        ],
        estimatedTime: "3-6个月",
        difficulty: 'moderate'
      }
    },
    {
      type: 'applicant-action',
      priority: 'high',
      target: 'user',
      title: "建议6个月后重新申请（改善信用分）",
      description: "信用分650低于推荐标准700。通过按时还款可在6-12个月内提升50分。",
      actionSteps: {
        steps: [
          "确保所有账单按时支付（设置自动还款）",
          "信用卡使用率保持在30%以下",
          "不要申请新的信用账户（避免硬查询）",
          "每月监控信用报告（Credit Karma免费）"
        ],
        estimatedTime: "6-12个月",
        difficulty: 'easy'
      }
    },
    {
      type: 'model-improvement',
      priority: 'medium',
      target: 'developer',
      title: "考虑增加'未来收入增长潜力'特征",
      description: "当前模型仅考虑当前收入，对于年轻申请人（如本案28岁）可能过于保守。",
      actionSteps: {
        steps: [
          "添加特征：教育水平、职业类型、行业前景",
          "计算'收入增长率'（过去2年收入变化）",
          "重新训练模型并评估对年轻申请人的影响"
        ],
        estimatedTime: "2-3周",
        difficulty: 'moderate'
      }
    },
    {
      type: 'compliance',
      priority: 'high',
      target: 'auditor',
      title: "此决策符合GDPR Article 22和EU AI Act要求",
      description: "已提供完整的决策解释、反事实建议和偏差分析。申请人有权要求人工复审。",
      actionSteps: {
        steps: [
          "存档本次解释报告（GDPR要求保留3年）",
          "向申请人发送拒绝通知 + 解释摘要",
          "提供人工复审渠道（compliance@bank.com）"
        ],
        estimatedTime: "立即执行",
        difficulty: 'easy'
      }
    }
  ],

  complianceReport: {
    standard: 'gdpr',
    generatedAt: '2025-12-12T10:30:00Z',
    gdprArticle22: {
      hasHumanInvolved: false,
      explanationProvided: true,
      contestMechanism: "申请人可通过compliance@bank.com申请人工复审",
      dataSubjectRights: [
        "Right to explanation (已提供)",
        "Right to contest (复审渠道可用)",
        "Right to opt-out of automated decision (可申请人工审批)"
      ]
    },
    euAIAct: {
      riskCategory: 'high',
      transparencyObligations: {
        technicalDocumentation: true,
        userInformation: true,
        humanOversight: true
      },
      conformityAssessment: "模型已通过第三方审计（Cert-ID: EU-AI-2025-001234）"
    },
    auditTrail: [
      {
        timestamp: '2025-12-12T10:29:45Z',
        action: 'model_prediction',
        userId: 'applicant-789',
        details: {
          modelVersion: 'credit-model-v2.3.1',
          inputHash: 'sha256:abc123...',
          outputHash: 'sha256:def456...'
        }
      },
      {
        timestamp: '2025-12-12T10:30:00Z',
        action: 'explanation_generated',
        details: {
          method: 'shap-tree',
          executionTimeMs: 145
        }
      }
    ],
    documentUrl: 'https://storage.example.com/compliance/gdpr-report-abc123.pdf'
  },

  metadata: {
    analysisTimestamp: '2025-12-12T10:30:00Z',
    executionTimeMs: 1850,
    modelVersion: 'credit-model-v2.3.1',
    analyzerVersion: '2.0.0'
  }
};
```

**效果**:
- **可解释性**: 清晰识别3个关键拒绝原因（债务比率、信用分、工作年限）
- **可操作性**: 提供具体的反事实建议（降低债务至32%、提升信用分至700）
- **公平性**: 通过3项指标验证无性别偏差
- **合规性**: 生成GDPR Article 22和EU AI Act合规文档
- **用户体验**: 申请人获得明确的改进路径,而非简单的"拒绝"

---

### Example 2: 招聘AI偏差检测 (Hiring AI Bias Audit)

**场景**: 审计招聘筛选AI是否存在年龄/性别偏差,确保符合平等就业法规

**输入**:
```typescript
const input: ExplainabilityAnalyzerInput = {
  prediction: {
    input: {
      years_experience: 18,
      education_level: 'bachelors',
      skills_match_score: 0.85,
      previous_companies: ['Google', 'Meta'],
      age: 45,              // 敏感属性
      gender: 'female',     // 敏感属性
      location: 'San Francisco'
    },
    output: 0,              // 0=未通过筛选, 1=推荐面试
    modelType: 'classification',
    probability: {
      reject: 0.62,
      interview: 0.38
    }
  },

  model: {
    type: 'neural-network',
    framework: 'tensorflow',
    predictFunction: async (inputs) => {
      return await recruitingModel.predict(inputs);
    }
  },

  dataset: {
    features: [
      { name: 'years_experience', type: 'numeric', range: [0, 40] },
      { name: 'education_level', type: 'categorical', categories: ['highschool', 'bachelors', 'masters', 'phd'] },
      { name: 'skills_match_score', type: 'numeric', range: [0, 1] },
      {
        name: 'age',
        type: 'numeric',
        range: [22, 70],
        sensitiveAttribute: true
      },
      {
        name: 'gender',
        type: 'categorical',
        categories: ['male', 'female', 'non-binary'],
        sensitiveAttribute: true
      }
    ],
    samples: historicalApplicants,  // 过去1年的5000个申请
    targetColumn: 'hired'
  },

  explanationMethods: {
    shap: {
      enabled: true,
      explainerType: 'deep',
      nSamples: 200
    },
    counterfactual: {
      enabled: true,
      maxChanges: 2
    }
  },

  biasDetection: {
    enabled: true,
    sensitiveAttributes: ['age', 'gender'],
    metrics: [
      'demographic-parity',
      'equalized-odds',
      'equal-opportunity'
    ],
    thresholds: {
      demographicParity: 0.15,    // 更严格的15%阈值
      disparateImpact: 0.85        // 85% rule for hiring
    }
  },

  compliance: {
    enabled: true,
    standards: ['sr-11-7'],       // EEOC guidelines
    includeAuditTrail: true
  }
};
```

**输出（关键部分）**:
```typescript
const output: ExplainabilityAnalyzerOutput = {
  summary: {
    decision: 'reject',
    confidence: 0.62,
    explainabilityScore: 78,
    fairnessScore: 45,           // 🚨 低分！检测到偏差
    riskLevel: 'high'
  },

  localExplanation: {
    method: 'shap',
    features: [
      {
        name: 'age',
        value: 45,
        impact: -0.22,           // 🚨 年龄45岁强烈负面影响
        importance: 0.35,
        explanation: "⚠️ 警告：年龄是决策的主要因素，这可能违反年龄歧视法（ADEA）。年龄45岁显著降低了面试概率。",
        direction: 'negative'
      },
      {
        name: 'skills_match_score',
        value: 0.85,
        impact: +0.18,
        importance: 0.28,
        explanation: "技能匹配度85%是强有力的正面因素，但被年龄因素抵消。",
        direction: 'positive'
      },
      {
        name: 'years_experience',
        value: 18,
        impact: -0.08,           // 🚨 经验越多反而不利？
        importance: 0.15,
        explanation: "⚠️ 异常：18年经验产生负面影响。模型可能倾向于经验较少的候选人。",
        direction: 'negative'
      }
    ]
  },

  biasAnalysis: {
    overallFairnessScore: 45,     // 🚨 严重偏差
    findings: [
      {
        sensitiveAttribute: 'age',
        metric: 'demographic-parity',
        value: 0.38,              // 38%差异，远超15%阈值
        threshold: 0.15,
        passed: false,            // ❌ 未通过
        severity: 'critical',
        explanation: "🚨 严重年龄偏差：40岁以上申请人通过率仅为24%，而30岁以下申请人通过率为62%，差异达38个百分点，严重违反ADEA（年龄歧视法）。",
        groupStatistics: {
          '22-30岁': {
            count: 1580,
            approvalRate: 0.62
          },
          '31-40岁': {
            count: 1820,
            approvalRate: 0.45
          },
          '41-50岁': {
            count: 1200,
            approvalRate: 0.24      // 🚨 显著更低
          },
          '50岁+': {
            count: 400,
            approvalRate: 0.18      // 🚨 极低
          }
        }
      },
      {
        sensitiveAttribute: 'gender',
        metric: 'demographic-parity',
        value: 0.08,
        threshold: 0.15,
        passed: true,
        severity: 'low',
        explanation: "性别偏差在可接受范围（男女通过率差异8%）。"
      },
      {
        sensitiveAttribute: 'age',
        metric: 'disparate-impact',
        value: 0.39,              // 🚨 远低于0.85阈值
        threshold: 0.85,
        passed: false,
        severity: 'critical',
        explanation: "40岁以上申请人的通过率仅为30岁以下申请人的39%（24%/62%），严重低于85% rule阈值，构成显著的差异影响（disparate impact）。"
      }
    ],

    recommendations: [
      {
        priority: 'critical',
        issue: "模型存在严重年龄歧视，可能违反联邦法律（ADEA）",
        mitigation: "立即暂停模型使用，移除年龄特征，重新训练模型并进行公平性测试。考虑使用adversarial debiasing或reweighting技术。",
        estimatedImpact: "消除年龄偏差，通过率差异降至<10%"
      },
      {
        priority: 'critical',
        issue: "经验年数与年龄高度相关，可能作为年龄的代理变量（proxy）",
        mitigation: "检查years_experience特征，确保其影响合理（更多经验应为正面因素）。考虑使用'relevant_experience'替代'total_experience'。",
        estimatedImpact: "避免间接年龄歧视"
      },
      {
        priority: 'high',
        issue: "模型未经过偏差测试即投入生产",
        mitigation: "建立持续监控流程，每月审计各人口统计群体的通过率。设置自动警报（通过率差异>15%触发）。",
        estimatedImpact: "预防未来偏差，确保持续合规"
      }
    ]
  },

  recommendations: [
    {
      type: 'compliance',
      priority: 'critical',
      target: 'developer',
      title: "🚨 立即暂停模型使用 - 存在法律风险",
      description: "模型表现出严重的年龄偏差，可能违反《年龄歧视法》（ADEA）和《平等就业机会法》（EEOC）。继续使用可能导致法律诉讼和监管处罚。",
      actionSteps: {
        steps: [
          "立即停用自动筛选系统，改为人工审查",
          "通知法务和合规团队进行风险评估",
          "审查过去6个月的筛选决策，识别可能的受害者",
          "准备整改计划（移除年龄特征、重新训练、公平性测试）"
        ],
        estimatedTime: "立即执行（24小时内）",
        difficulty: 'hard'
      }
    }
  ],

  metadata: {
    analysisTimestamp: '2025-12-12T11:00:00Z',
    executionTimeMs: 2300,
    analyzerVersion: '2.0.0'
  }
};
```

**关键发现**:
- **严重年龄偏差**: 40+岁申请人通过率仅为年轻申请人的39%
- **法律风险**: 违反ADEA和EEOC guidelines
- **代理变量**: years_experience可能作为年龄的间接指标
- **建议行动**: 立即暂停模型,移除偏差,重新训练

---

### Example 3: 医疗诊断AI置信度分析 (Medical Diagnosis Confidence Analysis)

**场景**: 分析医疗AI诊断的置信度和不确定性,支持医生决策

**输入**:
```typescript
const input: ExplainabilityAnalyzerInput = {
  prediction: {
    input: {
      patient_age: 62,
      symptom_duration_days: 7,
      fever: true,
      cough: true,
      shortness_of_breath: true,
      chest_xray_opacity: 0.65,
      white_blood_cell_count: 12500,
      c_reactive_protein: 85
    },
    output: 'pneumonia',
    modelType: 'classification',
    classes: ['healthy', 'bronchitis', 'pneumonia', 'covid-19', 'lung-cancer'],
    probability: {
      'healthy': 0.02,
      'bronchitis': 0.15,
      'pneumonia': 0.58,
      'covid-19': 0.22,
      'lung-cancer': 0.03
    }
  },

  model: {
    type: 'neural-network',
    framework: 'pytorch'
  },

  explanationMethods: {
    shap: {
      enabled: true,
      explainerType: 'deep'
    }
  },

  confidenceAnalysis: {
    enabled: true,
    method: 'bayesian',
    confidenceLevel: 0.95
  },

  output: {
    verbosity: 'detailed',
    includeVisualizations: true
  }
};
```

**输出（简化版）**:
```typescript
const output: ExplainabilityAnalyzerOutput = {
  summary: {
    decision: 'pneumonia',
    confidence: 0.58,           // 中等置信度
    explainabilityScore: 91,
    fairnessScore: 95,
    riskLevel: 'medium'         // 需要医生确认
  },

  localExplanation: {
    method: 'shap',
    features: [
      {
        name: 'chest_xray_opacity',
        value: 0.65,
        impact: +0.32,
        importance: 0.45,
        explanation: "胸部X光显示65%的混浊度，强烈支持肺炎诊断。这是最重要的影像学特征。",
        direction: 'positive'
      },
      {
        name: 'c_reactive_protein',
        value: 85,
        impact: +0.18,
        importance: 0.25,
        explanation: "C反应蛋白85 mg/L显著升高（正常<10），表明严重细菌感染，支持肺炎诊断。",
        direction: 'positive'
      },
      {
        name: 'shortness_of_breath',
        value: true,
        impact: +0.12,
        importance: 0.15,
        explanation: "呼吸困难是肺炎的典型症状之一。",
        direction: 'positive'
      }
    ]
  },

  confidenceAnalysis: {
    pointEstimate: 0.58,
    confidenceInterval: {
      lower: 0.48,
      upper: 0.68,
      level: 0.95
    },
    uncertainty: {
      total: 0.25,
      epistemic: 0.18,          // 模型不确定性较高
      aleatoric: 0.07
    },
    calibration: {
      score: 0.88               // 校准良好
    },
    outlierScore: 0.08
  },

  recommendations: [
    {
      type: 'decision-review',
      priority: 'high',
      target: 'user',
      title: "⚠️ 建议医生进一步确认诊断",
      description: "AI模型预测为肺炎（58%概率），但置信区间较宽（48-68%），且COVID-19概率也达到22%。建议进行PCR测试以排除COVID-19。",
      actionSteps: {
        steps: [
          "进行COVID-19 PCR测试（排除22%的COVID可能性）",
          "复查胸部X光（考虑CT扫描获得更清晰影像）",
          "根据测试结果调整治疗方案"
        ],
        estimatedTime: "24-48小时",
        difficulty: 'easy'
      }
    },
    {
      type: 'model-improvement',
      priority: 'medium',
      target: 'developer',
      title: "模型在肺炎/COVID-19区分上存在不确定性",
      description: "当前模型对两者的区分度不够（58% vs 22%）。建议增加COVID特异性特征（如嗅觉丧失、接触史）。",
      actionSteps: {
        steps: [
          "收集COVID特异性症状数据",
          "重新训练模型包含新特征",
          "在测试集上验证改进效果"
        ],
        estimatedTime: "2-3周",
        difficulty: 'moderate'
      }
    }
  ],

  metadata: {
    analysisTimestamp: '2025-12-12T12:00:00Z',
    executionTimeMs: 1650,
    analyzerVersion: '2.0.0'
  }
};
```

**临床价值**:
- **决策支持**: 医生获得58%肺炎概率,但需注意22% COVID可能性
- **不确定性量化**: 置信区间48-68%提醒医生进一步检查
- **可解释性**: X光混浊度和CRP升高是关键诊断依据
- **建议行动**: 进行PCR测试排除COVID-19

---

## Best Practices

### ✅ DO: Effective Explainability

```typescript
// ✅ GOOD: 多层次解释（全局+局部）
const goodExplanation = {
  global: {
    // 模型整体行为
    topFeatures: ['credit_score', 'debt_ratio', 'income'],
    decisionBoundary: '...'
  },
  local: {
    // 本次预测
    keyFactors: ['debt_ratio=0.45 (negative)', 'income=45k (positive)']
  }
};

// ✅ GOOD: 可操作的反事实解释
const goodCounterfactual = {
  changes: [
    {
      feature: 'debt_ratio',
      from: 0.45,
      to: 0.32,
      action: "偿还$6,000债务",     // 具体可行的行动
      feasibility: 'moderate',
      timeline: '3-6个月'
    }
  ],
  expectedOutcome: 'approve (89% probability)'
};

// ✅ GOOD: 使用校准后的置信度
const goodConfidence = {
  rawProbability: 0.73,
  calibratedProbability: 0.68,  // 经过calibration
  confidenceInterval: [0.58, 0.78],
  interpretation: "我们68%确信会拒绝，但有12-32%的不确定性"
};

// ✅ GOOD: 主动检测代理变量（proxy features）
const goodBiasCheck = {
  sensitiveAttribute: 'race',
  directUsage: false,             // 模型未直接使用race
  proxyFeatures: [
    {
      feature: 'zip_code',
      correlation_with_race: 0.72,  // ⚠️ 高度相关
      recommendation: "移除zip_code或使用debiasing技术"
    }
  ]
};
```

### ❌ DON'T: Poor Explainability Practices

```typescript
// ❌ BAD: 无法解释的"黑盒"决策
const badExplanation = {
  decision: 'reject',
  reason: '模型决定拒绝'  // 毫无信息量
};

// ❌ BAD: 不可操作的建议
const badCounterfactual = {
  suggestion: "如果你的信用分更高，就会被批准"
  // 问题：没有说明需要多高、如何提升
};

// ❌ BAD: 忽略不确定性
const badConfidence = {
  prediction: 'pneumonia',
  confidence: 0.58
  // 问题：58%其实置信度不高，但未提醒医生注意
};

// ❌ BAD: 仅测试直接偏差，忽略间接偏差
const badBiasCheck = {
  gender: 'no direct usage',  // ✓
  // ❌ 但未检查years_experience与gender的相关性
  //    （女性可能因育儿gap在工作年限上偏低）
};

// ❌ BAD: 过度复杂的技术解释
const badForUser = {
  explanation: "SHAP值为-0.28，TreeExplainer使用Shapley值理论...",
  // 问题：普通用户无法理解SHAP值
};
```

### 🎯 Implementation Guidelines

1. **Choose Right Explanation Method** (选择合适的解释方法)
   ```typescript
   // Tree-based models (XGBoost, LightGBM) → SHAP TreeExplainer (快速)
   if (model.type === 'xgboost') {
     use: 'shap-tree';  // 毫秒级
   }

   // Neural networks → SHAP DeepExplainer或LIME
   if (model.type === 'neural-network') {
     use: 'shap-deep';  // 秒级
     // 或 'lime' (更慢但模型无关)
   }

   // Black-box models → LIME
   if (!modelAccessible) {
     use: 'lime';       // 最通用
   }
   ```

2. **Calibrate Confidence** (校准置信度)
   ```python
   from sklearn.calibration import calibration_curve

   # 检查模型校准
   prob_true, prob_pred = calibration_curve(
       y_true, y_pred_proba, n_bins=10
   )

   # 如果校准差（prob_true ≠ prob_pred），使用CalibratedClassifierCV
   from sklearn.calibration import CalibratedClassifierCV
   calibrated_model = CalibratedClassifierCV(base_model, method='isotonic')
   calibrated_model.fit(X_train, y_train)
   ```

3. **Detect Proxy Features** (检测代理变量)
   ```python
   # 检查特征与敏感属性的相关性
   from scipy.stats import chi2_contingency, pearsonr

   for feature in features:
       if feature.type == 'categorical':
           # 卡方检验
           chi2, p_value = chi2_contingency(pd.crosstab(df[feature], df['race']))
           if p_value < 0.05:
               warn(f"{feature} may be proxy for race")
       else:
           # Pearson相关
           corr, p_value = pearsonr(df[feature], df['age'])
           if abs(corr) > 0.5:
               warn(f"{feature} correlated with age (r={corr})")
   ```

4. **Layered Explanations** (分层解释)
   - **Tier 1 (用户)**: "您的贷款被拒绝，因为债务收入比过高（45%）"
   - **Tier 2 (专家)**: "债务比率SHAP值=-0.28，贡献了42%的拒绝决策"
   - **Tier 3 (开发者)**: "TreeExplainer分析显示debt_ratio在树的第2层分裂，阈值0.35"

5. **Continuous Monitoring** (持续监控)
   ```typescript
   // 每月审计偏差
   scheduleCronJob('0 0 1 * *', async () => {
     const lastMonthData = await getApplicants(lastMonth);

     const biasReport = await analyzeExplainability({
       dataset: lastMonthData,
       biasDetection: {
         enabled: true,
         sensitiveAttributes: ['gender', 'race', 'age']
       }
     });

     if (biasReport.fairnessScore < 80) {
       sendAlert('Bias detected in production model!');
     }
   });
   ```

---

## Related Skills

- **ai-code-optimizer** (26) - Analyzes code performance using similar SHAP-like attribution
- **prompt-engineer** (27) - Optimizes prompts for better AI explainability
- **risk-assessor** (32) - Uses explainability for risk analysis
- **test-generator** (3) - Generates tests for edge cases identified by explainability

---

## Changelog

### Version 2.0.0 (2025-12-12)
- ✨ Initial release with comprehensive AI explainability capabilities
- 🔍 SHAP/LIME integration for model-agnostic explanations
- ⚖️ Bias detection across demographic groups (gender, race, age)
- 🎯 Counterfactual explanation generation with actionable recommendations
- 📊 Confidence interval and uncertainty quantification
- 📜 GDPR/EU AI Act compliance reporting
- 🏥 Medical AI uncertainty analysis example
- 💼 Credit scoring fairness audit example
- 👔 Hiring AI bias detection example
- 🛡️ Proxy feature detection for indirect bias
- 📈 Model calibration
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
interface ExplainabilityAnalyzerInput {
}
```

### 输出接口

```typescript
interface ExplainabilityAnalyzerOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

 analysis
