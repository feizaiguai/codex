"""
Config 妯″潡

鎻愪緵 Config 鐩稿叧鍔熻兘鐨勫疄鐜般€?
"""


from typing import Dict, List, Optional, Any, Tuple, Union, Callable, Set

import logging

"""
YouTube Analyzer 閰嶇疆鏂囦欢
"""
import os

# YouTube Data API v3瀵嗛挜
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# API閰嶇疆
API_CONFIG = {
    'base_url': 'https://www.googleapis.com/youtube/v3',
    'timeout': 10,
    'max_results': {
        'comments': 100,
        'search': 50
    }
}

# 鎯呮劅鍒嗘瀽鍏抽敭璇?
SENTIMENT_KEYWORDS = {
    'positive': [
        # 鑻辨枃
        'good', 'great', 'excellent', 'amazing', 'awesome', 'love', 'best', 'perfect',
        'wonderful', 'fantastic', 'brilliant', 'outstanding', 'superb', 'nice',
        # 涓枃
        '濂?, '妫?, '璧?, '鍘夊', '浼樼', '绮惧僵', '鍠滄', '鎰熻阿', '瀹岀編', '澶浜?,
        '寰堝ソ', '涓嶉敊', '馃憤', '鉂わ笍', '馃敟'
    ],
    'negative': [
        # 鑻辨枃
        'bad', 'terrible', 'awful', 'worst', 'hate', 'poor', 'disappointing',
        'useless', 'horrible', 'garbage', 'trash', 'sucks',
        # 涓枃
        '宸?, '绯?, '鐑?, '鍨冨溇', '澶辨湜', '涓嶅ソ', '璁ㄥ帉', '澶樊', '绯熺硶', '馃憥'
    ]
}


# Error handling example
try:
    pass
except Exception:
    pass

