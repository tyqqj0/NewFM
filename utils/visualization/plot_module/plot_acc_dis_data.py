# -*- coding: utf-8 -*-
"""
@File    :   plot_acc_dis_data.py
@Time    :   2024/10/16 11:21:20
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


class PlotAccDisData(BaseVisualization):
    data_format = {
        "S0.1": list,
        "S0.3": list,
        "S0.5": list,
        "S0.7": list,
    }

    def __init__(self, custom_config: dict | str = None):
        super().__init__(custom_config)

    def generate_plot(self, data: dict):
        """
        生成绘图对象

        :param data: 数据字典，包含 'S0.1', 'S0.3', 'S0.5', 'S0.7' 四个键
        :return: Figure 对象
        """
        # 创建一个 DataFrame，包含数据和对应的标签
        df = pd.DataFrame(
            {
                "S0.1": data["S0.1"],
                "S0.3": data["S0.3"],
                "S0.5": data["S0.5"],
                "S0.7": data["S0.7"],
            }
        )

        # 计算四组数据的平均值和标准差, 并添加到 DataFrame 中
        mean_values = df.mean(axis=1)
        std_values = df.std(axis=1)
        std_upper = mean_values + std_values
        std_lower = mean_values - std_values
        df["mean"] = mean_values
        df["std_upper"] = std_upper
        df["std_lower"] = std_lower

        # 创建一个图形对象
        fig, ax = plt.subplots(figsize=(10, 6))

        palette = self.config.get("palette", "deep")
        print(palette)

        # 绘制四条线
        sns.lineplot(
            data=df,
            x=df.index,
            y="S0.1",
            label="S0.1",
            ax=ax,
            color=palette[0],
        )
        sns.lineplot(
            data=df,
            x=df.index,
            y="S0.3",
            label="S0.3",
            ax=ax,
            color=palette[1],
        )
        sns.lineplot(
            data=df,
            x=df.index,
            y="S0.5",
            label="S0.5",
            ax=ax,
            color=palette[2],
        )
        sns.lineplot(
            data=df,
            x=df.index,
            y="S0.7",
            label="S0.7",
            ax=ax,
            color=palette[3],
        )

        # 绘制标准差区域
        sns.lineplot(
            data=df,
            x=df.index,
            y="mean",
            label="mean",
            ax=ax,
            color=palette[4],
        )
        sns.lineplot(
            data=df,
            x=df.index,
            y="std_upper",
            label="std_upper",
            ax=ax,
            color=palette[4],
        )
        sns.lineplot(
            data=df,
            x=df.index,
            y="std_lower",
            label="std_lower",
            ax=ax,
            color=palette[4],
        )
        ax.fill_between(
            df.index,
            df["std_lower"],
            df["std_upper"],
            color=palette[4],
            alpha=0.3,
        )

        # 设置背景颜色
        ax.set_facecolor(palette[5])

        # 设置y轴范围
        ax.set_ylim(0, 1)

        # 添加图例
        ax.legend()

        # 设置标题和标签
        ax.set_title("Accuracy Distribution")
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Accuracy")

        return fig


#         s0.1        s0.3        s0.7        s0.5
# 0.99624119	0.990226961	0.923302906 0.99
# 0.992941176	0.976686683	0.859280532 0.995
# 0.989740495	0.959031657	0.781078968 0.995
# 0.984331476	0.938702315	0.692041522 0.99
# 0.978477481	0.884083658	0.638981916 0.98
# 0.973275862	0.858428805	0.586770982 0.97
# 0.966992097	0.775258552	0.61221374  0.95
# 0.887418527	0.690599906	0.593706294 0.91
# 0.862290862	0.629817444	0.511125238 0.89
# 0.825064433	0.572005384	0.540364583 0.87
# 0.782712133	0.542840376	0.512091898 0.84
# 0.765855985	0.484502447	0.500863558 0.83
# 0.72847302	0.491638796	0.45912654  0.72
# 0.690728065	0.42	0.43061956  0.65
# 0.649879373	0.343915344	0.413491246 0.5
# 0.583484574	0.328767123	0.401476434 0.41
# 0.578692494	0.264150943	0.367883996 0.27
# 0.50831793	0.192307692	0.318718381 0.405
# 0.498575499	0.25	0.314375      0.25
# 0.404558405	0.272727273	0.262529833 0.247120419
# 0.333333333	0.25	0.247120419 0.25
# 0.266666667	0	0.250401284 0.250401284
# 0.083333333	0	0.214574899 0
# 0	0	0.171052632 0
# 0	0	0.363636364 0


if __name__ == "__main__":
    data = {
        "S0.1": [
            0.99624119,
            0.992941176,
            0.989740495,
            0.984331476,
            0.978477481,
            0.973275862,
            0.966992097,
            0.887418527,
            0.862290862,
            0.825064433,
            0.782712133,
            0.765855985,
            0.72847302,
            0.690728065,
            0.649879373,
            0.583484574,
            0.578692494,
            0.50831793,
            0.498575499,
            0.404558405,
            0.333333333,
            0.266666667,
            0.083333333,
            0,
            0,
        ],
        "S0.3": [
            0.990226961,
            0.976686683,
            0.959031657,
            0.938702315,
            0.884083658,
            0.858428805,
            0.775258552,
            0.690599906,
            0.629817444,
            0.572005384,
            0.542840376,
            0.484502447,
            0.491638796,
            0.42,
            0.343915344,
            0.328767123,
            0.264150943,
            0.192307692,
            0.25,
            0.272727273,
            0.25,
            0,
            0,
            0,
            0,
        ],
        "S0.7": [
            0.923302906,
            0.859280532,
            0.781078968,
            0.692041522,
            0.638981916,
            0.586770982,
            0.61221374,
            0.593706294,
            0.511125238,
            0.540364583,
            0.512091898,
            0.500863558,
            0.45912654,
            0.43061956,
            0.413491246,
            0.401476434,
            0.367883996,
            0.318718381,
            0.314375,
            0.262529833,
            0.247120419,
            0.250401284,
            0.214574899,
            0.171052632,
            0.363636364,
        ],
        "S0.5": [
            0.99,
            0.995,
            0.995,
            0.99,
            0.98,
            0.97,
            0.95,
            0.91,
            0.89,
            0.87,
            0.84,
            0.83,
            0.72,
            0.65,
            0.5,
            0.41,
            0.27,
            0.405,
            0.25,
            0.247120419,
            0.25,
            0.250401284,
            0,
            0,
            0,
        ],
    }
    # for k, v in data.items():
    #     print(k, len(v))

    COLOR_SCHEME = {
        "S0.1": "#ff7f0e",
        "S0.3": "#ffbf5e",
        "S0.5": "#bfbf5e",
        "S0.7": "#1f77b4",
        "mean": "#d9d9d9",
        "background": "#f2f2f2",
        "title": "#333333",
    }  # 橙色  # 蓝色

    palette = sns.color_palette(
        [
            COLOR_SCHEME["S0.1"],
            COLOR_SCHEME["S0.3"],
            COLOR_SCHEME["S0.5"],
            COLOR_SCHEME["S0.7"],
            COLOR_SCHEME["mean"],
            COLOR_SCHEME["background"],
            COLOR_SCHEME["title"],
        ]
    )

    plot = PlotAccDisData({"palette": palette})
    plot.get_plt(data)
    plt.savefig("acc_dis_data.png")
    plt.show()
    plt.close()
