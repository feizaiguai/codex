# Infrastructure Coder Skill - 基础设施代码生成器

**版本**: 2.0.0
**类型**: DevOps
**质量等级**: A+

## 📋 功能概述

自动生成基础设施即代码(IaC),支持Terraform/CloudFormation/Pulumi/Ansible。

### 核心能力

1. **多工具支持** - Terraform/CloudFormation/Pulumi/Ansible全覆盖
2. **模块化架构** - 可复用模块设计,参数化配置
3. **状态管理** - 远程状态存储,状态锁定,workspace管理
4. **安全最佳实践** - 最小权限IAM,加密,网络隔离,密钥管理
5. **成本优化** - 资源标签,预算告警,右适配,Spot实例

## 🚀 使用方法

### Slash Command
```bash
/infra-code --tool=[terraform|cloudformation|pulumi] --cloud=[aws|azure|gcp]
```

### 自然语言调用
```
生成Terraform配置创建AWS VPC
用CloudFormation部署EKS集群
创建Pulumi代码管理Azure资源
```

## 📖 使用示例

### 示例:Terraform创建AWS三层架构
**输入**:
```
/infra-code --tool=terraform --cloud=aws --vpc --rds --eks
```

**输出**:
- ✅ 项目结构生成:
  ```
  terraform/
  ├── main.tf           # 主配置
  ├── variables.tf      # 变量定义
  ├── outputs.tf        # 输出值
  ├── backend.tf        # 状态后端
  ├── modules/
  │   ├── vpc/          # VPC模块
  │   ├── rds/          # 数据库模块
  │   └── eks/          # K8s集群模块
  └── environments/
      ├── dev.tfvars
      ├── staging.tfvars
      └── prod.tfvars
  ```
- ✅ 资源清单:
  - VPC + 6个子网 (3公有+3私有)
  - NAT网关 + 互联网网关
  - RDS PostgreSQL (Multi-AZ)
  - EKS集群 (3个节点组)
- ✅ 安全配置:
  - 最小权限IAM角色
  - 加密启用 (RDS/EBS)
  - 安全组最小化
- ✅ 成本优化:
  - Spot实例节点组
  - 资源标签完整
  - 预估月成本: $450

## 🏗️ Terraform代码示例

### VPC模块
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-vpc"
    }
  )
}

# 公有子网
resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}

# 私有子网
resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-private-${count.index + 1}"
      Type = "private"
    }
  )
}

# NAT网关 (每个AZ一个)
resource "aws_eip" "nat" {
  count  = length(var.availability_zones)
  domain = "vpc"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-nat-eip-${count.index + 1}"
    }
  )
}

resource "aws_nat_gateway" "main" {
  count = length(var.availability_zones)

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-nat-${count.index + 1}"
    }
  )
}
```

### 状态后端配置
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/infrastructure.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # 防止误删状态文件
    workspace_key_prefix = "workspaces"
  }
}
```

### 安全配置
```hcl
# 最小权限IAM策略
resource "aws_iam_role" "eks_cluster" {
  name = "${var.project_name}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

# 密钥管理
resource "aws_kms_key" "main" {
  description             = "${var.project_name} encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = var.tags
}

# RDS加密
resource "aws_db_instance" "main" {
  allocated_storage    = 100
  storage_encrypted    = true
  kms_key_id          = aws_kms_key.main.arn
  engine              = "postgres"
  engine_version      = "15.3"
  instance_class      = "db.r6g.large"
  db_name             = var.db_name
  username            = var.db_username
  password            = random_password.db_password.result
  multi_az            = true
  skip_final_snapshot = false

  # 自动备份
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  tags = var.tags
}
```

## ☁️ CloudFormation示例

