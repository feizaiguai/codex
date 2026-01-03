#!/usr/bin/env python3
"""
Architecture Designer 测试套件
测试所有核心功能和边缘案例
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import os
from pathlib import Path

from core.models import (
    DesignDraft, ArchitectureDesign, ScaleLevel,
    ScaleAssessment, TechStack, PatternSelection, ADR
)
from analyzers.scale_estimator import ScaleEstimator
from analyzers.tech_recommender import TechStackRecommender
from analyzers.pattern_selector import PatternSelector, ArchitecturePattern
from generators.adr_generator import ADRGenerator
from architecture_designer import ArchitectureDesigner
from handler import ArchitectureHandler


class TestScaleEstimator(unittest.TestCase):
    """测试规模评估器"""

    def setUp(self):
        """测试前置准备"""
        self.estimator = ScaleEstimator()

    def test_estimate_small_project(self):
        """测试小型项目评估"""
        draft = DesignDraft(
            project_name="小型博客",
            entities=['User', 'Post', 'Comment'],
            features=['登录', '发布', '评论'],
            contexts=['用户管理', '内容管理']
        )

        assessment = self.estimator.estimate(draft)

        self.assertEqual(assessment.scale, ScaleLevel.SMALL)
        self.assertLess(assessment.score, 15)

    def test_estimate_medium_project(self):
        """测试中型项目评估"""
        draft = DesignDraft(
            project_name="电商平台",
            entities=['User', 'Product', 'Order', 'Payment', 'Shipping',
                     'Inventory', 'Category', 'Review', 'Cart'],
            features=['用户注册', '商品浏览', '下单', '支付', '物流',
                     '库存管理', '评价', '推荐', '优惠券', '客服'],
            contexts=['用户', '商品', '订单', '支付', '物流', '营销']
        )

        assessment = self.estimator.estimate(draft)

        self.assertEqual(assessment.scale, ScaleLevel.MEDIUM)
        self.assertGreaterEqual(assessment.score, 15)
        self.assertLess(assessment.score, 30)

    def test_estimate_large_project(self):
        """测试大型项目评估"""
        # 创建大量实体
        entities = [f'Entity{i}' for i in range(20)]
        features = [f'Feature{i}' for i in range(25)]
        contexts = [f'Context{i}' for i in range(10)]

        draft = DesignDraft(
            project_name="企业ERP系统",
            entities=entities,
            features=features,
            contexts=contexts
        )

        assessment = self.estimator.estimate(draft)

        self.assertEqual(assessment.scale, ScaleLevel.LARGE)
        self.assertGreaterEqual(assessment.score, 30)

    def test_zero_entities(self):
        """测试零实体"""
        draft = DesignDraft(
            project_name="测试",
            entities=[],
            features=[],
            contexts=[]
        )

        assessment = self.estimator.estimate(draft)

        self.assertEqual(assessment.scale, ScaleLevel.SMALL)
        self.assertEqual(assessment.score, 0)


class TestTechStackRecommender(unittest.TestCase):
    """测试技术栈推荐器"""

    def setUp(self):
        """测试前置准备"""
        self.recommender = TechStackRecommender()

    def test_recommend_for_small_project(self):
        """测试小型项目技术栈推荐"""
        draft = DesignDraft(
            project_name="小项目",
            entities=['User', 'Post'],
            features=['登录', '发布'],
            contexts=['用户']
        )

        assessment = ScaleAssessment(
            scale=ScaleLevel.SMALL,
            score=10,
            complexity_level="低",
            entity_count=2,
            feature_count=2,
            bounded_context_count=1,
            estimated_users=1000
        )

        tech_stack = self.recommender.recommend(draft, assessment)

        # 小型项目应该推荐轻量级技术
        self.assertIsNotNone(tech_stack.backend_language.recommendation)
        self.assertIsNotNone(tech_stack.database.recommendation)
        self.assertGreater(tech_stack.total_score, 0)

    def test_recommend_for_large_project(self):
        """测试大型项目技术栈推荐"""
        draft = DesignDraft(
            project_name="大项目",
            entities=[f'Entity{i}' for i in range(20)],
            features=[f'Feature{i}' for i in range(25)],
            contexts=[f'Context{i}' for i in range(10)]
        )

        assessment = ScaleAssessment(
            scale=ScaleLevel.LARGE,
            score=40,
            complexity_level="高",
            entity_count=20,
            feature_count=25,
            bounded_context_count=10,
            estimated_users=1000000
        )

        tech_stack = self.recommender.recommend(draft, assessment)

        # 大型项目应该推荐企业级技术
        self.assertIsNotNone(tech_stack.backend_language.recommendation)
        self.assertIsNotNone(tech_stack.cache.recommendation)
        self.assertIsNotNone(tech_stack.message_queue.recommendation)


class TestPatternSelector(unittest.TestCase):
    """测试架构模式选择器"""

    def setUp(self):
        """测试前置准备"""
        self.selector = PatternSelector()

    def test_select_monolith_for_small(self):
        """测试小项目选择单体架构"""
        draft = DesignDraft(
            project_name="小项目",
            entities=['User', 'Post'],
            features=['登录', '发布'],
            contexts=['用户']
        )

        assessment = ScaleAssessment(
            scale=ScaleLevel.SMALL,
            score=10,
            complexity_level="低",
            entity_count=2,
            feature_count=2,
            bounded_context_count=1,
            estimated_users=1000
        )

        selection = self.selector.select(draft, assessment)

        self.assertEqual(selection.primary_pattern, ArchitecturePattern.MONOLITH)
        self.assertIsNotNone(selection.rationale)
        self.assertIsNotNone(selection.implementation_guide)

    def test_select_microservices_for_large(self):
        """测试大项目选择微服务架构"""
        draft = DesignDraft(
            project_name="大项目",
            entities=[f'Entity{i}' for i in range(20)],
            features=[f'Feature{i}' for i in range(25)],
            contexts=[f'Context{i}' for i in range(10)]
        )

        assessment = ScaleAssessment(
            scale=ScaleLevel.LARGE,
            score=40,
            complexity_level="高",
            entity_count=20,
            feature_count=25,
            bounded_context_count=10,
            estimated_users=1000000
        )

        selection = self.selector.select(draft, assessment)

        self.assertEqual(selection.primary_pattern, ArchitecturePattern.MICROSERVICES)


class TestADRGenerator(unittest.TestCase):
    """测试ADR生成器"""

    def setUp(self):
        """测试前置准备"""
        self.generator = ADRGenerator()

    def test_generate_adrs(self):
        """测试生成ADR"""
        draft = DesignDraft(
            project_name="测试项目",
            entities=['User', 'Order'],
            features=['登录', '下单'],
            contexts=['用户', '订单']
        )

        assessment = ScaleAssessment(
            scale=ScaleLevel.MEDIUM,
            score=20,
            complexity_level="中",
            entity_count=2,
            feature_count=2,
            bounded_context_count=2,
            estimated_users=10000
        )

        tech_stack = TechStack(
            backend_language=Mock(recommendation='Python', reason='简单易用'),
            frontend_framework=Mock(recommendation='React', reason='流行'),
            database=Mock(recommendation='PostgreSQL', reason='可靠'),
            cache=Mock(recommendation='Redis', reason='高性能'),
            message_queue=Mock(recommendation='RabbitMQ', reason='可靠'),
            api_style=Mock(recommendation='RESTful', reason='标准'),
            deployment=Mock(recommendation='Docker', reason='便捷')
        )

        selection = PatternSelection(
            primary_pattern=ArchitecturePattern.LAYERED,
            supporting_patterns=[],
            rationale='清晰分层',
            implementation_guide='按层组织代码'
        )

        adrs = self.generator.generate(draft, assessment, tech_stack, selection)

        # 应该生成多个ADR
        self.assertGreater(len(adrs), 0)

        # 验证ADR结构
        for adr in adrs:
            self.assertIsNotNone(adr.title)
            self.assertIsNotNone(adr.context)
            self.assertIsNotNone(adr.decision)
            self.assertIsNotNone(adr.consequences)
            self.assertEqual(adr.status, 'Proposed')


class TestArchitectureDesigner(unittest.TestCase):
    """测试架构设计器"""

    def setUp(self):
        """测试前置准备"""
        self.designer = ArchitectureDesigner()

    def test_design_quick(self):
        """测试快速设计"""
        # 创建临时测试文件
        test_json = {
            "project_name": "测试项目",
            "entities": ["User", "Order"],
            "features": ["登录", "下单"],
            "contexts": ["用户", "订单"]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_json, f)
            temp_file = f.name

        try:
            result = self.designer.design_quick(temp_file)

            self.assertIn('project_name', result)
            self.assertIn('scale', result)
            self.assertIn('backend', result)
            self.assertIn('database', result)
            self.assertIn('pattern', result)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestHandler(unittest.TestCase):
    """测试Handler功能"""

    def setUp(self):
        """测试前置准备"""
        self.handler = ArchitectureHandler()

    def test_quick_design_json_input(self):
        """测试JSON输入的快速设计"""
        # 创建临时测试文件
        test_json = {
            "project_name": "测试项目",
            "entities": ["User", "Order", "Product"],
            "features": ["登录", "下单", "支付"],
            "contexts": ["用户", "订单"]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_json, f)
            temp_file = f.name

        try:
            result = self.handler.design_quick(temp_file, output_format='json')

            self.assertIsInstance(result, dict)
            self.assertIn('project_name', result)
            self.assertIn('scale', result)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_estimate_scale(self):
        """测试规模评估"""
        test_json = {
            "project_name": "测试项目",
            "entities": ["User", "Order"],
            "features": ["登录", "下单"],
            "contexts": ["用户"]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_json, f)
            temp_file = f.name

        try:
            result = self.handler.estimate_scale(temp_file, output_format='json')

            self.assertIn('scale', result)
            self.assertIn('score', result)
            self.assertIn('metrics', result)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestEdgeCases(unittest.TestCase):
    """测试边缘案例"""

    def test_empty_project(self):
        """测试空项目"""
        draft = DesignDraft(
            project_name="空项目",
            entities=[],
            features=[],
            contexts=[]
        )

        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        self.assertEqual(assessment.scale, ScaleLevel.SMALL)
        self.assertEqual(assessment.score, 0)

    def test_very_long_project_name(self):
        """测试超长项目名"""
        long_name = "A" * 1000

        draft = DesignDraft(
            project_name=long_name,
            entities=['User'],
            features=['登录'],
            contexts=['用户']
        )

        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        # 不应该抛出异常
        self.assertIsNotNone(assessment)

    def test_duplicate_entities(self):
        """测试重复实体"""
        draft = DesignDraft(
            project_name="测试",
            entities=['User', 'User', 'Order', 'Order'],
            features=['登录'],
            contexts=['用户']
        )

        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        # 应该处理重复
        self.assertIsNotNone(assessment)

    def test_special_characters_in_names(self):
        """测试名称中的特殊字符"""
        draft = DesignDraft(
            project_name="Test-Project_123",
            entities=['User-Account', 'Order_Item'],
            features=['用户/登录', '订单.支付'],
            contexts=['用户&权限']
        )

        estimator = ScaleEstimator()
        assessment = estimator.estimate(draft)

        # 应该正常处理
        self.assertIsNotNone(assessment)

    def test_missing_optional_fields(self):
        """测试缺失可选字段"""
        # 只提供必需字段
        draft = DesignDraft(
            project_name="最小项目",
            entities=['User'],
            features=['登录'],
            contexts=['用户']
        )

        recommender = TechStackRecommender()
        assessment = ScaleAssessment(
            scale=ScaleLevel.SMALL,
            score=5,
            complexity_level="低",
            entity_count=1,
            feature_count=1,
            bounded_context_count=1,
            estimated_users=100
        )

        tech_stack = recommender.recommend(draft, assessment)

        # 应该有默认推荐
        self.assertIsNotNone(tech_stack.backend_language.recommendation)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestScaleEstimator))
    suite.addTests(loader.loadTestsFromTestCase(TestTechStackRecommender))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternSelector))
    suite.addTests(loader.loadTestsFromTestCase(TestADRGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestArchitectureDesigner))
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
