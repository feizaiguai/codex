#!/usr/bin/env python3
"""
YouTube Analyzer 测试套件
测试所有核心功能和边缘案例
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

from youtube_analyzer import (
    YouTubeAPI, VideoAnalyzer, ChannelAnalyzer,
    extract_video_id, extract_channel_id,
    Alert
)
from handler import YouTubeAnalyzerHandler


class TestURLExtraction(unittest.TestCase):
    """测试URL提取功能"""

    def test_extract_video_id_from_watch_url(self):
        """测试从watch URL提取视频ID"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_from_short_url(self):
        """测试从短链接提取视频ID"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_from_embed_url(self):
        """测试从embed URL提取视频ID"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_from_plain_id(self):
        """测试直接视频ID"""
        video_id = "dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(video_id), "dQw4w9WgXcQ")

    def test_extract_video_id_invalid(self):
        """测试无效URL"""
        url = "https://www.google.com"
        self.assertIsNone(extract_video_id(url))

    def test_extract_channel_id_from_channel_url(self):
        """测试从channel URL提取频道ID"""
        url = "https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ"
        self.assertEqual(extract_channel_id(url), "UCBJycsmduvYEL83R_U4JriQ")

    def test_extract_channel_id_from_c_url(self):
        """测试从/c/ URL提取"""
        url = "https://www.youtube.com/c/GoogleDevelopers"
        self.assertEqual(extract_channel_id(url), "GoogleDevelopers")

    def test_extract_channel_id_invalid(self):
        """测试无效频道URL"""
        url = "https://www.youtube.com/watch?v=abc"
        self.assertIsNone(extract_channel_id(url))


class TestVideoAnalyzer(unittest.TestCase):
    """测试视频分析器"""

    def setUp(self):
        """测试前置准备"""
        self.mock_api = Mock(spec=YouTubeAPI)
        self.analyzer = VideoAnalyzer(self.mock_api)

    def test_analyze_video_basic(self):
        """测试基础视频分析"""
        # Mock API响应
        self.mock_api.get_video_details.return_value = {
            'snippet': {
                'title': '测试视频',
                'description': '测试描述',
                'channelId': 'UC123',
                'channelTitle': '测试频道',
                'publishedAt': '2024-01-01T00:00:00Z',
                'tags': ['test', 'video'],
                'categoryId': '22'
            },
            'statistics': {
                'viewCount': '10000',
                'likeCount': '500',
                'commentCount': '100',
                'favoriteCount': '0'
            },
            'contentDetails': {
                'duration': 'PT10M30S'
            }
        }

        result = self.analyzer.analyze_video('test_id', fetch_comments=False)

        # 验证结果结构
        self.assertIn('video', result)
        self.assertIn('statistics', result)
        self.assertIn('engagement', result)

        # 验证视频信息
        self.assertEqual(result['video']['title'], '测试视频')
        self.assertEqual(result['video']['channel_title'], '测试频道')

        # 验证统计数据
        self.assertEqual(result['statistics']['view_count'], 10000)
        self.assertEqual(result['statistics']['like_count'], 500)

    def test_calculate_engagement_metrics(self):
        """测试参与度计算"""
        # 高参与度
        engagement = self.analyzer._calculate_engagement(10000, 600, 50)
        self.assertGreater(engagement['engagement_score'], 7)
        self.assertEqual(engagement['rating'], '优秀')

        # 中等参与度
        engagement = self.analyzer._calculate_engagement(10000, 300, 20)
        self.assertGreater(engagement['engagement_score'], 4)
        self.assertLess(engagement['engagement_score'], 7)

        # 低参与度
        engagement = self.analyzer._calculate_engagement(10000, 50, 5)
        self.assertLess(engagement['engagement_score'], 4)

        # 零观看
        engagement = self.analyzer._calculate_engagement(0, 0, 0)
        self.assertEqual(engagement['engagement_score'], 0)
        self.assertEqual(engagement['rating'], 'N/A')

    def test_analyze_comments(self):
        """测试评论分析"""
        mock_comments = [
            {
                'snippet': {
                    'topLevelComment': {
                        'snippet': {
                            'textDisplay': 'Great video! Very helpful',
                            'authorDisplayName': 'User1',
                            'likeCount': 10,
                            'publishedAt': '2024-01-01T00:00:00Z'
                        }
                    }
                }
            },
            {
                'snippet': {
                    'topLevelComment': {
                        'snippet': {
                            'textDisplay': 'Not good at all',
                            'authorDisplayName': 'User2',
                            'likeCount': 2,
                            'publishedAt': '2024-01-01T00:00:00Z'
                        }
                    }
                }
            }
        ]

        result = self.analyzer._analyze_comments(mock_comments)

        self.assertEqual(result['total'], 2)
        self.assertEqual(result['analyzed'], 2)
        self.assertIn('sentiment', result)
        self.assertIn('positive', result['sentiment']['counts'])

    def test_sentiment_analysis(self):
        """测试情感分析"""
        # 正面评论
        sentiment = self.analyzer._simple_sentiment_analysis("Great video! Love it!")
        self.assertEqual(sentiment, 'positive')

        # 负面评论
        sentiment = self.analyzer._simple_sentiment_analysis("Terrible and awful")
        self.assertEqual(sentiment, 'negative')

        # 中性评论
        sentiment = self.analyzer._simple_sentiment_analysis("This is a video")
        self.assertEqual(sentiment, 'neutral')

        # 中文正面
        sentiment = self.analyzer._simple_sentiment_analysis("讲得太好了！很棒！")
        self.assertEqual(sentiment, 'positive')

    def test_format_duration(self):
        """测试时长格式化"""
        # 短视频
        self.assertEqual(self.analyzer._format_duration('PT5M30S'), '5:30')

        # 长视频
        self.assertEqual(self.analyzer._format_duration('PT1H23M45S'), '1:23:45')

        # 只有秒
        self.assertEqual(self.analyzer._format_duration('PT45S'), '0:45')

        # 无效格式
        invalid = self.analyzer._format_duration('INVALID')
        self.assertEqual(invalid, 'INVALID')


