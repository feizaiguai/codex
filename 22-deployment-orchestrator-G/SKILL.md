---
name: 22-deployment-orchestrator-G
description: Deployment orchestrator for multi-cloud deployment automation. Supports multi-cloud (Kubernetes/AWS/Azure/GCP), advanced deployment strategies (Blue-Green/Canary/Rolling), health checks (Liveness/Readiness), auto-rollback (failure detection), traffic management (Istio/Linkerd). Use for multi-environment deployment, zero-downtime updates, canary releases.
---

# Deployment Orchestrator

**Version**: 2.0.0
**Category**: DevOps
**Priority**: P1
**Last Updated**: 2025-12-12

---

## Description

Deployment Orchestrator provides comprehensive multi-cloud deployment automation with support for multiple deployment strategies including blue-green, canary releases, rolling updates, and A/B testing. It handles container orchestration across Kubernetes, AWS ECS/EKS/Lambda, Azure AKS/Container Apps, and GCP GKE/Cloud Run. The skill includes automated health checks, rollback mechanisms, traffic management, and cost optimization.

### Core Capabilities

1. **Multi-Cloud Platform Support**
   - Kubernetes (self-hosted, EKS, AKS, GKE)
   - AWS: ECS, EKS, Lambda, Fargate
   - Azure: AKS, Container Apps, App Service
   - GCP: GKE, Cloud Run, App Engine
   - Docker Swarm and Docker Compose

2. **Advanced Deployment Strategies**
   - Rolling updates with configurable surge and unavailability
   - Blue-green deployments with instant traffic switching
   - Canary releases with progressive rollout (10% → 25% → 50% → 100%)
   - A/B testing with traffic splitting
   - Shadow deployments for production testing
   - Recreate strategy for breaking changes

3. **Container Orchestration**
   - Docker multi-stage builds for optimization
   - Container registry management (ECR, ACR, GCR, Docker Hub)
   - Helm chart generation and management
   - Kubernetes manifest generation
   - Image scanning and vulnerability assessment

4. **Health Checks & Monitoring**
   - Liveness probes (restart unhealthy containers)
   - Readiness probes (remove from load balancer)
   - Startup probes (slow-starting applications)
   - Custom health check endpoints
   - Prometheus metrics integration
   - Real-time deployment monitoring

5. **Automated Rollback**
   - Error rate threshold triggers
   - Latency threshold triggers
   - Health check failure triggers
   - CrashLoopBackOff detection
   - Custom business metric triggers
   - Instant rollback to previous version

6. **Traffic Management**
   - Load balancer configuration
   - Ingress controller setup
   - SSL/TLS certificate management
   - Rate limiting and throttling
   - CDN integration
   - Service mesh configuration (Istio/Linkerd)

---

## Instructions

### Activation Triggers

This skill activates when detecting:
- "deploy to production/staging/development"
- "blue-green deployment"
- "canary release"
- "Kubernetes deployment"
- "Docker container deployment"
- "deploy to AWS/Azure/GCP"
- "zero-downtime deployment"
- "rollback deployment"
- "traffic switching"
- "create Helm chart"

### Execution Flow

```mermaid
graph TD
    A[Deployment Request] --> B{Platform Selection}

    B -->|Kubernetes| C[K8s Deployment Flow]
    C --> C1[Build Docker Image]
    C1 --> C2[Push to Registry]
    C2 --> C3[Generate K8s Manifests]
    C3 --> C4[Apply Strategy]
    C4 --> C5{Strategy Type}

    C5 -->|Rolling| D1[Configure Rolling Update]
    D1 --> D2[Apply Deployment]
    D2 --> D3[Monitor Health]

    C5 -->|Blue-Green| E1[Deploy Green Environment]
    E1 --> E2[Test Green]
    E2 --> E3[Switch Traffic]
    E3 --> E4[Delete Blue]

    C5 -->|Canary| F1[Deploy Canary 10%]
    F1 --> F2[Monitor Metrics]
    F2 --> F3{Metrics OK?}
    F3 -->|Yes| F4[Promote to 25%]
    F4 --> F5[Monitor Again]
    F5 --> F6{Metrics OK?}
    F6 -->|Yes| F7[Promote to 50%]
    F7 --> F8[Monitor Again]
    F8 --> F9{Metrics OK?}
    F9 -->|Yes| F10[Promote to 100%]
    F3 -->|No| G[Auto Rollback]
    F6 -->|No| G
    F9 -->|No| G

    B -->|Lambda| H[Serverless Flow]
    H --> H1[Package Function]
    H1 --> H2[Upload to S3]
    H2 --> H3[Update Function Code]
    H3 --> H4[Publish New Version]
    H4 --> H5[Blue-Green Alias Switch]

    B -->|Cloud Run| I[GCP Flow]
    I --> I1[Build Container]
    I1 --> I2[Push to GCR]
    I2 --> I3[Deploy Revision]
    I3 --> I4[Test with 0% Traffic]
    I4 --> I5[Switch 100% Traffic]

    D3 --> J[Health Check Validation]
    E4 --> J
    F10 --> J
    H5 --> J
    I5 --> J

    J --> K{Deployment Success?}
    K -->|Yes| L[Generate Report]
    K -->|No| M[Rollback]
    M --> N[Rollback Report]
```

