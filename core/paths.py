# -*- CODING: UTF-8 -*-
# @time 2024/9/11 16:19
# @Author tyqqj
# @File paths.py
# @
# @Aim

import os
import sys

# 获取 core 目录的父目录，即项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 其他目录
CORE_DIR = os.path.join(PROJECT_ROOT, "core")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")

# 将项目根目录添加到 Python 路径
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
