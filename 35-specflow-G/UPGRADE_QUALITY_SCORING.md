# 35-specflow 质量评分算法升级方案

**版本**: V5.0 Quality-First
**设计者**: Claude + Gemini 联合设计
**日期**: 2025-12-21
**目标**: 从"形式主义"转向"实质主义"，真实反映文档质量

---

## 问题诊断

### 当前问题（V4.0）
- ❌ 评分算法只看结构（数量、格式），不看内容质量
- ❌ 给模板化空壳文档打B级（85分），严重误导
- ❌ 实际质量F级（32.5分）被掩盖

### 问题案例
```
用户故事：作为产品经理，我想完成注册/登录的操作，以便达成业务目标
验收标准：（空）
BDD场景：Given 系统就绪 When 提交请求 Then 完成操作
项目信息：待明确、待定义、待识别

当前评分：B级（85分）❌
实际质量：F级（32.5分）✅
```

---

## 升级方案（Gemini设计）

### 1. 新一代质量评分算法

**核心思想**：基准分 + 惩罚扣分 + 关键一票否决

#### 维度与权重（总分100）

| 维度 | 权重 | 说明 | V4权重 |
|------|------|------|---------|
| **信息实质度 (Substance)** | 35% | 非占位符的有效信息占比 | 0% ❌ |
| **规格具体性 (Concreteness)** | 25% | 用户故事和BDD场景的明确程度 | 0% ❌ |
| **验证覆盖度 (Verifiability)** | 20% | 验收标准的可测试性 | 5% |
| **结构完整性 (Completeness)** | 10% | 元数据和文档结构 | 85% ⚠️ |
| **逻辑一致性 (Consistency)** | 10% | 术语统一性和连贯性 | 10% |

**变化**：
- ✅ 增加内容质量维度（60%权重）
- ⚠️ 大幅降低结构权重（85% → 10%）
- ✅ 增强验证覆盖度（5% → 20%）

#### 熔断机制（Circuit Breaker）

**一级熔断**：
- 触发条件：核心字段为空 OR 占位符占比 > 50%
- 后果：**总分上限锁定40分（F级）**

**二级熔断**：
- 触发条件：用户故事完全命中默认模板
- 后果：**该单项得分为0**

---

### 2. 内容质量检测规则

#### A. 占位符与垃圾词检测

**黑名单词库**：
```python
BLOCKLIST = [
    "待定", "待明确", "待定义", "待识别",
    "TBD", "TODO", "XX", "占位符",
    "填写这里", "填写", "示例", "模板",
    "Generic", "默认", "系统就绪", "默认操作",
    "达成业务目标", "完成操作", "提升效率"
]
```

**垃圾词密度计算**：
```python
JunkDensity = count(黑名单词) * 5 / total_words
# 赋予垃圾词5倍权重

if JunkDensity > 0.2:  # 20%阈值
    触发一级熔断，总分 ≤ 40分
```

#### B. 泛化描述检测（Generic BDD Detection）

**特征模式（Regex）**：
```python
GENERIC_PATTERNS = [
    r"Given 系统.*正常",
    r"Given .*就绪",
    r"When 用户.*操作",
    r"When .*提交.*请求",
    r"Then .*成功",
    r"Then 系统.*完成"
]
```

**检测逻辑**：
- BDD步骤平均长度 < 5字符 → 无效步骤
- 命中特征模式 → 泛化描述
- 无效步骤占比 > 30% → 扣除25分（规格具体性）

#### C. 空验收标准检测

**规则**：
```python
if len(acceptance_criteria) == 0:
    AC_Score = 0  # 验证覆盖度得0分

if acceptance_criteria in ["无", "略", "同上", "待补充"]:
    AC_Score = 0  # 等同于空

if "待定" in acceptance_criteria or "TBD" in acceptance_criteria:
    AC_Score *= 0.3  # 扣除70%
```

---

### 3. 质量分级标准

| 等级 | 分数区间 | 描述 | 关键特征 |
|------|----------|------|----------|
| **A+** | 97-100 | 完美 | 内容详实，无占位符，BDD可测性极高 |
| **A** | 90-96 | 优秀 | 逻辑严密，极少量非核心缺失，无泛化 |
| **B** | 80-89 | 合格 | 结构完整，核心清晰，可能有个别模糊 |
| **C** | 70-79 | 需改进 | 少量占位符(<10%)，部分AC不具体 |
| **D** | 60-69 | 不可用 | 明显模板痕迹，大量"待定"，逻辑断层 |
| **F** | < 60 | 垃圾 | **全篇模板、空AC、全是占位符** |

**对比V4标准**：
- V4的B级（80-89）→ V5的C级（70-79）
- V4的85分（问题文档）→ V5的32.5分（F级）✅

