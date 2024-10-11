# -*- coding: utf-8 -*-
"""
@File    :   resnet18.py
@Time    :   2024/10/11 19:10:47
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch
import torch.nn as nn
from torchvision.models import resnet18
import os
import sys
import time
import json

# import wandb
# import numpy as np


def get_model(args):
    return resnet18(num_classes=args.num_classes)


def get_criterion(args):
    return nn.CrossEntropyLoss()


def get_optimizer(args, model):
    return torch.optim.SGD(model.parameters(), lr=args.lr)


def get_scheduler(args, optimizer):
    return torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=args.step_size, gamma=args.gamma
    )
