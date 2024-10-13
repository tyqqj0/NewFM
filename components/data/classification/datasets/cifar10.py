# -*- coding: utf-8 -*-
"""
@File    :   CIFAR10
@Time    :   2024/10/11 19:14:53
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch
from torchvision import datasets, transforms
import os
import sys
import time
import json

# import wandb
# import numpy as np


class CIFAR10Dataset(datasets.CIFAR10):
    def __init__(self, root, train=True, download=True, transform=None):
        super().__init__(root=root, train=train, download=download, transform=transform)

    def __getitem__(self, index):
        image, target = super().__getitem__(index)
        return image, target, {"index": index}


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
