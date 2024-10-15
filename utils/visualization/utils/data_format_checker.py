# -*- coding: utf-8 -*-
"""
@File    :   data_format_checker.py
@Time    :   2024/10/15 18:19:59
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""


# decorator
from functools import wraps

def data_format_checker(func):
    @wraps(func)
    def wrapper(self, data: dict):
        data_format = self.data_format  # 从实例中获取 data_format

        # 检查 data 是否为字典
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")

        # 检查 data 的键是否符合预期
        for key in data.keys():
            if key not in data_format.keys():
                raise ValueError(
                    f"data[{key}] is not in data_format, {func.__name__} should have keys: {list(data_format.keys())}"
                )

        # 检查 data 的值是否符合预期类型
        for key, value in data.items():
            expected_type = data_format[key]
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"data[{key}] must be {expected_type}, but got {type(value)}"
                )
        return func(self, data)
    return wrapper
