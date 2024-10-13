# -*- coding: utf-8 -*-
"""
@File    :   train.py
@Time    :   2024/10/11 22:37:55
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch

from components.epochs.basic_epoch import BasicEpoch
from core import logger, save_manager
from utils import AverageMeter

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


class TrainEpoch(BasicEpoch):
    def __init__(self, name, loader, trainer, color="blue", bar=True):
        super().__init__(
            name=name, loader=loader, trainer=trainer, color=color, bar=bar
        )

    def epoch(self):
        self.model.train()

        loss_meter = AverageMeter()
        correct_meter = AverageMeter()

        # iterate the loader
        for inputs, targets, addition in self.loader:
            inputs, targets = inputs.to(self.device), targets.to(self.device)

            # forward
            outputs, _ = self.model(inputs)
            loss = self.criterion(outputs, targets)

            # update the total loss
            loss_meter.update(loss.item(), targets.size(0))

            # update the total correct and total samples
            _, predicted = torch.max(outputs, 1)
            correct_meter.update((predicted == targets).sum().item())

            # backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        # calculate the average loss and accuracy
        avg_loss = loss_meter.item()
        avg_accuracy = correct_meter.item()

        return {"train_loss": avg_loss, "train_accuracy": avg_accuracy}

    def after_epoch(self, result: dict):
        print(f"Epoch {self.epoch_count} result: {result}")
        save_manager.log_metrics(result, step=self.epoch_count)
