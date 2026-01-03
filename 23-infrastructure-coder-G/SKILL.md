---
name: 23-infrastructure-coder-G
description: Infrastructure code generator for IaC automation. Supports multiple tools (Terraform/CloudFormation/Pulumi/Ansible), modular architecture (reusable modules), state management (remote state), security best practices (encryption/IAM/network isolation), cost optimization (right-sizing resources). Use for infrastructure as code, environment replication, disaster recovery.
---

# Infrastructure Coder

**Version**: 2.0.0
**Category**: DevOps
**Priority**: P1
**Last Updated**: 2025-12-12

---

## Description

Infrastructure Coder generates production-ready Infrastructure as Code (IaC) for multi-cloud environments. It supports Terraform (HCL), AWS CloudFormation (YAML/JSON), Pulumi (TypeScript/Python/Go/C#), and Ansible (YAML), enabling teams to define, version, and manage infrastructure declaratively. The skill includes module design, state management, security hardening, cost optimization, and migration from existing infrastructure.

### Core Capabilities

1. **Multi-Tool IaC Generation**
   - Terraform (HCL) with latest provider syntax
   - AWS CloudFormation (YAML/JSON templates)
   - Pulumi (TypeScript, Python, Go, C#/.NET)
   - Ansible (YAML playbooks and roles)
   - CDK for Terraform (CDKTF) with TypeScript/Python

2. **Multi-Cloud Resource Orchestration**
   - AWS: VPC, EC2, RDS, S3, Lambda, ECS, EKS
   - Azure: VNet, VM, AKS, CosmosDB, Storage
   - GCP: VPC, Compute Engine, GKE, Cloud SQL
   - Kubernetes: Namespaces, Deployments, Services
   - Cross-cloud networking and hybrid setups

3. **Modular Architecture**
   - Reusable modules with versioning
   - Parameter-driven configurations
   - Composition patterns for complex systems
   - Module registry integration (Terraform Registry, Pulumi Packages)
   - Dependency management and ordering

4. **State Management**
   - Remote state backends (S3, Azure Blob, GCS, Terraform Cloud)
   - State locking with DynamoDB, Consul, etcd
   - Workspace management for environments
   - State migration and import strategies
   - Secure state encryption

5. **Security Best Practices**
   - Least privilege IAM policies
   - Secrets management (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault)
   - Network isolation and security groups
   - Encryption at rest and in transit
   - Compliance scanning (Checkov, Terrascan, tfsec)

6. **Cost Optimization**
   - Resource tagging strategies
   - Budget alerts and cost allocation
   - Right-sizing recommendations
   - Spot/preemptible instance usage
   - Lifecycle policies for storage

---

## Instructions

### Activation Triggers

This skill activates when detecting:
- "create Terraform configuration"
- "generate CloudFormation template"
- "write Pulumi code"
- "infrastructure as code"
- "IaC setup"
- "Terraform modules"
- "provision AWS/Azure/GCP resources"
- "import existing infrastructure"
- "Terraform state management"
- "multi-cloud deployment"

### Execution Flow

```mermaid
graph TD
    A[IaC Request] --> B{Tool Selection}

    B -->|Terraform| C[Terraform Flow]
    C --> C1[Generate Provider Config]
    C1 --> C2[Create Resource Definitions]
    C2 --> C3[Define Variables & Outputs]
    C3 --> C4[Configure Backend]
    C4 --> C5{Modular?}
    C5 -->|Yes| C6[Generate Modules]
    C5 -->|No| C7[Single File]
    C6 --> C8[Module Structure]

    B -->|CloudFormation| D[CFN Flow]
    D --> D1[Create Template]
    D1 --> D2[Define Parameters]
    D2 --> D3[Add Resources]
    D3 --> D4[Configure Outputs]
    D4 --> D5[Nested Stacks?]
    D5 -->|Yes| D6[Generate Child Stacks]

    B -->|Pulumi| E[Pulumi Flow]
    E --> E1{Language Choice}
    E1 -->|TypeScript| E2[Generate TS Code]
    E1 -->|Python| E3[Generate Python]
    E1 -->|Go| E4[Generate Go]
    E2 --> E5[Define Resources]
    E3 --> E5
    E4 --> E5
    E5 --> E6[Stack Configuration]

    B -->|Ansible| F[Ansible Flow]
    F --> F1[Create Playbook]
    F1 --> F2[Define Roles]
    F2 --> F3[Configure Inventory]
    F3 --> F4[Add Variables]

    C8 --> G[Security Scan]
    D6 --> G
    E6 --> G
    F4 --> G

    G --> H[Cost Estimation]
    H --> I[Generate Documentation]
    I --> J[Output Package]
```

---

## Input Schema

```typescript
/**
 * Input configuration for infrastructure code generation
 */
interface InfrastructureCoderInput {
  /**
   * IaC tool to use
   */
  tool: 'terraform' | 'cloudformation' | 'pulumi' | 'ansible' | 'cdktf';

  /**
   * Language/format (tool-dependent)
   */
  language?: 'hcl' | 'yaml' | 'json' | 'typescript' | 'python' | 'go' | 'csharp';

  /**
   * Cloud provider configuration
   */
  provider: {
    /**
     * Primary cloud provider
     */
    cloud: 'aws' | 'azure' | 'gcp' | 'kubernetes' | 'multi-cloud';

    /**
     * Cloud region
     * @example "us-east-1", "eastus", "us-central1"
     */
    region?: string;

    /**
     * Account/subscription ID
     */
    account?: string;

    /**
     * Profile name (for local auth)
     */
    profile?: string;
  };

  /**
   * Resources to provision
   */
  resources: Array<{
    /**
     * Resource type
     * @example "aws_instance", "azurerm_virtual_machine", "google_compute_instance"
     */
    type: string;

    /**
     * Resource name/identifier
     */
    name: string;

    /**
     * Resource properties
     */
    properties: Record<string, any>;

    /**
     * Number of instances to create
     * @default 1
     */
    count?: number;

    /**
     * Dependencies on other resources
     */
    dependencies?: string[];
  }>;

  /**
   * Networking configuration
   */
  networking?: {
    /**
     * VPC/VNet configuration
     */
    vpc?: {
      cidrBlock: string;
      enableDnsSupport?: boolean;
      enableDnsHostnames?: boolean;

      /**
       * Subnets configuration
       */
      subnets?: Array<{
        name: string;
        cidrBlock: string;
        availabilityZone?: string;
        public?: boolean;
      }>;
    };

    /**
     * Security groups/NSGs
     */
    securityGroups?: Array<{
      name: string;
      description: string;

      /**
       * Inbound rules
       */
      ingress?: Array<{
        fromPort: number;
        toPort: number;
        protocol: string;
        cidrBlocks?: string[];
        sourceSecurityGroupId?: string;
      }>;

      /**
       * Outbound rules
       */
      egress?: Array<{
        fromPort: number;
        toPort: number;
        protocol: string;
        cidrBlocks?: string[];
      }>;
    }>;
  };

  /**
   * Compute resources
   */
  compute?: {
    /**
     * VM/instance configuration
     */
    instances?: Array<{
      /**
       * Instance type
       * @example "t3.medium", "Standard_D2s_v3", "n1-standard-2"
       */
      type: string;

      /**
       * AMI ID (AWS)
       */
      ami?: string;

      /**
       * Image reference (Azure/GCP)
       */
      image?: string;

      /**
       * Startup script
       */
      userData?: string;

      /**
       * SSH key name
       */
      keyName?: string;

      /**
       * IAM role
       */
      iamRole?: string;

      /**
       * Resource tags
       */
      tags?: Record<string, string>;
    }>;

    /**
     * Auto-scaling configuration
     */
    autoscaling?: {
      minSize: number;
      maxSize: number;
      desiredCapacity: number;
      healthCheckType?: 'EC2' | 'ELB';
      healthCheckGracePeriod?: number;
      launchTemplate?: any;
    };
  };

  /**
   * Database configuration
   */
  database?: {
    /**
     * Database type
     */
    type: 'rds' | 'dynamodb' | 'cosmosdb' | 'cloud-sql' | 'aurora';

    /**
     * Database engine
     * @example "postgres", "mysql", "mongodb"
     */
    engine?: string;

    /**
     * Engine version
     * @example "14.7", "8.0"
     */
    version?: string;

    /**
     * Instance class
     * @example "db.t3.medium"
     */
    instanceClass?: string;

    /**
     * Allocated storage (GB)
     */
    allocatedStorage?: number;

    /**
     * Multi-AZ deployment
     * @default false
     */
    multiAZ?: boolean;

    /**
     * Backup retention period (days)
     * @default 7
     */
    backupRetention?: number;

    /**
     * Enable encryption at rest
     * @default true
     */
    encryptionEnabled?: boolean;
  };

  /**
   * Storage configuration
   */
  storage?: {
    /**
     * S3/Blob storage buckets
     */
    buckets?: Array<{
      name: string;
      versioning?: boolean;
      encryption?: boolean;

      /**
       * Lifecycle rules
       */
      lifecycleRules?: Array<{
        id: string;
        enabled: boolean;
        transitions?: Array<{
          days: number;
          storageClass: string;
        }>;
        expiration?: { days: number };
      }>;
    }>;
  };

  /**
   * Module configuration
   */
  modules?: {
    /**
     * Use modular structure
     * @default false
     */
    useModules: boolean;

    /**
     * External module sources
     */
    moduleSources?: Array<{
      name: string;
      source: string;
      version?: string;
      inputs?: Record<string, any>;
    }>;
  };

  /**
   * State backend configuration
   */
  backend?: {
    /**
     * Backend type
     */
    type: 's3' | 'azurerm' | 'gcs' | 'terraform-cloud' | 'local';

    /**
     * Bucket/container name
     */
    bucket?: string;

    /**
     * State file key/path
     */
    key?: string;

    /**
     * Region
     */
    region?: string;

    /**
     * DynamoDB table for locking (AWS)
     */
    dynamodbTable?: string;

    /**
     * Encryption enabled
     * @default true
     */
    encrypt?: boolean;
  };

  /**
   * Variables and outputs
   */
  variables?: Array<{
    name: string;
    type: string;
    description?: string;
    default?: any;
    sensitive?: boolean;
  }>;

  outputs?: Array<{
    name: string;
    description?: string;
    sensitive?: boolean;
  }>;

  /**
   * Generation options
   */
  options?: {
    /**
     * Generate modular structure
     * @default false
     */
    generateModules?: boolean;

    /**
     * Include documentation
     * @default true
     */
    includeDocumentation?: boolean;

    /**
     * Add cost allocation tags
     * @default true
     */
    addCostTags?: boolean;

    /**
     * Enable monitoring resources
     * @default false
     */
    enableMonitoring?: boolean;

    /**
     * Dry run (plan only)
     * @default false
     */
    dryRun?: boolean;
  };
}

/**
 * Output from infrastructure code generation
 */
interface InfrastructureCoderOutput {
  /**
   * Tool used
   */
  tool: string;

  /**
   * Language/format
   */
  language: string;

  /**
   * Generated files
   */
  files: {
    /**
     * Main IaC file
     */
    main: string;

    /**
     * Variables file
     */
    variables?: string;

    /**
     * Outputs file
     */
    outputs?: string;

    /**
     * Backend configuration
     */
    backend?: string;

    /**
     * Module files (key: module name, value: file content)
     */
    modules?: Record<string, string>;

    /**
     * README documentation
     */
    readme?: string;
  };

  /**
   * Recommended directory structure
   */
  directory_structure: string;

  /**
   * Commands to run
   */
  commands: {
    /**
     * Initialization command
     */
    init: string;

    /**
     * Plan/preview command
     */
    plan: string;

    /**
     * Apply command
     */
    apply: string;

    /**
     * Destroy command
     */
    destroy: string;

    /**
     * Validation command
     */
    validate?: string;
  };

  /**
   * Estimated resource counts
   */
  estimated_resources: Array<{
    type: string;
    count: number;
    region?: string;
  }>;

  /**
   * Cost estimation
   */
  cost_estimate?: {
    monthly: number;
    currency: string;
    breakdown: Array<{
      resource: string;
      cost: number;
    }>;
    assumptions: string[];
  };

  /**
   * Security review findings
   */
  security_review: {
    /**
     * Security score (0-100)
     */
    score: number;

    /**
     * Security issues found
     */
    issues: Array<{
      severity: 'critical' | 'high' | 'medium' | 'low';
      resource: string;
      issue: string;
      recommendation: string;
    }>;
  };

  /**
   * Best practices recommendations
   */
  best_practices: string[];

  /**
   * Migration notes (if importing existing infrastructure)
   */
  migration_notes?: string[];
}
```

---

## Usage Examples

### Example 1: Terraform AWS 3-Tier Architecture

**Scenario**: Generate a production-ready Terraform configuration for a 3-tier web application (web, application, database layers) with high availability.

**Input**:
```typescript
const terraformSetup: InfrastructureCoderInput = {
  tool: 'terraform',
  language: 'hcl',

  provider: {
    cloud: 'aws',
    region: 'us-east-1',
    profile: 'production'
  },

  networking: {
    vpc: {
      cidrBlock: '10.0.0.0/16',
      enableDnsSupport: true,
      enableDnsHostnames: true,
      subnets: [
        { name: 'public-1a', cidrBlock: '10.0.1.0/24', availabilityZone: 'us-east-1a', public: true },
        { name: 'public-1b', cidrBlock: '10.0.2.0/24', availabilityZone: 'us-east-1b', public: true },
        { name: 'private-1a', cidrBlock: '10.0.11.0/24', availabilityZone: 'us-east-1a', public: false },
        { name: 'private-1b', cidrBlock: '10.0.12.0/24', availabilityZone: 'us-east-1b', public: false },
        { name: 'database-1a', cidrBlock: '10.0.21.0/24', availabilityZone: 'us-east-1a', public: false },
        { name: 'database-1b', cidrBlock: '10.0.22.0/24', availabilityZone: 'us-east-1b', public: false }
      ]
    },
    securityGroups: [
      {
        name: 'web-sg',
        description: 'Security group for web servers',
        ingress: [
          { fromPort: 80, toPort: 80, protocol: 'tcp', cidrBlocks: ['0.0.0.0/0'] },
          { fromPort: 443, toPort: 443, protocol: 'tcp', cidrBlocks: ['0.0.0.0/0'] }
        ],
        egress: [
          { fromPort: 0, toPort: 0, protocol: '-1', cidrBlocks: ['0.0.0.0/0'] }
        ]
      },
      {
        name: 'app-sg',
        description: 'Security group for application servers',
        ingress: [
          { fromPort: 8080, toPort: 8080, protocol: 'tcp', sourceSecurityGroupId: 'web-sg' }
        ],
        egress: [
          { fromPort: 0, toPort: 0, protocol: '-1', cidrBlocks: ['0.0.0.0/0'] }
        ]
      },
      {
        name: 'db-sg',
        description: 'Security group for database',
        ingress: [
          { fromPort: 5432, toPort: 5432, protocol: 'tcp', sourceSecurityGroupId: 'app-sg' }
        ],
        egress: []
      }
    ]
  },

  compute: {
    instances: [
      {
        type: 't3.medium',
        ami: 'ami-0c55b159cbfafe1f0',
        keyName: 'production-key',
        iamRole: 'ec2-app-role',
        userData: `#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker`,
        tags: {
          Name: 'app-server',
          Environment: 'production',
          ManagedBy: 'terraform'
        }
      }
    ],
    autoscaling: {
      minSize: 2,
      maxSize: 6,
      desiredCapacity: 3,
      healthCheckType: 'ELB',
      healthCheckGracePeriod: 300
    }
  },

  database: {
    type: 'rds',
    engine: 'postgres',
    version: '14.7',
    instanceClass: 'db.t3.medium',
    allocatedStorage: 100,
    multiAZ: true,
    backupRetention: 7,
    encryptionEnabled: true
  },

  storage: {
    buckets: [
      {
        name: 'company-app-assets-prod',
        versioning: true,
        encryption: true,
        lifecycleRules: [
          {
            id: 'archive-old-logs',
            enabled: true,
            transitions: [
              { days: 30, storageClass: 'STANDARD_IA' },
              { days: 90, storageClass: 'GLACIER' }
            ],
            expiration: { days: 365 }
          }
        ]
      }
    ]
  },

  backend: {
    type: 's3',
    bucket: 'company-terraform-state',
    key: 'production/app/terraform.tfstate',
    region: 'us-east-1',
    dynamodbTable: 'terraform-state-lock',
    encrypt: true
  },

  variables: [
    { name: 'environment', type: 'string', description: 'Environment name', default: 'production' },
    { name: 'vpc_cidr', type: 'string', description: 'VPC CIDR block', default: '10.0.0.0/16' },
    { name: 'db_username', type: 'string', description: 'Database admin username', sensitive: true },
    { name: 'db_password', type: 'string', description: 'Database admin password', sensitive: true }
  ],

  outputs: [
    { name: 'vpc_id', description: 'VPC ID' },
    { name: 'alb_dns_name', description: 'Application Load Balancer DNS name' },
    { name: 'db_endpoint', description: 'RDS endpoint', sensitive: true }
  ],

  options: {
    generateModules: true,
    includeDocumentation: true,
    addCostTags: true,
    enableMonitoring: true
  }
};
```

**Generated main.tf**:
```hcl
# Terraform configuration for 3-tier architecture
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "production"

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "Company-App"
      CostCenter  = "Engineering"
    }
  }
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs              = data.aws_availability_zones.available.names
  private_subnets  = ["10.0.11.0/24", "10.0.12.0/24"]
  public_subnets   = ["10.0.1.0/24", "10.0.2.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  create_database_subnet_group = true

  tags = {
    Tier = "Networking"
  }
}

