#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hacker News趋势分析器 - 快速执行脚本

快速调用handler.py获取HN热门故事
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import main

if __name__ == "__main__":
    main()
