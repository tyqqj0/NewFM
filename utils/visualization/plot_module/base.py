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
import warnings
from PIL import Image
import numpy as np
import seaborn as sns
from ..utils.data_format_checker import data_format_checker
import io
import matplotlib.pyplot as plt


class BaseVisualization(ABC):
    data_format: dict = None

    def __init__(self, custom_config: dict | str = None):
        if not hasattr(self, "data_format") or self.data_format is None:
            raise ValueError("data_format must be defined in subclass")
        else:
            # print(self.data_format)
            pass

        # 应用自定义配置
        if custom_config is not None:
            self.config = custom_config
            self.apply_custom_config()
        else:
            self.config = {}

    def apply_custom_config(self):
        """
        应用自定义的 Seaborn 配置
        """
        # 如果 custom_config 是文件路径（字符串），则加载配置文件
        if isinstance(self.config, str):
            import yaml

            with open(self.config, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
        elif isinstance(self.config, dict):
            config = self.config
        else:
            raise TypeError("custom_config must be a dict or a path to a YAML file")

        key_list = [
            "context",
            "style",
            "palette",
            "font",
            "font_scale",
            "color_codes",
            "rc",
        ]
        config_sns = {key: config[key] for key in key_list if key in config}

        # 应用 Seaborn 配置
        sns.set_theme(**config_sns)

    @abstractmethod
    def generate_plot(self, data: dict) -> Image.Image | str:
        pass

    def convert_to_Image(self, plt_obj) -> Image.Image:
        """
        将 Matplotlib 的绘图对象转换为 PIL Image
        """
        buf = io.BytesIO()
        plt_obj.savefig(buf, format="png")
        buf.seek(0)
        image = Image.open(buf)
        plt.close()
        return image

    def convert_to_svg(self, plt_obj: plt.Figure) -> str:
        """
        将 Matplotlib 的 Figure 对象转换为 SVG 格式的字符串
        """
        if not isinstance(plt_obj, plt.Figure):
            try:
                plt_obj = plt_obj.gcf()
            except:
                raise ValueError("plt_obj must be a Matplotlib Figure object")
        buf = io.StringIO()
        plt_obj.savefig(buf, format="svg")
        svg_data = buf.getvalue()
        buf.close()
        plt.close(plt_obj)
        return svg_data

    @data_format_checker
    def __generate_plot(self, data: dict) -> Image.Image | str:
        # check data values
        image = self.generate_plot(data)
        # first try to convert to svg
        # print(type(image))
        if image is plt:
            try:
                warnings.warn("image is a plt module, please use plt.gcf()")
                image = self.convert_to_svg(plt.gcf())
            except:
                pass
        if isinstance(image, (plt.Figure, plt.Axes)):
            image = self.convert_to_svg(image)
        else:
            try:
                image = self.convert_to_Image(image)
            except:
                pass
        if not isinstance(image, (Image.Image, np.ndarray, str)):
            raise ValueError(
                "image must be a PIL.Image.Image or numpy.ndarray or svg_string"
            )
        return image

    def get_plt(self, data: dict) -> plt.Figure:
        """
        获取当前的 Matplotlib 绘图对象
        """
        image = self.generate_plot(data)
        if isinstance(image, plt.Figure):
            return image
        elif image is plt:
            return plt.gcf()
        else:
            raise ValueError("image must be a Matplotlib Figure object")

    def plot(self, data: dict) -> Image.Image | str:
        image = self.__generate_plot(data)
        return image

    def __call__(self, data) -> Image.Image | str:
        return self.__generate_plot(data)
