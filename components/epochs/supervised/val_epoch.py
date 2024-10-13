# -*- coding: utf-8 -*-
"""
@File    :   val.py
@Time    :   2024/10/11 23:44:25
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

from core import logger, save_manager
from utils import AverageMeter
from components.epochs.basic_epoch import BasicEpoch


class ValEpoch(BasicEpoch):
    def __init__(self, name, loader, trainer, color="yellow", bar=True):
        super().__init__(
            name=name, loader=loader, trainer=trainer, color=color, bar=bar
        )

    def epoch(self) -> dict:
        self.model.eval()

        loss_meter = AverageMeter()
        correct_meter = AverageMeter()

        with torch.no_grad():
            for inputs, targets, addition in self.loader:
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)

                outputs, _ = self.model(inputs)

                loss = self.criterion(outputs, targets)
                loss_meter.update(loss.item(), inputs.size(0))

                preds = outputs.argmax(dim=1)
                correct_meter.update(
                    torch.sum(preds == targets).item() / inputs.size(0)
                )

        result = {
            "val_loss": loss_meter.item(),
            "val_accuracy": correct_meter.item(),
        }
        return result

    def after_epoch(self, result: dict):
        print(f"Epoch {self.epoch_count} result: {result}")
        save_manager.log_metrics(result, step=self.epoch_count)
