# -*- coding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2024/10/14 16:17:20
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""


import plot_config

try:
	from .difficulty_accuracy_hist import plot_sample_difficulty
except ImportError as e:
	print(f"Error importing module: {e}")


