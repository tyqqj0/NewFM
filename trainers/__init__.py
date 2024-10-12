# -*- coding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2024/10/12 01:06:59
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   自动导入trainers包中的所有模块（除了basic），并提供工厂函数获取trainer类
"""

import os
import importlib
from typing import Optional
from .basic import BasicTrainer

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建一个字典，用于存储trainer名称到类的映射
trainer_dict = {}

# 遍历当前目录中的所有.py文件
for filename in os.listdir(current_dir):
    if (
        filename.endswith(".py")
        and filename != "__init__.py"
        and filename != "basic.py"
    ):
        module_name = filename[:-3]  # 去掉.py后缀
        module = importlib.import_module(f".{module_name}", package=__name__)

        # 将模块中的所有内容导入到当前命名空间
        for attr_name in dir(module):
            if not attr_name.startswith("_"):  # 排除私有属性
                attr = getattr(module, attr_name)
                globals()[attr_name] = attr
                # 如果属性是继承自BasicTrainer的类，则添加到trainer_dict
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BasicTrainer)
                    and attr is not BasicTrainer
                ):
                    trainer_dict[attr_name] = attr


# 定义工厂函数，根据名称返回对应的trainer类
def get_trainer_class(trainer_name) -> Optional[BasicTrainer]:
    # if end with .py
    if trainer_name.endswith(".py"):
        trainer_name = trainer_name[:-3]
    trainer = trainer_dict.get(trainer_name, None)
    if trainer is None:
        print(
            f"Trainer '{trainer_name}' not found. Available trainers are: {', '.join(trainer_dict.keys())}"
        )
    return trainer


# 清理不需要的变量
del os, importlib, current_dir, filename, module_name, module, attr_name, attr