class TestChannelAnalyzer(unittest.TestCase):
    """测试频道分析器"""

    def setUp(self):
        """测试前置准备"""
        self.mock_api = Mock(spec=YouTubeAPI)
        self.analyzer = ChannelAnalyzer(self.mock_api)

    def test_analyze_channel(self):
        """测试频道分析"""
        self.mock_api.get_channel_details.return_value = {
            'snippet': {
                'title': '测试频道',
                'description': '测试描述',
                'customUrl': '@testchannel',
                'publishedAt': '2020-01-01T00:00:00Z',
                'country': 'CN'
            },
            'statistics': {
                'subscriberCount': '100000',
                'videoCount': '200',
                'viewCount': '5000000'
            }
        }

        result = self.analyzer.analyze_channel('UC123')

        # 验证结果
        self.assertIn('channel', result)
        self.assertIn('statistics', result)
        self.assertEqual(result['channel']['title'], '测试频道')
        self.assertEqual(result['statistics']['subscriber_count'], 100000)
        self.assertEqual(result['statistics']['video_count'], 200)

        # 验证平均观看数计算
        avg_views = result['statistics']['avg_views_per_video']
        self.assertEqual(avg_views, 5000000 // 200)


class TestYouTubeAPI(unittest.TestCase):
    """测试YouTube API客户端"""

    def setUp(self):
        """测试前置准备"""
        self.api = YouTubeAPI('test_api_key')

    @patch('urllib.request.urlopen')
    def test_make_request_success(self, mock_urlopen):
        """测试成功的API请求"""
        # Mock响应
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"items": []}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        result = self.api._make_request('videos', {'id': 'test'})

        self.assertEqual(result, {'items': []})
        mock_urlopen.assert_called_once()

    @patch('urllib.request.urlopen')
    def test_make_request_http_error(self, mock_urlopen):
        """测试HTTP错误"""
        import urllib.error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            'url', 404, 'Not Found', {}, None
        )

        with self.assertRaises(Exception) as context:
            self.api._make_request('videos', {'id': 'test'})

        self.assertIn('API请求失败', str(context.exception))


