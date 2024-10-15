# -*- coding: utf-8 -*-
"""
@File    :   base.py
@Time    :   2024/10/15 18:07:36
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

from abc import ABC, abstractmethod
from ..utils.data_format_checker import data_format_checker


class BaseDataProcessor(ABC):
    """
    data_format: a dictionary with keys and types
    example:
    data_dict: {"data": np.ndarray, "label": np.ndarray}
    or
    data_dict: {"point_x": list, "point_y": list, "label": list}
    """

    data_format: dict = {}

    def __init__(self):
        # check data format exist and not empty
        if not hasattr(self, "data_format") or not self.data_format:
            raise ValueError("data_format must be defined in subclass")

    @abstractmethod
    def process(self, data: dict, *args, **kwargs):
        pass

    @data_format_checker(data_format)
    def __process(self, data: dict, *args, **kwargs):
        return self.process(data, *args, **kwargs)

    def __call__(self, data: dict, *args, **kwargs):
        return self.__process(data, *args, **kwargs)
