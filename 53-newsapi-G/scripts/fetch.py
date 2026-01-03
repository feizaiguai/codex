#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewsAPI全球科技新闻分析器 - 快速执行脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import main

if __name__ == "__main__":
    main()