---

## Input Schema

```typescript
/**
 * Input configuration for deployment orchestration
 */
interface DeploymentOrchestratorInput {
  /**
   * Application metadata
   */
  application: {
    /**
     * Application name (used for resource naming)
     * @example "payment-service"
     */
    name: string;

    /**
     * Version to deploy (semantic versioning recommended)
     * @example "2.3.0"
     */
    version: string;

    /**
     * Application type
     */
    type: 'container' | 'serverless' | 'vm' | 'static';

    /**
     * Source code repository
     */
    repository?: {
      /**
       * Git repository URL
       */
      url: string;

      /**
       * Branch to deploy from
       * @default "main"
       */
      branch?: string;

      /**
       * Path to Dockerfile
       * @default "Dockerfile"
       */
      dockerfile?: string;
    };
  };

  /**
   * Deployment target configuration
   */
  target: {
    /**
     * Target platform
     */
    platform: 'kubernetes' | 'aws-ecs' | 'aws-eks' | 'aws-lambda' |
              'azure-aks' | 'azure-container-apps' | 'gcp-gke' |
              'gcp-cloud-run' | 'docker-swarm';

    /**
     * Environment name
     */
    environment: 'dev' | 'staging' | 'production' | 'qa';

    /**
     * Cloud region
     * @example "us-east-1", "eastus", "us-central1"
     */
    region?: string;

    /**
     * Cluster name (for Kubernetes)
     */
    cluster?: string;

    /**
     * Namespace (for Kubernetes)
     * @default "default"
     */
    namespace?: string;
  };

  /**
   * Deployment strategy configuration
   */
  strategy: {
    /**
     * Deployment strategy type
     */
    type: 'rolling-update' | 'blue-green' | 'canary' | 'recreate' | 'ab-test';

    /**
     * Rolling update configuration
     */
    rollingUpdate?: {
      /**
       * Maximum additional replicas during update
       * @example 2 or "25%"
       */
      maxSurge: number | string;

      /**
       * Maximum unavailable replicas during update
       * @example 0 or "0%"
       */
      maxUnavailable: number | string;

      /**
       * Interval between updating pods (seconds)
       * @default 10
       */
      updateInterval?: number;
    };

    /**
     * Blue-green deployment configuration
     */
    blueGreen?: {
      /**
       * Traffic switching mode
       */
      routeTraffic: 'manual' | 'automatic';

      /**
       * Testing window before switching (minutes)
       * @default 10
       */
      testWindow?: number;

      /**
       * Auto-rollback on failure
       * @default true
       */
      autoRollbackOnFailure?: boolean;
    };

    /**
     * Canary deployment configuration
     */
    canary?: {
      /**
       * Traffic percentage steps
       * @example [10, 25, 50, 100]
       */
      steps: number[];

      /**
       * Interval between steps (minutes)
       * @default 15
       */
      stepInterval: number;

      /**
       * Metric thresholds for promotion
       */
      metrics?: {
        /**
         * Maximum error rate (%)
         * @default 1.0
         */
        errorRate?: number;

        /**
         * Maximum P95 latency (ms)
         * @default 500
         */
        latency?: number;

        /**
         * Minimum success rate (%)
         * @default 99.0
         */
        successRate?: number;
      };

      /**
       * Automatically promote if metrics pass
       * @default false
       */
      autoPromote?: boolean;

      /**
       * Automatically rollback if metrics fail
       * @default true
       */
      autoRollback?: boolean;
    };
  };

  /**
   * Resource configuration
   */
  resources: {
    /**
     * Number of replicas
     * @default 1
     */
    replicas?: number;

    /**
     * Horizontal Pod Autoscaler configuration
     */
    autoscaling?: {
      enabled: boolean;
      minReplicas: number;
      maxReplicas: number;

      /**
       * Target CPU utilization (%)
       * @default 70
       */
      targetCPU?: number;

      /**
       * Target memory utilization (%)
       * @default 80
       */
      targetMemory?: number;

      /**
       * Custom metrics for scaling
       */
      customMetrics?: Array<{
        name: string;
        targetValue: number;
      }>;
    };

    /**
     * Container resource requirements
     */
    container?: {
      /**
       * CPU request/limit
       * @example "500m", "1", "2000m"
       */
      cpu: string;

      /**
       * Memory request/limit
       * @example "512Mi", "2Gi"
       */
      memory: string;

      /**
       * GPU request (optional)
       * @example "1"
       */
      gpu?: string;
    };
  };

  /**
   * Networking configuration
   */
  networking: {
    /**
     * Container ports
     */
    ports?: Array<{
      name?: string;
      containerPort: number;
      protocol?: 'TCP' | 'UDP';
    }>;

    /**
     * Ingress configuration
     */
    ingress?: {
      enabled: boolean;
      host?: string;
      tls?: boolean;
      annotations?: Record<string, string>;
      paths?: Array<{
        path: string;
        pathType?: 'Prefix' | 'Exact';
      }>;
    };

    /**
     * Load balancer configuration
     */
    loadBalancer?: {
      type: 'internal' | 'external';

      /**
       * Health check configuration
       */
      healthCheck?: {
        path: string;
        port: number;
        interval?: number;
        timeout?: number;
        healthyThreshold?: number;
        unhealthyThreshold?: number;
      };
    };
  };

  /**
   * Configuration and secrets
   */
  configuration: {
    /**
     * Environment variables
     */
    environmentVariables?: Record<string, string>;

    /**
     * Secret references (not plaintext values)
     */
    secrets?: Record<string, string>;

    /**
     * ConfigMaps (Kubernetes)
     */
    configMaps?: Record<string, any>;

    /**
     * Volume mounts
     */
    volumes?: Array<{
      name: string;
      type: 'configMap' | 'secret' | 'persistentVolumeClaim' | 'emptyDir';
      mountPath: string;
      source?: string;
    }>;
  };

  /**
   * Monitoring and health checks
   */
  monitoring: {
    /**
     * Health check probes
     */
    healthCheck?: {
      /**
       * Liveness probe (restart if fails)
       */
      liveness?: {
        path: string;
        port: number;
        initialDelay?: number;
      };

      /**
       * Readiness probe (remove from LB if fails)
       */
      readiness?: {
        path: string;
        port: number;
        initialDelay?: number;
      };

      /**
       * Startup probe (for slow-starting apps)
       */
      startup?: {
        path: string;
        port: number;
        failureThreshold?: number;
      };
    };

    /**
     * Logging configuration
     */
    logging?: {
      driver: 'json-file' | 'syslog' | 'fluentd' | 'cloudwatch';
      options?: Record<string, string>;
    };

    /**
     * Metrics configuration
     */
    metrics?: {
      prometheus?: boolean;
      customMetrics?: string[];
    };
  };

  /**
   * Rollback configuration
   */
  rollback?: {
    enabled: boolean;

    /**
     * Automatic rollback triggers
     */
    autoRollbackTriggers?: {
      /**
       * Error rate threshold (%)
       */
      errorRate?: number;

      /**
       * Trigger on CrashLoopBackOff
       */
      crashLoopBackoff?: boolean;

      /**
       * Health check failure count
       */
      healthCheckFailures?: number;
    };
  };

  /**
   * Notification configuration
   */
  notifications?: {
    channels?: ('email' | 'slack' | 'webhook')[];
    recipients?: string[];
    webhookUrl?: string;
  };
}

/**
 * Output from deployment orchestration
 */
interface DeploymentOrchestratorOutput {
  /**
   * Deployment metadata
   */
  deployment: {
    id: string;
    status: 'pending' | 'in-progress' | 'completed' | 'failed' | 'rolled-back';
    strategy: string;
    startTime: string;
    endTime?: string;
    duration?: number;
  };

  /**
   * Generated manifests and configurations
   */
  manifests: {
    /**
     * Kubernetes manifests
     */
    kubernetes?: {
      deployment: string;
      service?: string;
      ingress?: string;
      configMap?: string;
      secret?: string;
      hpa?: string;
      helmChart?: string;
    };

    /**
     * Docker configuration
     */
    docker?: {
      dockerfile: string;
      dockerCompose?: string;
      buildCommands: string[];
      imageTag: string;
    };

    /**
     * Cloud-specific configurations
     */
    cloudSpecific?: {
      awsEcs?: any;
      awsLambda?: any;
      azureContainerApp?: any;
      gcpCloudRun?: any;
    };
  };

  /**
   * Deployment step execution details
   */
  deployment_steps: Array<{
    step: number;
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
    command?: string;
    output?: string;
    duration?: number;
    timestamp: string;
  }>;

  /**
   * Canary deployment progress
   */
  canary_progress?: {
    currentStep: number;
    totalSteps: number;
    currentTrafficPercentage: number;
    metrics: {
      errorRate: number;
      latency: number;
      requestsPerSecond: number;
      successRate: number;
    };
    decision: 'continue' | 'pause' | 'rollback' | 'promote';
  };

  /**
   * Resource endpoints and URLs
   */
  resources: {
    endpoints: string[];
    loadBalancerIP?: string;
    ingressURL?: string;
    dashboardURL?: string;
    logsURL?: string;
  };

  /**
   * Health status
   */
  health: {
    overallStatus: 'healthy' | 'degraded' | 'unhealthy';
    readyReplicas: number;
    totalReplicas: number;
    conditions: Array<{
      type: string;
      status: boolean;
      reason?: string;
      message?: string;
    }>;
  };

  /**
   * Rollback plan
   */
  rollback_plan?: {
    previousVersion: string;
    rollbackCommand: string;
    estimatedTime: number;
    impactAssessment: string;
  };

  /**
   * Recommendations
   */
  recommendations?: string[];

  /**
   * Cost estimate
   */
  costs?: {
    estimatedMonthlyCost: number;
    currency: string;
    breakdown: Record<string, number>;
  };
}
```

