# -*- coding: utf-8 -*-
"""
@File    :   average_meter.py
@Time    :   2024/10/11 23:36:26
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch

#import os
#import sys
#import time
#import json
#import wandb
#import numpy as np


class AverageMeter:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
        
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n  # val 为批次平均值，n 为批次样本数量
        self.count += n
        self.avg = self.sum / self.count
        
    def __str__(self):
        return f"Avg: {self.avg:.4f}"
    
    def item(self):
        return self.avg
