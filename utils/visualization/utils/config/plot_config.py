# -*- coding: utf-8 -*-
"""
@File    :   plot_config.py
@Time    :   2024/10/14 15:43:45
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""


import yaml

# import matplotlib.pyplot as plt
import seaborn as sns
import os

# 初始化配置变量
# CONFIG_PLT: dict | None = None
CONFIG_SNS: dict | None = None
__is_loaded: bool = False


def load_config(sns_config_path=None):  # plt_config_path=None,
    # global CONFIG_PLT, CONFIG_SNS
    global CONFIG_SNS
    # if CONFIG_PLT is None:
    #     if plt_config_path is None:
    #         plt_config_path = os.path.join(
    #             os.path.dirname(__file__), "config", "plot_config_plt.yaml"
    #         )
    #     with open(plt_config_path, "r") as f:
    #         CONFIG_PLT = yaml.safe_load(f)
    if CONFIG_SNS is None:
        if sns_config_path is None:
            sns_config_path = os.path.join(
                os.path.dirname(__file__), "plot_config_sns.yaml"
            )
        with open(sns_config_path, "r", encoding="utf-8") as f:
            CONFIG_SNS = yaml.safe_load(f)
    apply_config()


def apply_config():
    # 应用 Matplotlib 配置
    # plt_rcParams = CONFIG_PLT.get("rcParams", {})
    # for key, value in plt_rcParams.items():
    #     plt.rcParams[key] = value

    # # 如果需要设置颜色，可以在这里处理
    # plt_colors = CONFIG_PLT.get("colors", {})
    # if plt_colors:
    #     plt.rcParams["axes.facecolor"] = plt_colors.get("background", "#FFFFFF")
    #     plt.rcParams["grid.color"] = plt_colors.get("grid", "#E5E5E5")
    #     plt.rcParams["axes.edgecolor"] = plt_colors.get("axis", "#333333")
    #     # 其他颜色配置...

    # 应用 Seaborn 配置
    sns_context = CONFIG_SNS.get("context", "notebook")
    sns_style = CONFIG_SNS.get("style", "darkgrid")
    sns_palette = CONFIG_SNS.get("palette", "deep")

    sns.set_context(sns_context)
    sns.set_style(sns_style)
    sns.set_palette(sns_palette)

    # 如果需要设置颜色，可以在这里处理
    sns_colors = CONFIG_SNS.get("colors", {})
    if sns_colors:
        # 自定义调色板
        custom_palette = sns_colors.get("lines", [])
        if custom_palette:
            sns.set_palette(custom_palette)
        # 设置其他颜色...


if not __is_loaded:
    load_config()
    print(f"default visualization config: plot_config_sns.yaml loaded")
    # print(CONFIG_SNS)
    __is_loaded = True