---

## Usage Examples

### Example 1: Kubernetes Canary Deployment - Production Node.js Microservice

**Scenario**: Deploy a payment service to production Kubernetes cluster using canary strategy with automated promotion based on metrics.

**Input**:
```typescript
const canaryDeployment: DeploymentOrchestratorInput = {
  application: {
    name: 'payment-service',
    version: '2.3.0',
    type: 'container',
    repository: {
      url: 'https://github.com/company/payment-service',
      branch: 'release/v2.3.0',
      dockerfile: 'Dockerfile.production'
    }
  },

  target: {
    platform: 'kubernetes',
    environment: 'production',
    region: 'us-east-1',
    cluster: 'prod-cluster',
    namespace: 'payments'
  },

  strategy: {
    type: 'canary',
    canary: {
      steps: [10, 25, 50, 100],
      stepInterval: 15,
      metrics: {
        errorRate: 1.0,
        latency: 200,
        successRate: 99.5
      },
      autoPromote: true,
      autoRollback: true
    }
  },

  resources: {
    replicas: 6,
    autoscaling: {
      enabled: true,
      minReplicas: 6,
      maxReplicas: 20,
      targetCPU: 70,
      targetMemory: 80,
      customMetrics: [
        { name: 'requests_per_second', targetValue: 1000 }
      ]
    },
    container: {
      cpu: '1000m',
      memory: '2Gi'
    }
  },

  networking: {
    ports: [
      { name: 'http', containerPort: 3000, protocol: 'TCP' },
      { name: 'metrics', containerPort: 9090, protocol: 'TCP' }
    ],
    ingress: {
      enabled: true,
      host: 'payment.company.com',
      tls: true,
      annotations: {
        'nginx.ingress.kubernetes.io/rate-limit': '100',
        'cert-manager.io/cluster-issuer': 'letsencrypt-prod'
      },
      paths: [
        { path: '/api/payment', pathType: 'Prefix' }
      ]
    },
    loadBalancer: {
      type: 'external',
      healthCheck: {
        path: '/health',
        port: 3000,
        interval: 10,
        timeout: 5,
        healthyThreshold: 2,
        unhealthyThreshold: 3
      }
    }
  },

  configuration: {
    environmentVariables: {
      NODE_ENV: 'production',
      LOG_LEVEL: 'info',
      PAYMENT_GATEWAY_TIMEOUT: '30000',
      REDIS_POOL_SIZE: '10'
    },
    secrets: {
      DATABASE_URL: 'payment-db-credentials',
      STRIPE_API_KEY: 'payment-stripe-secret',
      JWT_SECRET: 'payment-jwt-secret'
    },
    configMaps: {
      'rate-limits': 'payment-rate-limits-config'
    },
    volumes: [
      {
        name: 'logs',
        type: 'emptyDir',
        mountPath: '/var/log/app'
      }
    ]
  },

  monitoring: {
    healthCheck: {
      liveness: {
        path: '/health/liveness',
        port: 3000,
        initialDelay: 30
      },
      readiness: {
        path: '/health/readiness',
        port: 3000,
        initialDelay: 10
      },
      startup: {
        path: '/health/startup',
        port: 3000,
        failureThreshold: 30
      }
    },
    logging: {
      driver: 'json-file',
      options: {
        'max-size': '10m',
        'max-file': '3'
      }
    },
    metrics: {
      prometheus: true,
      customMetrics: ['payment_transactions_total', 'payment_latency_seconds']
    }
  },

  rollback: {
    enabled: true,
    autoRollbackTriggers: {
      errorRate: 5.0,
      crashLoopBackoff: true,
      healthCheckFailures: 5
    }
  },

  notifications: {
    channels: ['slack', 'email'],
    recipients: ['devops@company.com'],
    webhookUrl: 'https://hooks.slack.com/services/xxx'
  }
};
```

