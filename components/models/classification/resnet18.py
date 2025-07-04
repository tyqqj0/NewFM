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
# import time
# import json
# import wandb
# import numpy as np

__all__ = ["ResNet18", "get_criterion", "get_optimizer", "get_scheduler"]


class ResNet18(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.inside_model = resnet18(num_classes=num_classes)

    def forward(self, x):
        # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        # return the output before fc and the final output
        x = self.inside_model.conv1(x)
        x = self.inside_model.bn1(x)
        x = self.inside_model.relu(x)
        x = self.inside_model.maxpool(x)
        x = self.inside_model.layer1(x)
        x = self.inside_model.layer2(x)
        x = self.inside_model.layer3(x)
        x = self.inside_model.layer4(x)
        x = self.inside_model.avgpool(x)
        x = torch.flatten(x, 1)
        before_fc = x
        x = self.inside_model.fc(x)
        return x, {"feature": before_fc}


def get_model(args):
    return ResNet18(num_classes=args.num_classes)


def get_criterion(args):
    return nn.CrossEntropyLoss()


def get_optimizer(args, model):
    return torch.optim.SGD(
        model.parameters(),
        lr=args.lr,
        momentum=args.momentum,
        weight_decay=args.weight_decay,
    )


def get_scheduler(args, optimizer):
    return torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=args.step_size, gamma=args.gamma
    )
