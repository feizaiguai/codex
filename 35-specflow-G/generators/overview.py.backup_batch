"""
项目概览生成器
负责生成 00-项目概览.md
"""
from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from generators.base import BaseGenerator
from core.models import Document, DocumentType, QualityReport


class OverviewGenerator(BaseGenerator):
    """项目概览生成器"""

    def generate(self, context: Dict[str, Any]) -> Document:
        """
        生成项目概览文档

        context 必需字段:
            - project_name: str
            - project_version: str
            - task_description: str
            - quality_report: QualityReport
        """
        # 1. 提取数据
        project_name = context['project_name']
        project_version = context['project_version']
        task_description = context['task_description']
        quality_report: QualityReport = context['quality_report']

        # 2. 准备模板数据
        template_data = {
            'project_name': project_name,
            'project_version': project_version,
            'domain': quality_report.domain.value,
            'complexity': quality_report.complexity.value,
            'estimated_hours': quality_report.estimated_hours,
            'estimated_days': round(quality_report.estimated_hours / 8, 1),
            'task_description': task_description,
            'overall_grade': quality_report.metrics.overall_grade.value,
        }

        # 3. 尝试使用模板渲染,否则降级到老方法
        markdown = ""
        try:
            markdown = self.render_template('overview.md.j2', template_data)
        except Exception as e:
            print(f"  模板渲染失败,使用内置生成: {e}")
            markdown = self._generate_builtin(template_data)

        # 如果模板渲染结果为空,使用内置生成
        if not markdown or markdown.strip() == "":
            markdown = self._generate_builtin(template_data)

        # 4. 创建Document对象
        return Document(
            type=DocumentType.OVERVIEW,
            title=f"{project_name} - 项目概览",
            version=project_version,
            content=template_data,
            markdown=markdown,
            token_budget=15000
        )

    def _generate_builtin(self, data: Dict[str, Any]) -> str:
        """内置生成逻辑(向后兼容)"""
        return f"""## 执行摘要

**项目名称**: {data['project_name']}
**版本**: {data['project_version']}
**领域**: {data['domain']}
**复杂度**: {data['complexity']}
**估算工时**: {data['estimated_hours']}小时
**预估工期**: {data['estimated_days']}工作日(按每天8小时计算)

本项目旨在{data['task_description']}.

**质量等级**: {data['overall_grade']}

## 愿景声明

通过{data['project_name']},我们致力于为用户提供高质量的解决方案,提升业务效率,创造商业价值.

### 核心价值主张
- **用户价值**: 显著提升用户体验和工作效率
- **业务价值**: 降低运营成本,提高业务响应速度
- **技术价值**: 构建可扩展,易维护的技术架构

## 业务背景

**业务领域**: {data['domain']}

本项目面向{data['domain']}领域,致力于解决该领域的核心业务问题.

### 当前挑战
- 业务流程效率有待提升
- 系统集成度不足
- 数据利用率较低

### 解决方案
通过本项目的实施,将有效解决上述挑战,为业务发展提供坚实的技术支撑.

## 成功指标(关键假设)

### 业务指标
- **用户满意度**: 目标 ≥ 4.5/5.0
- **业务转化率**: 提升 20%+
- **运营成本**: 降低 15%+

### 技术指标
- **系统可用性**: ≥ 99.9%
- **响应时间**: P95 < 500ms
- **错误率**: < 0.1%

### 关键假设
- 用户接受新系统的学习曲线
- 现有数据可以平滑迁移
- 第三方服务稳定可靠

## 利益相关者

| 角色 | 关注点 | 期望 | 参与方式 |
|------|-------|------|---------|
| 最终用户 | 易用性,性能 | 高效完成任务 | 用户测试,反馈 |
| 业务负责人 | ROI,上市时间 | 快速交付价值 | 需求评审,验收 |
| 技术团队 | 可维护性,扩展性 | 稳定可靠的系统 | 开发,运维 |
| 产品经理 | 功能完整性,用户体验 | 符合产品规划 | 需求定义,优先级 |
| 运维团队 | 稳定性,监控 | 易于运维 | 部署,监控 |
"""