# Security Groups
resource "aws_security_group" "web" {
  name_prefix = "${var.environment}-web-sg"
  description = "Security group for web servers"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.environment}-web-sg"
    Tier = "Web"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "app" {
  name_prefix = "${var.environment}-app-sg"
  description = "Security group for application servers"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "Application port from web tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.environment}-app-sg"
    Tier = "Application"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "db" {
  name_prefix = "${var.environment}-db-sg"
  description = "Security group for database"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "PostgreSQL from app tier"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  tags = {
    Name = "${var.environment}-db-sg"
    Tier = "Database"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# RDS PostgreSQL Database
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.environment}-app-db"

  engine               = "postgres"
  engine_version       = "14.7"
  family               = "postgres14"
  major_engine_version = "14"
  instance_class       = var.db_instance_class

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true

  db_name  = "appdb"
  username = var.db_username
  password = var.db_password
  port     = 5432

  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.db.id]

  maintenance_window      = "Mon:00:00-Mon:03:00"
  backup_window           = "03:00-06:00"
  backup_retention_period = 7
  skip_final_snapshot     = false
  final_snapshot_identifier = "${var.environment}-app-db-final-snapshot"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  performance_insights_enabled          = true
  performance_insights_retention_period = 7

  tags = {
    Tier = "Database"
  }
}

