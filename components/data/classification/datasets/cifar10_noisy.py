# -*- coding: utf-8 -*-
"""
@File    :   cifar10_noisy.py
@Time    :   2024/10/12 22:31:43
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import numpy as np
import warnings
import torch
from torchvision import datasets, transforms

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


class CIFAR10Dataset_Noisy(datasets.CIFAR10):
    def __init__(
        self,
        root,
        train=True,
        download=True,
        transform=None,
        noise_type=None,
        noise_ratio=None,
        seed=42,
    ):
        super().__init__(root=root, train=train, download=download, transform=transform)
        if not train:
            # set noisy ratio to 0
            noise_ratio = 0
            # warning
            warnings.warn("Noisy ratio is set to 0 for validation set")

        self.noise_type = noise_type
        self.noise_ratio = noise_ratio
        self.seed = seed
        np.random.seed(self.seed)
        self.true_targets = self.targets

        if self.noise_type is not None and self.noise_ratio > 0 and train:
            self.targets = self._add_symmetric_noise(self.true_targets)
        else:
            self.targets = self.true_targets

    def __getitem__(self, index):
        image, target = super().__getitem__(index)
        return image, target, {"index": index, "true_target": self.true_targets[index]}

    def _add_symmetric_noise(self, targets):
        """
        在训练集上添加对称标签噪声
        """
        # 计算需要添加噪声的样本数量
        n_samples = len(targets)
        n_noisy = int(self.noise_ratio * n_samples)

        # 获取所有样本的索引
        indices = np.arange(n_samples)
        # 随机选择要添加噪声的样本索引
        noisy_indices = np.random.choice(indices, size=n_noisy, replace=False)

        # 创建一个新的标签数组
        new_targets = np.array(targets)

        for idx in noisy_indices:
            original_label = new_targets[idx]
            # 生成除原始标签之外的所有可能的标签
            possible_labels = list(range(10))  # CIFAR-10 has 10 classes
            # possible_labels.remove(original_label)
            # 随机选择一个标签作为噪声标签
            noisy_label = np.random.choice(possible_labels)
            new_targets[idx] = noisy_label

        return new_targets.tolist()


def CIFAR10_transform(train=True):
    if train:
        return transforms.Compose(
            [
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                ),
            ]
        )
    else:
        return transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                ),
            ]
        )
