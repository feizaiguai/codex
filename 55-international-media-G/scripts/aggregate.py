#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
国外社媒资讯聚合器 - 快速执行脚本

快速调用handler.py执行聚合分析
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import main

if __name__ == "__main__":
    main()