**Generated Kubernetes Deployment Manifest**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: payments
  labels:
    app: payment-service
    version: "2.3.0"
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
        version: "2.3.0"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: payment-service
        image: company.azurecr.io/payment-service:2.3.0
        ports:
        - name: http
          containerPort: 3000
        - name: metrics
          containerPort: 9090
        env:
        - name: NODE_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: payment-db-credentials
              key: url
        - name: STRIPE_API_KEY
          valueFrom:
            secretKeyRef:
              name: payment-stripe-secret
              key: api_key
        resources:
          requests:
            cpu: "1000m"
            memory: "2Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health/liveness
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/readiness
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
        startupProbe:
          httpGet:
            path: /health/startup
            port: 3000
          failureThreshold: 30
          periodSeconds: 10
        volumeMounts:
        - name: logs
          mountPath: /var/log/app
      volumes:
      - name: logs
        emptyDir: {}
```

**Generated HorizontalPodAutoscaler**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-service-hpa
  namespace: payments
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 6
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

**Deployment Output**:
```typescript
const output: DeploymentOrchestratorOutput = {
  deployment: {
    id: 'deploy-payment-2.3.0-canary-20251212-143022',
    status: 'completed',
    strategy: 'canary',
    startTime: '2025-12-12T14:30:22Z',
    endTime: '2025-12-12T15:30:45Z',
    duration: 3623
  },

  deployment_steps: [
    {
      step: 1,
      name: 'Build Docker image',
      status: 'completed',
      command: 'docker build -f Dockerfile.production -t company.azurecr.io/payment-service:2.3.0 .',
      output: 'Successfully built image with tag 2.3.0',
      duration: 245,
      timestamp: '2025-12-12T14:30:22Z'
    },
    {
      step: 2,
      name: 'Push image to registry',
      status: 'completed',
      command: 'docker push company.azurecr.io/payment-service:2.3.0',
      output: 'Image pushed successfully (compressed size: 287MB)',
      duration: 58,
      timestamp: '2025-12-12T14:34:27Z'
    },
    {
      step: 3,
      name: 'Deploy canary (10% traffic)',
      status: 'completed',
      command: 'kubectl apply -f canary-10percent.yaml',
      output: 'Canary deployment created with 1 replica (10% traffic)',
      duration: 12,
      timestamp: '2025-12-12T14:35:25Z'
    },
    {
      step: 4,
      name: 'Monitor canary metrics (10%)',
      status: 'completed',
      output: 'Error rate: 0.3%, Latency P95: 145ms, Success rate: 99.9% ✓',
      duration: 900,
      timestamp: '2025-12-12T14:35:37Z'
    },
    // ... additional steps through 100% promotion
  ],

  canary_progress: {
    currentStep: 4,
    totalSteps: 4,
    currentTrafficPercentage: 100,
    metrics: {
      errorRate: 0.4,
      latency: 156,
      requestsPerSecond: 2340,
      successRate: 99.8
    },
    decision: 'promote'
  },

  resources: {
    endpoints: [
      'https://payment.company.com/api/payment',
      'http://payment-service.payments.svc.cluster.local'
    ],
    ingressURL: 'https://payment.company.com',
    dashboardURL: 'https://grafana.company.com/d/payment-service',
    logsURL: 'https://kibana.company.com/app/discover#/?...'
  },

  health: {
    overallStatus: 'healthy',
    readyReplicas: 6,
    totalReplicas: 6,
    conditions: [
      {
        type: 'Available',
        status: true,
        message: 'Deployment has minimum availability'
      },
      {
        type: 'Progressing',
        status: true,
        reason: 'NewReplicaSetAvailable',
        message: 'ReplicaSet has successfully progressed'
      }
    ]
  },

  rollback_plan: {
    previousVersion: '2.2.5',
    rollbackCommand: 'kubectl rollout undo deployment/payment-service -n payments',
    estimatedTime: 120,
    impactAssessment: 'Rolling restart of all pods, zero-downtime expected'
  },

  recommendations: [
    '✅ Canary deployment completed successfully with all metrics within thresholds',
    '✅ All 6 replicas are healthy and serving traffic',
    '⚠️ Consider increasing HPA maxReplicas to 30 during peak holiday shopping season',
    '💡 Monitor memory usage closely - currently at 78% of limit',
    '💡 Consider implementing request queuing for better traffic spike handling'
  ],

  costs: {
    estimatedMonthlyCost: 432.50,
    currency: 'USD',
    breakdown: {
      compute: 360.00,
      loadBalancer: 45.00,
      storage: 12.50,
      egress: 15.00
    }
  }
};
```

**Metrics**: 60-minute deployment, zero downtime, auto-promoted through all canary stages

---

### Example 2: AWS Lambda Blue-Green Deployment

**Scenario**: Deploy a Python serverless analytics API to AWS Lambda with blue-green strategy and automated testing.

**Input**:
```typescript
const lambdaDeployment: DeploymentOrchestratorInput = {
  application: {
    name: 'analytics-api',
    version: '1.5.2',
    type: 'serverless',
    repository: {
      url: 'https://github.com/company/analytics-api',
      branch: 'main'
    }
  },

  target: {
    platform: 'aws-lambda',
    environment: 'production',
    region: 'us-east-1'
  },

  strategy: {
    type: 'blue-green',
    blueGreen: {
      routeTraffic: 'automatic',
      testWindow: 10,
      autoRollbackOnFailure: true
    }
  },

  resources: {
    container: {
      cpu: '2048',
      memory: '4096Mi'
    }
  },

  configuration: {
    environmentVariables: {
      PYTHON_ENV: 'production',
      LOG_LEVEL: 'INFO',
      DYNAMODB_TABLE: 'analytics-data-prod',
      S3_BUCKET: 'analytics-reports-prod'
    },
    secrets: {
      DATABASE_URL: 'arn:aws:secretsmanager:us-east-1:123456789:secret:analytics-db',
      API_KEY: 'arn:aws:secretsmanager:us-east-1:123456789:secret:analytics-api-key'
    }
  },

  monitoring: {
    logging: {
      driver: 'cloudwatch',
      options: {
        retention: '30'
      }
    },
    metrics: {
      customMetrics: [
        'analytics_queries_processed',
        'analytics_query_duration',
        'analytics_cache_hit_rate'
      ]
    }
  },

  rollback: {
    enabled: true,
    autoRollbackTriggers: {
      errorRate: 2.0,
      healthCheckFailures: 3
    }
  }
};
```

**Generated Lambda Configuration**:
```json
{
  "FunctionName": "analytics-api",
  "Runtime": "python3.11",
  "Role": "arn:aws:iam::123456789:role/lambda-analytics-execution-role",
  "Handler": "app.lambda_handler",
  "Code": {
    "S3Bucket": "company-lambda-deployments",
    "S3Key": "analytics-api/1.5.2/function.zip"
  },
  "Environment": {
    "Variables": {
      "PYTHON_ENV": "production",
      "LOG_LEVEL": "INFO",
      "DYNAMODB_TABLE": "analytics-data-prod",
      "S3_BUCKET": "analytics-reports-prod"
    }
  },
  "MemorySize": 4096,
  "Timeout": 300,
  "ReservedConcurrentExecutions": 100,
  "TracingConfig": {
    "Mode": "Active"
  }
}
```

**Output**: 15-minute deployment, instant traffic switch, 5-second rollback capability, $245.80/month cost

---

### Example 3: React SPA Blue-Green Deployment to Cloud Run with CDN

**Scenario**: Deploy a React customer portal to GCP Cloud Run with manual approval and CDN cache invalidation.

**Input**:
```typescript
const staticDeployment: DeploymentOrchestratorInput = {
  application: {
    name: 'customer-portal',
    version: '3.1.0',
    type: 'static',
    repository: {
      url: 'https://github.com/company/customer-portal',
      branch: 'release/v3.1.0'
    }
  },

  target: {
    platform: 'gcp-cloud-run',
    environment: 'production',
    region: 'us-central1'
  },

  strategy: {
    type: 'blue-green',
    blueGreen: {
      routeTraffic: 'manual',
      testWindow: 30,
      autoRollbackOnFailure: false
    }
  },

  configuration: {
    environmentVariables: {
      REACT_APP_API_URL: 'https://api.company.com',
      REACT_APP_ENVIRONMENT: 'production',
      REACT_APP_VERSION: '3.1.0'
    }
  },

  networking: {
    ingress: {
      enabled: true,
      host: 'portal.company.com',
      tls: true,
      annotations: {
        'cloud.google.com/cdn': 'true',
        'cloud.google.com/cache-control': 'public, max-age=3600'
      }
    }
  },

  monitoring: {
    metrics: {
      customMetrics: [
        'page_load_time',
        'first_contentful_paint',
        'time_to_interactive',
        'cumulative_layout_shift'
      ]
    }
  }
};
```

**Generated Dockerfile**:
```dockerfile
# Multi-stage Dockerfile for React SPA
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Security headers
RUN echo 'add_header X-Frame-Options "SAMEORIGIN" always;' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-Content-Type-Options "nosniff" always;' >> /etc/nginx/conf.d/security.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Output**: 45-minute deployment with manual approval, Lighthouse 98/100 performance, $185.40/month with CDN

