#!/usr/bin/env python3
"""
百度热搜快速查询脚本

Usage:
    python scripts/baidu_trending.py
    python scripts/baidu_trending.py --limit 5
    python scripts/baidu_trending.py --keyword "AI"
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import main

if __name__ == '__main__':
    main()
