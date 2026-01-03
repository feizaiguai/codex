# CI/CD Pipeline Builder Skill - CI/CD管道构建器

**版本**: 2.0.0
**类型**: DevOps
**质量等级**: A+

## 📋 功能概述

自动化流水线生成,支持GitHub Actions/GitLab CI/Jenkins/CircleCI。

### 核心能力

1. **多平台支持** - GitHub Actions/GitLab CI/Jenkins/Azure DevOps/CircleCI
2. **完整工作流** - 构建→测试→安全扫描→部署全流程自动化
3. **矩阵构建** - 多环境/多版本/多平台并行测试
4. **安全集成** - SAST/DAST/SCA/Container扫描全覆盖
5. **部署策略** - 多环境部署/审批流程/自动回滚

## 🚀 使用方法

### Slash Command
```bash
/build-pipeline [平台] [语言]
```

### 自然语言调用
```
创建GitHub Actions流水线
配置Jenkins多阶段Pipeline
生成GitLab CI配置
```

## 📖 使用示例

### 示例:Node.js应用完整CI/CD
**输入**:
```
/build-pipeline github-actions nodejs --test --security --deploy
```

**输出**:
- ✅ 生成文件: `.github/workflows/ci-cd.yml`
- ✅ 流水线阶段:
  1. **代码质量** (2分钟)
     - ESLint检查
     - Prettier格式化
  2. **测试** (5分钟)
     - 单元测试 (Jest)
     - 集成测试
     - E2E测试 (Cypress)
     - 覆盖率报告: 92%
  3. **安全扫描** (3分钟)
     - npm audit (依赖漏洞)
     - SAST扫描 (Snyk)
     - Docker镜像扫描 (Trivy)
  4. **构建** (4分钟)
     - Docker多阶段构建
     - 镜像大小: 145MB → 58MB (优化60%)
  5. **部署** (6分钟)
     - 部署到Staging (自动)
     - 部署到Production (需审批)
- 📊 总耗时: ~20分钟
- ✅ 质量门控: 全部通过

## 🔄 GitHub Actions完整示例

### Node.js应用CI/CD
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18.x'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 代码质量检查
  lint:
    name: Code Quality
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

      - name: Run ESLint
        run: npm run lint

      - name: Check formatting
        run: npm run format:check

  # 测试套件
  test:
    name: Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]

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
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests

  # E2E测试
  e2e:
    name: E2E Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb

      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: cypress-screenshots
          path: cypress/screenshots

  # 安全扫描
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=moderate

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # 构建Docker镜像
  build:
    name: Build and Push
    runs-on: ubuntu-latest
    needs: [lint, test, e2e, security]
    if: github.event_name == 'push'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # 部署到Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=staging

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/myapp \
            --namespace=staging \
            --timeout=5m

      - name: Run smoke tests
        run: |
          curl -f https://staging.example.com/health || exit 1

  # 部署到Production (需审批)
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --namespace=production

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/myapp \
            --namespace=production \
            --timeout=10m

      - name: Verify deployment
        run: |
          curl -f https://example.com/health || exit 1

      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment completed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🎯 矩阵构建

### 多版本测试
```yaml
# 测试多个Node.js版本
strategy:
  matrix:
    node-version: [16.x, 18.x, 20.x]
    os: [ubuntu-latest, macos-latest, windows-latest]

# 生成9个并行任务:
# - Node 16 on Ubuntu
# - Node 16 on macOS
# - Node 16 on Windows
# - Node 18 on Ubuntu
# ... (共9个组合)
```

### 多环境部署
```yaml
strategy:
  matrix:
    environment: [dev, staging, production]
    region: [us-east-1, eu-west-1, ap-southeast-1]

# 并行部署到9个环境-区域组合
```

## 🔒 安全扫描集成

### 1. SAST (静态应用安全测试)
```yaml
- name: Run CodeQL analysis
  uses: github/codeql-action/analyze@v2
  with:
    languages: javascript

- name: Run SonarQube scan
  uses: sonarsource/sonarcloud-github-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 2. Dependency Scanning (依赖漏洞)
```yaml
- name: npm audit
  run: npm audit --audit-level=moderate

- name: Snyk dependency scan
  uses: snyk/actions/node@master
  with:
    args: --severity-threshold=high
```

### 3. Container Scanning (容器镜像)
```yaml
- name: Trivy container scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    format: 'table'
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

### 4. DAST (动态应用安全测试)
```yaml
- name: OWASP ZAP scan
  uses: zaproxy/action-baseline@v0.7.0
  with:
    target: 'https://staging.example.com'
    rules_file_name: '.zap/rules.tsv'
```

## 📊 性能优化

### 缓存策略
```yaml
# 依赖缓存
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

# Docker层缓存
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 并行执行
```yaml
# 所有测试并行运行
jobs:
  unit-test:
    runs-on: ubuntu-latest
    # 不依赖其他job

  integration-test:
    runs-on: ubuntu-latest
    # 不依赖其他job

  e2e-test:
    runs-on: ubuntu-latest
    # 不依赖其他job

  # 构建等待所有测试完成
  build:
    needs: [unit-test, integration-test, e2e-test]
```

## 📝 GitLab CI示例

### 完整.gitlab-ci.yml
```yaml
stages:
  - lint
  - test
  - security
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

# 代码质量
lint:
  stage: lint
  image: node:18
  script:
    - npm ci
    - npm run lint
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

# 单元测试
test:unit:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Statements\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# 安全扫描
security:
  stage: security
  image: node:18
  script:
    - npm audit --audit-level=moderate
    - npm install -g snyk
    - snyk test --severity-threshold=high
  allow_failure: true

# Docker构建
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - develop

# 部署到Staging
deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n staging
    - kubectl rollout status deployment/myapp -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# 部署到Production (手动触发)
deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/myapp -n production
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

## 🛠️ 最佳实践

1. **快速反馈**: 最常用的检查放前面
2. **并行优先**: 独立任务并行执行
3. **缓存依赖**: 减少下载时间
4. **质量门控**: 测试覆盖率>80%,安全扫描通过
5. **环境隔离**: dev/staging/prod独立配置

## 🔗 与其他 Skills 配合

- `test-automation`: 生成测试代码
- `security-audit`: 深度安全扫描
- `deployment-orchestrator`: 自动化部署

---

**状态**: ✅ 生产就绪 | **质量等级**: A+
