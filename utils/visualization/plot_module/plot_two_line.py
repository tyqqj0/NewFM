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
        "before": list,
        "after": list,
    }

    def __init__(self, custom_config: dict | str = None):
        super().__init__(custom_config)

    def generate_plot(self, data: dict, m_value: int):
        """
        生成绘图对象

        :param data: 数据字典，包含 'before' 和 'after' 两个键
        :param m_value: m 的取值，用于标题和图例
        :return: Figure 对象
        """
        # 将数据转换为 DataFrame
        df = pd.DataFrame(
            {
                "Epoch": list(range(len(data["before"]))),
                "Before": data["before"],
                "After": data["after"],
            }
        )

        # 设置图形大小
        figsize = self.config.get("figsize", (8, 6))
        plt.figure(figsize=figsize)

        # 设置调色板
        palette = sns.color_palette(self.config.get("palette", "deep"))
        color = palette[0] if m_value == 1 else palette[1]

        # 设置背景颜色
        plt.rcParams["axes.facecolor"] = COLOR_SCHEME["background"]
        # 设置y轴范围
        plt.ylim(0, 1)

        # 设置绘图区域大小

        # 绘制 "Before" 曲线
        sns.lineplot(
            data=df,
            x="Epoch",
            y="Before",
            label=f"Accuracy Before Correction when m={m_value}",
            linestyle="-",
            color=color,
        )

        # 绘制 "After" 曲线
        sns.lineplot(
            data=df,
            x="Epoch",
            y="After",
            label=f"Accuracy After Correction when m={m_value}",
            linestyle="--",
            color=color,
        )

        # 填充曲线之间的区域
        plt.fill_between(
            df["Epoch"],
            df["Before"],
            df["After"],
            color=color,
            alpha=0.2,
        )

        # 设置刻度字体大小
        # plt.xticks(fontsize=12)
        # plt.yticks(fontsize=12)

        # 设置标签和标题
        plt.xlabel("Epoch Number")
        plt.ylabel("Average Accuracy of Filtered Noisy Labels")
        plt.title(
            f"Accuracy Before and After Correction (m={m_value})",
            color=COLOR_SCHEME["title"],
            fontsize=15,
        )
        plt.legend(loc="best")

        # 调整布局，防止轴标签被裁剪
        plt.tight_layout()

        # 返回绘图对象
        fig = plt.gcf()
        return fig


if __name__ == "__main__":
    # 数据
    data_m3 = {
        "before": [
            0.05,
            0.14,
            0.21,
            0.25,
            0.245,
            0.29,
            0.33,
            0.32,
            0.34,
            0.345,
            0.36,
        ],
        "after": [
            0.89,
            0.75,
            0.62,
            0.52,
            0.45,
            0.43,
            0.428,
            0.426,
            0.425,
            0.421,
            0.42,
        ],
    }

    data_m1 = {
        "before": [
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
        "after": [
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

    import seaborn as sns

    COLOR_SCHEME = {
        "accuracy": "#ff7f0e",
        "distribution": "#1f77b4",
        "background": "#f2f2f2",
        "title": "#333333",
    }  # 橙色  # 蓝色

    # 创建sns的色板
    palette = sns.color_palette(
        [
            COLOR_SCHEME["accuracy"],
            COLOR_SCHEME["distribution"],
            COLOR_SCHEME["background"],
            COLOR_SCHEME["title"],
        ]
    )

    # 初始化绘图对象
    plotter = PlotTwoLine({"palette": palette, "figsize": (5, 4)})

    # 生成 m=3 的图
    fig_m3 = plotter.generate_plot(data=data_m3, m_value=3)
    fig_m3.savefig("plot_m3.svg", format="svg")
    fig_m3.savefig("plot_m3.png", format="png")

    # 清空当前图，以防止重叠
    plt.clf()

    # 生成 m=1 的图
    fig_m1 = plotter.generate_plot(data=data_m1, m_value=1)
    fig_m1.savefig("plot_m1.svg", format="svg")
    fig_m1.savefig("plot_m1.png", format="png")
    # 关闭所有图形，释放内存
    plt.close("all")
