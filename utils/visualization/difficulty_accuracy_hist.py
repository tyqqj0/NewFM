# -*- coding: utf-8 -*-
"""
@File    :   difficulty-accuracy-hist.py
@Time    :   2024/10/14 13:56:51
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import numpy as np
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from PIL import Image

from . import plot_config

def plot_sample_difficulty(
    values,
    labels,
    epoch,
    weights=None,
    mode="hist",
    prefix="",
):
    """
    绘制样本难度与伪标签准确率，样本难度与分布密度关系的图。

    参数：
        values (array-like): 一维数组或张量，表示样本难度的值。
        labels (array-like): 一维数组或张量，表示样本的类别标签或伪标签准确率。
        epoch (int): 当前的 epoch 数。
        weights (array-like, 可选): 一维数组或张量，表示每个样本的权重。
        mode (str): 绘图模式，'hist' 或 'prob'。
        prefix (str): 图像标题前缀。

    返回：
        PIL.Image.Image: 绘制的图像对象。
        dict: 包含绘图数据的字典（仅在 'prob' 模式下返回）。
    """
    # 确保输入数据是 NumPy 数组
    if isinstance(values, torch.Tensor):
        values = values.cpu().numpy()
    else:
        values = np.array(values)

    if isinstance(labels, torch.Tensor):
        labels = labels.cpu().numpy()
    else:
        labels = np.array(labels)

    if weights is not None:
        if isinstance(weights, torch.Tensor):
            weights = weights.cpu().numpy()
        else:
            weights = np.array(weights)

    if mode == "prob":
        fig, data_dict = plot_accuracy_vs_difficulty(values, labels, weights, prefix)
    else:
        fig = plot_distribution_by_class(values, labels, epoch, prefix)

    # 将绘图转换为 PIL 图像
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image = Image.open(buf)
    plt.close(fig)  # 关闭图像以释放内存

    if mode == "prob":
        return image, data_dict
    else:
        return image


def plot_accuracy_vs_difficulty(values, labels, weights, prefix):
    """
    绘制样本难度与伪标签准确率的关系图。

    参数：
        values (array-like): 样本难度值。
        labels (array-like): 伪标签准确率（0或1）。
        weights (array-like): 样本权重，可为 None。
        prefix (str): 图像标题前缀。

    返回：
        matplotlib.figure.Figure: 绘制的图形对象。
        dict: 包含绘图数据的字典。
    """
    n_bins = 25
    bin_edges = np.linspace(np.min(values), np.max(values), n_bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    correct_rates = []
    densities = []
    avg_weights = []

    # 计算每个 bin 的密度和平均权重
    for i in range(n_bins):
        in_bin = (values >= bin_edges[i]) & (values < bin_edges[i + 1])
        bin_count = np.sum(in_bin)
        densities.append(bin_count / len(values))
        if weights is not None:
            avg_weights.append(np.mean(weights[in_bin]) if bin_count > 0 else np.nan)

        if bin_count > 0:
            correct_rate = np.mean(labels[in_bin])
        else:
            correct_rate = np.nan
        correct_rates.append(correct_rate)

    # 绘图
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(bin_centers, correct_rates, "o-", color="b", label="Accuracy")
    ax1.set_xlabel("Difficulty")
    ax1.set_ylabel("Accuracy", color="b")
    ax1.tick_params(axis="y", labelcolor="b")
    ax1.grid(True)

    ax2.bar(
        bin_centers,
        densities,
        width=bin_edges[1] - bin_edges[0],
        alpha=0.3,
        color="r",
        label="Density",
    )
    ax2.set_ylabel("Density", color="r")
    ax2.tick_params(axis="y", labelcolor="r")

    if weights is not None and len(avg_weights) > 0:
        ax2.bar(
            bin_centers,
            avg_weights,
            width=bin_edges[1] - bin_edges[0],
            alpha=0.3,
            color="g",
            label="Weight",
        )

    plt.title(f"{prefix} Accuracy vs Difficulty")
    fig.tight_layout()

    # 准备数据字典
    data_dict = {
        "bin_centers": bin_centers,
        "densities": densities,
        "correct_rates": correct_rates,
    }
    if weights is not None:
        data_dict["avg_weights"] = avg_weights

    return fig, data_dict


def plot_distribution_by_class(values, labels, epoch, prefix):
    """
    绘制不同类别的样本难度分布直方图。

    参数：
        values (array-like): 样本难度值。
        labels (array-like): 样本的类别标签。
        epoch (int): 当前的 epoch 数。
        prefix (str): 图像标题前缀。

    返回：
        matplotlib.figure.Figure: 绘制的图形对象。
    """
    plt.figure(figsize=(10, 6))
    unique_classes = np.unique(labels)

    for cls in unique_classes:
        class_mask = labels == cls
        class_values = values[class_mask]
        sns.histplot(
            class_values,
            bins=25,
            kde=True,
            label=f"Class {cls}",
            log_scale=(False, True),
        )

    plt.title(f"{prefix} Distribution by Class at Epoch {epoch}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    fig = plt.gcf()  # 获取当前图形对象
    return fig