---

## Best Practices

### Deployment Strategy Selection

**DO**:
- ✅ Use **rolling updates** for stateless apps with minimal risk (lowest resource cost)
- ✅ Use **blue-green** for critical apps needing instant rollback (requires 2x resources temporarily)
- ✅ Use **canary** for high-risk changes with gradual validation (progressive confidence)
- ✅ Use **A/B testing** for feature flags and business metric validation
- ✅ Use **recreate** only for apps that can't run multiple versions simultaneously

**DON'T**:
- ❌ Use rolling updates for stateful applications without careful planning
- ❌ Skip blue-green for production databases (use it for read replicas first)
- ❌ Set canary steps too aggressively (10% → 100% is risky, use 10 → 25 → 50 → 100)
- ❌ Ignore resource costs of blue-green (2x resources during deployment)

### Health Check Design

**DO**:
- ✅ **Liveness probe**: Check if process is alive (restart container if fails)
  ```yaml
  livenessProbe:
    httpGet:
      path: /health/liveness
      port: 3000
    initialDelaySeconds: 30  # Give app time to start
    periodSeconds: 10
    failureThreshold: 3      # Restart after 3 failures
  ```

- ✅ **Readiness probe**: Check if ready for traffic (remove from LB if fails)
  ```yaml
  readinessProbe:
    httpGet:
      path: /health/readiness
      port: 3000
    initialDelaySeconds: 10
    periodSeconds: 5
    failureThreshold: 2
  ```