# S3 Bucket for Application Assets
module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = "company-app-assets-${var.environment}"
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  versioning = {
    enabled = true
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule = [
    {
      id      = "archive-old-logs"
      enabled = true

      transition = [
        {
          days          = 30
          storage_class = "STANDARD_IA"
        },
        {
          days          = 90
          storage_class = "GLACIER"
        }
      ]

      expiration = {
        days = 365
      }
    }
  ]

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  tags = {
    Tier = "Storage"
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name_prefix = "${var.environment}-app-asg-"

  min_size         = var.asg_min_size
  max_size         = var.asg_max_size
  desired_capacity = var.asg_desired_capacity

  health_check_type         = "ELB"
  health_check_grace_period = 300
  wait_for_capacity_timeout = "10m"

  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = module.alb.target_group_arns

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  enabled_metrics = [
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupMaxSize",
    "GroupMinSize"
  ]

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

**Generated variables.tf**:
```hcl
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_username" {
  description = "Database admin username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database admin password"
  type        = string
  sensitive   = true
}

variable "asg_min_size" {
  description = "Minimum size of Auto Scaling Group"
  type        = number
  default     = 2
}

variable "asg_max_size" {
  description = "Maximum size of Auto Scaling Group"
  type        = number
  default     = 6
}

variable "asg_desired_capacity" {
  description = "Desired capacity of Auto Scaling Group"
  type        = number
  default     = 3
}

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
  default     = "production-key"
}
```

**Generated outputs.tf**:
```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "database_subnets" {
  description = "Database subnet IDs"
  value       = module.vpc.database_subnets
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = module.alb.lb_dns_name
}

output "alb_zone_id" {
  description = "Application Load Balancer zone ID"
  value       = module.alb.lb_zone_id
}

output "db_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "db_arn" {
  description = "RDS ARN"
  value       = module.rds.db_instance_arn
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = module.s3_bucket.s3_bucket_id
}

output "s3_bucket_arn" {
  description = "S3 bucket ARN"
  value       = module.s3_bucket.s3_bucket_arn
}

output "asg_name" {
  description = "Auto Scaling Group name"
  value       = aws_autoscaling_group.app.name
}
```

**Output Summary**:
```typescript
const output: InfrastructureCoderOutput = {
  tool: 'terraform',
  language: 'hcl',

  files: {
    main: '<generated main.tf above>',
    variables: '<generated variables.tf above>',
    outputs: '<generated outputs.tf above>',
    backend: '<backend config in main.tf>',
    readme: '# 3-Tier Application Infrastructure\n\n## Architecture\n...'
  },

  directory_structure: `
project/
├── main.tf           # Main infrastructure definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── terraform.tfvars  # Variable values (gitignored)
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── README.md
`,

  commands: {
    init: 'terraform init',
    plan: 'terraform plan -out=tfplan',
    apply: 'terraform apply tfplan',
    destroy: 'terraform destroy',
    validate: 'terraform validate && terraform fmt -check'
  },

  estimated_resources: [
    { type: 'aws_vpc', count: 1, region: 'us-east-1' },
    { type: 'aws_subnet', count: 6, region: 'us-east-1' },
    { type: 'aws_security_group', count: 3, region: 'us-east-1' },
    { type: 'aws_lb', count: 1, region: 'us-east-1' },
    { type: 'aws_autoscaling_group', count: 1, region: 'us-east-1' },
    { type: 'aws_db_instance', count: 1, region: 'us-east-1' },
    { type: 'aws_s3_bucket', count: 1, region: 'us-east-1' }
  ],

  cost_estimate: {
    monthly: 687.50,
    currency: 'USD',
    breakdown: [
      { resource: 'EC2 instances (3x t3.medium)', cost: 180.00 },
      { resource: 'RDS Multi-AZ (db.t3.medium)', cost: 285.00 },
      { resource: 'Application Load Balancer', cost: 22.50 },
      { resource: 'NAT Gateways (2x)', cost: 90.00 },
      { resource: 'S3 storage (100GB)', cost: 2.30 },
      { resource: 'Data transfer', cost: 50.00 },
      { resource: 'CloudWatch logs', cost: 10.00 },
      { resource: 'EBS volumes', cost: 47.70 }
    ],
    assumptions: [
      'Assumes 730 hours/month (24x7)',
      'Data transfer estimate: 500GB/month',
      'S3 storage: 100GB standard class',
      'RDS Multi-AZ pricing for us-east-1',
      'Excludes data transfer within same AZ'
    ]
  },

  security_review: {
    score: 92,
    issues: [
      {
        severity: 'medium',
        resource: 'aws_security_group.web',
        issue: 'Allows HTTP (port 80) from 0.0.0.0/0',
        recommendation: 'Consider using HTTPS only and redirecting HTTP to HTTPS at ALB level'
      },
      {
        severity: 'low',
        resource: 'aws_s3_bucket',
        issue: 'Bucket name includes environment suffix which may change',
        recommendation: 'Use prefix instead of suffix for better DNS compatibility'
      }
    ]
  },

  best_practices: [
    '✅ Remote state with S3 backend and DynamoDB locking',
    '✅ Multi-AZ deployment for high availability',
    '✅ Encryption at rest enabled for RDS and S3',
    '✅ Network isolation with private subnets for app and database',
    '✅ Auto Scaling configured with proper health checks',
    '✅ Resource tagging strategy implemented',
    '✅ Lifecycle policies for cost optimization',
    '⚠️ Consider enabling AWS Config for compliance monitoring',
    '⚠️ Add CloudWatch alarms for critical resources',
    '💡 Use AWS Secrets Manager for database credentials instead of variables'
  ]
};
```

---

## Best Practices

### Terraform State Management

**DO**:
- ✅ Always use remote state backend (S3, Azure Blob, GCS, Terraform Cloud)
- ✅ Enable state locking (DynamoDB for S3, native for others)
- ✅ Encrypt state files (`encrypt = true`)
- ✅ Use separate state files per environment
- ✅ Use workspaces for environment isolation
- ✅ Never commit `.tfstate` files to Git

**Example S3 Backend**:
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/app/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789:key/abc-123"
  }
}
```

**DON'T**:
- ❌ Use local state for production
- ❌ Share state files via Git
- ❌ Manually edit state files
- ❌ Use same state file for multiple environments

### Module Design

**DO**:
- ✅ Create reusable modules for common patterns
- ✅ Version modules using Git tags or Terraform Registry
- ✅ Document module inputs/outputs with descriptions
- ✅ Use semantic versioning for module releases
- ✅ Test modules independently

**Module Structure**:
```
modules/
└── networking/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── README.md
    └── examples/
        └── complete/
            ├── main.tf
            └── variables.tf