### EKS集群模板
```yaml
# eks-cluster.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'EKS Cluster with Node Groups'

Parameters:
  ClusterName:
    Type: String
    Description: Name of the EKS cluster
    Default: my-cluster

  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID for the cluster

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs for the cluster

  NodeInstanceType:
    Type: String
    Description: EC2 instance type for nodes
    Default: t3.medium
    AllowedValues:
      - t3.small
      - t3.medium
      - t3.large

Resources:
  # EKS集群角色
  EKSClusterRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

  # EKS集群
  EKSCluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: !Ref ClusterName
      Version: '1.28'
      RoleArn: !GetAtt EKSClusterRole.Arn
      ResourcesVpcConfig:
        SubnetIds: !Ref SubnetIds
        EndpointPublicAccess: true
        EndpointPrivateAccess: true
      Logging:
        ClusterLogging:
          EnabledTypes:
            - Type: api
            - Type: audit
            - Type: authenticator

  # 节点组角色
  NodeGroupRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy

  # 节点组
  NodeGroup:
    Type: AWS::EKS::Nodegroup
    DependsOn: EKSCluster
    Properties:
      ClusterName: !Ref ClusterName
      NodegroupName: !Sub '${ClusterName}-nodegroup'
      NodeRole: !GetAtt NodeGroupRole.Arn
      Subnets: !Ref SubnetIds
      ScalingConfig:
        MinSize: 2
        MaxSize: 10
        DesiredSize: 3
      InstanceTypes:
        - !Ref NodeInstanceType
      DiskSize: 100
      Labels:
        role: worker
      Tags:
        Environment: production
        ManagedBy: CloudFormation

Outputs:
  ClusterName:
    Description: EKS Cluster Name
    Value: !Ref EKSCluster
    Export:
      Name: !Sub '${AWS::StackName}-ClusterName'

  ClusterEndpoint:
    Description: EKS Cluster API Endpoint
    Value: !GetAtt EKSCluster.Endpoint
```

## 💎 Pulumi示例 (TypeScript)

### 完整AWS基础设施
```typescript
// index.ts
import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';

// 配置
const config = new pulumi.Config();
const projectName = pulumi.getProject();
const stackName = pulumi.getStack();

// 标签
const tags = {
  Project: projectName,
  Environment: stackName,
  ManagedBy: 'Pulumi'
};

// VPC
const vpc = new aws.ec2.Vpc('main-vpc', {
  cidrBlock: '10.0.0.0/16',
  enableDnsHostnames: true,
  enableDnsSupport: true,
  tags: { ...tags, Name: `${projectName}-vpc` }
});

// 子网
const azs = aws.getAvailabilityZones({ state: 'available' });
const publicSubnets = azs.then(azs =>
  azs.names.slice(0, 3).map((az, i) =>
    new aws.ec2.Subnet(`public-subnet-${i}`, {
      vpcId: vpc.id,
      cidrBlock: `10.0.${i}.0/24`,
      availabilityZone: az,
      mapPublicIpOnLaunch: true,
      tags: { ...tags, Name: `public-${i + 1}`, Type: 'public' }
    })
  )
);

// RDS数据库
const dbSubnetGroup = new aws.rds.SubnetGroup('db-subnet-group', {
  subnetIds: publicSubnets.then(s => s.map(subnet => subnet.id)),
  tags
});

const dbPassword = new pulumi.Output(config.requireSecret('dbPassword'));

const rds = new aws.rds.Instance('postgres-db', {
  allocatedStorage: 100,
  engine: 'postgres',
  engineVersion: '15.3',
  instanceClass: 'db.t3.medium',
  dbName: 'myapp',
  username: 'admin',
  password: dbPassword,
  dbSubnetGroupName: dbSubnetGroup.name,
  multiAz: true,
  storageEncrypted: true,
  backupRetentionPeriod: 7,
  skipFinalSnapshot: false,
  finalSnapshotIdentifier: `${projectName}-final-snapshot`,
  tags
});

// 导出
export const vpcId = vpc.id;
export const rdsEndpoint = rds.endpoint;
export const rdsPort = rds.port;
```

## 📊 成本优化

### 资源标签策略
```hcl
# 统一标签
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
    BackupSchedule = "daily"
  }
}

# 应用到所有资源
resource "aws_instance" "app" {
  # ...
  tags = merge(
    local.common_tags,
    {
      Name = "app-server"
      Component = "application"
    }
  )
}
```

### 成本告警
```hcl
# AWS预算告警
resource "aws_budgets_budget" "monthly" {
  name              = "${var.project_name}-monthly-budget"
  budget_type       = "COST"
  limit_amount      = "1000"
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = ["ops-team@company.com"]
  }
}
```

## 🛠️ 最佳实践

1. **远程状态**: 使用S3+DynamoDB存储状态
2. **模块化**: 创建可复用模块
3. **环境隔离**: dev/staging/prod独立workspace
4. **密钥管理**: 使用Vault或云平台密钥服务
5. **代码审查**: PR前运行`terraform plan`

## 🔗 与其他 Skills 配合

- `deployment-orchestrator`: 部署IaC创建的基础设施
- `cicd-pipeline-builder`: CI/CD中集成IaC
- `security-audit`: 扫描IaC安全问题

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
