# -*- coding: utf-8 -*-
"""
@File    :   datasets.py
@Time    :   2024/10/11 19:17:07
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   数据集标准接口
"""

import torch
import os
import sys
import time
import json
#import wandb
#import numpy as np


class Dataset(torch.utils.data.Dataset):
    def __init__(self, args):
        pass

    def __len__(self):
        pass

    def __getitem__(self, index):
        pass