```

**Example Module Usage**:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # Pin to major version

  name = "${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = var.environment == "dev"

  tags = var.common_tags
}
```

**DON'T**:
- ❌ Copy-paste code instead of using modules
- ❌ Create overly complex mega-modules
- ❌ Use `latest` tag for module versions
- ❌ Hard-code values in modules

### Security Hardening

**DO**:
- ✅ Use IAM roles instead of access keys
- ✅ Enable encryption at rest and in transit
- ✅ Apply least privilege principle
- ✅ Use security groups with specific rules (not 0.0.0.0/0)
- ✅ Store secrets in AWS Secrets Manager/HashiCorp Vault
- ✅ Scan IaC with tools (Checkov, Terrascan, tfsec)

**Example IAM Policy (Least Privilege)**:
```hcl
data "aws_iam_policy_document" "app" {
  statement {
    sid    = "AllowS3ReadWrite"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "${module.s3_bucket.s3_bucket_arn}/*"
    ]
  }

  statement {
    sid    = "AllowSecretsManagerRead"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue"
    ]
    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:app/*"
    ]
  }
}
```

**DON'T**:
- ❌ Use `"*"` for IAM actions or resources
- ❌ Hard-code secrets in code
- ❌ Allow `0.0.0.0/0` for SSH (port 22)
- ❌ Disable encryption to "simplify" things
- ❌ Use root credentials