class TestHandler(unittest.TestCase):
    """测试Handler功能"""

    def setUp(self):
        """测试前置准备"""
        self.mock_api = Mock(spec=YouTubeAPI)
        self.handler = YouTubeAnalyzerHandler.__new__(YouTubeAnalyzerHandler)
        self.handler.api = self.mock_api
        self.handler.video_analyzer = VideoAnalyzer(self.mock_api)
        self.handler.channel_analyzer = ChannelAnalyzer(self.mock_api)

    def test_compare_videos_validation(self):
        """测试视频对比验证"""
        # 少于2个视频
        with self.assertRaises(ValueError):
            self.handler.compare_videos(['url1'])

        # 超过5个视频
        with self.assertRaises(ValueError):
            self.handler.compare_videos(['url' + str(i) for i in range(10)])

    def test_find_best_performing(self):
        """测试找出最佳表现视频"""
        metrics = [
            {
                'title': 'Video 1',
                'views': 1000,
                'likes': 50,
                'engagement_score': 7.5
            },
            {
                'title': 'Video 2',
                'views': 2000,
                'likes': 150,
                'engagement_score': 8.5
            },
            {
                'title': 'Video 3',
                'views': 1500,
                'likes': 100,
                'engagement_score': 6.0
            }
        ]

        best = self.handler._find_best_performing(metrics)

        self.assertEqual(best['views'], 'Video 2')
        self.assertEqual(best['likes'], 'Video 2')
        self.assertEqual(best['engagement'], 'Video 2')


class TestEdgeCases(unittest.TestCase):
    """测试边缘案例"""

    def test_empty_comments(self):
        """测试空评论列表"""
        mock_api = Mock(spec=YouTubeAPI)
        analyzer = VideoAnalyzer(mock_api)

        result = analyzer._analyze_comments([])

        self.assertEqual(result['total'], 0)
        self.assertEqual(result['analyzed'], 0)
        self.assertEqual(len(result['top_comments']), 0)

    def test_missing_optional_fields(self):
        """测试缺失可选字段"""
        mock_api = Mock(spec=YouTubeAPI)
        mock_api.get_video_details.return_value = {
            'snippet': {
                'title': '测试',
                'description': '描述',
                'channelId': 'UC123',
                'channelTitle': '频道',
                'publishedAt': '2024-01-01T00:00:00Z'
                # 缺少tags和categoryId
            },
            'statistics': {
                'viewCount': '1000',
                'likeCount': '50'
                # 缺少commentCount
            },
            'contentDetails': {
                'duration': 'PT5M'
            }
        }

        analyzer = VideoAnalyzer(mock_api)
        result = analyzer.analyze_video('test_id')

        # 应该有默认值
        self.assertEqual(result['video']['tags'], [])
        self.assertEqual(result['statistics']['comment_count'], 0)

    def test_very_long_title(self):
        """测试超长标题"""
        mock_api = Mock(spec=YouTubeAPI)
        analyzer = VideoAnalyzer(mock_api)

        long_title = "A" * 1000
        mock_api.get_video_details.return_value = {
            'snippet': {
                'title': long_title,
                'description': '描述',
                'channelId': 'UC123',
                'channelTitle': '频道',
                'publishedAt': '2024-01-01T00:00:00Z'
            },
            'statistics': {
                'viewCount': '1000',
                'likeCount': '50',
                'commentCount': '10'
            },
            'contentDetails': {
                'duration': 'PT5M'
            }
        }

        result = analyzer.analyze_video('test_id')
        # 不应该抛出异常
        self.assertEqual(result['video']['title'], long_title)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestURLExtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestVideoAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestChannelAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestYouTubeAPI))
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