- ✅ **Startup probe**: Check startup completion (for slow-starting apps)
  ```yaml
  startupProbe:
    httpGet:
      path: /health/startup
      port: 3000
    failureThreshold: 30     # 30 attempts * 10s = 5 minutes max startup
    periodSeconds: 10
  ```

**DON'T**:
- ❌ Use same endpoint for liveness and readiness
- ❌ Set initialDelaySeconds too low (causes restart loops)
- ❌ Make health checks call external dependencies (should be fast, local checks)
- ❌ Skip startup probes for apps with >30s startup time

### Auto-Rollback Configuration

**DO**:
- ✅ Set realistic error rate thresholds (5% for non-critical, 1% for payment systems)
- ✅ Monitor P95/P99 latency, not just average
- ✅ Use business metrics (order success rate, payment completion)
- ✅ Enable CrashLoopBackOff detection
- ✅ Set health check failure thresholds (3-5 consecutive failures)

**Example Configuration**:
```typescript
rollback: {
  enabled: true,
  autoRollbackTriggers: {
    errorRate: 5.0,              // 5% error rate
    crashLoopBackoff: true,      // Pod restart loop
    healthCheckFailures: 5,      // 5 consecutive failures
    customMetrics: {
      'payment_success_rate': 95.0,  // < 95% triggers rollback
      'checkout_latency_p95': 2000   // > 2s P95 latency
    }
  }
}
```