### Cost Optimization

**DO**:
- ✅ Tag all resources for cost allocation
  ```hcl
  default_tags {
    tags = {
      Environment = var.environment
      CostCenter  = "Engineering"
      Project     = "MyApp"
      ManagedBy   = "Terraform"
    }
  }
  ```

- ✅ Use lifecycle policies for S3 (transition to cheaper storage)
- ✅ Enable auto-scaling to match demand
- ✅ Use Spot instances for non-critical workloads
- ✅ Set up budget alerts
- ✅ Right-size instances based on actual usage

**DON'T**:
- ❌ Use large instances without monitoring usage
- ❌ Keep unused EBS snapshots
- ❌ Run dev/staging environments 24/7
- ❌ Ignore CloudWatch cost optimization recommendations

### Multi-Cloud Patterns

**DO**:
- ✅ Use provider aliases for multi-region/multi-account
  ```hcl
  provider "aws" {
    alias  = "us-east"
    region = "us-east-1"
  }

  provider "aws" {
    alias  = "eu-west"
    region = "eu-west-1"
  }

  module "vpc_us" {
    source = "./modules/vpc"
    providers = {
      aws = aws.us-east
    }
  }
  ```

- ✅ Abstract cloud-specific details in modules
- ✅ Use consistent naming conventions across clouds
- ✅ Document cloud-specific differences

