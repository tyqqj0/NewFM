# -*- coding: utf-8 -*-
"""
@File    :   Resnet18_CIFAR10_noisy_Supervised .py
@Time    :   2024/10/12 23:40:04
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


from coqpit import Coqpit

# from attr import dataclass
from dataclasses import asdict, dataclass, field

# from ..base.basic import Basic
# from ..base.data import CIFAR10
# from ..base.model import Resnet18
# from ..base.training import Supervised

configs = [
    "base/data/cifar10.py",
    "base/model/resnet18.py",
    "base/training/supervised.py",
]


# import coqpit
# from attr import dataclass


# Define the configuration file for the ResNet18 model on CIFAR10 dataset
# The configuration file is a dictionary that contains the following keys:
# trainer.py: The file that contains the training script
# use_wandb: A boolean that indicates whether to use Weights and Biases for logging
# project: The name of the project, whether to use Weights and Biases for logging
@dataclass
class Config(Coqpit):
    trainer: str = "CIFAR10_noisy_Supervised"
    project_name: str = "Resnet18_CIFAR10_noisy"
    use_wandb: bool = True
    batch_size: int = 128
    lr: float = 0.1
    momentum: float = 0.9
    weight_decay: float = 5e-4
    noise_type: str = "symmetric"
    noise_ratio: float = 0.5
    seed: int = 42


if __name__ == "__main__":
    print(Config())