**DON'T**:
- ❌ Set thresholds too sensitive (causes false rollbacks)
- ❌ Ignore latency spikes (can indicate cascading failures)
- ❌ Disable rollback in production (always have escape hatch)

### Zero-Downtime Deployment

**DO**:
- ✅ Set `maxUnavailable: 0` for zero-downtime rolling updates
- ✅ Configure `preStop` hook for graceful shutdown (drain connections)
  ```yaml
  lifecycle:
    preStop:
      exec:
        command: ["/bin/sh", "-c", "sleep 15"]  # Wait for LB to update
  ```

- ✅ Set adequate `terminationGracePeriodSeconds` (default 30s, use 60s for long requests)
- ✅ Ensure readiness probe passes before receiving traffic
- ✅ Use connection draining on load balancer (30-60s)

**DON'T**:
- ❌ Kill pods instantly (use preStop hooks)
- ❌ Set terminationGracePeriodSeconds too low
- ❌ Skip readiness probes (traffic sent to non-ready pods)

### Multi-Environment Strategy

**DO**:
- ✅ Use namespaces (Kubernetes) or resource tags (cloud) for isolation
- ✅ Different configs per environment (use separate ConfigMaps/Secrets)
- ✅ Require manual approval for production deployments
- ✅ Automate smoke tests in each environment
- ✅ Progressive rollout: dev → staging → prod

