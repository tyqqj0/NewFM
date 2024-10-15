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
def data_format_checker(data_format: dict):
    def decorator(func):
        def wrapper(data: dict):
            # check data format
            if not isinstance(data, dict):
                raise ValueError("data must be a dictionary")

            # check data keys
            for key in data.keys():
                if key not in data_format.keys():
                    raise ValueError(
                        f"data[{key}] is not in data_format, {func.__name__} should have keys: {data_format.keys()}"
                    )

            # check data values
            for key, value in data.items():
                if not isinstance(value, data_format[key]):
                    raise ValueError(
                        f"data[{key}] must be {data_format[key]}, but got {type(value)}"
                    )
            return func(data)

        return wrapper

    return decorator
