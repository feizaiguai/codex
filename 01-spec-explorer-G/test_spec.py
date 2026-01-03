#!/usr/bin/env python3
"""
SpecExplorer 测试套件
测试所有核心功能和边缘案例
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import os
from pathlib import Path

from core.models import RequirementContext, ImpactModel, FlowModel, DomainModel
from modelers import impact, flow, domain
from generators import gherkin, design_doc, json_generator
from handler import SpecExplorerHandler


class TestRequirementContext(unittest.TestCase):
    """测试需求上下文模型"""

    def test_create_context(self):
        """测试创建上下文"""
        context = RequirementContext(
            core_problem="解决支付问题",
            target_users=["商家", "消费者"],
            value_proposition="快速安全支付",
            technical_challenges=["高并发", "安全性"],
            mvp_scope=["扫码支付", "订单管理"]
        )

        self.assertEqual(context.core_problem, "解决支付问题")
        self.assertEqual(len(context.target_users), 2)
        self.assertEqual(len(context.technical_challenges), 2)

    def test_empty_context(self):
        """测试空上下文"""
        context = RequirementContext(
            core_problem="",
            target_users=[],
            value_proposition="",
            technical_challenges=[],
            mvp_scope=[]
        )

        # 应该能创建，即使是空的
        self.assertIsNotNone(context)


class TestImpactAnalyzer(unittest.TestCase):
    """测试影响力分析器"""

    def test_analyze_impact(self):
        """测试影响力分析"""
        context = RequirementContext(
            core_problem="提升用户留存率",
            target_users=["新用户", "老用户"],
            value_proposition="个性化推荐提升体验",
            technical_challenges=["冷启动", "实时推荐"],
            mvp_scope=["基础推荐", "用户画像"]
        )

        impact_model = impact.analyze_impact(context)

        self.assertIsNotNone(impact_model.business_goal)
        self.assertIsInstance(impact_model.key_actors, list)
        self.assertGreater(len(impact_model.key_actors), 0)
        self.assertIsInstance(impact_model.impacts, list)
        self.assertIsInstance(impact_model.deliverables, list)

    def test_impact_with_minimal_context(self):
        """测试最小上下文的影响分析"""
        context = RequirementContext(
            core_problem="构建博客系统",
            target_users=["博主"],
            value_proposition="简单易用",
            technical_challenges=[],
            mvp_scope=[]
        )

        impact_model = impact.analyze_impact(context)

        # 即使输入最少，也应该有输出
        self.assertIsNotNone(impact_model.business_goal)
        self.assertGreater(len(impact_model.key_actors), 0)


class TestFlowAnalyzer(unittest.TestCase):
    """测试流程分析器"""

    def test_analyze_flow(self):
        """测试流程分析"""
        context = RequirementContext(
            core_problem="订单管理",
            target_users=["用户", "商家"],
            value_proposition="高效订单处理",
            technical_challenges=[],
            mvp_scope=["下单", "支付", "发货"]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)

        self.assertIsInstance(flow_model.events, list)
        self.assertGreater(len(flow_model.events), 0)
        self.assertIsInstance(flow_model.user_stories, list)
        self.assertGreater(len(flow_model.user_stories), 0)
        self.assertIsInstance(flow_model.journey_stages, list)

    def test_flow_events_generation(self):
        """测试事件生成"""
        context = RequirementContext(
            core_problem="用户注册流程",
            target_users=["新用户"],
            value_proposition="快速注册",
            technical_challenges=[],
            mvp_scope=["注册", "验证", "激活"]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)

        # 应该生成多个事件
        self.assertGreaterEqual(len(flow_model.events), 3)


class TestDomainAnalyzer(unittest.TestCase):
    """测试领域分析器"""

    def test_analyze_domain(self):
        """测试领域分析"""
        context = RequirementContext(
            core_problem="电商系统",
            target_users=["买家", "卖家"],
            value_proposition="便捷交易",
            technical_challenges=[],
            mvp_scope=["商品", "订单", "支付"]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        self.assertIsInstance(domain_model.entities, list)
        self.assertGreater(len(domain_model.entities), 0)
        self.assertIsInstance(domain_model.value_objects, list)
        self.assertIsInstance(domain_model.aggregates, list)
        self.assertIsInstance(domain_model.bounded_contexts, list)

    def test_domain_entity_extraction(self):
        """测试实体提取"""
        context = RequirementContext(
            core_problem="图书管理系统",
            target_users=["读者", "管理员"],
            value_proposition="方便管理",
            technical_challenges=[],
            mvp_scope=["图书", "借阅", "归还"]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        # 应该提取到核心实体
        entity_names = [e.lower() for e in domain_model.entities]
        # 至少应该有一些实体
        self.assertGreaterEqual(len(entity_names), 2)


class TestBDDGenerator(unittest.TestCase):
    """测试BDD生成器"""

    def test_generate_bdd_scenarios(self):
        """测试生成BDD场景"""
        flow_model = FlowModel(
            events=['用户注册', '邮箱验证', '账户激活'],
            user_stories=['作为用户我想注册账号', '作为用户我想验证邮箱'],
            journey_stages=['注册', '验证', '激活']
        )

        domain_model = DomainModel(
            entities=['User', 'Email', 'Account'],
            value_objects=['EmailAddress', 'Password'],
            aggregates=['User'],
            bounded_contexts=['用户管理']
        )

        scenarios = gherkin.generate_bdd_scenarios(flow_model, domain_model)

        self.assertIsInstance(scenarios, list)
        self.assertGreater(len(scenarios), 0)

        # 验证场景结构
        for scenario in scenarios:
            self.assertIn('feature', scenario)
            self.assertIn('scenario', scenario)
            self.assertIn('steps', scenario)
            self.assertGreater(len(scenario['steps']), 0)

    def test_generate_acceptance_criteria(self):
        """测试生成验收标准"""
        flow_model = FlowModel(
            events=['订单创建', '支付完成'],
            user_stories=['作为用户我想下单', '作为用户我想支付'],
            journey_stages=['下单', '支付']
        )

        criteria = gherkin.generate_acceptance_criteria(flow_model)

        self.assertIsInstance(criteria, list)
        self.assertGreater(len(criteria), 0)


class TestDesignDocGenerator(unittest.TestCase):
    """测试设计文档生成器"""

    def test_generate_design_doc(self):
        """测试生成设计文档"""
        context = RequirementContext(
            core_problem="项目管理系统",
            target_users=["项目经理", "开发者"],
            value_proposition="高效协作",
            technical_challenges=["实时同步"],
            mvp_scope=["任务管理", "进度跟踪"]
        )

        impact_model = ImpactModel(
            business_goal="提升团队效率",
            key_actors=["项目经理", "开发者"],
            impacts=["提高协作效率"],
            deliverables=["任务管理模块"]
        )

        flow_model = FlowModel(
            events=['任务创建', '任务分配'],
            user_stories=['作为PM我想创建任务'],
            journey_stages=['创建', '分配', '执行']
        )

        domain_model = DomainModel(
            entities=['Task', 'User', 'Project'],
            value_objects=['TaskStatus'],
            aggregates=['Project'],
            bounded_contexts=['任务管理', '用户管理']
        )

        scenarios = [
            {
                'feature': '任务管理',
                'scenario': '创建任务',
                'steps': ['Given 用户已登录', 'When 创建任务', 'Then 任务创建成功']
            }
        ]

        doc_content = design_doc.generate(
            context=context,
            impact=impact_model,
            flow=flow_model,
            domain=domain_model,
            scenarios=scenarios
        )

        # 验证文档包含关键章节
        self.assertIn('需求概览', doc_content)
        self.assertIn('Impact Mapping', doc_content)
        self.assertIn('Flow Modeling', doc_content)
        self.assertIn('Domain Modeling', doc_content)
        self.assertIn('BDD', doc_content)


class TestJSONGenerator(unittest.TestCase):
    """测试JSON生成器"""

    def test_generate_json(self):
        """测试生成JSON"""
        context = RequirementContext(
            core_problem="测试项目",
            target_users=["用户"],
            value_proposition="测试",
            technical_challenges=[],
            mvp_scope=["功能1"]
        )

        impact_model = ImpactModel(
            business_goal="目标",
            key_actors=["角色"],
            impacts=["影响"],
            deliverables=["交付"]
        )

        flow_model = FlowModel(
            events=['事件1'],
            user_stories=['故事1'],
            journey_stages=['阶段1']
        )

        domain_model = DomainModel(
            entities=['Entity1'],
            value_objects=['VO1'],
            aggregates=['Agg1'],
            bounded_contexts=['Context1']
        )

        scenarios = [
            {
                'feature': 'Feature1',
                'scenario': 'Scenario1',
                'steps': ['Step1']
            }
        ]

        json_data = json_generator.generate_json(
            project_name="测试项目",
            context=context,
            impact=impact_model,
            flow=flow_model,
            domain=domain_model,
            scenarios=scenarios
        )

        # 验证JSON结构
        self.assertIn('project_name', json_data)
        self.assertIn('entities', json_data)
        self.assertIn('features', json_data)
        self.assertIn('contexts', json_data)


class TestHandler(unittest.TestCase):
    """测试Handler功能"""

    def setUp(self):
        """测试前置准备"""
        self.handler = SpecExplorerHandler()

    def test_analyze_impact(self):
        """测试影响力分析"""
        result = self.handler.analyze_impact(
            "构建在线教育平台",
            output_format='json'
        )

        self.assertIsInstance(result, dict)
        self.assertIn('business_goal', result)
        self.assertIn('key_actors', result)

    def test_analyze_flow(self):
        """测试流程分析"""
        result = self.handler.analyze_flow(
            "用户注册流程",
            output_format='json'
        )

        self.assertIsInstance(result, dict)
        self.assertIn('events', result)
        self.assertIn('user_stories', result)

    def test_analyze_domain(self):
        """测试领域分析"""
        result = self.handler.analyze_domain(
            "订单管理系统",
            output_format='json'
        )

        self.assertIsInstance(result, dict)
        self.assertIn('entities', result)
        self.assertIn('bounded_contexts', result)

    def test_generate_bdd(self):
        """测试生成BDD"""
        result = self.handler.generate_bdd(
            "支付流程",
            output_format='json'
        )

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


class TestEdgeCases(unittest.TestCase):
    """测试边缘案例"""

    def test_empty_description(self):
        """测试空描述"""
        context = RequirementContext(
            core_problem="",
            target_users=[],
            value_proposition="",
            technical_challenges=[],
            mvp_scope=[]
        )

        # 应该不会抛出异常
        impact_model = impact.analyze_impact(context)
        self.assertIsNotNone(impact_model)

    def test_very_long_description(self):
        """测试超长描述"""
        long_text = "A" * 10000

        context = RequirementContext(
            core_problem=long_text,
            target_users=["用户"],
            value_proposition="测试",
            technical_challenges=[],
            mvp_scope=[]
        )

        # 应该能处理
        impact_model = impact.analyze_impact(context)
        self.assertIsNotNone(impact_model)

    def test_special_characters(self):
        """测试特殊字符"""
        context = RequirementContext(
            core_problem="测试@#$%^&*()",
            target_users=["用户-123", "Admin/Root"],
            value_proposition="Test & Verify",
            technical_challenges=["问题1?", "问题2!"],
            mvp_scope=["功能/模块", "API:接口"]
        )

        # 应该正常处理
        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        self.assertIsNotNone(domain_model)

    def test_duplicate_items(self):
        """测试重复项"""
        context = RequirementContext(
            core_problem="测试",
            target_users=["用户", "用户", "管理员"],
            value_proposition="测试",
            technical_challenges=["挑战1", "挑战1"],
            mvp_scope=["功能1", "功能1", "功能2"]
        )

        impact_model = impact.analyze_impact(context)
        # 应该能处理重复
        self.assertIsNotNone(impact_model)

    def test_chinese_and_english_mixed(self):
        """测试中英文混合"""
        context = RequirementContext(
            core_problem="Build一个智能AI系统for数据分析",
            target_users=["Data Scientist", "业务分析师"],
            value_proposition="提供real-time insights",
            technical_challenges=["Big Data处理", "Machine Learning模型"],
            mvp_scope=["数据可视化Dashboard", "预测模型Training"]
        )

        impact_model = impact.analyze_impact(context)
        flow_model = flow.analyze_flow(context, impact_model)
        domain_model = domain.analyze_domain(context, flow_model)

        # 应该能处理中英文混合
        self.assertIsNotNone(domain_model.entities)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestRequirementContext))
    suite.addTests(loader.loadTestsFromTestCase(TestImpactAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestFlowAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestDomainAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestBDDGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDesignDocGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 返回结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