**Example Structure**:
```
environments/
├── dev/
│   ├── deployment.yaml
│   ├── config.yaml (3 replicas, t3.small)
│   └── auto-deploy: true
├── staging/
│   ├── deployment.yaml
│   ├── config.yaml (5 replicas, t3.medium)
│   └── auto-deploy: true, smoke-tests: required
└── production/
    ├── deployment.yaml
    ├── config.yaml (10 replicas, t3.large)
    └── manual-approval: required, canary: enabled
```

**DON'T**:
- ❌ Share secrets across environments
- ❌ Use production data in dev/staging
- ❌ Deploy directly to production without staging validation
- ❌ Skip environment-specific resource limits

### Resource Sizing

**DO**:
- ✅ Set both `requests` (guaranteed) and `limits` (maximum)
  ```yaml
  resources:
    requests:
      cpu: "500m"      # Guaranteed 0.5 CPU
      memory: "1Gi"    # Guaranteed 1GB RAM
    limits:
      cpu: "1000m"     # Max 1 CPU
      memory: "2Gi"    # Max 2GB RAM
  ```

- ✅ Use HPA with multiple metrics (CPU + memory + custom)
- ✅ Set conservative minimums, generous maximums
- ✅ Monitor actual usage and adjust

**DON'T**:
- ❌ Set requests == limits (prevents efficient bin packing)
- ❌ Omit limits (risk OOMKilled or CPU throttling)
- ❌ Use tiny requests (causes frequent scaling)
- ❌ Ignore memory leaks (monitor trends)

---

## Related Skills

- **24-infrastructure-coder**: Generate Terraform/IaC for infrastructure
- **25-cicd-pipeline-builder**: Integrate deployments into CI/CD pipelines
- **10-monitoring-dashboard**: Set up deployment monitoring and alerts
- **08-security-scanner**: Scan container images for vulnerabilities
- **32-risk-assessor**: Assess deployment risk and create rollback plans

---

## Changelog

### Version 2.0.0 (2025-12-12)
- Initial release with multi-cloud deployment support
- Canary, blue-green, rolling update strategies
- Kubernetes, AWS Lambda, GCP Cloud Run support
- Automated health checks and rollback
- Cost estimation and opt
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
interface DeploymentOrchestratorInput {
}
```

### 输出接口

```typescript
interface DeploymentOrchestratorOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

imization