---

### 4. 实施优先级

#### P0: 止血（立即实施）
**任务**: 实现 `PlaceholderValidator`
**目标**: 检测到"待定"、"XX"超过阈值，直接F级
**文件**: `rules/content_quality.py`（新建）
**估时**: 2小时

#### P1: 提质（本周内）
**任务**: 实现 `GenericStepDetector` 和 `EmptyACValidator`
**目标**: 识别泛化BDD步骤和空验收标准
**文件**: `rules/content_quality.py`, `analyzer_v5.py`
**估时**: 4小时

#### P2: 优选（下一迭代）
**任务**: NLP语义分析或LLM辅助评分
**目标**: 判断用户故事的业务价值
**文件**: `analyzer_v5_llm.py`
**估时**: 8小时

---

## 实施计划

### Phase 1: P0实施（立即）

#### 1.1 创建内容质量检查模块
```python
# rules/content_quality.py
class PlaceholderValidator:
    BLOCKLIST = [...]  # 见上文

    def validate(self, spec_model):
        junk_density = self._calculate_junk_density(spec_model)
        if junk_density > 0.2:
            return ValidationResult(
                passed=False,
                score=0,
                message="严重质量问题：文档包含大量占位符或未完成内容",
                severity="CRITICAL"
            )
```

#### 1.2 集成到Analyzer
```python
# analyzer_v5.py
class QualityAnalyzerV5:
    def analyze_substance(self, spec_model):
        validator = PlaceholderValidator()
        result = validator.validate(spec_model)

        if not result.passed:
            # 一级熔断
            return -100  # 标记触发熔断
```

### Phase 2: P1实施（本周）

#### 2.1 泛化检测
```python
class GenericStepDetector:
    GENERIC_PATTERNS = [...]  # 见上文

    def detect_generic_bdd(self, scenarios):
        invalid_steps = 0
        total_steps = 0

        for scenario in scenarios:
            for step in scenario.steps:
                if self._is_generic(step):
                    invalid_steps += 1
                total_steps += 1

        return invalid_steps / total_steps
```

#### 2.2 验收标准检查
```python
class EmptyACValidator:
    def validate_acceptance_criteria(self, stories):
        empty_count = 0

        for story in stories:
            if not story.acceptance_criteria:
                empty_count += 1
            elif story.acceptance_criteria in ["无", "略", "待补充"]:
                empty_count += 1

        return empty_count / len(stories)
```

### Phase 3: 集成测试

#### 3.1 使用问题文档测试
输入：当前B级（85分）的问题文档
预期输出：F级（30-40分）

#### 3.2 使用高质量文档测试
输入：真实的高质量规格文档
预期输出：A级（90+分）

---

## 预期效果

### 对问题文档的评分

**输入**（当前案例）：
- 用户故事：12个模板化描述
- 验收标准：全部为空
- BDD场景：13个generic场景
- 占位符密度：45%

**V4评分**：85分（B级）❌
**V5评分**：32.5分（F级）✅

**报告消息**：
```
质量等级: F (32.5/100)

严重质量问题：
- 文档包含大量占位符或未完成内容（占位符密度45%）
- 验收标准缺失：12个用户故事中12个缺少验收标准
- BDD场景过于泛化：13个场景中11个为模板化描述

建议：
1. 重新运行01-spec-explorer（不使用--no-interactive）
2. 补充具体的验收标准
3. 细化BDD场景，增加具体的Given/When/Then步骤
```

---

## 成功标准

### 算法验收标准
- ✅ 问题文档（占位符多、空AC）评分 < 60分（F级）
- ✅ 高质量文档（无占位符、完整AC）评分 ≥ 90分（A级）
- ✅ 评分报告包含具体的质量问题和改进建议
- ✅ 熔断机制正确触发

### A+验收标准（Gemini验收）
- ✅ 评分算法权重合理（内容质量60%）
- ✅ 检测规则覆盖主要质量问题
- ✅ 误判率 < 5%
- ✅ 代码质量符合Clean Code原则

---

## 文件清单

### 新建文件
- `rules/content_quality.py` - 内容质量检查模块
- `analyzer_v5.py` - V5质量分析器

### 修改文件
- `specflow_v4.py` - 集成V5分析器
- `models_v2.py` - 增加验证结果模型

### 测试文件
- `tests/test_quality_analyzer_v5.py` - V5分析器单元测试
- `tests/test_content_quality.py` - 内容质量检查测试

---

**设计完成时间**: 2025-12-21 02:40
**设计者**: Claude + Gemini
**预计实施时间**: 6小时（P0+P1）
**目标质量**: A+ (95+/100)
