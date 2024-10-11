# -*- coding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2024/10/12 01:06:59
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   自动导入trainers包中的所有模块（除了basic）
"""

import os
import importlib
from .basic import BasicTrainer

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 遍历当前目录中的所有.py文件
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != '__init__.py' and filename != 'basic.py':
        module_name = filename[:-3]  # 去掉.py后缀
        module = importlib.import_module(f'.{module_name}', package=__name__)
        
        # 将模块中的所有内容导入到当前命名空间
        for attr_name in dir(module):
            if not attr_name.startswith('_'):  # 排除私有属性
                globals()[attr_name] = getattr(module, attr_name)

# 清理不需要的变量
del os, importlib, current_dir, filename, module_name, module, attr_name

