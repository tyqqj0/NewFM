# -*- coding: utf-8 -*-
"""
@File    :   plot_two_line.py
@Time    :   2024/10/15 18:46:31
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

from .base import BaseVisualization
from ..utils.config import plot_config
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class PlotTwoLine(BaseVisualization):
    data_format = {
        "m1_before": list,
        "m1_after": list,
        "m3_before": list,
        "m3_after": list,
    }

    def __init__(self, custom_config: dict | str = None):
        super().__init__(custom_config)

    def generate_plot(self, data: dict):
        # 将数据转换为 DataFrame
        df = pd.DataFrame({
            'Index': list(range(len(data['m1_before']))),
            'm1_before': data['m1_before'],
            'm1_after': data['m1_after'],
            'm3_before': data['m3_before'],
            'm3_after': data['m3_after']],
        })

        # 设置绘图风格
        sns.set_theme(**self.seaborn_config)

        # 设置图形大小
        figsize = self.other_config.get('figsize', (8, 6))
        plt.figure(figsize=figsize)

        # 绘制 m=1 的曲线
        sns.lineplot(
            data=df,
            x='Index',
            y='m1_before',
            label='m=1 Before',
            linestyle='-',
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[0]
        )
        sns.lineplot(
            data=df,
            x='Index',
            y='m1_after',
            label='m=1 After',
            linestyle='--',
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[0]
        )

        # 填充 m=1 曲线之间的区域
        plt.fill_between(
            df['Index'],
            df['m1_before'],
            df['m1_after'],
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[0],
            alpha=0.2
        )

        # 绘制 m=3 的曲线
        sns.lineplot(
            data=df,
            x='Index',
            y='m3_before',
            label='m=3 Before',
            linestyle='-',
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[1]
        )
        sns.lineplot(
            data=df,
            x='Index',
            y='m3_after',
            label='m=3 After',
            linestyle='--',
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[1]
        )

        # 填充 m=3 曲线之间的区域
        plt.fill_between(
            df['Index'],
            df['m3_before'],
            df['m3_after'],
            color=sns.color_palette(self.seaborn_config.get('palette', 'deep'))[1],
            alpha=0.2
        )

        # 设置标签和标题
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Comparison of Before and After for m=1 and m=3')
        plt.legend()

        # 返回绘图对象
        return plt


if __name__ == "__main__":
    data_max_m1 = {
        "m1_before": [
            0.05,
            0.14,
            0.21,
            0.25,
            0.245,
            0.29,
            0.31,
            0.3,
            0.32,
            0.325,
            0.36,
        ],
        "m1_after": [0.89, 0.75, 0.62, 0.52, 0.45, 0.43, 0.425, 0.35, 0.33, 0.33, 0.42],
        "m3_before": [
            0.15,
            0.35,
            0.39,
            0.42,
            0.41,
            0.395,
            0.4,
            0.4,
            0.395,
            0.405,
            0.397,
        ],
        "m3_after": [
            0.65,
            0.45,
            0.42,
            0.42,
            0.39,
            0.4,
            0.395,
            0.41,
            0.395,
            0.41,
            0.402,
        ],
    }
    # figsize: (5, 3), palette: deep
    plot_two_line = PlotTwoLine({"palette": "deep", "figsize": (5, 3)})(data_max_m1)
    plot_two_line.show()
