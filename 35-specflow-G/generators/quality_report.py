"""
质量报告生成器
负责生成 07-质量报告.md
"""
from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, QualityReport


class QualityReportGenerator(BaseGenerator):
    """质量报告生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成质量报告文档

        context 必需字段:
            - quality_report: QualityReport
        """
        # 1. 提取数据
        quality_report: QualityReport = context['quality_report']
        metrics = quality_report.metrics

        # 2. 准备模板数据
        template_data = {
            'overall_grade': metrics.overall_grade.value,
            'overall_score': metrics.overall_score,  # V5: 总体得分
            'completeness': metrics.completeness_score,
            'consistency': metrics.consistency_score,
            'atomicity': metrics.atomicity_score,
            'testability': metrics.testability_score,
            'issues_count': len(quality_report.validation_issues),
            'issues': quality_report.validation_issues,
            'recommendations': quality_report.recommendations,
        }

        # 3. 尝试使用模板渲染,否则降级到内置生成
        markdown = ""
        try:
            markdown = self.render_template('quality_report.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 4. 创建Document对象
        return Document(
            type=DocumentType.QUALITY_REPORT,
            title="质量报告",
            version="1.0.0",
            content=template_data,
            markdown=markdown,
            token_budget=15000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容V3)"""
        parts = []

        # 质量摘要
        parts.append(f"## 质量摘要\n\n")
        parts.append(f"**总体等级**: {data['overall_grade']} ({data['overall_score']:.1f}/100)\n")
        parts.append(f"**完整性**: {data['completeness']}/100\n")
        parts.append(f"**一致性**: {data['consistency']}/100\n")
        parts.append(f"**原子性**: {data['atomicity']}/100\n")
        parts.append(f"**可测试性**: {data['testability']}/100\n\n")
        parts.append(f"本规格文档发现{data['issues_count']}个问题.\n\n")

        # 指标详情
        parts.append(f"## 指标详情\n\n")
        parts.append(f"### 完整性({data['completeness']}/100)\n")
        parts.append("评估需求的完整性,确保所有必要信息都已包含.\n\n")
        parts.append(f"### 一致性({data['consistency']}/100)\n")
        parts.append("评估需求间的一致性,避免矛盾和冲突.\n\n")
        parts.append(f"### 原子性({data['atomicity']}/100)\n")
        parts.append("评估需求的原子性,确保每个需求独立且不可再分.\n\n")
        parts.append(f"### 可测试性({data['testability']}/100)\n")
        parts.append("评估需求的可测试性,确保每个需求都可验证.\n\n")

        # 验证问题(V5: validation_issues现在是字符串列表)
        parts.append(f"## 验证问题\n\n")
        if data['issues_count'] > 0:
            parts.append(f"共发现{data['issues_count']}个问题:\n\n")
            for i, issue in enumerate(data['issues'][:10], 1):  # 只显示前10个
                # V5: issue现在是字符串,不再是ValidationIssue对象
                parts.append(f"{i}. {issue}\n\n")
        else:
            parts.append("暂无验证问题\n\n")

        # 改进建议
        parts.append(f"## 改进建议\n\n")
        for i, rec in enumerate(data['recommendations'], 1):
            parts.append(f"{i}. {rec}\n")
        parts.append("\n")

        # 质量度量仪表盘
        parts.append(self._get_quality_dashboard(data))

        return "".join(parts)

    def _get_quality_dashboard(self, data: Dict[str, Any]) -> str:
        """获取质量仪表盘章节"""
        return f"""## 质量度量仪表盘

### 整体质量概览
```
总体得分: {"█" * int(data['overall_score']/10)}{"░" * (10-int(data['overall_score']/10))} {data['overall_score']:.1f}/100
完整性: {"█" * int(data['completeness']/10)}{"░" * (10-int(data['completeness']/10))} {data['completeness']}/100
一致性: {"█" * int(data['consistency']/10)}{"░" * (10-int(data['consistency']/10))} {data['consistency']}/100
原子性: {"█" * int(data['atomicity']/10)}{"░" * (10-int(data['atomicity']/10))} {data['atomicity']}/100
可测性: {"█" * int(data['testability']/10)}{"░" * (10-int(data['testability']/10))} {data['testability']}/100
```

### V5评分公式
**总分 = 内容质量(80%) + 结构完整性(10%) + 逻辑一致性(10%)**
- 内容质量 = 实质度(35%) + 具体性(25%) + 验证度(20%)

### 质量等级解读
- **A+级(97-100分)**: 卓越,Gemini认证
- **A级(90-96分)**: 优秀,可直接进入开发
- **B级(80-89分)**: 良好,少量优化后可用
- **C级(70-79分)**: 合格,需要改进
- **D级(60-69分)**: 不合格,需要重大改进
- **F级(<60分)**: 严重不合格,需要重写

### 当前等级
**{data['overall_grade']}级 ({data['overall_score']:.1f}/100)** - {"卓越,Gemini认证" if data['overall_grade'] == "A+" else "优秀,可直接进入开发" if data['overall_grade'] == "A" else "良好,少量优化后可用" if data['overall_grade'] == "B" else "合格,需要改进" if data['overall_grade'] == "C" else "不合格,需要重大改进" if data['overall_grade'] == "D" else "严重不合格,需要重写"}

### 质量改进路线图
1. **立即处理**: 修复所有Critical和High级别问题
2. **短期优化**: 提升可测试性和一致性
3. **持续改进**: 定期评审和更新需求文档
"""
