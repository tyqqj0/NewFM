# -*- coding: utf-8 -*-
"""
@File    :   base.py
@Time    :   2024/10/15 14:52:49
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

from abc import ABC, abstractmethod
from PIL import Image
import numpy as np
import seaborn as sns
from ..utils.data_format_checker import data_format_checker


class BaseVisualization(ABC):
    data_format: dict = {}

    def __init__(self, custom_config: dict | str = None):
        if not hasattr(self, "data_format") or not self.data_format:
            raise ValueError("data_format must be defined in subclass")
        
        # 应用自定义配置
        if custom_config is not None:
            self.custom_config = custom_config
            self.apply_custom_config()
        else:
            self.custom_config = {}
    
    def apply_custom_config(self):
        """
        应用自定义的 Seaborn 配置
        """
        # 如果 custom_config 是文件路径（字符串），则加载配置文件
        if isinstance(self.custom_config, str):
            import yaml
            with open(self.custom_config, 'r') as f:
                config = yaml.safe_load(f)
        elif isinstance(self.custom_config, dict):
            config = self.custom_config
        else:
            raise TypeError("custom_config must be a dict or a path to a YAML file")
        
        # 应用 Seaborn 配置
        sns.set_theme(**config)
    
    @abstractmethod
    def generate_plot(self, data: dict) -> Image:
        pass

    @data_format_checker(data_format)
    def __generate_plot(self, data: dict) -> Image:
        # check data values
        image = self.generate_plot(data)
        if not isinstance(image, [Image.Image, np.ndarray]):
            raise ValueError("image must be a PIL.Image.Image or numpy.ndarray")
        return image

    def plot(self, data: dict) -> Image:
        image = self.__generate_plot(data)
        return image