**DON'T**:
- ❌ Mix resources from different clouds in same module without clear separation
- ❌ Assume features are identical across clouds
- ❌ Use cloud-specific names (prefer generic)

### Testing IaC

**DO**:
- ✅ Run `terraform validate` before apply
- ✅ Use `terraform plan` to preview changes
- ✅ Test in dev/staging before production
- ✅ Use Terratest or Kitchen-Terraform for automated tests
- ✅ Implement policy as code (Sentinel, OPA)

**Example Test Script**:
```bash
#!/bin/bash
set -e

echo "Validating Terraform configuration..."
terraform validate

echo "Formatting check..."
terraform fmt -check -recursive

echo "Security scan with Checkov..."
checkov -d .

echo "Generating plan..."
terraform plan -out=tfplan

echo "Cost estimation with Infracost..."
infracost breakdown --path tfplan

echo "All checks passed! ✅"
```

**DON'T**:
- ❌ Apply changes without reviewing plan
- ❌ Skip validation in CI/CD
- ❌ Test only in production
- ❌ Ignore security scan findings

---

## Related Skills

- **23-deployment-orchestrator**: Deploy infrastructure after provisioning
- **25-cicd-pipeline-builder**: Integrate IaC into CI/CD pipelines
- **08-security-scanner**: Security scanning for IaC code
- **10-monitoring-dashboard**: Monitor provisioned infrastructure
- **32-risk-assessor**: Assess risk of infrastructure changes

---

## Changelog

### Version 2.0.0 (2025-12-12)
- Initial release with multi-tool IaC generation
- Terraform, CloudFormation, Pulumi, Ansible support
- Multi-cloud resource orchestration (AWS, Azure, GCP)
- Automated security scanning and cost estimation
- Module generation and state m
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
interface InfrastructureCoderInput {
}
```

### 输出接口

```typescript
interface InfrastructureCoderOutput extends BaseOutput {
  success: boolean;          // 来自BaseOutput
  error?: ErrorInfo;         // 来自BaseOutput
  metadata?: Metadata;       // 来自BaseOutput
  warnings?: Warning[];      // 来自BaseOutput

  // ... 其他业务字段
}
```

---

anagement
