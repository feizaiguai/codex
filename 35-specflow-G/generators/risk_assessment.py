"""
风险评估生成器
负责生成 06-风险评估.md
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, ComplexityLevel


class RiskAssessmentGenerator(BaseGenerator):
    """风险评估生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成风险评估文档

        context 必需字段:
            - complexity: ComplexityLevel
            - validation_issues: List (可选)
        """
        # 1. 提取数据
        complexity: ComplexityLevel = context['complexity']
        validation_issues: List = context.get('validation_issues', [])

        # 2. 识别风险
        risks = self._identify_risks(complexity, validation_issues)

        # 3. 准备模板数据
        template_data = {
            'complexity': complexity.value,
            'risk_count': len(risks),
            'risks': risks,
        }

        # 4. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('risk_assessment.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 5. 创建Document对象
        return Document(
            type=DocumentType.RISK_ASSESSMENT,
            title="风险评估",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=15000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 风险概览
        parts.append(f"## 风险概览\n\n")
        parts.append(f"**项目复杂度**: {data['complexity']}\n")
        parts.append(f"**识别风险数**: {data['risk_count']}\n\n")
        parts.append("本文档列出了项目的主要风险及应对措施.\n\n")

        # 风险列表
        parts.append(f"## 风险列表\n\n")
        for risk in data['risks']:
            parts.append(f"### {risk['id']}: {risk['name']}\n\n")
            parts.append(f"- **严重程度**: {risk['severity']}\n")
            parts.append(f"- **可能性**: {risk['probability']}\n")
            parts.append(f"- **影响**: {risk['impact']}\n")
            parts.append(f"- **应对措施**: {risk['mitigation']}\n\n")

        # 缓解计划
        parts.append(self._get_mitigation_plan())

        # RAID分析
        parts.append(self._get_raid_analysis())

        return "".join(parts)

    def _identify_risks(self, complexity: ComplexityLevel, validation_issues: List) -> List[Dict[str, str]]:
        """识别风险(基于复杂度和验证问题)"""
        risks = []

        # 基于复杂度的默认风险
        if complexity.value in ["复杂", "非常复杂"]:
            risks.extend([
                {
                    "id": "RISK-001",
                    "name": "技术复杂度风险",
                    "severity": "High",
                    "probability": "Medium",
                    "impact": "系统架构复杂,集成难度大",
                    "mitigation": "提前进行技术验证,分阶段实施"
                },
                {
                    "id": "RISK-002",
                    "name": "团队技能风险",
                    "severity": "Medium",
                    "probability": "Medium",
                    "impact": "团队需要学习新技术栈",
                    "mitigation": "提供技术培训,安排技术预研"
                }
            ])

        # 通用风险
        risks.extend([
            {
                "id": "RISK-003",
                "name": "需求变更风险",
                "severity": "Medium",
                "probability": "High",
                "impact": "需求变更导致进度延期",
                "mitigation": "采用敏捷开发,快速迭代"
            },
            {
                "id": "RISK-004",
                "name": "第三方依赖风险",
                "severity": "Medium",
                "probability": "Low",
                "impact": "第三方服务不稳定",
                "mitigation": "准备备选方案,签订SLA协议"
            }
        ])

        # 如果有验证问题,添加质量风险
        if len(validation_issues) > 5:
            risks.append({
                "id": "RISK-005",
                "name": "需求质量风险",
                "severity": "High",
                "probability": "High",
                "impact": f"发现{len(validation_issues)}个需求问题",
                "mitigation": "优先修复Critical和High级别问题"
            })

        return risks

    def _get_mitigation_plan(self) -> str:
        """获取缓解计划章节"""
        return """## 风险缓解计划

1. **定期风险评审**: 每周评估风险状态
2. **技术预研**: 对高风险技术进行预研
3. **备份方案**: 为关键决策准备备选方案
4. **早期验证**: 在项目早期验证关键技术可行性
5. **持续监控**: 建立风险监控机制,及时发现新风险

"""

    def _get_raid_analysis(self) -> str:
        """获取RAID分析章节"""
        return """## RAID分析(风险,假设,问题,依赖)

### Risks(风险)
- **技术风险**: 新技术栈学习曲线,性能瓶颈
- **进度风险**: 需求变更,人员流动
- **业务风险**: 市场变化,竞争压力

### Assumptions(假设)
- **技术假设**: 选定的技术栈能满足性能要求
- **资源假设**: 团队具备必要的技能
- **业务假设**: 用户需求保持相对稳定

### Issues(问题)
- **当前问题**: 需及时解决的阻塞问题
- **潜在问题**: 可能出现的问题及预防措施

### Dependencies(依赖)
- **内部依赖**: 团队间协作,资源分配
- **外部依赖**: 第三方服务,硬件设备
- **技术依赖**: 特定技术栈,开源库

### 应对策略
| 类型 | 优先级 | 应对措施 | 责任人 |
|------|--------|---------|--------|
| 技术风险 | High | 提前技术验证 | 技术负责人 |
| 进度风险 | High | 敏捷迭代,快速反馈 | 项目经理 |
| 外部依赖 | Medium | 备选方案,SLA协议 | 架构师 |
"""
